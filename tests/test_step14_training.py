import csv
import hashlib
import json
from pathlib import Path

import torch
import pytest

from shiftsleep_uq.models.baseline_b0 import BaselineB0, count_trainable_parameters

ROOT = Path(__file__).parents[1]
EXPECTED_NORMS = {
    "D1_SLEEPEDF_TO_ISRUC": "be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3",
    "D2_ISRUC_TO_SLEEPEDF": "3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e",
}


def test_step14_has_exactly_six_complete_summary_rows_and_exposure_conservation():
    rows = list(csv.DictReader(open(ROOT / "reports/b1_training_summary_v1.csv", newline="")))
    assert len(rows) == 6
    assert {(r["experiment_id"], int(r["seed"])) for r in rows} == {
        (experiment, seed)
        for experiment in EXPECTED_NORMS
        for seed in (17, 42, 2026)
    }
    for row in rows:
        total = sum(int(row[field]) for field in ("cumulative_full_exposures", "cumulative_eeg_only_exposures", "cumulative_eog_only_exposures"))
        assert total > 0
        assert int(row["cumulative_forbidden_exposures"]) == 0
        assert sum(float(row[field]) for field in ("full_fraction", "eeg_only_fraction", "eog_only_fraction")) == pytest.approx(1.0)


def test_step14_checkpoint_hashes_reload_and_match_manifests():
    rows = list(csv.DictReader(open(ROOT / "reports/b1_checkpoint_hashes_v1.txt", newline="")))
    assert len(rows) == 6
    for row in rows:
        checkpoint = ROOT / row["relative_path"]
        assert checkpoint.exists()
        assert hashlib.sha256(checkpoint.read_bytes()).hexdigest() == row["sha256"]
        payload = torch.load(checkpoint, map_location="cpu", weights_only=False)
        model = BaselineB0()
        model.load_state_dict(payload["model_state_dict"])
        assert count_trainable_parameters(model) == 654597
        assert payload["metadata"]["architecture_id"] == "B0_DUAL_BRANCH_RAW_CNN"
        assert payload["metadata"]["exposure_seed"] == 2029
        manifest = json.loads((checkpoint.parent / "run_manifest.json").read_text())
        assert manifest["checkpoint_sha256"] == row["sha256"]
        assert manifest["cumulative_forbidden_count"] == 0


def test_step14_access_firewall_and_dev_history_schema():
    access = list(csv.DictReader(open(ROOT / "reports/step14_data_access_audit.csv", newline="")))
    assert access
    assert {(row["source_role"], row["purpose"]) for row in access} == {("TRAIN", "train"), ("DEV", "dev")}
    assert {row["dataset"] for row in access} == {"sleep_edf_sc", "isruc_s1"}
    for path in ROOT.glob("artifacts/models/b1_moddrop/**/training_history.csv"):
        fields = set(next(csv.reader(path.open(newline=""))))
        assert {"epoch", "train_cross_entropy", "dev_macro_f1", "dev_nll", "checkpoint_selected"} <= fields
        assert not {"test", "target", "calibration"} & {field.lower() for field in fields}


def test_step14_reuses_exact_b0_normalization_and_creates_no_forbidden_outputs():
    for experiment, expected in EXPECTED_NORMS.items():
        path = ROOT / f"artifacts/normalization/b0/{experiment}.json"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
    gate = ROOT / "reports/step15_b1_evaluation_gate.json"
    assert gate.exists() or not list((ROOT / "artifacts/predictions").glob("b1_moddrop/**/*"))
    assert gate.exists() or not list((ROOT / "artifacts/calibration").glob("b1_moddrop/**/*"))
    assert not list((ROOT / "artifacts/normalization").glob("b1/**/*"))
