# ShiftSleep-UQ Step 8 Experiment Protocol Freeze Report

## 1. Status

`COMPLETE`

Step 8 froze the subject-level experimental protocol before model implementation, training, prediction, calibration fitting, conformal execution, or ML evaluation.

## 2. Protocol Gate

`EXPERIMENT_PROTOCOL_FROZEN`

## 3. Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Preflight working tree: clean
- Step 7.11 freeze commit verified: `4447a52 data: freeze original ISRUC and accessible PSG core`
- Final Step 8 changes were committed locally after validation.
- No GitHub push was performed.
- No existing model outputs, predictions, checkpoints, logits, embeddings, or fitted normalization artifacts were found before Step 8.

## 4. Frozen Cohort Inputs

### Sleep-EDF SC

- Subjects: 78
- Recordings: 153
- Valid epochs: 414,961
- Manifest: `reports/core_recording_manifest_v1_1.csv`
- Manifest SHA-256: `417286a0b5562c80693c4c410f64b3dcf773c8328568f5123deecca34c92a806`

### ISRUC-S1

- Expected subjects: 100
- Terminally accounted: 100
- Included subjects: 99
- Structural exclusions: 1, I040
- Included recordings: 99
- Valid epochs: 89,312
- Montage counts: 17 `ISRUC_A1A2`, 82 `ISRUC_M1M2`
- Cohort config: `configs/isruc_original_cohort_v3.yaml`
- Config SHA-256: `af4fb75be97df99443d5b7bc42d8f49bd55440702d07dffd49563356f7cece9d`

### Contracts

- Data contract: `1.2.0`
- Preprocessing: `0.1.0`
- Accessible core config: `configs/core_cohort_v2.yaml`
- Accessible core config SHA-256: `e8dbc91b04b4b54797e8d83be1866b28674fa2587e31507f94b3583e1f24f9ae`

## 5. Experiment Directions

### D1 — `D1_SLEEPEDF_TO_ISRUC`

- Source: Sleep-EDF SC TRAIN/DEV/CALIBRATION subjects
- Target: all 99 included ISRUC-S1 subjects
- Target adaptation: forbidden
- Target labels and observations are unavailable to source fitting, normalization, checkpoint selection, hyperparameter selection, calibration, threshold selection, conformal calibration, and adaptation.

### D2 — `D2_ISRUC_TO_SLEEPEDF`

- Source: ISRUC-S1 TRAIN/DEV/CALIBRATION subjects
- Target: all 78 included Sleep-EDF SC subjects
- Target adaptation: forbidden
- Target labels and observations are unavailable to source fitting, normalization, checkpoint selection, hyperparameter selection, calibration, threshold selection, conformal calibration, and adaptation.

The stored source role is ignored when a dataset acts as the complete held-out target.

## 6. Future SHHS Extension

SHHS remains unaccessed and is not fabricated. When validated, use leave-one-dataset-out domain generalization: source pool equals all other validated primary datasets and target equals the entirety of the frozen target dataset. Existing Sleep-EDF and ISRUC partitions must not be reshuffled because SHHS becomes available. SHHS uses the same deterministic subject-level partition algorithm, without performance-driven repartitioning.

## 7. Source Split Rule

Partition unit: `SUBJECT`.

Roles and nominal proportions:

- TRAIN: 70%
- DEV: 15%
- CALIBRATION: 15%

Allocation uses deterministic largest-remainder rounding with fixed role order TRAIN, DEV, CALIBRATION. Sleep-EDF is assigned without label/stage stratification and all nights remain grouped. ISRUC is stratified only by the frozen `montage_variant` acquisition nuisance stratum. Epoch totals do not influence assignment.

## 8. Source Partition Counts

Manifest: `reports/subject_partitions_v1.csv`.

| Dataset | TRAIN | DEV | CALIBRATION | Total |
|---|---:|---:|---:|---:|
| Sleep-EDF SC | 54 | 12 | 12 | 78 |
| ISRUC-S1 | 70 | 15 | 14 | 99 |
| Total | 124 | 27 | 26 | 177 |

