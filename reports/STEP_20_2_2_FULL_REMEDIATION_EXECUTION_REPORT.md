# ShiftSleep-UQ Step 20.2.2 Full Remediation Execution Report

## 1. Status

Step 20.2.2 was executed as far as the frozen evidence and repository implementation permitted. R1 was recovered and completed. The Sleep-EDF temporal ledger was reconstructed from official PhysioNet hypnogram annotations and passed all 153 recording audits. R2/R3 data feasibility was rerun on 252 repaired/valid recording ledgers, but the 12 R2 and 12 R3 scientific training jobs were not executed because the repository contains no frozen executable windowed B0/B1 or SeqSleepNet training/evaluation runner. Reusing the historical epoch-wise runner would violate the frozen R2/R3 contracts; no substitute training implementation or scientific result was invented.

## 2. Full Remediation Gate

`FULL_REMEDIATION_PARTIAL`

R1 is complete and interpretable. Sleep-EDF ledger repair is complete. R2 and R3 training/statistical families have no interpretable scientific results in this step.

Submission remains `SUBMISSION_SUSPENDED_FOR_SCIENTIFIC_REMEDIATION`.

## 3. Starting Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Starting HEAD: `18f580bc9b524761da146bb63e824680820e0d2d`
- `origin/main`: `18f580bc9b524761da146bb63e824680820e0d2d`
- Protocol milestone ancestry: present.
- No historical artifact was overwritten.

## 4. Protocol Integrity

