# ShiftSleep-UQ Step 20.1.2 Executable Remediation Protocol v2 Report

## 1. Status

Step 20.1.2 completed. The historical v1 protocol and blocked Step 20.2 report were preserved. A new executable v2 protocol and synthetic-only execution scaffolding were created and validated. No R1, R2, or R3 scientific execution occurred.

## 2. Protocol v2 Gate

`EXECUTABLE_REMEDIATION_PROTOCOL_V2_FROZEN`

Submission state remains `SUBMISSION_SUSPENDED_FOR_SCIENTIFIC_REMEDIATION`.

## 3. Starting Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Starting synchronized HEAD: `dc37ed49e60f4ce04034d50513183d83ac0340ac`
- `origin/main` at pre-freeze validation: `dc37ed49e60f4ce04034d50513183d83ac0340ac`
- v1 protocol gate: `SCIENTIFIC_REMEDIATION_PROTOCOL_FROZEN`
- synchronization gate: `STEP20_1_SYNCHRONIZED`
- The four intentional Step 18 historical files remained untracked and unstaged.

## 4. Historical v1 Integrity

`configs/postreview_remediation_protocol_v1.yaml` was not modified.

- Required SHA-256: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`
- Observed SHA-256: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`
- Result: `PASS`

## 5. Blocked Step 20.2 Preservation

`reports/STEP_20_2_POSTREVIEW_REMEDIATION_EXECUTION_REPORT.md` was preserved unchanged as the historical blocked-execution report. It continues to state `STEP20_2_PROTOCOL_UNDERSPECIFIED` and `REMEDIATION_EXPERIMENTS_BLOCKED`; it was not rewritten to imply scientific execution.

## 6. Amendment Scope

v2 resolves execution mechanics only. It preserves the v1 questions: R1 randomized conformal sensitivity, R2 harmonized B0/B1 sleep-window sensitivity, R3 SeqSleepNet-class confirmation, four primary compound cells, source-only calibration, target-free evaluation, seeds 17/42/2026, subject-level inference, no SHHS, and no target adaptation.

## 7. R1 Final Method

`RANDOMIZED_APS`. RAPS is not executed and remains related-method context only. Alpha values are exactly `0.10` and `0.05`.

## 8. Historical APS Probability-Stream Binding

The historical stream is uncalibrated softmax probabilities produced by `softmax` in `src/shiftsleep_uq/evaluation_step11.py`; the historical APS functions are `aps_scores`, `aps_quantile`, and `aps_prediction_set`. The bound source hash is `a531942efe60d1ba3208b88d8ba164f87274992d0f60b07d08e39921d9c41a99`. R1 uses the same unscaled probability stream and does not use source-temperature-scaled probabilities.

## 9. Randomized APS Definition

For sorted probabilities and true-label rank `r`, the score is the probability mass before the true label plus `U` times the true-label probability. Calibration uses the clamped 1-indexed `ceil((n+1)(1-alpha))` order statistic without interpolation. Prediction sets randomize only the boundary class; empty sets are allowed and reported.

## 10. Randomization/Reproducibility Rule

The namespace is `SHIFT_SLEEP_UQ_RAPSENS_V1`, global seed `2031`, with direction, model family, model seed, split, subject, recording, epoch index, and purpose as key fields. `U` is generated from SHA-256 and the first 53 usable bits of the first eight big-endian digest bytes divided by `2^53`. Alpha is excluded from the key. Implementation: `src/shiftsleep_uq/randomized_aps.py`, hash `ab02e702a2f19ac5a10d134fa2ff2b7bc8a6b7294e63a5d203fdad4c5b967392`.

## 11. R1 Synthetic Validation

Synthetic tests passed for deterministic randomization, quantile selection, prediction-set construction, row-order-independent keying, finite set summaries, alpha handling, and empty-set accounting. No scientific prediction bundle was read.

## 12. R2 Window Rule

The implementation operates on original 30-second epoch positions, finds the first and last valid non-Wake labels, retains the inclusive physical interval with 60 chronological epoch positions on each side, then applies historical validity exclusions. Recordings without valid non-Wake sleep are excluded. If this removes an entire subject, execution must stop with `R2_SUBJECT_SET_CHANGED_BY_NO_SLEEP_RECORDING`. Implementation hash: `3fb8ef4e29f5dc1d8b19370c6c254d3505086d3fc1b4c201da11b68172d755bd`.

