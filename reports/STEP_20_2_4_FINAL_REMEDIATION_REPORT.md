# ShiftSleep-UQ Step 20.2.4 Final Remediation Report

## 1. Status

Step 20.2.4 preserved the completed R1/R2 science, corrected class-prior reporting, completed the R2 reliability metric generation, and implemented/attempted the R3 scientific executor. R3 did not complete: the first three isolated attempts did not produce an accepted checkpoint manifest. The third attempt was stopped after prolonged first-job execution with measured host memory pressure reaching 96.7% and low GPU utilization. No R3 scientific result is reported.

## 2. Final Remediation Gate

`FULL_REMEDIATION_PARTIAL`

## 3. Starting State

HEAD and `origin/main` were both `7300c0d6e5af59a4d681fd40343ade9e743627c4` before the Step 20.2.4 checkpoint. The worktree contained the uncommitted Step 20.2.3 R1/R2 outputs and R3 preflight infrastructure.

## 4. Protocol Integrity

Protocol v1 hash: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`.

Protocol v2 hash: `c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`.

The v2 validator returned `valid: true`. No protocol amendment was made.

## 5. R1/R2 Preservation Checkpoint

Checkpoint commit created and pushed:

`e8fddae research: preserve randomized APS and harmonized-window remediation results`

The commit contains lightweight R1/R2 reports, manifests, code, tests, and statistical tables. Heavy checkpoints, prediction bundles, bootstrap shards, raw data, and transformed data remain outside Git.

## Class-Prior Correction

## 6. Cross-Dataset Prior Divergence Before

Using exact stage counts and natural-log Jensen-Shannon divergence:

`JS_BEFORE = 0.11943661377861878`

The distributions compare original Sleep-EDF with original ISRUC proportions over Wake, N1, N2, N3, and REM.

## 7. Cross-Dataset Prior Divergence After

Using the harmonized-window retained counts:

`JS_AFTER = 0.025504007696203264`

Absolute reduction: `0.09393260608241552`.

Relative reduction: `0.7864640758865108`, or 78.6464%.

Artifact: `reports/remediation/r2_cross_dataset_class_prior_divergence_v1.csv`.

Within-dataset before/after divergences remain separately recorded in `r2_class_prior_before_after_v1.csv`:

- Sleep-EDF internal JS: `0.06279623913213969`.
- ISRUC internal JS: `0.0002737809042398639`.

## 8. Prior-Shift Interpretation

Harmonization substantially reduced the cross-dataset class-prior mismatch descriptively. This is a distributional observation, not a causal claim and not evidence that harmonization alone caused the R2 predictive effects.

## R2 Reliability Completion

## 9. R2 Calibration

All 12 direction × variant × seed source-CAL temperature groups were generated. Each group records temperature, NLL before and after calibration, calibration count, and checkpoint hash.

Artifact: `r2_temperature_calibration_v1.csv`.

The 72 prediction bundles were reused without retraining or replacement.

## 10. R2 Error Ranking

The complete R2 reliability metric table includes uncalibrated predictive-entropy ERROR_AUROC and ERROR_AUPRC for all 72 bundles. The metric generation uses the frozen evaluator definitions. Full subject-bootstrap paired intervals for every ranking metric were not completed.

Artifact: `r2_reliability_results_v1.csv`.

## 11. R2 Selective Prediction

AURC and fixed-coverage risk/selective-macro-F1 diagnostics were generated for all 72 bundles using uncalibrated predictive entropy. These are descriptive outputs in this step; the paired reliability bootstrap package remains incomplete.

## 12. R2 Randomized APS

Source-CAL APS q-hats were generated separately for the 12 R2 direction/variant/seed groups. Secondary APS coverage, signed/absolute nominal deviations, set sizes, singleton fractions, empty fractions, and related metrics are present in the reliability result table.

## 13. R2 Reliability Effects

`r2_reliability_paired_v1.csv` contains 32 descriptive B1-W minus B0-W reliability rows for the four primary cells across NLL, ERROR_AUROC, ERROR_AUPRC, AURC, and APS diagnostics. Non-additive reliability bootstrap intervals were not completed and are explicitly labeled `NOT_COMPUTED_FOR_THIS_METRIC`.

No composite reliability score was created.

## 14. R2 Final Interpretation

R2 remains `WINDOW_PARTIALLY_ROBUST`. D1/C4, D1/C5, and D2/C4 have positive Holm-supported macro-F1 effects. D2/C5 is inconclusive, with a 95% interval crossing zero.

## R3 Executor

## 15. R3 Executor Implementation

A scientific executor was added at `scripts/run_r3_scientific.py`. It implements:

- protocol hash gating;
- original benchmark composition;
- repaired Sleep-EDF temporal-index overlay;
- contiguous physical sequence construction;
- vectorized STFT generation;
- source-TRAIN frequency-bin normalization;
- matched S0/S1 initialization;
- deterministic exposure masking;
- sequence training configuration;
- DEV checkpoint selection;
- immutable attempt namespaces;
- checkpoint and run manifests.

The earlier preflight executor remains at `scripts/run_r3_seqsleepnet.py`.

## 16. R3 Executor Tests

The existing focused R3 tests passed: 4 tests. The SeqSleepNet parameter count was verified as 117,062.

## 17. R3 Dataset/Sequence Coverage

R3 execution did not reach an accepted coverage manifest. Three attempt namespaces were created for the first D1/S0/seed17 job across the interrupted runs. No accepted R3 checkpoint manifest exists.

## 18. R3 Normalization

The executor fit source-TRAIN per-modality/frequency-bin normalization artifacts under the R3 remediation namespace. These are technical execution artifacts only; no R3 scientific result was accepted.

## 19. R3 Training Environment

The local device was an NVIDIA GeForce RTX 3060 Laptop GPU with 6 GiB VRAM. During the third attempt, host memory utilization reached 96.7% while GPU utilization remained approximately 22%, indicating a severe CPU-memory/data-materialization bottleneck. The attempt was stopped to avoid uncontrolled resource exhaustion.

## 20. S0 Training

Not completed. No accepted S0 checkpoint or scientific result exists.

## 21. S1 Training

Not executed. No accepted S1 checkpoint or scientific result exists.

## 22. R3 Checkpoint Selection

No accepted R3 checkpoint selection rows exist. The partial checkpoint created during an earlier interrupted attempt was not promoted or reused.

## 23. R3 Prediction Completeness

Zero accepted R3 prediction bundles. The required 72/72 completeness gate failed.

## 24. R3 Calibration

Not computed.

## 25. R3 Error Ranking

Not computed.

## 26. R3 Selective Prediction

Not computed.

## 27. R3 Randomized APS

Not computed.

## 28. R3 Bootstrap

Not computed.

## 29. R3 Holm

Not computed.

## 30. R3 Final Outcome

`BACKBONE_RESULT_INCONCLUSIVE`

This is an execution/resource blocker, not evidence for or against strong-backbone generalization.

## Integration

## 31. Historical vs R2 vs R3

R1 is complete and materially changes the conformal interpretation. R2 is complete for predictive training, prediction bundles, bootstrap macro-F1 effects, and Holm testing. R3 has no accepted scientific result.

## 32. Four Primary Predictive Effects

R2 B1-W minus B0-W:

- D1/C4: `0.059708122154225995`; 95% CI `[0.054432928690153516, 0.06510282347956471]`; Holm p `0.001999000499750125`.
- D1/C5: `0.03844705104012917`; 95% CI `[0.026546135324031026, 0.05014303287836442]`; Holm p `0.001999000499750125`.
- D2/C4: `0.024723406815649922`; 95% CI `[0.01552602451246182, 0.034012401219026094]`; Holm p `0.001999000499750125`.
- D2/C5: `0.004304605650325828`; 95% CI `[-0.009520719118135042, 0.018355018519060958]`; Holm p `0.5602198900549725`.

R3 effects and confidence intervals: `NOT COMPUTED`.

## 33. Seed-Level Stability

R2 seed effects are preserved in `r2_seed_results_v1.csv`. D1/C5 has the largest seed spread and includes one negative seed effect. D2/C5 remains small and mixed. R3 seed stability is unavailable.

## 34. Reliability Matrix

`remediation_reliability_summary_final.csv` distinguishes R2 measured descriptive metrics from incomplete paired-bootstrap inference and marks all R3 reliability fields `NOT_COMPUTED`.

The final reliability interpretation is `PARTIALLY_SUPPORTED`: R2 reliability metrics were generated broadly, but the requested complete paired uncertainty package was not completed; R3 reliability is unavailable.

## 35. Conformal Final Position

The historical non-randomized APS headline is superseded for interpretation by the R1 randomized-APS sensitivity finding. Historical APS can remain reported as a prespecified historical analysis, but conformal transfer must not be described as robust.

## 36. Integrated Conclusion Matrix

The final matrix records:

- Modality-exposure predictive effect: `SUPPORTED`.
- Sleep-window robustness: `PARTIALLY_SUPPORTED`.
- Strong-backbone generalization: `INCONCLUSIVE`.
- Probability calibration: `PARTIALLY_SUPPORTED`.
- Error ranking: `PARTIALLY_SUPPORTED`.
- Selective prediction: `PARTIALLY_SUPPORTED`.
- Conformal transfer: `NOT_SUPPORTED`.

Artifact: `remediation_conclusion_matrix_final.csv`.

## 37. Manuscript Impact

`ORIGINAL_CONCLUSION_MATERIALLY_REVISED`

## 38. JBHI Story Classification

`JBHI_STORY_REQUIRES_MAJOR_REFRAMING`

## 39. Final Scientific Claims

Saved to `reports/remediation/final_scientific_claims_v1.md`.

Supported claims are limited to provenance-equivalent R1 reconstruction, the R1 conformal reinterpretation, Sleep-EDF ledger repair, and the completed R2 predictive findings.

Strong-backbone generalization remains unresolved. No causal claim is made for the R2 improvements.

## 40. Manuscript Revision Plan

Saved to `reports/remediation/postremediation_manuscript_revision_plan_final.md`.

The plan includes R1, corrected Figure 2, R2, cross-dataset prior reduction, the unresolved R3 branch, R2 reliability caveats, Ovadia/Tibshirani references, bibliography correction, workflow-jargon removal, precision reduction, and Table 4 redesign.

## Validation

## 41. Target Firewall

R2 training, normalization, checkpoint selection, and calibration used source data only. Target data were accessed only for post-training evaluation. R3 did not reach scientific evaluation.

## 42. Historical Integrity

Historical processed files, checkpoints, prediction bundles, calibration objects, original Figure 2, and manuscript packages were preserved. All new outputs use remediation namespaces.

## 43. Tests

- Protocol validator: `valid: true`.
- Protocol v1/v2 hashes: PASS.
- R3 focused tests: 4 passed.
- R2 jobs: 12/12 complete.
- R2 bundles: 72/72.
- Compileall and `git diff --check`: passed before the final reporting edits.

## 44. Full Validation

The full final gate failed because:

- R3 jobs were not completed;
- R3 prediction bundles were not generated;
- R3 calibration/statistics/Holm outputs are absent;
- complete paired R2 reliability bootstrap outputs are absent.

No values were fabricated to fill those gaps.

## 45. Runtime / Retry Summary

R2 completed all 12 jobs without technical retry.

R2 reliability generation initially failed on a CSV schema union and was corrected and rerun successfully, producing 12 calibration groups and 7,488 metric rows.

R3 attempt 001 produced partial, invalidated execution evidence. Attempts 002 and 003 did not produce accepted scientific completion. Attempt 003 was stopped after measured host memory pressure reached 96.7% with low GPU utilization. No partial R3 checkpoint was reused.

## 46. Files Created

Key Step 20.2.4 files:

- `scripts/compute_cross_dataset_prior_divergence.py`
- `scripts/complete_r2_reliability.py`
- `scripts/finalize_r2_reliability_paired.py`
- `scripts/run_r3_scientific.py`
- `scripts/evaluate_r3_scientific.py`
- `scripts/finalize_step20_2_4_integration.py`
- `reports/remediation/r2_cross_dataset_class_prior_divergence_v1.csv`
- `reports/remediation/r2_temperature_calibration_v1.csv`
- `reports/remediation/r2_reliability_results_v1.csv`
- `reports/remediation/r2_reliability_paired_v1.csv`
- `reports/remediation/remediation_primary_effect_summary_final.csv`
- `reports/remediation/remediation_reliability_summary_final.csv`
- `reports/remediation/remediation_conclusion_matrix_final.csv`
- `reports/remediation/final_scientific_claims_v1.md`
- `reports/remediation/postremediation_manuscript_revision_plan_final.md`
- this report.

## 47. Files Modified

The Step 20.2.4 remediation scripts, reports, and class-prior output were modified. Historical artifacts and the canonical manuscript were not modified.

## 48. Explicitly Not Done

- R3 accepted training completion;
- R3 12-job scientific matrix;
- R3 72 prediction bundles;
- R3 calibration;
- R3 reliability metrics;
- R3 bootstrap and Holm analysis;
- complete paired R2 reliability bootstrap intervals for every requested metric;
- manuscript editing;
- Step 20.3;
- Step 21.

## 49. Remaining Scientific Risks

R3 may change the integrated backbone-generalization conclusion. R2 D2/C5 remains inconclusive. R2 reliability inference is incomplete for non-additive paired metrics. The R1 conformal revision remains decisive against an unqualified historical conformal-transfer claim.

## 50. Recommended Next Step

Do not execute Step 20.3. First repair the R3 executor's memory behavior using a disk-backed/vectorized spectrogram cache or an explicitly authorized hardware path, then rerun the frozen R3 matrix from fresh attempts and complete the remaining reliability bootstrap package.

## 51. Git Commit

Preservation checkpoint:

`e8fddae research: preserve randomized APS and harmonized-window remediation results`

No Step 20.2.4 final-results commit was created because the gate is partial.

## 52. Git Tag

`step20-2-remediation-results-frozen` was not created.

## 53. GitHub Push

The Step 20.2.3 preservation checkpoint was pushed to `origin/main`. No Step 20.2.4 final-results push or tag push was performed.

## 54. Git Status

The repository remains on `main`. Step 20.2.4 code and reports are uncommitted. Existing unrelated Step 18 files remain untracked. No force push, manuscript modification, or historical-artifact mutation occurred.
