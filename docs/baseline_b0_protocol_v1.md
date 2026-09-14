# ShiftSleep-UQ Baseline B0 Protocol v1

## Status

- Baseline ID: `B0_DUAL_BRANCH_RAW_CNN`
- Human-readable name: Dual-Branch Raw-Signal CNN
- Baseline config: `configs/baseline_b0_v1.yaml`, version `1.0.0`
- Training config: `configs/training_b0_v1.yaml`, version `1.0.0`
- Upstream evaluation protocol: `configs/evaluation_protocol_v1_1.yaml`, version `1.1.0`
- Formal upstream amendment: `A-08.1-01`
- Step 9 gate: `BASELINE_PROTOCOL_FROZEN` only after implementation and validation

This is a transparent benchmark baseline, not a novel architecture and not a claim of state-of-the-art performance. No full baseline experiment is executed by Step 9.

## 1. Scientific Rationale

ShiftSleep-UQ studies reliability under dataset and missing-modality shift. B0 is intentionally compact, epoch-wise, multimodal, and auditable. EEG and EOG have independent raw-signal encoders because they have different source sampling rates and distinct physiological roles. Late concatenation keeps the fusion rule explicit. The same model/checkpoint is evaluated under all six frozen conditions for one direction and seed; C1/C2 and C4/C5 are test-time missing-modality shifts rather than separately trained models.

The design is conceptually motivated by compact raw-signal sleep-staging work such as TinySleepNet and DeepSleepNet, without claiming architectural equivalence or reproduction.

## 2. Input Contract

Each prediction corresponds to one canonical 30-second epoch:

- EEG: `[B, 1, 3000]`, 100 Hz.
- EOG: `[B, 1, 1500]`, 50 Hz.
- Modality mask: `[B, 2]`, ordered `[EEG_available, EOG_available]`.
- Allowed masks: `[1,1]`, `[1,0]`, `[0,1]`.
- `[0,0]` is forbidden and raises an error.
- Class order: `[Wake, N1, N2, N3, REM]`.

The forward pass returns raw logits and does not apply softmax.

## 3. EEG Encoder

Input `[B,1,3000]`.

Stem:

- Conv1d 1→32, kernel 51, stride 2, padding 25, bias false;
- GroupNorm(8,32);
- GELU;
- MaxPool1d(4,4).

Residual blocks:

- 32→64, kernel 7, first stride 2, second stride 1;
- 64→128, kernel 5, first stride 2, second stride 1;
- 128→128, kernel 3, first stride 2, second stride 1.

Each block uses GroupNorm after both convolutions, GELU after the first normalization and residual addition, and a projection shortcut when shape changes. AdaptiveAvgPool1d(1) produces 128 features, followed by Linear(128,128), GELU, and Dropout(0.20).

## 4. EOG Encoder

Input `[B,1,1500]`.

The architecture is conceptually identical to EEG, with an EOG-specific stem:

- Conv1d 1→32, kernel 25, stride 2, padding 12, bias false;
- GroupNorm(8,32);
- GELU;
- MaxPool1d(4,4).

Subsequent blocks are 32→64 kernel 7, 64→128 kernel 5, and 128→128 kernel 3 with the same strides, GroupNorm, GELU, pooling, projection, and dropout. EEG and EOG encoders do not share weights.

## 5. Normalization Layers

Convolutional encoders use GroupNorm. BatchNorm is not used. No batch-statistic adaptation is performed at evaluation time.

## 6. Modality Gating and Fusion

The 128-D EEG and EOG embeddings are gated deterministically:

```text
z_eeg_gated = m_eeg * z_eeg
z_eog_gated = m_eog * z_eog
```

A missing branch therefore contributes exactly zero before fusion. The numerical contents of a missing input cannot affect predictions. There is no learned missing-modality token or mask embedding.

The gated embeddings are concatenated into a 256-D vector. Modalities are not averaged, attention-weighted, or dynamically reweighted.

## 7. Classification Head

- Linear(256,128)
- GELU
- Dropout(0.30)
- Linear(128,5)

The output is raw five-class logits.

## 8. Sequence Context

B0 is strictly epoch-wise. It uses no previous or future epoch labels, recurrent context, Transformer context, neighboring target epochs as learned context, or hypnogram post-processing.

## 9. Initialization

Conv1d and Linear weights use Kaiming initialization for the nonlinear path. Biases are zero. GroupNorm weights are one and biases are zero. No pretrained or external foundation-model weights are loaded.

## 10. Training Recipe

