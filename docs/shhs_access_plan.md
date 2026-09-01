# SHHS Access Plan

## Current state

`PUBLIC_METADATA_VERIFIED`; `RAW_ACCESS_PENDING`. The official NSRR pages expose public documentation and require a signed-in NSRR account for raw-file access. No credentials, cookies, or agreement acceptance were automated or stored.

## Official mechanism

Create/sign in to an NSRR account, review the SHHS data-use terms, and request/enable SHHS raw-file access through the dataset’s official NSRR interface. The project description should state that ShiftSleep-UQ studies target-free predictive reliability under dataset/domain and synthetic missing-modality shift, uses subject-level splits, source-only calibration, and does not redistribute raw data.

## Files required

For an initial core audit, request SHHS1 EDF signal files and their official XML scoring files; request SHHS2 only when its repeated-visit role is authorized. Metadata, documentation, and per-record headers are required before any preprocessing.

## Data-use considerations

Keep raw EDF/XML files local and immutable, honor NSRR/NHLBI terms, do not commit or redistribute restricted files, and maintain visit/participant linkage. Validate each record because official documentation warns that nominal settings have exceptions.

## Recommendation

Request SHHS1 first. Its public schema is scientifically adequate for a conditional EEG+EOG domain, but it is not considered acquired until raw access is approved and files are legally available.