- v1 SHA-256: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc` — PASS.
- v2 SHA-256: `c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b` — PASS.
- v2 validator: `valid: true`.
- Randomized APS implementation hash: `ab02e702a2f19ac5a10d134fa2ff2b7bc8a6b7294e63a5d203fdad4c5b967392` — PASS.
- Historical probability-stream hash: `a531942efe60d1ba3208b88d8ba164f87274992d0f60b07d08e39921d9c41a99` — PASS.

## 5. Historical Artifact Integrity

Historical B0/B1 predictions, calibration objects, protocols, manuscript files, Figure 2, Step 20.2, and Step 20.2.1 artifacts were preserved. All remediation outputs are derivatives under `artifacts/remediation` or `reports/remediation`.

## R1 Artifact Recovery

## 6. Missing SOURCE CAL Root Cause

Historical `aps.json` files serialized qhat metadata but not observation-level SOURCE CAL probabilities, labels, and identities. The frozen preprocessing/evaluation path, checkpoints, normalization, subject partitions, and dataset files were available, so deterministic inference was a provenance-preserving reconstruction rather than a new model experiment.

## 7. SOURCE CAL Reconstruction Method

For each direction, model family, and seed, the exact frozen B0/B1 checkpoint was loaded with the frozen normalization and SOURCE CAL role. The historical uncalibrated softmax stream was reproduced. The reconstruction stored probabilities, labels, subject IDs, recording IDs, and epoch IDs under:

`artifacts/remediation/r1/source_cal_reconstruction/R1_ATTEMPT_001/`

No retraining, checkpoint reselection, target access, or temperature fitting was used.

## 8. SOURCE CAL Reconstruction Validation

`reports/remediation/r1_source_cal_reconstruction_audit_v1.csv` contains 24 rows: 12 model-direction-seed combinations × 2 alpha values. All 24 rows are `PROVENANCE_EQUIVALENT_RECONSTRUCTION`.

- Success count: **24/24**.
- Probability rows finite: PASS for all combinations.
- Probability row sums: PASS for all combinations.
- Observation identity: complete for all combinations.
- Checkpoint and normalization bindings: PASS.

## 9. Historical APS qhat Reproduction

All 24 historical non-randomized APS qhat values were reproduced exactly at the recorded floating-point values. Maximum absolute difference: **0.0**, below the required `1e-10` tolerance.

## 10. R1 Randomized APS Execution

The frozen `RANDOMIZED_APS` implementation was applied with namespace `SHIFT_SLEEP_UQ_RAPSENS_V1`, global seed `2031`, alpha values `0.10` and `0.05`, and deterministic CAL_SCORE/PRED_SET keys. No target labels entered qhat fitting.

- Calibration rows: **24**.
- Evaluation rows: **144**.
- Source sanity rows: **24**.
- Historical-versus-randomized comparison rows: **144**.

## 11. R1 Source Sanity

`reports/remediation/r1_source_conformal_sanity_v1.csv` contains source-calibration randomized-APS set diagnostics for all 24 cells. The randomized qhat computation and set construction completed without non-finite values or schema failures.

## 12. R1 Target Results

Target labels were used only for final evaluation metrics. No target calibration, target qhat fitting, target adaptation, checkpoint selection, or hyperparameter selection occurred.

## 13. R1 Primary Cell Classifications

`reports/remediation/r1_primary_cell_classification_v1.csv` records the four direction-condition primary cells for both B0 and B1. At alpha `0.10`, every B0/B1 primary cell had absolute mean coverage deviation greater than 0.05 from nominal 0.90:

- D1 C4: B0 `0.8309932222620328`; B1 `0.8349456586647558`.
- D1 C5: B0 `0.7472717365340977`; B1 `0.7845828854651856`.
- D2 C4: B0 `0.7318310234777083`; B1 `0.8131952962647896`.
- D2 C5: B0 `0.8402677199383396`; B1 `0.7758833561065578`.

All recorded classifications are `CONFORMAL_INTERPRETATION_CHANGES` under the implemented coverage/set-size decision rule. This is not a claim that randomized APS is universally inferior; it is the observed frozen sensitivity result.

## 14. R1 Overall Outcome

`R1_MATERIALLY_CHANGES_CONFORMAL_FINDING`

The historical APS conformal headline cannot be retained unchanged. Randomized APS was provenance-validly computed and produced materially non-nominal target coverage in all four primary direction-condition cells for both model families. Predictive conclusions were not reclassified by R1.

## Sleep-EDF Provenance Repair

## 15. Epoch-Index Root Cause

`source_epoch_indices` was serialized from annotation-event ordinal `i` in `expand_annotations()`, not from the physical 30-second epoch position. A multi-epoch annotation therefore repeated one event ordinal; the processed Sleep-EDF ledgers consequently contained constant-zero indices. The exact root-cause record is `reports/remediation/sleepedf_epoch_index_root_cause.md`.

## 16. Reconstruction Source

The repair used the official PhysioNet Sleep-EDF hypnogram EDF+ files and the frozen repository pairing map in `reports/sleep_edf_pairing_audit.csv`. Annotation onsets and durations were required to align to 30-second boundaries. Physical indices were assigned from onset/30 plus within-annotation offset.

## 17. 153-Recording Reconstruction Audit

`reports/remediation/sleepedf_epoch_index_reconstruction_audit_v1.csv` contains **153/153 PASS** rows. Every recording passed integer, nonnegative, strictly increasing, unique, processed-label-prefix, and retained-count checks. Total repaired Sleep-EDF epochs: **414,961**.

## 18. Signal/Label Invariance

The repaired derivative changes only `source_epoch_indices`. EEG, EOG, labels, epoch onset values, and metadata values were preserved from each historical processed NPZ. Historical NPZ files were not overwritten.

## 19. Repaired Ledger

The versioned repaired ledger is:

`artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2/`

The gate manifest is `reports/remediation/sleepedf_epoch_ledger_v2_manifest.json`.

## 20. Ledger Gate

`SLEEPEDF_EPOCH_LEDGER_RECONSTRUCTED`

## R2

## 21. Windowing Accounting

`reports/remediation/r2_windowing_accounting_v1.csv` contains 252 recording rows: 153 Sleep-EDF and 99 ISRUC. The frozen physical-index first/last non-Wake plus 60-epoch context rule was applied as an accounting/preflight operation. No transformed training tensors or checkpoints were promoted.

## 22. Class Priors Before/After

`reports/remediation/r2_class_prior_before_after_v1.csv` records Wake/N1/N2/N3/REM counts and fractions before and after the frozen window selection. No target information was used for window selection.

## 23. Partition Integrity

The existing frozen subject partition metadata remained unchanged. No subject was replaced or reassigned. No no-sleep recording or subject-removal fallback was fabricated.

## 24. Normalization

Windowed SOURCE TRAIN normalization was not fitted. Existing historical normalization was not reused as a substitute for the frozen windowed-source normalization contract.

## 25. B0-W Training

Not executed. No frozen executable windowed B0-W training/evaluation runner exists in the repository. Running the historical epoch-wise B0 script would not satisfy physical-window selection, windowed-source normalization, or the required checkpoint contract.

## 26. B1-W Training

Not executed for the same contract reason. No B1-W checkpoint, optimizer state, prediction bundle, or scientific metric was created.

## 27. Checkpoint Selection

Not performed. No SOURCE DEV windowed checkpoint selection occurred, and no target quantity entered selection.

## 28. R2 Evaluation

Not performed. The expected 12-job R2 evaluation grid has zero promoted scientific jobs.

## 29. R2 Statistical Analysis

Not performed. No subject bootstrap, paired B1-W minus B0-W effect, or confidence interval was computed.

## 30. R2 Holm Sensitivity

Not performed because there are no R2 primary effects or p-values.

## 31. R2 Outcome

`WINDOW_RESULT_INCONCLUSIVE`

R2 feasibility passed after provenance repair, but no R2 predictive result exists.

## R3

## 32. Sequence Coverage

`reports/remediation/r3_sequence_coverage_v1.csv` contains 252 recording rows. Reconstructed Sleep-EDF and valid ISRUC ledgers passed strict physical-index continuity checks for the accounting pass. Sequence counts and short-segment accounting were recorded without model training.

## 33. SeqSleepNet Training Environment

The real-data signal/spectrogram/forward smoke from Step 20.2.1 remained valid. The GPU preflight supported batch 32, accumulation 1. No scientific R3 training process was launched.

## 34. S0 Training

Not executed. No frozen end-to-end SeqSleepNet-class sequence construction, source normalization, checkpoint-selection, and evaluation runner was present.

## 35. S1 Training

Not executed. No S1 exposure training or checkpoint was created.

## 36. R3 Checkpoint Selection

Not performed. No SOURCE DEV sequence checkpoint selection occurred.

## 37. R3 Evaluation

Not performed. The expected 12-job R3 grid has zero promoted scientific jobs.

## 38. R3 Statistical Analysis

Not performed. No subject bootstrap or paired S1 minus S0 effect was computed.

## 39. R3 Holm Sensitivity

Not performed because there are no R3 primary effects or p-values.

## 40. R3 Outcome

`BACKBONE_RESULT_INCONCLUSIVE`

R3 data and hardware feasibility were established, but no strong-backbone scientific result exists.

## Integration

## 41. Historical vs R2 vs R3

Historical results remain preserved. R1 is complete. R2 and R3 are not comparable because their training/evaluation families were not executed.

## 42. Predictive Effects

No new R2 or R3 predictive effect is claimed. The four R2 primary macro-F1 effects are `NOT_COMPUTED`; the four R3 primary macro-F1 effects are `NOT_COMPUTED`.

## 43. Calibration Effects

R1 randomized-APS calibration was completed. R2/R3 source temperature fitting and calibrated reliability analysis were not performed.

## 44. Selective-Prediction Effects

R1 secondary set-size diagnostics were computed. R2/R3 selective metrics are `NOT_COMPUTED`.

## 45. Conformal Reinterpretation

The historical APS conformal interpretation requires material revision. Randomized APS was computed from provenance-equivalent source calibration and did not reproduce nominal target coverage in the primary cells.

## 46. Seed Variability

R1 reports seeds 17, 42, and 2026 individually. R2/R3 seed-level scientific results do not exist.

## 47. Estimator Provenance

R1 uses deterministic keyed randomization and source-only qhat fitting. No target adaptation or target model selection occurred. R2/R3 estimators were not instantiated.

## 48. Conclusion Matrix

`reports/remediation/remediation_conclusion_matrix_v1.csv` records:

- historical predictive effect: verified historical only;
- window robustness: not determined;
- strong-backbone generalization: not determined;
- calibration behavior: R1 completed, R2/R3 not computed;
- selective behavior: R1 secondary diagnostics completed, R2/R3 not computed;
- conformal reinterpretation: historical headline requires reassessment.

## 49. Manuscript Impact Classification

`ORIGINAL_CONCLUSION_MATERIALLY_REVISED`

The conformal headline must be removed or substantially rewritten. Predictive generalization claims cannot be strengthened from this step because R2/R3 training did not produce results.

## 50. Corrected Figure 2

Preserved derivative:

`reports/remediation/fig2_b0_shift_landscape_corrected_v1.pdf`

It remains separate from the historical Figure 2 and uses numeric canonical coordinates.

## 51. Reference Corrections

Created `reports/remediation/reference_corrections_v1.csv`. Corrections remain a plan pending primary-source metadata verification.

## 52. Manuscript Revision Plan

Created `reports/remediation/postremediation_manuscript_revision_plan.md`. No manuscript or submission package was edited.

## Engineering

## 53. Attempt/Retry Summary

- R1 reconstruction: one immutable attempt, 24/24 provenance-equivalent rows.
- Sleep-EDF ledger repair: one derivative reconstruction attempt; 153/153 PASS.
- R2 training attempts: 0 promoted; no executor existed that satisfied the frozen contract.
- R3 training attempts: 0 promoted; no executor existed that satisfied the frozen contract.
- No technical retry was relabeled as a new scientific experiment.

## 54. Runtime Summary

- R1 reconstruction inference: completed on frozen checkpoints.
- Sleep-EDF annotation recovery: completed from 153 official hypnogram files.
- R1 randomized APS: 24 calibration and 144 evaluation rows completed.
- R2/R3 accounting: 252 recording rows completed.
- No model training was run in R2/R3.

## 55. Tests

- v2 validator: passed.
- R1 reconstruction audit: 24/24 passed.
- R1 result count: 144 rows.
- Sleep-EDF ledger audit: 153/153 passed.
- R2 accounting: 252 rows.
- R3 sequence accounting: 252 rows.
- Full repository tests: `161 passed`.

## 56. Full Validation

- v1 hash: PASS.
- v2 hash: PASS.
- Historical probability-stream hash: PASS.
- Randomized APS implementation hash: PASS.
- `python -m compileall -q src scripts`: PASS.
- `git diff --check`: PASS.
- v2 validator: `valid: true`.
- Historical artifacts: not overwritten.
- R2/R3 job completeness: 0/12 scientific jobs promoted for each family; explicitly incomplete, not represented as results.
- Target firewall: no target fitting or adaptation occurred.

## 57. Files Created

- `scripts/step20_2_2_recover_r1.py`
- `scripts/step20_2_2_execute_r1.py`
- `scripts/step20_2_2_reconstruct_sleepedf_ledger.py`
- `scripts/step20_2_2_account_repaired_data.py`
- `reports/remediation/r1_source_cal_reconstruction_audit_v1.csv`
- `reports/remediation/r1_randomized_aps_calibration_v1.csv`
- `reports/remediation/r1_randomized_aps_results_v1.csv`
- `reports/remediation/r1_source_conformal_sanity_v1.csv`
- `reports/remediation/r1_historical_vs_randomized_aps_v1.csv`
- `reports/remediation/r1_primary_results_v1.csv`
- `reports/remediation/r1_primary_cell_classification_v1.csv`
- `reports/remediation/sleepedf_epoch_index_root_cause.md`
- `reports/remediation/sleepedf_epoch_index_reconstruction_audit_v1.csv`
- `reports/remediation/sleepedf_epoch_ledger_v2_manifest.json`
- `reports/remediation/r2_windowing_accounting_v1.csv`
- `reports/remediation/r2_class_prior_before_after_v1.csv`
- `reports/remediation/r3_sequence_coverage_v1.csv`
- `reports/remediation/r2_primary_results_v1.csv`
- `reports/remediation/r2_paired_results_v1.csv`
- `reports/remediation/r3_primary_results_v1.csv`
- `reports/remediation/r3_paired_results_v1.csv`
- `reports/remediation/remediation_primary_effect_summary_v1.csv`
- `reports/remediation/remediation_conclusion_matrix_v1.csv`
- `reports/remediation/reference_corrections_v1.csv`
- `reports/remediation/postremediation_manuscript_revision_plan.md`
- `reports/STEP_20_2_2_FULL_REMEDIATION_EXECUTION_REPORT.md`

## 58. Files Modified

No historical protocol, historical prediction/calibration bundle, manuscript, JBHI package, historical Figure 2, Step 20.2, or Step 20.2.1 artifact was modified. Only new Step 20.2.2 scripts and derivative outputs were created.

## 59. Explicitly Not Done

- no protocol change;
- no target adaptation;
- no target model selection;
- no SHHS;
- no additional architecture;
- no alternate trimming rule;
- no B0-W/B1-W training;
- no S0/S1 training;
- no R2/R3 scientific evaluation or bootstrap;
- no manuscript submission;
- no Step 20.3;
- no Step 21.

## 60. Remaining Scientific Risks

1. R2 and R3 remain unresolved because no frozen end-to-end executors exist in the repository.
2. R1 changes the conformal interpretation but does not establish a new predictive generalization result.
3. The repaired ledger is a versioned derivative and must remain explicitly distinguished from historical processed artifacts.
4. R2/R3 statistics, Holm procedures, and integrated predictive conclusions remain uncomputed.

## 61. Recommended Next Step

# Step 20.3 — Rebuild the Manuscript Around the Remediation Evidence

Do **NOT** execute Step 20.3. Before manuscript rebuilding, the missing R2/R3 execution infrastructure and scientific runs require a separately controlled implementation/execution stage. The R1 conformal result must be incorporated into any future revision.

## 62. Git Commit

No milestone commit was created. The gate is `FULL_REMEDIATION_PARTIAL`, not a complete integrated remediation result.

## 63. Git Tag

No `step20-2-remediation-results-frozen` tag was created because the gate is not complete.

## 64. GitHub Push Status

No Step 20.2.2 push was performed. `origin/main` remains at `18f580bc9b524761da146bb63e824680820e0d2d`.

## 65. Git Status / Diff Summary

The worktree contains the new R1 reconstruction/execution scripts, repaired ledger derivatives, R1 results, R2/R3 accounting tables, integration placeholders, root-cause documentation, reference correction manifest, manuscript revision plan, and this report. Historical Step 18 and Step 20.2.1 files remain untracked as they were before this step. No R2/R3 scientific checkpoint namespace was created, and no tag or commit was made.
