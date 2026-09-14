"""Leak-safe source-role dataset access for B0 infrastructure."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import Dataset

from .normalization import apply_normalization


class RoleAccessError(PermissionError):
    pass


_ALLOWED_PURPOSE_ROLES = {
    "train": {"TRAIN"},
    "normalization_fit": {"TRAIN"},
    "dev": {"DEV"},
    "calibration": {"CALIBRATION"},
    "test": {"TEST"},
}


def assert_role_allowed(role: str, purpose: str) -> None:
    allowed = _ALLOWED_PURPOSE_ROLES.get(purpose)
    if allowed is None:
        raise RoleAccessError(f"unknown dataset purpose: {purpose}")
    if role not in allowed:
        raise RoleAccessError(f"role {role} is not allowed for purpose {purpose}")


def source_dataset_for_experiment(experiment_id: str) -> str:
    mapping = {
        "D1_SLEEPEDF_TO_ISRUC": "sleep_edf_sc",
        "D2_ISRUC_TO_SLEEPEDF": "isruc_s1",
    }
    try:
        return mapping[experiment_id]
    except KeyError as exc:
        raise ValueError(f"unknown experiment_id: {experiment_id}") from exc


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ManifestEpochDataset(Dataset[dict[str, Any]]):
    """Epoch dataset restricted to one frozen source dataset and source role."""

    def __init__(self, dataset: str, role: str, purpose: str, *, root: str | Path = ".") -> None:
        assert_role_allowed(role, purpose)
        self.root = Path(root)
        self.dataset = dataset
        self.role = role
        self.purpose = purpose
        partition_rows = _read_csv(self.root / "reports/subject_partitions_v2.csv")
        subjects = {
            row["subject_id"]
            for row in partition_rows
            if row["dataset"] == dataset and row["source_role"] == role
        }
        if not subjects:
            raise ValueError(f"no frozen subjects for dataset={dataset}, role={role}")
        manifest_path = (
            self.root / "reports/core_recording_manifest_v1_1.csv"
            if dataset == "sleep_edf_sc"
            else self.root / "reports/isruc_original_recording_manifest_v2.csv"
        )
        records = [
            row
            for row in _read_csv(manifest_path)
            if row.get("subject_id") in subjects and row.get("terminal_status") == "INCLUDED"
        ]
        if not records:
            raise ValueError(f"no included records for dataset={dataset}, role={role}")
        self.records: list[tuple[Path, int, str, str]] = []
        for row in records:
            subject = row["subject_id"]
            path = self._resolve_npz(row, subject)
            if not path.exists():
                continue
            with np.load(path, allow_pickle=False) as arrays:
                n_epochs = int(arrays["labels"].shape[0])
            recording_id = row.get("recording_id", subject)
            self.records.extend((path, index, subject, recording_id) for index in range(n_epochs))
        if not self.records:
            raise FileNotFoundError(f"no processed epoch files available for {dataset}/{role}")
        self._cache: dict[Path, dict[str, np.ndarray]] = {}
        self.normalization: dict[str, dict[str, float]] | None = None

    def set_normalization(self, normalization: dict[str, dict[str, float]]) -> None:
        self.normalization = normalization

    def _resolve_npz(self, row: dict[str, str], subject: str) -> Path:
        if row.get("output_path"):
            candidate = Path(row["output_path"])
            if candidate.exists():
                return candidate
            relative = self.root / Path(row["output_path"])
            if relative.exists():
                return relative
        prefix = "sleep_edf_sc" if self.dataset == "sleep_edf_sc" else "isruc_s1"
        expected = self.root / "data/processed/core_v1_1" / f"{prefix}__{subject}__core_v1.npz"
        if expected.exists():
            return expected
        matches = list((self.root / "data/processed/core_v1_1").glob(f"{prefix}__*{subject}*.npz"))
        return matches[0] if matches else expected

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, Any]:
        path, epoch_index, subject, recording_id = self.records[index]
        if path not in self._cache:
            with np.load(path, allow_pickle=False) as arrays:
                self._cache[path] = {
                    "eeg": arrays["eeg"],
                    "eog": arrays["eog"],
                    "labels": arrays["labels"],
                }
        arrays = self._cache[path]
        label = int(arrays["labels"][epoch_index])
        if label < 0 or label >= 5:
            raise ValueError(f"label outside frozen class range: {label}")
        eeg = np.asarray(arrays["eeg"][epoch_index], dtype=np.float32)
        eog = np.asarray(arrays["eog"][epoch_index], dtype=np.float32)
        if self.normalization is not None:
            eeg = apply_normalization(eeg, self.normalization["EEG"])
            eog = apply_normalization(eog, self.normalization["EOG"])
        return {
            "eeg": torch.from_numpy(eeg).unsqueeze(0),
            "eog": torch.from_numpy(eog).unsqueeze(0),
            "label": torch.tensor(label, dtype=torch.long),
            "dataset": self.dataset,
            "subject_id": subject,
            "recording_id": recording_id,
            "source_role": self.role,
        }


def build_source_dataset(experiment_id: str, role: str, purpose: str, *, root: str | Path = ".") -> ManifestEpochDataset:
    return ManifestEpochDataset(source_dataset_for_experiment(experiment_id), role, purpose, root=root)
