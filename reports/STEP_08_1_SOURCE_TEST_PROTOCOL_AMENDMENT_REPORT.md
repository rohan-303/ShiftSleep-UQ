# ShiftSleep-UQ Step 8.1 Source-Test Protocol Amendment Report

## 1. Protocol Status

`EXPERIMENT_PROTOCOL_FROZEN`

Protocol version: `1.1.0`.

Formal amendment: `A-08.1-01 — Independent Source-Test Partition for Known-Domain Evaluation`.

This is a surgical pre-model amendment. No model was implemented or trained. No predictions, logits, calibration outputs, conformal outputs, performance metrics, or model-derived information existed or influenced the repartitioning.

## 2. Amendment Scope

The amendment changes source-role allocation only:

```text
OLD: TRAIN 70% / DEV 15% / CALIBRATION 15%
NEW: TRAIN 60% / DEV 15% / CALIBRATION 10% / TEST 15%
```

Preserved unchanged:

- frozen cohorts;
- target populations;
- C0–C5 meanings;
- metrics;
- seeds;
- oracle protocol;
- ISRUC montage contract;
- data contract `1.2.0`;
- preprocessing `0.1.0`;
- target-free firewall.

## 3. Frozen Cohorts

### Sleep-EDF SC

- Subjects: 78
- Recordings: 153
- Valid epochs: 414,961

### Original-provider ISRUC-S1

- Included subjects: 99
- Valid epochs: 89,312
- Structural exclusion: I040, `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`
- `ISRUC_A1A2`: 17 subjects
- `ISRUC_M1M2`: 82 subjects

SHHS was not accessed. `FINAL_BENCHMARK_GATE = NO` remains unchanged.

## 4. Partition Unit and Seed

Partition unit: `SUBJECT`.

```text
SPLIT_SEED = 2026
```

No alternative seeds were searched.

All recordings and nights belonging to one subject remain in one source role.

## 5. Required Source Role Counts

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

ISRUC is stratified only by frozen `montage_variant`.

| Montage | TRAIN | DEV | CALIBRATION | TEST | Total |
|---|---:|---:|---:|---:|---:|
| ISRUC_A1A2 | 10 | 3 | 2 | 2 | 17 |
| ISRUC_M1M2 | 49 | 12 | 8 | 13 | 82 |
| **Total** | **59** | **15** | **10** | **15** | **99** |

The deterministic constrained quota table is predeclared in `configs/evaluation_protocol_v1_1.yaml`. Stable SHA-256 subject ordering under seed 2026 assigns subjects within each stratum. The fixed exact-tie rule is documented in the YAML: `ISRUC_A1A2` gives priority to CALIBRATION before TEST; `ISRUC_M1M2` gives priority to TEST before DEV. No stage distribution, model information, epoch count, target information, or performance result is used.

Total source rows: 177.

## 6. Evaluation Mapping

### C0–C2: SOURCE TEST

C0–C2 use the same untouched SOURCE TEST subjects and epochs:

- C0: SOURCE TEST with EEG + EOG.
- C1: the same SOURCE TEST subjects/epochs with synthetic EOG removal.
- C2: the same SOURCE TEST subjects/epochs with synthetic EEG removal.

C0, C1, and C2 are paired evaluations.

### C3–C5: COMPLETE TARGET

C3–C5 use the complete held-out target population:

- C3: all target subjects with EEG + EOG.
- C4: the same target subjects with synthetic EOG removal.
- C5: the same target subjects with synthetic EEG removal.

C3, C4, and C5 are paired evaluations. Stored source roles are ignored when that dataset acts as TARGET.

Reciprocal directions remain:

- D1: Sleep-EDF source → complete ISRUC target.
- D2: ISRUC source → complete Sleep-EDF target.

## 7. Source Role Firewall

### TRAIN

May fit model weights and source-only normalization. It may not select the final checkpoint or fit calibration parameters.

### DEV

May select architecture, hyperparameters, checkpoint, and early stopping. It may not fit final temperature scaling or conformal calibration.

### CALIBRATION

May fit scalar temperature scaling and APS conformal calibration after checkpoint selection. It may not update weights or select the architecture/checkpoint.

### TEST

May only be used for final known-domain C0–C2 evaluation. TEST cannot influence:

- model weights;
- normalization;
- architecture or hyperparameter selection;
- checkpoint selection;
- early stopping;
- temperature fitting;
- conformal quantiles;
- thresholds.

## 8. Normalization

Existing Step 8 normalization policy is preserved.

Fit one global mean and standard deviation per modality using `SOURCE TRAIN ONLY`. Apply unchanged to TRAIN, DEV, CALIBRATION, TEST, and TARGET.

No TEST statistics, TARGET statistics, subject-specific fitting, or montage-specific fitting are permitted.

No normalization parameters were fitted in Step 8.1.

## 9. Calibration

Scalar temperature scaling is fitted using `SOURCE CALIBRATION ONLY` after checkpoint selection.

It is evaluated on:

