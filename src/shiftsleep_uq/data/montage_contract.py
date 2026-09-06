"""Exact, provenance-preserving ISRUC source montage contract."""
from __future__ import annotations

_ALLOWED = {
    ("C3-A2", "LOC-A2"): "ISRUC_A1A2",
    ("C3-M2", "E1-M2"): "ISRUC_M1M2",
}


def supported_isruc_source_pairs() -> tuple[tuple[str, str], ...]:
    """Return the frozen exact source pairings in deterministic order."""
    return tuple(_ALLOWED)


def resolve_isruc_montage(source_eeg_derivation: str, source_eog_derivation: str) -> dict[str, str]:
    """Return exact ISRUC family metadata; reject aliases and substitutions."""
    key = (source_eeg_derivation, source_eog_derivation)
    if key not in _ALLOWED:
        raise ValueError(f"UNSUPPORTED_ISRUC_MONTAGE:{source_eeg_derivation}+{source_eog_derivation}")
    return {
        "source_eeg_derivation": source_eeg_derivation,
        "source_eog_derivation": source_eog_derivation,
        "eeg_anatomical_role": "LEFT_CENTRAL_EEG",
        "eog_anatomical_role": "LEFT_OCULAR_EOG",
        "montage_variant": _ALLOWED[key],
    }


def resolve_isruc_channels(labels: list[str] | tuple[str, ...]) -> dict[str, object]:
    """Resolve channel indices using only the authoritative exact pair contract."""
    labels = tuple(labels)
    for eeg, eog in supported_isruc_source_pairs():
        if eeg in labels and eog in labels:
            metadata = resolve_isruc_montage(eeg, eog)
            return {**metadata, "eeg_index": labels.index(eeg), "eog_index": labels.index(eog)}
    raise ValueError("UNSUPPORTED_ISRUC_CHANNEL_LAYOUT")
