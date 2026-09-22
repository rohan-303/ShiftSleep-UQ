# ShiftSleep-UQ Step 20.2.1 R1 and Execution Preflight Report

## 1. Status

Step 20.2.1 was partially completed. Protocol validation passed, all 72 frozen B0/B1 SOURCE/target prediction bundles were audited, the corrected Figure 2 was generated, and R2/R3 real-data feasibility preflights were run without training. R1 randomized-APS computation was blocked before calibration because the frozen SOURCE CAL probability bundles required to compute randomized quantiles are absent. R2 and R3 were independently blocked by invalid Sleep-EDF original epoch-index ledgers.

No model inference rerun, temperature fitting, conformal fitting, training, scientific bootstrap, manuscript modification, submission, Step 20.2.2, or Step 21 occurred.

## 2. Step Gate

`STEP20_2_1_PARTIAL`

R1 gate: `R1_REMEDIATION_BLOCKED`.

R1 overall outcome: `R1_CONFORMAL_RESULT_INCONCLUSIVE`.

R2 authorization: `R2_EXECUTION_BLOCKED`.

R3 authorization: `R3_EXECUTION_BLOCKED`.

Submission remains `SUBMISSION_SUSPENDED_FOR_SCIENTIFIC_REMEDIATION`.

## 3. Starting Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Starting HEAD: `18f580bc9b524761da146bb63e824680820e0d2d`
- `origin/main`: `18f580bc9b524761da146bb63e824680820e0d2d`
- Required protocol milestone `3601b05082d780b9c149fcc3f74ecdaccf54ebce`: present in ancestry.
- Documentation descendant `18f580bc9b524761da146bb63e824680820e0d2d`: present and synchronized.
- Intentional historical Step 18 files remained untracked and unstaged.

## 4. Protocol v1 Hash

`configs/postreview_remediation_protocol_v1.yaml`:

`9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`

Result: `PASS`.

## 5. Protocol v2 Hash

`configs/postreview_remediation_protocol_v2.yaml`:

`c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`

Result: `PASS`; no protocol drift.

## 6. Validator

`scripts/validate_postreview_remediation_protocol_v2.py` returned `valid: true` before R1 input processing.

## 7. Historical Artifact Integrity

The historical probability-stream implementation hash matched v2:

- `src/shiftsleep_uq/evaluation_step11.py`: `a531942efe60d1ba3208b88d8ba164f87274992d0f60b07d08e39921d9c41a99`;
- `src/shiftsleep_uq/randomized_aps.py`: `ab02e702a2f19ac5a10d134fa2ff2b7bc8a6b7294e63a5d203fdad4c5b967392`.

R1 was configured to use uncalibrated softmax probabilities only. Temperature-scaled probabilities were not used.

## 8. R1 Input Audit

`reports/remediation/r1_input_hash_audit_v1.csv` contains 72 expected prediction-bundle rows:

- 2 directions;
- 2 model families;
- 3 seeds;
- 6 conditions.

All 72 prediction bundles existed and had observed SHA-256 values. No historical expected bundle hashes were available in the frozen manifest, so the rows are recorded as `PASS_OBSERVED_FILE`, not as expected-hash equivalence.

The required SOURCE CAL probability bundles were not present. The 24 existing `artifacts/calibration/{b0,b1_moddrop}/<direction>/seed_<seed>/aps.json` files contain historical qhat metadata but not per-observation SOURCE CAL logits/probabilities and labels. Historical qhat values cannot be transformed into randomized-APS qhat values without the underlying calibration observations.

## 9. R1 Randomization Validation

The deterministic randomizer implementation was previously validated synthetically. A real-data R1 randomization audit was not started because calibration inputs were incomplete. No real observation-level `U` values were generated for scientific computation.

## 10. R1 Calibration

The expected calibration table has 24 direction/model/seed/alpha combinations. `reports/remediation/r1_randomized_aps_calibration_v1.csv` records all 24 combinations with status `BLOCKED_SOURCE_CAL_BUNDLE_MISSING`; no qhat, calibration count, or source-calibration hash is claimed.

No target label entered q estimation.

## 11. R1 Result Completeness

`reports/remediation/r1_randomized_aps_results_v1.csv` contains the frozen schema but zero scientific result rows. The required 144 rows were not produced because the 24 SOURCE CAL randomized qhat values could not be computed.

This is an input-artifact blocker, not evidence for or against the historical conformal finding.

## 12. R1 Source-Domain Sanity

`reports/remediation/r1_source_conformal_sanity_v1.csv` contains the required schema but no computed randomized-APS rows. D1 and D2 source-test randomized-APS sanity is `NOT COMPUTED`.