- SOURCE TEST for C0–C2;
- complete TARGET for C3–C5.

TEST and TARGET cannot fit temperature scaling.

## 10. Conformal Protocol

APS remains the primary conformal method, using `SOURCE CALIBRATION ONLY`.

Frozen APS is evaluated on:

- SOURCE TEST for C0–C2;
- complete TARGET for C3–C5.

No TEST or TARGET conformal calibration is used in primary results. Alpha values remain 0.10 and 0.05. Coverage under shift is empirical; no transferred formal guarantee is claimed.

## 11. C0–C5 Definitions

The definitions are unchanged:

- C0: `known_domain_EEG_EOG`
- C1: `known_domain_EEG_only_synthetic_no_EOG`
- C2: `known_domain_EOG_only_synthetic_no_EEG`
- C3: `unseen_domain_EEG_EOG`
- C4: `unseen_domain_EEG_only_synthetic_no_EOG`
- C5: `unseen_domain_EOG_only_synthetic_no_EEG`

## 12. Interaction Contrasts

For any metric M, the following contrasts are frozen but not calculated in Step 8.1:

```text
Δ_known_EEGonly  = M(C1) - M(C0)
Δ_known_EOGonly  = M(C2) - M(C0)
Δ_unseen_EEGonly = M(C4) - M(C3)
Δ_unseen_EOGonly = M(C5) - M(C3)

I_EEGonly = Δ_unseen_EEGonly - Δ_known_EEGonly
I_EOGonly = Δ_unseen_EOGonly - Δ_known_EOGonly
```

For higher-is-better metrics such as macro-F1, a negative delta indicates degradation. For lower-is-better metrics such as NLL and AURC, a positive delta indicates degradation.

No metric values were calculated.

## 13. Oracle Protocol

`reports/oracle_target_partitions_v1.csv` was preserved unchanged and remains separate from primary results.

Oracle target calibration remains an explicitly labeled upper bound and cannot influence target-free model selection or primary results.

## 14. Versioned Artifacts Created

- `configs/evaluation_protocol_v1_1.yaml`
- `reports/subject_partitions_v2.csv`
- `reports/step08_1_subject_split_audit.csv`
- `docs/experimental_protocol_v1_1.md`
- `reports/step08_1_protocol_hashes.txt`
- `reports/STEP_08_1_SOURCE_TEST_PROTOCOL_AMENDMENT_REPORT.md`
- `scripts/step_08_1_amend_source_test.py`
- `tests/test_step08_1_protocol.py`

The prior Step 8 v1.0 artifacts were not overwritten.

## 15. Artifact Hashes

```text
configs/evaluation_protocol_v1_1.yaml,dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756
reports/subject_partitions_v2.csv,9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329
reports/step08_1_subject_split_audit.csv,ce3388a01d43dad17cf5a8e560c30974cd05502437556fda3ecba6a6e2b1d486
docs/experimental_protocol_v1_1.md,8ffa565df7873352d0abfcadcec1b3bdf6635f201f9af600e1028ea68beb8cba
reports/oracle_target_partitions_v1.csv,835344bcbd1992b00ec309082317d7f08a0b7f5f6c8d401ee670627d6bd806de
```

## 16. Validation

Focused Step 8.1 tests:

```text
pytest -q tests/test_step08_1_protocol.py
5 passed in 0.14s
```

The tests require:

1. 177 source rows;
2. exactly TRAIN, DEV, CALIBRATION, TEST roles;
3. Sleep-EDF 47/12/8/11 counts;
4. ISRUC 59/15/10/15 counts;
5. exact ISRUC montage allocations;
6. no subject overlap;
7. SOURCE TEST for C0–C2;
8. COMPLETE TARGET for C3–C5;
9. TEST firewall restrictions;
10. unchanged C0–C5 definitions;
11. unchanged/separate oracle artifact;
12. reproducible protocol hashes.

Required final validation:

```text
pytest -q
76 passed in 10.12s

PYTHONPATH=src python -m compileall -q src tests scripts
PASS

git diff --check
PASS

Step 8.1 artifact, hash, cohort, oracle, and tracking checks
PASS
```

The validation confirmed Sleep-EDF rows = 78, ISRUC rows = 99, total rows = 177, four source roles, no role overlap, SOURCE TEST mapping for C0–C2, COMPLETE TARGET mapping for C3–C5, reproducible protocol hashes, unchanged oracle artifact, no model artifacts or predictions, no fitted normalization, and no raw/processed data tracked.

## 17. Explicitly Not Done

- no model implementation;
- no training;
- no normalization fitting;
- no logits or predictions;
- no ML metrics;
- no temperature fitting;
- no conformal inference;
- no SHHS access;
- no cohort modification;
- no raw/processed data tracked;
- no GitHub push;
- no Step 9 execution.

## 18. Final Gate

`EXPERIMENT_PROTOCOL_FROZEN`

The amended protocol is frozen under version `1.1.0`. The next possible phase is Step 9, but Step 9 is not executed by this task.
