# Competitor Boundary

This document freezes a conservative, non-priority boundary. `NOT_VERIFIED` is retained where publisher access prevented method inspection.

## SleepDG
**They study:** Generalizable sleep staging using multi-level domain alignment across public datasets; domain-generalization performance is central.

**We study:** Reliability of source-calibrated predictions across a factorial of known/unseen dataset conditions and modality availability, including calibration, correctness ranking, selective risk-coverage, and empirical conformal coverage.

**Overlap:** Unseen-dataset evaluation and domain shift.

**Non-overlap:** Reliability endpoints and missing-modality interaction were not verified in the accessible SleepDG record.

**Claim we must avoid:** “First cross-dataset sleep-staging method” or “SleepDG does not use multiple datasets.”

## CIMSleepNet
**They study:** Robust sleep staging over incomplete multimodal physiological signals through contrastive imagination.

**We study:** Benchmarking how reliability changes under explicit synthetic versus structural modality loss crossed with held-out dataset/domain shift.

**Overlap:** Missing/incomplete multimodal signals.

**Non-overlap:** Cross-dataset reliability factorial, formal calibration, selective risk-coverage, and conformal transfer were not verified in accessible evidence.

**Claim we must avoid:** “First missing-modality sleep-staging study.”

## RMSSC
**They study:** A 2026 ICASSP proceedings paper whose verified title concerns robust multimodal sleep staging with noisy labels and missing modalities. Exact datasets, masks, splits, and reliability endpoints are NOT_VERIFIED because IEEE full text was inaccessible.

**We study:** A pre-specified target-free reliability benchmark with dataset/domain × modality interaction.

**Overlap:** Multimodal missingness and possibly robustness.

**Non-overlap:** Cannot be asserted until full methods are inspected; simultaneous held-out-dataset plus modality-loss and calibration/selective/conformal scope remain NOT_VERIFIED.

**Claim we must avoid:** “RMSSC does not evaluate compound shift.”

## SleepTransformer
**They study:** Sleep staging with interpretability and entropy/uncertainty analysis across two databases; uncertainty motivates deferral.

**We study:** Formal calibration, error detection, risk-coverage, and empirical conformal coverage under controlled shift conditions.

**Overlap:** Sleep-staging uncertainty and possible rejection/deferral.

**Non-overlap:** Strict target-free compound-shift reliability was not verified.

**Claim we must avoid:** “No previous sleep-staging paper used uncertainty.”

## U-PASS
**They study:** An uncertainty-guided pipeline spanning acquisition, training, and deployment; the accessible PubMed record describes supervised pretraining and recording-wise semi-supervised fine-tuning.

**We study:** Source-only target-free transfer evaluation with no target data before final evaluation, and reliability metrics under domain × modality shift.

**Overlap:** Operational uncertainty in sleep staging.

**Non-overlap:** Exact calibration, shift, selective, and conformal protocol NOT_VERIFIED.

**Claim we must avoid:** Equating a general uncertainty-guided pipeline with calibrated probabilities under unseen-domain shift.

## DREAM
**They study:** Domain-invariant representation learning and sleep-dynamics modeling, with new-subject/generalization and uncertainty analysis.

**We study:** A reliability factorial whose primary factors are dataset/domain condition and modality availability.

**Overlap:** Domain invariance/generalization and uncertainty.

**Non-overlap:** Cross-dataset calibration and compound missing-modality reliability were not verified.

**Claim we must avoid:** Treating subject-held-out generalization as equivalent to leave-one-dataset-out domain shift.

## Direct Quantification
**They study:** Direct uncertainty quantification for automatic sleep staging; exact model, data, MC-dropout, Hypnodensity Interval, rejection, and calibration details are NOT_VERIFIED from accessible primary text.

**We study:** Reliability transfer under controlled compound shift, including distinction between confidence ranking and probability calibration.

**Overlap:** Direct sleep-staging uncertainty and potentially uncertainty-based rejection.

**Non-overlap:** NOT_VERIFIED until full text is accessible.

**Claim we must avoid:** Claiming formal risk-coverage or absence of calibration without reading the paper.

## SF-UIDA
**They study:** Zhou et al., “Personalized Sleep Staging Leveraging Source-free Unsupervised Domain Adaptation,” AAAI 2025, pp. 14529–14537, DOI 10.1609/aaai.v39i13.33592. The official abstract describes two-step subject-specific adaptation to each newly appearing unlabeled individual without source data, evaluated on three public datasets and three classic staging models.

**We study:** Primary target-free domain generalization: no target data, labeled or unlabeled, before final evaluation.

**Overlap:** Unseen target generalization and strict source-free terminology.

**Non-overlap:** SF-UIDA adapts using unlabeled target individuals; it is not pure no-target-data domain generalization. Missing modalities, calibration, selective prediction, and conformal prediction were not described in the official abstract.

**Claim we must avoid:** Calling SF-UIDA a target-free domain-generalization baseline.

## Terminology boundary

- **Target-free domain generalization:** target data are not accessed before evaluation.
- **Unsupervised target-domain adaptation:** unlabeled target data are accessed and used to adapt; target labels are withheld.
- **Source-free unsupervised adaptation:** source data are unavailable during adaptation, but unlabeled target data are used.

ShiftSleep-UQ's primary protocol is the first category. Any adaptation experiment must be separately named and excluded from the main target-free result.
