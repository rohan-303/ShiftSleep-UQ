# Paper Thesis Freeze

## Working Title

**ShiftSleep-UQ: Calibration and Selective Reliability of Multimodal Sleep Staging Under Compound Dataset and Missing-Modality Shift**

## One-Sentence Problem

Determine whether source-calibrated multimodal sleep-staging predictions remain probabilistically reliable, useful for error detection and abstention, and empirically conformal under an unseen PSG dataset/domain combined with physiological modality loss.

## Scientific Gap

The audit verifies separate prior clusters for cross-dataset generalization, incomplete multimodal sleep staging, and sleep-staging uncertainty. It did not verify a unified, leakage-safe, target-free reliability evaluation crossing dataset/domain shift with modality availability. This is a qualified gap, not a priority claim.

## Why Existing Work Does Not Resolve It

SleepDG and DREAM address generalization/representation; CIMSleepNet and RMSSC address incomplete modalities; SleepTransformer, U-PASS, and Direct Quantification address uncertainty. Accessible evidence does not establish that these works jointly evaluate source-only calibration, correctness ranking, formal risk-coverage, and empirical conformal coverage under simultaneous dataset and modality shift. RMSSC and Direct Quantification remain incomplete collision checks.

## Primary Research Question

How do predictive probabilities and uncertainty-based reliability change when a multimodal sleep-staging system is transferred from source data to an unseen PSG dataset/domain with full or missing physiological modalities?

## Frozen Contributions

1. **Benchmark:** A leakage-safe benchmark crossing held-out PSG dataset/domain and modality availability, with synthetic masking separated from structural channel mismatch.
2. **Empirical analysis:** Calibration, correctness ranking, selective risk-coverage, and empirical conformal coverage as shift severity changes, using subject-level statistical inference.
3. **Conditional method:** A lightweight modality-aware or shift-aware calibrator only if frozen baseline evidence identifies a reproducible, actionable failure mode.

## Evaluation Philosophy

Test data remain untouched until the protocol is frozen. Source-only calibration is primary. Results separate predictive quality, probability calibration, uncertainty ranking, selective prediction, and conformal empirical coverage. ECE is never the sole calibration endpoint.

## Novelty Boundary

The claim is an interaction-focused reliability benchmark and analysis, not a new sleep-staging architecture, a first domain-generalization method, a first missing-modality method, or a guarantee of conformal coverage under shift.

## Claims Allowed

The project may report what happens empirically under explicitly defined datasets, masks, splits, metrics, and source-only protocols. It may report observed coverage gaps and interaction effects with uncertainty intervals.

## Claims Prohibited

No “first,” “state of the art,” “clinical-grade,” diagnostic, or unconditional distribution-shift guarantee claims. Do not call entropy/confidence calibrated without calibration evidence, or informal rejection a formal selective-prediction result.

## Conditional Method Policy

No method implementation is authorized before baseline experiments, preregistration of the comparison, and a report showing a reproducible failure not explained by leakage, label mapping, channel incompatibility, or threshold misuse. The method must be lightweight, modality/shift-conditioned, target-free in the primary setting, and evaluated against frozen baselines without target labels.

## Conditions That Would Falsify the Paper Thesis

- A verified paper evaluates essentially the same target-free dataset × modality reliability factorial.
- Candidate datasets cannot support meaningful modality comparison after source/schema audit.
- Source-only calibration cannot be defined consistently across domains.
- The apparent interaction is only a trivial artifact of incompatible channels or labels.
- No legally reproducible multi-domain configuration can be assembled.
- The benchmark cannot enforce subject identity and duplicate-recording separation.
