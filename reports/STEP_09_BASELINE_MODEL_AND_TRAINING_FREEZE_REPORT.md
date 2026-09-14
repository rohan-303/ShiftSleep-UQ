# ShiftSleep-UQ Step 9 Baseline Model and Training Freeze Report

## 1. Status

COMPLETE

Step 9 was executed only. The primary B0 architecture, training recipe, leak-safe infrastructure, tests, hashes, and protocol documentation are frozen. The six full baseline experiments were not run.

## 2. Baseline Gate

BASELINE_PROTOCOL_FROZEN

## 3. Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Required upstream commit verified: `bcbc20c research: add independent source test protocol`
- Upstream protocol commit exists locally.
- No GitHub push was performed.
- The worktree was clean before Step 9 implementation.
- Step 9 changes are committed locally at the end of this task with commit message `ml: freeze and implement B0 baseline`.

## 4. Frozen Upstream Protocol

- Authoritative path: `configs/evaluation_protocol_v1_1.yaml`
- Protocol version: `1.1.0`
- Amendment: `A-08.1-01`
- Protocol gate: `EXPERIMENT_PROTOCOL_FROZEN`
- SHA-256: `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`
- Split seed: `2026`
- Source roles: `TRAIN`, `DEV`, `CALIBRATION`, `TEST`
- C0–C2 population: untouched `SOURCE TEST`
- C3–C5 population: complete held-out `TARGET`
- The authoritative protocol file was read and verified unchanged during Step 9.

## 5. Baseline Identity

- Baseline ID: `B0_DUAL_BRANCH_RAW_CNN`
- Human-readable name: `Dual-Branch Raw-Signal CNN`
- Role: transparent benchmark baseline
- Novelty claim: none
- Literature motivation is limited to the general compact raw-signal sleep-staging family; B0 is not claimed to reproduce TinySleepNet, DeepSleepNet, or any other published architecture.

## 6. Scientific Rationale

B0 is an epoch-wise, dual-branch raw-signal CNN selected for auditability and reliability-under-shift analysis. EEG and EOG receive independent encoders because their sampling rates and signal characteristics differ. Late concatenation keeps modality contributions explicit. The model contains no learned missing-modality token, no attention-based reliability mechanism, no temporal context, and no architecture search. The same architecture and training recipe will be used for both reciprocal directions and all six conditions.

## 7. Input Contract

One prediction corresponds to one canonical 30-second epoch.

- EEG input: `[B, 1, 3000]`, 100 Hz
- EOG input: `[B, 1, 1500]`, 50 Hz
- Availability mask: `[B, 2]`, order `[EEG_available, EOG_available]`
- Class order: `[Wake, N1, N2, N3, REM]`
- Forward output: raw logits `[B, 5]`
- Softmax is not applied inside the model.
- `[0, 0]` is rejected.

## 8. EEG Encoder

The independent EEG branch is frozen as:

- Stem: `Conv1d(1, 32, kernel_size=51, stride=2, padding=25, bias=False)`
- `GroupNorm(8, 32)`, GELU, `MaxPool1d(4, 4)`
- Residual block 1: `32 -> 64`, kernel 7, first stride 2
- Residual block 2: `64 -> 128`, kernel 5, first stride 2
- Residual block 3: `128 -> 128`, kernel 3, first stride 2
- GroupNorm follows each convolution.
- GELU follows the first normalization and residual addition.
- Projection shortcuts are used when shape or channel count changes.
- `AdaptiveAvgPool1d(1)` and flattening produce 128 features.
- Projection: `Linear(128, 128)`, GELU, Dropout 0.20
- Final EEG embedding: 128-D

## 9. EOG Encoder

The independent EOG branch uses the same conceptual architecture but preserves the 50 Hz input contract:

- Stem: `Conv1d(1, 32, kernel_size=25, stride=2, padding=12, bias=False)`
- `GroupNorm(8, 32)`, GELU, `MaxPool1d(4, 4)`
- Residual blocks: `32 -> 64` kernel 7, `64 -> 128` kernel 5, `128 -> 128` kernel 3
- The first convolution of each residual block has stride 2; the second has stride 1.
- GroupNorm, GELU, adaptive pooling, projection, and dropout match the EEG branch.
- Final EOG embedding: 128-D
- EEG and EOG encoder weights are not shared.

## 10. Modality Gating

The model validates binary masks with shape `[B, 2]` or `[2]`, rejects unknown values, and rejects `[0, 0]`.

The implementation computes:

- `z_eeg_gated = m_eeg * z_eeg`
- `z_eog_gated = m_eog * z_eog`

