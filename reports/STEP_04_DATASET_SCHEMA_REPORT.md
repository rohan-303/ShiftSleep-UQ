# ShiftSleep-UQ Step 4 Dataset Schema Report

## 1. Status

PARTIAL

The metadata-first audit produced useful verified Sleep-EDF evidence and partial CAP header evidence. ISRUC and SHHS remain access/schema unresolved, CAP could not be completed because of network failures, and the label/exclusion/trimming contract is not ready to freeze.

## 2. Dataset Gate

SCHEMA_PARTIAL

## 3. Repository State

* path: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* Step 3 commit: `1cc17ddc3824194380bca746fb107d677bdc4041` (substantive thesis-freeze commit)
* Step 3 report commit if separate: `659d864afe1acfa005375370c99763f9ca020c5d` (`docs: record Step 3 novelty gate report`)
* Step 4 commit: to be recorded after this report is finalized and committed
* push status: NOT_PUSHED; no GitHub push performed

## 4. Acquisition Summary

| Dataset | Official source | Access state | Material acquired | Local bytes | Checksums | Full signal data downloaded? |
|---|---|---|---|---:|---|---|
| Sleep-EDF Expanded 1.0.0 | https://physionet.org/content/sleep-edfx/1.0.0/ | Open under ODC Attribution License v1.0 terms | RECORDS, SHA256SUMS.txt, SC/ST spreadsheets; remote headers only | metadata files only; exact sizes preserved in acquisition manifest where measured | official metadata files matched locally; checksum-file status is NO_OFFICIAL_CHECKSUM | No |
| ISRUC-Sleep | https://sleeptight.isr.uc.pt/ | ACCESS_UNRESOLVED; audited URL returned 404 | None | 0 | NOT_APPLICABLE | No |
| SHHS | https://sleepdata.org/datasets/shhs | Public page extraction failed with certificate verification; raw access requires official account/access path | None | 0 | NOT_APPLICABLE | No |
| CAP Sleep Database 1.0.0 | https://physionet.org/content/capslpdb/1.0.0/ | Open official page; range audit partial | RECORDS, gender-age.xlsx; 13 remote headers parsed in final network window | metadata only | RECORDS locally hashed; demographic file has NO_OFFICIAL_CHECKSUM | No |

No credentials, cookies, tokens, restricted annotations, or full EDF signal bodies were acquired.

## 5. Sleep-EDF Subject Audit

* SC unique subjects: **78**, derived from official documented filename rule; SC recordings: **153**.
* ST unique subjects: **22**, derived from official documented filename rule; ST recordings: **44**.
* repeated-night structure: SC uses up to two nights per subject. PhysioNet explicitly documents missing SC subject 36 night 1, subject 52 night 1, and subject 13 night 2. ST has two nights per subject, one temazepam and one placebo.
* missing recordings: the three documented SC missing nights; no additional missing-record conclusion was inferred.
* treatment structure: ST one temazepam and one placebo night per participant is verified at study-description level; exact filename-to-condition assignment remains to be extracted from `ST-subjects.xls` before modeling.
* subject-ID derivation rule: `SC4<ss><N><E/O>-PSG.edf` and `ST7<ss><N>J0-PSG.edf`; IDs are `SC_<ss>` or `ST_<ss>`. This is a high-confidence filename rule, not a claim that SC and ST subject numbers refer to the same people.
* verification source: official Sleep-EDF page and local official `RECORDS`; generated artifact `reports/sleep_edf_subject_manifest.csv`.

Subjects, nights, and recordings are separate fields. SC and ST are separate substudies and cohorts.

## 6. Sleep-EDF Raw Schema

