# Dataset registry (post-audit)

Facts are source-verified only where a cited official page or documentation supports them. `NOT_VERIFIED` is intentional. Recordings and subjects are distinct.

| Dataset | Official source / DOI | access / terms | subjects | recordings | PSG/modalities verified | scoring | verified status | key caveat |
|---|---|---|---|---|---|---|---|---|
| Sleep-EDF Expanded v1.0.0 | PhysioNet; DOI 10.13026/C2X676 | Open access; Open Data Commons Attribution License v1.0; official page states 8.1 GB uncompressed | SC subject count NOT_VERIFIED; ST has 22 subjects | 197 total; 153 SC files; 44 ST files | EEG Fpz-Cz/Pz-Oz; horizontal EOG; chin EMG; some SC respiration/temp; SC EEG/EOG 100 Hz and chin EMG envelope 1 Hz; ST EEG/EOG/EMG 100 Hz | R&K; W,R,1,2,3,4,M,? | PARTIAL | repeated nights, substudy/device/medication differences, EMG representation differs |
| ISRUC-Sleep | Official site inaccessible in this environment | access/terms NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | must not be used until official audit |
| Sleep Heart Health Study (SHHS) | NSRR official page; DOI 10.25822/ghy8-ks59 | NSRR access mechanism and terms require account/page audit | 6,441 enrolled at Visit 1; 3,295 had Visit 2 PSG; available PSG subject count NOT_VERIFIED | NOT_VERIFIED from audited page | montage/sampling documentation exists on NSRR but exact channel table not extracted in this step | NOT_VERIFIED from audited page | PARTIAL | repeated participants across visits; multi-cohort design; exact usable PSG/channel inventory pending |
| CAP Sleep Database v1.0.0 | PhysioNet official page; DOI NOT_VERIFIED on page | Open access; license link on official page | 16 healthy subjects; pathological recording-level breakdown is documented; unique pathological subject count NOT_VERIFIED | 108 recordings | at least 3 EEG; 2 EOG; submentalis and bilateral anterior tibial EMG; respiration/SaO2/ECG | R&K macrostructure; CAP annotations by Terzano rules; W,R,S1-S4,REM,MT | PARTIAL | pathology/device/population stress test; R&K and richer channels reduce primary comparability |

## Sleep-EDF substudies

The official PhysioNet page states 197 whole-night recordings, not 197 people. Sleep Cassette (SC) contains 153 files from a 1987–1991 age-effects study of healthy Caucasians aged 25–101; file names encode subject and night, and several nights were lost. Its EEG and EOG were sampled at 100 Hz, while the chin EMG was filtered, rectified, low-pass filtered, and sampled as a 1-Hz RMS envelope. Sleep Telemetry (ST) contains 44 files from 22 Caucasian subjects, two nights per subject, in a 1994 temazepam/placebo study; EEG, EOG, and EMG were sampled at 100 Hz. Both use manually scored R&K annotations with W, R, stages 1–4, movement, and not-scored labels.[1]

**Recommendation:** treat SC and ST as separate candidate domains/subdomains, not as one homogeneous domain, until subject-level identifiers, recording-device effects, medication/night pairing, and channel representation are modeled. A conservative primary benchmark may select SC only for an initial healthy within-dataset baseline, while using ST only if the protocol explicitly treats telemetry/medication as a separate domain. Do not report “197 subjects.”

## Sources
[1] https://physionet.org/content/sleep-edfx/1.0.0/
[2] https://sleepdata.org/datasets/shhs
[3] https://physionet.org/content/capslpdb/1.0.0/

## Step 4 audit status (2026-09-01)

| Dataset | Verified status | Provenance |
|---|---|---|
| Sleep-EDF Expanded 1.0.0 | 197 records; 153 SC and 44 ST; 196/197 PSG headers parsed by official PhysioNet HTTP Range | Official page, `RECORDS`, `reports/sleep_edf_subject_manifest.csv`, `reports/sleep_edf_channel_inventory.csv` |
| ISRUC-Sleep | ACCESS_UNRESOLVED; audited official URL returned 404 | `reports/dataset_access_registry.csv` |
| SHHS | RAW_ACCESS_PENDING; schema NOT_VERIFIED in this run | `reports/dataset_access_registry.csv` |
| CAP Sleep Database 1.0.0 | 108 official records; 13/108 headers parsed in final network window; heterogeneous schema | Official page, `reports/cap_channel_inventory.csv` |

Unverified values remain `NOT_VERIFIED`, `ACCESS_UNRESOLVED`, or `RAW_ACCESS_PENDING`; no model-ready dataset claim is made.
