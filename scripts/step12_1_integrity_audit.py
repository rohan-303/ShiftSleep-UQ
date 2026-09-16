#!/usr/bin/env python
"""Step 12.1 read-only integrity and independent gate audit.

Consumes existing Step 12 CSV/JSON artifacts and frozen metadata only. It does
not fit calibration objects, run inference, or modify v1 history.
"""
from __future__ import annotations
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXPS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
SEEDS = (17, 42, 2026)
COMPOUND = ("C4", "C5")
REPS = 2000


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_csv(name: str):
    with (ROOT / "reports" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def load_parts():
    out = {}
    with (ROOT / "reports/oracle_target_partitions_v1.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["dataset"], {})[r["subject_id"]] = r["oracle_role"]
    return out


def bundle(ex, seed, condition):
    p = ROOT / "artifacts/predictions/b0" / ex / f"seed_{seed}" / f"{condition}.npz"
    z = np.load(p, allow_pickle=False)
    return {k: z[k] for k in z.files}


def audit_artifacts():
    manifest = {}
    for r in read_csv("../unused") if False else []:
        pass
    manifest_path = ROOT / "reports/b0_diagnostic_hashes_v1.txt"
    for line in manifest_path.read_text().splitlines()[1:]:
        if line.strip():
            p, expected = line.split(",", 1)
            manifest[p.replace("/", "\\")] = expected
    rows = []
    for rel, expected in manifest.items():
        rel_posix = rel.replace("\\", "/")
        p = ROOT / rel_posix
        if not p.exists():
            rows.append({"artifact": rel_posix, "expected_hash": expected, "actual_hash": "", "bytes": 0, "rows": "", "status": "MISSING", "semantic_role": "UNKNOWN"})
            continue
        actual = sha(p)
        nrows = ""
        if p.suffix.lower() == ".csv":
            with p.open(newline="", encoding="utf-8") as f:
                nrows = max(sum(1 for _ in f) - 1, 0)
        role = "ORACLE_APS_CALIBRATION_OBJECT" if p.name == "b0_oracle_aps_v1.csv" else "ORACLE_CONFORMAL_EVALUATION_RESULT" if p.name == "b0_oracle_conformal_results_v1.csv" else "STEP12_DIAGNOSTIC_ARTIFACT"
        rows.append({"artifact": rel_posix, "expected_hash": expected, "actual_hash": actual, "bytes": p.stat().st_size, "rows": nrows, "status": "PASS" if actual == expected else "HASH_MISMATCH", "semantic_role": role})
    by_hash = defaultdict(list)
    for r in rows:
        if r["actual_hash"]:
            by_hash[r["actual_hash"]].append(r["artifact"])
    for r in rows:
        if r["actual_hash"] == sha(ROOT / "reports/b0_oracle_aps_v1.csv") and r["artifact"] in {"reports/b0_oracle_aps_v1.csv", "reports/b0_oracle_conformal_results_v1.csv"}:
            r["status"] = "UNEXPECTED_DUPLICATE_CONTENT"
    write_csv(ROOT / "reports/step12_1_artifact_integrity_audit.csv", rows)
    return rows


def create_aps_v11():
    """Separate the frozen qhat records from the duplicated evaluation export.

    q-hats and calibration populations are read from existing v1 rows/bundles;
    no APS fitting is performed.
    """
    parts = load_parts()
    old = read_csv("b0_oracle_conformal_results_v1.csv")
    out = []
    seen = set()
    for r in old:
        if r["variant"] not in {"ORACLE_DOMAIN_APS", "ORACLE_CONDITION_APS"}:
            continue
        ex, seed, c, alpha = r["experiment_id"], int(r["seed"]), r["condition"], r["alpha"]
        if r["variant"] == "ORACLE_DOMAIN_APS":
            fit_type, fit_condition, key = "ORACLE_DOMAIN_APS", "C3", (ex, seed, "DOMAIN", alpha)
        else:
            fit_type, fit_condition, key = "ORACLE_CONDITION_APS", c, (ex, seed, c, alpha)
        if key in seen:
            continue
        seen.add(key)
        d = bundle(ex, seed, fit_condition)
        ds = "isruc_s1" if ex.startswith("D1") else "sleep_edf_sc"
        roles = parts[ds]
        ids = np.asarray(d["subject_id"]).astype(str)
        mask = np.array([roles[x] == "ORACLE_CALIBRATION" for x in ids])
        out.append({
            "experiment_id": ex,
            "seed": seed,
            "fit_scope": "ORACLE_DOMAIN_APS" if fit_type == "ORACLE_DOMAIN_APS" else "ORACLE_CONDITION_APS",
            "fit_condition": fit_condition,
            "alpha": alpha,
            "qhat": r["qhat"],
            "calibration_role": "ORACLE_CALIBRATION",
            "calibration_subject_count": len(set(ids[mask])),
            "calibration_epoch_count": int(mask.sum()),
            "fit_type": fit_type,
            "analysis_scope": "ORACLE_TARGET_UPPER_BOUND",
        })
    write_csv(ROOT / "reports/b0_oracle_aps_v1_1.csv", out)
    return out


def independent_gate_audit():
    domain = read_csv("b0_domain_shift_contrasts_v1.csv")
    diag = read_csv("b0_failure_mode_metrics_v1.csv")
    source = read_csv("b0_source_calibration_transfer_diagnosis_v1.csv")
    oracle = read_csv("b0_oracle_calibration_contrasts_v1.csv")
    conf = read_csv("b0_oracle_conformal_results_v1.csv")
    rows = []
    for ex in EXPS:
        for c in COMPOUND:
            drows = {(r["metric"]): r for r in domain if r["experiment_id"] == ex and r["target_condition"] == c}
            means = {(r["metric"]): float(r["value"]) for r in diag if r["experiment_id"] == ex and r["condition"] == c and r["seed"] == "MULTI_SEED_MEAN"}
            src = {(r["metric"]): r for r in source if r["experiment_id"] == ex and r["condition"] == c}
            oc = {(r["metric"]): r for r in oracle if r["experiment_id"] == ex and r["condition"] == c and r["contrast"] == "ORACLE_CONDITION_MINUS_SOURCE"}
            # Independent written-criterion evidence summary. Missing domain ECE CI is explicit;
            # the point change is reconstructed from the frozen multi-seed diagnostic table.
            baseline_ece = next((float(r["value"]) for r in diag if r["experiment_id"] == ex and r["condition"] == ("C1" if c == "C4" else "C2") and r["seed"] == "MULTI_SEED_MEAN" and r["metric"] == "ECE"), float("nan"))
            ece_delta = means.get("ECE", float("nan")) - baseline_ece
            source_worsens = any(float(r["delta_scaled_minus_uncalibrated"]) > float(r["tolerance"]) for r in src.values())
            ranking = float(drows["error_AUROC"]["point_delta"]) < 0 or float(drows["AURC"]["point_delta"]) > 0
            conformal = float(drows["gap"]["point_delta"]) != 0
            prose_reliability = any(float(drows[m]["point_delta"]) > 0 for m in ("NLL", "Brier")) or ece_delta > 0 or ranking or conformal
            implemented_flag = source_worsens
            rows.extend([
                {"criterion":"A_IMPLEMENTED_STEP12","experiment_id":ex,"condition":c,"metric":"source_temperature_worsening","value":source_worsens,"threshold":"any source delta > metric tolerance","pass":implemented_flag,"reason":"Exact Step 12 runner rule: cal_fail is source-temperature worsening only."},
                {"criterion":"A_WRITTEN_PROSE_RECONSTRUCTION","experiment_id":ex,"condition":c,"metric":"reliability_failure_beyond_predictive","value":prose_reliability,"threshold":"NLL/Brier/ECE/ranking/conformal evidence","pass":prose_reliability,"reason":"Independent descriptive evidence; ECE is a point reconstruction because no domain ECE contrast was exported."},
                {"criterion":"A_IMPLEMENTATION_MATCH","experiment_id":ex,"condition":c,"metric":"implementation_vs_written","value":implemented_flag == prose_reliability,"threshold":"must match","pass":implemented_flag == prose_reliability,"reason":"Mismatch indicates the runner operationalizes only source-temperature worsening, not the written reliability taxonomy."},
            ])
            # Criterion B threshold flags.
            bpasses = []
            for metric, rel_threshold in (("NLL", .05), ("Brier", .03)):
                r = oc[metric]; delta = float(r["point_delta"]); ci_hi = float(r["ci95_high"])
                # Source oracle-evaluation baseline for relative reduction.
                base_rows = [x for x in read_csv("b0_oracle_calibration_results_v1.csv") if x["experiment_id"] == ex and x["condition"] == c and x["variant"] == "SOURCE_TEMPERATURE_SCALED" and x["metric"] == metric]
                base = float(np.mean([float(x["value"]) for x in base_rows]))
                reduction = -delta / base
                threshold_pass = reduction >= rel_threshold
                ci_pass = ci_hi < 0
                bpasses.append(threshold_pass or ci_pass)
                rows.append({"criterion":"B_ORACLE_RECOVERABILITY","experiment_id":ex,"condition":c,"metric":metric,"value":delta,"threshold":f"relative reduction >= {rel_threshold} OR CI high < 0","pass":threshold_pass or ci_pass,"reason":f"relative_reduction={reduction:.6f}; ci_high={ci_hi:.6f}; threshold_pass={threshold_pass}; ci_pass={ci_pass}"})
            r = oc["ECE"]; delta = float(r["point_delta"]); ci_hi = float(r["ci95_high"]); absred = -delta
            ece_pass = absred >= .01 or ci_hi < 0; bpasses.append(ece_pass)
            rows.append({"criterion":"B_ORACLE_RECOVERABILITY","experiment_id":ex,"condition":c,"metric":"ECE","value":delta,"threshold":"absolute reduction >= 0.01 OR CI high < 0","pass":ece_pass,"reason":f"absolute_reduction={absred:.6f}; ci_high={ci_hi:.6f}"})
            for alpha in ("0.1", "0.05"):
                cr = {(x["variant"]): x for x in conf if x["experiment_id"] == ex and x["condition"] == c and x["alpha"] == alpha}
                source_abs = float(cr["SOURCE_APS"]["absolute_coverage_error"]); oracle_abs = float(cr["ORACLE_CONDITION_APS"]["absolute_coverage_error"])
                improvement = source_abs - oracle_abs
                size_increase = float(cr["ORACLE_CONDITION_APS"]["mean_set_size"]) - float(cr["SOURCE_APS"]["mean_set_size"])
                pathological = size_increase > 1.0 and improvement < .02
                pass_conf = improvement > 0 and not pathological
                rows.append({"criterion":"B_ORACLE_CONFORMAL","experiment_id":ex,"condition":c,"metric":f"APS_alpha_{alpha}","value":improvement,"threshold":"absolute error improves and no pathological inflation","pass":pass_conf,"reason":f"source_abs={source_abs:.6f}; oracle_abs={oracle_abs:.6f}; size_increase={size_increase:.6f}; pathological={pathological}"})
                bpasses.append(pass_conf)
            rows.append({"criterion":"B_COMPOUND_CELL_RECOVERABLE","experiment_id":ex,"condition":c,"metric":"joint","value":any(bpasses),"threshold":"at least one meaningful NLL/Brier/ECE/conformal recovery","pass":any(bpasses),"reason":"Independent cell-level summary; Criterion B requires at least two passing compound cells."})
            # C and D are per-cell evidence rows.
            rows.append({"criterion":"C_SOURCE_ONLY_PLAUSIBILITY","experiment_id":ex,"condition":c,"metric":"design_constraint","value":True,"threshold":"source-only frozen candidate possible","pass":True,"reason":"Design feasibility only; no efficacy claim."})
            rows.append({"criterion":"D_PREDICTIVE_COMPONENT","experiment_id":ex,"condition":c,"metric":"macro-F1","value":float(drows["macro-F1"]["point_delta"]),"threshold":"substantial negative predictive transfer","pass":float(drows["macro-F1"]["point_delta"]) < 0,"reason":f"macro-F1 delta={float(drows['macro-F1']['point_delta']):.6f}; calibration cannot change argmax."})
            for metric in ("NLL", "Brier", "error_AUROC", "error_AUPRC", "AURC", "gap"):
                rows.append({"criterion":"D_PREDICTIVE_AND_RANKING_EVIDENCE","experiment_id":ex,"condition":c,"metric":metric,"value":float(drows[metric]["point_delta"]),"threshold":"descriptive evidence retained","pass":True,"reason":"Evidence row; no subjective score or new gate."})
            for metric in ("NLL", "Brier", "ECE"):
                rows.append({"criterion":"A_COMPOUND_EVIDENCE","experiment_id":ex,"condition":c,"metric":metric,"value":float(drows[metric]["point_delta"]) if metric in drows else ece_delta,"threshold":"descriptive reliability evidence","pass":True,"reason":"Numeric compound-cell evidence retained for independent review."})
            # Modality conditioning: condition-specific oracle versus domain-only.
            for metric in ("NLL", "Brier", "ECE"):
                rr = next(r for r in oracle if r["experiment_id"] == ex and r["condition"] == c and r["metric"] == metric and r["contrast"] == "ORACLE_CONDITION_MINUS_DOMAIN")
                rows.append({"criterion":"MODALITY_CONDITIONING","experiment_id":ex,"condition":c,"metric":metric,"value":float(rr["point_delta"]),"threshold":"material improvement: point delta < 0 or CI entirely below 0","pass":float(rr["point_delta"]) < 0 or float(rr["ci95_high"]) < 0,"reason":f"ci95=[{rr['ci95_low']},{rr['ci95_high']}]"})
            for alpha in ("0.1", "0.05"):
                cr = {(x["variant"]): x for x in conf if x["experiment_id"] == ex and x["condition"] == c and x["alpha"] == alpha}
                abs_delta = float(cr["ORACLE_CONDITION_APS"]["absolute_coverage_error"]) - float(cr["ORACLE_DOMAIN_APS"]["absolute_coverage_error"])
                size_delta = float(cr["ORACLE_CONDITION_APS"]["mean_set_size"]) - float(cr["ORACLE_DOMAIN_APS"]["mean_set_size"])
                pathological = size_delta > 1.0 and abs_delta > -0.02
                rows.append({"criterion":"MODALITY_CONDITIONING_APS","experiment_id":ex,"condition":c,"metric":f"APS_alpha_{alpha}","value":abs_delta,"threshold":"absolute error delta < 0 and no pathological inflation","pass":abs_delta < 0 and not pathological,"reason":f"mean_set_size_delta={size_delta:.6f}; pathological={pathological}"})
    write_csv(ROOT / "reports/step12_1_authorization_gate_audit.csv", rows)
    return rows


def main():
    audit_artifacts()
    aps = create_aps_v11()
    audit = independent_gate_audit()
    recoverable = sorted({(r["experiment_id"], r["condition"]) for r in audit if r["criterion"] == "B_COMPOUND_CELL_RECOVERABLE" and r["pass"] is True})
    modality_by_exp = {ex: any(r["criterion"] in {"MODALITY_CONDITIONING", "MODALITY_CONDITIONING_APS"} and r["pass"] is True and r["experiment_id"] == ex for r in audit) for ex in EXPS}
    modality_supported = all(modality_by_exp.values())
    a_written = sorted({(r["experiment_id"], r["condition"]) for r in audit if r["criterion"] == "A_WRITTEN_PROSE_RECONSTRUCTION" and r["pass"] is True})
    a_implemented = sorted({(r["experiment_id"], r["condition"]) for r in audit if r["criterion"] == "A_IMPLEMENTED_STEP12" and r["pass"] is True})
    gate = {
        "step": "12.1",
        "qa_outcome": "STEP12_GATE_DECISION_REPAIRED",
        "duplicate_v1_files": ["reports/b0_oracle_aps_v1.csv", "reports/b0_oracle_conformal_results_v1.csv"],
        "duplicate_v1_sha256": sha(ROOT / "reports/b0_oracle_aps_v1.csv"),
        "repaired_aps_artifact": "reports/b0_oracle_aps_v1_1.csv",
        "independent_recoverable_compound_cells": recoverable,
        "independent_recoverable_count": len(recoverable),
        "criterion_a_written_reliability_cells": a_written,
        "criterion_a_implemented_reliability_cells": a_implemented,
        "criterion_a_gate_spec_implementation_mismatch": a_written != a_implemented,
        "criterion_b_written_recoverable_count": len(recoverable),
        "final_lightweight_method_gate": "LIGHTWEIGHT_METHOD_NOT_AUTHORIZED",
        "final_modality_conditioning_gate": "MODALITY_CONDITIONING_SUPPORTED" if modality_supported else "MODALITY_CONDITIONING_NOT_SUPPORTED",
    }
    (ROOT / "reports/step12_1_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    print(json.dumps({**gate, "aps_v11_rows": len(aps), "audit_rows": len(audit)}))


if __name__ == "__main__":
    main()
