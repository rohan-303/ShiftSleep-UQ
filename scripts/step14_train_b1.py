#!/usr/bin/env python
"""Train exactly the frozen Step 14 B1 source-only matrix."""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import torch
import yaml
from torch import nn
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shiftsleep_uq.models.baseline_b0 import CLASS_ORDER, BaselineB0, count_trainable_parameters
from shiftsleep_uq.training.checkpointing import CheckpointSelector
from shiftsleep_uq.training.datasets import build_source_dataset
from shiftsleep_uq.training.modality_exposure import assign_masks, apply_missing_modality_zeroing
from shiftsleep_uq.training.reproducibility import make_epoch_generator, seed_everything

EXPERIMENTS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
SEEDS = (17, 42, 2026)
EXPECTED_PARAM_COUNT = 654597
EXPOSURE_SEED = 2029
B1_MODEL_CONFIG = "configs/baseline_b1_moddrop_v1.yaml"
B1_TRAINING_CONFIG = "configs/training_b1_moddrop_v1.yaml"
B0_MODEL_CONFIG = "configs/baseline_b0_v1.yaml"
EVAL_CONFIG = "configs/evaluation_protocol_v1_1.yaml"
PARTITIONS = "reports/subject_partitions_v2.csv"
B0_NORMS = {
    "D1_SLEEPEDF_TO_ISRUC": "artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json",
    "D2_ISRUC_TO_SLEEPEDF": "artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json",
}
EXPECTED_HASHES = {
    B1_MODEL_CONFIG: "b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6",
    B1_TRAINING_CONFIG: "467ed74d465a65990388f4ac4f271311ccb156605cc1cfef1d4339057298bbc7",
    "docs/baseline_b1_moddrop_protocol_v1.md": "7db8bc63f21df1ea53fb58d881c8e4996651e57e1c8fd154283b1d273caa2c1c",
    EVAL_CONFIG: "dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756",
    PARTITIONS: "9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329",
    B0_MODEL_CONFIG: "a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17",
    "configs/training_b0_v1.yaml": "2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7",
    B0_NORMS["D1_SLEEPEDF_TO_ISRUC"]: "be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3",
    B0_NORMS["D2_ISRUC_TO_SLEEPEDF"]: "3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def verify_preflight() -> dict[str, str]:
    gate = json.loads((ROOT / "reports/step13_b1_protocol_gate.json").read_text(encoding="utf-8"))
    if gate.get("protocol_gate") != "B1_PROTOCOL_FROZEN":
        raise RuntimeError("STEP14_FROZEN_ARTIFACT_MISMATCH: Step 13 protocol gate")
    actual = {}
    for relative, expected in EXPECTED_HASHES.items():
        path = ROOT / relative
        actual[relative] = sha256_file(path)
        if actual[relative] != expected:
            raise RuntimeError(f"STEP14_FROZEN_ARTIFACT_MISMATCH: {relative}")
    forbidden = []
    for pattern in (
        "artifacts/models/b1_moddrop/**/*.pt",
        "artifacts/predictions/b1_moddrop/**/*",
        "artifacts/normalization/b1/**/*",
        "artifacts/calibration/b1_moddrop/**/*",
    ):
        forbidden.extend(ROOT.glob(pattern))
    if forbidden:
        raise RuntimeError("STEP14_FROZEN_ARTIFACT_MISMATCH: pre-existing B1 output")
    if count_trainable_parameters(BaselineB0()) != EXPECTED_PARAM_COUNT:
        raise RuntimeError("B1_PARAMETER_COUNT_MISMATCH")
    return actual


def stable_keys(batch: dict[str, Any]) -> list[str]:
    return [
        f"{dataset}|{subject}|{recording}|{int(epoch)}"
        for dataset, subject, recording, epoch in zip(
            batch["dataset"], batch["subject_id"], batch["recording_id"], batch["epoch_index"]
        )
    ]


def train_epoch(model: BaselineB0, loader: DataLoader, optimizer: torch.optim.Optimizer, device: torch.device, epoch: int) -> tuple[dict[str, float], dict[str, int]]:
    if loader.dataset.role != "TRAIN":
        raise RuntimeError("STEP14_DATA_FIREWALL_VIOLATION")
    model.train()
    criterion = nn.CrossEntropyLoss(weight=None, label_smoothing=0.0)
    total_loss = 0.0
    total = 0
    gradient_norm = float("nan")
    counts = {(1, 1): 0, (1, 0): 0, (0, 1): 0, (0, 0): 0}
    for batch in loader:
        masks_list = assign_masks(EXPOSURE_SEED, epoch, stable_keys(batch))
        masks = torch.tensor(masks_list, dtype=torch.float32, device=device)
        for mask in masks_list:
            counts[mask] = counts.get(mask, 0) + 1
        eeg, eog = apply_missing_modality_zeroing(batch["eeg"].to(device), batch["eog"].to(device), masks)
        labels = batch["label"].to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(eeg, eog, masks)
        loss = criterion(logits, labels)
        if not torch.isfinite(loss):
            raise FloatingPointError("B1_SOURCE_TRAINING_BLOCKED: non-finite loss")
        loss.backward()
        gradient_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        if not torch.isfinite(gradient_norm):
            raise FloatingPointError("B1_SOURCE_TRAINING_BLOCKED: non-finite gradient")
        optimizer.step()
        n = int(labels.shape[0])
        total_loss += float(loss.detach()) * n
        total += n
    if total == 0:
        raise RuntimeError("empty SOURCE TRAIN loader")
    return {"train_cross_entropy": total_loss / total, "gradient_norm": float(gradient_norm)}, {
        "total_exposures": total,
        "full_count": counts[(1, 1)],
        "eeg_only_count": counts[(1, 0)],
        "eog_only_count": counts[(0, 1)],
        "forbidden_count": counts[(0, 0)],
    }


def evaluate_dev(model: BaselineB0, loader: DataLoader, device: torch.device) -> dict[str, float]:
    if loader.dataset.role != "DEV":
        raise RuntimeError("STEP14_DATA_FIREWALL_VIOLATION")
    model.eval()
    criterion = nn.CrossEntropyLoss(weight=None, label_smoothing=0.0)
    confusion = torch.zeros((5, 5), dtype=torch.long)
    nll = 0.0
    total = 0
    with torch.no_grad():
        for batch in loader:
            labels = batch["label"].to(device)
            mask = torch.ones((labels.shape[0], 2), dtype=torch.float32, device=device)
            logits = model(batch["eeg"].to(device), batch["eog"].to(device), mask)
            loss = criterion(logits, labels)
            if not torch.isfinite(loss):
                raise FloatingPointError("B1_SOURCE_TRAINING_BLOCKED: non-finite DEV NLL")
            pred = logits.argmax(dim=1)
            for truth, prediction in zip(labels.cpu(), pred.cpu()):
                confusion[int(truth), int(prediction)] += 1
            count = int(labels.shape[0])
            nll += float(loss) * count
            total += count
    recalls = confusion.diag().float() / confusion.sum(dim=1).clamp_min(1).float()
    precision = confusion.diag().float() / confusion.sum(dim=0).clamp_min(1).float()
    f1 = 2 * precision * recalls / (precision + recalls).clamp_min(1e-12)
    return {"dev_macro_f1": float(f1.mean()), "dev_nll": nll / total}


def memory_gate(device: torch.device, train_dataset: Any) -> None:
    loader = DataLoader(train_dataset, batch_size=128, shuffle=False, num_workers=0, pin_memory=device.type == "cuda")
    batch = next(iter(loader))
    model = BaselineB0().to(device).float()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4, betas=(0.9, 0.999), eps=1e-8)
    labels = batch["label"].to(device)
    eeg = batch["eeg"].to(device)
    eog = batch["eog"].to(device)
    mask = torch.ones((labels.shape[0], 2), dtype=torch.float32, device=device)
    try:
        logits = model(eeg, eog, mask)
        loss = nn.CrossEntropyLoss()(logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    except RuntimeError as exc:
        if "out of memory" in str(exc).lower():
            raise RuntimeError("B1_BATCH_MEMORY_BLOCKED") from exc
        raise
    finally:
        del model, optimizer, batch
        if device.type == "cuda":
            torch.cuda.empty_cache()


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def train_run(experiment: str, seed: int, frozen_hashes: dict[str, str], device: torch.device) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, str]]]:
    seed_everything(seed)
    norm_path = ROOT / B0_NORMS[experiment]
    norm = json.loads(norm_path.read_text(encoding="utf-8"))
    normalization = {
        "EEG": {"mean": norm["EEG_mean"], "std": norm["EEG_std"], "std_epsilon": norm["epsilon"]},
        "EOG": {"mean": norm["EOG_mean"], "std": norm["EOG_std"], "std_epsilon": norm["epsilon"]},
    }
    train = build_source_dataset(experiment, "TRAIN", "train", root=ROOT)
    dev = build_source_dataset(experiment, "DEV", "dev", root=ROOT)
    train.set_normalization(normalization)
    dev.set_normalization(normalization)
    run_dir = ROOT / "artifacts/models/b1_moddrop" / experiment / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "normalization_reference.json").write_text(json.dumps({"path": B0_NORMS[experiment], "sha256": sha256_file(norm_path)}, indent=2) + "\n", encoding="utf-8")
    batch_size = 128
    dev_loader = DataLoader(dev, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=device.type == "cuda")
    model = BaselineB0().to(device).float()
    if count_trainable_parameters(model) != EXPECTED_PARAM_COUNT:
        raise RuntimeError("B1_PARAMETER_COUNT_MISMATCH")
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4, betas=(0.9, 0.999), eps=1e-8)
    selector = CheckpointSelector(patience=6, min_epochs=5, tolerance=1e-6)
    history = []
    exposure = []
    started = time.perf_counter()
    for epoch in range(1, 31):
        loader = DataLoader(train, batch_size=batch_size, shuffle=True, generator=make_epoch_generator(seed, epoch), num_workers=0, pin_memory=device.type == "cuda")
        epoch_started = time.perf_counter()
        train_stats, exposure_counts = train_epoch(model, loader, optimizer, device, epoch)
        dev_stats = evaluate_dev(model, dev_loader, device)
        selected = selector.observe(epoch, dev_stats["dev_macro_f1"], dev_stats["dev_nll"])
        history.append({"epoch": epoch, **train_stats, **dev_stats, "learning_rate": optimizer.param_groups[0]["lr"], "checkpoint_selected": selected, "elapsed_seconds": time.perf_counter() - epoch_started})
        total = exposure_counts["total_exposures"]
        exposure.append({"epoch": epoch, **exposure_counts, "full_fraction": exposure_counts["full_count"] / total, "eeg_only_fraction": exposure_counts["eeg_only_count"] / total, "eog_only_fraction": exposure_counts["eog_only_count"] / total})
        if exposure_counts["forbidden_count"] != 0:
            raise RuntimeError("B1_SOURCE_TRAINING_BLOCKED: forbidden mask")
        if selected:
            metadata = {
                "baseline_id": "B1_B0_ARCH_SOURCE_MODALITY_DROPOUT",
                "architecture_id": "B0_DUAL_BRANCH_RAW_CNN",
                "experiment_id": experiment,
                "model_seed": seed,
                "selected_epoch": epoch,
                "selected_dev_macro_f1": dev_stats["dev_macro_f1"],
                "selected_dev_nll": dev_stats["dev_nll"],
                "class_order": list(CLASS_ORDER),
                "b1_model_config_sha256": frozen_hashes[B1_MODEL_CONFIG],
                "b1_training_config_sha256": frozen_hashes[B1_TRAINING_CONFIG],
                "b0_model_config_sha256": frozen_hashes[B0_MODEL_CONFIG],
                "normalization_sha256": sha256_file(norm_path),
                "evaluation_protocol_sha256": frozen_hashes[EVAL_CONFIG],
                "subject_partition_sha256": frozen_hashes[PARTITIONS],
                "exposure_seed": EXPOSURE_SEED,
                "exposure_policy": "FULL_0.50_EEG_ONLY_0.25_EOG_ONLY_0.25",
                "epoch_convention": "1_BASED",
                "pytorch_version": torch.__version__,
                "cuda_version": torch.version.cuda,
                "cudnn_version": torch.backends.cudnn.version(),
                "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
                "git_commit": git_commit(),
            }
            torch.save({"model_state_dict": model.state_dict(), "metadata": metadata}, run_dir / "best.pt")
        if selector.should_stop(epoch):
            break
    if selector.best is None:
        raise RuntimeError("B1_SOURCE_TRAINING_BLOCKED: no checkpoint selected")
    checkpoint_path = run_dir / "best.pt"
    checkpoint_hash = sha256_file(checkpoint_path)
    cumulative = {key: sum(row[key] for row in exposure) for key in ("total_exposures", "full_count", "eeg_only_count", "eog_only_count", "forbidden_count")}
    cumulative["full_fraction"] = cumulative["full_count"] / cumulative["total_exposures"]
    cumulative["eeg_only_fraction"] = cumulative["eeg_only_count"] / cumulative["total_exposures"]
    cumulative["eog_only_fraction"] = cumulative["eog_only_count"] / cumulative["total_exposures"]
    history_fields = ["epoch", "train_cross_entropy", "dev_macro_f1", "dev_nll", "learning_rate", "gradient_norm", "checkpoint_selected", "elapsed_seconds"]
    exposure_fields = ["epoch", "total_exposures", "full_count", "eeg_only_count", "eog_only_count", "forbidden_count", "full_fraction", "eeg_only_fraction", "eog_only_fraction"]
    write_csv(run_dir / "training_history.csv", history, history_fields)
    write_csv(run_dir / "modality_exposure_history.csv", exposure, exposure_fields)
    target_name = "isruc_s1" if experiment.startswith("D1") else "sleep_edf_sc"
    manifest = {
        "baseline_id": "B1_B0_ARCH_SOURCE_MODALITY_DROPOUT",
        "architecture_id": "B0_DUAL_BRANCH_RAW_CNN",
        "experiment_id": experiment,
        "source_dataset": train.dataset,
        "target_dataset_provenance_only": target_name,
        "model_seed": seed,
        "selected_epoch": selector.best["epoch"],
        "epochs_executed": len(history),
        "stop_reason": "EARLY_STOPPING" if len(history) < 30 else "MAX_EPOCHS",
        "selected_dev_macro_f1": selector.best["macro_f1"],
        "selected_dev_nll": selector.best["nll"],
        "b1_model_config_sha256": frozen_hashes[B1_MODEL_CONFIG],
        "b1_training_config_sha256": frozen_hashes[B1_TRAINING_CONFIG],
        "b0_model_config_sha256": frozen_hashes[B0_MODEL_CONFIG],
        "evaluation_protocol_sha256": frozen_hashes[EVAL_CONFIG],
        "subject_partition_sha256": frozen_hashes[PARTITIONS],
        "normalization_sha256": sha256_file(norm_path),
        "exposure_seed": EXPOSURE_SEED,
        "epoch_convention": "1_BASED",
        **{f"cumulative_{k}": v for k, v in cumulative.items()},
        "checkpoint_sha256": checkpoint_hash,
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "cudnn_version": torch.backends.cudnn.version(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "git_commit": git_commit(),
        "wall_clock_training_seconds": time.perf_counter() - started,
        "restart_count": 0,
    }
    manifest_path = run_dir / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    reload_checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    reload_model = BaselineB0().to(device).float()
    reload_model.load_state_dict(reload_checkpoint["model_state_dict"])
    reload_model.eval()
    batch = next(iter(dev_loader))
    with torch.no_grad():
        logits = reload_model(batch["eeg"].to(device), batch["eog"].to(device), torch.ones((batch["label"].shape[0], 2), device=device))
    if not torch.isfinite(logits).all() or any(not torch.isfinite(p).all() for p in reload_model.parameters()):
        raise FloatingPointError("B1_SOURCE_TRAINING_BLOCKED: checkpoint reload non-finite")
    events = train.access_events + dev.access_events
    summary = {
        "baseline_id": "B1_B0_ARCH_SOURCE_MODALITY_DROPOUT", "experiment_id": experiment, "seed": seed,
        "source_dataset": train.dataset, "selected_epoch": selector.best["epoch"], "epochs_executed": len(history),
        "stop_reason": manifest["stop_reason"], "selected_dev_macro_f1": selector.best["macro_f1"], "selected_dev_nll": selector.best["nll"],
        "final_train_ce": history[-1]["train_cross_entropy"], "cumulative_full_exposures": cumulative["full_count"],
        "cumulative_eeg_only_exposures": cumulative["eeg_only_count"], "cumulative_eog_only_exposures": cumulative["eog_only_count"],
        "cumulative_forbidden_exposures": cumulative["forbidden_count"], "full_fraction": cumulative["full_fraction"],
        "eeg_only_fraction": cumulative["eeg_only_fraction"], "eog_only_fraction": cumulative["eog_only_fraction"],
        "checkpoint_sha256": checkpoint_hash, "normalization_sha256": sha256_file(norm_path),
        "run_manifest_sha256": sha256_file(manifest_path), "training_seconds": manifest["wall_clock_training_seconds"], "status": "COMPLETE",
    }
    return summary, events, exposure


def main() -> None:
    frozen_hashes = verify_preflight()
    if not torch.cuda.is_available():
        raise RuntimeError("B1_BATCH_MEMORY_BLOCKED: CUDA unavailable")
    device = torch.device("cuda:0")
    memory_train = build_source_dataset(EXPERIMENTS[0], "TRAIN", "train", root=ROOT)
    memory_norm = json.loads((ROOT / B0_NORMS[EXPERIMENTS[0]]).read_text(encoding="utf-8"))
    memory_train.set_normalization({"EEG": {"mean": memory_norm["EEG_mean"], "std": memory_norm["EEG_std"], "std_epsilon": memory_norm["epsilon"]}, "EOG": {"mean": memory_norm["EOG_mean"], "std": memory_norm["EOG_std"], "std_epsilon": memory_norm["epsilon"]}})
    memory_gate(device, memory_train)
    summaries, events, exposure_rows = [], [], []
    for experiment in EXPERIMENTS:
        for seed in SEEDS:
            print(json.dumps({"stage": "START", "experiment_id": experiment, "seed": seed}, sort_keys=True), flush=True)
            summary, run_events, run_exposure = train_run(experiment, seed, frozen_hashes, device)
            summaries.append(summary)
            events.extend(run_events)
            exposure_rows.append({"experiment_id": experiment, "seed": seed, **{f"expected_{k}": v for k, v in {"full_fraction": 0.5, "eeg_only_fraction": 0.25, "eog_only_fraction": 0.25}.items()}, "total_exposures": sum(r["total_exposures"] for r in run_exposure), "full_count": sum(r["full_count"] for r in run_exposure), "eeg_only_count": sum(r["eeg_only_count"] for r in run_exposure), "eog_only_count": sum(r["eog_only_count"] for r in run_exposure), "forbidden_count": sum(r["forbidden_count"] for r in run_exposure), "full_fraction": sum(r["full_count"] for r in run_exposure) / sum(r["total_exposures"] for r in run_exposure), "eeg_only_fraction": sum(r["eeg_only_count"] for r in run_exposure) / sum(r["total_exposures"] for r in run_exposure), "eog_only_fraction": sum(r["eog_only_count"] for r in run_exposure) / sum(r["total_exposures"] for r in run_exposure)})
            print(json.dumps({"stage": "COMPLETE", **summary}, sort_keys=True), flush=True)
            if device.type == "cuda":
                torch.cuda.empty_cache()
    summary_fields = list(summaries[0])
    write_csv(ROOT / "reports/b1_training_summary_v1.csv", summaries, summary_fields)
    lines = ["experiment_id,seed,relative_path,sha256"]
    for row in summaries:
        lines.append(f"{row['experiment_id']},{row['seed']},artifacts/models/b1_moddrop/{row['experiment_id']}/seed_{row['seed']}/best.pt,{row['checkpoint_sha256']}")
    (ROOT / "reports/b1_checkpoint_hashes_v1.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    exposure_fields = ["experiment_id", "seed", "expected_full_fraction", "expected_eeg_only_fraction", "expected_eog_only_fraction", "total_exposures", "full_count", "eeg_only_count", "eog_only_count", "forbidden_count", "full_fraction", "eeg_only_fraction", "eog_only_fraction"]
    write_csv(ROOT / "reports/b1_modality_exposure_summary_v1.csv", exposure_rows, exposure_fields)
    unique = {(e["dataset"], e["source_role"], e["purpose"], e["subject_id"], e["recording_id"], e["path"]): e for e in events}
    audit_fields = ["dataset", "source_role", "purpose", "subject_id", "recording_id", "path"]
    write_csv(ROOT / "reports/step14_data_access_audit.csv", list(unique.values()), audit_fields)
    forbidden = [e for e in unique.values() if e["source_role"] not in {"TRAIN", "DEV"} or e["purpose"] not in {"train", "dev"}]
    if forbidden:
        raise RuntimeError("STEP14_DATA_FIREWALL_VIOLATION")
    print(json.dumps({"status": "B1_SOURCE_TRAINING_COMPLETE", "runs": len(summaries), "access_rows": len(unique)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
