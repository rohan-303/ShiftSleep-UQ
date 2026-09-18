# ShiftSleep-UQ Step 15.3 B1 Primary Evaluation and Paired B0 v1.2 Comparison Report

## 1. Status

`STEP_15_3_COMPLETE`. The frozen B1 primary evaluation was executed against authoritative B0 v1.2. No Step 16 work was executed.

## 2. Evaluation Gate

`B1_PRIMARY_EVALUATION_COMPLETE`

All 36 frozen B1 bundles, C0–C5 statistics, 2,000-replicate vectors, paired comparisons, compound cells, stage analysis, confusion analysis, interactions, montage evidence, hashes, tests, and validation completed.

## 3. Starting Authoritative State

B0 statistics were `v1_2` with `B0_V1_2_AUTHORITATIVE`. The ranking engine was `WEIGHTED_RANKING_ENGINE_FROZEN`. B1 was the preregistered source-modality-dropout control. The method gate remained `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`.

## 4. B0 v1.2 Integrity

B0 v1.2 bootstrap SHA-256: `e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1`.

B0 v1.2 primary-results SHA-256: `617fd699d0a0549abe9a032ff4cd3ae366a3c3863e8f314f17f722878bc9caa9`.

B0 v1.2 contrasts SHA-256: `ac1f8b75fdfacf25509560c258889b1b3653e0c87cb0e2925c43f2503971343a`.

The historical v1.1 artifacts were not used as inferential comparators.

## 5. Weighted Engine Integrity

The frozen engine gate metadata reported `WEIGHTED_RANKING_ENGINE_FROZEN`. The exact engine hashes were checked before evaluation and were not modified.

## 6. B1 Checkpoint Integrity

All six checkpoint hashes matched `reports/b1_checkpoint_hashes_v1.txt`, including the expected D1/D2 seeds 17, 42, and 2026. No checkpoint was loaded for inference during this step; the frozen prediction bundles were the evaluation inputs.

## 7. B1 Calibration Integrity

The six frozen SOURCE temperature objects and six SOURCE APS objects were read from `artifacts/calibration/b1_moddrop/`. Their existing manifest and `SOURCE_CALIBRATION_FROZEN` state were preserved. No temperature or APS fitting occurred.

## 8. B1 Prediction Integrity

The prediction manifest contained exactly 36 bundles. Every on-disk bundle hash matched. The canonical prediction manifest remains `reports/b1_primary_prediction_hashes_v1.txt`.

## 9. B0/B1 Observation Alignment

All 36 matched B0/B1 bundles agreed on labels, subject IDs, recording IDs, epoch indices, montage identifiers, and epoch counts. No alignment failure occurred.

## 10. Bootstrap Draw Integrity

The frozen B1 multiplicity matrices were reused from `artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz`. They contain four population matrices, each with 2,000 rows, nonnegative integer counts, correct row sums, and the recorded seed-2028 provenance.

## 11. Production Shard Execution

B1 production used 100-replicate shards under `artifacts/statistics/b1_moddrop/shards_v1/`. The exact engine was used for ranking metrics. Additive metrics and conformal coverage were computed with the same subject multiplicities.

## 12. Shard Completeness

`reports/step15_3_shard_completeness_audit.csv` contains 7,200 expected shards: 2 directions × 6 conditions × 3 seeds × 10 metrics × 20 ranges. Every range was present, valid, non-overlapping, and consumed exactly once. Heavy shards remain Git-ignored.

## 13. B1 Per-Seed Metrics

`reports/b1_primary_metrics_per_seed_v1.csv` contains the frozen per-seed C0–C5 values for macro-F1, calibrated NLL/Brier, uncalibrated error ranking, AURC, and conformal metrics. All three model seeds are retained.

## 14. D1 C0–C5 Results

D1 B1 results are in `reports/b1_primary_results_multiseed_v1.csv`. C4 macro-F1 improved over B0 by `+0.03673` with paired 95% CI `[+0.03141,+0.04215]`; C5 improved by `+0.18587` with CI `[+0.16786,+0.20296]`. Known-domain C1/C2 effects and full-modality C0/C3 are retained in the canonical table.

## 15. D2 C0–C5 Results

D2 C4 macro-F1 improved by `+0.05992` with CI `[+0.05308,+0.06667]`. D2 C5 was effectively unchanged: `+0.00063`, CI `[-0.01255,+0.01451]`. All D2 C0–C5 rows are present in the canonical result table.

