# Research Specification — Step 3 Thesis Freeze

## Problem

ShiftSleep-UQ studies whether multimodal sleep-staging systems know when they are unreliable under unseen PSG dataset/domain shift, physiological modality loss, and their interaction. The project is about reliability and safe selective use, not merely accuracy.

## Frozen research questions

1. How do predictive performance and probability calibration change across known-domain/full-modality, missing-modality, unseen-domain/full-modality, and compound-shift conditions?
2. How effectively do uncertainty scores identify incorrect predictions and support formal selective prediction as shift severity changes, and can ranking quality dissociate from probability calibration?
3. How does empirical conformal coverage and prediction-set size change when source-calibrated sets are transferred to unseen domains and modality-loss conditions?
4. Are reliability failures attributable primarily to domain shift, modality loss, or their interaction after accounting for subject clustering, dataset heterogeneity, and channel/label confounds?

## Scope

The planned benchmark evaluates five provisional conditions S0–S4, separates synthetic masking from structural channel absence, preserves subject identity, and compares source-only, cross-source, and explicitly labeled oracle calibration regimes. EEG/EOG/EMG remain candidate modality families pending schema verification. Five-class labels remain provisional until annotation mapping is audited.

## Out of scope for the thesis freeze

Dataset download, preprocessing implementation, neural architecture design, training, performance claims, clinical validation, target-label tuning in the primary setting, and unconditional conformal guarantees under shift.

## Contribution hierarchy

1. **Primary benchmark:** subject- and dataset-leakage-safe reliability benchmark crossing held-out PSG dataset/domain and modality availability.
2. **Secondary analysis:** calibration, correctness ranking, formal selective risk-coverage, and empirical conformal coverage degradation.
3. **Conditional method:** one lightweight modality/shift-aware calibration method only after a reproducible baseline failure is demonstrated and the method is separately preregistered.

## Scientific decision

Step 3 remains a research gate. The bounded audit supports MODIFY: proceed to source-verified dataset acquisition/schema auditing, while retaining unresolved RMSSC and Direct Quantification collision risk and making no priority claim.
