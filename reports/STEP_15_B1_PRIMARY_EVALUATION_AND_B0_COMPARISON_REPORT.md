# ShiftSleep-UQ Step 15 B1 Primary Evaluation and Paired B0 Comparison Report

## 1. Status

`STEP15_PARTIAL_FINALIZATION_BLOCKED`

Phase A calibration and Phase-B inference completed and were independently verified. The corrected 2,000-replicate statistical finalization did not complete within the available execution window and was stopped without accepting partial statistical output.

## 2. Evaluation Gate

`B1_PRIMARY_EVALUATION_PARTIAL`

The package does not satisfy the Step 15 `COMPLETE` criteria because paired B0-vs-B1 statistical tables, compound-failure classification, and the scientific interpretation were not finalized.

## 3. Frozen B1 Inputs

Verified from disk: B1 model configuration, training configuration, protocol, six-run training summary, exposure summary, checkpoint manifest, six immutable checkpoint hashes, frozen B0 normalization objects, evaluation protocol, and subject partitions. No B1 retraining or checkpoint reselection occurred.

## 4. Frozen B0 Comparator

The authoritative B0 v1.1 comparator inputs were verified, including `reports/b0_primary_results_multiseed_v1_1.csv`, `reports/b0_primary_contrasts_v1_1.csv`, `reports/b0_primary_prediction_hashes_v1.txt`, and `artifacts/statistics/b0/bootstrap_replicates_v1_1.npz`. The v1.1 bootstrap artifact SHA-256 is `47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022`.

## 5. Calibration Phase-A Firewall

`VERIFIED`. Six B1 scalar temperatures and six distinct B1 APS objects were fitted from full-modality SOURCE CALIBRATION only: eight Sleep-EDF subjects for D1 and ten ISRUC subjects for D2. No SOURCE TEST, TARGET, ORACLE, or SHHS signal was used for fitting.

## 6. B1 SOURCE CALIBRATION Populations

D1: Sleep-EDF SOURCE CALIBRATION, full modality `[1,1]`, eight subjects.

D2: ISRUC SOURCE CALIBRATION, full modality `[1,1]`, ten subjects.

## 7. B1 Temperature Fits

`VERIFIED`: six temperature JSON artifacts and the six-row `reports/b1_temperature_calibration_v1.csv` were created. The fitted objects use `T = exp(log_T)`, initialization `T=1`, LBFGS, 100 maximum iterations, strong Wolfe line search, and the frozen tolerances.

## 8. B1 APS Fits

`VERIFIED`: six distinct APS JSON artifacts and the six-row `reports/b1_aps_calibration_v1.csv` were created. APS was fitted from uncalibrated SOURCE CALIBRATION probabilities at alpha 0.10 and 0.05 using the frozen finite-sample quantile rule.

## 9. B1 Calibration Freeze Gate

`B1_SOURCE_CALIBRATION_FROZEN`. The freeze metadata records six temperature objects, six APS objects, and Phase-B opening only after calibration artifacts were written and hashed.

## 10. Evaluation Phase-B Firewall

`VERIFIED`: Phase B used only SOURCE TEST and COMPLETE TARGET datasets. No fitting operation was executed after the freeze. No TRAIN, DEV, ORACLE, or SHHS signal access occurred during Step 15.

## 11. B1 Evaluation Populations

The exact B0 populations were used: D1 C0/C1/C2 on Sleep-EDF SOURCE TEST and C3/C4/C5 on complete ISRUC TARGET; D2 C0/C1/C2 on ISRUC SOURCE TEST and C3/C4/C5 on complete Sleep-EDF TARGET.

## 12. Prediction Alignment with B0

`VERIFIED`: all 36 B1 bundles were checked against their matched B0 bundle for labels, subject IDs, recording IDs, epoch indices, montage variants, ordering, and observation identity.

## 13. Prediction Artifact Integrity

`VERIFIED`: exactly 36 B1 prediction bundles exist under `artifacts/predictions/b1_moddrop/`. Bundles contain float32 logits and observation metadata. The two independently checked initial bundle hashes were:

