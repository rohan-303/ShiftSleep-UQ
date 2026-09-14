# ShiftSleep-UQ Experimental Protocol v1.1

## Step 8.1 Amendment

**Amendment ID:** `A-08.1-01 — Independent Source-Test Partition for Known-Domain Evaluation`

**Protocol version:** `1.1.0`

**Protocol gate:** `EXPERIMENT_PROTOCOL_FROZEN`

This surgical amendment was discovered and executed before model implementation, training, predictions, calibration outputs, or performance results. No performance information influenced repartitioning. The amendment changes source-role allocation only. Cohorts, target populations, C0–C5 meanings, metrics, seeds, oracle protocol, and montage contract remain unchanged.

## 1. Frozen Cohorts

The accessible core is unchanged:

- Sleep-EDF SC: 78 subjects, 153 recordings, 414,961 valid epochs.
- Original-provider ISRUC-S1: 99 included subjects, 89,312 valid epochs.
- ISRUC structural exclusion: I040, `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`.
- ISRUC montage strata: 17 `ISRUC_A1A2`, 82 `ISRUC_M1M2`.
- Data contract: `1.2.0`.
- Preprocessing: `0.1.0`.
- SHHS: unaccessed; final benchmark gate remains `NO`.

## 2. Subject-Level Source Partition

Partition unit is `SUBJECT`. All recordings and nights belonging to one subject remain in one role.

The preserved split seed is:

```text
SPLIT_SEED = 2026
```

No alternative seeds were searched.

Source-role proportions are:

```text
TRAIN        60%
DEV          15%
CALIBRATION  10%
TEST         15%
```

### Sleep-EDF SC

No label, stage, or epoch-count stratification is used.

| Role | Subjects |
|---|---:|
| TRAIN | 47 |
| DEV | 12 |
| CALIBRATION | 8 |
| TEST | 11 |
| **Total** | **78** |

### ISRUC-S1

ISRUC is stratified only by the frozen `montage_variant` nuisance stratum. No stage distribution, label, epoch-count, model, or result information is used.

| Montage | TRAIN | DEV | CALIBRATION | TEST | Total |
|---|---:|---:|---:|---:|---:|
| ISRUC_A1A2 | 10 | 3 | 2 | 2 | 17 |
| ISRUC_M1M2 | 49 | 12 | 8 | 13 | 82 |
| **Total** | **59** | **15** | **10** | **15** | **99** |

The exact per-stratum quotas are predeclared. Stable SHA-256 ordering under seed 2026 assigns subjects within each stratum. If fractional allocation produces an exact tie, the fixed amendment priority is used: `ISRUC_A1A2` assigns CALIBRATION before TEST; `ISRUC_M1M2` assigns TEST before DEV. This produces the exact frozen quotas above.

## 3. Source Role Firewall

### TRAIN

TRAIN may be used for:

- model-weight fitting;
- source-only normalization fitting;
- predeclared training augmentation.

TRAIN may not select final checkpoints or fit calibration parameters.

### DEV

DEV may be used for:

- architecture selection;
- hyperparameter selection;
- checkpoint selection;
- early stopping.

DEV cannot fit final temperature scaling or conformal calibration.

### CALIBRATION

CALIBRATION may be used after checkpoint selection for:

- scalar source temperature scaling;
- APS conformal calibration;
- separately predeclared source-only abstention analysis.

CALIBRATION cannot update model weights or select the architecture/checkpoint.

### TEST

TEST is an untouched source population used only for final known-domain C0–C2 evaluation. TEST must not influence:

- model weights;
- normalization;
- architecture or hyperparameter selection;
- checkpoint selection;
- early stopping;
- temperature fitting;
- conformal quantiles;
- thresholds.

## 4. Evaluation Mapping

### C0–C2: Known-Domain Source-Test Evaluation

C0–C2 use the same SOURCE TEST subjects and epochs, making the comparisons paired:

- **C0:** SOURCE TEST with EEG + EOG.
- **C1:** the same SOURCE TEST subjects/epochs with synthetic EOG removal.
- **C2:** the same SOURCE TEST subjects/epochs with synthetic EEG removal.

The C0–C2 source-test population is not used for any model-development or calibration decision.

### C3–C5: Held-Out-Target Evaluation

C3–C5 use the complete held-out target population, making the comparisons paired:

- **C3:** all target subjects with EEG + EOG.
- **C4:** the same target subjects with synthetic EOG removal.
- **C5:** the same target subjects with synthetic EEG removal.

When a dataset acts as TARGET, its stored source roles are ignored.

The reciprocal directions remain:

- D1: Sleep-EDF source → complete ISRUC target.
- D2: ISRUC source → complete Sleep-EDF target.

## 5. C0–C5 Definitions

The meanings are unchanged:

- C0: `known_domain_EEG_EOG`
- C1: `known_domain_EEG_only_synthetic_no_EOG`
- C2: `known_domain_EOG_only_synthetic_no_EEG`
- C3: `unseen_domain_EEG_EOG`
- C4: `unseen_domain_EEG_only_synthetic_no_EOG`
- C5: `unseen_domain_EOG_only_synthetic_no_EEG`

Structural channel absence is not synthetic masking. Missing physiological signals are not synthesized, and alternate modalities are not substituted.

## 6. Normalization

Persisted preprocessing outputs remain unnormalized. A future model-time normalization fit estimates one global mean and standard deviation per modality from `SOURCE TRAIN ONLY`.

The frozen values are applied unchanged to:

- SOURCE TRAIN;
- SOURCE DEV;
- SOURCE CALIBRATION;
- SOURCE TEST;
- TARGET.

No TEST statistics, TARGET statistics, subject-specific fitting, or montage-specific fitting are permitted.

## 7. Calibration and Conformal Policy

Scalar temperature scaling is fitted using `SOURCE CALIBRATION ONLY` after checkpoint selection. It is evaluated on SOURCE TEST for C0–C2 and the complete TARGET for C3–C5. TEST and TARGET cannot fit temperature.

APS conformal calibration uses `SOURCE CALIBRATION ONLY`. Frozen APS is evaluated on SOURCE TEST for C0–C2 and complete TARGET for C3–C5. No TEST or TARGET conformal calibration is part of primary results.

Nominal alpha values remain 0.10 and 0.05. Coverage under domain shift is reported empirically; no transferred formal guarantee is claimed.

## 8. Interaction Contrasts

For any metric M, calculate only after model execution under this protocol:

```text
Δ_known_EEGonly  = M(C1) - M(C0)
Δ_known_EOGonly  = M(C2) - M(C0)
Δ_unseen_EEGonly = M(C4) - M(C3)
Δ_unseen_EOGonly = M(C5) - M(C3)

I_EEGonly = Δ_unseen_EEGonly - Δ_known_EEGonly
I_EOGonly = Δ_unseen_EOGonly - Δ_known_EOGonly
```

No values are calculated in Step 8.1.

Metric orientation is recorded explicitly:

- higher-is-better metrics such as macro-F1: a negative delta indicates degradation;
- lower-is-better metrics such as NLL and AURC: a positive delta indicates degradation.

## 9. Seeds and Statistics

Unchanged seeds:

- model seeds: `[17, 42, 2026]`;
- bootstrap seed: `2028`;
- bootstrap replicates: 2,000;
- subject-level percentile 95% intervals;
- paired subject bootstrap across paired conditions and model seeds.

The oracle target partition remains `reports/oracle_target_partitions_v1.csv` and is unchanged and separate from primary results.

## 10. Versioned Artifacts

New Step 8.1 artifacts:

- `configs/evaluation_protocol_v1_1.yaml`
- `reports/subject_partitions_v2.csv`
- `reports/step08_1_subject_split_audit.csv`
- `docs/experimental_protocol_v1_1.md`
- `reports/step08_1_protocol_hashes.txt`
- `reports/STEP_08_1_SOURCE_TEST_PROTOCOL_AMENDMENT_REPORT.md`
- `scripts/step_08_1_amend_source_test.py`
- `tests/test_step08_1_protocol.py`

The prior v1.0 artifacts remain preserved and are not overwritten. The oracle partition remains unchanged.

## 11. Step Boundary

Step 8.1 is protocol-only. The following remain prohibited:

- model implementation;
- training;
- normalization fitting;
- logits or prediction generation;
- ML metric calculation;
- temperature fitting;
- conformal inference;
- SHHS access;
- cohort modification;
- raw/processed data tracking;
- GitHub push.

The next possible phase remains Step 9, but Step 9 is not executed by this amendment.