## 16. Multi-Seed Stability

Every primary row reports the mean of independently computed seeds 17, 42, and 2026 plus sample seed SD. No seed was discarded or selected by performance.

## 17. Primary Compound Macro-F1 B1-vs-B0

The primary compound cells show supported improvement in D1 C4, D1 C5, and D2 C4. D2 C5 is inconclusive and small magnitude.

## 18. D1 C4

Macro-F1 delta: `+0.03673`; CI `[+0.03141,+0.04215]`; `SUPPORTED_IMPROVEMENT`; `PRACTICALLY_NOTABLE_GAIN`.

## 19. D1 C5

Macro-F1 delta: `+0.18587`; CI `[+0.16786,+0.20296]`; `SUPPORTED_IMPROVEMENT`; `PRACTICALLY_NOTABLE_GAIN`.

## 20. D2 C4

Macro-F1 delta: `+0.05992`; CI `[+0.05308,+0.06667]`; `SUPPORTED_IMPROVEMENT`; `PRACTICALLY_NOTABLE_GAIN`.

## 21. D2 C5

Macro-F1 delta: `+0.00063`; CI `[-0.01255,+0.01451]`; `INCONCLUSIVE_DIRECTION`; `SMALL_MAGNITUDE`.

## 22. Known-Domain Missing-Modality Effects

The known-domain C1/C2 paired effects are reported in `reports/b1_vs_b0_paired_results_v1.csv`. These are descriptive controls for the intervention’s explicitly trained missing-modality setting and are not substituted for the primary unseen-domain cells.

## 23. Full-Modality Source Comparison

D1 C0 and D2 C0 B1-vs-B0 macro-F1 effects are reported descriptively with paired confidence intervals. No source full-modality pass/fail threshold was applied.

## 24. Full-Modality Target Guardrail

D1 C3 and D2 C3 were checked against the frozen `-0.02` tradeoff rule. Neither direction was classified as a practically notable full-modality tradeoff.

## 25. Calibration Comparison

Primary calibration used SOURCE-temperature-scaled probabilities. Paired NLL and Brier results are in `reports/b1_vs_b0_paired_results_v1.csv`. D1 C4 and C5 NLL improved; D2 C4 improved; D2 C5 NLL worsened with CI `[+0.07808,+0.25053]`.

## 26. Error-Ranking Comparison

Primary error ranking used uncalibrated predictive entropy. ERROR_AUROC and ERROR_AUPRC were computed with the frozen exact duplicate-preserving engine. The paired table contains both metrics for all conditions.

## 27. Selective-Prediction Comparison

AURC used uncalibrated predictive entropy and exact subject-bootstrap semantics. D1 C4, D1 C5, D2 C4, and D2 C5 all had negative AURC deltas, with supported improvement in each primary cell.

## 28. Conformal Comparison

APS conformal metrics used each frozen model’s SOURCE APS object at alpha 0.10 and 0.05. The primary residual axis was alpha 0.10 absolute coverage error; no alpha was changed after observing results.

## 29. Compound Failure Matrix

`reports/b1_vs_b0_compound_failure_matrix_v1.csv` contains exactly the four primary cells and the three primary reliability axes: SOURCE-temperature NLL, entropy AURC, and alpha-0.10 absolute coverage error.

## 30. Residual Reliability Classification

- D1 C4: `MIXED_RELIABILITY_RESPONSE` — calibration and selective reliability improved, conformal absolute-gap axis worsened.
- D1 C5: `RELIABILITY_IMPROVES_WITH_PREDICTION`.
- D2 C4: `RELIABILITY_IMPROVES_WITH_PREDICTION`.
- D2 C5: `MIXED_RELIABILITY_RESPONSE` — calibration worsened, selective improved, conformal axis inconclusive.

## 31. Stage-Level Effects

`reports/b1_vs_b0_stage_analysis_v1.csv` contains all five stage recalls for every direction and condition, with paired 2,000-replicate confidence intervals. C3, C4, and C5 are included as required.

## 32. Confusion Changes

`reports/b1_vs_b0_confusion_analysis_v1.csv` contains all 25 row-normalized confusion cells for every direction and C0–C5 condition. No favorable-transition-only selection was used.