* number of recording headers inspected: **196/197** successfully parsed by HTTP Range; one (`SC4721E0-PSG.edf`) failed with a transient connection reset and remains unverified.
* distinct channel schemas: **2** among successful records: 152 SC records and 44 ST records.
* sampling rates: SC: EEG/EOG 100 Hz, EMG/respiration/temperature/event marker 1 Hz; ST: EEG/EOG/EMG 100 Hz, marker 10 Hz in the inspected headers. The official documentation describes ST event marker at 1 Hz; this discrepancy is retained as a header-vs-page issue requiring review.
* EEG details: `EEG Fpz-Cz` and `EEG Pz-Oz`, 100 Hz in both schemas.
* EOG details: `EOG horizontal`, 100 Hz in both schemas.
* EMG details: SC `EMG submental`, documented processed 1-Hz RMS envelope; ST `EMG submental`, 100 Hz.
* SC/ST differences: SC adds `Resp oro-nasal`, `Temp rectal`, and `Event marker`; ST has `Marker` and a different EMG representation. PhysioNet says ST unrecorded signals were removed.
* annotation labels: official documentation reports W, R, 1, 2, 3, 4, M, and `?` in EDF+ hypnograms; direct annotation-file parsing was not performed.
* anomalies: one transiently unavailable SC header; the ST marker sampling discrepancy above; EDF PSG headers parsed as non-EDF+ while hypnograms are EDF+.

## 7. ISRUC Audit

* access status: ACCESS_UNRESOLVED; the audited official URL `https://sleeptight.isr.uc.pt/ISRUC/` returned HTTP 404.
* S1/S2/S3 meaning: NOT_VERIFIED.
* subjects/recordings: NOT_VERIFIED.
* channels: NOT_VERIFIED.
* sampling: NOT_VERIFIED.
* annotations: NOT_VERIFIED.
* identity handling: no subject identity inferred and no unofficial mirror used.
* unresolved facts: hosting institution, group semantics, repeated sessions, modalities, scoring standard, scorer information, demographics/pathology, license, registration, and download method.

## 8. SHHS Audit

* SHHS1 structure: NOT_VERIFIED from the official page in this run.
* SHHS2 structure: NOT_VERIFIED from the official page in this run.
* repeat-visit rules: NOT_VERIFIED; must group all official visits by participant when access is authorized.
* channels: NOT_VERIFIED; prompt examples such as C3-A2/C4-A1, EOG, and chin EMG were not accepted without source confirmation.
* sampling: NOT_VERIFIED.
* annotations: NOT_VERIFIED.
* access state: NSRR account/access controls indicated by the official resource context; exact terms require successful official page audit.
* raw-access status: RAW_ACCESS_PENDING. No credentials were requested or stored.

## 9. CAP Audit

* subjects/recordings: official page documents 16 healthy subjects and 92 pathological recordings, totaling 108 recordings. Recording-level subject mapping is not established.
* healthy/pathology structure: official filename groups include controls, bruxism, insomnia, narcolepsy, NFLE, PLM, RBD, and SDB.
* channel heterogeneity: 13 successful range-parsed headers showed multiple distinct label orders/sets, including bipolar and referenced EEG, ROC/LOC EOG, EMG1-EMG2, tibial channels, respiratory, ECG, and oximetry channels.
* sampling: heterogeneous in successful headers, with observed rates including 128, 256, 512, 64, 8, and 1 Hz depending on channel.
* annotations: official page documents R&K W/S1-S4/R/MT macrostructure and CAP-specific phase-A annotations; `.txt` and `.edf.st` records are available.
* suitability as stress test: YES, provisionally. CAP has independent clinical/pathological context and substantial schema heterogeneity, but it is not ready as a primary harmonized domain.

The final range run parsed 13/108 headers; 95 attempts failed with network/DNS errors. The failed records are retained in `reports/cap_channel_inventory.csv` and are not treated as inspected.

## 10. Optional Dataset

NO_ADDITIONAL_DATASET_SELECTED

ISRUC and SHHS are required unresolved candidates; adding a fifth dataset before resolving them would add complexity without verified primary-benchmark benefit.

## 11. Dataset Overlap Findings

