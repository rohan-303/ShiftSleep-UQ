# ShiftSleep-UQ Harmonization Contract v1

## Scope

This is a Step 5 protocol artifact, not preprocessing code. It defines a partial freeze for a target-free reliability benchmark. `CONTRACT_PARTIAL` means Step 6 is not authorized.

## Dataset Roles

Sleep-EDF SC is the primary provisional domain. Sleep-EDF ST is secondary medication/acquisition stress. SHHS is a conditional primary candidate with public schema verified but raw access pending. ISRUC-S1/S2/S3 are deferred until original channel and annotation semantics are resolved. CAP is an external stress candidate only.

## Subject Identity

SC uses the official filename subject token and groups all nights. ST groups both placebo/temazepam nights. ISRUC uses NEMAR participant IDs and keeps all S2 sessions together. SHHS groups all visits by participant. CAP has no subject-level inference until identity is resolved.

## Canonical Labels

Wake, N1, N2, N3, REM. R&K Stage 3 and Stage 4 map to N3 because AASM N3 supersedes the former two deep-sleep stages. Source labels are retained until deterministic mapping; unknown labels never map to Wake.

## Exclusions

Movement time, unknown, `?`, artifact, unscored, corrupt annotation, incomplete epoch, missing signal samples, and scorer-disagreement epochs are excluded from primary supervised stage evaluation. Excluded labels are not relabeled as Wake.

## Scorer Policy

For Sleep-EDF, use the official distributed hypnogram stream. ISRUC’s two streams are retained separately; a primary stream is not frozen until the original representation is verified. The secondary analysis will report scorer disagreement/agreement sensitivity, never an outcome-driven choice.

## Wake Policy

Preserve every valid scored 30-second epoch, including Wake. Any label-derived trimming is secondary only because target-free input selection must not use true sleep labels.

## Epoch Policy

Canonical duration is 30 seconds. Reject or quarantine incomplete final epochs, overlapping annotations, unresolvable clock offsets, and signal/annotation duration mismatches. Record-level validation precedes extraction.

## Primary Modalities

EEG and EOG are primary. EMG is `SECONDARY` only for a verified compatible subset; SC’s 1-Hz RMS envelope is never treated as raw chin EMG equivalent to ST/SHHS.

## Channel Selection

SC provisional selection is one documented EEG and one documented horizontal EOG channel. SHHS uses one C3-A2 or C4-A1 EEG and one left/right EOG only after per-record validation. ISRUC selection is intentionally unresolved. No silent fallback is allowed.

## Sampling Policy

No Step 5 resampling occurred. Step 6 target policy is EEG 100 Hz and EOG 50 Hz with modality-specific lengths, subject to per-record validation and explicit anti-aliasing design. Native rates are preserved in manifests.

## EMG Policy

Secondary compatible-subset or separate representation-mismatch stress condition only. Compatibility requires verified channel meaning, reference, sampling, units, and representation; otherwise exclude from the EMG track.

## Synthetic Missingness

A synthetic missing modality exists in the raw record but is withheld at condition time. The future representation must include an explicit availability mask and cannot remove both EEG and EOG. Synthetic condition identifiers are distinct from natural absence.

## Structural Mismatch

Unacquired modality, unavailable required channel, incompatible EMG representation, or corrupt required channel is structural. Disposition is record exclusion or separate stress analysis; it is never encoded as ordinary synthetic masking.

## Shift Taxonomy

C0 known/full EEG+EOG; C1 known/EEG-only; C2 known/EOG-only; C3 unseen/full; C4 unseen/EEG-only; C5 unseen/EOG-only. Structural mismatch conditions are separate and not relabeled C1/C2/C4/C5.

## Split Rules

All splitting is subject-level. SC nights, ST treatment nights, ISRUC-S2 sessions, and SHHS visits remain together. Within-domain intent is train/dev/test. Cross-domain intent is source train/dev/source calibration/held-out target test; final memberships are not generated here.

## Target-Free Rules

Held-out target data cannot inform normalization, temperature/calibrator fitting, abstention thresholds, conformal calibration, checkpoint choice, hyperparameters, channel selection, or model selection. Oracle target calibration is a separately named upper bound.

## Dataset Scale Policy

SHHS use may be all records, deterministic subject subset, dataset-balanced subject sampling, or a documented combination. It must be subject-level, outcome-independent, and reproducible; no final subset is selected in Step 5.

## Schema Validation

Raw data remain immutable. Every record requires header/channel validation, required EEG/EOG presence, 30-second annotation alignment, explicit units/reference interpretation, and rejection on ambiguous identity or unsupported fallback.

## Known Confounds

Cohort health status, medication, home versus clinical acquisition, hardware/version rates, repeated nights/visits, annotation source, and channel-reference differences may be domain cues. They must be reported, not silently harmonized.

## Frozen vs Optional Decisions

Frozen: primary families, C0–C5 semantics, exclusion principles, Wake policy, subject grouping, target-free rules, structural/synthetic separation. Optional or blocked: ISRUC original semantics, SHHS raw approval/per-record validation, CAP identity, final split lists, SHHS scale choice, EMG compatible subset.

## Conditions Requiring Contract v2

Any change to primary dataset roles, ISRUC scorer/channel semantics, SHHS access or per-record deviations, annotation mapping, sampling target, missingness representation, or split policy requires a new version and amendment entry.
