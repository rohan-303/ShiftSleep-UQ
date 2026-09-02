"""Pure, deterministic preprocessing primitives for the frozen PSG core."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import numpy as np
from scipy.signal import resample_poly

LABELS = ("Wake", "N1", "N2", "N3", "REM")
LABEL_TO_INT = {x: i for i, x in enumerate(LABELS)}
# Exclusions are exact strings after whitespace normalization.  They are not
# case-folded or fuzzily inferred; dataset schemas restrict which source form
# may appear in a real adapter stream.
EXCLUSION_REASONS = {
    "Movement time": "movement", "Sleep stage ?": "unknown", "Sleep stage U": "unscored",
    "?": "unknown", "unknown": "unknown", "unscored": "unscored",
    "artifact": "artifact", "corrupt_annotation": "artifact",
}

# The shared mapper recognizes only exact source spellings. Dataset allowlists are
# applied before canonicalization so a valid label from one source cannot silently
# be accepted in another source's annotation stream.
DATASET_ALLOWED_SOURCE_LABELS = {
    "sleep_edf_sc": frozenset({
        "Sleep stage W", "Sleep stage 1", "Sleep stage 2", "Sleep stage 3",
        "Sleep stage 4", "Sleep stage R", "Sleep stage ?", "Movement time",
    }),
    "isruc_s1": frozenset({
        "Sleep stage W", "Sleep stage N1", "Sleep stage N2", "Sleep stage N3",
        "Sleep stage R", "Sleep stage U",
    }),
}

class PreprocessingError(ValueError): pass

@dataclass(frozen=True)
class EpochLabel:
    onset: float
    duration: float
    original: str
    canonical: str | None
    source_index: int
    exclusion: str | None = None

def canonicalize_label(value: str, *, dataset: str | None = None) -> str:
    s = " ".join(str(value).strip().split())
    if dataset is not None:
        allowed = DATASET_ALLOWED_SOURCE_LABELS.get(dataset)
        if allowed is None:
            raise PreprocessingError(f"UNKNOWN_DATASET_LABEL_SCHEMA:{dataset}")
        if s not in allowed:
            raise PreprocessingError(f"ANNOTATION_SOURCE_LABEL_NOT_ALLOWED:{dataset}:{s}")
    if s in EXCLUSION_REASONS:
        raise PreprocessingError(f"ANNOTATION_EXCLUDED_LABEL:{EXCLUSION_REASONS[s]}")
    mapping = {
        "Sleep stage W":"Wake", "W":"Wake", "Wake":"Wake",
        # Sleep-EDF SC uses numbered stage labels; NEMAR ISRUC uses the
        # explicit AASM/R&K strings below. Keep source spellings exact.
        "Sleep stage 1":"N1", "Sleep stage N1":"N1", "Stage 1":"N1", "N1":"N1",
        "Sleep stage 2":"N2", "Sleep stage N2":"N2", "Stage 2":"N2", "N2":"N2",
        "Sleep stage 3":"N3", "Sleep stage 4":"N3", "Sleep stage N3":"N3", "Stage 3":"N3", "Stage 4":"N3", "N3":"N3",
        "Sleep stage R":"REM", "Stage R":"REM", "REM":"REM",
    }
    if s not in mapping:
        raise PreprocessingError(f"ANNOTATION_UNKNOWN_LABEL:{s}")
    return mapping[s]

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

def expand_annotations(events: Iterable[tuple[float,float,str]], tolerance: float = .001, *, dataset: str | None = None) -> list[EpochLabel]:
    out=[]
    for i,(onset,duration,label) in enumerate(events):
        onset=float(onset); duration=float(duration)
        # Zero-duration events are BIDS impulse/non-stage events, not sleep
        # epochs. They remain visible in the raw event audit but do not enter
        # the source-stage accounting denominator.
        if duration <= 0:
            continue
        if abs(duration/30-round(duration/30)) > tolerance/30:
            out.append(EpochLabel(onset,duration,str(label),None,i,"alignment_error")); continue
        try: canon=canonicalize_label(label, dataset=dataset); exc=None
        except PreprocessingError as e:
            canon=None
            if "ANNOTATION_EXCLUDED_LABEL:" in str(e):
                exc=str(e).rsplit(":", 1)[1]
            elif "ANNOTATION_SOURCE_LABEL_NOT_ALLOWED" in str(e):
                exc="unknown"
            else:
                exc="unknown" if "UNKNOWN_LABEL" in str(e) else "other"
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
