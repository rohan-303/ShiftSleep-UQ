import copy
import pytest
from shiftsleep_uq.data.contracts import LABELS, load_contract, validate_contract


def test_contract_loads_and_core_gate_is_explicit():
    c = load_contract()
    assert c["contract_version"] == "1.2.0"
    assert c["status"] == "CORE_PREPROCESSING_FROZEN"
    assert c["final_benchmark_frozen"] is False


def test_isruc_primary_channels_and_scorer():
    c = load_contract()
    d = next(x for x in c["datasets"] if x["dataset_id"] == "isruc_s1")
    assert d["selected_channels"]["EEG"]["accepted_exact_derivations"] == ["C3-A2", "C3-M2"]
    assert d["selected_channels"]["EOG"]["accepted_exact_derivations"] == ["LOC-A2", "E1-M2"]
    assert d["scorer_policy"].startswith("scorer_1 primary")


def test_scorer_disagreement_is_not_primary_exclusion():
    c = load_contract()
    assert "scorer_disagreement" not in {x.lower() for x in c["excluded_annotations"]}
    bad = copy.deepcopy(c)
    bad["excluded_annotations"].append("scorer_disagreement")
    with pytest.raises(ValueError): validate_contract(bad)


def test_labels_and_unknown_mapping():
    c = load_contract()
    assert set(c["canonical_labels"]) == LABELS
    assert "Sleep stage 4" in c["label_mappings"]["N3"]
    bad = copy.deepcopy(c)
    bad["label_mappings"]["Wake"].append("unknown")
    with pytest.raises(ValueError): validate_contract(bad)


def test_core_subject_grouping_and_exact_channels():
    c = load_contract()
    core = [d for d in c["datasets"] if d["role"] == "PRIMARY_ACCESSIBLE_CORE"]
    assert {d["dataset_id"] for d in core} == {"sleep_edf_sc", "isruc_s1"}
    for d in core:
        assert d["subject_key_rule"] and d["repeat_group_rule"]
        assert d["selected_channels"]["EEG"] and d["selected_channels"]["EOG"]


def test_sampling_missingness_structural_and_target_free_rules():
    c = load_contract()
    assert c["resampling_policy"]["target_rates"] == {"EEG": 100, "EOG": 50}
    assert "no_EEG_EOG" in c["synthetic_missingness_conditions"]["forbidden"]
    assert c["structural_mismatch_policy"]["separate_from_synthetic_masking"] is True
    assert c["target_free_rules"]["held_out_target_allowed_before_evaluation"] is False
    assert set(c["shift_taxonomy"]) >= {"C0", "C1", "C2", "C3", "C4", "C5"}


def test_shhs_pending_cannot_masquerade_as_acquired():
    c = load_contract()
    d = next(x for x in c["datasets"] if x["dataset_id"] == "shhs1")
    assert d["role"] == "PLANNED_PRIMARY_DOMAIN_PENDING_RAW_ACCESS"
    assert d["access_state"] == "RAW_ACCESS_PENDING"
    bad = copy.deepcopy(c)
    bad["datasets"][-2]["access_state"] = "RAW_ACCESS_APPROVED"
    with pytest.raises(ValueError): validate_contract(bad)


def test_primary_freeze_levels_are_distinct():
    c = load_contract()
    assert "CORE_PREPROCESSING_FROZEN" in c["freeze_levels"]
    assert "FINAL_BENCHMARK_FROZEN" in c["freeze_levels"]
    assert c["final_benchmark_frozen"] is False