## 13. R2 Historical Model Binding

R2 binds to the historical B0/B1 architecture and configuration artifacts:

- architecture: `src/shiftsleep_uq/models/baseline_b0.py`, SHA-256 `fce3e0dbef2e818d2c408ba5aecfd2eddeaa31a169c4ace99ce7badf5d7e5109`;
- B0 config: `configs/baseline_b0_v1.yaml`, SHA-256 `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`;
- B1 config: `configs/baseline_b1_moddrop_v1.yaml`, SHA-256 `b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6`.

## 14. R2 Training Configuration

B0_W and B1_W use historical B0/B1 architecture, cross-entropy, AdamW, learning rate `3e-4`, weight decay `1e-4`, betas `(0.9, 0.999)`, epsilon `1e-8`, physical/effective batch size `128`, FP32, global gradient clipping `1.0`, maximum 30 epochs, minimum 5 epochs, patience 6, and no scheduler. Seeds are 17, 42, and 2026. B0 and B1 differ only in exposure.

## 15. R2 Checkpoint Rule

Source DEV full-modality selection only: highest macro-F1, lowest NLL on a numeric tie under project precision, then earliest epoch. Missing-modality DEV selection and target selection are forbidden.

## 16. R2 Normalization

Global scalar mean/std per modality is refit on windowed source TRAIN only, with epsilon `1e-8`, using the historical normalization implementation bound to `src/shiftsleep_uq/training/normalization.py`, SHA-256 `1406d760f7f1728efcf5ba34a2c2b38e42e287fcd136b43fc020594c572e4ff5`. No target normalization is permitted.

## 17. R2 Calibration

Temperature is fit on source CAL only with the historical routine. Ranking uses uncalibrated predictive entropy. Randomized APS is secondary only; conformal coverage gap is not a primary directional reliability axis.

## 18. R2 Modality Exposure

B0_W is FULL-only. B1_W uses FULL `0.50`, EEG-only `0.25`, and EOG-only `0.25`, with exposure seed `2029` and the historical exposure binding `src/shiftsleep_uq/training/modality_exposure.py`, SHA-256 `5c3b2924267de6b8052187c003eb41d9a8a4ade6e49d15839368998c6f0b59bf`. Matched initialization is required for each direction and seed.

## 19. R2 Config Equality Audit

The v2 YAML and validator bind B0_W and B1_W to identical architecture, optimizer, batch, precision, epoch, checkpoint, normalization, calibration, and statistical settings. The sole intended difference is training modality exposure. This was validated by the protocol structure; no real-data run was performed.

## 20. SeqSleepNet Literature/Source Binding

R3 is explicitly `SeqSleepNet-class`, not byte-identical SeqSleepNet reproduction. The published reference is Phan et al. (2019), DOI `10.1109/TNSRE.2019.2896659`. The official author repository is `https://github.com/pquochuy/SeqSleepNet`, observed at commit `f8a5fd039e9511bfd5573e6cc684d8e9bfd2fab9` on 2026-09-22. The original TensorFlow repository is not a runtime dependency.

## 21. R3 Time-Frequency Input

EEG and EOG are used, with EEG at 100 Hz. EOG is deterministically resampled from 50 Hz with `scipy.signal.resample_poly(up=2, down=1)`. Each 30-second epoch uses a 2-second, 50%-overlap Hamming STFT, hop 100, FFT 256, 129 one-sided bins, and 29 frames; power is `abs(STFT)^2`, followed by `ln(power + 1e-8)`.

## 22. R3 Filterbanks

Each channel has a separate trainable `W_c` of shape `129 x 32`; the effective filterbank is `sigmoid(W_c) * T`, where `T` is the fixed linear-frequency triangular support from the referenced construction. Local support shape is `129 x 32`; synthetic comparison tolerance is `1e-7`. The local model module is `src/shiftsleep_uq/models/seqsleepnet_class.py`, SHA-256 `f1e6b3f0f105ec2b002d6d80f3d8eafc0f665ebae12635f66b41c90b3aee7894`.

## 23. R3 Epoch Encoder

The concatenated 64-dimensional per-frame representation is processed by a bidirectional GRU with hidden size 64 per direction, projected from 128 to 64, and aggregated with softmax attention over 29 frames.

