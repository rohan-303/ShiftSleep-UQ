# ShiftSleep-UQ Step 15.1 B1 Statistical Finalization Report

## 1. Status

`STEP15_1_PARTIAL_FINALIZATION_BLOCKED`

Step 15.1 preserved the frozen calibration and prediction artifacts, finalized the 36-row prediction manifest, generated shared 2,000-replicate subject multiplicity matrices, and finalized deterministic per-seed B1 point metrics. The exact weighted ranking-statistics bootstrap did not finish within the execution window. No incomplete inferential output was accepted.

## 2. Final Evaluation Gate

`B1_PRIMARY_EVALUATION_PARTIAL`

The gate is not `B1_PRIMARY_EVALUATION_COMPLETE` because B1 multi-seed confidence intervals, paired B0-vs-B1 statistics, compound-failure classification, and the final interpretation case remain incomplete.

## 3. Reason Step 15.1 Was Required

The original Step 15 runner repeatedly reconstructed large epoch arrays during bootstrap finalization. Step 15.1 introduced artifact-only post-processing and subject-multiplicity sufficient statistics. It did not change the scientific protocol.

## 4. Frozen Prediction Integrity

Verified before finalization: exactly 36 B1 prediction bundles exist, all six B1 checkpoint hashes reproduce, all B0/B1 observation keys and labels align, and the 36-row B1 prediction manifest was written before statistical processing.

## 5. Frozen Calibration Integrity

Verified: six B1 temperature objects and six B1 APS objects were reused without refitting. Their namespace and hashes were unchanged.

## 6. B0 Comparator Integrity

Verified: B0 v1.1 prediction bundles, result tables, contrasts, and `artifacts/statistics/b0/bootstrap_replicates_v1_1.npz` were unchanged. The authoritative bootstrap SHA-256 is `47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022`.

## 7. No-Inference / No-Refit Confirmation

`VERIFIED`. Step 15.1 did not load model checkpoints, execute model inference, read raw PSG signal, fit temperature, fit APS, fit normalization, access ORACLE data, or access SHHS.

## 8. Bootstrap Draw Construction

The finalizer generated one deterministic subject-draw schedule per evaluation population using NumPy `default_rng(2028)`, sampling each population's sorted subject list with replacement for 2,000 replicates.

## 9. Subject Multiplicity Representation

Each draw was converted to an integer `[replicate, subject]` multiplicity matrix. Duplicate draws retain full cluster weight. The ignored artifact is `artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz`.

## 10. Statistical Optimization Strategy

The finalizer used subject-level weighted confusion matrices and per-subject additive sufficient statistics for macro-F1, NLL, Brier, and conformal coverage/gap. Ranking metrics used fixed uncertainty ordering and weighted repeated-observation semantics. The ranking pass remained computationally incomplete.

## 11. Equivalence to Literal Cluster Duplication

`NOT COMPLETED`. The optimized implementation was compiled and exercised on the frozen artifacts, but the required complete equivalence-test package was not finalized before the ranking pass was stopped.

## 12. Resumable Shard Design

`NOT COMPLETED`. The frozen draw artifact is resumable input, but per-metric statistical shards were not finalized.

## 13. B1 Per-Seed Metrics

`VERIFIED`: `reports/b1_primary_metrics_per_seed_v1.csv` was generated from the 36 frozen bundles. It contains deterministic per-seed point metrics and calibration/conformal rows. No inferential interpretation was made from this table.

## 14. D1 B1 C0–C5 Results

Per-seed extraction exists. Final multi-seed/bootstrap results: `NOT COMPUTED`.

## 15. D2 B1 C0–C5 Results

Per-seed extraction exists. Final multi-seed/bootstrap results: `NOT COMPUTED`.

## 16. B1 Multi-Seed Stability

`NOT COMPUTED`. The required 2,000-replicate multi-seed confidence intervals were not finalized.

## 17. Primary Compound Macro-F1 B1-vs-B0

`NOT COMPUTED`. D1 C4, D1 C5, D2 C4, and D2 C5 paired macro-F1 point/CI tables were not accepted.

## 18. Known-Domain Missing-Modality Effects

`NOT COMPUTED`. C1-C0 and C2-C0 paired inferential results remain open.

## 19. Full-Modality Guardrail

`NOT COMPUTED`. C0 and C3 B1-B0 guardrail results were not finalized.

## 20. Calibration B1-vs-B0

`NOT COMPUTED`. Temperature-scaled NLL, Brier, and ECE contrasts were not finalized.

## 21. Error-Ranking B1-vs-B0

`NOT COMPUTED`. Entropy AUROC and AUPRC paired confidence intervals were not finalized.

## 22. Selective Reliability B1-vs-B0

`NOT COMPUTED`. AURC and fixed-coverage paired results were not finalized.

## 23. Conformal B1-vs-B0

`NOT COMPUTED`. Signed gap and absolute coverage-error comparisons were not finalized.

## 24. Compound Failure Matrix

`NOT COMPUTED`. No compound matrix was accepted.

## 25. Reliability Persistence

`NOT IDENTIFIABLE`. The required paired reliability axes were not complete.

## 26. Stage-Level Changes

`NOT COMPUTED`. Stage-level paired bootstrap results were not finalized.

