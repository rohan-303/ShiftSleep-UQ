# Hypothesis registry

All hypotheses are **UNTESTED**. Primary statistical unit is the subject unless a later frozen protocol justifies another unit.

## H1
**Hypothesis:** Cross-dataset shift reduces sleep-staging performance relative to within-domain evaluation. **IVs:** domain condition (within/unseen), dataset. **Outcomes:** macro-F1, kappa, balanced accuracy, per-stage recall. **Direction:** deterioration under unseen domain. **Evidence:** paired subject-level performance comparisons and intervals. **Status:** UNTESTED.

## H2
**Hypothesis:** Missing modalities increase predictive error and calibration error. **IVs:** modality mask, missingness condition. **Outcomes:** error rate, NLL, Brier, ECE, stage recall. **Direction:** worse with missingness. **Evidence:** matched full-versus-mask comparisons. **Status:** UNTESTED.

## H3
**Hypothesis:** Compound dataset + modality shift causes greater reliability degradation than either shift alone. **IVs:** dataset shift, modality shift, interaction. **Outcomes:** calibration/error-detection/selective metrics. **Direction:** negative interaction or greater degradation in compound condition. **Evidence:** factorial interaction analysis with subject-level resampling. **Status:** UNTESTED.

## H4
**Hypothesis:** Standard softmax confidence and IID/source-optimized calibration do not remain reliably calibrated under compound shift. **IVs:** calibrator and deployment condition. **Outcomes:** calibration metrics and reliability diagrams. **Direction:** increased miscalibration under compound shift. **Evidence:** frozen source calibration evaluated on held-out targets. **Status:** UNTESTED.

## H5
**Hypothesis:** Selective prediction improves retained-example quality as coverage decreases, with strength varying by domain and mask. **IVs:** coverage, domain, modality condition, uncertainty method. **Outcomes:** risk-coverage, AURC, selective macro-F1, risk at coverage. **Direction:** lower retained risk at lower coverage. **Evidence:** curves and subject-level intervals. **Status:** UNTESTED.

## H6
**Hypothesis:** Source-only conformal calibration may show empirical coverage below nominal coverage on unseen datasets, especially with missing modalities. **IVs:** nominal level, domain, mask, calibration regime. **Outcomes:** coverage gap, set size. **Direction:** undercoverage under shift. **Evidence:** nominal-versus-empirical coverage with subject-level intervals. **Status:** UNTESTED.

## H7 (exploratory)
**Hypothesis:** A later modality-conditioned calibrator may improve compound-shift calibration over one global calibrator. **IVs:** calibrator type, domain, mask. **Outcomes:** calibration and selective metrics, coverage. **Direction:** possible improvement without excessive coverage loss. **Evidence:** only after baseline failure mode and method protocol are independently established. **Status:** UNTESTED / EXPLORATORY.
