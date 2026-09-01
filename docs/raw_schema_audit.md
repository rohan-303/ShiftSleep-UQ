# Raw schema audit

Audit date: 2026-09-01. Sources are official provider pages and header-only HTTP Range requests. No signal samples were read.

## Sleep-EDF Expanded

### Subject structure
PhysioNet documents 153 SC recordings and 44 ST recordings. The official filename rules support 78 SC subject identifiers and 22 ST subject identifiers in the generated manifest. SC has two possible nights per subject, with explicitly documented missing nights: SC subject 36 night 1, subject 52 night 1, and subject 13 night 2. ST has two nights per subject, one temazepam and one placebo; the per-night treatment assignment must be read from the official spreadsheet before modeling.

### Recording structure
SC and ST are separate cohorts/studies, not interchangeable records. IDs are derived only from `SC4<ss><N><E/O>-PSG.edf` and `ST7<ss><N>J0-PSG.edf` naming documented by PhysioNet.

### Channel schema
All 196 successfully inspected headers had one of two schemas: 152 SC files with EEG Fpz-Cz, EEG Pz-Oz, horizontal EOG, oro-nasal respiration, submental EMG, rectal temperature, event marker; and 44 ST files with EEG Fpz-Cz, EEG Pz-Oz, horizontal EOG, EMG submental, Marker. One SC header request failed transiently and is retained as unresolved.

### Sampling frequencies and representations
SC EEG/EOG are 100 Hz; SC submental EMG is a processed high-pass-filtered, rectified, low-pass-filtered 1-Hz RMS envelope; SC respiration, temperature, and marker are 1 Hz. ST EEG/EOG/EMG are 100 Hz and event marker is 1 Hz. This is a fundamental SC/ST EMG representation difference.

### Annotation schema
PhysioNet documents EDF+ hypnograms with W, R, 1, 2, 3, 4, M, and `?`, manually scored under 1968 R&K. PSG files are EDF and hypnograms EDF+. Annotation files were not downloaded as a separate signal audit in this step.

### Access/legal constraints
Open access under the provider's ODC Attribution License v1.0, subject to license terms. Full archive is 8.1 GB; not downloaded.

### Known irregularities
SC/ST channel sets differ; ST unrecorded signals were removed; event-marker labels differ; SC includes low-rate derived EMG while ST EMG is 100 Hz. These prevent treating exact EMG as harmonized without an explicit secondary contract.

### Suitability
Strong candidate for a source-domain audit and EEG+EOG primary core. SC/ST should not be treated as independent domains if the scientific question is dataset shift across cohorts without accounting for substudy structure.

## ISRUC-Sleep

The audited historical official URL returned HTTP 404. No unofficial mirror was used. S1/S2/S3 semantics, identity, channels, scoring, license, and raw access are `ACCESS_UNRESOLVED` / `NOT_VERIFIED`.

## SHHS

The NSRR page could not be extracted in this environment because of certificate verification failure. Raw access is account/access controlled and remains `RAW_ACCESS_PENDING`. SHHS1/SHHS2 visit linkage, exact montage, frequencies, annotation, and terms require fresh official verification before inclusion.

## CAP Sleep Database

The official PhysioNet page documents 108 records, 16 healthy subjects, and 92 pathological recordings across pathology-coded groups. It documents at least three EEGs, two EOGs, submentalis EMG, bilateral tibial EMG, respiration, SaO2, ECG, R&K macrostructure annotations, and CAP annotations. Header-range inspection parsed 13 records in the available network window and found substantial channel-label and sampling heterogeneity; 95 requests failed due transient DNS/network errors and are not treated as inspected. CAP is therefore an external stress-test candidate, not a frozen primary domain.

## Remaining blockers
Official SHHS/ISRUC access and schema verification; complete CAP header audit; direct annotation-file inventory; treatment assignment extraction from ST spreadsheet; and a source-supported decision about whether SC/ST EMG can be secondary only.