ISRUC montage counts:

| Source role | ISRUC_A1A2 | ISRUC_M1M2 | Total |
|---|---:|---:|---:|
| TRAIN | 12 | 58 | 70 |
| DEV | 3 | 12 | 15 |
| CALIBRATION | 2 | 12 | 14 |
| Total | 17 | 82 | 99 |

The 14-subject ISRUC calibration count is the deterministic largest-remainder result within the two montage strata; no balancing adjustment was made.

The split audit is `reports/step08_subject_split_audit.csv` and contains six dataset × role rows. Audit epoch totals are descriptive only:

- ISRUC TRAIN: 70 subjects, 70 recordings, 62,915 epochs
- ISRUC DEV: 15 subjects, 15 recordings, 13,718 epochs
- ISRUC CALIBRATION: 14 subjects, 14 recordings, 12,679 epochs
- Sleep-EDF TRAIN: 54 subjects, 107 recordings, 291,078 epochs
- Sleep-EDF DEV: 12 subjects, 23 recordings, 60,805 epochs
- Sleep-EDF CALIBRATION: 12 subjects, 23 recordings, 63,078 epochs

## 9. Split Seed

`SPLIT_SEED = 2026`.

Repository preflight found no previously frozen valid split seed. No multiple-seed search was performed.

## 10. Target Evaluation Rule

Primary target evaluation uses every included subject in the held-out target dataset:

- D1: all 99 ISRUC-S1 subjects
- D2: all 78 Sleep-EDF SC subjects

The source-role field in the stable partition manifest is ignored for that direction’s target dataset.

## 11. Target-Free Firewall

Before primary target evaluation, target labels, raw signal distributions, normalization statistics, class/stage frequencies, target montage distribution for tuning, feature/representation statistics, calibration statistics, uncertainty statistics, thresholds, conformal scores, and target error rates are prohibited.

Intrinsic frozen-contract metadata, including exact montage identity, may be retained for analysis but may not tune the model. Target-test-label scaling, target-adaptive normalization, subject-specific target normalization, record-specific target z-scoring, montage-specific normalization, and target-domain recentering are prohibited.

## 12. Normalization Policy

Persisted preprocessing outputs remain unnormalized. Future model-time normalization fits one global mean and standard deviation per modality from SOURCE TRAIN only, freezes them, and applies them unchanged to SOURCE TRAIN, SOURCE DEV, SOURCE CALIBRATION, and TARGET.

No normalization values were fitted in Step 8.

## 13. TRAIN Role

TRAIN may be used for parameter optimization, predeclared training augmentation, predeclared source-only modality masking, and source-only normalization fitting.

## 14. DEV Role

DEV may be used for architecture/hyperparameter selection, checkpoint selection, and early stopping. DEV cannot fit final calibration parameters.

## 15. CALIBRATION Role

CALIBRATION is available only after checkpoint selection for source-only temperature scaling, separately predeclared source-only abstention threshold analysis if required, and source-only conformal scores. CALIBRATION cannot update weights or select an architecture/checkpoint.

## 16. Checkpoint Selection Rule

Primary criterion: SOURCE DEV macro-F1.

Tie-break order:

1. Higher SOURCE DEV macro-F1
2. Lower SOURCE DEV NLL
3. Earlier epoch

Target information and calibration metrics are unavailable for checkpoint selection. Maximum epoch budget and patience remain Step 9 decisions and must be frozen before training.

## 17. Model Seeds

`MODEL_SEEDS = [17, 42, 2026]`.

Repository preflight found no previously frozen valid model seed list. The same seeds must be used across reciprocal directions, C0–C5 conditions, baseline comparisons, and later lightweight-method comparisons. Primary numerical results require all three seeds. Seed 42 is only a canonical presentation seed for a single illustrative visualization.

## 18. C0–C5 Frozen Definitions

The authoritative definition is preserved unchanged from `docs/benchmark_spec.md`, `configs/data_contract_v1.yaml`, and `docs/harmonization_contract_v1_2.md`:

- C0: known domain + EEG + EOG (`known_domain_EEG_EOG`)
- C1: known domain + EEG only, synthetic EOG loss (`known_domain_EEG_only_synthetic_no_EOG`)
- C2: known domain + EOG only, synthetic EEG loss (`known_domain_EOG_only_synthetic_no_EEG`)
- C3: unseen domain + EEG + EOG (`unseen_domain_EEG_EOG`)
- C4: unseen domain + EEG only, compound dataset shift plus synthetic EOG loss (`unseen_domain_EEG_only_synthetic_no_EOG`)
- C5: unseen domain + EOG only, compound dataset shift plus synthetic EEG loss (`unseen_domain_EOG_only_synthetic_no_EEG`)

Both-primary-modality removal is forbidden. ISRUC montage family is an acquisition nuisance stratum, not a C0–C5 missing-modality condition. Structural channel absence is not synthetic masking.

No C0–C5 conflict was found.

## 19. Missing-Modality Semantics

When a modality is designated missing, its physiological signal is not synthesized. The normalized tensor is replaced by the frozen missing-modality representation expected by the future baseline, with an explicit modality-availability mask where supported. Another modality is never substituted. Architectural implementation is deferred to Step 9.

## 20. Calibration Protocol

### Source-only

Primary calibration is scalar `TEMPERATURE_SCALING`, fitted with SOURCE CALIBRATION labels only after checkpoint selection. Report `UNCALIBRATED` and `SOURCE_TEMPERATURE_SCALED` probabilities.

### Cross-source future calibration

Relevant only when multiple source datasets are available, such as after SHHS integration. It uses source calibration subjects only and is `NOT_APPLICABLE_FOR_TWO_DOMAIN_CORE`.

### Oracle target calibration

Separate upper-bound analysis only. It is never pooled with primary target-free results.

## 21. Oracle Target Partition

Manifest: `reports/oracle_target_partitions_v1.csv`.

- Rows: 177
- `ORACLE_SPLIT_SEED = 2027`
- ORACLE_CALIBRATION: 20%
- ORACLE_EVALUATION: 80%
- Sleep-EDF: 16 calibration, 62 evaluation subjects
- ISRUC: 19 calibration, 80 evaluation subjects
- ISRUC oracle calibration montage counts: 3 A1/A2, 16 M1/M2

The oracle partition is disjoint by subject and never affects primary roles or primary target-free results.

## 22. Uncertainty Scores

Primary uncertainty: predictive entropy, `H(p) = -Σ p_c log(p_c)`.

Secondary uncertainty: `1 - max_c p_c`.

Higher values mean more uncertainty and should predict more errors. Optional model-specific epistemic scores are not primary and are deferred.

## 23. Predictive Metrics

Primary: macro-F1 over the fixed five-class list `[Wake, N1, N2, N3, REM]`.

Secondary: Cohen’s kappa, balanced accuracy, per-stage recall, and confusion matrix. Plain accuracy is not the primary metric.

## 24. Calibration Metrics

Primary: NLL and Brier score.

Reliability summaries: ECE with 15 equal-width confidence bins, adaptive ECE with 15 equal-mass bins where feasible, classwise reliability, and classwise ECE. Bin definitions and empty-bin policy must be recorded. ECE is not sufficient as the sole calibration conclusion.

## 25. Error-Detection Metrics

`ERROR = 1` when predicted class differs from ground truth and `ERROR = 0` otherwise. Primary uncertainty orientation is higher score → higher error likelihood.

Report error-detection AUROC and AUPRC. ERROR is the positive class for AUPRC. Do not reverse the result into correctness AUROC.

## 26. Selective-Prediction Metrics

Sort predictions from lowest to highest uncertainty. Risk is misclassification rate, `1 - accuracy`. Primary selective metric: AURC.

Also report:

- empirical risk-coverage curve;
- risk at 95%, 90%, 80%, 70%, and 50% retained coverage;
- selective macro-F1 at those coverages.

