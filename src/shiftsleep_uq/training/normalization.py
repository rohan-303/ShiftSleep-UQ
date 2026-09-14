"""Source-only streaming normalization for future Step 10 execution."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class NormalizationRoleError(ValueError):
    pass


@dataclass
class StreamingMoments:
    count: int = 0
    mean_value: float = 0.0
    m2: float = 0.0

    def update(self, values: np.ndarray) -> None:
        array = np.asarray(values, dtype=np.float64)
        if not np.isfinite(array).all():
            raise ValueError("normalization input contains non-finite values")
        flat = array.reshape(-1)
        for value in flat:
            self.count += 1
            delta = float(value) - self.mean_value
            self.mean_value += delta / self.count
            delta2 = float(value) - self.mean_value
            self.m2 += delta * delta2

    def finalize(self, *, std_epsilon: float = 1e-8) -> tuple[float, float]:
        if self.count == 0:
            raise ValueError("cannot finalize empty normalization moments")
        variance = max(self.m2 / self.count, 0.0)
        return self.mean_value, max(float(np.sqrt(variance)), std_epsilon)


def fit_source_train_normalization(
    modality_batches: dict[str, list[np.ndarray]], *, role: str, std_epsilon: float = 1e-8
) -> dict[str, dict[str, float]]:
    if role != "TRAIN":
        raise NormalizationRoleError("normalization fitting requires SOURCE TRAIN role")
    result: dict[str, dict[str, float]] = {}
    for modality, batches in modality_batches.items():
        moments = StreamingMoments()
        for batch in batches:
            moments.update(batch)
        mean, std = moments.finalize(std_epsilon=std_epsilon)
        result[modality] = {"mean": mean, "std": std, "std_epsilon": std_epsilon}
    return result


def fit_source_train_dataset(dataset: object, *, role: str, std_epsilon: float = 1e-8) -> dict[str, dict[str, float]]:
    if role != "TRAIN":
        raise NormalizationRoleError("normalization fitting requires SOURCE TRAIN role")
    moments = {"EEG": StreamingMoments(), "EOG": StreamingMoments()}
    for index in range(len(dataset)):  # type: ignore[arg-type]
        sample = dataset[index]  # type: ignore[index]
        moments["EEG"].update(np.asarray(sample["eeg"]))
        moments["EOG"].update(np.asarray(sample["eog"]))
    return {
        modality: {
            "mean": moments[modality].finalize(std_epsilon=std_epsilon)[0],
            "std": moments[modality].finalize(std_epsilon=std_epsilon)[1],
            "std_epsilon": std_epsilon,
        }
        for modality in moments
    }


def apply_normalization(values: np.ndarray, parameters: dict[str, float]) -> np.ndarray:
    array = np.asarray(values, dtype=np.float32)
    if not np.isfinite(array).all():
        raise ValueError("normalization input contains non-finite values")
    return (array - np.float32(parameters["mean"])) / np.float32(parameters["std"])
