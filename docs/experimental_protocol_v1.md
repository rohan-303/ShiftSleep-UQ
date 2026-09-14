# ShiftSleep-UQ Experimental Protocol v1

**Status:** frozen before model implementation

**Protocol version:** 1.0.0

**Protocol gate:** `EXPERIMENT_PROTOCOL_FROZEN`

## Purpose and scope

This document freezes the pre-model experimental protocol for the accessible Sleep-EDF SC + original-provider ISRUC-S1 core. It does not implement a model, fit normalization values, run calibration, generate predictions, calculate performance, or access SHHS. The purpose is to make subsequent results difficult to manipulate through post-hoc changes to splits, metrics, uncertainty definitions, calibration, or statistical units.

The frozen data contract is `1.2.0` and preprocessing is `0.1.0`. The final benchmark remains `NO` because SHHS has not been accessed.

## Frozen cohort inputs

### Sleep-EDF SC

- 78 included subjects
- 153 included recordings
- 414,961 valid epochs
- Frozen source manifest: `reports/core_recording_manifest_v1_1.csv`
- Manifest SHA-256: `417286a0b5562c80693c4c410f64b3dcf773c8328568f5123deecca34c92a806`

All nights for one Sleep-EDF subject remain in one source role. Sleep-EDF SC is the accessible source/target domain; Sleep-EDF ST is not silently added as a separate domain.

### ISRUC-S1

- 99 included subjects
- 99 included recordings
- 89,312 valid epochs
- Cohort config: `configs/isruc_original_cohort_v3.yaml`
- Config SHA-256: `af4fb75be97df99443d5b7bc42d8f49bd55440702d07dffd49563356f7cece9d`
- Structural exclusion: I040, `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`
- Montage strata: 17 `ISRUC_A1A2`, 82 `ISRUC_M1M2`

ISRUC exact source pairings remain unchanged: `C3-A2 + LOC-A2` → `ISRUC_A1A2`; `C3-M2 + E1-M2` → `ISRUC_M1M2`.

### Accessible core

- Config: `configs/core_cohort_v2.yaml`
- Config SHA-256: `e8dbc91b04b4b54797e8d83be1866b28674fa2587e31507f94b3583e1f24f9ae`
- Total included subjects: 177
- No cohort modification occurred in Step 8.

## Reciprocal experiment directions

### D1 — `D1_SLEEPEDF_TO_ISRUC`

- Source: Sleep-EDF SC source TRAIN/DEV/CALIBRATION partitions
- Target: all 99 included ISRUC-S1 subjects
- Target observations and labels are unavailable to fitting, normalization, checkpoint selection, hyperparameter selection, calibration, threshold selection, conformal calibration, and adaptation.

### D2 — `D2_ISRUC_TO_SLEEPEDF`

- Source: ISRUC-S1 source TRAIN/DEV/CALIBRATION partitions
- Target: all 78 included Sleep-EDF SC subjects
- Target observations and labels are unavailable to fitting, normalization, checkpoint selection, hyperparameter selection, calibration, threshold selection, conformal calibration, and adaptation.

The stored source-role field is ignored when that dataset acts as the held-out target. Thus every included target subject is evaluated in the primary target population.

## Future SHHS extension

SHHS is not available and no SHHS data were accessed or fabricated. When a third validated primary domain exists, use leave-one-dataset-out domain generalization: the source pool is all other validated primary datasets and the target is the entirety of the frozen target dataset. Existing Sleep-EDF and ISRUC partitions must not be reshuffled merely because SHHS becomes available. SHHS must use the same deterministic subject-level partition algorithm, with no performance-driven repartitioning.

## Source split rule

The partition unit is the subject. The source roles are TRAIN, DEV, and CALIBRATION with nominal proportions 70%, 15%, and 15%. Largest-remainder allocation is applied independently within each frozen ISRUC montage stratum and to the unstratified Sleep-EDF subject set. Ties use fixed role order TRAIN, DEV, CALIBRATION. Exact realized counts are reported in the audit; epoch totals never influence assignment.

