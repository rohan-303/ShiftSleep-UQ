"""Exact, provenance-preserving ISRUC source montage contract."""
from __future__ import annotations


_ALLOWED = {
    ("C3-A2", "LOC-A2"): ("ISRUC_A1A2",),
    ("C3-M2", "E1-M2"): ("ISRUC_M1M2",),
}


def resolve_isruc_montage(source_eeg_derivation: str, source_eog_derivation: str) -> dict[str, str]:
    """Return exact ISRUC family metadata; reject aliases and substitutions."""
    key = (source_eeg_derivation, source_eog_derivation)
    if key not in _ALLOWED:
        raise ValueError(f"UNSUPPORTED_ISRUC_MONTAGE:{source_eeg_derivation}+{source_eog_derivation}")
    variant = _ALLOWED[key][0]
    if variant == "ISRUC_A1A2":
        eeg_role, eog_role = "LEFT_CENTRAL_EEG", "LEFT_OCULAR_EOG"
    else:
        eeg_role, eog_role = "LEFT_CENTRAL_EEG", "LEFT_OCULAR_EOG"
    return {
        "source_eeg_derivation": source_eeg_derivation,
        "source_eog_derivation": source_eog_derivation,
        "eeg_anatomical_role": eeg_role,
        "eog_anatomical_role": eog_role,
        "montage_variant": variant,
    }
