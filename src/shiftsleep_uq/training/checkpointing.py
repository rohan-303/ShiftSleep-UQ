"""Frozen source-DEV checkpoint selection rules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def is_better(candidate: dict[str, float | int], incumbent: dict[str, float | int] | None, tolerance: float = 1e-6) -> bool:
    if incumbent is None:
        return True
    macro_delta = float(candidate["macro_f1"]) - float(incumbent["macro_f1"])
    if macro_delta > tolerance:
        return True
    if macro_delta < -tolerance:
        return False
    nll_delta = float(candidate["nll"]) - float(incumbent["nll"])
    if nll_delta < -tolerance:
        return True
    if nll_delta > tolerance:
        return False
    return int(candidate["epoch"]) < int(incumbent["epoch"])


@dataclass
class CheckpointSelector:
    patience: int = 6
    min_epochs: int = 5
    tolerance: float = 1e-6
    best: dict[str, float | int] | None = None
    stale_epochs: int = 0

    def observe(self, epoch: int, macro_f1: float, nll: float) -> bool:
        candidate = {"epoch": epoch, "macro_f1": macro_f1, "nll": nll}
        if is_better(candidate, self.best, self.tolerance):
            self.best = candidate
            self.stale_epochs = 0
            return True
        self.stale_epochs += 1
        return False

    def should_stop(self, epoch: int) -> bool:
        return epoch >= self.min_epochs and self.stale_epochs >= self.patience

    def state_dict(self) -> dict[str, Any]:
        return {"best": self.best, "stale_epochs": self.stale_epochs}


def checkpoint_path(root: str, experiment_id: str, seed: int) -> str:
    return f"{root}/artifacts/models/b0/{experiment_id}/seed_{seed}/best.pt"


def build_run_manifest(**metadata: Any) -> dict[str, Any]:
    forbidden = {key for key in metadata if "target" in key.lower() and metadata[key] is not None}
    if forbidden:
        raise ValueError(f"target metrics/metadata are forbidden in training checkpoint metadata: {sorted(forbidden)}")
    return metadata
