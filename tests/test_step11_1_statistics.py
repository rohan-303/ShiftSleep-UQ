from __future__ import annotations

import numpy as np

from shiftsleep_uq.evaluation_step11 import (
    aps_prediction_set,
    aps_quantile,
    aps_scores,
    aurc,
    macro_f1,
)
from shiftsleep_uq.step11_1_statistics import (
    bootstrap_metric_from_bundles,
    bootstrap_subject_draws,
    conformal_gap_orientation,
    identity_metric_from_bundle,
    paired_bootstrap_difference,
    reconstruct_cluster_indices,
    interaction_bootstrap_difference,
    percentile_interval,
)


def _bundle(subjects, labels, predictions, probabilities=None):
    labels = np.asarray(labels, dtype=np.int64)
    predictions = np.asarray(predictions, dtype=np.int64)
    if probabilities is None:
        probabilities = np.full((len(labels), 5), 0.01, dtype=np.float64)
        probabilities[np.arange(len(labels)), predictions] = 0.96
    logits = np.log(probabilities)
    return {
        "subject_id": np.asarray(subjects),
        "labels": labels,
        "logits": logits,
    }


def test_duplicate_subject_draw_preserves_cluster_multiplicity() -> None:
    subjects = np.asarray(["A", "A", "B", "C"])
    sampled = np.asarray([0, 0, 2])
    idx = reconstruct_cluster_indices(subjects, sampled, ["A", "B", "C"])
    assert np.array_equal(idx, [0, 1, 0, 1, 3])
    duplicated = _bundle(subjects[idx], [0, 1, 2, 0, 1], [0, 0, 2, 0, 0])
    collapsed = _bundle(subjects[[0, 1, 3]], [0, 1, 1], [0, 0, 1])
    assert macro_f1(duplicated["logits"].argmax(1), duplicated["labels"]) != macro_f1(
        collapsed["logits"].argmax(1), collapsed["labels"]
    )


def test_identity_subject_sample_reproduces_full_metric() -> None:
    b = _bundle(["A", "A", "B", "C"], [0, 1, 2, 3], [0, 1, 1, 3])
    for metric in ("macro-F1", "NLL", "Brier", "ERROR_AUROC", "ERROR_AUPRC", "AURC"):
        assert np.isclose(identity_metric_from_bundle(b, metric), identity_metric_from_bundle(b, metric, identity=True))


def test_same_bootstrap_subject_sequence_is_shared_across_seeds() -> None:
    draws = bootstrap_subject_draws(4, reps=8, seed=2028)
    assert np.array_equal(draws, bootstrap_subject_draws(4, reps=8, seed=2028))


def test_fixed_five_class_macro_f1_includes_absent_classes() -> None:
    b = _bundle(["A", "B"], [0, 0], [0, 0])
    assert np.isclose(identity_metric_from_bundle(b, "macro-F1"), 0.2)


def test_percentile_interval_uses_exact_2_5_and_97_5_endpoints() -> None:
    values = np.arange(2000, dtype=float)
    low, high = percentile_interval(values)
    assert low == np.percentile(values, 2.5)
    assert high == np.percentile(values, 97.5)


def test_paired_condition_bootstrap_uses_one_subject_draw() -> None:
    full = _bundle(["A", "A", "B"], [0, 1, 2], [0, 1, 2])
    eeg = _bundle(["A", "A", "B"], [0, 1, 2], [0, 0, 2])
    out = paired_bootstrap_difference([eeg], [full], "macro-F1", reps=4, seed=2028)
    assert out.shape == (4,)


def test_interaction_bootstrap_samples_source_and_target_independently() -> None:
    source = _bundle(["A", "B"], [0, 1], [0, 1])
    target = _bundle(["X", "Y"], [0, 1], [1, 1])
    out = interaction_bootstrap_difference(source, source, target, target, "macro-F1", reps=4, seed=2028)
    assert out.shape == (4,)


def test_signed_conformal_gap_orientation_is_zero_ideal() -> None:
    assert conformal_gap_orientation() == "zero_is_ideal_signed_gap"


def test_aps_qhat_monotonicity_and_set_nesting() -> None:
    p = np.array([[0.60, 0.25, 0.10, 0.03, 0.02], [0.20, 0.50, 0.15, 0.10, 0.05]])
    y = np.array([0, 1])
    q90 = aps_quantile(aps_scores(p, y), 0.10)
    q95 = aps_quantile(aps_scores(p, y), 0.05)
    assert q95 >= q90
    s90 = aps_prediction_set(p, q90)
    s95 = aps_prediction_set(p, q95)
    assert np.all(~s90 | s95)


def test_aps_exact_synthetic_set_membership() -> None:
    p = np.array([[0.60, 0.25, 0.10, 0.03, 0.02]])
    assert np.array_equal(aps_prediction_set(p, 0.60), [[True, False, False, False, False]])
    assert np.array_equal(aps_prediction_set(p, 0.85), [[True, True, False, False, False]])


def test_bootstrap_reproducibility_seed_2028() -> None:
    b = _bundle(["A", "A", "B", "C"], [0, 1, 2, 3], [0, 0, 2, 3])
    a = bootstrap_metric_from_bundles([b, b], "macro-F1", reps=8, seed=2028)
    c = bootstrap_metric_from_bundles([b, b], "macro-F1", reps=8, seed=2028)
    assert np.array_equal(a, c)
