from pathlib import Path

import pytest
import yaml

from shiftsleep_uq.data.montage_contract import resolve_isruc_montage


CONTRACT = yaml.safe_load(
    (Path(__file__).parents[1] / "configs" / "data_contract_v1.yaml").read_text(encoding="utf-8")
)


def test_accepts_exact_a1a2_family():
    result = resolve_isruc_montage("C3-A2", "LOC-A2")
    assert result == {
        "source_eeg_derivation": "C3-A2",
        "source_eog_derivation": "LOC-A2",
        "eeg_anatomical_role": "LEFT_CENTRAL_EEG",
        "eog_anatomical_role": "LEFT_OCULAR_EOG",
        "montage_variant": "ISRUC_A1A2",
    }


def test_accepts_exact_m1m2_family():
    result = resolve_isruc_montage("C3-M2", "E1-M2")
    assert result["source_eeg_derivation"] == "C3-M2"
    assert result["source_eog_derivation"] == "E1-M2"
    assert result["montage_variant"] == "ISRUC_M1M2"


@pytest.mark.parametrize("eeg,eog", [
    ("c3-a2", "LOC-A2"),
    ("C3-M2", "E1-M1"),
    ("C4-M1", "E1-M2"),
    ("C3-M2", "ROC-A1"),
    ("C3-A1", "LOC-A2"),
])
def test_rejects_fuzzy_substitution_or_unknown_combination(eeg, eog):
    with pytest.raises(ValueError):
        resolve_isruc_montage(eeg, eog)


def test_contract_version_and_frozen_semantics():
    assert CONTRACT["contract_version"] == "1.2.0"
    assert set(CONTRACT["shift_taxonomy"]) >= {"C0", "C1", "C2", "C3", "C4", "C5"}
    assert CONTRACT["target_free_rules"]["held_out_target_allowed_before_evaluation"] is False
    isruc = next(d for d in CONTRACT["datasets"] if d["dataset_id"] == "isruc_s1")
    assert isruc["selected_channels"]["EEG"]["accepted_exact_derivations"] == ["C3-A2", "C3-M2"]
    assert isruc["selected_channels"]["EOG"]["accepted_exact_derivations"] == ["LOC-A2", "E1-M2"]
    assert isruc["channel_fallbacks"] == "none"
    assert CONTRACT["resampling_policy"]["target_rates"] == {"EEG": 100, "EOG": 50}
