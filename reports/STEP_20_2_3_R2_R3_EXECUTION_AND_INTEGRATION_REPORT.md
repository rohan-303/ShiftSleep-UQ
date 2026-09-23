# STEP 20.2.3 — R2/R3 Execution and Integration Report

## 1. Status

Step 20.2.3 was executed as far as the available implementation and hardware permitted. R1 preservation and R2 confirmatory execution completed. R3 remained preflight-only because the executor's scientific loop was not implemented; invoking `--execute` failed closed by design. No R3 results were inferred.

## 2. Final Remediation Gate

`FULL_REMEDIATION_PARTIAL`

## 3. Starting State

Repository: `C:\Users\rohan\ShiftSleep-UQ`; branch `main`. Step 20.2.2 was at `FULL_REMEDIATION_PARTIAL`, with R1 complete, Sleep-EDF repair complete, and R2/R3 training previously blocked.

## 4. Protocol Integrity

The v2 protocol hash was verified as `c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`. The v1 hash remained `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`. No protocol file was modified.

## 5. Step 20.2.2 Preservation

The Step 20.2.2 outputs were preserved in checkpoint commit `7300c0d`, pushed to `origin/main`. Historical checkpoints, processed NPZ files, prediction bundles, calibration artifacts, figures, manuscript files, and reports were not overwritten.

## Execution Infrastructure

## 6. Remediation Data Overlay

The remediation overlay resolves Sleep-EDF recordings to `artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2/` while preserving signals and labels. ISRUC uses its existing valid indices. Audit: 252/252 PASS, comprising 153 Sleep-EDF and 99 ISRUC recordings. The R2 window manifest contains 252 rows.

## 7. Runner Architecture

R2 uses one reusable executor, `scripts/run_r2_window_sensitivity.py`, with frozen protocol gating, matched initialization, source-only normalization, AdamW training, checkpoint selection, and remediation namespaces. R3 infrastructure is in `scripts/run_r3_seqsleepnet.py` and implements preflight contracts, STFT checks, physical-contiguity checks, source-only normalization scaffolding, matched initialization, exposure determinism, and attempt allocation.

## 8. Attempt/Resume System

R2 attempts use `artifacts/remediation/r2/<job>/ATTEMPT_001/`, with protocol, configuration, checkpoint, normalization, history, and completion metadata. Completed R2 jobs were recorded and are restart-detectable. R3 attempt allocation is collision-failing, but no R3 scientific attempt was promoted.

## R2

## 9. Windowed Dataset

The frozen first-valid-non-Wake through last-valid-non-Wake rule with 60 physical epochs of context on each side was applied before validity filtering. No-no-sleep recordings were excluded according to protocol. Dataset manifest: `reports/remediation/r2_windowed_dataset_manifest_v1.csv`.

## 10. Class Priors Before/After

Sleep-EDF BEFORE proportions were Wake 0.687855, N1 0.051865, N2 0.166599, N3 0.031422, REM 0.062259. Sleep-EDF AFTER proportions were Wake 0.337348, N1 0.110104, N2 0.353672, N3 0.066706, REM 0.132169; JS divergence 0.0627962. ISRUC BEFORE proportions were Wake 0.228689, N1 0.128632, N2 0.315702, N3 0.193508, REM 0.133469. ISRUC AFTER proportions were Wake 0.209336, N1 0.131860, N2 0.323623, N3 0.198363, REM 0.136818; JS divergence 0.000273781. Full artifact: `r2_class_prior_before_after_v1.csv`.

## 11. Subject/Partition Integrity

The executor retained frozen source roles and did not use target data for training, normalization, or checkpoint selection. Target access was restricted to post-training evaluation.

## 12. R2 Training Environment

R2 used the RTX 3060 Laptop GPU, FP32, batch size 128, AdamW, learning rate 3e-4, weight decay 1e-4, gradient clipping 1.0, no scheduler, maximum 30 epochs, minimum 5 epochs, and patience 6. All 12 jobs completed without technical retry.

## 13. B0-W Runs

Six B0-W jobs completed across both directions and seeds 17, 42, and 2026. All produced finite checkpoints and valid completion metadata.