## 33. B1 Domain × Modality Interactions

B1 EEG-only and EOG-only interactions were computed as `(C4-C3)-(C1-C0)` and `(C5-C3)-(C2-C0)` for the primary metric families. Results are in `reports/b1_vs_b0_interaction_analysis_v1.csv`.

## 34. B1-vs-B0 Interaction Changes

The interaction artifact reports B1 interaction, B0 v1.2 interaction, and their paired difference with confidence intervals. B0 values use v1.2 arrays only.

## 35. ISRUC Montage Sensitivity

The frozen B1 ISRUC montage analysis is preserved in `reports/b1_isruc_montage_sensitivity_v1.csv`. It reports ISRUC_A1A2 and ISRUC_M1M2 associations for the requested metrics. No causal montage claim or rebalancing was made.

## 36. Interpretation Case

`MIXED_CASE`

D1 and D2 differ in D2 C5, and the reliability response differs across primary cells. A single cleaner CASE_A/B/C/D assignment would discard observed heterogeneity.

## 37. Direction-Specific Interpretation

D1 supports substantial missing-modality predictive gains in both C4 and C5. D1 C4 retains a conformal reliability worsening axis, while D1 C5 improves across all three primary reliability axes. D2 supports C4 improvement across prediction and reliability but does not establish a C5 predictive gain; D2 C5 has mixed reliability evidence.

## 38. What B1 Explains About B0

B1 demonstrates that source-only modality-dropout training can improve predictive robustness in three of the four primary compound cells. It also shows that the predictive intervention can improve calibration and selective ranking without guaranteeing conformal improvement in every cell.

## 39. What B1 Does Not Explain

B1 does not establish a universal reliability repair, does not remove all direction/modality heterogeneity, and does not authorize a new reliability method. It does not provide target oracle evidence or causal montage evidence.

## 40. Implications for the Original ShiftSleep-UQ Hypotheses

F1: source-only modality-dropout training improves missing-modality robustness in D1 C4, D1 C5, and D2 C4, but not conclusively in D2 C5.

F2: robustness gains are direction- and modality-dependent rather than universal.

F3: predictive improvement does not guarantee uniform calibration, selective, and conformal reliability improvement.

F4: residual failures remain heterogeneous across reliability families and domains.

F5: the B1 control does not by itself justify changing the frozen evaluation protocol or authorizing a new method.

F6 method efficacy is not addressed here.

## 41. Canonical B1 Result Artifacts

- `artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz`;
- `reports/b1_primary_metrics_per_seed_v1.csv`;
- `reports/b1_primary_results_multiseed_v1.csv`;
- `reports/b1_primary_contrasts_v1.csv`;
- `reports/b1_vs_b0_paired_results_v1.csv`;
- `reports/b1_vs_b0_compound_failure_matrix_v1.csv`;
- `reports/b1_vs_b0_stage_analysis_v1.csv`;
- `reports/b1_vs_b0_confusion_analysis_v1.csv`;
- `reports/b1_vs_b0_interaction_analysis_v1.csv`;
- `reports/b1_isruc_montage_sensitivity_v1.csv`;
- `reports/step15_3_shard_completeness_audit.csv`;
- `reports/step15_3_data_access_audit.csv`;
- `reports/step15_3_b1_evaluation_gate.json`.

## 42. B1 Prediction Hash Manifest

`reports/b1_primary_prediction_hashes_v1.txt` contains 36 verified frozen prediction bundles. No prediction bundle was rewritten.

## 43. B1 Statistical Hash Manifest

`reports/b1_statistical_hashes_v1.txt` hashes the B1 bootstrap artifact, per-seed table, multi-seed results, contrasts, paired results, compound matrix, stage analysis, confusion analysis, interaction analysis, montage analysis, shard audit, data-access audit, and gate metadata.

## 44. B0 v1.2 Comparator Hashes

- bootstrap: `e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1`;
- primary results: `617fd699d0a0549abe9a032ff4cd3ae366a3c3863e8f314f17f722878bc9caa9`;
- contrasts: `ac1f8b75fdfacf25509560c258889b1b3653e0c87cb0e2925c43f2503971343a`.

## 45. Weighted Engine Hashes

The frozen engine hashes are recorded in `reports/weighted_bootstrap_engine_gate_v1_2.json` and were verified before B1 evaluation.

