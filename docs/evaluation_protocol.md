# Evaluation protocol (draft)

1. Split at participant/subject level before epoch construction or any learned preprocessing. A subject occurs in exactly one partition within a study role.
2. Train/dev are the only data used for fitting preprocessing, selecting hyperparameters, selecting models/checkpoints, calibrating target-free methods, thresholds, and operating points.
3. A leave-one-dataset-out design holds one dataset/domain out as target; target labels are inaccessible in strict target-free evaluation.
4. Freeze the protocol, configurations, split manifests, preprocessing contract, and analysis plan before opening test labels.
5. Fit normalization/statistical transforms on training subjects only; apply frozen transforms to dev/test. No test-subject statistics.
6. Keep source-only, cross-source, and ORACLE TARGET CALIBRATION separate in names, configs, tables, and figures.
7. Report macro-F1, kappa, balanced accuracy, per-stage recall, confusion matrices, NLL, Brier, ECE/adaptive ECE where implemented, class-wise calibration, reliability diagrams, AUROC/AUPRC for error detection, risk-coverage/AURC, selective macro-F1, coverage/risk operating points, conformal coverage gaps, and set size as applicable. ECE alone is insufficient.
8. Use multiple controlled seeds and record all seeds. Compare paired conditions on the same subjects where possible.
9. Prefer subject-level bootstrap confidence intervals and subject-level resampling for statistical comparisons. PSG epochs from the same participant are correlated and must not be treated as statistically independent observations for confidence intervals or significance tests.
10. Interpret effect sizes and intervals, account for multiplicity and repeated conditions, and distinguish exploratory analyses from confirmatory analyses.

## Missingness and comparison rules
Mask definitions, availability assumptions, and whether models receive the mask must be predeclared. Comparisons should preserve subject and recording pairing where possible. No target-domain labels may enter source-only calibration or selection.
