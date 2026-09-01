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
