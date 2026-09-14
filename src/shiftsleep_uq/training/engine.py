"""Leak-safe B0 training/evaluation primitives for future Step 10 runs."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import torch
from torch import nn

from .checkpointing import CheckpointSelector
from .datasets import RoleAccessError


def _require_dataset_role(loader: Any, role: str) -> None:
    actual = getattr(getattr(loader, "dataset", None), "role", None)
    if actual != role:
        raise RoleAccessError(f"loader role {actual!r} is not permitted; expected {role!r}")


def train_one_epoch(
    model: nn.Module,
    loader: Iterable[dict[str, Any]],
    optimizer: torch.optim.Optimizer,
    *,
    device: torch.device,
    max_grad_norm: float = 1.0,
) -> dict[str, float]:
    _require_dataset_role(loader, "TRAIN")
    model.train()
    criterion = nn.CrossEntropyLoss(weight=None, label_smoothing=0.0)
    total_loss = 0.0
    total_items = 0
    for batch in loader:
        optimizer.zero_grad(set_to_none=True)
        logits = model(
            batch["eeg"].to(device),
            batch["eog"].to(device),
            torch.ones((batch["label"].shape[0], 2), device=device),
        )
        loss = criterion(logits, batch["label"].to(device))
        if not torch.isfinite(loss):
            raise FloatingPointError("non-finite training loss")
        loss.backward()
        gradient_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        if not torch.isfinite(gradient_norm):
            raise FloatingPointError("non-finite gradient norm")
        optimizer.step()
        count = int(batch["label"].shape[0])
        total_loss += float(loss.detach()) * count
        total_items += count
    if total_items == 0:
        raise ValueError("empty TRAIN loader")
    return {"train_cross_entropy": total_loss / total_items, "gradient_norm": float(gradient_norm)}


def evaluate_source_dev(model: nn.Module, loader: Iterable[dict[str, Any]], *, device: torch.device) -> dict[str, float]:
    _require_dataset_role(loader, "DEV")
    model.eval()
    criterion = nn.CrossEntropyLoss(weight=None, label_smoothing=0.0)
    confusion = torch.zeros((5, 5), dtype=torch.long)
    total_nll = 0.0
    total_items = 0
    with torch.no_grad():
        for batch in loader:
            labels = batch["label"].to(device)
            logits = model(
                batch["eeg"].to(device),
                batch["eog"].to(device),
                torch.ones((labels.shape[0], 2), device=device),
            )
            loss = criterion(logits, labels)
            predictions = logits.argmax(dim=1)
            for truth, prediction in zip(labels.cpu(), predictions.cpu()):
                confusion[int(truth), int(prediction)] += 1
            count = int(labels.shape[0])
            total_nll += float(loss) * count
            total_items += count
    if total_items == 0:
        raise ValueError("empty DEV loader")
    recalls = confusion.diag().float() / confusion.sum(dim=1).clamp_min(1).float()
    predicted_totals = confusion.sum(dim=0).float()
    precision = confusion.diag().float() / predicted_totals.clamp_min(1.0)
    f1 = 2.0 * precision * recalls / (precision + recalls).clamp_min(1e-12)
    return {"macro_f1": float(f1.mean()), "nll": total_nll / total_items}


def should_stop_after_observation(selector: CheckpointSelector, epoch: int) -> bool:
    return selector.should_stop(epoch)
