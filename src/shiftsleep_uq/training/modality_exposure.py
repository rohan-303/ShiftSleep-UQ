"""Deterministic source-training modality exposure for B1.

This module assigns training masks from immutable sample identity, epoch, and a
frozen exposure seed only. It never consumes labels, model outputs, or signal
values.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Iterable, Sequence

import torch
from torch import Tensor

EXPOSURE_SEED = 2029
FULL = (1, 1)
EEG_ONLY = (1, 0)
EOG_ONLY = (0, 1)
ALLOWED_MASKS = (FULL, EEG_ONLY, EOG_ONLY)
EXPOSURE_PROBABILITIES = {FULL: 0.50, EEG_ONLY: 0.25, EOG_ONLY: 0.25}


def _canonical_key(exposure_seed: int, epoch: int, sample_key: str) -> bytes:
    if not isinstance(exposure_seed, int) or not isinstance(epoch, int):
        raise TypeError("exposure_seed and epoch must be integers")
    if epoch < 0:
        raise ValueError("epoch must be non-negative")
    if not isinstance(sample_key, str) or not sample_key:
        raise ValueError("sample_key must be a non-empty string")
    return f"{exposure_seed}\x1f{epoch}\x1f{sample_key}".encode("utf-8")


def uniform_value(exposure_seed: int, epoch: int, sample_key: str) -> float:
    """Return a stable u in [0, 1) using the first 64 SHA-256 bits (big-endian)."""
    digest = hashlib.sha256(_canonical_key(exposure_seed, epoch, sample_key)).digest()
    integer = int.from_bytes(digest[:8], byteorder="big", signed=False)
    return integer / float(1 << 64)


def assign_mask(exposure_seed: int, epoch: int, sample_key: str, *, label: object | None = None) -> tuple[int, int]:
    """Assign FULL/EEG_ONLY/EOG_ONLY; ``label`` is accepted only for audit tests."""
    del label
    value = uniform_value(exposure_seed, epoch, sample_key)
    if value < 0.50:
        return FULL
    if value < 0.75:
        return EEG_ONLY
    return EOG_ONLY


def assign_masks(exposure_seed: int, epoch: int, sample_keys: Iterable[str]) -> list[tuple[int, int]]:
    return [assign_mask(exposure_seed, epoch, key) for key in sample_keys]


def mask_distribution(exposure_seed: int, epoch: int, sample_keys: Iterable[str]) -> Counter[tuple[int, int]]:
    return Counter(assign_masks(exposure_seed, epoch, sample_keys))


def apply_missing_modality_zeroing(eeg: Tensor, eog: Tensor, modality_mask: Tensor | Sequence[int]) -> tuple[Tensor, Tensor]:
    """Zero unavailable normalized branches without modifying available values."""
    if eeg.ndim < 1 or eog.ndim < 1 or eeg.shape[0] != eog.shape[0]:
        raise ValueError("EEG and EOG batch dimensions must match")
    mask = torch.as_tensor(modality_mask, device=eeg.device, dtype=eeg.dtype)
    if mask.ndim == 1:
        mask = mask.unsqueeze(0).expand(eeg.shape[0], -1)
    if mask.shape != (eeg.shape[0], 2) or not torch.all((mask == 0) | (mask == 1)) or torch.any(mask.sum(dim=1) == 0):
        raise ValueError("modality_mask must be [B,2], binary, and cannot contain [0,0]")
    return eeg * mask[:, 0].reshape(-1, *([1] * (eeg.ndim - 1))), eog * mask[:, 1].reshape(-1, *([1] * (eog.ndim - 1)))