The unavailable branch is multiplied to exactly zero before fusion. No learned mask embedding or missing-modality token is used. Unit tests verify that changing the numerical contents of a missing EOG or EEG tensor cannot change logits.

## 11. Fusion

The two gated 128-D embeddings are concatenated into a 256-D vector. Modalities are not averaged, attention-weighted, or dynamically reweighted.

## 12. Classification Head

- `Linear(256, 128)`
- GELU
- Dropout 0.30
- `Linear(128, 5)`
- Output: raw five-class logits only

## 13. Parameter Count

Exact trainable parameter count: **654,597**.

A regression test freezes this count to detect accidental architecture drift.

## 14. Sequence Context Policy

NONE.

B0 is strictly epoch-wise. It uses no previous or future epoch labels, recurrent state, Transformer context, neighboring target epochs as learned context, or hypnogram transition post-processing.

## 15. Training Modality Policy

FULL EEG+EOG ONLY.

Every SOURCE TRAIN example uses mask `[1, 1]`. No modality dropout, random modality removal, channel substitution, or missing-channel augmentation is implemented for B0. C1/C2/C4/C5 remain genuine test-time missing-modality shifts.

## 16. Loss

Standard unweighted multiclass cross-entropy:

- `CrossEntropyLoss(weight=None, label_smoothing=0.0)`
- No focal loss
- No class weighting
- No target-derived priors
- No label smoothing

## 17. Sampling / Class-Balance Policy

One training epoch is one pass through all available SOURCE TRAIN epochs with natural epoch-level sampling. Training epochs are shuffled deterministically per seed and epoch. No stage, subject, montage, recording, oversampling, undersampling, or weighted sampling is used.

## 18. Optimizer

AdamW with:

- betas `(0.9, 0.999)`
- epsilon `1e-8`
- weight decay `1e-4`

## 19. Learning Rate

- Learning rate: `3e-4`
- Schedule: NONE
- The primary baseline uses a constant learning rate.

## 20. Precision

FP32.

AMP and mixed precision are not used by the primary baseline.

## 21. Batch Size

- Physical batch size: `128`
- Effective batch size: `128`
- Gradient accumulation: none by default

The training entrypoint does not silently alter this value. A future verified memory failure requires a protocol amendment and must not be handled by implicit batch-size reduction.

## 22. Training Budget

- Maximum epochs: `30`
- Minimum epochs before early stopping: `5`
- Gradient clipping: global norm `1.0`
- Training history fields include epoch, TRAIN cross-entropy, DEV macro-F1, DEV NLL, learning rate, gradient norm summary, checkpoint-selected flag, and elapsed training seconds.

## 23. Early Stopping

- Patience: `6`
- Patience counts consecutive epochs without checkpoint replacement.
- Early stopping cannot terminate before epoch 5.
- No TEST or TARGET metric is available to stopping logic.

## 24. Checkpoint Selection

Selection uses SOURCE DEV only and follows the frozen lexicographic rule:

1. higher DEV macro-F1;
2. within `1e-6` macro-F1 equality, lower DEV NLL;
3. within `1e-6` equality for both, earlier epoch.

The `CheckpointSelector` implementation and patience behavior are unit-tested. Target metrics are not accepted by the selector.

## 25. Augmentation

NONE.

No time shifting, amplitude jitter, Gaussian noise, frequency masking, MixUp, CutMix, SpecAugment, or modality dropout is used.

## 26. Normalization Implementation

SOURCE TRAIN ONLY.

A streaming Welford-style fitter was implemented separately for EEG and EOG. It:

- requires role `TRAIN` programmatically;
- rejects DEV, CALIBRATION, TEST, and TARGET fitting attempts;
- rejects non-finite source values;
- computes a global scalar mean and population standard deviation over source training samples;
- uses `std_epsilon = 1e-8`;
- applies frozen parameters unchanged through the dataset interface once Step 10 executes.

No real normalization values were fitted or saved in Step 9.

## 27. Condition Mask Mapping

| Condition | Population | Mask |
|---|---|---|
| C0 | SOURCE TEST | `[1, 1]` |
| C1 | SOURCE TEST | `[1, 0]` |
| C2 | SOURCE TEST | `[0, 1]` |
| C3 | complete TARGET | `[1, 1]` |
| C4 | complete TARGET | `[1, 0]` |
| C5 | complete TARGET | `[0, 1]` |

Unknown condition IDs and `[0, 0]` are rejected. No condition-specific checkpoint, retraining, normalization, or method selection is implemented.

## 28. Experiment Count