## 14. B1-W Runs

Six B1-W jobs completed across both directions and seeds 17, 42, and 2026. Matched initialization hashes were recorded per direction and seed.

## 15. R2 Checkpoints

`reports/remediation/r2_checkpoint_manifest_v1.csv` contains 12/12 accepted rows and zero failures. Checkpoint, normalization, initialization, and protocol hashes are recorded for every job.

## 16. R2 Calibration

Source-CAL temperature and APS quantities were computed for the six direction/seed calibration groups and applied only as remediation diagnostics. Calibration ledger: `r2_calibration_v1.csv`.

## 17. R2 Evaluation

All 72 expected prediction bundles were generated: 2 directions × 2 variants × 3 seeds × 6 conditions. Primary metrics are in `r2_primary_results_v1.csv`.

## 18. R2 Bootstrap

Subject-cluster bootstrap used 2,000 duplicate-preserving replicates and seed 2028. Optimized confusion-matrix aggregation was used to preserve the macro-F1 definition while making the required bootstrap feasible. Summary: `r2_bootstrap_summary_v1.csv`.

## 19. R2 Holm

The four-cell R2 family used the frozen two-sided null-centered bootstrap p-value and step-down Holm correction. Results: `r2_holm_v1.csv`.

## 20. R2 Outcome

`WINDOW_PARTIALLY_ROBUST`. Three of four primary effects were positive and Holm-rejected; D2/C5 was small and its confidence interval crossed zero.

## R3

## 21. Sequence Dataset

R3 preflight infrastructure validates physical contiguous sequences, recording/subject boundaries, and gap termination. No R3 sequence training dataset was promoted to scientific execution.

## 22. Sequence Coverage

The R3 preflight reported the 12-job grid and validated the sequence/STFT contract in synthetic tests. Scientific sequence coverage and prediction counts were not produced.

## 23. R3 Training Environment

The frozen SeqSleepNet-class parameter count was verified as 117,062. The scientific training loop remains unavailable in the executor.

## 24. S0 Runs

Not executed. No S0 checkpoints or scientific results exist.

## 25. S1 Runs

Not executed. No S1 checkpoints or scientific results exist.

## 26. R3 Checkpoints

No accepted R3 checkpoint rows exist. R3 checkpoint manifest is therefore not complete.

## 27. R3 Calibration

Not executed.

## 28. R3 Evaluation

Not executed.

## 29. R3 Bootstrap

Not executed.

## 30. R3 Holm

Not executed.

## 31. R3 Outcome

`BACKBONE_RESULT_INCONCLUSIVE`. The explicit `--execute` invocation failed closed with `R3 training loop is intentionally gated; wire only after the bounded executor review`. This is an implementation blocker, not a negative scientific result.

## Integration

## 32. Historical vs R2 vs R3

R1 is complete and materially changes the historical conformal interpretation. R2 is complete for the 12 training jobs and 72 bundles. R3 has no scientific evidence. Integrated effect matrix: `remediation_primary_effect_summary_v2.csv`.

## 33. Four Primary Effects

R2 B1-W minus B0-W effects: D1/C4 = 0.0597081, 95% CI [0.0544329, 0.0651028]; D1/C5 = 0.0384471, CI [0.0265461, 0.0501430]; D2/C4 = 0.0247234, CI [0.0155260, 0.0340124]; D2/C5 = 0.00430461, CI [-0.00952072, 0.0183550]. R3 effects are not computed.

## 34. Seed-Level Stability

R2 seed effects are stored in `r2_seed_results_v1.csv`. D1/C5 shows the greatest seed spread, including one negative seed effect; D2/C5 is consistently small but mixed. R3 seed stability is unavailable.

## 35. Calibration Comparison

Source-CAL calibration artifacts were generated for R2. A complete calibrated reliability comparison was not generated; no composite reliability score was created.

## 36. Selective Prediction Comparison

Not computed in this partial step. No selective-prediction claim is made.

## 37. Conformal Reinterpretation

