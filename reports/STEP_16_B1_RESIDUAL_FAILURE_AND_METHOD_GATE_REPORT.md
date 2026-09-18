# ShiftSleep-UQ Step 16 B1 Residual Failure and Reliability-Method Gate Report

## 1. Status

`STEP16_METHOD_GATE_COMPLETE`. Step 16 was executed against frozen B0 v1.2 and frozen B1 Step 15.3 artifacts. No Step 17 work was executed.

## 2. Step 16 Gate

`STEP16_METHOD_GATE_COMPLETE`.

## 3. Starting Scientific State

B0: `B0_V1_2_AUTHORITATIVE`. B1: `B1_PRIMARY_EVALUATION_COMPLETE`. Weighted engine: `WEIGHTED_RANKING_ENGINE_FROZEN`. B1 milestone tag: `step15-b1-evaluation-frozen`. Starting reliability-method gate: `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`.

## 4. Frozen B0 v1.2 Integrity

The authoritative B0 v1.2 bootstrap SHA-256 was verified as `e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1`. The v1.2 primary-results and contrast hashes remained those recorded by Step 15.3: `617fd699d0a0549abe9a032ff4cd3ae366a3c3863e8f314f17f722878bc9caa9` and `ac1f8b75fdfacf25509560c258889b1b3653e0c87cb0e2925c43f2503971343a`. No B0 artifact was modified.

## 5. Frozen B1 Step 15.3 Integrity

The B1 gate, 36 prediction-bundle hashes, frozen calibration manifests, 120 vectors × 2,000 replicates, 7,200 shards, and Step 15.3 primary CSVs were preserved. No Step 15.3 result was replaced. The original B1 milestone tag target was verified before diagnostics.

## 6. Original Step 12.1 Method-Gate Specification

The written-equivalent logical definitions are frozen in `reports/step16_original_method_gate_spec.md`. Criterion A identifies reliability degradation beyond predictive degradation across calibration, ranking/selective, and conformal evidence. Criterion B requires threshold-qualified oracle recoverability without pathological set-size inflation. Criterion C requires a source-only, target-label-free deployment design frozen before target evaluation. Criterion D asks whether reliability failure is substantially dominated by predictive/representation transfer loss that calibration cannot repair. The Step 12.1 written specification, rather than the narrower historical source-temperature-only runner rule, was used.

## 7. Why B1 Was Required

Step 12.1 found large B0 predictive/representation transfer losses in all four compound cells. Since scalar calibration cannot change argmax decisions, a calibration-only method could not be interpreted cleanly while that confound dominated. B1 was therefore the preregistered source-only modality-dropout predictive control. Step 16 reassesses residual reliability only after B1.

## 8. B1 Residual Failure Matrix

`reports/step16_residual_failure_matrix_v1.csv` contains 12 rows: three frozen seeds for each primary cell. It records B0 macro-F1, B1 macro-F1 and delta, B1 NLL, Brier, ECE, frozen Step 15.3 entropy-ranking metrics, alpha .10 coverage and absolute gap, mean set size, and the Step 15.3 residual label. Aggregate B1-vs-B0 primary deltas remain: D1 C4 `+0.03673` (CI `[+0.03141,+0.04215]`), D1 C5 `+0.18587` (`[+0.16786,+0.20296]`), D2 C4 `+0.05992` (`[+0.05308,+0.06667]`), and D2 C5 `+0.00063` (`[-0.01255,+0.01451]`).

## 9. D1 C4 Residual Diagnosis

B1 reduced the predictive confound and improved macro-F1. The Step 15.3 label was `MIXED_RELIABILITY_RESPONSE`: calibration and selective reliability improved, while the alpha .10 conformal axis remained a residual concern. Source mask-specific calibration was evaluated without target fitting; the residual was not classified as resolved by the simple control.

## 10. D1 C5 Residual Diagnosis

B1 produced a large supported macro-F1 gain and the Step 15.3 label `RELIABILITY_IMPROVES_WITH_PREDICTION`. Oracle diagnostics show target-label recoverability signals, but those are diagnostic upper bounds only. The simple source-only mask-specific control was not accepted as a universal resolution criterion.

## 11. D2 C4 Residual Diagnosis

B1 produced a supported macro-F1 gain and the Step 15.3 label `RELIABILITY_IMPROVES_WITH_PREDICTION`. Residual reliability is reduced but not eliminated across all axes. The source-only mask-specific baseline did not provide sufficient evidence for a universal reliability-method authorization.

## 12. D2 C5 Residual Diagnosis