* Sleep-EDF SC and ST are distinct substudies but must not be treated as independent people or casually collapsed.
* Older Sleep-EDF/sleep-edf-20 names may be derived subsets of Sleep-EDF and cannot be used as an independent domain without source-lineage checking.
* Repeated SC nights and ST treatment/placebo nights create within-subject leakage risk.
* SHHS1/SHHS2 repeated visits must be grouped by participant once identifiers are verified.
* CAP pathology prefixes are recording/category labels, not verified subject IDs.
* Converted EDF, hypnogram, `.st`, and benchmark copies must map to one canonical source recording.
* Filename differences do not establish dataset independence.

Rules are defined in `docs/dataset_overlap_policy.md`.

## 12. Subject Identity Safety

| dataset | classification | reason |
|---|---|---|
| Sleep-EDF SC | SAFE_WITH_RULES | Official filename convention supports subject/night grouping; all nights must remain together and missing nights preserved. |
| Sleep-EDF ST | SAFE_WITH_RULES | Official filename convention supports subject/night grouping; treatment/placebo nights must remain together; exact condition assignment remains pending. |
| ISRUC S1/S2/S3 | UNRESOLVED | Official access and group/identity semantics unavailable. |
| SHHS1/SHHS2 | UNRESOLVED | Official participant/visit semantics not verified in this run; raw access pending. |
| CAP | UNRESOLVED | Official page gives aggregate healthy/pathology counts, but no verified recording-to-subject mapping. |

## 13. Channel Compatibility Matrix

| Dataset | EEG | EOG | EMG |
|---|---|---|---|
| Sleep-EDF SC | COMPATIBLE_WITH_SHIFT: Fpz-Cz/Pz-Oz, 100 Hz | COMPATIBLE_WITH_SHIFT: horizontal EOG, 100 Hz | QUESTIONABLE: 1-Hz processed submental RMS envelope |
| Sleep-EDF ST | COMPATIBLE_WITH_SHIFT: Fpz-Cz/Pz-Oz, 100 Hz | COMPATIBLE_WITH_SHIFT: horizontal EOG, 100 Hz | QUESTIONABLE: 100-Hz submental signal differs from SC envelope |
| CAP | QUESTIONABLE: multiple referenced/bipolar EEG sets, heterogeneous rates | QUESTIONABLE: ROC-LOC/LOC-ROC and other label/order variation | QUESTIONABLE: submentalis and tibial channels with heterogeneous rates |
| SHHS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| ISRUC | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |

Exact channel evidence is in `reports/sleep_edf_channel_inventory.csv`, `reports/cap_channel_inventory.csv`, and the expanded schema manifest. No category is used to excuse fundamentally incomparable signals.

## 14. EMG Compatibility Finding

SC-vs-ST EMG is **not suitable for the primary exact-EMG benchmark condition** as currently evidenced. SC is explicitly a processed, rectified/filtered 1-Hz RMS envelope; ST is documented as 100-Hz EMG and appears as such in headers. The primary proposal should use EEG+EOG modality families, with EMG secondary or as a structural representation-mismatch stress condition. EMG must not be silently resampled or treated as equivalent in Step 5.

## 15. Label Compatibility

Sleep-EDF and CAP use R&K-derived macrostructure. Proposed canonical labels are Wake, N1, N2, N3, REM. W/Wake, R/REM, Stage 1/S1, and Stage 2/S2 have source-supported semantic correspondence. Stage 3 + Stage 4 -> N3 is proposed but remains REVIEW/PROPOSE until an authoritative mapping is added. Movement/MT, `?`, unknown, unscored, artifact, and scorer disagreement are not silently mapped; each requires explicit INCLUDE/EXCLUDE/REVIEW policy. CAP phase-A labels are not sleep-stage labels.

The full proposal is in `docs/label_contract_proposal.md`; direct annotation-file inspection and source-supported N3 aggregation remain blockers.

## 16. Wake-Trimming Finding

The audit did not establish sufficient source evidence to freeze a trimming rule. Candidate policies are: preserve all scored epochs; trim prolonged pre-sleep/post-final-awakening wake; or use a fixed context window. Preserving all scored epochs maximizes source fidelity but may change class balance; trimming may improve comparability but introduces choices based on labels and risks inconsistent cross-dataset definitions; a context window may reduce extremes but requires a frozen, label-independent rule. Final decision: **NOT_FROZEN**. No trimming was implemented.