B0 training uses complete source EEG+EOG for every SOURCE TRAIN example: mask `[1,1]`. There is no modality dropout, random removal, channel substitution, or synthetic missing-modality augmentation.

Loss is unweighted multiclass CrossEntropyLoss with `weight=None` and `label_smoothing=0.0`.

Sampling is one natural epoch-level pass over all SOURCE TRAIN epochs, shuffled deterministically per epoch. Subjects, stages, montages, and recordings are not balanced.

Optimizer: AdamW with learning rate `3e-4`, weight decay `1e-4`, betas `(0.9,0.999)`, and epsilon `1e-8`.

Learning rate schedule: none; constant learning rate.

Precision: FP32.

Physical and effective batch size: 128. No gradient accumulation by default. A future execution that cannot hold batch 128 must stop with `BASELINE_BATCH_MEMORY_BLOCKED`, not silently alter the protocol.

Global gradient norm clipping: `1.0`.

Augmentation: none.

Maximum epochs: 30. Minimum epochs before early stopping: 5. Patience: 6.

## 11. Checkpoint Selection

Checkpoint selection uses SOURCE DEV macro-F1 only, with frozen tie-breaks:

1. higher SOURCE DEV macro-F1;
2. lower SOURCE DEV NLL when macro-F1 differs by no more than `1e-6`;
3. earlier epoch when both metrics are equal within tolerance.

Patience counts consecutive epochs without checkpoint replacement. Target, TEST, and CALIBRATION information cannot influence stopping or checkpoint choice.

## 12. Source-Only Normalization

The implemented streaming fitter accepts only role `TRAIN` and rejects DEV, CALIBRATION, TEST, and TARGET. It computes one global scalar mean and standard deviation per modality using a numerically stable streaming update, rejects non-finite values, and uses `std_epsilon=1e-8`.

Step 9 implements and tests the mechanism only. No real normalization values are fitted or saved. Future Step 10 will fit SOURCE TRAIN values once per direction and apply them unchanged to TRAIN, DEV, CALIBRATION, TEST, and TARGET. Synthetically missing normalized inputs will be zeroed and gated.

## 13. Condition Mapping

- C0: SOURCE TEST, mask `[1,1]`
- C1: SOURCE TEST, mask `[1,0]`
- C2: SOURCE TEST, mask `[0,1]`
- C3: complete TARGET, mask `[1,1]`
- C4: complete TARGET, mask `[1,0]`
- C5: complete TARGET, mask `[0,1]`

One checkpoint is evaluated across all six conditions for one direction and seed. No condition-specific retraining, normalization, or checkpoint is permitted.

## 14. Dataset and Role Firewall

The training entrypoint accepts frozen `experiment_id` values rather than arbitrary source/target filenames:

- D1 training source: Sleep-EDF TRAIN; DEV: Sleep-EDF DEV.
- D2 training source: ISRUC TRAIN; DEV: ISRUC DEV.

Role-gated dataset access rejects CALIBRATION, TEST, and TARGET for optimizer training. Normalization fitting requires TRAIN. Calibration, TEST, and TARGET access are separate future execution boundaries.

## 15. Reproducibility

The seed utility sets Python random, `PYTHONHASHSEED`, NumPy, PyTorch CPU, and CUDA seeds. Deterministic PyTorch algorithms are enabled where supported, with cuDNN deterministic mode and benchmarking disabled.

Data-loader epoch generators are derived deterministically from model seed and epoch. Validation is unshuffled. Worker seed initialization is provided.

Frozen model seeds: `[17, 42, 2026]`.

Future full execution requires exactly six trained checkpoints: two directions × three seeds.

## 16. Artifact Contract

Future checkpoints use:

```text
artifacts/models/b0/<experiment_id>/seed_<seed>/
```

Potential future contents are `best.pt`, `training_history.json`, `normalization.json`, and `run_manifest.json`. These remain Git-ignored. Checkpoint metadata records baseline/config/protocol/data/preprocessing hashes, source dataset, seed, selected epoch, DEV metrics, versions, device, and git commit, without TARGET metrics.

Step 9 creates no trained checkpoint.

## 17. Explicit Step Boundary

Step 9 implements and validates infrastructure only. It does not:

- run the six full experiments;
- fit real normalization;
- save trained checkpoints;
- generate target predictions;
- calculate C0–C5 performance;
- fit temperature scaling;
- execute conformal inference;
- access SHHS.

Step 10 will execute B0 source training for D1 and D2 across seeds 17, 42, and 2026, fit SOURCE TRAIN normalization, use SOURCE DEV only for checkpoint selection, and stop before TEST/TARGET evaluation.
