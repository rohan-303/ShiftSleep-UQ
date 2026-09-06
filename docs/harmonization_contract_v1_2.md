# ShiftSleep-UQ Harmonization Contract v1.2

## Scope

This contract governs deterministic data engineering only. It does not authorize model training, final preprocessing execution, final splits, or experimental evaluation.

## Freeze levels

`CORE_PREPROCESSING_FROZEN` means Sleep-EDF SC and ISRUC-S1 have verified subject identity, frozen source derivations or exact source-supported channel-family roles, 30-second labels, scorer policy, exclusions, missingness, and target rates sufficient to implement deterministic preprocessing.

`FINAL_BENCHMARK_FROZEN` remains `NO` until intended SHHS1 raw/XML data are legitimately acquired and every record passes schema validation.

## Primary accessible core

Sleep-EDF SC uses `EEG Fpz-Cz` and `EOG horizontal`, both native 100 Hz. ISRUC-S1 uses two exact source-supported channel-family roles at native 200 Hz:

- `LEFT_CENTRAL_EEG`: exact `C3-A2` or exact `C3-M2`.
- `LEFT_OCULAR_EOG`: exact `LOC-A2` or exact `E1-M2`.

The exact source derivation is retained. These derivations are not renamed, re-referenced, numerically equated, lowercased, fuzzy-matched, or treated as the same electrode placement. The accepted ISRUC pair allowlist is exactly:

- `C3-A2` + `LOC-A2` → `ISRUC_A1A2`.
- `C3-M2` + `E1-M2` → `ISRUC_M1M2`.

Any other pair, including `C4-M1`, `ROC-A1`, mixed-reference combinations, lowercase variants, or unknown labels, is rejected. The montage variant is mandatory metadata and a mandatory future sensitivity stratum.

No silent fallback is permitted. A source derivation outside the exact allowlist is a structural mismatch, not a synthetic missing-modality condition.

## ISRUC scoring

ISRUC scorer 1 is primary gold because the NEMAR v1.0.1 README states that events are derived from scorer-1 Excel files; scorer-2 labels are retained as annotation extras. Scorer 2 is secondary for agreement, Cohen's kappa, stage-specific disagreement, and sensitivity analyses. A valid scorer-1 epoch is not excluded because scorer 2 disagrees. Consensus-only evaluation is secondary.

## Labels and exclusions

Canonical labels are Wake, N1, N2, N3, REM. R&K stages 3 and 4 map to N3. Primary exclusions are Movement Time/non-stage events, unknown/unscored labels, explicit invalid artifact annotations, corrupt annotations, incomplete epochs, missing matching signal samples, and irreconcilable annotation/signal alignment. Valid Wake and difficult transitions remain included.

## Missingness and shifts

Synthetic missingness applies only when the raw modality exists and is intentionally masked, with an explicit modality mask. C0–C5 are all-present, one-modality-missing known/unseen-domain conditions. Removing both primary modalities is forbidden. Montage variant is an acquisition nuisance stratum and is not a C0–C5 missingness condition. Structural channel absence, unsupported derivation, unexpected rate, and incompatible representation remain separate conditions.

## Sampling

Target rates are EEG 100 Hz and EOG 50 Hz. Step 5.1 performs no resampling. Any future downsampling must specify deterministic anti-aliasing and validate each record first.

## Future montage-stratified reliability reporting

If ISRUC is evaluated under the amended family contract, all later key reliability outcomes must be separately reportable for `ISRUC_A1A2` and `ISRUC_M1M2`, including predictive performance, calibration, and selective risk/AURC. No such outcome is calculated by this contract-amendment step.

## Planned SHHS1

SHHS1 is planned primary with intended `C3-A2` EEG at nominal 125 Hz and `EOG(L)-PG1` at nominal 50 Hz. Official per-record deviations require header validation after authorized access. SHHS1 is `PLANNED_PRIMARY_DOMAIN_PENDING_RAW_ACCESS`, not acquired.

## Target-free safeguards

Held-out target data cannot inform channel selection, normalization, calibration, thresholds, checkpoint selection, hyperparameters, or model selection. Oracle target calibration is upper-bound-only. The montage-family decision was made before modeling and without model, calibration, uncertainty, stage-distribution, or target-domain results.