B1 did not establish predictive improvement: the macro-F1 CI crossed zero. This cell remains `PREDICTIVE_CONFOUND_REMAINS`. It also has mixed calibration, selective, and conformal behavior. A learned reliability method cannot be authorized as if this unresolved predictive failure were calibration-only.

## 13. Predictive Residuals

Predictive residuals were assessed through macro-F1 and the frozen Step 15.3 class-decision results. D1 C4, D1 C5, and D2 C4 reduced the original predictive confound. D2 C5 remains inconclusive and therefore retains a predictive/representation residual.

## 14. Calibration Residuals

NLL, Brier, and ECE were evaluated under the frozen B1 source-global-full calibration and the separate source-mask-specific temperatures. The comparison artifact includes point estimates and paired 2,000-replicate confidence intervals. Mask-specific calibration was a diagnostic baseline, not a learned method.

## 15. Ranking / Selective Residuals

ERROR_AUROC, ERROR_AUPRC, and entropy AURC remain the uncalibrated frozen Step 15.3 axes. They were not redefined using mask-specific calibration. Their canonical values remain in the Step 15.3 paired results and are copied into the Step 16 residual matrix for diagnosis.

## 16. Conformal Residuals

Mask-specific APS was fit separately on source calibration subjects for each direction, seed, and mask. Alpha values remained .10 and .05. No alpha was changed after observing results. Target oracle APS was isolated to diagnostic-only artifacts in the Step 16 oracle table.

## 17. Source Mask-Specific Calibration Protocol

For each direction × seed, exactly three masks were processed: FULL `[1,1]`, EEG-only `[1,0]`, and EOG-only `[0,1]`. The source-control phase used only SOURCE CALIBRATION subjects. Existing B1 full-modality source calibration remained unchanged and served as the comparison control.

## 18. Source Mask-Specific Temperature Results

`reports/step16_source_mask_temperature_v1.csv` contains exactly 18 `SOURCE_MASK_SPECIFIC_T` fits. Each fit used the frozen checkpoint, frozen normalization, SOURCE CALIBRATION data only, `T=exp(log_T)`, and the existing LBFGS settings. The corresponding JSON objects are under `artifacts/calibration/step16_source_mask/`.

## 19. Source Mask-Specific APS Results

`reports/step16_source_mask_aps_v1.csv` contains exactly 18 mask-specific APS objects, each with alpha .10 and .05 q-hats. APS scores and q-hats were fit only from SOURCE CALIBRATION subjects. The objects are separate from the frozen B1 APS objects.

## 20. Simple-Control Effect on D1 C4

The source-mask comparison artifact records NLL, Brier, ECE, and alpha .10 absolute-gap deltas with paired intervals. D1 C4 remains `PERSISTS_AFTER_SIMPLE_SOURCE_CALIBRATION`: improvement on selected calibration axes does not establish resolution of the mixed residual pattern or the conformal axis.

## 21. Simple-Control Effect on D1 C5

D1 C5 shows source-mask diagnostic changes, but the simple baseline was not treated as a universal reliability repair. The residual classification remains `PERSISTS_AFTER_SIMPLE_SOURCE_CALIBRATION` under the preregistered multi-axis rule because resolution cannot be claimed from one favorable family while ranking/conformal and deployment-generalization evidence remain heterogeneous.

## 22. Simple-Control Effect on D2 C4

D2 C4 remains `PERSISTS_AFTER_SIMPLE_SOURCE_CALIBRATION`. Source-only mask calibration is a useful control, but it does not remove all reliability differences relative to matched known-domain missing-modality behavior.

## 23. Simple-Control Effect on D2 C5

D2 C5 remains `PERSISTS_AFTER_SIMPLE_SOURCE_CALIBRATION`. The unresolved predictive confound makes a calibration-only resolution claim inappropriate, regardless of target-oracle diagnostic gains.

## 24. Simple-Control Sufficiency Assessment

`SIMPLE_SOURCE_CALIBRATION_SUFFICIENT` was not supported. The baseline did not uniformly resolve the primary residual pattern across the four cells and all required reliability families. It also cannot repair macro-F1.

## 25. B1 Oracle Diagnostic Protocol

After source-mask artifacts were frozen, target oracle diagnostics reused the frozen Step 12.1 oracle partition. For each direction × seed × C3/C4/C5, the target calibration-role subjects were used to fit a diagnostic scalar temperature and APS; disjoint target evaluation-role subjects were then evaluated. This phase was marked `DIAGNOSTIC_ORACLE_ONLY`.

