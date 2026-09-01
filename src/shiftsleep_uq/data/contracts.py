"""Validation for the Step 5 data contract; no signal processing."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

LABELS = {"Wake", "N1", "N2", "N3", "REM"}
ROLES = {"PRIMARY_DOMAIN_PROVISIONAL", "SECONDARY_STRESS_DOMAIN", "DEFERRED_PRIMARY_CANDIDATE", "CONDITIONAL_PRIMARY_CANDIDATE", "EXTERNAL_STRESS_DOMAIN"}
STATUSES = {"PRIMARY", "SECONDARY_COMPATIBLE_SUBSET_ONLY"}


def load_contract(path: str | Path = "configs/data_contract_v1.yaml") -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    validate_contract(data)
    return data


def validate_contract(data: dict[str, Any]) -> None:
    if not isinstance(data, dict) or data.get("contract_version") != "1.0.0":
        raise ValueError("invalid contract version")
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
    primary = [d for d in data["datasets"] if d["role"] in {"PRIMARY_DOMAIN_PROVISIONAL", "CONDITIONAL_PRIMARY_CANDIDATE"}]
    for d in primary:
        for key in ("subject_key_rule", "repeat_group_rule", "annotation_source"):
            if not d.get(key): raise ValueError(f"{d['dataset_id']} lacks {key}")
        if d["dataset_id"] == "sleep_edf_sc" and not d["selected_channels"].get("EEG"): raise ValueError("SC EEG channel missing")
    for name, spec in data["modalities"].items():
        if spec.get("status") not in STATUSES: raise ValueError(f"invalid modality status: {name}")
    if "no_EEG_EOG" in data["synthetic_missingness_conditions"]["forbidden"]: pass
    else: raise ValueError("all-primary-modality removal must be forbidden")
    rules = data["target_free_rules"]
    if rules["held_out_target_allowed_before_evaluation"] is not False: raise ValueError("target leakage rule invalid")
    if not data["structural_mismatch_policy"]["separate_from_synthetic_masking"]: raise ValueError("structural mismatch must be separate")
    if not data["schema_acceptance_rules"]["raw_immutable"]: raise ValueError("raw immutability required")