## 24. R3 Sequence Encoder

The 20-epoch embeddings are processed by a bidirectional GRU with input 64 and hidden size 64 per direction, followed by a `128 -> 5` classifier for Wake/N1/N2/N3/REM.

## 25. R3 Sequence Construction

Training uses complete length-20 sequences with stride 10 and no padding. Evaluation uses complete length-20 sequences with stride 1 and averages raw logits over every window containing each epoch. Recording, subject, and original-index continuity boundaries are enforced; gaps terminate segments. Segments shorter than 20 are excluded and reported.

## 26. R3 Modality Gating

The modality mask is applied after the channel filterbank and before EEG/EOG concatenation. S0 is FULL-only. S1 uses FULL `0.50`, EEG-only `0.25`, and EOG-only `0.25`. A sequence mask is constant over all 20 epochs.

## 27. R3 Training Configuration

R3 uses mean cross-entropy over 20 labels, Adam, learning rate `1e-4`, weight decay `1e-3`, batch size 32 sequences, exactly 10 epochs, FP32, no scheduler, and global gradient clipping 1.0. Exposure seed is 2029. Python, NumPy, PyTorch CPU/CUDA RNGs are seeded; deterministic algorithms are requested and cuDNN benchmarking is disabled.

## 28. R3 Checkpoint Rule

After every epoch, evaluate source DEV full modality. Select highest macro-F1, then lowest NLL, then earliest epoch. All 10 epochs are required; missing-modality DEV and target selection are forbidden.

## 29. R3 Hardware Fallback

The target is an RTX 3060 Laptop GPU with 6 GB VRAM. The only fallbacks are batch 16 with accumulation 2, then batch 8 with accumulation 4, preserving effective batch size 32. No precision, sequence, hidden-size, or model reduction is allowed. Batch-8 OOM produces `R3_HARDWARE_BLOCKED`.

## 30. R3 Synthetic Forward Validation

Using synthetic input `[2,20,2,129,29]`, FULL, EEG-only, and EOG-only masks produced finite logits of shape `[2,20,5]`. The synthetic smoke test passed.

## 31. R3 Config Equality Audit

S0 and S1 share the same model, input, sequence, optimizer, training, checkpoint, deterministic, calibration, and statistical settings. They differ only in training exposure. Matched initialization is required and tested by the protocol contract. No scientific initialization was created.

## 32. Statistical Estimand

The estimand is subject-sampling uncertainty for the mean of three prespecified model seeds per bootstrap replicate. It is not the distribution over arbitrary future initializations. Primary cells are exactly D1 C4, D1 C5, D2 C4, and D2 C5. Primary metric is macro-F1; R2 effect is B1_W minus B0_W and R3 effect is S1 minus S0.

## 33. Bootstrap

Subject-level duplicate-preserving bootstrap uses 2,000 replicates and seed 2028. Each replicate computes metrics separately for seeds 17, 42, and 2026, then averages them. CIs are paired percentile 95% intervals.

## 34. Holm P-Value Construction

For each observed effect and bootstrap effects, null-centered deviations are `d_b = delta_b - delta_hat`; the two-sided sensitivity p-value is `(1 + count(abs(d_b) >= abs(delta_hat))) / (2000 + 1)`. This is confirmatory sensitivity only and does not replace percentile CIs.

## 35. Holm Procedure

Standard step-down Holm at 0.05 is applied separately to the four R2 primary macro-F1 effects and the four R3 primary macro-F1 effects. Reliability metrics are not included in the Holm families.

## 36. Artifact Namespace

R1, R2, and R3 namespaces are `artifacts/remediation/r1`, `artifacts/remediation/r2`, and `artifacts/remediation/r3`. Attempt IDs are deterministic and increment on retry. Required attempt contents include config snapshot, protocol hash, environment manifest, stdout/stderr, run metadata, and completion marker; checkpoints and hashes are required where applicable.

## 37. Attempt Immutability

Retries use new attempt directories and never overwrite. Existing promoted paths fail rather than being replaced.

## 38. Promotion Rules

Promotion requires successful completion, matching v2 protocol hash, expected files, schema validation, finite required outputs, checkpoint hash where applicable, and a passing target-firewall audit. Promotion creates a lightweight manifest referencing the immutable attempt.

## 39. Target Firewall

