from __future__ import annotations

import numpy as np
import pytest

from shiftsleep_uq.evaluation_step11 import (
    EvaluationPhaseError,
    PhaseGate,
    aps_prediction_set,
    aps_quantile,
    aps_scores,
    compute_metric_rows,
    fit_temperature,
    softmax,
)


def test_phase_gate_rejects_calibration_after_freeze_and_requires_phase_b() -> None:
    gate = PhaseGate("PHASE_A_CALIBRATION")
    with pytest.raises(EvaluationPhaseError):
        gate.begin_evaluation()
    frozen = gate.freeze()
    phase_b = frozen.begin_evaluation()
    phase_b.require_evaluation()
    with pytest.raises(EvaluationPhaseError):
        phase_b.require_calibration()


def test_temperature_scaling_preserves_argmax_and_rejects_noncalibration() -> None:
    logits = np.array([[3., 1., 0., -1., -2.], [0., 2., 1., -1., -2.], [1., 0., 4., -2., -3.]])
    labels = np.array([0, 1, 2])
    with pytest.raises(EvaluationPhaseError):
        fit_temperature(logits, labels, role="TEST")
    result = fit_temperature(logits, labels, role="CALIBRATION")
    assert result["temperature"] > 0
    assert np.array_equal(softmax(logits).argmax(1), softmax(logits / result["temperature"]).argmax(1))


def test_aps_quantile_and_prediction_sets_are_deterministic_nonempty() -> None:
    probabilities = np.array([[0.60, 0.25, 0.10, 0.03, 0.02], [0.20, 0.50, 0.15, 0.10, 0.05]])
    labels = np.array([0, 1])
    scores = aps_scores(probabilities, labels)
    assert np.allclose(scores, [0.60, 0.50])
    assert aps_quantile(scores, 0.10) == 0.60
    sets = aps_prediction_set(probabilities, 0.60)
    assert sets.shape == probabilities.shape
    assert sets.any(1).all()
    assert sets[0, 0] and sets[1, 1]


def test_metric_engine_emits_fixed_class_metrics() -> None:
    logits = np.array([[4., 0., 0., 0., 0.], [0., 4., 0., 0., 0.], [0., 0., 4., 0., 0.]])
    labels = np.array([0, 1, 2])
    rows, matrix = compute_metric_rows(logits, labels, 1.0, {0.10: 0.6, 0.05: 0.6})
    assert matrix.shape == (5, 5)
    assert any(row["metric"] == "macro-F1" for row in rows)
    assert any(row["metric"] == "NLL" and row["probability_variant"] == "UNCALIBRATED" for row in rows)
    assert any(row["metric"].startswith("APS_empirical_coverage") for row in rows)