The historical non-randomized APS source-test artifacts were not relabeled as randomized-APS results.

## 13. R1 Target Results

`NOT COMPUTED`. No target labels were used for calibration, and no target randomized-APS evaluation was performed.

## 14. R1 Set-Size Behavior

`NOT COMPUTED` for randomized APS. No empty-set, singleton, size-2, size-3, size-4, or size-5 randomized set distribution was generated.

## 15. Historical APS vs Randomized APS

`reports/remediation/r1_historical_vs_randomized_aps_v1.csv` contains the comparison schema but no rows. A historical-versus-randomized comparison cannot be made without randomized qhat and prediction-set outputs.

No universal conformal winner was declared.

## 16. D1 C4 Conformal Classification

`INCONCLUSIVE` — SOURCE CAL randomized-APS inputs are unavailable.

## 17. D1 C5 Conformal Classification

`INCONCLUSIVE` — SOURCE CAL randomized-APS inputs are unavailable.

## 18. D2 C4 Conformal Classification

`INCONCLUSIVE` — SOURCE CAL randomized-APS inputs are unavailable.

## 19. D2 C5 Conformal Classification

`INCONCLUSIVE` — SOURCE CAL randomized-APS inputs are unavailable.

## 20. R1 Overall Outcome

`R1_CONFORMAL_RESULT_INCONCLUSIVE`.

The historical interpretation remains unchanged and cannot be updated from this step: APS requires primary-axis reframing, while randomized-APS sensitivity remains uncomputed.

## 21. Corrected Figure 2 Source Audit

Created:

`reports/remediation/fig2_b0_shift_landscape_corrected_source_v1.csv`

The table contains exactly 48 rows: 2 directions × 6 conditions × 4 metrics. Values were derived from frozen B0 v1.2 per-seed metrics without rerunning inference:

- macro-F1;
- calibrated NLL;
- entropy AURC;
- absolute alpha-.10 coverage gap.

All 48 values are floating-point numeric values and all absolute-gap values are nonnegative. D1 macro-F1 retains the canonical non-monotonic sequence.

## 22. Corrected Figure 2

Created:

`reports/remediation/fig2_b0_shift_landscape_corrected_v1.pdf`

The figure plots actual numeric coordinates and does not overwrite any historical Figure 2 artifact.

## 23. R2 Windowing Preflight

Created:

`reports/remediation/r2_windowing_preflight_v1.csv`

The audit covers 252 recording ledgers:

- Sleep-EDF: 153 recordings;
- ISRUC: 99 recordings.

All 99 ISRUC recordings passed the original-epoch-index contract. All 153 Sleep-EDF recordings have `source_epoch_indices` that are constant zero rather than strictly increasing original epoch positions. Therefore the frozen physical-index window rule cannot be applied validly to Sleep-EDF from the current ledger.

Sleep-EDF window start/end and retained counts are marked `NOT_COMPUTED`, with status `BLOCKED_INVALID_SOURCE_EPOCH_INDICES`. No transformed real-data tensors were written.

## 24. R2 Recording Accounting

No valid before/after recording accounting can authorize R2 for Sleep-EDF because its original epoch-index ledger is invalid. ISRUC has 99 usable recording ledgers and no detected no-non-Wake recording among those valid ledgers.

Subject preservation for the full two-dataset R2 cohort is not established because 153 Sleep-EDF recordings cannot be windowed under the frozen physical-index rule. The required subject-removal stop condition was not triggered from a fabricated fallback; R2 is blocked earlier by the ledger defect.

## 25. R2 Class-Prior Before/After

`reports/remediation/r2_class_prior_preflight_v1.csv` contains descriptive BEFORE counts where available. Sleep-EDF AFTER counts and the corresponding AFTER Jensen-Shannon divergence are `NOT_COMPUTED` because its source epoch-index contract failed. No after-window class-prior claim is made.

## 26. R2 Partition Integrity

`reports/remediation/r2_partition_preflight_v1.csv` contains 177 subject rows, all `PASS` for one preserved role among TRAIN, DEV, CALIBRATION, and TEST:

- Sleep-EDF: 78 subjects;
- ISRUC: 99 subjects.

Partition metadata itself is preserved. This does not override the invalid Sleep-EDF epoch-index blocker.

## 27. R2 Model/Config Hashes

The following hashes matched the v2 protocol:

- architecture: `fce3e0dbef2e818d2c408ba5aecfd2eddeaa31a169c4ace99ce7badf5d7e5109`;
- B0 config: `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`;
- B1 config: `b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6`;
- normalization: `1406d760f7f1728efcf5ba34a2c2b38e42e287fcd136b43fc020594c572e4ff5`;
- exposure: `5c3b2924267de6b8052187c003eb41d9a8a4ade6e49d15839368998c6f0b59bf`.

