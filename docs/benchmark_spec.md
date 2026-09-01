# Benchmark specification (post-Step-2 draft)

**Status: STEP 5.1 AMENDED / CORE_PREPROCESSING_FROZEN.** Deterministic preprocessing engineering may be implemented for the accessible Sleep-EDF SC + ISRUC-S1 core. The final three-domain benchmark remains incomplete until SHHS1 is authorized, acquired, and per-record validated.

## Benchmark axes

- within-domain vs unseen-domain;
- full vs missing modality;
- single vs compound shift;
- explicit modality masks;
- dataset leave-one-domain-out evaluation;
- subject-independent splits;
- source-only vs oracle calibration.

## Deployment levels

- **C0:** known domain + EEG + EOG.
- **C1:** known domain + EEG only (synthetic EOG loss).
- **C2:** known domain + EOG only (synthetic EEG loss).
- **C3:** unseen domain + EEG + EOG.
- **C4:** unseen domain + EEG only (compound dataset + synthetic EOG loss).
- **C5:** unseen domain + EOG only (compound dataset + synthetic EEG loss).

S1/S3/S4 must distinguish synthetic masking from structural/natural channel mismatch. Structural mismatch is not a controlled modality ablation and must be analyzed as part of acquisition/domain shift.

## Domain definition

A dataset is a candidate domain, but Sleep-EDF SC and ST should initially be treated as separate candidate subdomains because their acquisition settings, study purpose, recording duration, subject/night structure, medication/placebo design, and EMG representation differ. This choice must be finalized after subject-ID and channel audits.

## Modality families and masks

EEG and EOG are the primary families. EMG is secondary compatible-subset only because Sleep-EDF SC supplies a 1-Hz RMS envelope while ST supplies 100-Hz EMG. The primary mask vocabulary is `{all_present, no_EEG, no_EOG}`; removing both primary families is forbidden. Natural absence and synthetic masking have distinct identifiers.

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
