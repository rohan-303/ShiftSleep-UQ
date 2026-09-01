import copy
from pathlib import Path
import pytest
from shiftsleep_uq.data.contracts import LABELS, load_contract, validate_contract


def test_contract_loads_and_validates():
    c = load_contract()
    assert c["contract_version"] == "1.0.0"


def test_mapping_and_exclusions_are_explicit():
    c = load_contract()
    assert set(c["canonical_labels"]) == LABELS
    assert "Sleep stage 4" in c["label_mappings"]["N3"]
    assert "unknown" in {x.lower() for x in c["excluded_annotations"]}


def test_unknown_cannot_silently_map_to_wake():
    c = copy.deepcopy(load_contract())
    c["label_mappings"]["Wake"].append("unknown")
    with pytest.raises(ValueError): validate_contract(c)


def test_primary_grouping_and_channels():
    c = load_contract()
    for d in c["datasets"]:
        if d["role"] in {"PRIMARY_DOMAIN_PROVISIONAL", "CONDITIONAL_PRIMARY_CANDIDATE"}:
            assert d["subject_key_rule"] and d["repeat_group_rule"]
    assert c["datasets"][0]["selected_channels"]["EEG"]["channel"]


def test_missingness_keeps_one_modality_and_target_free():
    c = load_contract()
    assert "no_EEG_EOG" in c["synthetic_missingness_conditions"]["forbidden"]
    assert c["target_free_rules"]["held_out_target_allowed_before_evaluation"] is False


def test_emg_and_structural_policy():
    c = load_contract()
    assert c["modalities"]["EMG"]["status"] == "SECONDARY_COMPATIBLE_SUBSET_ONLY"
    assert c["structural_mismatch_policy"]["separate_from_synthetic_masking"] is True
