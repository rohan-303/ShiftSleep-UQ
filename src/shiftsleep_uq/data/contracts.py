"""Validation for the Step 5.1 data contract; no signal processing."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

LABELS = {"Wake", "N1", "N2", "N3", "REM"}
CORE = {"PRIMARY_ACCESSIBLE_CORE"}


def load_contract(path: str | Path = "configs/data_contract_v1.yaml") -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    validate_contract(data)
    return data


def validate_contract(data: dict[str, Any]) -> None:
    if not isinstance(data, dict) or data.get("contract_version") != "1.2.0":
        raise ValueError("invalid contract version")
    if data.get("status") != "CORE_PREPROCESSING_FROZEN" or data.get("final_benchmark_frozen") is not False:
        raise ValueError("freeze gates invalid")
    if set(data["canonical_labels"]) != LABELS:
        raise ValueError("canonical labels must be exactly Wake/N1/N2/N3/REM")
    mappings = data["label_mappings"]
    if set(mappings) != LABELS or any(not isinstance(v, list) or not v for v in mappings.values()):
        raise ValueError("every canonical label needs a nonempty mapping list")
    if any("unknown" in str(v).lower() and "Wake" in k for k, v in mappings.items()):
        raise ValueError("unknown cannot map to Wake")
    excluded = {str(x).lower() for x in data["excluded_annotations"]}
    for required in ("movement time", "unknown", "unscored", "artifact", "incomplete_epoch"):
        if required not in excluded:
            raise ValueError(f"missing explicit exclusion: {required}")
    if "scorer_disagreement" in excluded:
        raise ValueError("scorer disagreement must not be a primary exclusion")
    datasets = data["datasets"]
    core = [d for d in datasets if d["role"] in CORE]
    if {d["dataset_id"] for d in core} != {"sleep_edf_sc", "isruc_s1"}:
        raise ValueError("accessible core must be Sleep-EDF SC and ISRUC-S1")
    for d in core:
        for key in ("subject_key_rule", "repeat_group_rule", "annotation_source"):
            if not d.get(key): raise ValueError(f"{d['dataset_id']} lacks {key}")
        channels = d.get("selected_channels", {})
        if not channels.get("EEG") or not channels.get("EOG"):
            raise ValueError(f"{d['dataset_id']} lacks exact EEG/EOG channels")
        if d["dataset_id"] == "isruc_s1":
            if channels["EEG"].get("accepted_exact_derivations") != ["C3-A2", "C3-M2"]:
                raise ValueError("ISRUC EEG allowlist invalid")
            if channels["EOG"].get("accepted_exact_derivations") != ["LOC-A2", "E1-M2"]:
                raise ValueError("ISRUC EOG allowlist invalid")
            if d.get("exact_derivation_allowlist") != [
                {"eeg": "C3-A2", "eog": "LOC-A2", "montage_variant": "ISRUC_A1A2"},
                {"eeg": "C3-M2", "eog": "E1-M2", "montage_variant": "ISRUC_M1M2"},
            ]:
                raise ValueError("ISRUC exact derivation pair allowlist invalid")
            if d.get("channel_fallbacks") != "none":
                raise ValueError("ISRUC fallback policy invalid")
        if d["dataset_id"] == "isruc_s1" and d.get("scorer_policy") != "scorer_1 primary; scorer_2 secondary diagnostic":
            raise ValueError("ISRUC primary scorer must be explicit")
    shhs = next(d for d in datasets if d["dataset_id"] == "shhs1")
    if shhs["role"] != "PLANNED_PRIMARY_DOMAIN_PENDING_RAW_ACCESS" or shhs["access_state"] != "RAW_ACCESS_PENDING":
        raise ValueError("SHHS must remain explicitly pending")
    if shhs["selected_channels"]["EEG"]["channel"] != "C3-A2" or shhs["selected_channels"]["EOG"]["channel"] != "EOG(L)-PG1":
        raise ValueError("SHHS intended channels not frozen")
    for name, spec in data["modalities"].items():
        if name in {"EEG", "EOG"} and spec.get("status") != "PRIMARY":
            raise ValueError(f"invalid primary modality status: {name}")
    if "no_EEG_EOG" not in data["synthetic_missingness_conditions"]["forbidden"]:
        raise ValueError("all-primary-modality removal must be forbidden")
    if not data["structural_mismatch_policy"]["separate_from_synthetic_masking"]:
        raise ValueError("structural mismatch must be separate")
    if data["resampling_policy"]["target_rates"] != {"EEG": 100, "EOG": 50}:
        raise ValueError("sampling targets invalid")
    rules = data["target_free_rules"]
    if rules["held_out_target_allowed_before_evaluation"] is not False:
        raise ValueError("target leakage rule invalid")
    if not data["schema_acceptance_rules"]["raw_immutable"]:
        raise ValueError("raw immutability required")