## 46. Tests Added

`tests/test_step15_3_b1_finalization.py` covers authoritative B0 v1.2 hashes, frozen engine status, 120 B1 arrays, 7,200 shards, and Step 16 exclusion. Existing engine/provenance tests remain active.

## 47. Full Validation

- B1 shard production: `7,200` valid shards;
- B1 arrays: `120` vectors × `2,000` replicates;
- B1 prediction bundles: `36/36` hashes verified;
- B0/B1 alignment: `36/36` matched;
- full confusion matrix: `300` cells;
- stage analysis: `60` rows;
- compound matrix: `4` primary cells;
- data-access audit: artifact reads only;
- no raw PSG, oracle, SHHS, training, or inference access;
- full repository tests: `146 passed`;
- compileall: passed;
- `git diff --check`: passed;
- frozen-input and tracked-artifact checks: passed.

## 48. Files Created

- `scripts/step15_3_b1_frozen_evaluation.py`;
- `scripts/step15_3_b1_postprocess.py`;
- `tests/test_step15_3_b1_finalization.py`;
- `reports/b1_statistical_hashes_v1.txt`;
- `reports/b1_primary_results_multiseed_v1.csv`;
- `reports/b1_primary_contrasts_v1.csv`;
- `reports/b1_vs_b0_paired_results_v1.csv`;
- `reports/b1_vs_b0_compound_failure_matrix_v1.csv`;
- `reports/b1_vs_b0_stage_analysis_v1.csv`;
- `reports/b1_vs_b0_confusion_analysis_v1.csv`;
- `reports/b1_vs_b0_interaction_analysis_v1.csv`;
- `reports/step15_3_shard_completeness_audit.csv`;
- `reports/step15_3_data_access_audit.csv`;
- `reports/step15_3_b1_evaluation_gate.json`;
- `reports/STEP_15_3_B1_PRIMARY_EVALUATION_AND_B0_V1_2_COMPARISON_REPORT.md`.

## 49. Files Modified

- `reports/b1_primary_metrics_per_seed_v1.csv` was finalized from the frozen prediction bundles;
- `reports/b1_primary_prediction_hashes_v1.txt` remained unchanged;
- `reports/b1_isruc_montage_sensitivity_v1.csv` remained unchanged;
- no B0 v1.1 or v1.2 artifact was modified.

## 50. Explicitly Not Done

- no training;
- no inference rerun;
- no checkpoint reselection;
- no normalization fitting;
- no calibration fitting;
- no APS fitting;
- no target fitting;
- no oracle B1 analysis;
- no target adaptation;
- no new method;
- no Step 16;
- no SHHS;
- no protocol changes;
- no bootstrap changes.

## 51. B1 Primary Result Freeze

The B1 primary package is frozen at 120 canonical multi-seed bootstrap vectors and 2,000 replicates per vector. Canonical artifact hashes are in `reports/b1_statistical_hashes_v1.txt`.

## 52. Remaining Scientific Questions

The remaining question is formal residual-failure diagnosis and reassessment of the reliability-method authorization gate. That work belongs to Step 16 and was not performed here.

## 53. Recommended Next Step

# Step 16 — Diagnose B1 Residual Failures and Reassess the Reliability-Method Authorization Gate

This is a recommendation only. Step 16 was not executed.

## 54. Git Commit

Milestone commit: `16a7cfc21bf2e5c8a8d057073fd357f2791818c5` — `eval: freeze B1 primary robustness results`.

A final documentation-only commit records the externally verified push state without changing scientific artifacts.

## 55. Milestone Tag

Tag: `step15-b1-evaluation-frozen`

Tag target: `16a7cfc21bf2e5c8a8d057073fd357f2791818c5`, exactly the validated B1 primary-result milestone commit.

## 56. GitHub Push Status

`PUSH_COMPLETE`

Remote: `origin` (`https://github.com/rohan-303/ShiftSleep-UQ.git`).

Branch push: `main` succeeded.

Tag push: `step15-b1-evaluation-frozen` succeeded.

No force push or history rewrite was used.

## 57. Git Status / Diff Summary

The scientific milestone tree was clean before tagging and pushing. The final documentation-only commit is pushed separately; the tag remains pinned to the validated B1 milestone commit above. Remote read-back verified the branch and tag targets. Heavy shards remain ignored and untracked.
