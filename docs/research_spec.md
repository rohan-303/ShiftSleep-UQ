# Research specification

## Problem
Multimodal sleep staging may produce confident predictions that are unreliable when the population, recording system, dataset, or available physiological channels change. ShiftSleep-UQ studies calibration, error detection, selective prediction, and conformal coverage under subject, domain, missing-modality, and compound shifts.

## Motivation
Accuracy can conceal unsafe failures. A deployment-relevant benchmark must distinguish known-domain/full-modality performance from unseen-domain and missing-modality reliability, while preventing subject and preprocessing leakage.

## Research questions
- **RQ1:** How much does predictive performance deteriorate under cross-dataset, missing-modality, and compound shift?
- **RQ2:** Does predictive confidence become miscalibrated under these shifts?
- **RQ3:** Can uncertainty estimates reliably identify incorrect predictions under compound shift?
- **RQ4:** Can selective prediction/abstention recover safer operating regions as coverage decreases?
- **RQ5:** Do nominal conformal coverage guarantees deteriorate under cross-dataset and missing-modality shift?
- **RQ6:** After benchmark failure modes are established, can a lightweight modality-aware or shift-aware calibration method improve target-free reliability without excessive coverage loss?

RQ6 is secondary and conditional; no new method is committed at this stage.

## Scope
Subject-level splits; candidate EEG/EOG/EMG modality families; five-class Wake/N1/N2/N3/REM label space provisionally; dataset leave-one-domain-out evaluation; source-only, cross-source, and explicitly separated oracle calibration regimes; predictive, probabilistic, error-detection, selective, and conformal metrics.

## Out of scope for Step 1
Dataset downloads, preprocessing, channel harmonization implementation, model architectures, training, calibration implementation, conformal implementation, benchmark execution, literature novelty claims, and clinical validation.

## Contribution hierarchy
1. **Primary:** leakage-safe benchmark for uncertainty/reliability under cross-dataset × missing-modality shift.
2. **Secondary:** systematic analysis of calibration, error detection, selective prediction, and conformal coverage degradation.
3. **Conditional methodological contribution:** one lightweight shift/modality-aware uncertainty-calibration method, introduced only if baseline evidence identifies a specific failure mode. No complicated architecture is assumed.

## Claim boundary
This milestone establishes a protocol and software foundation only. It supports no empirical claim, clinical claim, novelty claim, or state-of-the-art claim.

## Post-Step-2 Novelty Positioning

### Established areas

Based on the literature identified in this audit, cross-dataset/domain-generalized sleep staging, multimodal sleep staging, domain/subject-invariant representation learning, and sleep-staging uncertainty quantification are already established areas. Missing/incomplete multimodal physiological signals are also directly represented by CIMSleepNet. These areas are therefore benchmark context or baselines, not standalone novelty claims.

### Remaining apparent gap

The remaining apparent gap is a rigorously leakage-safe reliability evaluation crossing held-out dataset/domain with synthetic or structural modality loss, while separating source-only calibration from oracle target calibration and measuring calibration, error detection, selective risk-coverage, and empirical conformal coverage. This is provisional because the full methods of RMSSC and the 2026 Direct Quantification paper, and source-free sleep-staging work, were not fully accessible in this audit.

### Claims we must avoid

We must not claim to be the first domain-generalized sleep-staging model, first missing-modality sleep-staging model, first sleep-staging uncertainty model, or first multimodal sleep-staging method. We must not call confidence/entropy alone calibration, call deferral alone formal selective prediction, or claim conformal guarantees on unseen domains without exchangeability evidence.

## Post-Step-2 thesis

Subject to the unresolved full-text and data-access gates, the provisional thesis is: existing sleep-staging work has separately studied cross-dataset generalization, incomplete multimodal signals, and predictive uncertainty, but the reliability of source-calibrated predictions under their compound interaction remains insufficiently characterized. ShiftSleep-UQ will therefore evaluate calibration, uncertainty-based error detection, selective prediction, and empirical conformal coverage when an unseen PSG domain is combined with modality loss, without interpreting empirical coverage as an unconditional guarantee.

## Step-2 decision

**MODIFY.** Continue the project, but narrow the primary contribution to a benchmark and reliability analysis rather than a new architecture. Treat Sleep-EDF SC/ST as separate candidate domains, defer CAP to an external pathology/device stress test, and do not freeze the primary dataset/channel configuration until the remaining official-source audit is complete.
