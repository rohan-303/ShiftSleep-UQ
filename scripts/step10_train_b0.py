#!/usr/bin/env python
"""Execute exactly the frozen Step 10 B0 source-training matrix."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch
import yaml
from torch.utils.data import DataLoader

from shiftsleep_uq.models.baseline_b0 import CLASS_ORDER, BaselineB0, count_trainable_parameters
from shiftsleep_uq.training.checkpointing import CheckpointSelector
from shiftsleep_uq.training.datasets import build_source_dataset, source_dataset_for_experiment
from shiftsleep_uq.training.engine import evaluate_source_dev, train_one_epoch
from shiftsleep_uq.training.normalization import fit_source_train_dataset
from shiftsleep_uq.training.reproducibility import make_epoch_generator, seed_everything

EXPERIMENTS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
SEEDS = (17, 42, 2026)
HASHES = {
    "evaluation_protocol": "configs/evaluation_protocol_v1_1.yaml",
    "model_config": "configs/baseline_b0_v1.yaml",
    "training_config": "configs/training_b0_v1.yaml",
    "baseline_protocol": "docs/baseline_b0_protocol_v1.md",
    "subject_partition": "reports/subject_partitions_v2.csv",
    "data_contract": "configs/data_contract_v1.yaml",
    "preprocessing": "configs/preprocessing_v1.yaml",
}
EXPECTED_HASHES = {
    "evaluation_protocol": "dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756",
    "model_config": "a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17",
    "training_config": "2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7",
    "baseline_protocol": "dea145bb27fc61325c5c79653c625233bd107eb689d12e8d13fa65e8a71ca4df",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def verify_frozen_hashes() -> dict[str, str]:
    actual = {}
    for name, relative in HASHES.items():
        actual[name] = sha256_file(ROOT / relative)
        expected = EXPECTED_HASHES.get(name)
        if expected and actual[name] != expected:
            raise RuntimeError(f"STEP10_FROZEN_ARTIFACT_MISMATCH: {relative}")
    return actual


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def source_population(experiment_id: str, role: str) -> dict[str, Any]:
    dataset = source_dataset_for_experiment(experiment_id)
    data = build_source_dataset(experiment_id, role, "normalization_fit" if role == "TRAIN" else "dev", root=ROOT)
    return {
        "dataset": dataset,
        "role": role,
        "subjects": len(data.subject_ids),
        "recordings": len(data.recording_ids),
        "epochs": len(data),
    }


def fit_direction_normalization(experiment_id: str, frozen_hashes: dict[str, str], config: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    dataset = source_dataset_for_experiment(experiment_id)
    train = build_source_dataset(experiment_id, "TRAIN", "normalization_fit", root=ROOT)
    values = fit_source_train_dataset(train, role="TRAIN", std_epsilon=config["normalization"]["std_epsilon"])
    verification_dataset = build_source_dataset(experiment_id, "TRAIN", "normalization_fit", root=ROOT)
    repeated = fit_source_train_dataset(verification_dataset, role="TRAIN", std_epsilon=config["normalization"]["std_epsilon"])
    for modality in ("EEG", "EOG"):
        for field in ("mean", "std", "std_epsilon"):
            if values[modality][field] != repeated[modality][field]:
                raise RuntimeError(f"normalization reproducibility failure: {experiment_id}/{modality}/{field}")
        if not (torch.isfinite(torch.tensor(values[modality]["mean"])) and torch.isfinite(torch.tensor(values[modality]["std"]))):
            raise FloatingPointError(f"non-finite normalization: {experiment_id}/{modality}")
        if values[modality]["std"] <= values[modality]["std_epsilon"]:
            raise ValueError(f"degenerate normalization std: {experiment_id}/{modality}")
    artifact = {
        "experiment_id": experiment_id,
        "source_dataset": dataset,
        "source_role": "TRAIN",
        "subject_count": len(train.subject_ids),
        "recording_count": len(train.recording_ids),
        "EEG_sample_count": len(train) * 3000,
        "EEG_mean": values["EEG"]["mean"],
        "EEG_std": values["EEG"]["std"],
        "EOG_sample_count": len(train) * 1500,
        "EOG_mean": values["EOG"]["mean"],
        "EOG_std": values["EOG"]["std"],
        "epsilon": config["normalization"]["std_epsilon"],
        "data_contract_version": "1.2.0",
        "data_contract_sha256": frozen_hashes["data_contract"],
        "preprocessing_version": "0.1.0",
        "preprocessing_sha256": frozen_hashes["preprocessing"],
        "evaluation_protocol_version": "1.1.0",
        "evaluation_protocol_sha256": frozen_hashes["evaluation_protocol"],
        "subject_partition_sha256": frozen_hashes["subject_partition"],
        "fitting_code_version": "step10_streaming_welford_v1",
        "git_commit": git_commit(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }
    output = ROOT / "artifacts/normalization/b0" / f"{experiment_id}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact, train.access_events + verification_dataset.access_events


def write_history(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["epoch", "train_cross_entropy", "macro_f1", "nll", "learning_rate", "gradient_norm", "checkpoint_selected", "elapsed_training_seconds"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in fields} for row in rows)


def train_one_run(experiment_id: str, seed: int, normalization: dict[str, Any], frozen_hashes: dict[str, str], model_config: dict[str, Any], training_config: dict[str, Any], access_events: list[dict[str, str]]) -> dict[str, Any]:
    seed_everything(seed)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    train = build_source_dataset(experiment_id, "TRAIN", "train", root=ROOT)
    dev = build_source_dataset(experiment_id, "DEV", "dev", root=ROOT)
    train.set_normalization({"EEG": {"mean": normalization["EEG_mean"], "std": normalization["EEG_std"], "std_epsilon": normalization["epsilon"]}, "EOG": {"mean": normalization["EOG_mean"], "std": normalization["EOG_std"], "std_epsilon": normalization["epsilon"]}})
    dev.set_normalization({"EEG": {"mean": normalization["EEG_mean"], "std": normalization["EEG_std"], "std_epsilon": normalization["epsilon"]}, "EOG": {"mean": normalization["EOG_mean"], "std": normalization["EOG_std"], "std_epsilon": normalization["epsilon"]}})

    run_dir = ROOT / "artifacts/models/b0" / experiment_id / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    normalization_path = ROOT / "artifacts/normalization/b0" / f"{experiment_id}.json"
    normalization_hash = sha256_file(normalization_path)
    (run_dir / "normalization.json").write_text(json.dumps({"path": str(normalization_path.relative_to(ROOT)), "sha256": normalization_hash}, indent=2) + "\n", encoding="utf-8")
    batch_size = training_config["batch_size"]["physical"]
    dev_loader = DataLoader(dev, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=device.type == "cuda")
    model = BaselineB0().to(device).float()
    if count_trainable_parameters(model) != 654597:
        raise RuntimeError("parameter count mismatch")
    optimizer = torch.optim.AdamW(model.parameters(), lr=training_config["optimizer"]["learning_rate"], weight_decay=training_config["optimizer"]["weight_decay"], betas=tuple(training_config["optimizer"]["betas"]), eps=training_config["optimizer"]["eps"])
    selector = CheckpointSelector(patience=training_config["early_stopping"]["patience"], min_epochs=training_config["minimum_epochs"], tolerance=training_config["early_stopping"]["tolerance"])
    history: list[dict[str, Any]] = []
    started = time.perf_counter()
    for epoch in range(1, training_config["max_epochs"] + 1):
        epoch_started = time.perf_counter()
        train_loader = DataLoader(train, batch_size=batch_size, shuffle=True, generator=make_epoch_generator(seed, epoch), num_workers=0, pin_memory=device.type == "cuda")
        train_stats = train_one_epoch(model, train_loader, optimizer, device=device, max_grad_norm=training_config["gradient_clipping"]["max_norm"])
        dev_stats = evaluate_source_dev(model, dev_loader, device=device)
        selected = selector.observe(epoch, dev_stats["macro_f1"], dev_stats["nll"])
        row = {"epoch": epoch, **train_stats, **dev_stats, "learning_rate": optimizer.param_groups[0]["lr"], "checkpoint_selected": selected, "elapsed_training_seconds": time.perf_counter() - epoch_started}
        history.append(row)
        if selected:
            checkpoint_metadata = {"baseline_id": "B0_DUAL_BRANCH_RAW_CNN", "architecture_version": model_config["version"], "experiment_id": experiment_id, "source_dataset": train.dataset, "seed": seed, "selected_epoch": epoch, "selected_dev_macro_f1": dev_stats["macro_f1"], "selected_dev_nll": dev_stats["nll"], "class_order": list(CLASS_ORDER), "model_config_sha256": frozen_hashes["model_config"], "training_config_sha256": frozen_hashes["training_config"], "evaluation_protocol_sha256": frozen_hashes["evaluation_protocol"], "subject_partition_sha256": frozen_hashes["subject_partition"], "normalization_sha256": normalization_hash, "data_contract_version": "1.2.0", "data_contract_sha256": frozen_hashes["data_contract"], "preprocessing_version": "0.1.0", "preprocessing_sha256": frozen_hashes["preprocessing"], "pytorch_version": torch.__version__, "cuda_version": torch.version.cuda, "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu", "git_commit": git_commit(), "timestamp_utc": datetime.now(UTC).isoformat()}
            torch.save({"model_state_dict": model.state_dict(), "metadata": checkpoint_metadata}, run_dir / "best.pt")
        if selector.should_stop(epoch):
            break
    if selector.best is None:
        raise RuntimeError(f"no checkpoint selected: {experiment_id}/{seed}")
    stop_reason = "EARLY_STOPPING" if len(history) < training_config["max_epochs"] else "MAX_EPOCHS"
    write_history(run_dir / "training_history.csv", history)
    checkpoint_path = run_dir / "best.pt"
    checkpoint_sha = sha256_file(checkpoint_path)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    reload_model = BaselineB0().to(device).float()
    reload_model.load_state_dict(checkpoint["model_state_dict"])
    reload_model.eval()
    smoke_batch = next(iter(DataLoader(dev, batch_size=min(2, len(dev)), shuffle=False, num_workers=0)))
    with torch.no_grad():
        smoke_logits = reload_model(smoke_batch["eeg"].to(device), smoke_batch["eog"].to(device), torch.ones((smoke_batch["label"].shape[0], 2), device=device))
    if not torch.isfinite(smoke_logits).all():
        raise FloatingPointError(f"non-finite checkpoint smoke logits: {experiment_id}/{seed}")
    manifest = {"baseline_id": "B0_DUAL_BRANCH_RAW_CNN", "experiment_id": experiment_id, "source_dataset": train.dataset, "target_dataset": "isruc_s1" if experiment_id.startswith("D1") else "sleep_edf_sc", "model_seed": seed, "selected_epoch": selector.best["epoch"], "selected_dev_macro_f1": selector.best["macro_f1"], "selected_dev_nll": selector.best["nll"], "epochs_executed": len(history), "stop_reason": stop_reason, "model_config_sha256": frozen_hashes["model_config"], "training_config_sha256": frozen_hashes["training_config"], "evaluation_protocol_sha256": frozen_hashes["evaluation_protocol"], "subject_partition_sha256": frozen_hashes["subject_partition"], "source_cohort_sha256": sha256_file(ROOT / ("configs/core_cohort_v2.yaml" if train.dataset == "sleep_edf_sc" else "configs/isruc_original_cohort_v3.yaml")), "normalization_sha256": normalization_hash, "checkpoint_sha256": checkpoint_sha, "pytorch_version": torch.__version__, "cuda_version": torch.version.cuda, "cudnn_version": torch.backends.cudnn.version(), "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu", "git_commit": git_commit(), "wall_clock_training_seconds": time.perf_counter() - started, "restart_count": 0}
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    access_events.extend(train.access_events)
    access_events.extend(dev.access_events)
    return {"baseline_id": "B0_DUAL_BRANCH_RAW_CNN", "experiment_id": experiment_id, "seed": seed, "source_dataset": train.dataset, "selected_epoch": selector.best["epoch"], "epochs_executed": len(history), "stop_reason": stop_reason, "selected_dev_macro_f1": selector.best["macro_f1"], "selected_dev_nll": selector.best["nll"], "final_train_ce": history[-1]["train_cross_entropy"], "checkpoint_sha256": checkpoint_sha, "normalization_sha256": normalization_hash, "run_manifest_sha256": sha256_file(run_dir / "run_manifest.json"), "training_seconds": manifest["wall_clock_training_seconds"], "status": "COMPLETE"}


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", required=True)
    args = parser.parse_args()
    del args
    frozen_hashes = verify_frozen_hashes()
    if not torch.cuda.is_available():
        raise RuntimeError("BASELINE_BATCH_MEMORY_BLOCKED: CUDA unavailable")
    model_config = yaml.safe_load((ROOT / HASHES["model_config"]).read_text(encoding="utf-8"))
    training_config = yaml.safe_load((ROOT / HASHES["training_config"]).read_text(encoding="utf-8"))
    access_events: list[dict[str, str]] = []
    normalizations: dict[str, dict[str, Any]] = {}
    for experiment_id in EXPERIMENTS:
        artifact, events = fit_direction_normalization(experiment_id, frozen_hashes, training_config)
        normalizations[experiment_id] = artifact
        access_events.extend(events)
    summaries = []
    for experiment_id in EXPERIMENTS:
        for seed in SEEDS:
            summaries.append(train_one_run(experiment_id, seed, normalizations[experiment_id], frozen_hashes, model_config, training_config, access_events))
            torch.cuda.empty_cache()
    write_csv(ROOT / "reports/step10_normalization_summary.csv", [{"experiment_id": e, "source_dataset": a["source_dataset"], "source_role": a["source_role"], "subject_count": a["subject_count"], "recording_count": a["recording_count"], "EEG_sample_count": a["EEG_sample_count"], "EEG_mean": a["EEG_mean"], "EEG_std": a["EEG_std"], "EOG_sample_count": a["EOG_sample_count"], "EOG_mean": a["EOG_mean"], "EOG_std": a["EOG_std"], "artifact_sha256": sha256_file(ROOT / "artifacts/normalization/b0" / f"{e}.json")} for e, a in normalizations.items()], ["experiment_id", "source_dataset", "source_role", "subject_count", "recording_count", "EEG_sample_count", "EEG_mean", "EEG_std", "EOG_sample_count", "EOG_mean", "EOG_std", "artifact_sha256"])
    write_csv(ROOT / "reports/b0_training_summary_v1.csv", summaries, list(summaries[0]))
    checkpoint_lines = []
    for row in summaries:
        checkpoint_lines.append(f"{row['experiment_id']},seed_{row['seed']},artifacts/models/b0/{row['experiment_id']}/seed_{row['seed']}/best.pt,{row['checkpoint_sha256']}")
    (ROOT / "reports/b0_checkpoint_hashes_v1.txt").write_text("experiment_id,seed,relative_path,sha256\n" + "\n".join(checkpoint_lines) + "\n", encoding="utf-8")
    (ROOT / "reports/b0_normalization_hashes_v1.txt").write_text("experiment_id,relative_path,sha256\n" + "\n".join(f"{e},artifacts/normalization/b0/{e}.json,{sha256_file(ROOT / 'artifacts/normalization/b0' / f'{e}.json')}" for e in EXPERIMENTS) + "\n", encoding="utf-8")
    unique_events = {(event["dataset"], event["source_role"], event["purpose"], event["subject_id"], event["recording_id"], event["path"]): event for event in access_events}
    audit_fields = ["dataset", "source_role", "purpose", "subject_id", "recording_id", "path"]
    write_csv(ROOT / "reports/step10_data_access_audit.csv", list(unique_events.values()), audit_fields)
    forbidden = [event for event in unique_events.values() if event["source_role"] not in {"TRAIN", "DEV"}]
    if forbidden:
        raise RuntimeError("STEP10_DATA_FIREWALL_VIOLATION")
    print(json.dumps({"status": "B0_SOURCE_TRAINING_COMPLETE", "runs": len(summaries), "normalizations": len(normalizations), "access_rows": len(unique_events)}, sort_keys=True))


if __name__ == "__main__":
    main()