## 17. Recommended Primary Dataset Plan

PRIMARY:

A deferred EEG+EOG core centered on Sleep-EDF SC/ST only after the label, treatment, and trimming contracts are frozen; do not represent SC and ST as independent subjects or silently equate their EMG.

EXTERNAL STRESS TEST:

CAP, if complete header/annotation and subject-identity audits succeed. Its pathology and channel heterogeneity are scientifically useful as a stress test, not a primary exact-channel domain at present.

DEFERRED:

ISRUC-Sleep and SHHS pending official access and schema verification. No three-dataset leave-one-out claim is currently justified. Configurations A/B/C remain unselected because the required third-domain evidence is incomplete.

## 18. Proposed Harmonization Contract

Not frozen. Candidate Step 5 proposal: canonical modality families EEG and EOG for the primary core; preserve source montage/reference as domain metadata; treat EMG as secondary/structural-mismatch only; keep SC/ST separate; map only source-supported labels; exclude or review Movement, unknown, `?`, artifact, and unscored labels explicitly; preserve all subject nights/visits together; freeze trimming and missingness rules before preprocessing. This proposal cannot become a frozen contract until ISRUC/SHHS/CAP blockers and annotation semantics are resolved.

## 19. Leakage Risks Identified

* splitting SC or ST nights independently;
* separating ST temazepam/placebo nights;
* treating repeated SHHS visits as independent;
* treating CAP pathology-coded filenames as subject IDs;
* using Sleep-EDF-derived subsets as separate domains;
* duplicate converted recordings across partitions;
* target-domain labels or calibration influencing model design;
* normalization statistics computed from held-out subjects;
* conflating missing channels with missing EEG/EOG/EMG modalities;
* deriving trimming thresholds from target labels.

## 20. Access / Legal Risks

* Sleep-EDF and CAP are provider-hosted open datasets, but license attribution and redistribution terms still govern use.
* SHHS raw files remain RAW_ACCESS_PENDING and must not be obtained by bypassing NSRR controls.
* ISRUC access is unresolved; unofficial mirrors are prohibited.
* No credentials or access tokens were requested or stored.
* Full Sleep-EDF archive is listed as 8.1 GB and was not downloaded.
* Header-range inspection is metadata-only and does not confer redistribution rights.

## 21. Machine-Readable Artifacts

* `reports/sleep_edf_subject_manifest.csv`: 197 data rows, 10 columns.
* `reports/sleep_edf_channel_inventory.csv`: 197 data rows, 17 columns; 196 VERIFIED and 1 preserved network error.
* `reports/cap_channel_inventory.csv`: 108 data rows, 17 columns; 13 VERIFIED and 95 preserved network/DNS errors.
* `reports/dataset_access_registry.csv`: 4 data rows, 12 columns.
* `reports/dataset_schema_manifest.csv`: 1,538 data rows, 13 columns, generated only from successfully parsed headers.
* `reports/dataset_recording_manifest.csv`: 305 data rows, 13 columns; CAP identity fields remain unresolved.
* `reports/acquisition_manifest.csv`: 6 data rows, 8 columns.

## 22. Schema Tooling Implemented

`src/shiftsleep_uq/data/edf.py` implements a pure-Python EDF/EDF+ fixed-plus-signal-header parser. `scripts/audit_remote_edf_headers.py` performs two HTTP Range requests per EDF, validates `206`/`Content-Range`, parses only the header, and preserves failures. `scripts/audit_sleep_edf_metadata.py` builds the official filename-derived Sleep-EDF subject manifest. `scripts/build_step4_manifests.py` builds safe machine-readable registries. No preprocessing, model, tensor, filtering, resampling, normalization, or training code was added.

## 23. Tests Added