Hashes pass, but data-ledger feasibility does not.

## 28. R2 Runtime Estimate

`NOT AUTHORIZED`. Approximate batch planning was not promoted because the frozen physical-window accounting is unavailable for Sleep-EDF. No R2 training job was launched.

## 29. R2 Execution Authorization

`R2_EXECUTION_BLOCKED`.

Reason: the Sleep-EDF processed ledger does not preserve strictly increasing original 30-second epoch indices required by the frozen window rule. No scientific fallback to row positions was used.

## 30. R3 Real-Data Signal Smoke

The deterministic lexicographically first SOURCE TRAIN smoke records were:

- ISRUC: subject I001, recording I001;
- Sleep-EDF: subject SC_03, recording SC4031E0.

Both had finite EEG/EOG arrays. EEG input was 100 Hz-equivalent with 3,000 samples per epoch. EOG was resampled deterministically from 50 Hz-equivalent 1,500 samples to 3,000 samples using `resample_poly(up=2, down=1)`.

## 31. R3 Spectrogram Smoke

Both real-data smoke records produced finite spectrogram tensors with shape `[20,2,129,29]`. No accuracy, loss, label metric, or model-selection quantity was computed.

## 32. R3 Sequence Coverage

Created:

`reports/remediation/r3_sequence_coverage_preflight_v1.csv`

The ISRUC ledgers passed the strictly increasing contiguous original-index contract. All 153 Sleep-EDF ledgers failed it because their source epoch indices are constant zero. Sleep-EDF sequence coverage, stride-10 training counts, and stride-1 evaluation counts are therefore `NOT_COMPUTED` rather than inferred from row order.

## 33. R3 Short-Segment Warnings

No valid short-segment percentage was promoted for Sleep-EDF because sequence continuity is blocked at the source-index contract. No `R3_SHORT_SEGMENT_COVERAGE_WARNING` was used to mask this earlier blocker.

## 34. R3 Model Hash

`src/shiftsleep_uq/models/seqsleepnet_class.py` matched the frozen v2 hash:

`f1e6b3f0f105ec2b002d6d80f3d8eafc0f665ebae12635f66b41c90b3aee7894`

The model has 117,062 trainable parameters.

## 35. R3 Real-Data Forward Smoke

Using technical seed `99991`, real-data smoke tensors produced finite logits of shape `[1,20,5]` under:

- FULL;
- EEG_ONLY;
- EOG_ONLY.

No accuracy or scientific metric was computed, and no prediction bundle was saved.

## 36. R3 GPU Memory Preflight

The available GPU was an NVIDIA GeForce RTX 3060 Laptop GPU with 6,144 MiB total VRAM. A technical FP32 batch-32 forward/backward smoke succeeded without an epoch-training loop:

- output shape: `[32,20,5]`;
- finite forward output: `true`;
- finite backward loss: `true`;
- peak allocated VRAM: 302,106,624 bytes;
- permitted configuration: `batch32 accumulation1`.

This is engineering evidence only and does not overcome the Sleep-EDF sequence-ledger blocker.

## 37. R3 Execution Authorization

`R3_EXECUTION_BLOCKED`.

Reason: complete R3 sequence construction cannot be verified for Sleep-EDF because original epoch-index continuity is invalid. The signal and model forward smoke passed, but the frozen real-data sequence contract did not.

## 38. Target Firewall Audit

Created:

`reports/remediation/step20_2_1_target_firewall_audit.csv`

The audit records that target labels were never used to fit randomized-APS q values, and that R2/R3 normalization, model training, checkpoint selection, temperature fitting, conformal fitting, and hyperparameter selection were not performed. No SHHS data was accessed.

## 39. No-Training Audit

Created:

`reports/remediation/step20_2_1_no_training_audit.csv`

No new R2/R3 checkpoints, trained state dictionaries, optimizer states, or prediction bundles were created. The seed-99991 technical model was ephemeral and was not promoted.

## 40. Tests

Completed checks:

- v2 protocol validator: passed;
- R1 input-bundle audit: 72 rows, all observed bundles present;
- calibration completeness ledger: 24 blocked combinations recorded;
- corrected Figure 2 source: 48 rows;
- R2 window preflight: 252 rows;
- R2 partition preflight: 177 rows, all metadata rows PASS;
- R3 sequence preflight: 252 rows with explicit Sleep-EDF index blockers;
- real-data spectrogram smoke: finite `[20,2,129,29]` tensors;
- real-data model forward smoke: all three masks passed;
- technical batch-32 FP32 forward/backward smoke: passed.