Do not choose coverages after curve inspection and do not artificially smooth the primary curve.

## 27. Conformal Protocol

Primary method: split conformal classification with APS, using UNCALIBRATED model probabilities and SOURCE CALIBRATION only.

Nominal miscoverage levels:

- alpha = 0.10, nominal 90% coverage
- alpha = 0.05, nominal 95% coverage

Report empirical coverage, nominal-minus-empirical coverage gap, mean set size, median set size, and singleton-set fraction. Formal exchangeability-based marginal coverage guarantees do not generally transfer under arbitrary dataset/domain or modality shift; these are empirical under-shift results, not transferred guarantees.

Temperature-scaled conformal is not primary because it reuses the same source calibration subjects; any later use is secondary/exploratory unless independent or cross-fitted calibration is frozen first.

## 28. Montage-Stratified ISRUC Sensitivity

Whenever ISRUC is TARGET, report at minimum `ISRUC_A1A2` and `ISRUC_M1M2`, with subject and epoch counts. Where support permits, report macro-F1, NLL, Brier, error-detection AUROC, error-detection AUPRC, and AURC by stratum.

These are sensitivity strata, not separate target datasets. Target subjects are not rebalanced. The known raw-scale difference remains an acquisition nuisance factor.

## 29. Statistical Unit

`SUBJECT`.

Epochs are clustered within subjects. Sleep-EDF nights remain within selected subject clusters and the ISRUC recording remains intact.

## 30. Bootstrap Protocol

- Replicates: 2,000
- Seed: `BOOTSTRAP_SEED = 2028`
- Interval: percentile 95% CI
- Resampling unit: subjects with replacement
- Cluster contents: all relevant epochs for selected subjects
- Epoch-level inferential intervals/tests: forbidden

## 31. Multi-Seed Aggregation

For each direction/condition, run all three frozen model seeds. Report mean and standard deviation across seeds. Subject-bootstrap indices are identical across model seeds; each bootstrap replicate computes each seed’s metric on the same subject sample, then stores the replicate mean.

## 32. Paired Comparison Protocol

Use paired subject bootstrap for full versus missing modality, uncalibrated versus temperature-scaled probabilities, and baseline versus later methods. Use identical target subjects, bootstrap samples, and model seeds. Report observed metric delta and paired 95% bootstrap CI.

## 33. Domain × Modality Interaction

Use the authoritative C0–C5 definitions to construct a predeclared modality-loss effect relative to the corresponding full-modality condition for each target domain. Compare modality degradation across held-out target domains with paired/hierarchical subject-bootstrap contrasts where structure permits.

Interaction direction is not assumed. With two accessible domains, report the reciprocal interaction descriptively and with the predeclared subject-respecting contrast. Extend the same contrast to SHHS without retuning when SHHS becomes available.

## 34. Multiple-Comparison Policy

Primary inference is limited to:

- macro-F1 degradation;
- NLL degradation;
- AURC degradation;
- conformal coverage gap;
- predeclared domain × modality interaction contrast.

Other metrics are supporting/descriptive unless linked to a research question. Secondary p-values are not implemented in Step 8; if later added, use a documented false-discovery correction within a clearly defined family.

## 35. Target-Free Hyperparameter Rule

Fit using SOURCE TRAIN and select using SOURCE DEV. SOURCE CALIBRATION and TARGET are unavailable for architecture or hyperparameter selection. No target performance may be inspected during tuning.

## 36. Lightweight-Method Gate

Do not implement the modality-conditioned/shift-aware calibrator in Step 8 and do not predeclare success. A later method is authorized only after baseline results establish a reproducible, actionable failure mode not explained by leakage, labels, channels, or threshold misuse, followed by separate preregistration.

## 37. Machine-Readable Protocol

- Path: `configs/evaluation_protocol_v1.yaml`
- Version: `1.0.0`
- SHA-256: `f5271f4c22feed4e2b95708025d94fc82b60f9a09e96c1227075d927c2ee1294`
- Gate encoded: `EXPERIMENT_PROTOCOL_FROZEN`

