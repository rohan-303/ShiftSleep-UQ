# Original Step 12.1 Method-Gate Specification

- **Criterion A — residual reliability failure:** identify compound target cells with reliability degradation beyond the predictive degradation, using the written reliability taxonomy: NLL, Brier, ECE, error ranking/selective metrics, or conformal coverage/set behavior. The operational source-temperature-only rule is not the full written criterion.
- **Criterion B — recoverability:** a residual failure is recoverable when frozen oracle calibration produces threshold-qualified improvement in NLL/Brier/ECE or conformal absolute coverage error without pathological set-size inflation; the written cell evidence is assessed across compound cells, not by a source-temperature conjunction.
- **Criterion C — source-only deployability:** any future candidate must fit only on permitted source calibration data, remain frozen before target evaluation, and use no target labels, target normalization, target thresholds, or target fitting.
- **Criterion D — predictive confounding:** determine whether the observed reliability failure is substantially dominated by predictive/representation transfer loss that calibration cannot repair because scalar calibration does not change argmax predictions. B1 is the required predictive robustness control for this reassessment.

The original final decision was `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`; Step 16 reassesses these criteria using frozen B1 evidence and separate source-only/oracle diagnostics.