Six future trained checkpoints:

- D1 `D1_SLEEPEDF_TO_ISRUC`, seeds `17`, `42`, `2026`
- D2 `D2_ISRUC_TO_SLEEPEDF`, seeds `17`, `42`, `2026`

Each direction/seed produces one selected checkpoint evaluated across all six conditions. No condition-specific model is trained.

## 29. Target-Free Loader Guards

The training entrypoint takes `experiment_id` and resolves the source dataset from the frozen direction mapping:

- D1 optimizer data: Sleep-EDF TRAIN only
- D1 DEV data: Sleep-EDF DEV only
- D2 optimizer data: ISRUC TRAIN only
- D2 DEV data: ISRUC DEV only

Role guards reject SOURCE DEV, CALIBRATION, TEST, and TARGET as optimizer data. CALIBRATION and TEST roles are reserved for later stages, and TARGET observations are not exposed by the Step 9 training loader. The permitted Step 9 real-data smoke loaded only one batch from each SOURCE TRAIN population.

## 30. Reproducibility

Implemented utilities set:

- Python `random`
- NumPy seed
- PyTorch CPU seed
- PyTorch CUDA seeds
- deterministic PyTorch algorithms where supported
- deterministic cuDNN behavior where applicable
- deterministic per-epoch DataLoader generators derived from model seed plus epoch
- deterministic worker initialization support

No data augmentation randomness exists in B0.

## 31. Environment

Recorded live environment:

- OS: Windows 10 host
- Python: `3.11.15`
- PyTorch: `2.14.0+cu126`
- NumPy: `2.4.3`
- CUDA available: `True`
- CUDA runtime: `12.6`
- cuDNN: `91002`
- GPU: `NVIDIA GeForce RTX 3060 Laptop GPU`
- CPU fallback remains supported for tests.

PyTorch was installed through the official PyTorch CUDA 12.6 wheel index because it was absent before Step 9. No unrelated ML framework was installed. Ruff was installed only to run repository quality checks.

## 32. Model Config

- Path: `configs/baseline_b0_v1.yaml`
- Version: `1.0.0`
- SHA-256: `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`

The config encodes input lengths, sampling rates, branch channels and kernels, residual blocks, GroupNorm, embeddings, gating, fusion, head, dropout, class count, initialization, and no sequence context.

## 33. Training Config

- Path: `configs/training_b0_v1.yaml`
- Version: `1.0.0`
- SHA-256: `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7`

The config encodes optimizer, learning rate, weight decay, loss, batch size, FP32, gradient clipping, epoch budget, patience, minimum epochs, selection rule, seeds, augmentation `NONE`, training mask `[1, 1]`, class weighting `NONE`, scheduler `NONE`, and normalization epsilon.

## 34. Baseline Protocol Document

- Path: `docs/baseline_b0_protocol_v1.md`
- SHA-256: `dea145bb27fc61325c5c79653c625233bd107eb689d12e8d13fa65e8a71ca4df`

The document explains the scientific rationale, modality branches, late fusion, GroupNorm, no-context policy, unweighted CE, no augmentation or balancing, complete-modality training, missing-modality evaluation, target-free boundaries, and Step 10 scope.

## 35. Tests Added

Added `tests/test_step09_baseline.py` with ten focused tests covering:

- B=1 and B>1 model shapes;
- exact condition masks and invalid mask/condition rejection;
- missing-branch invariance;
- streaming normalization and role firewall;
- source training loader role firewall;
- lexicographic checkpoint selection;
- patience and minimum-epoch behavior;
- deterministic initialization and forward behavior;
- deterministic optimization step;
- exact parameter count and explicit config values.

The complete repository test suite passed with `86 passed`.

## 36. Missing-Branch Invariance Test

PASS.

With mask `[1, 0]`, drastically changing EOG values leaves logits unchanged within strict tolerance. With mask `[0, 1]`, changing EEG values leaves logits unchanged within strict tolerance. Gating occurs after branch encoding and before fusion, and the masked embedding is exactly zero.

## 37. Normalization Firewall Test

PASS.

Synthetic streaming moments match the analytically known mean and population standard deviation. Fitting accepts `TRAIN` and rejects `DEV`, `CALIBRATION`, `TEST`, and `TARGET`. No real normalization artifact exists.

## 38. Training Firewall Test

PASS.

The optimizer dataset path accepts only SOURCE TRAIN. SOURCE DEV, SOURCE CALIBRATION, SOURCE TEST, and TARGET are rejected for training. DEV access is evaluation-only.

## 39. Checkpoint Selection Test

