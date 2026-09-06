# Evaluation Protocol — Step 3 Freeze Addendum

## Frozen target-free terminology

- **SOURCE TRAIN:** labeled source participants used for model fitting only.
- **SOURCE DEV:** disjoint labeled source participants used for hyperparameters, checkpoint policy, and design choices.
- **SOURCE CALIBRATION:** a separately identified source-only split, or source DEV subset under a predeclared policy, used to fit temperature/conformal/calibration parameters after model selection.
- **HELD-OUT TARGET DATASET:** a dataset/domain excluded from fitting, model selection, calibration, and adaptation.
- **TARGET TEST:** the final labeled evaluation partition of the held-out target; labels are inaccessible until the protocol is frozen and evaluation is run.

Primary setting: no target data, labeled or unlabeled, are accessed before final target evaluation. Any unlabeled-target adaptation is a separate adaptation setting and is not target-free domain generalization.

## Train/dev/test discipline

Splits are subject-level, with nights/recordings nested under subjects. No subject, duplicate recording, or derived segment may cross partitions. Dataset leave-one-domain-out is the preferred external test concept when enough harmonizable domains pass the schema audit. Test data remain untouched until preprocessing, masks, calibration, thresholds, metrics, and statistical analysis are frozen.

## Model selection and preprocessing

All hyperparameters, architecture choices, checkpoint selection, normalization statistics, feature selection, mask policy, and abstention thresholds use TRAIN/DEV only. Preprocessing transforms are fit on source TRAIN (or a separately predeclared source-only fit split) and applied without refitting to target. Target labels are prohibited from all fitting and selection in the primary regime.

## Calibration regimes

A. **SOURCE-ONLY / TARGET-FREE:** calibration uses only source TRAIN/DEV information.
B. **CROSS-SOURCE:** calibration strategy uses multiple source domains while the held-out target remains untouched.
C. **ORACLE TARGET CALIBRATION:** labeled target data are permitted as an explicitly labeled upper bound and never pooled with target-free results.

## Reliability and selective evaluation

Report predictive, probabilistic, correctness-ranking, selective, and conformal endpoints separately. Formal selective prediction requires risk-versus-coverage curves, AURC, and fixed-risk/fixed-coverage summaries; removing uncertain epochs alone is insufficient. ECE is not sufficient as a sole calibration conclusion.

## Statistical plan (future; no statistics performed here)

Treat domain condition (known/unseen) and modality condition (full/missing) as factorial factors, with an explicit DOMAIN × MODALITY interaction contrast. Include dataset heterogeneity, mask type, and seed as planned factors or nuisance terms. Use paired comparisons where identical subjects/predictions permit them. Use subject-level bootstrap confidence intervals, with recording/night nested within subjects; do not resample epochs as independent units.

PSG epochs from the same participant are correlated and must not be treated as statistically independent observations for confidence intervals or significance tests. Repeated recordings/visits require participant-aware clustering. Dataset-level generalization should also report per-dataset estimates, not only pooled epochs. Multiple comparisons and metric families require a predeclared reporting strategy.

## ISRUC montage-stratified reporting addendum

Under protocol amendment A-07.7-01, ISRUC source-supported channel families are acquisition nuisance strata, not missing-modality conditions. Any future ISRUC analysis must preserve and report exact source derivations and separately report at least `ISRUC_A1A2` (`C3-A2` + `LOC-A2`) and `ISRUC_M1M2` (`C3-M2` + `E1-M2`) for predictive performance, calibration, and selective risk/AURC. No result may pool these strata without also showing the stratum-specific estimates and a predeclared pooled-analysis rationale. This addendum does not authorize acquisition, preprocessing, splits, modeling, or metrics in Step 7.7.
