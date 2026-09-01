# Metric protocol (provisional)

## Primary
1. Macro-F1 and balanced accuracy for class-imbalance-aware predictive performance.
2. Multiclass Brier score and NLL for probabilistic quality.
3. ECE plus reliability diagrams, with binning rule and empty-bin policy frozen before test access.
4. Error-detection AUROC, with AUPRC reported when correctness/event imbalance makes AUROC incomplete.
5. Risk-coverage curve and AURC for selective prediction.
6. Conformal empirical coverage and prediction-set size, with nominal-minus-empirical gap.

## Secondary
Cohen's kappa, per-stage recall/sensitivity, class-wise calibration, adaptive/equal-mass ECE, selective macro-F1, risk at predefined coverage, and coverage at predefined risk.

## Diagnostic
Confusion matrices, stage prevalence, reliability diagrams by domain/mask, uncertainty distributions, calibration curves by stage, and subgroup/domain slices only when metadata are verified.

ECE is sensitive to bin count, binning rule, sample size, class imbalance, and aggregation choices; it must not be the sole calibration conclusion. Confidence/entropy is an uncertainty score, not evidence of calibration. Deferral is not formal selective prediction without risk-versus-coverage analysis.