## 26. B1 Oracle Calibration Results

`reports/step16_b1_oracle_diagnostics_v1.csv` contains target-oracle NLL, Brier, and ECE comparisons against source-mask-specific deployment on the same oracle evaluation partitions. Target-label oracle improvements are present in multiple cells, but they are upper-bound evidence and not deployable calibration results.

## 27. B1 Oracle Conformal Results

The same oracle artifact contains alpha .10 absolute coverage gap and mean set-size comparisons. Oracle conformal results are diagnostic only and remain partition-isolated. They do not authorize target fitting or replace source-only deployment evidence.

## 28. Recoverability Matrix

`reports/step16_method_authorization_matrix_v1.csv` records all four primary cells as having diagnostic target-label recoverability signals, while retaining the status `RECOVERABLE_WITH_TARGET_LABELS_DIAGNOSTIC_ONLY`. It records `PREDICTIVE_CONFOUND_REDUCED` for D1 C4, D1 C5, and D2 C4, and `PREDICTIVE_CONFOUND_REMAINS` for D2 C5.

## 29. Criterion A Reassessment

Criterion A remains supported as a residual-reliability diagnosis: B1 does not erase all calibration, ranking/selective, or conformal heterogeneity. The Step 16 source-control results do not justify collapsing all residuals into a single resolved category.

## 30. Criterion B Reassessment

Criterion B has diagnostic support through target-oracle improvements on frozen disjoint partitions. This is recoverability with target labels, not source-only deployability, and is insufficient by itself for method authorization.

## 31. Criterion C Reassessment

Criterion C passes as a design constraint. The source mask-specific control was fit only from SOURCE CALIBRATION and was frozen before evaluating the frozen source-test/target bundles. No target labels were used in the source-control phase.

## 32. Criterion D Reassessment

Criterion D is mixed by cell. B1 materially reduced predictive confounding in three cells, but D2 C5 did not establish a predictive gain and remains predictive-confounded. Because scalar calibration cannot alter argmax predictions, the residual evidence does not support treating the full problem as reliability-only.

## 33. Predictive-Confound Status by Cell

- D1 C4: `PREDICTIVE_CONFOUND_REDUCED`.
- D1 C5: `PREDICTIVE_CONFOUND_REDUCED`.
- D2 C4: `PREDICTIVE_CONFOUND_REDUCED`.
- D2 C5: `PREDICTIVE_CONFOUND_REMAINS`.

## 34. Method Authorization Matrix

The four-cell matrix records `RELIABILITY_METHOD_NOT_AUTHORIZED`. A learned method was not authorized merely because oracle calibration improved or because a future method could be made source-only. The residual evidence is heterogeneous and includes an unresolved predictive cell.

## 35. Final Reliability-Method Gate

`RELIABILITY_METHOD_NOT_AUTHORIZED`.

## 36. Scientific Rationale

The authorization requirements were not jointly satisfied. B1 reduced the predictive confound in three cells, but D2 C5 remains inconclusive. Source-only mask-specific scalar temperature and APS did not establish uniform residual resolution. Oracle gains demonstrate target-label recoverability in diagnostic conditions, not deployability. The evidence therefore supports stopping rather than adding a learned reliability architecture.

## 37. What B1 Solved

B1 demonstrated supported predictive robustness gains in D1 C4, D1 C5, and D2 C4, with no practically notable full-modality C3 tradeoff. It made calibration-specific diagnosis scientifically more interpretable in those cells.

## 38. What B1 Did Not Solve

B1 did not establish a universal predictive gain, did not remove direction/modality heterogeneity, and did not uniformly repair calibration, selective, or conformal reliability. D2 C5 remains predictive-confounded.

## 39. What Simple Source Calibration Solved

It provided a valid source-only mask-matched baseline and quantified the effect of replacing the full-modality calibration object with mask-specific objects. It demonstrated that some probability/conformal changes can be isolated without changing logits or argmax predictions.

## 40. What Simple Source Calibration Did Not Solve

It did not establish a uniform resolution of the four-cell residual matrix, did not repair macro-F1, did not change the frozen uncalibrated ranking axes, and did not justify a learned modality-conditioned calibrator.

## 41. What Oracle Diagnostics Establish

With frozen disjoint oracle partitions, target-label fitting can improve selected calibration and conformal quantities. This establishes diagnostic recoverability for portions of the residual behavior under an oracle upper bound.

## 42. What Oracle Diagnostics Do NOT Establish

