# Frozen Hypothesis Registry — Step 3

Step 1 hypotheses H1–H7 are preserved in the history section below. The following hypotheses are the frozen pre-experimental set. All remain UNTESTED.

## Step 5 protocol amendment

The original S0–S4 and three-family modality formulation is superseded for the primary benchmark by C0–C5 over EEG+EOG. F1–F5 are interpreted over domain × primary-modality availability; EMG is secondary and structural mismatches are separate. F6 remains conditional and unauthorized.

## F1 — Interaction-related reliability degradation
- **Hypothesis:** The effect of unseen-domain evaluation on calibration and uncertainty reliability depends on modality availability; the domain × modality interaction is non-zero and may be super-additive, but direction is not assumed.
- **Independent variables:** domain condition (known/unseen), modality condition (full/single missing/multiple missing), dataset, mask type.
- **Dependent outcomes:** NLL, Brier, ECE/adaptive ECE, correctness AUROC/AUPRC, AURC, conformal coverage gap.
- **Statistical unit:** subject, with recording/night nested within subject.
- **Framework:** mixed-effects or cluster-robust factorial analysis with dataset and seed terms; subject-level bootstrap.
- **Falsification:** interaction estimates are practically negligible with predeclared equivalence bounds, or disappear after channel/label confound controls.
- **Status:** UNTESTED.

## F2 — Ranking/calibration dissociation
- **Hypothesis:** Uncertainty-score ranking for correctness and probability calibration can degrade at different rates under shift.
- **Independent variables:** domain, modality, shift interaction.
- **Dependent outcomes:** correctness AUROC/AUPRC versus NLL/Brier/ECE/reliability diagrams.
- **Statistical unit:** subject.
- **Framework:** paired subject-level bootstrap differences and interaction contrasts.
- **Falsification:** all reliability dimensions show indistinguishable, stable changes within predeclared bounds.
- **Status:** UNTESTED.

## F3 — Selective prediction is not guaranteed by confidence
- **Hypothesis:** Retaining high-confidence predictions can improve selective risk, but the gain and monotonicity of risk-coverage may vary under compound shift.
- **Independent variables:** coverage, domain, modality, uncertainty score.
- **Dependent outcomes:** selective risk, selective macro-F1, AURC, coverage at fixed risk.
- **Statistical unit:** subject-level aggregated curve contributions.
- **Framework:** paired bootstrap confidence bands and area/point contrasts.
- **Falsification:** no score produces useful risk reduction above a predeclared minimum, or compound shift reverses the expected ordering consistently.
- **Status:** UNTESTED.

## F4 — Source-calibrated conformal transfer can under-cover
- **Hypothesis:** Source-calibrated prediction sets may deviate below nominal coverage on unseen domains or missing modalities; the magnitude is an empirical question.
- **Independent variables:** domain, modality, nominal level, calibration regime.
- **Dependent outcomes:** empirical coverage, nominal-minus-empirical gap, set size.
- **Statistical unit:** subject.
- **Framework:** subject bootstrap intervals and predeclared coverage-gap tests/descriptive thresholds; no universal guarantee claim.
- **Falsification:** coverage remains within predeclared tolerance across all shifted conditions, or conformalization is not feasible under the frozen label space.
- **Status:** UNTESTED.

## F5 — Reliability failure attribution
- **Hypothesis:** Dataset/domain shift, modality loss, and their interaction contribute distinguishable components to reliability degradation.
- **Independent variables:** factorial domain/modality conditions and dataset.
- **Dependent outcomes:** vector of predictive and reliability metrics.
- **Statistical unit:** subject.
- **Framework:** hierarchical factorial model with dataset heterogeneity and seed as repeated nuisance factor; paired contrasts.
- **Falsification:** one main effect explains all observed differences and interaction confidence intervals include a practically null effect.
- **Status:** UNTESTED.

## F6 — Conditional method gate
- **Hypothesis:** A lightweight modality-aware/shift-aware calibrator may improve reliability only for a diagnosed baseline failure mode without unacceptable coverage loss.
- **Independent variables:** frozen baseline versus method, condition, calibration regime.
- **Dependent outcomes:** primary calibration and selective metrics plus predictive utility.
- **Statistical unit:** subject.
- **Framework:** preregistered paired comparison on untouched test data after design freeze.
- **Falsification:** no reproducible baseline failure, no improvement over baseline within uncertainty, or method requires target labels/data in the primary setting.
- **Status:** EXPLORATORY / NOT AUTHORIZED.

## Superseded Step 1 hypotheses

H1 cross-dataset shift reduces performance; H2 missing modalities increase error/calibration error; H3 compound shift causes greater reliability degradation; H4 IID-calibrated confidence fails under compound shift; H5 selective prediction improves retained quality; H6 source-calibrated conformal coverage under-covers on unseen datasets; H7 modality-conditioned calibration may help. These are retained as historical candidate hypotheses, not erased. F1–F6 supersede them by making interaction, ranking/calibration dissociation, falsification, and statistical units explicit. H7 remains conditional and exploratory.
