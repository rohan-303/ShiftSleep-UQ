import csv
import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]


def _rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_step08_source_partition_manifest_is_complete_and_disjoint():
    rows = _rows("reports/subject_partitions_v1.csv")
    assert len(rows) == 177
    assert len({(r["dataset"], r["subject_id"]) for r in rows}) == 177
    assert set(r["source_role"] for r in rows) == {"TRAIN", "DEV", "CALIBRATION"}
    for dataset in {r["dataset"] for r in rows}:
        subset = [r for r in rows if r["dataset"] == dataset]
        assert {r["subject_id"] for r in subset if r["source_role"] == "TRAIN"}.isdisjoint(
            {r["subject_id"] for r in subset if r["source_role"] == "DEV"}
        )
        assert {r["subject_id"] for r in subset if r["source_role"] == "TRAIN"}.isdisjoint(
            {r["subject_id"] for r in subset if r["source_role"] == "CALIBRATION"}
        )
        assert {r["subject_id"] for r in subset if r["source_role"] == "DEV"}.isdisjoint(
            {r["subject_id"] for r in subset if r["source_role"] == "CALIBRATION"}
        )


def test_step08_oracle_is_separate_and_disjoint_from_primary_roles():
    primary = {(r["dataset"], r["subject_id"]) for r in _rows("reports/subject_partitions_v1.csv")}
    oracle = _rows("reports/oracle_target_partitions_v1.csv")
    assert len(oracle) == 177
    assert {(r["dataset"], r["subject_id"]) for r in oracle} == primary
    assert set(r["oracle_role"] for r in oracle) == {"ORACLE_CALIBRATION", "ORACLE_EVALUATION"}
    assert not {r["subject_id"] for r in oracle if r["oracle_role"] == "ORACLE_CALIBRATION"}.intersection(
        {r["subject_id"] for r in oracle if r["oracle_role"] == "ORACLE_EVALUATION"}
    )


def test_step08_protocol_freezes_c0_c5_and_target_free_rules():
    protocol = yaml.safe_load((ROOT / "configs/evaluation_protocol_v1.yaml").read_text(encoding="utf-8"))
    assert protocol["protocol_gate"] == "EXPERIMENT_PROTOCOL_FROZEN"
    assert protocol["split"]["seed"] == 2026
    assert protocol["model_seeds"] == [17, 42, 2026]
    assert protocol["oracle"]["split_seed"] == 2027
    assert protocol["c0_c5"] == {
        "C0": "known_domain_EEG_EOG",
        "C1": "known_domain_EEG_only_synthetic_no_EOG",
        "C2": "known_domain_EOG_only_synthetic_no_EEG",
        "C3": "unseen_domain_EEG_EOG",
        "C4": "unseen_domain_EEG_only_synthetic_no_EOG",
        "C5": "unseen_domain_EOG_only_synthetic_no_EEG",
    }
    assert protocol["target_free_firewall"]["target_labels_before_primary_evaluation"] is False
    assert protocol["normalization"]["fit_scope"] == "SOURCE_TRAIN_ONLY"
    assert protocol["conformal"]["primary_method"] == "APS"


def test_step08_reciprocal_directions_keep_targets_out_of_source_roles():
    protocol = yaml.safe_load((ROOT / "configs/evaluation_protocol_v1.yaml").read_text(encoding="utf-8"))
    rows = _rows("reports/subject_partitions_v1.csv")
    source_datasets = {r["dataset"] for r in rows}
    for direction in protocol["experiment_matrix"].values():
        assert direction["target_dataset"] in source_datasets
        assert direction["target_dataset"] not in direction["source_datasets"]
        assert direction["target_adaptation"] == "forbidden"


def test_step08_sleep_edf_subject_grouping_and_montage_inclusion_are_invariant():
    rows = _rows("reports/subject_partitions_v1.csv")
    role_by_subject = {(r["dataset"], r["subject_id"]): r["source_role"] for r in rows}
    recordings = _rows("reports/core_recording_manifest_v1_1.csv")
    for row in recordings:
        if row["dataset"] == "sleep_edf_sc" and row["terminal_status"] == "INCLUDED":
            assert (row["dataset"], row["subject_id"]) in role_by_subject
    isruc = [r for r in rows if r["dataset"] == "isruc_s1"]
    assert {r["montage_variant"] for r in isruc} == {"ISRUC_A1A2", "ISRUC_M1M2"}
    assert len(isruc) == 99
    assert "I040" not in {r["subject_id"] for r in isruc}


def test_step08_firewall_blocks_target_fitting_and_oracle_contamination():
    protocol = yaml.safe_load((ROOT / "configs/evaluation_protocol_v1.yaml").read_text(encoding="utf-8"))
    firewall = protocol["target_free_firewall"]
    assert all(value is False for key, value in firewall.items() if key != "intrinsic_montage_metadata_for_analysis_only")
    assert protocol["normalization"]["fit_scope"] == "SOURCE_TRAIN_ONLY"
    assert protocol["calibration"]["source_only"]["fit_labels"] == "SOURCE_CALIBRATION_ONLY"
    assert protocol["oracle"]["primary_results_use_oracle"] is False
    assert protocol["montage_sensitivity"]["no_target_rebalancing"] is True


def test_step08_hash_manifest_reproduces():
    hashes = {}
    for line in (ROOT / "reports/step08_protocol_hashes.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            path, digest = line.split(",", 1)
            hashes[path] = digest
    for path, digest in hashes.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