## 38. Subject Partition Manifest

- Path: `reports/subject_partitions_v1.csv`
- Rows: 177
- SHA-256: `fd2bb296502a339b2593b7d5dd0e14c6952ed229a950beffb9f5e6057d85967a`
- Dataset counts: Sleep-EDF 78, ISRUC 99
- I040 absent by design

## 39. Oracle Partition Manifest

- Path: `reports/oracle_target_partitions_v1.csv`
- Rows: 177
- SHA-256: `835344bcbd1992b00ec309082317d7f08a0b7f5f6c8d401ee670627d6bd806de`
- Roles: ORACLE_CALIBRATION and ORACLE_EVALUATION
- Subject-disjoint within each dataset

## 40. Human-Readable Protocol

- Path: `docs/experimental_protocol_v1.md`
- SHA-256: `1c18c069be871fba27243a0b36a033ecda3416270f587d537ecbc35a99f964f6`

## 41. Leakage Tests

Added `tests/test_step08_protocol.py` checks for:

- 177-row complete source manifest;
- unique subject/dataset keys;
- mutually exclusive source roles;
- complete reciprocal direction target/source separation;
- Sleep-EDF subject grouping;
- ISRUC montage inclusion and I040 exclusion;
- target-free normalization and calibration boundaries;
- oracle separation from primary use;
- C0–C5 exact definitions;
- montage non-rebalancing;
- reproducible protocol hashes.

## 42. Tests Added

- `tests/test_step08_protocol.py`
- `scripts/step_08_freeze_protocol.py` is the metadata-only reproducible generator for source/oracle manifests and split audit.

## 43. Validation

Actual focused validation:

```text
pytest -q tests/test_step08_protocol.py
7 passed in 0.13s
```

The generator produced:

```text
177 source rows, 177 oracle rows, 6 audit rows
```

Final required validation results:

```text
pytest -q
71 passed in 9.92s

PYTHONPATH=src python -m compileall -q src tests scripts
PASS

git diff --check
PASS

Step 8 artifact validation
PASS

raw/processed tracked-file check
PASS
```

The protocol hash reproduction test passed. No signal arrays, labels, predictions, or model outputs were read or generated by the Step 8 generator.

## 44. Files Created

- `configs/evaluation_protocol_v1.yaml`
- `docs/experimental_protocol_v1.md`
- `reports/subject_partitions_v1.csv`
- `reports/oracle_target_partitions_v1.csv`
- `reports/step08_subject_split_audit.csv`
- `reports/step08_protocol_hashes.txt`
- `reports/STEP_08_EXPERIMENT_PROTOCOL_FREEZE_REPORT.md`
- `scripts/step_08_freeze_protocol.py`
- `tests/test_step08_protocol.py`

## 45. Files Modified

No prior frozen cohort, contract, preprocessing, C0–C5 definition, or raw/processed artifact was modified. The Step 8 additions are new protocol, partition, audit, generator, test, and report artifacts.

## 46. Explicitly Not Done

- no model implementation;
- no model training;
- no normalization fitting;
- no predictions;
- no ML results;
- no calibration fitting;
- no conformal execution;
- no SHHS access;
- no cohort modification;
- no raw/processed data committed;
- no GitHub push.

## 47. Remaining Pre-Model Issues

`NONE` for the Step 8 protocol freeze.

The next phase must still define and implement the baseline model/training system inside this frozen protocol, including architecture, tensor interfaces, optimizer, training budget, patience, augmentation, checkpoint storage, and execution controls.

## 48. Final Benchmark Status

`NO`.

SHHS remains outstanding and unaccessed.

## 49. Recommended Next Step

# Step 9 — Baseline Model and Training Protocol Freeze + Implementation

The baseline must operate entirely inside the frozen Step 8 protocol.

Do **not** execute Step 9 in this step.

## 50. Git Status / Diff Summary

The Step 8 artifact set is ready for local commit with:

```text
research: freeze ShiftSleep-UQ experimental protocol
```

No remote push is authorized or performed.