PASS.

Tests cover higher macro-F1, lower NLL within the `1e-6` macro-F1 tolerance, earlier epoch on full ties, and patience behavior with the minimum five-epoch rule.

## 40. Determinism Test

PASS.

Same-seed B0 initialization produces equal parameter hashes. Evaluation-mode forward outputs match. Identical CPU optimization steps produce equal resulting parameter hashes under deterministic support.

## 41. Real-Data Read-Only Smoke

PASS.

Exactly one SOURCE TRAIN batch was loaded from each direction’s source interface:

- Sleep-EDF SOURCE TRAIN: shapes `[B, 1, 3000]` and `[B, 1, 1500]`, finite values, valid labels, source metadata, role `TRAIN`.
- ISRUC SOURCE TRAIN: shapes `[B, 1, 3000]` and `[B, 1, 1500]`, finite values, valid labels, source metadata, role `TRAIN`.

This was an interface-only check. No dataset-level normalization, DEV inspection, TEST inspection, TARGET inspection, performance metric, prediction, or training epoch was performed.

## 42. Synthetic Forward/Backward Smoke

PASS on CPU and available CUDA device.

The smoke path exercised forward pass, unweighted CE loss, backward pass, global gradient clipping, and optimizer step. Logits, loss, gradients, and updated parameters were finite, and parameters changed. The smoke used synthetic tensors only and its numerical loss was not interpreted.

## 43. Validation

Actual validation results:

- `pytest -q`: **86 passed in 15.32s**
- `PYTHONPATH=src python -m compileall -q src tests scripts`: PASS
- Step 9-only Ruff check: PASS
- `git diff --check`: PASS
- Step 8.1 authoritative protocol hash: unchanged and verified as `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`
- Source partition, oracle partition, and frozen cohort files: unchanged
- Required upstream commit: verified
- Repository-wide Ruff: not clean because 97 pre-existing findings remain in older Step 4–8 files; no prior files were modified to mask those findings
- No full baseline experiment was run

## 44. Files Created

- `configs/baseline_b0_v1.yaml`
- `configs/training_b0_v1.yaml`
- `docs/baseline_b0_protocol_v1.md`
- `reports/step09_baseline_protocol_hashes.txt`
- `reports/STEP_09_BASELINE_MODEL_AND_TRAINING_FREEZE_REPORT.md`
- `scripts/train_b0.py`
- `src/shiftsleep_uq/models/__init__.py`
- `src/shiftsleep_uq/models/baseline_b0.py`
- `src/shiftsleep_uq/training/__init__.py`
- `src/shiftsleep_uq/training/checkpointing.py`
- `src/shiftsleep_uq/training/datasets.py`
- `src/shiftsleep_uq/training/engine.py`
- `src/shiftsleep_uq/training/normalization.py`
- `src/shiftsleep_uq/training/reproducibility.py`
- `tests/test_step09_baseline.py`

## 45. Files Modified

- `pyproject.toml`: added the pinned PyTorch compatibility range `torch>=2.14,<2.15`.

No frozen Step 8.1 protocol, cohort, source partition, oracle partition, raw data, processed data, or prior research artifact was modified.

## 46. Explicitly Not Done

The following were not performed:

- no full model training;
- no six baseline experiments;
- no real normalization fit;
- no saved trained checkpoint;
- no DEV model-selection run;
- no calibration fitting;
- no TEST prediction;
- no TARGET prediction;
- no C0–C5 metrics;
- no uncertainty metrics;
- no conformal evaluation;
- no SHHS access;
- no cohort change;
- no protocol amendment;
- no raw or processed data committed;
- no GitHub push.

## 47. Remaining Pre-Experiment Issues

NONE for the frozen Step 9 protocol and implementation gate.

The repository-wide legacy Ruff findings are pre-existing quality debt outside the Step 9 scope and do not block the tested B0 implementation. They were not modified because doing so would alter earlier frozen work.

## 48. Recommended Next Step

# Step 10 — Execute B0 Source Training for D1 and D2 Across the Three Frozen Seeds

Step 10 should fit SOURCE TRAIN normalization, train the six checkpoints, use SOURCE DEV only for checkpoint selection, and STOP before TEST/TARGET evaluation.

Step 10 was not executed here.

## 49. Git Status / Diff Summary

Step 9 changes were committed locally with:

`ml: freeze and implement B0 baseline`

No push was performed. The final repository state after the local commit is clean on branch `main`. The commit contains only the B0 model/training infrastructure, configs, tests, protocol document, hash manifest, report, and the PyTorch project dependency declaration.
