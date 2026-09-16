import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT / "reports" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_oracle_v1_duplicate_is_detected_and_v11_aps_schema_is_distinct():
    aps = ROOT / "reports/b0_oracle_aps_v1.csv"
    conf = ROOT / "reports/b0_oracle_conformal_results_v1.csv"
    assert aps.read_bytes() == conf.read_bytes()
    repaired = rows("b0_oracle_aps_v1_1.csv")
    conformal = rows("b0_oracle_conformal_results_v1.csv")
    assert repaired
    assert set(repaired[0]) != set(conformal[0])
    assert {r["fit_type"] for r in repaired} == {"ORACLE_DOMAIN_APS", "ORACLE_CONDITION_APS"}


def test_step12_1_manifest_paths_and_hashes_are_correct():
    for r in rows("step12_1_artifact_integrity_audit.csv"):
        p = ROOT / r["artifact"]
        assert p.exists()
        assert hashlib.sha256(p.read_bytes()).hexdigest() == r["actual_hash"]
    dup = [r for r in rows("step12_1_artifact_integrity_audit.csv") if r["status"] == "UNEXPECTED_DUPLICATE_CONTENT"]
    assert {r["artifact"] for r in dup} == {"reports/b0_oracle_aps_v1.csv", "reports/b0_oracle_conformal_results_v1.csv"}


def test_independent_gate_reproduces_four_cells_and_final_decision():
    gate = json.loads((ROOT / "reports/step12_1_gate.json").read_text())
    assert gate["independent_recoverable_count"] == 4
    assert gate["criterion_b_written_recoverable_count"] == 4
    assert gate["criterion_a_gate_spec_implementation_mismatch"] is True
    assert gate["final_lightweight_method_gate"] == "LIGHTWEIGHT_METHOD_NOT_AUTHORIZED"
    assert gate["final_modality_conditioning_gate"] == "MODALITY_CONDITIONING_SUPPORTED"


def test_temperature_and_aps_reference_integrity():
    temps = rows("b0_oracle_temperature_v1.csv")
    assert len(temps) == 24
    assert all(float(r["temperature"]) > 0 for r in temps)
    assert all(float(r["final_nll"]) <= float(r["initial_nll"]) + 1e-9 for r in temps)
    aps = rows("b0_oracle_aps_v1_1.csv")
    assert len(aps) == 48
    for key in {(r["experiment_id"], r["seed"], r["fit_scope"], r["fit_condition"]) for r in aps}:
        subset = [r for r in aps if (r["experiment_id"], r["seed"], r["fit_scope"], r["fit_condition"]) == key]
        q = {r["alpha"]: float(r["qhat"]) for r in subset}
        assert q["0.05"] >= q["0.1"]
