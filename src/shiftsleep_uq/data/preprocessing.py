"""Pure, deterministic preprocessing primitives for the frozen PSG core."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import numpy as np
from scipy.signal import resample_poly

LABELS = ("Wake", "N1", "N2", "N3", "REM")
LABEL_TO_INT = {x: i for i, x in enumerate(LABELS)}
EXCLUSIONS = {"movement", "movement time", "sleep stage ?", "?", "unknown", "unscored", "artifact", "corrupt_annotation"}

class PreprocessingError(ValueError): pass

@dataclass(frozen=True)
class EpochLabel:
    onset: float
    duration: float
    original: str
    canonical: str | None
    source_index: int
    exclusion: str | None = None

def canonicalize_label(value: str) -> str:
    s = " ".join(str(value).strip().split())
    low = s.lower()
    if low in EXCLUSIONS or "movement" in low:
        raise PreprocessingError(f"ANNOTATION_UNKNOWN_LABEL:{s}")
    mapping = {
        "sleep stage w":"Wake", "w":"Wake", "wake":"Wake",
        "sleep stage 1":"N1", "stage 1":"N1", "n1":"N1",
        "sleep stage 2":"N2", "stage 2":"N2", "n2":"N2",
        "sleep stage 3":"N3", "sleep stage 4":"N3", "stage 3":"N3", "stage 4":"N3", "n3":"N3",
        "sleep stage r":"REM", "stage r":"REM", "rem":"REM",
    }
    if low not in mapping:
        raise PreprocessingError(f"ANNOTATION_UNKNOWN_LABEL:{s}")
    return mapping[low]

def unit_to_uv(values: np.ndarray, unit: str) -> np.ndarray:
    u = "".join(str(unit).strip().lower().replace("µ", "u").split())
    factor = {"v": 1e6, "volt": 1e6, "volts": 1e6, "mv": 1e3, "millivolt": 1e3, "millivolts": 1e3, "uv": 1.0, "microvolt": 1.0, "microvolts": 1.0}.get(u)
    if factor is None: raise PreprocessingError(f"STRUCTURAL_UNIT_MISMATCH:{unit!r}")
    return np.asarray(values, dtype=np.float64) * factor

def resample_continuous(values: np.ndarray, source_rate: float, target_rate: float) -> np.ndarray:
    if source_rate == target_rate: return np.asarray(values, dtype=np.float64).copy()
    if source_rate < target_rate: raise PreprocessingError("UPSAMPLING_FORBIDDEN")
    ratio = source_rate / target_rate
    if abs(ratio - round(ratio)) > 1e-12: raise PreprocessingError("NON_INTEGER_DOWNsample_UNSUPPORTED")
    return resample_poly(np.asarray(values, dtype=np.float64), 1, int(round(ratio)), window=("kaiser", 5.0), padtype="constant")

def expand_annotations(events: Iterable[tuple[float,float,str]], tolerance: float = .001) -> list[EpochLabel]:
    out=[]
    for i,(onset,duration,label) in enumerate(events):
        onset=float(onset); duration=float(duration)
        if duration <= 0 or abs(duration/30-round(duration/30)) > tolerance/30:
            out.append(EpochLabel(onset,duration,str(label),None,i,"alignment_error")); continue
        try: canon=canonicalize_label(label); exc=None
        except PreprocessingError as e:
            canon=None; exc="movement" if "movement" in str(label).lower() else ("unknown" if "UNKNOWN_LABEL" in str(e) else "other")
        for k in range(int(round(duration/30))):
            out.append(EpochLabel(onset+30*k,30,str(label),canon,i,exc))
    return out

def slice_epochs(signal: np.ndarray, onsets: Iterable[float], rate: int, expected: int) -> tuple[list[np.ndarray], list[str]]:
    result=[]; errors=[]
    for onset in onsets:
        start=int(round(float(onset)*rate)); stop=start+expected
        if abs(float(onset)*rate-start)>1e-6 or start<0 or stop>len(signal): errors.append("alignment_error"); continue
        x=np.asarray(signal[start:stop])
        if len(x)!=expected: errors.append("missing_signal_samples"); continue
        result.append(x); errors.append("")
    return result, errors

def validate_output(eeg: np.ndarray, eog: np.ndarray, labels: np.ndarray) -> None:
    if eeg.ndim != 2 or eeg.shape[1] != 3000 or eog.ndim != 2 or eog.shape[1] != 1500: raise PreprocessingError("OUTPUT_SHAPE_ERROR")
    if eeg.shape[0] != eog.shape[0] or eeg.shape[0] != len(labels): raise PreprocessingError("OUTPUT_LENGTH_ERROR")
    if not set(np.asarray(labels).tolist()).issubset(set(range(5))): raise PreprocessingError("OUTPUT_LABEL_ERROR")
    if not np.isfinite(eeg).all() or not np.isfinite(eog).all(): raise PreprocessingError("OUTPUT_NONFINITE")
