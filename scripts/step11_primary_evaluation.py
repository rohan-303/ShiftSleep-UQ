#!/usr/bin/env python
"""Execute the frozen ShiftSleep-UQ Step 11 B0 primary evaluation."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch
import yaml
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shiftsleep_uq.evaluation_step11 import (  # noqa: E402
    PhaseGate, aps_quantile, aps_scores, compute_metric_rows, fit_temperature, softmax,
    entropy, _rank_auc, auprc, aurc, macro_f1, nll, brier, conformal_metrics,
)
from shiftsleep_uq.models.baseline_b0 import BaselineB0, count_trainable_parameters, condition_mask  # noqa: E402
from shiftsleep_uq.training.datasets import build_evaluation_dataset, build_source_dataset  # noqa: E402

EXPERIMENTS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
SEEDS = (17, 42, 2026)
CONDITIONS = ("C0", "C1", "C2", "C3", "C4", "C5")
EXPECTED = {
    "configs/evaluation_protocol_v1_1.yaml": "dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756",
    "configs/baseline_b0_v1.yaml": "a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17",
    "configs/training_b0_v1.yaml": "2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7",
    "docs/baseline_b0_protocol_v1.md": "dea145bb27fc61325c5c79653c625233bd107eb689d12e8d13fa65e8a71ca4df",
    "reports/subject_partitions_v2.csv": "9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329",
    "artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json": "be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3",
    "artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json": "3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e",
}
CHECKPOINTS = {
    ("D1_SLEEPEDF_TO_ISRUC", 17): ("artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_17/best.pt", "3e0ca3d3d7a345a4b2add8900499485bf2cf72afccb522de64d5d3115a9a5f9c"),
    ("D1_SLEEPEDF_TO_ISRUC", 42): ("artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_42/best.pt", "380496b69b5622944d259a0abd163325daecf39638ca3af4a1f6c01a9738d8fb"),
    ("D1_SLEEPEDF_TO_ISRUC", 2026): ("artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_2026/best.pt", "edf8d12f40c33d3096de3dffd0c6fcfc5028b3923bb2e6894fc9e2a83e96ce45"),
    ("D2_ISRUC_TO_SLEEPEDF", 17): ("artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_17/best.pt", "bb82549b8860d07c83c85f27cd65a72b905d60ff220eab5942da9966c4d3afe6"),
    ("D2_ISRUC_TO_SLEEPEDF", 42): ("artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_42/best.pt", "3d12a02aeccbf0d5ffab2b5864b5c8ace5b51f27ca641dc6c5f1981831258574"),
    ("D2_ISRUC_TO_SLEEPEDF", 2026): ("artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_2026/best.pt", "7af6ab439225b24fe1b2cb00c1285b88a54a527fe07be70b17d042418a203744"),
}
BOOT_REPS = 2000
BOOT_SEED = 2028

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(dict.fromkeys(key for row in rows for key in row))
    else:
        fields = list(dict.fromkeys([*fields, *(key for row in rows for key in row if key not in fields)]))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def preflight() -> dict[str, str]:
    if Path.cwd().resolve() != ROOT.resolve():
        raise RuntimeError("STEP11_WRONG_REPOSITORY")
    actual = {}
    for rel, expected in EXPECTED.items():
        p = ROOT / rel
        if not p.exists() or sha256(p) != expected: raise RuntimeError(f"STEP11_FROZEN_ARTIFACT_MISMATCH:{rel}")
        actual[rel] = expected
    for key, (rel, expected) in CHECKPOINTS.items():
        p = ROOT / rel
        if not p.exists() or sha256(p) != expected: raise RuntimeError(f"STEP11_CHECKPOINT_MISMATCH:{rel}")
        payload = torch.load(p, map_location="cpu", weights_only=False); model = BaselineB0(); model.load_state_dict(payload["model_state_dict"])
        if count_trainable_parameters(model) != 654597: raise RuntimeError(f"STEP11_PARAMETER_COUNT_MISMATCH:{rel}")
    for rel in ("artifacts/predictions", "artifacts/calibration", "artifacts/statistics"):
        if (ROOT / rel).exists() and any((ROOT / rel).rglob("*")): raise RuntimeError(f"STEP11_PROHIBITED_PREEXISTING_OUTPUT:{rel}")
    for rel in ("reports/b0_primary_metrics_per_seed_v1.csv", "reports/b0_primary_results_multiseed_v1.csv"):
        if (ROOT / rel).exists(): raise RuntimeError(f"STEP11_PROHIBITED_PREEXISTING_OUTPUT:{rel}")
    return actual

def normalization_for(experiment: str) -> dict:
    a = json.loads((ROOT / "artifacts/normalization/b0" / f"{experiment}.json").read_text())
    return {"EEG": {"mean": a["EEG_mean"], "std": a["EEG_std"], "std_epsilon": a["epsilon"]}, "EOG": {"mean": a["EOG_mean"], "std": a["EOG_std"], "std_epsilon": a["epsilon"]}}

def load_model(experiment: str, seed: int, device: torch.device) -> torch.nn.Module:
    rel, expected = CHECKPOINTS[(experiment, seed)]
    if sha256(ROOT / rel) != expected: raise RuntimeError("STEP11_CHECKPOINT_CHANGED")
    payload = torch.load(ROOT / rel, map_location=device, weights_only=False); model = BaselineB0().to(device).float(); model.load_state_dict(payload["model_state_dict"]); model.eval(); return model

def predict(model: torch.nn.Module, dataset, mask: tuple[int, int], device: torch.device) -> dict[str, np.ndarray]:
    loader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=0, pin_memory=device.type == "cuda")
    logits=[]; labels=[]; subjects=[]; recordings=[]; epochs=[]; montages=[]
    with torch.no_grad():
        for batch in loader:
            n = len(batch["label"]); m = torch.tensor(mask, device=device, dtype=torch.float32).expand(n, -1)
            out = model(batch["eeg"].to(device), batch["eog"].to(device), m).cpu().numpy().astype(np.float32)
            logits.append(out); labels.append(batch["label"].numpy().astype(np.int8)); subjects.extend(batch["subject_id"]); recordings.extend(batch["recording_id"]); epochs.extend(batch["epoch_index"].numpy().tolist()); montages.extend(batch["montage_variant"])
    result = {"logits": np.concatenate(logits), "labels": np.concatenate(labels), "subject_id": np.asarray(subjects), "recording_id": np.asarray(recordings), "epoch_index": np.asarray(epochs, dtype=np.int32), "montage_variant": np.asarray(montages)}
    if not np.isfinite(result["logits"]).all(): raise FloatingPointError("non-finite evaluation logits")
    return result

def phase_a_calibration(device: torch.device, access: list[dict]) -> tuple[dict, dict, PhaseGate]:
    temperatures={}; aps={}; gate=PhaseGate("PHASE_A_CALIBRATION")
    for experiment in EXPERIMENTS:
        ds = build_source_dataset(experiment, "CALIBRATION", "calibration", root=ROOT); norm=normalization_for(experiment); ds.set_normalization(norm)
        for seed in SEEDS:
            model=load_model(experiment, seed, device); data=predict(model, ds, (1,1), device); fit=fit_temperature(data["logits"], data["labels"], role="CALIBRATION")
            raw=softmax(data["logits"]); qh={alpha: aps_quantile(aps_scores(raw, data["labels"]), alpha) for alpha in (0.10,0.05)}
            key=f"{experiment}/seed_{seed}"; d=ROOT/"artifacts/calibration/b0"/experiment/f"seed_{seed}"; d.mkdir(parents=True, exist_ok=True)
            t={"artifact_type":"SOURCE_CALIBRATION_TEMPERATURE","experiment_id":experiment,"seed":seed,"checkpoint_sha256":CHECKPOINTS[(experiment,seed)][1],"normalization_sha256":sha256(ROOT/"artifacts/normalization/b0"/f"{experiment}.json"),"source_dataset":ds.dataset,"source_role":"CALIBRATION","source_subject_count":len(ds.subject_ids),"source_epoch_count":len(ds),**fit,"protocol_sha256":EXPECTED["configs/evaluation_protocol_v1_1.yaml"],"timestamp_utc":datetime.now(UTC).isoformat()}
            a={"artifact_type":"SOURCE_CALIBRATION_APS","experiment_id":experiment,"seed":seed,"checkpoint_sha256":CHECKPOINTS[(experiment,seed)][1],"normalization_sha256":t["normalization_sha256"],"source_dataset":ds.dataset,"source_role":"CALIBRATION","source_subject_count":len(ds.subject_ids),"source_epoch_count":len(ds),"score_definition":"cumulative uncalibrated softmax probability through true class in descending probability order","tie_rule":"descending probability then ascending class index","alpha_0.10_qhat":qh[0.10],"alpha_0.05_qhat":qh[0.05],"quantile_rule":"k=ceil((n+1)*(1-alpha)), clamped 1..n, kth ascending score","protocol_sha256":EXPECTED["configs/evaluation_protocol_v1_1.yaml"],"timestamp_utc":datetime.now(UTC).isoformat()}
            (d/"temperature.json").write_text(json.dumps(t,indent=2,sort_keys=True)+"\n"); (d/"aps.json").write_text(json.dumps(a,indent=2,sort_keys=True)+"\n"); temperatures[key]=t; aps[key]=a
            access.extend({**e,"phase":"PHASE_A","operation":"calibration_inference"} for e in ds.access_events); access.append({"dataset":ds.dataset,"source_role":"CALIBRATION","purpose":"temperature_and_aps_fit","phase":"PHASE_A","operation":"fit_parameters","subject_id":"ALL","recording_id":"ALL","path":"SOURCE_CALIBRATION_ONLY"})
            del model; torch.cuda.empty_cache()
    write_csv(ROOT/"reports/b0_temperature_calibration_v1.csv", list(temperatures.values()))
    write_csv(ROOT/"reports/b0_aps_calibration_v1.csv", list(aps.values()))
    (ROOT/"reports/b0_calibration_hashes_v1.txt").write_text("artifact,sha256\n"+"\n".join(f"{k.replace('/','_')}_{name},{sha256(ROOT/'artifacts/calibration/b0'/k.split('/')[0]/k.split('/')[1]/(name+'.json'))}" for k in temperatures for name in ("temperature","aps"))+"\n")
    return temperatures, aps, gate.freeze()

def save_bundle(path: Path, data: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True); np.savez_compressed(path, **data); return sha256(path)

def bootstrap_metric(preds: list[dict], metric: str, qhats: dict[float,float] | None = None, reps: int=BOOT_REPS) -> np.ndarray:
    subjects=sorted(set(preds[0]["subject_id"].tolist())); by=[{s:np.flatnonzero(p["subject_id"]==s) for s in subjects} for p in preds]; rng=np.random.default_rng(BOOT_SEED); out=np.empty(reps)
    for r in range(reps):
        sampled=rng.choice(len(subjects),len(subjects),replace=True); vals=[]
        for p, maps in zip(preds,by):
            idx=np.concatenate([maps[subjects[i]] for i in sampled]); prob=softmax(p["logits"][idx]); lab=p["labels"][idx]; pred=prob.argmax(1); score=entropy(prob); err=(pred!=lab).astype(int)
            if metric=="macro-F1": val=macro_f1(pred,lab)
            elif metric=="NLL": val=nll(prob,lab)
            elif metric=="Brier": val=brier(prob,lab)
            elif metric=="ERROR_AUROC": val=_rank_auc(score,err)
            elif metric=="ERROR_AUPRC": val=auprc(score,err)
            elif metric=="AURC": val=aurc(score,pred,lab)
            elif metric.startswith("coverage_"):
                alpha=float(metric.split("_")[-1]); val=conformal_metrics(prob,lab,qhats[alpha],alpha)["empirical_coverage"]
            elif metric.startswith("gap_"):
                alpha=float(metric.split("_")[-1]); val=conformal_metrics(prob,lab,qhats[alpha],alpha)["coverage_gap"]
            else: raise ValueError(metric)
            vals.append(val)
        out[r]=np.nanmean(vals)
    return out

def execute() -> None:
    hashes=preflight(); device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"); access=[]
    temperatures, aps, frozen=phase_a_calibration(device, access)
    (ROOT/"artifacts/calibration/b0/SOURCE_CALIBRATION_FROZEN.json").write_text(json.dumps({"gate":"SOURCE_CALIBRATION_FROZEN","temperature_count":6,"aps_count":6,"phase_b_opened":True,"calibration_hashes":{k:sha256(ROOT/"artifacts/calibration/b0"/k.split('/')[0]/k.split('/')[1]/name) for k in temperatures for name in ("temperature.json","aps.json")}},indent=2,sort_keys=True)+"\n")
    predictions={}; hash_rows=[]; metric_rows=[]; confusion_rows=[]; montage_rows=[]
    for experiment in EXPERIMENTS:
        populations={"SOURCE_TEST":"SOURCE_TEST","COMPLETE_TARGET":"COMPLETE_TARGET"}; datasets={pop:build_evaluation_dataset(experiment,pop,root=ROOT) for pop in populations};
        for ds in datasets.values(): ds.set_normalization(normalization_for(experiment))
        for seed in SEEDS:
            model=load_model(experiment,seed,device); key=f"{experiment}/seed_{seed}"; t=temperatures[key]; a=aps[key]; th=sha256(ROOT/"artifacts/calibration/b0"/experiment/f"seed_{seed}"/"temperature.json"); ah=sha256(ROOT/"artifacts/calibration/b0"/experiment/f"seed_{seed}"/"aps.json")
            for condition in CONDITIONS:
                pop="SOURCE_TEST" if condition in {"C0","C1","C2"} else "COMPLETE_TARGET"; ds=datasets[pop]; data=predict(model,ds,condition_mask(condition),device); rel=Path("artifacts/predictions/b0")/experiment/f"seed_{seed}"/f"{condition}.npz"; ph=save_bundle(ROOT/rel,data); predictions[(experiment,seed,condition)]={**data,"prediction_hash":ph,"prediction_path":str(rel),"population":pop}
                hash_rows.append({"experiment_id":experiment,"seed":seed,"condition":condition,"population":pop,"epoch_count":len(data["labels"]),"prediction_bundle":str(rel),"sha256":ph,"checkpoint_sha256":CHECKPOINTS[(experiment,seed)][1],"normalization_sha256":sha256(ROOT/"artifacts/normalization/b0"/f"{experiment}.json"),"temperature_sha256":th,"aps_sha256":ah})
                rows,cm=compute_metric_rows(data["logits"],data["labels"],t["temperature"],{0.10:a["alpha_0.10_qhat"],0.05:a["alpha_0.05_qhat"]});
                for row in rows: metric_rows.append({"baseline_id":"B0_DUAL_BRANCH_RAW_CNN","experiment_id":experiment,"source_dataset":ds.dataset,"target_dataset":"isruc_s1" if experiment.startswith("D1") else "sleep_edf_sc","seed":seed,"condition":condition,"population":pop,**row,"subject_count":len(set(data["subject_id"])),"epoch_count":len(data["labels"]),"checkpoint_hash":CHECKPOINTS[(experiment,seed)][1],"calibration_hash":th,"prediction_hash":ph})
                for i in range(5):
                    for j in range(5): confusion_rows.append({"experiment_id":experiment,"seed":seed,"condition":condition,"population":pop,"true_class":i,"predicted_class":j,"count":int(cm[i,j]),"prediction_hash":ph})
                if ds.dataset=="isruc_s1":
                    for montage in ("ISRUC_A1A2","ISRUC_M1M2"):
                        idx=data["montage_variant"]==montage
                        if idx.any():
                            sub=data["logits"][idx]; lab=data["labels"][idx]; pr=softmax(sub); pred=pr.argmax(1); ent=entropy(pr); err=(pred!=lab).astype(int)
                            for metric,value in {"macro-F1":macro_f1(pred,lab),"NLL":nll(pr,lab),"Brier":brier(pr,lab),"error_entropy_AUROC":_rank_auc(ent,err),"error_entropy_AUPRC":auprc(ent,err),"entropy_AURC":aurc(ent,pred,lab)}.items(): montage_rows.append({"direction":experiment,"seed":seed,"condition":condition,"montage":montage,"metric":metric,"probability_variant":"UNCALIBRATED","value":value,"subject_count":len(set(data["subject_id"][idx])),"epoch_count":int(idx.sum())})
            for ds in datasets.values(): access.extend({**e,"phase":"PHASE_B","operation":"evaluation_inference"} for e in ds.access_events)
            del model; torch.cuda.empty_cache()
    write_csv(ROOT/"reports/b0_primary_prediction_hashes_v1.txt",hash_rows)
    write_csv(ROOT/"reports/b0_primary_metrics_per_seed_v1.csv",metric_rows)
    write_csv(ROOT/"reports/b0_confusion_matrices_v1.csv",confusion_rows)
    write_csv(ROOT/"reports/b0_isruc_montage_sensitivity_per_seed_v1.csv",montage_rows)
    required=("macro-F1","NLL","Brier","ERROR_AUROC","ERROR_AUPRC","AURC","coverage_0.1","gap_0.1","coverage_0.05","gap_0.05")
    boot_rows=[]; contrast_rows=[]; boot_arrays={}
    for experiment in EXPERIMENTS:
        for condition in CONDITIONS:
            ps=[predictions[(experiment,s,condition)] for s in SEEDS]; q={.1:aps[f"{experiment}/seed_17"]["alpha_0.10_qhat"],.05:aps[f"{experiment}/seed_17"]["alpha_0.05_qhat"]}
            for metric in required:
                arr=bootstrap_metric(ps,metric,q); boot_arrays[f"{experiment}_{condition}_{metric}"]=arr; point=[]
                for s in SEEDS:
                    d=predictions[(experiment,s,condition)]; p=softmax(d["logits"]); lab=d["labels"]; pred=p.argmax(1); ent=entropy(p); err=(pred!=lab).astype(int)
                    point.append({"macro-F1":macro_f1(pred,lab),"NLL":nll(p,lab),"Brier":brier(p,lab),"ERROR_AUROC":_rank_auc(ent,err),"ERROR_AUPRC":auprc(ent,err),"AURC":aurc(ent,pred,lab),"coverage_0.1":conformal_metrics(p,lab,q[.1],.1)["empirical_coverage"],"gap_0.1":conformal_metrics(p,lab,q[.1],.1)["coverage_gap"],"coverage_0.05":conformal_metrics(p,lab,q[.05],.05)["empirical_coverage"],"gap_0.05":conformal_metrics(p,lab,q[.05],.05)["coverage_gap"]}[metric])
                boot_rows.append({"experiment_id":experiment,"condition":condition,"metric":metric,"probability_variant":"UNCALIBRATED","point_estimate":float(np.mean(point)),"seed_sd":float(np.std(point,ddof=1)),"ci95_low":float(np.nanpercentile(arr,2.5)),"ci95_high":float(np.nanpercentile(arr,97.5)),"subject_count":len(set(ps[0]["subject_id"])),"epoch_count":len(ps[0]["labels"])})
    np.savez_compressed(ROOT/"artifacts/statistics/b0/bootstrap_replicates.npz",**boot_arrays); write_csv(ROOT/"reports/b0_primary_results_multiseed_v1.csv",boot_rows)
    for experiment in EXPERIMENTS:
        pairs=(("KNOWN_EEG_ONLY_MINUS_FULL","C1","C0"),("KNOWN_EOG_ONLY_MINUS_FULL","C2","C0"),("UNSEEN_EEG_ONLY_MINUS_FULL","C4","C3"),("UNSEEN_EOG_ONLY_MINUS_FULL","C5","C3"))
        for name,a,b in pairs:
            for metric in ("macro-F1","NLL","AURC","gap_0.1"):
                x=boot_arrays[f"{experiment}_{a}_{metric}"]; y=boot_arrays[f"{experiment}_{b}_{metric}"]; delta=x-y; contrast_rows.append({"experiment_id":experiment,"metric":metric,"contrast_name":name,"probability_variant":"UNCALIBRATED","point_delta":float(np.nanmean(delta)),"ci95_low":float(np.nanpercentile(delta,2.5)),"ci95_high":float(np.nanpercentile(delta,97.5)),"orientation":"higher_is_better" if metric=="macro-F1" else "lower_is_better","bootstrap_replicates":BOOT_REPS})
        for name,un,kn in (("INTERACTION_EEG_ONLY","UNSEEN_EEG_ONLY_MINUS_FULL","KNOWN_EEG_ONLY_MINUS_FULL"),("INTERACTION_EOG_ONLY","UNSEEN_EOG_ONLY_MINUS_FULL","KNOWN_EOG_ONLY_MINUS_FULL")):
            for metric in ("macro-F1","NLL","AURC","gap_0.1"):
                d=(boot_arrays[f"{experiment}_{('C4' if 'EEG' in name else 'C5')}_{metric}"]-boot_arrays[f"{experiment}_{('C3')}_{metric}"])-(boot_arrays[f"{experiment}_{('C1' if 'EEG' in name else 'C2')}_{metric}"]-boot_arrays[f"{experiment}_C0_{metric}"])
                contrast_rows.append({"experiment_id":experiment,"metric":metric,"contrast_name":name,"probability_variant":"UNCALIBRATED","point_delta":float(np.nanmean(d)),"ci95_low":float(np.nanpercentile(d,2.5)),"ci95_high":float(np.nanpercentile(d,97.5)),"orientation":"higher_is_better" if metric=="macro-F1" else "lower_is_better","bootstrap_replicates":BOOT_REPS})
    write_csv(ROOT/"reports/b0_primary_contrasts_v1.csv",contrast_rows)
    audit_fields=["phase","dataset","source_role","purpose","operation","subject_id","recording_id","path"]; write_csv(ROOT/"reports/step11_data_access_audit.csv",access,audit_fields)
    (ROOT/"reports/b0_primary_prediction_hashes_v1.txt.sha256").write_text(sha256(ROOT/"reports/b0_primary_prediction_hashes_v1.txt")+"\n")
    (ROOT/"reports/b0_statistical_hashes_v1.txt").write_text("artifact,sha256\n"+"\n".join(f"{p},{sha256(ROOT/p)}" for p in ("reports/b0_primary_results_multiseed_v1.csv","reports/b0_primary_contrasts_v1.csv","reports/b0_isruc_montage_sensitivity_per_seed_v1.csv","artifacts/statistics/b0/bootstrap_replicates.npz")))
    if any(e.get("source_role") in {"TRAIN","DEV"} for e in access): raise RuntimeError("STEP11_DATA_FIREWALL_VIOLATION")
    print(json.dumps({"status":"B0_PRIMARY_EVALUATION_COMPLETE","temperatures":6,"aps":6,"bundles":len(hash_rows),"bootstrap_replicates":BOOT_REPS,"access_rows":len(access)},sort_keys=True))

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--execute",action="store_true",required=True); args=parser.parse_args(); del args
    execute()
if __name__ == "__main__": main()
