"""B0 dual-branch raw-signal CNN baseline.

This module implements the frozen epoch-wise architecture only. It performs no
training, calibration, prediction export, or data access.
"""
from __future__ import annotations

from collections.abc import Sequence

import torch
from torch import Tensor, nn

CLASS_ORDER = ("Wake", "N1", "N2", "N3", "REM")
CONDITION_MASKS = {
    "C0": (1, 1),
    "C1": (1, 0),
    "C2": (0, 1),
    "C3": (1, 1),
    "C4": (1, 0),
    "C5": (0, 1),
}


def condition_mask(condition_id: str) -> tuple[int, int]:
    try:
        return CONDITION_MASKS[condition_id]
    except KeyError as exc:
        raise ValueError(f"unknown condition: {condition_id}") from exc


def _validate_mask(mask: Tensor, batch_size: int) -> Tensor:
    if mask.ndim == 1:
        mask = mask.unsqueeze(0).expand(batch_size, -1)
    if mask.shape != (batch_size, 2):
        raise ValueError(f"modality mask must have shape [{batch_size}, 2]")
    if not torch.all((mask == 0) | (mask == 1)):
        raise ValueError("modality mask values must be binary")
    if torch.any(mask.sum(dim=1) == 0):
        raise ValueError("[0, 0] modality mask is forbidden")
    return mask


class ResidualBlock1D(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, stride: int) -> None:
        super().__init__()
        padding = kernel_size // 2
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding, bias=False)
        self.norm1 = nn.GroupNorm(8, out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, 1, padding, bias=False)
        self.norm2 = nn.GroupNorm(8, out_channels)
        self.shortcut = (
            nn.Sequential(
                nn.Conv1d(in_channels, out_channels, 1, stride, bias=False),
                nn.GroupNorm(8, out_channels),
            )
            if in_channels != out_channels or stride != 1
            else nn.Identity()
        )
        self.activation = nn.GELU()

    def forward(self, x: Tensor) -> Tensor:
        residual = self.shortcut(x)
        x = self.activation(self.norm1(self.conv1(x)))
        x = self.norm2(self.conv2(x))
        return self.activation(x + residual)


class RawSignalEncoder(nn.Module):
    def __init__(self, *, eog: bool = False) -> None:
        super().__init__()
        kernel = 25 if eog else 51
        padding = 12 if eog else 25
        self.stem = nn.Sequential(
            nn.Conv1d(1, 32, kernel, stride=2, padding=padding, bias=False),
            nn.GroupNorm(8, 32),
            nn.GELU(),
            nn.MaxPool1d(kernel_size=4, stride=4),
        )
        self.blocks = nn.Sequential(
            ResidualBlock1D(32, 64, 7, 2),
            ResidualBlock1D(64, 128, 5, 2),
            ResidualBlock1D(128, 128, 3, 2),
        )
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.projection = nn.Sequential(nn.Linear(128, 128), nn.GELU(), nn.Dropout(0.20))

    def forward(self, x: Tensor) -> Tensor:
        x = self.blocks(self.stem(x))
        x = self.pool(x).flatten(1)
        return self.projection(x)


class BaselineB0(nn.Module):
    """B0_DUAL_BRANCH_RAW_CNN; returns raw five-class logits."""

    baseline_id = "B0_DUAL_BRANCH_RAW_CNN"
    class_order = CLASS_ORDER

    def __init__(self) -> None:
        super().__init__()
        self.eeg_encoder = RawSignalEncoder(eog=False)
        self.eog_encoder = RawSignalEncoder(eog=True)
        self.head = nn.Sequential(
            nn.Linear(256, 128),
            nn.GELU(),
            nn.Dropout(0.30),
            nn.Linear(128, 5),
        )
        self.reset_parameters()

    def reset_parameters(self) -> None:
        for module in self.modules():
            if isinstance(module, (nn.Conv1d, nn.Linear)):
                nn.init.kaiming_normal_(module.weight, nonlinearity="relu")
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.GroupNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)

    def forward(self, eeg: Tensor, eog: Tensor, modality_mask: Tensor | Sequence[int]) -> Tensor:
        if eeg.ndim != 3 or eeg.shape[1:] != (1, 3000):
            raise ValueError("EEG must have shape [B, 1, 3000]")
        if eog.ndim != 3 or eog.shape[1:] != (1, 1500):
            raise ValueError("EOG must have shape [B, 1, 1500]")
        if eeg.shape[0] != eog.shape[0]:
            raise ValueError("EEG and EOG batch sizes must match")
        mask = torch.as_tensor(modality_mask, device=eeg.device, dtype=eeg.dtype)
        mask = _validate_mask(mask, eeg.shape[0])
        z_eeg = self.eeg_encoder(eeg) * mask[:, 0:1]
        z_eog = self.eog_encoder(eog) * mask[:, 1:2]
        return self.head(torch.cat([z_eeg, z_eog], dim=1))


def count_trainable_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
