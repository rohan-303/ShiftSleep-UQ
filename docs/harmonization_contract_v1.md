# ShiftSleep-UQ Harmonization Contract v1.1

## Scope

This contract governs deterministic data engineering only. It does not authorize model training, final preprocessing execution, final splits, or experimental evaluation.

## Freeze levels

`CORE_PREPROCESSING_FROZEN` means Sleep-EDF SC and ISRUC-S1 have verified subject identity, exact primary EEG/EOG labels, 30-second labels, scorer policy, exclusions, missingness, and target rates sufficient to implement deterministic preprocessing.

`FINAL_BENCHMARK_FROZEN` remains `NO` until intended SHHS1 raw/XML data are legitimately acquired and every record passes schema validation.

## Primary accessible core

Sleep-EDF SC uses `EEG Fpz-Cz` and `EOG horizontal`, both native 100 Hz. ISRUC-S1 uses `C3-A2` EEG and `LOC-A2` EOG, both native 200 Hz. These are modality-family choices, not claims of exact electrode or reference equivalence. Montage/reference differences remain an explicit domain-shift component.

No silent fallback is permitted. Missing exact channels are structural mismatches and are quarantined or excluded from the exact-channel condition.

## ISRUC scoring

ISRUC scorer 1 is primary gold because the NEMAR v1.0.1 README states that events are derived from scorer-1 Excel files; scorer-2 labels are retained as annotation extras. Scorer 2 is secondary for agreement, Cohen's kappa, stage-specific disagreement, and sensitivity analyses. A valid scorer-1 epoch is not excluded because scorer 2 disagrees. Consensus-only evaluation is secondary.

## Labels and exclusions

Canonical labels are Wake, N1, N2, N3, REM. R&K stages 3 and 4 map to N3. Primary exclusions are Movement Time/non-stage events, unknown/unscored labels, explicit invalid artifact annotations, corrupt annotations, incomplete epochs, missing matching signal samples, and irreconcilable annotation/signal alignment. Valid Wake and difficult transitions remain included.

## Missingness and shifts

Synthetic missingness applies only when the raw modality exists and is intentionally masked, with an explicit modality mask. C0–C5 are all-present, one-modality-missing known/unseen-domain conditions. Removing both primary modalities is forbidden. Structural channel absence, unexpected rate, and incompatible representation are separate conditions.

## Sampling

Target rates are EEG 100 Hz and EOG 50 Hz. Step 5.1 performs no resampling. Any future downsampling must specify deterministic anti-aliasing and validate each record first.

## Planned SHHS1

SHHS1 is planned primary with intended `C3-A2` EEG at nominal 125 Hz and `EOG(L)-PG1` at nominal 50 Hz. Official per-record deviations require header validation after authorized access. SHHS1 is `PLANNED_PRIMARY_DOMAIN_PENDING_RAW_ACCESS`, not acquired.

## Target-free safeguards

Held-out target data cannot inform channel selection, normalization, calibration, thresholds, checkpoint selection, hyperparameters, or model selection. Oracle target calibration is upper-bound-only.