- D1 seed 17 C0: `aca1481761ee4c3258755da5c349c25d5bcdd6fd883162c1ad53cecb200c47cd`;
- D1 seed 17 C1: `f1dcfdb167fcca5bb718c85e543a444e8711312fa2b892d53c4ab5a32f84c3b9`.

The complete 36-row prediction hash manifest was not finalized because the statistical runner stopped before its final export stage.

## 14. D1 B1 C0–C5 Results

`NOT COMPUTED AS ACCEPTED RESULTS`. Per-seed metric extraction occurred in memory, but no finalized Step 15 result table was accepted after the statistical finalization stopped.

## 15. D2 B1 C0–C5 Results

`NOT COMPUTED AS ACCEPTED RESULTS`. Per-seed metric extraction occurred in memory, but no finalized Step 15 result table was accepted after the statistical finalization stopped.

## 16. B1 Predictive Robustness

`NOT COMPUTED`. No finalized multi-seed estimates or corrected subject-bootstrap intervals were accepted.

## 17. Primary Compound B1-vs-B0 Macro-F1

`NOT COMPUTED`. D1 C4, D1 C5, D2 C4, and D2 C5 paired point estimates and 95% subject-bootstrap intervals remain open.

## 18. Known-Domain Missing-Modality Comparison

`NOT COMPUTED`. C1 and C2 paired comparisons remain open.

## 19. Full-Modality Tradeoff

`NOT COMPUTED`. C0 and C3 guardrail comparisons remain open.

## 20. Per-Stage B1-vs-B0 Analysis

`NOT COMPUTED`. No finalized C3/C4/C5 stage-recall contrasts were accepted.

## 21. Confusion Changes

Per-seed B1 confusion extraction was performed, but the required finalized `B1 - B0` comparison artifact was not accepted. Status: `NOT COMPUTED`.

## 22. Calibration B1-vs-B0

`NOT COMPUTED`. Temperature-scaled B1-vs-B0 NLL, Brier, ECE, adaptive ECE, and classwise reliability contrasts remain open.

## 23. Error-Ranking B1-vs-B0

`NOT COMPUTED`. Entropy AUROC and AUPRC paired contrasts remain open.

## 24. Selective Reliability B1-vs-B0

`NOT COMPUTED`. AURC and coverage-specific selective metrics remain open.

## 25. Conformal B1-vs-B0

`NOT COMPUTED`. Signed coverage-gap and absolute coverage-error diagnostics remain open.

## 26. Compound Failure Matrix

`NOT COMPUTED`. No compound failure matrix was finalized.

## 27. Reliability Persistence After Predictive Robustness

`NOT IDENTIFIABLE`. The required paired reliability axes were not finalized, so no persistence label is assigned.

## 28. B1 Domain × Modality Interactions

`NOT COMPUTED`. Corrected known-versus-unseen interaction contrasts remain open.

## 29. B1-vs-B0 Interaction Changes

`NOT COMPUTED`.

## 30. ISRUC Montage Sensitivity

Per-seed montage extraction was initiated, but the finalized paired montage artifact was not accepted. Status: `NOT COMPUTED`.

## 31. Multi-Seed Stability

`NOT COMPUTED AS FINAL`. The six seeds were retained exactly as preregistered; no seed was replaced or selected after evaluation.

## 32. Corrected Bootstrap Execution

The intended implementation was `src/shiftsleep_uq/step11_1_statistics.py`, with subject-level replacement, duplicate-cluster multiplicity, seed `2028`, and 2,000 replicates. The finalizer was stopped before completion because repeated ranking-statistic reconstruction was computationally excessive. No incomplete arrays were promoted to result artifacts.

## 33. Full-Modality Guardrail

`NOT COMPUTED`. The `-0.02` macro-F1 tradeoff guardrail was not evaluated in an accepted final table.

## 34. Interpretation Case

`NOT ASSIGNED`. CASE_A, CASE_B, CASE_C, CASE_D, and MIXED_CASE require completed paired results.

## 35. Scientific Interpretation

No scientific interpretation is authorized from this partial package. The verified observations are limited to frozen calibration, complete prediction-bundle generation, and exact B0/B1 observation alignment.

## 36. What B1 Explains About B0