- Sleep-EDF: deterministic subject assignment without label or stage stratification; all nights remain grouped.
- ISRUC: deterministic subject assignment stratified only by `montage_variant`.
- No target outcomes, target stage distributions, target performance, calibration behavior, or uncertainty behavior enter assignment.

## Source partition counts

The machine-readable manifest is `reports/subject_partitions_v1.csv` with 177 rows.

| Dataset | TRAIN | DEV | CALIBRATION | Total |
|---|---:|---:|---:|---:|
| Sleep-EDF SC | 54 | 12 | 12 | 78 |
| ISRUC-S1 | 70 | 15 | 14 | 99 |
| Total | 124 | 27 | 26 | 177 |

ISRUC montage counts by source role:

| Role | A1/A2 | M1/M2 | Total |
|---|---:|---:|---:|
| TRAIN | 12 | 58 | 70 |
| DEV | 3 | 12 | 15 |
| CALIBRATION | 2 | 12 | 14 |
| Total | 17 | 82 | 99 |

The slight 14-subject ISRUC calibration count is the deterministic result of largest-remainder allocation within the two montage strata; no balancing adjustment is permitted.

## Split seed

`SPLIT_SEED = 2026`.

No seed search or aesthetic rebalancing was performed.

## Target evaluation rule

For D1, all 99 included ISRUC subjects are primary target evaluation subjects. For D2, all 78 included Sleep-EDF subjects are primary target evaluation subjects. The target dataset is not reduced to its stored source-role partition.

## Strict target-free firewall

Before primary target evaluation, prohibited target information includes target labels, raw signal distributions, normalization statistics, class/stage frequencies, target montage distribution for tuning, feature or representation statistics, calibration statistics, uncertainty statistics, thresholds, conformal scores, and error rates. Intrinsic frozen-contract metadata such as exact montage identity may be retained for analysis, but not used to tune the model.

There is no target-test-label scaling, target-adaptive normalization, subject-specific target normalization, record-specific target z-scoring, montage-specific normalization, or target-domain recentering.

## Normalization policy

Persisted preprocessing outputs remain unnormalized. At model time, fit one global mean and standard deviation per input modality using observed SOURCE TRAIN values only. Freeze those parameters and apply them identically to SOURCE TRAIN, SOURCE DEV, SOURCE CALIBRATION, and TARGET. No normalization values are fitted in Step 8, and no target, subject, record, or montage adaptive normalization is allowed.

## Development roles

### TRAIN

TRAIN may be used for parameter optimization, predeclared training augmentation, predeclared source-only modality masking, and normalization fitting.

### DEV

DEV may be used for architecture/hyperparameter selection, checkpoint selection, and early stopping. DEV must not fit final calibration parameters.

### CALIBRATION

CALIBRATION is used only after checkpoint selection for source-only temperature scaling, any separately predeclared source-only abstention threshold analysis, and source-only conformal scores. CALIBRATION cannot update network weights, select checkpoints, or select architectures.

### TARGET

TARGET is evaluation only under the primary protocol.

## Checkpoint and hyperparameter selection

The primary checkpoint criterion is SOURCE DEV macro-F1. Tie-breaks are, in order: higher SOURCE DEV macro-F1, lower SOURCE DEV NLL, and earlier epoch. Target information and calibration metrics are prohibited from checkpoint selection. Training epoch budgets and patience must be frozen in the later model/training step before execution.

Hyperparameters are fit using SOURCE TRAIN and selected using SOURCE DEV. SOURCE CALIBRATION and TARGET are unavailable for architecture or hyperparameter selection.

## Model seeds

`MODEL_SEEDS = [17, 42, 2026]`. The same seeds apply across reciprocal directions, C0–C5 conditions, baseline comparisons, and later lightweight method comparisons. Primary numerical results require all three seeds. Seed 42 is only the canonical presentation seed for a single illustrative visualization, if needed.

## C0–C5 frozen definitions

The authoritative definitions are preserved from `docs/benchmark_spec.md`, `configs/data_contract_v1.yaml`, and `docs/harmonization_contract_v1_2.md`:

- **C0:** known domain + EEG + EOG (`known_domain_EEG_EOG`).
- **C1:** known domain + EEG only, with synthetic EOG loss (`known_domain_EEG_only_synthetic_no_EOG`).
- **C2:** known domain + EOG only, with synthetic EEG loss (`known_domain_EOG_only_synthetic_no_EEG`).
- **C3:** unseen domain + EEG + EOG (`unseen_domain_EEG_EOG`).
- **C4:** unseen domain + EEG only, with compound dataset shift plus synthetic EOG loss (`unseen_domain_EEG_only_synthetic_no_EOG`).
- **C5:** unseen domain + EOG only, with compound dataset shift plus synthetic EEG loss (`unseen_domain_EOG_only_synthetic_no_EEG`).

C0–C5 are all-present or one-primary-modality-missing conditions. Removing both primary modalities is forbidden. ISRUC montage family is an acquisition nuisance stratum, not a C0–C5 missing-modality condition. Structural channel absence is not controlled synthetic masking.

## Missing-modality semantics

When a modality is designated missing, its physiological signal is not synthesized. Its normalized tensor is replaced by the frozen missing-modality representation expected by the later baseline, and an explicit modality-availability mask is supplied to architectures that support it. Another modality is never substituted. Exact architectural implementation is Step 9 work.

## Calibration protocol

### SOURCE_ONLY — primary

Use scalar `TEMPERATURE_SCALING` fitted with SOURCE CALIBRATION labels only after the checkpoint is frozen. Report both `UNCALIBRATED` and `SOURCE_TEMPERATURE_SCALED` probabilities. No target fitting or target class-specific tuning is allowed.

### CROSS_SOURCE — future only

This is relevant only when the source pool contains multiple datasets, such as a future SHHS-enabled experiment. Calibration uses source-dataset calibration subjects only and never target data. It is `NOT_APPLICABLE_FOR_TWO_DOMAIN_CORE`.

### ORACLE_TARGET — upper bound only

Oracle target calibration is separate from primary results, explicitly labelled, and never pooled with target-free results.

## Oracle target partition

`reports/oracle_target_partitions_v1.csv` has 177 rows and uses `ORACLE_SPLIT_SEED = 2027`. It allocates 20% to `ORACLE_CALIBRATION` and 80% to `ORACLE_EVALUATION`, with subject grouping and ISRUC montage stratification where feasible:

- Sleep-EDF: 16 oracle calibration subjects, 62 oracle evaluation subjects.
- ISRUC: 19 oracle calibration subjects, 80 oracle evaluation subjects; calibration includes 3 A1/A2 and 16 M1/M2 subjects.

Only ORACLE_CALIBRATION labels may be used for the explicitly labelled oracle upper bound. Primary evaluation remains the complete target population and is unaffected.

## Uncertainty and error detection

Primary uncertainty is predictive entropy, `H(p) = -Σ p_c log(p_c)`. Secondary uncertainty is `1 - max_c p_c`. Higher values mean more uncertainty and should indicate higher error probability.

`ERROR = 1` when predicted class differs from ground truth; otherwise `ERROR = 0`. Report AUROC and AUPRC for error detection, with ERROR as the AUPRC positive class. Do not reverse the orientation into correctness AUROC.

## Predictive metrics

Primary predictive metric: macro-F1 over the fixed five-class list Wake, N1, N2, N3, REM. Secondary metrics are Cohen’s kappa, balanced accuracy, per-stage recall, and confusion matrix. Plain accuracy is not the primary metric.

## Calibration metrics

Primary calibration metrics are NLL and Brier score. Reliability summaries are ECE with 15 equal-width confidence bins, adaptive ECE with 15 equal-mass bins where feasible, and classwise reliability/classwise ECE. Bin definitions and empty-bin behavior must be recorded. ECE is not sufficient as the sole calibration conclusion.

## Selective prediction

Sort predictions from lowest uncertainty to highest uncertainty. Risk is misclassification rate, `1 - accuracy`. The primary selective metric is AURC. Also report the empirical risk-coverage curve, risk at retained coverages 95%, 90%, 80%, 70%, and 50%, and selective macro-F1 at those coverages. Do not select coverages after observing curves. Do not artificially smooth the primary curve; any fixed-coverage interpolation must be deterministic and documented.

## Conformal protocol