R1 remains `R1_MATERIALLY_CHANGES_CONFORMAL_FINDING`. R2 convenience or positive predictive effects do not restore the historical conformal-transfer claim.

## 38. Integrated Conclusion Matrix

`remediation_conclusion_matrix_v2.csv` records modality-dropout predictive effect as SUPPORTED, recording-window robustness as PARTIALLY_SUPPORTED, backbone generalization as INCONCLUSIVE, calibration as INCONCLUSIVE, selective prediction as INCONCLUSIVE, and conformal transfer as NOT_SUPPORTED.

## 39. Manuscript Impact

`ORIGINAL_CONCLUSION_MATERIALLY_REVISED`.

## 40. JBHI Story Classification

`JBHI_STORY_REQUIRES_MAJOR_REFRAMING`.

## 41. Manuscript Revision Plan

`reports/remediation/postremediation_manuscript_revision_plan_v2.md` was created. The canonical manuscript and JBHI submission package were not edited.

## Validation

## 42. Target Firewall

R2 training, normalization, and checkpoint selection used source data only. Target data were accessed only during post-training evaluation. R3 was not executed.

## 43. Historical Integrity

Historical NPZ files, historical checkpoints, historical predictions, calibration artifacts, original Figure 2, and manuscript packages were preserved. New outputs are under remediation namespaces or remediation reports.

## 44. Tests

R3 focused tests: 4 passed. Earlier repository suite: 161 passed. Protocol preflight reported 12 R3 jobs, target access forbidden, and exact v2 hash. Compileall and diff checks were run during executor development.

## 45. Full Validation

R1 reconstruction remains 24/24 provenance-equivalent with exact historical qhat reproduction and Sleep-EDF repair remains 153/153 PASS. R2 is 12/12 complete with 72/72 prediction bundles. R3 completeness, R3 statistics, and full integrated reliability acceptance are not satisfied.

## 46. Runtime / Retries

R2 required long local GPU execution but completed all 12 jobs without technical retry. Several stale evaluator launches failed before code corrections; they produced no scientific outputs. The corrected evaluator completed successfully. R3 was not retried because its executor explicitly fails closed before scientific execution.

## 47. Files Created

Key files include `src/shiftsleep_uq/remediation/datasets.py`, `scripts/run_r2_window_sensitivity.py`, `scripts/run_r3_seqsleepnet.py`, `scripts/evaluate_r2_remediation.py`, `scripts/finalize_r2_statistics.py`, `scripts/finalize_r2_r3_integration.py`, `reports/remediation/remediation_data_overlay_audit_v1.csv`, R2 manifests/results/statistics, integration matrices, and `postremediation_manuscript_revision_plan_v2.md`.

## 48. Files Modified

The remediation overlay and new remediation scripts/reports were modified. No historical scientific artifact or canonical manuscript was modified. Existing unrelated untracked Step 18 files remain outside this checkpoint scope.

## 49. Explicitly Not Done

R3 scientific training, R3 evaluation, R3 calibration, R3 bootstrap, R3 Holm correction, complete R3 prediction bundles, selective-prediction analysis, full reliability matrix, manuscript reconstruction, Step 20.3, and Step 21 were not done.

## 50. Remaining Scientific Risks

R3 may change the integrated generalization conclusion. R2 C5/D2 is inconclusive, and seed variation is material in D1/C5. Calibration and selective-prediction conclusions remain incomplete. The R1 conformal revision is already decisive against unqualified historical transfer claims.

## 51. Recommended Next Step

Complete and review the bounded R3 executor, then run the frozen 12-job R3 program and integrate its results. Do not execute Step 20.3 until R3 and the remaining reliability/statistical gates are complete.

## 52. Git Commit

The authorized preservation checkpoint exists as `7300c0d`. No Step 20.2.3 final-results commit was created because the final gate is partial.

## 53. Git Tag

`step20-2-remediation-results-frozen` was not created.

## 54. GitHub Push

The preservation checkpoint was pushed. No Step 20.2.3 final-results push was performed.

## 55. Git Status

The repository remains on `main`. New Step 20.2.3 remediation scripts and reports are uncommitted. No force push or historical-artifact mutation occurred.