Oracle diagnostics do not establish source-only deployment, do not authorize target adaptation, do not repair argmax classification errors, and do not constitute evidence that a learned method will generalize without target labels.

## 43. Implications for ShiftSleep-UQ Contribution

The evidence supports a controlled conclusion: source-only modality-dropout training is a useful predictive robustness control, while reliability behavior remains heterogeneous and cannot be converted into a universal reliability-method claim. The benchmark should preserve this separation between predictive robustness, source-only calibration, and target-oracle diagnostics.

## 44. Canonical Step 16 Artifacts

- `reports/step16_original_method_gate_spec.md`
- `reports/step16_residual_failure_matrix_v1.csv`
- `reports/step16_source_mask_temperature_v1.csv`
- `reports/step16_source_mask_aps_v1.csv`
- `reports/step16_source_mask_calibration_comparison_v1.csv`
- `reports/step16_b1_oracle_diagnostics_v1.csv`
- `reports/step16_original_gate_reassessment_v1.csv`
- `reports/step16_method_authorization_matrix_v1.csv`
- `reports/step16_method_gate.json`
- `reports/step16_data_access_audit.csv`
- `reports/step16_statistical_hashes_v1.txt`

## 45. Statistical Hash Manifest

The final hash manifest records the Step 16 diagnostic CSVs, gate metadata, original specification, data-access audit, and this report. Hashes are generated only after all Step 16 artifacts are finalized.

## 46. Tests Added

`tests/test_step16_residual_method_gate.py` verifies frozen B0/B1 gates and hashes, 18 source temperatures, 18 source APS objects, source-calibration-only metadata, argmax invariance, mask-condition mapping, oracle namespace isolation, oracle partition disjointness, gate determinism, absence of learned-method artifacts, and absence of SHHS.

## 47. Full Validation

Validation requires: Step 16 script execution completed with `STEP16_METHOD_GATE_COMPLETE`; source mask temperatures `18`; source mask APS objects `18`; oracle rows `60`; residual matrix rows `12`; source-control comparison rows `24`; frozen B0/B1 gate checks passed; source/oracle phase firewall checks passed; full pytest, compileall, and `git diff --check` passed; no raw data, checkpoints, prediction bundles, oracle-heavy binaries, or secrets added to Git.

## 48. Files Created

The canonical Step 16 reports listed in Section 44, `scripts/step16_residual_method_gate.py`, `scripts/step16_finalize.py`, and `tests/test_step16_residual_method_gate.py` were created. Source-control JSON artifacts were created below `artifacts/calibration/step16_source_mask/`; these are lightweight calibration objects and not prediction bundles or checkpoints.

## 49. Files Modified

No Step 15.3 primary artifact, B0 v1.1/v1.2 artifact, checkpoint, prediction bundle, partition, or protocol artifact was modified. Step 16 generated its own namespace and diagnostic reports.

## 50. Explicitly Not Done

- no B1 retraining;
- no checkpoint selection;
- no new architecture;
- no learned reliability method;
- no target-trained deployment method;
- no protocol change;
- no B0 modification;
- no Step 15.3 modification;
- no SHHS;
- no Step 17.

## 51. Remaining Scientific Questions

The remaining question is whether a future preregistered benchmark-only synthesis should retain mask-specific source calibration as a baseline. No learned reliability method is authorized by this Step 16 gate.

## 52. Recommended Next Step

`# Step 17 — Freeze the Benchmark-Only Scientific Conclusion and Begin Final Analysis/Figure Synthesis`.

This is a recommendation only. Step 17 was not executed.

## 53. Git Commit

Scientific milestone commit: `e9d4cc8f59d4f791dad45c2fed3df8a5ffb67225` — `research: freeze B1 residual diagnosis and method gate`. The commit contains the validated Step 16 diagnostic package.

## 54. Milestone Tag

Annotated tag: `step16-method-gate-frozen`, targeting validated scientific commit `e9d4cc8f59d4f791dad45c2fed3df8a5ffb67225`, with annotation `ShiftSleep-UQ residual reliability diagnosis and method authorization gate frozen`. The tag was created only after validation and is not moved.

## 55. GitHub Push Status

`PUSH_COMPLETE`. Remote `origin` received `main` and `step16-method-gate-frozen` without force push or history rewrite.

## 56. Git Status / Diff Summary

Scientific commit and annotated tag were pushed successfully; the follow-up documentation-only commit records the final report text without changing the scientific tag target. Remote read-back verified the branch and tag targets. Heavy shards remain ignored and untracked; no checkpoints, prediction bundles, raw data, or secrets are included.
