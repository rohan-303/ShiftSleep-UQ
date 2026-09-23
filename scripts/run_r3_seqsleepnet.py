"""Step 20.2.3 R3 SeqSleepNet executor.

The default command is a non-scientific preflight.  Scientific execution is
explicitly opt-in via ``--execute`` and writes only ``artifacts/remediation/r3``.
Historical data and result namespaces are never modified.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from scipy.signal import stft
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PROTOCOL = ROOT / "configs/postreview_remediation_protocol_v2.yaml"
PROTOCOL_SHA256 = "c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b"
R3_ROOT = ROOT / "artifacts/remediation/r3"
SEEDS = (17, 42, 2026)
DIRECTIONS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
VARIANTS = ("S0", "S1")
EXPOSURE_SEED = 2029


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protocol_gate(path: Path = PROTOCOL) -> str:
    """Require the exact frozen v2 protocol before any data or model access."""
    actual = sha256(path)
    if actual != PROTOCOL_SHA256:
        raise RuntimeError(f"R3_PROTOCOL_HASH_FAILURE: expected {PROTOCOL_SHA256}, got {actual}")
    return actual


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False


def state_hash(model: nn.Module) -> str:
    digest = hashlib.sha256()
    for name, value in model.state_dict().items():
        digest.update(name.encode("utf-8"))
        digest.update(value.detach().cpu().numpy().tobytes())
    return digest.hexdigest()


def matched_initialization(seed: int) -> tuple[nn.Module, nn.Module, str]:
    """Return independently named S0/S1 models with byte-identical initialization."""
    from shiftsleep_uq.models.seqsleepnet_class import SeqSleepNetClass

    seed_everything(seed)
    base = SeqSleepNetClass()
    initial = copy.deepcopy(base.state_dict())
    s0 = SeqSleepNetClass(); s1 = SeqSleepNetClass()
    s0.load_state_dict(initial); s1.load_state_dict(initial)
    h0, h1 = state_hash(s0), state_hash(s1)
    if h0 != h1:
        raise RuntimeError("R3 matched initialization invariant failed")
    return s0, s1, h0


def stft_log_power(signal: np.ndarray, *, sample_rate: int) -> np.ndarray:
    """Apply the frozen 200/100/256 Hamming STFT and ln(power + 1e-8)."""
    values = np.asarray(signal, dtype=np.float32)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("STFT input must be a finite one-dimensional signal")
    _, _, transformed = stft(
        values, fs=sample_rate, window="hamming", nperseg=200, noverlap=100,
        nfft=256, boundary=None, padded=False, return_onesided=True,
    )
    result = np.log(np.abs(transformed).astype(np.float64) ** 2 + 1e-8).astype(np.float32)
    if result.shape != (129, 29):
        raise ValueError(f"R3 STFT contract violation: got {result.shape}, expected (129, 29)")
    return result


def epoch_spectrogram(eeg: np.ndarray, eog: np.ndarray) -> np.ndarray:
    """Return one epoch as [2, 129, 29], with EOG resampled 50 Hz -> 100 Hz."""
    from scipy.signal import resample_poly

    eeg = np.asarray(eeg); eog = np.asarray(eog)
    if eeg.size != 3000 or eog.size != 1500:
        raise ValueError(f"R3 epoch contract requires EEG=3000/EOG=1500 samples, got {eeg.size}/{eog.size}")
    eog_100 = resample_poly(eog.astype(np.float32), 2, 1)
    return np.stack((stft_log_power(eeg, sample_rate=100), stft_log_power(eog_100, sample_rate=100)))


def fit_source_normalization(epochs: Iterable[np.ndarray]) -> dict[str, Any]:
    """Fit per-modality/frequency-bin moments on SOURCE TRAIN epochs only."""
    total = np.zeros((2, 129), dtype=np.float64); square = np.zeros_like(total); count = 0
    for epoch in epochs:
        value = np.asarray(epoch, dtype=np.float64)
        if value.shape != (2, 129, 29) or not np.isfinite(value).all():
            raise ValueError("normalization received a non-finite or malformed STFT epoch")
        total += value.sum(axis=2); square += np.square(value).sum(axis=2); count += value.shape[2]
    if count == 0:
        raise ValueError("source-only normalization cannot fit an empty epoch set")
    mean = total / count
    std = np.maximum(np.sqrt(np.maximum(square / count - mean * mean, 0.0)), 1e-6)
    return {"scope": "SOURCE_TRAIN_ONLY", "count": count, "mean": mean.tolist(), "std": std.tolist(), "epsilon": 1e-6}


def apply_source_normalization(value: np.ndarray, normalization: dict[str, Any]) -> np.ndarray:
    if normalization.get("scope") != "SOURCE_TRAIN_ONLY":
        raise ValueError("R3 normalization scope is not source-only")
    mean = np.asarray(normalization["mean"], dtype=np.float32)[:, :, None]
    std = np.asarray(normalization["std"], dtype=np.float32)[:, :, None]
    value = np.asarray(value, dtype=np.float32)
    if value.shape != (2, 129, 29): raise ValueError("malformed spectrogram")
    return (value - mean) / std


@dataclass(frozen=True)
class SequenceRef:
    path: Path
    indices: tuple[int, ...]
    subject_id: str
    recording_id: str
    start_index: int


def physical_contiguous_sequences(records: Iterable[tuple[Path, int, str, str, str]], *, length: int = 20, stride: int = 10) -> list[SequenceRef]:
    """Build complete sequences only within recording/subject contiguous segments."""
    grouped: dict[tuple[Path, str, str], list[int]] = {}
    for path, row_index, subject, recording, _ in records:
        grouped.setdefault((path, subject, recording), []).append(int(row_index))
    output: list[SequenceRef] = []
    for (path, subject, recording), row_indices in grouped.items():
        row_indices = sorted(row_indices)
        segment: list[int] = []
        segments: list[list[int]] = []
        for index in row_indices:
            if segment and index != segment[-1] + 1:
                segments.append(segment); segment = []
            segment.append(index)
        if segment: segments.append(segment)
        for contiguous in segments:
            for offset in range(0, len(contiguous) - length + 1, stride):
                indices = tuple(contiguous[offset:offset + length])
                output.append(SequenceRef(path, indices, subject, recording, indices[0]))
    return output


def sequence_key(direction: str, model_seed: int, training_epoch: int, ref: SequenceRef) -> str:
    return "|".join((direction, str(model_seed), str(training_epoch), ref.subject_id, ref.recording_id, str(ref.start_index)))


def sequence_mask(variant: str, direction: str, model_seed: int, training_epoch: int, ref: SequenceRef) -> tuple[int, int]:
    if variant == "S0": return (1, 1)
    if variant != "S1": raise ValueError(f"unknown R3 variant: {variant}")
    digest = hashlib.sha256(f"{EXPOSURE_SEED}\x1f{sequence_key(direction, model_seed, training_epoch, ref)}".encode()).digest()
    value = int.from_bytes(digest[:8], "big") / float(1 << 64)
    return (1, 1) if value < .50 else ((1, 0) if value < .75 else (0, 1))


def allocate_attempt(direction: str, variant: str, seed: int, *, root: Path = R3_ROOT) -> Path:
    """Create a collision-failing attempt with the complete required layout."""
    base = root / f"R3_{direction}_{variant}_SEED_{seed}"
    base.mkdir(parents=True, exist_ok=True)
    for number in range(1, 10000):
        attempt = base / f"ATTEMPT_{number:03d}"
        try:
            attempt.mkdir()
        except FileExistsError:
            continue
        for name in ("checkpoints", "predictions", "logs", "diagnostics", "manifests", "tmp"):
            (attempt / name).mkdir()
        return attempt
    raise RuntimeError(f"R3 attempt namespace exhausted: {base}")


def required_metadata(*, protocol_hash: str, direction: str, variant: str, seed: int, attempt: Path, status: str) -> dict[str, Any]:
    if status not in {"RUNNING", "COMPLETE", "FAILED"}: raise ValueError("invalid run status")
    return {"status": status, "protocol_sha256": protocol_hash, "direction": direction,
            "variant": variant, "seed": seed, "attempt_root": str(attempt),
            "model_id": "SEQSLEEPNET_CLASS_L20_V1", "source_roles": ["SOURCE_TRAIN", "SOURCE_DEV"],
            "target_access": "FORBIDDEN", "normalization_scope": "SOURCE_TRAIN_ONLY",
            "stft_contract": {"window_samples": 200, "hop_samples": 100, "nfft": 256, "bins": 129, "frames": 29},
            "physical_contiguous_sequences": True, "matched_initialization": True}


def preflight() -> dict[str, Any]:
    protocol_hash = protocol_gate()
    return {"status": "PREFLIGHT_ONLY", "protocol_sha256": protocol_hash, "jobs": len(DIRECTIONS) * len(VARIANTS) * len(SEEDS),
            "scientific_training": "NOT_EXECUTED", "target_access": "FORBIDDEN"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="run authorized R3 training; omitted by default")
    args = parser.parse_args()
    result = preflight()
    if not args.execute:
        print(json.dumps(result, sort_keys=True)); return
    raise RuntimeError("R3 training loop is intentionally gated; wire only after the bounded executor review")


if __name__ == "__main__":
    main()