* valid EDF header parsing and sampling-frequency extraction;
* stream-based header parsing;
* malformed/incomplete header rejection;
* Sleep-EDF filename mapping exercised through the generated 197-record manifest;
* CSV width and row-count validation performed during Step 4 validation.

## 24. Validation Results

Final validation must be rerun after report generation. Required commands and expected recorded outputs are:

* `pytest -q` — must pass.
* `python -m compileall -q src tests scripts` — must exit 0.
* `git diff --check` — must exit 0.
* CSV validation — all generated CSV rows must have consistent widths and required columns; no blank subject IDs are accepted as real subjects.
* forbidden-artifact scan — no tracked EDF/EDF+, restricted annotation, archive, credentials, cookies, or paper PDF.

The successful parser/manifest run before final document generation was `4 passed` with `197` Sleep-EDF recordings, `153` SC, `44` ST, `78` SC subjects, and `22` ST subjects.

## 25. Files Created

* `data/README.md`
* `docs/raw_schema_audit.md`
* `docs/modality_contract_proposal.md`
* `docs/label_contract_proposal.md`
* `docs/dataset_overlap_policy.md`
* `src/shiftsleep_uq/data/__init__.py`
* `src/shiftsleep_uq/data/edf.py`
* `scripts/audit_sleep_edf_metadata.py`
* `scripts/audit_remote_edf_headers.py`
* `scripts/build_step4_manifests.py`
* `tests/test_edf.py`
* `reports/sleep_edf_subject_manifest.csv`
* `reports/sleep_edf_channel_inventory.csv`
* `reports/cap_channel_inventory.csv`
* `reports/dataset_access_registry.csv`
* `reports/dataset_schema_manifest.csv`
* `reports/dataset_recording_manifest.csv`
* `reports/acquisition_manifest.csv`
* `reports/STEP_04_DATASET_SCHEMA_REPORT.md`

## 26. Files Modified

* `docs/dataset_registry.md` — to be updated with Step 4 provenance and unresolved statuses.
* `docs/dataset_harmonization_audit.md` — to be updated with raw-schema findings.
* `docs/leakage_policy.md` — to be updated only with source-supported Sleep-EDF and proposed unresolved-dataset rules.

## 27. Explicitly Not Done

* no model implemented;
* no model trained;
* no signal filtering;
* no signal normalization;
* no resampling;
* no final epoch extraction;
* no final dataset split generated;
* no target-domain calibration;
* no experimental result generated;
* no raw PSG committed;
* no restricted data committed;
* no GitHub push.

## 28. Blockers / Unknowns

1. ISRUC official access and S1/S2/S3 meanings are unresolved.
2. SHHS official documentation could not be accessed successfully; participant/visit/channel/scoring/access facts remain unresolved.
3. CAP complete header audit is blocked by transient DNS/network failures; 95/108 headers remain unverified.
4. SC4721E0 header remains unverified after a connection reset.
5. ST treatment condition requires direct spreadsheet parsing/verification.
6. ST marker sampling differs between official prose (1 Hz) and inspected headers (10 Hz); requires adjudication.
7. Direct annotation-file audit was not completed.
8. R&K Stage 3+4 -> N3 mapping needs authoritative source evidence before freeze.
9. Wake trimming and treatment of movement/unknown/artifact/scorer disagreement are not frozen.
10. Cross-dataset subject overlap cannot be claimed absent official identity/linkage evidence.
11. Exact EMG equivalence is not supported for SC/ST primary benchmarking.

## 29. Recommended Step 5

Do not execute Step 5 preprocessing yet. The single recommended next major step is: **resolve the remaining official-access and annotation/schema blockers, then freeze the channel, label, exclusion, trimming, missingness, and subject-level split contract before any preprocessing.**

## 30. Git Status / Diff Summary

Final commit and exact clean/dirty status must be recorded after validation. The Step 4 commit must contain only code, documentation, safe manifests, and audit results; it must not contain raw signal files, restricted annotations, credentials, cookies, archives, or paper PDFs. Push status remains NOT_PUSHED.