`NOT COMPUTED`.

## 37. What B1 Does Not Explain

`NOT COMPUTED`.

## 38. Machine-Readable Result Artifacts

Verified calibration artifacts:

- `reports/b1_temperature_calibration_v1.csv`;
- `reports/b1_aps_calibration_v1.csv`;
- `reports/b1_calibration_hashes_v1.txt`;
- `artifacts/calibration/b1_moddrop/SOURCE_CALIBRATION_FROZEN.json`.

Verified inference namespace:

- `artifacts/predictions/b1_moddrop/`, exactly 36 bundles.

Not created/accepted:

- `reports/b1_primary_results_multiseed_v1.csv`;
- `reports/b1_vs_b0_paired_results_v1.csv`;
- `reports/b1_vs_b0_compound_failure_matrix_v1.csv`;
- `reports/b1_vs_b0_stage_analysis_v1.csv`;
- `reports/b1_vs_b0_confusion_analysis_v1.csv`;
- `reports/b1_isruc_montage_sensitivity_v1.csv`;
- `reports/b1_statistical_hashes_v1.txt`;
- `reports/step15_b1_evaluation_gate.json`.

## 39. Prediction Hashes

The six checkpoint hashes remained unchanged. The 36 prediction bundles were generated and aligned, but the canonical 36-row compact manifest was not finalized after the statistical-stage stop.

## 40. Calibration Hashes

The six B1 temperature and six B1 APS object hashes were recorded in `reports/b1_calibration_hashes_v1.txt`. The calibration namespace contains exactly 12 JSON objects.

## 41. Statistical Hashes

`NOT CREATED`. No incomplete statistical table was hashed or treated as authoritative.

## 42. Tests Added

`NOT COMPLETED`. No Step 15 test package was accepted because the statistical finalizer did not complete. Existing repository tests were not weakened, and no Step 16 code was implemented.

## 43. Full Validation

Not complete. Verified so far:

- runner compilation passed;
- frozen input hashes passed before execution;
- six calibration objects per type exist;
- exactly 36 prediction bundles exist;
- B0/B1 observation alignment passed for all 36 bundles;
- no retraining occurred;
- no oracle calibration occurred;
- no SHHS access occurred.

The full Step 15 validation gate remains open because the result tables and tests are incomplete.

## 44. Files Created

- `scripts/step15_b1_evaluation.py`;
- six B1 temperature artifacts;
- six B1 APS artifacts;
- calibration CSV/hash/freeze artifacts;
- 36 ignored B1 prediction bundles.

## 45. Files Modified

No frozen B0, B1 training, normalization, partition, evaluation-protocol, or checkpoint artifact was modified. The Step 15 runner is new and remains uncommitted pending repair of the statistical finalizer.

## 46. Explicitly Not Done

- no B1 retraining;
- no checkpoint reselection;
- no architecture change;
- no normalization refit;
- no target fitting;
- no oracle calibration;
- no target adaptation;
- no new reliability method;
- no lightweight calibrator;
- no changed scientific metrics;
- no accepted changed bootstrap settings;
- no SHHS;
- no Step 16;
- no push;
- no scientific conclusion from partial results.

## 47. Primary Result Freeze

`NOT FROZEN`. Calibration and prediction inputs are frozen; primary B1 and paired B0-vs-B1 statistical result hashes do not yet exist.

## 48. Remaining Scientific Questions

All Step 15 scientific questions remain open until corrected statistical finalization produces complete multi-seed and paired subject-bootstrap outputs.

## 49. Recommended Next Step

# Step 16 — Diagnose B1 Residual Failures and Reassess the Reliability-Method Authorization Gate

This recommendation is procedural only. Step 16 must not execute until Step 15 is complete; no Step 16 execution occurred here.

## 50. Git Status / Diff Summary

The worktree contains the new Step 15 runner and partial Step 15 compact artifacts. Heavy calibration/prediction objects remain outside the committed artifact set. No commit or push was made for the partial package.

## Scientific Stop Rule

Step 15 is not complete. No B1-vs-B0 scientific claim is made, no favorable seed was selected, and no downstream method was authorized.
