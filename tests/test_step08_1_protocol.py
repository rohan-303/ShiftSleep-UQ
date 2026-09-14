import csv
import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]


def rows(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def counts(dataset):
    source = rows("reports/subject_partitions_v2.csv")
    return {
        role: sum(r["dataset"] == dataset and r["source_role"] == role for r in source)
        for role in ("TRAIN", "DEV", "CALIBRATION", "TEST")
    }


def test_step081_has_four_source_roles_and_required_counts():
    source = rows("reports/subject_partitions_v2.csv")
    assert len(source) == 177
    assert {r["source_role"] for r in source} == {"TRAIN", "DEV", "CALIBRATION", "TEST"}
    assert counts("sleep_edf_sc") == {"TRAIN": 47, "DEV": 12, "CALIBRATION": 8, "TEST": 11}
    assert counts("isruc_s1") == {"TRAIN": 59, "DEV": 15, "CALIBRATION": 10, "TEST": 15}
    assert len({(r["dataset"], r["subject_id"]) for r in source}) == 177


def test_step081_isruc_montage_quotas_are_exact_and_deterministic():
    source = rows("reports/subject_partitions_v2.csv")
    expected = {
        ("ISRUC_A1A2", "TRAIN"): 10,
        ("ISRUC_A1A2", "DEV"): 3,
        ("ISRUC_A1A2", "CALIBRATION"): 2,
        ("ISRUC_A1A2", "TEST"): 2,
        ("ISRUC_M1M2", "TRAIN"): 49,
        ("ISRUC_M1M2", "DEV"): 12,
        ("ISRUC_M1M2", "CALIBRATION"): 8,
        ("ISRUC_M1M2", "TEST"): 13,
    }
    actual = {(montage, role): sum(r["montage_variant"] == montage and r["source_role"] == role for r in source) for montage, role in expected}
    assert actual == expected
    assert "I040" not in {r["subject_id"] for r in source if r["dataset"] == "isruc_s1"}


def test_step081_evaluation_mapping_and_role_firewall():
    protocol = yaml.safe_load((ROOT / "configs/evaluation_protocol_v1_1.yaml").read_text(encoding="utf-8"))
    assert protocol["protocol_version"] == "1.1.0"
    assert protocol["amendment_id"] == "A-08.1-01"
    assert protocol["split"]["seed"] == 2026
    assert protocol["evaluation_mapping"]["C0"]["population"] == "SOURCE_TEST"
    assert protocol["evaluation_mapping"]["C1"]["population"] == "SOURCE_TEST"
    assert protocol["evaluation_mapping"]["C2"]["population"] == "SOURCE_TEST"
    assert protocol["evaluation_mapping"]["C3"]["population"] == "COMPLETE_TARGET"
    assert protocol["evaluation_mapping"]["C4"]["population"] == "COMPLETE_TARGET"
    assert protocol["evaluation_mapping"]["C5"]["population"] == "COMPLETE_TARGET"
    assert protocol["role_firewall"]["TEST"]["may_fit_normalization"] is False
    assert protocol["role_firewall"]["TEST"]["may_select_checkpoint"] is False
    assert protocol["role_firewall"]["TEST"]["may_fit_temperature"] is False
    assert protocol["role_firewall"]["TEST"]["may_fit_conformal"] is False
    assert protocol["normalization"]["fit_scope"] == "SOURCE_TRAIN_ONLY"
    assert protocol["calibration"]["fit_scope"] == "SOURCE_CALIBRATION_ONLY"
    assert protocol["oracle"]["primary_results_use_oracle"] is False


def test_step081_preserves_c0_c5_and_oracle_artifact():
    protocol = yaml.safe_load((ROOT / "configs/evaluation_protocol_v1_1.yaml").read_text(encoding="utf-8"))
    assert protocol["c0_c5"] == yaml.safe_load((ROOT / "configs/evaluation_protocol_v1.yaml").read_text(encoding="utf-8"))["c0_c5"]
    old_oracle = ROOT / "reports/oracle_target_partitions_v1.csv"
    assert hashlib.sha256(old_oracle.read_bytes()).hexdigest() == protocol["oracle"]["manifest_sha256"]


def test_step081_protocol_hashes_reproduce():
    for line in (ROOT / "reports/step08_1_protocol_hashes.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            path, digest = line.split(",", 1)
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