Use split conformal classification with primary method `APS` and uncalibrated model probabilities. Fit APS scores using SOURCE CALIBRATION only. Use nominal miscoverage levels alpha 0.10 and 0.05, corresponding to nominal 90% and 95% coverage. Report empirical target coverage, nominal-minus-empirical coverage gap, mean and median prediction-set size, and singleton-set fraction.

Formal marginal coverage guarantees do not generally transfer under arbitrary domain or modality shift because exchangeability may fail. These results measure empirical degradation under shift; they are not transferred target coverage guarantees. Temperature-scaled conformal is not primary because it reuses the same source calibration subjects; any later use is secondary/exploratory unless independently or cross-fitted calibration is frozen first.

## ISRUC montage sensitivity

Whenever ISRUC is TARGET, report at minimum the `ISRUC_A1A2` and `ISRUC_M1M2` strata. Where support permits, report macro-F1, NLL, Brier, error-detection AUROC/AUPRC, and AURC, together with subject and epoch counts. The strata are not separate target datasets and are not rebalanced. The known raw-scale difference remains an acquisition nuisance issue.

## Statistical unit and bootstrap

The statistical unit is SUBJECT. Epochs are clustered within subjects; Sleep-EDF nights remain within the selected subject cluster and the ISRUC recording remains intact. Never calculate inferential intervals by treating epochs as independent.

Use 2,000 subject-bootstrap replicates with `BOOTSTRAP_SEED = 2028` and percentile 95% confidence intervals. Resample target subjects with replacement, include all relevant epochs for each selected subject, and compute fixed five-class metrics without changing definitions.

For multiple model seeds, report the mean and standard deviation across seeds. Subject-bootstrap indices are identical across model seeds; each replicate computes each seed’s metric on the same resampled subjects and stores the replicate mean.

## Paired comparisons and interaction

For full versus missing modality, uncalibrated versus temperature-scaled probabilities, or baseline versus a later method, use paired subject bootstrap with identical target subjects, bootstrap samples, and model seeds. Report observed metric delta and its 95% bootstrap CI.

The domain × modality analysis is a predeclared contrast based on the authoritative C0–C5 definitions. For each target domain, calculate modality-loss effect relative to the corresponding full-modality condition, then compare modality degradation across held-out target domains with paired/hierarchical subject-bootstrap contrasts where structure permits. Interaction direction is not assumed. The same mathematical contrast extends to SHHS without retuning.

No epoch-level t-tests, confidence intervals, significance tests, or regressions are permitted. Primary statistical reporting is effect size plus subject-bootstrap 95% CI. Secondary p-values are not implemented in Step 8; if later added, they require a documented false-discovery correction within a defined family.

## Multiple-comparison policy

Primary inference is limited to macro-F1 degradation, NLL degradation, AURC degradation, conformal coverage gap, and the predeclared domain × modality interaction. Other metrics are supporting/descriptive unless explicitly tied to a research question. Per-stage recall is descriptive/secondary.

## Lightweight-method gate

The proposed lightweight modality/shift-aware calibrator is not implemented or preregistered as successful in Step 8. It may be considered only after baseline results establish a reproducible failure mode that the method is designed to address, followed by a separate protocol amendment.

## Machine-readable and audit artifacts

- Protocol: `configs/evaluation_protocol_v1.yaml`
- Subject partition manifest: `reports/subject_partitions_v1.csv` — 177 rows
- Oracle partition manifest: `reports/oracle_target_partitions_v1.csv` — 177 rows
- Split audit: `reports/step08_subject_split_audit.csv`
- Protocol hashes: `reports/step08_protocol_hashes.txt`
- Reproducible generator: `scripts/step_08_freeze_protocol.py`

## What remains for Step 9

Step 9 must define and implement the baseline model/training system inside this frozen protocol, including architecture, tensor interfaces, maximum epoch budget, patience, optimizer, training augmentations, model-time normalization implementation, checkpoint storage, and execution controls. Step 9 must not alter the subject partitions, C0–C5 meanings, target-free firewall, calibration policy, uncertainty metrics, selective coverages, conformal alpha, bootstrap procedure, or model seeds frozen here.
