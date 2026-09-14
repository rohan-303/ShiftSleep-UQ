#!/usr/bin/env python
"""Future B0 source-training entrypoint.

Step 9 deliberately does not invoke this script. Passing --execute is required
for a future Step 10 run and still accepts only frozen experiment IDs/seeds.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
import yaml
from torch.utils.data import DataLoader

from shiftsleep_uq.models.baseline_b0 import BaselineB0
from shiftsleep_uq.training.checkpointing import CheckpointSelector, build_run_manifest
from shiftsleep_uq.training.datasets import build_source_dataset
from shiftsleep_uq.training.engine import evaluate_source_dev, train_one_epoch
from shiftsleep_uq.training.normalization import fit_source_train_dataset
from shiftsleep_uq.training.reproducibility import make_epoch_generator, seed_everything


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-id", required=True, choices=["D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF"])
    parser.add_argument("--seed", required=True, type=int, choices=[17, 42, 2026])
    parser.add_argument("--root", default=".")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--execute", action="store_true", help="required; Step 10 only")
    return parser.parse_args()


def resolve_device(requested: str) -> torch.device:
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA but CUDA is unavailable")
    return torch.device("cuda" if requested == "auto" and torch.cuda.is_available() else requested if requested != "auto" else "cpu")


def main() -> None:
    args = parse_args()
    if not args.execute:
        raise SystemExit("training is intentionally disabled during Step 9; pass --execute in Step 10")
    root = Path(args.root)
    training_config = yaml.safe_load((root / "configs/training_b0_v1.yaml").read_text(encoding="utf-8"))
    seed_everything(args.seed)
    device = resolve_device(args.device)
    train_dataset = build_source_dataset(args.experiment_id, "TRAIN", "train", root=root)
    dev_dataset = build_source_dataset(args.experiment_id, "DEV", "dev", root=root)
    normalization = fit_source_train_dataset(train_dataset, role="TRAIN", std_epsilon=training_config["normalization"]["std_epsilon"])
    train_dataset.set_normalization(normalization)
    dev_dataset.set_normalization(normalization)
    normalization_path = root / "artifacts/models/b0" / args.experiment_id / f"seed_{args.seed}" / "normalization.json"
    normalization_path.parent.mkdir(parents=True, exist_ok=True)
    normalization_path.write_text(json.dumps(normalization, indent=2), encoding="utf-8")
    dev_loader = DataLoader(dev_dataset, batch_size=training_config["batch_size"]["physical"], shuffle=False, num_workers=0)
    model = BaselineB0().to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=training_config["optimizer"]["learning_rate"],
        weight_decay=training_config["optimizer"]["weight_decay"],
        betas=tuple(training_config["optimizer"]["betas"]),
        eps=training_config["optimizer"]["eps"],
    )
    selector = CheckpointSelector(
        patience=training_config["early_stopping"]["patience"],
        min_epochs=training_config["minimum_epochs"],
        tolerance=training_config["early_stopping"]["tolerance"],
    )
    history = []
    checkpoint_root = root / "artifacts/models/b0" / args.experiment_id / f"seed_{args.seed}"
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    for epoch in range(1, training_config["max_epochs"] + 1):
        epoch_started = time.perf_counter()
        train_loader = DataLoader(
            train_dataset,
            batch_size=training_config["batch_size"]["physical"],
            shuffle=True,
            generator=make_epoch_generator(args.seed, epoch),
            num_workers=0,
        )
        train_stats = train_one_epoch(model, train_loader, optimizer, device=device)
        dev_stats = evaluate_source_dev(model, dev_loader, device=device)
        selected = selector.observe(epoch, dev_stats["macro_f1"], dev_stats["nll"])
        history.append({
            "epoch": epoch,
            **train_stats,
            **dev_stats,
            "learning_rate": optimizer.param_groups[0]["lr"],
            "elapsed_training_seconds": time.perf_counter() - epoch_started,
            "checkpoint_selected": selected,
        })
        if selected:
            torch.save({"model_state_dict": model.state_dict(), "epoch": epoch, "dev": dev_stats}, checkpoint_root / "best.pt")
        if selector.should_stop(epoch):
            break
    (checkpoint_root / "training_history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    manifest = build_run_manifest(
        baseline_id="B0_DUAL_BRANCH_RAW_CNN",
        experiment_id=args.experiment_id,
        source_dataset=train_dataset.dataset,
        seed=args.seed,
        selected_epoch=selector.best["epoch"] if selector.best else None,
        protocol_version="1.1.0",
        data_contract_version="1.2.0",
        preprocessing_version="0.1.0",
    )
    (checkpoint_root / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