## 27. Confusion Changes

Per-seed B1 confusion counts were extracted. The required finalized B1-B0 row-normalized confusion artifact was not created.

## 28. Domain × Modality Interactions

`NOT COMPUTED`.

## 29. B1-vs-B0 Interaction Changes

`NOT COMPUTED`.

## 30. ISRUC Montage Sensitivity

`NOT COMPUTED AS FINAL`. No accepted paired montage artifact was created.

## 31. Interpretation Case

`NOT ASSIGNED`. CASE_A, CASE_B, CASE_C, CASE_D, and MIXED_CASE require complete paired statistics.

## 32. Scientific Interpretation

No scientific conclusion is authorized. Verified results are limited to frozen artifact integrity, manifest creation, subject-draw construction, and deterministic per-seed extraction.

## 33. What B1 Explains About B0

`NOT COMPUTED`.

## 34. What B1 Does Not Explain

`NOT COMPUTED`.

## 35. Canonical Result Artifacts

Verified or created:

- `reports/b1_primary_prediction_hashes_v1.txt` — 36 entries;
- `reports/b1_bootstrap_draw_hashes_v1.txt` — four population rows;
- `reports/b1_primary_metrics_per_seed_v1.csv`;
- `artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz`;
- `reports/step15_1_data_access_audit.csv`;
- `reports/step15_1_evaluation_gate.json`.

Not created/accepted:

- `reports/b1_primary_results_multiseed_v1.csv`;
- `reports/b1_primary_contrasts_v1.csv`;
- `reports/b1_vs_b0_paired_results_v1.csv`;
- `reports/b1_vs_b0_compound_failure_matrix_v1.csv`;
- `reports/b1_vs_b0_stage_analysis_v1.csv`;
- `reports/b1_vs_b0_confusion_analysis_v1.csv`;
- `reports/b1_isruc_montage_sensitivity_v1.csv`;
- `reports/b1_statistical_hashes_v1.txt`;
- `artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz`.

## 36. Prediction Hash Manifest

`VERIFIED`: `reports/b1_primary_prediction_hashes_v1.txt` contains exactly 36 bundle entries. Every hash was calculated from the frozen on-disk bundle.

## 37. Statistical Hash Manifest

`NOT CREATED`. The final statistical result tables and canonical bootstrap replicate artifact do not exist as complete outputs.

## 38. Bootstrap Artifact Hash

The subject-multiplicity artifact exists and is hashed in `reports/b1_bootstrap_draw_hashes_v1.txt`. The canonical completed replicate artifact was not created.

## 39. Tests Added

`NOT COMPLETED`. No Step 15.1 equivalence-test package was accepted.

## 40. Equivalence Tests

`NOT COMPLETED`. Required tests cover macro-F1, NLL, Brier, ECE, AUROC, AUPRC, AURC, conformal coverage, signed gap, mean set size, and the `[A,A,C]` duplicate regression. They remain open.

## 41. Resume/Recovery Tests

`NOT COMPLETED`. The draw artifact is persistent, but a complete shard resume test was not accepted.

## 42. Full Validation

Verified:

- finalizer compilation;
- frozen B0/B1 input hashes before processing;
- 36-row prediction manifest;
- four 2,000-replicate multiplicity matrices;
- deterministic per-seed table generation;
- no model inference;
- no calibration refit;
- no raw PSG access;
- no ORACLE or SHHS access.

Not complete: full test suite after finalizer implementation, complete ranking bootstrap, complete paired tables, complete result hashes, and post-commit verification.

## 43. Files Created

- `scripts/step15_1_finalize.py`;
- `reports/b1_primary_prediction_hashes_v1.txt`;
- `reports/b1_bootstrap_draw_hashes_v1.txt`;
- `reports/b1_primary_metrics_per_seed_v1.csv`;
- `reports/step15_1_data_access_audit.csv`;
- `reports/step15_1_evaluation_gate.json`;
- `artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz`.

## 44. Files Modified

The historical Step 15 partial report was preserved byte-for-byte. No B1 checkpoint, calibration JSON, B0 comparator, normalization, partition, or evaluation protocol was modified.

## 45. Explicitly Not Done

- no retraining;
- no checkpoint reselection;
- no model inference;
- no normalization refit;
- no temperature refit;
- no APS refit;
- no target fitting;
- no oracle analysis;
- no changed statistical protocol;
- no reduced bootstrap count;
- no accepted approximation;
- no new scientific method;
- no SHHS;
- no Step 16;
- no push.

## 46. Primary Result Freeze

`NOT FROZEN`. The prediction manifest and draw matrices are frozen; final inferential results and statistical hash manifest do not exist.

## 47. Remaining Scientific Questions

All B1-vs-B0 predictive, calibration, selective, conformal, stage, montage, interaction, and reliability-persistence questions remain open.

## 48. Recommended Next Step

Do not execute Step 16. Repair the exact weighted ranking-statistics finalizer, add the required equivalence and resume tests, and rerun Step 15.1 statistics-only from the frozen prediction bundles.

## 49. Git Status / Diff Summary

Step 15.1 remains uncommitted and partial. Heavy prediction/calibration/statistical artifacts remain outside the committed artifact set. No push occurred.
