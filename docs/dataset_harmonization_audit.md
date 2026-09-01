# Dataset Harmonization Audit — Step 3 Gate Status

Step 3 did not acquire or download PSG datasets. The Step 2 source audit remains the data-feasibility baseline.

## Gate status

- Sleep-EDF Expanded SC/ST: candidate substudy separation remains required; unique-subject identity and exact header audit remain open.
- ISRUC-Sleep: official access/channel/scoring facts remain NOT_VERIFIED.
- SHHS: exact usable PSG inventory, participant identity across visits, montage/reference/sampling details, and access workflow remain open.
- CAP: external pathology/device/scoring stress-test role remains; exact per-signal sampling and redistribution terms require verification.

## Harmonization rule

Do not collapse EEG, EOG, and EMG family labels into exact channel equivalence. Preserve montage, reference, sampling, raw-versus-envelope representation, provenance, and missingness type. Synthetic masking and structural absence must receive different condition identifiers.

## Step 3 decision

No dataset is admitted to preprocessing from this document. Step 4 should begin with an official-source acquisition and raw-schema audit only after the reviewer accepts the qualified MODIFY decision.
