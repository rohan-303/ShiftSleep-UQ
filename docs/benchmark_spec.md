# Benchmark specification (post-Step-2 draft)

**Status: PROVISIONAL and not yet frozen.** This document incorporates the source audit but still requires the Step 3 data acquisition/schema gate.

## Benchmark axes

- within-domain vs unseen-domain;
- full vs missing modality;
- single vs compound shift;
- explicit modality masks;
- dataset leave-one-domain-out evaluation;
- subject-independent splits;
- source-only vs oracle calibration.

## Deployment levels

- **S0:** source/known domain + full modalities.
- **S1:** source/known domain + synthetic modality missingness.
- **S2:** unseen dataset/domain + full modalities.
- **S3:** unseen dataset/domain + one missing modality.
- **S4:** unseen dataset/domain + multiple missing modalities.

S1/S3/S4 must distinguish synthetic masking from structural/natural channel mismatch. Structural mismatch is not a controlled modality ablation and must be analyzed as part of acquisition/domain shift.

## Domain definition

A dataset is a candidate domain, but Sleep-EDF SC and ST should initially be treated as separate candidate subdomains because their acquisition settings, study purpose, recording duration, subject/night structure, medication/placebo design, and EMG representation differ. This choice must be finalized after subject-ID and channel audits.

## Modality families and masks

EEG, EOG, and EMG remain candidate shared families. Exact channel definitions are not frozen. A provisional mask vocabulary is `{all_present, no_EEG, no_EOG, no_EMG, no_EEG_EOG, no_EEG_EMG, no_EOG_EMG}` only for protocol planning; a mask becomes admissible only when the underlying signals are verified. Natural absence and synthetic masking must use distinct condition identifiers.

## Label space

Wake/N1/N2/N3/REM remains provisional. R&K stage 3/4 to N3, movement, unknown, artifacts, unscored epochs, and scorer disagreement require source-supported mapping decisions. No mapping is frozen by convention alone.

## Calibration regimes

A. **SOURCE-ONLY / TARGET-FREE:** calibration uses source TRAIN/DEV only; the strict primary setting.
B. **CROSS-SOURCE CALIBRATION:** calibrator developed over multiple source domains without held-out-target labels.
C. **ORACLE TARGET CALIBRATION:** labeled target sample permitted only as an explicitly named upper bound.

## Candidate evaluation structure

For each held-out dataset/domain, train/model selection/calibration occur only on source TRAIN/DEV. The target test set remains untouched until protocol freeze. Where feasible, compare the same subjects across full and synthetic-mask conditions. Report domain and mask as factors and preserve the dataset×mask interaction.

## Unresolved gates

Official access/terms and exact signal inventories for ISRUC and SHHS; Sleep-EDF subject-level identity mapping; channel references and sampling by dataset; annotation conventions and mapping; dataset overlap; missingness mechanism; and exact admissible primary configuration. These are Step 3 prerequisites.

## Sources

- https://physionet.org/content/sleep-edfx/1.0.0/
- https://sleepdata.org/datasets/shhs
- https://physionet.org/content/capslpdb/1.0.0/
- https://arxiv.org/abs/2401.05363v5
- https://www.proceedings.com/079017-3557.html