The prior synthetic R1/R3 scaffolding tests remain passing. No test was used to convert the missing SOURCE CAL artifact into a scientific result.

## 41. Full Validation

The following fresh validations passed:

- protocol v1 hash: unchanged;
- protocol v2 hash: unchanged;
- randomized APS implementation hash: unchanged;
- historical probability-stream hash: unchanged;
- model/config binding hashes: matched;
- `python -m compileall -q src scripts`: passed;
- full repository test suite: `161 passed`;
- `git diff --check`: passed.

## 42. Files Created

- `scripts/step20_2_1_preflight.py`
- `reports/remediation/r1_input_hash_audit_v1.csv`
- `reports/remediation/r1_randomized_aps_calibration_v1.csv`
- `reports/remediation/r1_randomized_aps_results_v1.csv`
- `reports/remediation/r1_source_conformal_sanity_v1.csv`
- `reports/remediation/r1_historical_vs_randomized_aps_v1.csv`
- `reports/remediation/r1_primary_cell_classification_v1.csv`
- `reports/remediation/fig2_b0_shift_landscape_corrected_source_v1.csv`
- `reports/remediation/fig2_b0_shift_landscape_corrected_v1.pdf`
- `reports/remediation/r2_windowing_preflight_v1.csv`
- `reports/remediation/r2_class_prior_preflight_v1.csv`
- `reports/remediation/r2_class_prior_js_preflight_v1.csv`
- `reports/remediation/r2_partition_preflight_v1.csv`
- `reports/remediation/r3_sequence_coverage_preflight_v1.csv`
- `reports/remediation/r3_real_data_smoke_v1.csv`
- `reports/remediation/step20_2_1_target_firewall_audit.csv`
- `reports/remediation/step20_2_1_no_training_audit.csv`
- `reports/STEP_20_2_1_R1_AND_EXECUTION_PREFLIGHT_REPORT.md`

## 43. Files Modified

No v1/v2 protocol, historical B0/B1 result, historical Figure 2, model checkpoint, prediction bundle, calibration object, partition, manuscript, JBHI package, or Step 20.2 blocked report was modified.

The new preflight script was corrected once after its initial metadata mapping exposed that Sleep-EDF subject IDs must be resolved through the recording manifest. The final script explicitly blocks invalid Sleep-EDF original epoch-index ledgers instead of using row positions as a scientific fallback.

## 44. Explicitly Not Done

- no B0_W training;
- no B1_W training;
- no S0 training;
- no S1 training;
- no R2 scientific inference;
- no R3 scientific inference;
- no randomized-APS q fitting;
- no randomized-APS target evaluation;
- no target calibration;
- no protocol change;
- no manuscript modification;
- no submission;
- no Step 20.2.2;
- no Step 21.

## 45. Remaining Risks

1. R1 cannot be completed until frozen per-observation SOURCE CAL probability/label bundles are restored or a separately authorized pre-outcome artifact amendment defines an equivalent immutable source.
2. R2 and R3 cannot be authorized until the Sleep-EDF processed ledger provides strictly increasing original 30-second epoch indices, or a separately authorized correction restores the missing ledger field without changing scientific data.
3. The corrected Figure 2 is an artifact-level correction only; it does not resolve the blocked conformal sensitivity.
4. No window robustness, backbone generalization, or overall manuscript-impact conclusion is supported by this step.

## 46. Recommended Next Step

# Step 20.2.2 — Execute the Harmonized Sleep-Window B0/B1 Sensitivity

Do NOT execute Step 20.2.2.

Before Step 20.2.2 can be authorized, the missing SOURCE CAL R1 inputs and invalid Sleep-EDF original epoch-index ledger require separately authorized provenance-preserving remediation. This report does not amend either frozen protocol.

## 47. Git Commit

No commit was created because the Step 20.2.1 gate is `STEP20_2_1_PARTIAL`, R1 is blocked, and R2/R3 are blocked. The commit policy authorizes a checkpoint only for `STEP20_2_1_COMPLETE` or `STEP20_2_1_COMPLETE_WITH_WARNINGS`. No remediation-results tag is permitted.

## 48. GitHub Push Status

No Step 20.2.1 push was performed. The synchronized v2 protocol state remains intact at `origin/main` through the starting commit.

## 49. Git Status / Diff Summary

The worktree contains new preflight scripts, R1 blocker/audit tables, the corrected Figure 2, R2/R3 preflight tables, firewall/no-training audits, and this report. The intentional historical Step 18 files remain untracked and unstaged. No R2/R3 attempt namespace or scientific checkpoint namespace was created.