The v2 firewall forbids target labels in primary execution, target normalization, target checkpoint selection, target temperature/conformal calibration, target hyperparameter selection, and SHHS use. Source CAL is the only calibration population.

## 40. Protocol Validator

`scripts/validate_postreview_remediation_protocol_v2.py` validates the v1 hash, v2 gate, R1 method/randomizer, R2 window/training/checkpoint/normalization bindings, R3 architecture/sequence/training/fallback fields, bootstrap/Holm settings, artifact contract, and target firewall. It passed with `valid: true`.

## 41. Dry-Run Job Matrix

`reports/step20_1_2_execution_plan_v2.json` was created without execution:

- R1: 36 resolvable descriptive jobs across directions, B0/B1, three seeds, six conditions, and two alphas;
- R2: 12/12 jobs valid;
- R3: 12/12 jobs valid.

The exact requested R2 and R3 matrices are represented in the JSON file. The plan declares scientific execution false.

## 42. Tests

Added synthetic-only tests for v1 immutability, deterministic randomized APS, quantile/set construction, physical window indexing, triangular filterbank shape, SeqSleepNet forward shape and masks, finite outputs, and parameter reporting. Relevant test result: 6 passed. No scientific data was accessed for computation.

## 43. Full Validation

- v2 validator: passed;
- relevant synthetic tests: 6 passed;
- full repository test suite: `161 passed`;
- `python -m compileall -q src scripts`: passed;
- `git diff --check`: passed.

## 44. Protocol v2 Path

`configs/postreview_remediation_protocol_v2.yaml`

## 45. Protocol v2 SHA-256

`c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`

The hash is recorded in `reports/step20_1_2_remediation_protocol_v2_hash.txt` together with the unchanged v1 hash. The YAML is now immutable for this milestone.

## 46. Files Created

- `configs/postreview_remediation_protocol_v2.yaml`
- `src/shiftsleep_uq/randomized_aps.py`
- `src/shiftsleep_uq/windowing.py`
- `src/shiftsleep_uq/models/seqsleepnet_class.py`
- `scripts/validate_postreview_remediation_protocol_v2.py`
- `tests/test_step20_1_2_scaffolding.py`
- `reports/step20_1_2_execution_plan_v2.json`
- `reports/step20_1_2_remediation_protocol_v2_hash.txt`
- `reports/STEP_20_1_2_EXECUTABLE_REMEDIATION_PROTOCOL_V2_REPORT.md`

## 47. Files Modified

No historical v1 protocol, blocked Step 20.2 report, manuscript, JBHI package, dataset, partition, checkpoint, prediction, calibration, or prior scientific result was modified. The files listed in Section 46 are new scaffolding/report artifacts.

## 48. Explicitly Not Done

- no R1 scientific execution;
- no real-data windowing;
- no B0_W/B1_W training;
- no S0/S1 training;
- no scientific inference;
- no scientific conformal refit;
- no scientific bootstrap results;
- no manuscript modification;
- no submission;
- no Step 20.2.1;
- no Step 21.

## 49. Remaining Risks

The v2 protocol is executable as a contract and synthetic scaffolding, but scientific execution remains subject to runtime verification of real-data availability, GPU memory, historical artifact schema compatibility, and any technically surfaced failure under the frozen rules. Such failures must be reported without protocol improvisation. SeqSleepNet-class is a faithful PyTorch adaptation, not a claim of byte-identical reproduction. No scientific conclusion has been updated.

## 50. Recommended Next Step

# Step 20.2.1 — Execute the Frozen Remediation Protocol v2

Do NOT execute Step 20.2.1 in this step.

## 51. Git Commit

Pending milestone commit: `research: freeze executable post-review remediation protocol v2`. No scientific outputs are included.

## 52. Git Tag

Pending annotated tag: `step20-1-remediation-protocol-v2-frozen`.

Annotation: `ShiftSleep-UQ executable post-review remediation protocol v2 frozen before R1/R2/R3 execution`.

## 53. GitHub Push Status

Pending. No push has occurred in the report-generation phase.

## 54. Git Status / Diff Summary

New v2 protocol, scaffolding, validator, tests, dry-run plan, hash manifest, and this report are intended for the milestone. The four intentional historical Step 18 files and the blocked Step 20.2 report remain preserved and must not be deleted or rewritten. No scientific output namespace was created.
