# ShiftSleep-UQ Step 20.2.5 Final R3 and Remediation Freeze Report

## 1. Status

Step 20.2.5 remains partial. R3 execution mechanics were repaired with disk-backed spectrogram caches and bounded in-process cache retention. Existing R3 attempts were reconciled. Two latest R3 jobs are accepted, but the remaining matrix could not continue safely on the local host because host memory remained above the hard engineering-abort threshold while GPU utilization was near zero. R2 paired reliability bootstrap inference also remains incomplete.

## 2. Final Gate

`FULL_REMEDIATION_PARTIAL`

## 3. Protocol Integrity

Protocol v1 SHA-256: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`.

Protocol v2 SHA-256: `c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`.

The v2 validator passed using the project environment. No protocol file was changed.

## 4. Starting Git State

Starting HEAD and `origin/main`: `e8fddae36d27682fbadd4642f4d099c174fdde0c`.

Step 20.2.4 preservation checkpoint: `c10652c9f0dd5e64519c3bfb2e668488295df637`.

R3 memory-engineering commit: `f4f195713ae362b2c874cb94c985ce37d02b0983`.

R3 attempt-reconciliation commit: `d4a5fb6`.

Both engineering commits were pushed to `origin/main`. Unrelated Step 18 files and `uv.lock` remain untracked and were not included.

## 5. R1/R2 Preservation

R1 and R2 preservation checks passed for the available artifacts:

- R1 SOURCE CAL audit: 24 rows.
- R1 calibration rows: 24.
- R1 evaluation rows: 144.
- R1 primary classification rows: present.
- Sleep-EDF reconstruction audit: 153 rows.
- R2 checkpoint rows: 12.
- R2 primary prediction rows: 72.
- R2 bootstrap primary rows: 4.
- R2 Holm rows: 4.
- R2 reliability rows: 7,488.
- R2 temperature groups: 12.

## 6. R3 Existing Attempt Reconciliation

`R3_D1_SLEEPEDF_TO_ISRUC_S0_SEED_17 / ATTEMPT_003` is accepted as `ACCEPTED_EXISTING_R3_JOB`.

Validated evidence includes the completion marker, ten-epoch history, checkpoint, parameter count 117,062, source-only normalization, matching checkpoint and normalization hashes, and the frozen protocol hash. DEV macro-F1 is `0.793102551969719`; DEV NLL is `0.3046142043351252`.

A second existing complete job was independently validated:

- `R3_D1_SLEEPEDF_TO_ISRUC_S0_SEED_42 / ATTEMPT_002`.
- Best epoch: 9.
- DEV macro-F1: `0.7880814393149074`.
- DEV NLL: `0.2963486845354727`.

The authoritative accepted manifest currently contains **2 latest accepted jobs**, not all historical attempt directories. Earlier duplicate attempts are preserved but not selected.

## 7. R3 Memory Root Cause

The original executor materialized complete per-recording spectrogram tensors in an unbounded Python cache and recomputed large recording arrays inside the dataset path. This caused high host-memory pressure and poor GPU utilization.

## 8. R3 Cache/Streaming Fix

The executor now:

- builds per-recording float32 `.npy` spectrogram caches;
- stores cache metadata with input hash, protocol hash, STFT hash, shape, dtype, labels, physical indices, and cache hash;
- reuses valid caches and rejects metadata mismatches;
- uses NumPy memory mapping for dataset access;
- limits the in-process recording cache to two entries with LRU eviction;
- fits source normalization in chunks from the disk-backed cache;
- uses `num_workers=0`;
- records loss with `loss.detach().item()`;
- reuses validated complete attempts instead of creating duplicate scientific attempts.

Cache location: `artifacts/remediation/r3/spectrogram_cache/`.

Cache files are ignored by Git.

## 9. Memory Profile

The technical profile created a cache with shape `[2820, 2, 129, 29]`, dtype `float32`, and STFT hash `63e844a6d2b5f8560c42785d5044bbac1c297c6fd9a469aaa4c33b0cfc9ffc2d`.

The cached transform matched the prior vectorized transform exactly on a four-epoch check: maximum absolute difference `0.0`; all values finite.

Profile artifact: `reports/remediation/r3_memory_profile_v1.csv`.

Measured cache footprint during execution: approximately `7.2G`. Technical profile host utilization was 89%. During the subsequent CUDA execution, host utilization reached 93% while GPU utilization was 0% at the hard-stop sample and GPU memory used was 568 MiB. The process was stopped to avoid sustained resource exhaustion.

## 10. R3 Sequence Coverage

No complete 12-job sequence-coverage manifest exists. The accepted jobs use the original benchmark composition, physical-contiguity checks, sequence length 20, and stride 10 for training. Remaining coverage is not computed.

## 11. R3 Training Jobs

Accepted: **2/12 latest scientific jobs**.

Accepted jobs:

- D1/S0/17: ATTEMPT_003.
- D1/S0/42: ATTEMPT_002.

The next D1/S0/2026 attempt was invalidated after the host-memory hard abort before checkpoint creation. The remaining jobs were not executed.

## 12. R3 Checkpoint Manifest

`reports/remediation/r3_checkpoint_manifest_v1.csv` contains 2 accepted latest-job rows. The required 12 rows are not present.

## 13. R3 Prediction Completeness

R3 prediction bundles: **0/72 accepted**. No R3 evaluation bundle was generated.

## 14. R3 Calibration

Not computed. No R3 source-CAL temperature table was generated.

## 15. R3 Predictive Metrics

Not computed beyond the accepted jobs' source-DEV checkpoint-selection metrics. No R3 C0-C5 evaluation metrics are accepted.

## 16. R3 Error Ranking

Not computed.

## 17. R3 Selective Prediction

Not computed.

## 18. R3 Randomized APS

Not computed. No R3 target or source-test conformal result is claimed.

## 19. R3 Bootstrap

Not computed. The required 2,000 subject-cluster replicates were not started for R3.

## 20. R3 Holm

Not computed. No R3 Holm family exists.

## 21. R3 Primary Effects

R3 S1-minus-S0 effects for D1/C4, D1/C5, D2/C4, and D2/C5 are `NOT COMPUTED`.

## 22. R3 Reliability Effects

Not computed. No R3 reliability paired table exists.

## 23. R3 Outcome

`BACKBONE_RESULT_INCONCLUSIVE`

This is an execution-resource outcome, not a negative strong-backbone scientific finding.

## 24. R2 Reliability Bootstrap Completion

The requested R2 paired reliability bootstrap output `r2_reliability_paired_v2.csv` was not completed. A background run was stopped when host memory pressure reached the engineering safety threshold while R3 was also active. The existing 32-row descriptive paired table remains distinct from the missing bootstrap inference.

R2 reliability bootstrap status: `NOT COMPLETE`.

## 25. Class-Prior Result

Cross-dataset natural-log Jensen-Shannon divergence:

- Before harmonization: `0.11943661377861878`.
- After harmonization: `0.025504007696203264`.
- Absolute reduction: `0.09393260608241552`.
- Relative reduction: `78.6464%`.

Harmonization substantially reduced the cross-dataset prior mismatch descriptively. This is not a causal claim.

## 26. Historical vs R2 vs R3

R1 materially changes the historical conformal interpretation. R2 remains partially robust with three Holm-supported positive primary macro-F1 effects and one inconclusive cell. R3 has two accepted development jobs but no evaluation evidence, so strong-backbone generalization remains unresolved.

## 27. Integrated Reliability Matrix

R2 descriptive reliability metrics are available for 72 bundles and 12 calibration groups. R2 paired bootstrap intervals for NLL, error ranking, and AURC are missing. R3 reliability is unavailable. No composite reliability score is created.

## 28. Conformal Final Position

The historical non-randomized APS headline is superseded for interpretation by the R1 randomized-APS sensitivity finding. Conformal transfer must not be described as robust. R2 and R3 conformal conclusions are not promoted beyond their available source-only diagnostics.

## 29. Integrated Conclusion Matrix

- Modality-exposure predictive effect: `SUPPORTED` by R2.
- Sleep-window robustness: `PARTIALLY_SUPPORTED`.
- Strong-backbone generalization: `INCONCLUSIVE`.
- Calibration robustness: `PARTIALLY_SUPPORTED` for descriptive R2 metrics; inferential completion missing.
- Ranking robustness: `PARTIALLY_SUPPORTED` descriptively; paired inference incomplete.
- Selective robustness: `PARTIALLY_SUPPORTED` descriptively; paired inference incomplete.
- Conformal transfer: `NOT_SUPPORTED` under the R1 reinterpretation.

## 30. Manuscript Impact

`ORIGINAL_CONCLUSION_MATERIALLY_REVISED`

## 31. JBHI Story

`JBHI_STORY_REQUIRES_MAJOR_REFRAMING`

## 32. Final Scientific Claims

Supported claims remain limited to provenance-equivalent R1 reconstruction, the R1 conformal reinterpretation, Sleep-EDF temporal provenance repair, and completed R2 predictive findings.

R3 strong-backbone generalization, R3 reliability, and complete R2 reliability inference remain unresolved.

## 33. Target Firewall

No target data were used for accepted R3 training, normalization, or DEV checkpoint selection. No R3 target calibration or evaluation occurred. R2 target use remains restricted to post-training evaluation under the previous remediation contract.

## 34. Historical Integrity

Historical processed NPZ files, checkpoints, prediction bundles, calibration artifacts, Figure 2, and manuscript packages were not overwritten. New R3 caches and attempts remain in remediation namespaces. Invalidated partial attempt evidence is retained and not reused.

## 35. Tests

Verified:

- v1/v2 protocol hashes;
- v2 validator: `valid: true`;
- R3 focused tests from the prior executor: 4 passed;
- R3 runner compilation;
- Ruff for the repaired runner and memory profiler;
- cache numerical equivalence: maximum absolute difference `0.0` on the technical sample;
- `git diff --check` at the preservation checkpoint.

A fresh full repository test suite after the latest R3 edits remains pending.

## 36. Full Validation

Not satisfied. Missing gates include 12 accepted R3 jobs, 72 R3 bundles, R3 calibration, R3 bootstrap, R3 Holm, R3 reliability, and R2 paired reliability bootstrap inference.

## 37. Runtime/Memory Summary

- CUDA interpreter: Torch `2.14.0+cu126`, CUDA available.
- CPU-only `uv` environment was rejected for scientific execution because it exposed Torch `2.14.0+cpu` and no CUDA.
- R3 cache footprint observed: approximately 7.2G.
- Technical cache profile: 2.34 seconds on a cache miss and 0.043 seconds on reuse for the profiled recording.
- Host utilization during profile: 89%.
- Host utilization during attempted CUDA continuation: 93%.
- GPU utilization at hard-stop sample: 0%.
- GPU memory used at hard-stop sample: 568 MiB.
- R3 D1/S0/17 prior accepted runtime: 1,483.9169 seconds.
- R3 D1/S0/42 accepted prior runtime: 13,479.9999 seconds.

## 38. Files Created

- `reports/remediation/r3_existing_attempt_reconciliation_v1.md`
- `reports/remediation/r3_memory_profile_v1.csv`
- `reports/remediation/r3_checkpoint_manifest_v1.csv`
- `scripts/run_r3_scientific.py` engineering revision
- `scripts/profile_r3_memory.py`
- `scripts/audit_r3_checkpoint_manifest.py`
- `scripts/bootstrap_r2_reliability_v2.py`
- invalidation metadata for D1/S0/2026 ATTEMPT_003.

## 39. Files Modified

- `scripts/run_r3_scientific.py` was modified for disk-backed caches, LRU retention, source-only streaming normalization, loss logging, and resumable accepted-attempt selection.
- No frozen protocol was modified.
- No canonical manuscript was modified.

## 40. Explicitly Not Done

- Remaining 10 accepted R3 jobs.
- R3 72 prediction bundles.
- R3 calibration and reliability.
- R3 bootstrap and Holm analysis.
- R2 paired reliability bootstrap v2.
- Final integrated effect matrix with R3 values.
- Final remediation tag.
- Step 20.3 and Step 21.

## 41. Remaining Risks

Local execution remains resource-blocked by host memory pressure and poor GPU utilization despite the disk-backed cache. The accepted existing jobs were produced before the latest cache-engineering revision and are retained as valid historical attempts; remaining jobs require a fresh, resource-safe continuation. The overall scientific conclusion may change after R3.

## 42. Recommended Next Step

Authorize an explicitly bounded external CUDA execution path, or otherwise provide a verified local CUDA environment with sufficient host memory. Continue from the immutable accepted-attempt manifest, never reuse the invalidated D1/S0/2026 ATTEMPT_003, then complete R3 evaluation and the missing R2/R3 reliability inference. Do not execute Step 20.3.

## 43. Git Commit

Latest pushed engineering commit: `d4a5fb6` (`research: reconcile resumable R3 attempts`).

Earlier pushed memory-engineering commit: `f4f1957` (`research: bound R3 spectrogram memory`).

The current invalidation/audit/reporting additions are not yet included in a final remediation commit.

## 44. Git Tag

`step20-2-remediation-results-frozen` was not created.

## 45. Push Status

`origin/main` was updated through `d4a5fb6`. No final remediation-results tag or final freeze push was made.

## 46. Git Status

The worktree contains uncommitted R3 audit/invalidation artifacts and the R2 bootstrap script, plus unrelated untracked Step 18 files and `uv.lock`. No historical artifact or manuscript mutation was performed.
