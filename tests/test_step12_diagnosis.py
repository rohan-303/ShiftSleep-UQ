import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from shiftsleep_uq.evaluation_step11 import aps_prediction_set, ece, softmax
from step12_baseline_diagnosis import bootstrap_ece, fit_oracle_temperature, slice_bundle


def test_oracle_partition_roles_are_disjoint_and_complete():
    import csv
    rows = list(csv.DictReader((ROOT / "reports/oracle_target_partitions_v1.csv").open()))
    for dataset in sorted({r["dataset"] for r in rows}):
        subset = [r for r in rows if r["dataset"] == dataset]
        subjects = [r["subject_id"] for r in subset]
        assert len(subjects) == len(set(subjects))
        assert {r["oracle_role"] for r in subset} == {"ORACLE_CALIBRATION", "ORACLE_EVALUATION"}
        assert all(r["oracle_split_seed"] == "2027" for r in subset)


def test_scalar_temperature_preserves_argmax():
    logits = np.array([[2.0, 1.0, -1.0], [0.1, 3.0, 2.0]])
    assert np.array_equal(softmax(logits).argmax(1), softmax(logits / 4.2).argmax(1))


def test_aps_role_rule_is_nonempty_and_nested():
    probs = softmax(np.array([[3.0, 2.0, 0.0, -1.0, -2.0], [0.0, 0.0, 0.0, 0.0, 0.0]]))
    sets90 = aps_prediction_set(probs, 0.80)
    sets95 = aps_prediction_set(probs, 0.99)
    assert sets90.any(1).all() and sets95.any(1).all()
    assert np.all(~sets90 | sets95)


def test_oracle_temperature_fit_is_positive_and_improves_or_matches_calibration_nll():
    logits = np.array([[4.0, 0.0, 0.0, 0.0, 0.0], [0.0, 4.0, 0.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0, 0.0]], dtype=float)
    labels = np.array([0, 1, 2])
    result = fit_oracle_temperature(logits, labels)
    assert result["converged"]
    assert result["temperature"] > 0
    assert result["final_nll"] <= result["initial_nll"] + 1e-10


def test_bootstrap_ece_matches_duplicate_preserving_reconstruction():
    d = {
        "logits": np.array([[3., 0., 0., 0., 0.], [0., 2., 0., 0., 0.], [0., 0., 2., 0., 0.], [0., 0., 0., 3., 0.]]),
        "labels": np.array([0, 0, 2, 3]),
        "subject_id": np.array(["A", "A", "B", "B"]),
    }
    probs = softmax(d["logits"])
    draws = np.array([[0, 1], [1, 1]], dtype=int)
    observed = bootstrap_ece(d, probs, draws)
    identity = ece(probs, d["labels"])
    duplicate = slice_bundle(d, np.array([2, 3, 2, 3]))
    expected_duplicate = ece(softmax(duplicate["logits"]), duplicate["labels"])
    assert np.isclose(observed[0], identity)
    assert np.isclose(observed[1], expected_duplicate)
