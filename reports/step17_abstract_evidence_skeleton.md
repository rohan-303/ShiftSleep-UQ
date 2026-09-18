# Step 17 Abstract Evidence Skeleton

- **Problem:** Multimodal sleep-staging systems may encounter dataset and missing-modality shift simultaneously.
- **Gap:** Predictive robustness and reliability behavior require separate controlled evaluation.
- **Benchmark/protocol:** ShiftSleep-UQ evaluates reciprocal dataset shift, known/unseen modality conditions, source-only calibration, subject-level bootstrap inference, and a source modality-dropout control.
- **B0 finding:** Compound cells show direction- and modality-dependent predictive and reliability degradation.
- **B1 finding:** Macro-F1 improves in D1 C4 (+0.03673), D1 C5 (+0.18587), and D2 C4 (+0.05992), while D2 C5 is inconclusive (+0.00063).
- **Reliability:** Calibration, selective, and conformal responses remain heterogeneous; mask-specific source calibration does not uniformly resolve them.
- **Conclusion:** Predictive robustness improvements do not guarantee uniform reliability improvement, and the evidence does not authorize an additional learned reliability method.
