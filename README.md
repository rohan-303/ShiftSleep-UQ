# ShiftSleep-UQ

**Working title:** *ShiftSleep-UQ: Calibration and Selective Reliability of Multimodal Sleep Staging Under Compound Dataset and Missing-Modality Shift*

## Objective
ShiftSleep-UQ is a research benchmark for testing whether multimodal sleep-staging systems know when they are likely to fail under subject shift, cross-dataset/domain shift, missing physiological modalities, and their combination. The scientific focus is reliability—not accuracy alone.

This repository is at **Foundation/Idea** status. No datasets have been downloaded, no models trained, and no empirical results are claimed.

## Research questions
RQ1 performance deterioration; RQ2 confidence calibration under shift; RQ3 uncertainty-based error detection; RQ4 selective prediction; RQ5 conformal coverage under shift; RQ6 a conditional, lightweight modality/shift-aware calibration method after baseline failure analysis.

## Benchmark philosophy
Evaluation is subject-independent, dataset-aware, and test-isolated. Candidate shared modality families are EEG, EOG, and EMG; channel harmonization and five-class label mapping remain unverified. Planned deployment levels are S0 known/full, S1 known/missing, S2 unseen/full, S3 unseen/single-missing, and S4 unseen/multiple-missing.

## Reproducibility and safety
Seeds, configurations, software/hardware, provenance, checksums where permitted, manifests, and machine-readable outputs must be recorded. Raw data are immutable. PSG epochs from one participant are correlated and are not independent statistical observations. This is research software, **not a diagnostic medical device**; it must not be used for clinical decisions.

## Structure
- `docs/` research and evaluation contracts
- `configs/` future experiment configurations
- `data/` provenance/readme boundary; no data in this bootstrap
- `src/shiftsleep_uq/` minimal package boundary
- `tests/` smoke tests
- `reports/` milestone reports
- `scripts/` future reproducible entry points

## Environment setup (placeholder)
Use Python 3.11+ and an isolated environment. The bootstrap intentionally does not install large ML or dataset dependencies. Future setup commands will be frozen after the dataset/channel audit.

## Roadmap
1. **Step 1:** repository bootstrap and protocol documentation (current).
2. Source-verified literature, dataset, licensing, annotation, and channel-harmonization audit.
3. Freeze benchmark schemas, split manifests, preprocessing contract, and baseline models.
4. Implement and validate leakage-safe baselines and uncertainty metrics.
5. Execute multi-seed benchmark and subject-level statistical analysis.
6. Consider the conditional calibration method only if a specific baseline failure mode is demonstrated.
