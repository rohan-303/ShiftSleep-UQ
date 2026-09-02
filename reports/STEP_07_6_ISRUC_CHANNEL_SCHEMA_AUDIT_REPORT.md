# ShiftSleep-UQ Step 7.6 ISRUC Channel Schema Audit Report

## 1. Status

COMPLETE

This diagnostic step is complete for the acquired, body-valid original-provider ISRUC-S1 recordings I001–I035. It is not a complete ISRUC migration: I036 remains partial and I037–I100 remain unacquired under the Step 7.5 quota boundary.

## 2. Channel Schema Gate

CHANNEL_CONTRACT_REVIEW_REQUIRED

The apparent exclusions are explained by genuine source-header montage/label variants, not by a parser or representational bug. The frozen exact-channel contract was not changed. A future protocol-level review is required before any alternate labels could be considered scientifically admissible.

## 3. ISRUC Migration Gate

Expected:
ISRUC_ORIGINAL_COHORT_PARTIAL

This step does not change the migration gate. No I036–I100 acquisition was attempted or resumed.

## 4. Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Starting Step 7.5 commit: `dc1f03a` (`research: record ISRUC migration blocker`)
- Provider under audit: official original-provider ISRUC-Sleep Cohort I MEGA distribution.
- Audited population: I001–I035, exactly 35 complete body-valid original REC files.
- I036 partial `.getxfer` state: untouched.
- I037–I100: unacquired; no acquisition command was run in Step 7.6.
- Raw and processed data remain Git-ignored.

## 5. Trigger

Step 7.5 reported 17/35 acquired body-valid subjects as containing both frozen required channels (`C3-A2` and `LOC-A2`) and 18/35 as `MISSING_REQUIRED_CHANNEL`. This was suspicious because published Subgroup-1 descriptions report a six-EEG/two-EOG nominal schema containing these labels at 200 Hz.

Step 7.6 independently reproduced the header labels before accepting the prior classification. The result is:

- 17/35: exact `C3-A2` present and exact `LOC-A2` present.
- 18/35: both exact labels absent.
- 18/18 excluded subjects: explicit alternate M1/M2-style source labels, including `C3-M2` and EOG-side `E1-M2`/`E2-M1`; no exact-channel fallback was applied.

## 6. Pre-Fix Population

The pre-fix snapshot contains exactly 35 rows in `reports/isruc_channel_exclusion_pre_fix_snapshot.csv`. It records each REC SHA-256, independent body-valid state, signal count, exact raw inventory, current project labels/classification, current terminal status, and current failure code.

- Body-valid: 35/35.
- Complete original bundles: 35/35.
- Current channel-compatible: 17/35.
- Current schema-excluded: 18/35.
- Current schema failure code for those 18: `MISSING_REQUIRED_CHANNEL`.
- No pre-fix data were rewritten.

## 7. Published / Official Nominal Schema

The original dataset reference is Khalighi et al., *ISRUC-Sleep: A comprehensive public dataset for sleep researchers*, Computer Methods and Programs in Biomedicine 124 (2016), 180–192, PubMed PMID 26589468: <https://pubmed.ncbi.nlm.nih.gov/26589468/>.

A peer-reviewed open article describing its Subgroup-1 use states that 100 Subgroup-1 subjects were used; each recording contained six EEG channels (`C3-A2`, `C4-A1`, `F3-A2`, `O1-A2`, `O2-A1`, `F4-A1`), two EOG channels (`LOC-A2`, `ROC-A1`), and three EMG channels, with a recording rate of 200 Hz: *Automatic and Accurate Sleep Stage Classification via a Convolutional Deep Neural Network and Nanomembrane Electrodes*, Methods §2.1, <https://pmc.ncbi.nlm.nih.gov/articles/PMC8946692/>.

The TorchEEG ISRUC documentation identifies Group 1 as 100 subjects, documents the `Subgroup_1/<subject>/<subject>.rec` structure and scorer-1 filename pattern, and lists the nominal A1/A2 labels. It also exposes M1/M2 labels in its default example: <https://torcheeg.readthedocs.io/en/stable/generated/torcheeg.datasets.ISRUCDataset.html>. This is treated as evidence of representation variation, not as scientific authority to map M1/M2 to A1/A2.

The sources establish a nominal schema, not universal proof that every raw export uses identical strings. The report therefore separates nominal documentation from the observed raw headers.

## 8. Independent Raw Header Audit

`step_07_6_channel_schema_audit.py` reads the REC file directly without initially using the project channel-selection logic:

- Fixed EDF header: 256 bytes.
- Number of signals: ASCII field at fixed-header bytes 252–255.
- Signal labels: `16 × ns` bytes immediately after the fixed header.
- Also extracted: transducer, physical dimension, physical minimum/maximum, digital minimum/maximum, prefilter/reserved layout, samples per record, record count, and record duration.
- Expected body size: `256 × (ns + 1) + records × sum(samples_per_record) × 2`.

Results:

- 35/35 REC bodies passed the independent byte-length check.
- 672 signal fields were inspected.
- The raw label fields are fixed-width ASCII labels with legal trailing ASCII-space padding.
- No NUL bytes, tabs, non-ASCII bytes, embedded control characters, Unicode lookalikes, or hyphen variants were found.
- No header offset or signal-index anomaly was found.

Artifact: `reports/isruc_original_raw_header_labels.csv`.

## 9. Exact Channel Inventories

The complete 35-subject diagnostic inventory is in `reports/isruc_original_channel_inventory_35_diagnostic.csv`; labels are not truncated.

The 17 exact-channel-compatible subjects are I001–I010, I012, I015, I016, I018, I022, I024, and I026. I008 is a valid source-supported inventory variant with 21 signals but still contains exact `C3-A2` and `LOC-A2`.

The 18 exact-channel-excluded subjects are shown below. Each has both required exact labels absent:

| Subject | Exact raw inventory | C3-A2 | LOC-A2 | F3-A2 | O1-A2 | C4-A1 | ROC-A1 | C3-M2 | EOG-side M1/M2 labels | Other variant labels |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| I011 | E1-M2, E2-M1, F3-M2, C3-M2, O1-M2, F4-M1, C4-M1, O2-M1, X1–X6, DC4, X7, X8, X7-X8, SpO2, DC8, DC1–DC3, DC5 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, X7-X8, SpO2, DC1–DC3, DC5 |
| I013 | E1-M2, E2-M1, F3-M2, C3-M2, O1-M2, F4-M1, C4-M1, O2-M1, X1–X6, DC4, X7, X8, SpO2, DC8 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I014 | E1-M2, E2-M1, F3-M2, C3-M2, O1-M2, F4-M1, C4-M1, O2-M1, 24–29, DC01, 30, 31, SpO2, DC02 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I017 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I019 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I020 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I021 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I023 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I025 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I027 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I028 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I029 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |
| I030 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I031 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I032 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I033 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I034 | same 19-signal numeric M1/M2 inventory as I014 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | numeric 24–31, DC01, DC02, SpO2 |
| I035 | same 19-signal M1/M2 inventory as I013 | no | no | no | no | no | no | yes | E1-M2, E2-M1 | DC4, SpO2 |

The related labels `F3-A2`, `O1-A2`, `C4-A1`, and `ROC-A1` are absent in all 18 excluded subjects. `C3-M2` is present in all 18. No exact standalone `C3` or `LOC` label was observed, and no `C3-A1` or `LOC-A1` label was observed.

## 10. Character-Level Label Findings

`reports/isruc_channel_label_character_audit.csv` contains one row per signal field.

- ASCII-space padding: present as trailing EDF field padding and removed only for the `stripped_repr` comparison.
- NUL: 0/672.
- Non-ASCII: 0/672.
- Tabs/control characters: 0/672.
- Unicode lookalikes: 0/672.
- Hyphen variants: 0/672.
- Exact `C3-A2` and `LOC-A2` were found after stripping only trailing ASCII padding in the 17 compatible subjects.
- No near-match was promoted to an exact match.

Conclusion: representational padding and encoding cannot explain the 18 exclusions.

## 11. Schema Clusters

The schema fingerprint is SHA-256 over ordered channel labels, samples-per-record, and physical dimensions. `reports/isruc_channel_schema_clusters.csv` records each subject and fingerprint.

There are seven deterministic fingerprints:

| Subjects | Count | Characterization |
|---|---:|---|
| I001–I007, I009–I010, I012, I015–I016, I018, I022, I024, I026 | 16 | Nominal A1/A2 labels; 19 signals |
| I008 | 1 | A1/A2-compatible variant with 21 signals and additional DC channels |
| I011 | 1 | M1/M2 variant with 24 signals and additional DC/X7-X8 channels |
| I013 | 1 | M1/M2 labels with X1–X6, DC4, X7, X8, SpO2, DC8; 19 signals |
| I014, I017, I023, I025, I030–I034 | 9 | M1/M2 labels with numeric labels 24–31, DC01/DC02, SpO2; 19 signals |
| I019–I021, I028, I035 | 5 | M1/M2 labels with X1–X6, DC4, X7, X8, SpO2, DC8; 19 signals |
| I027, I029 | 2 | M1/M2 label family with the same ordered labels but a distinct physical/sample schema fingerprint |

These seven fingerprints are deterministic groups, not claims of seven biological montages. The schema transition is not a simple subject-number-only cutoff: A1/A2 subjects and multiple M1/M2 variants are interspersed across I001–I035.

## 12. Existing Parser Cross-Check

`reports/isruc_channel_parser_crosscheck.csv` compares every existing project label with the independent raw-header label.

- Total signal fields compared: 672.
- Exact matches: 672.
- Differences: 0.
- Difference type: none.

The current project path ultimately obtains labels with `pyedflib.EdfReader.getSignalLabels()` in `src/shiftsleep_uq/data/preprocess.py:19–31`; that result matches the independently extracted, padding-stripped raw labels for every signal in all 35 subjects. No parser code is responsible for the exclusions.

## 13. PyEDFlib Cross-Check

`reports/isruc_three_way_channel_parser_audit.csv` compares raw manual labels, pyedflib labels, and the project inventory.

- `ALL_AGREE`: 35/35 subjects.
- `PROJECT_DISAGREES`: 0.
- `PYEDFLIB_DISAGREES`: 0.
- `RAW_PARSER_AMBIGUOUS`: 0.

PyEDFlib was not treated as automatically authoritative; agreement was established independently against the fixed-width raw fields.

## 14. Cohort/File Identity Check

`reports/isruc_cohort_identity_audit.csv` records identity and bundle evidence for all 35 subjects.

- Official folder ID equals local numeric subject ID: 35/35.
- REC patient field equals the corresponding subject number: 35/35.
- REC recording fields identify the Somnostar Pro source: 35/35.
- Expected scorer-1/scorer-2 text and Excel files are present: 35/35.
- REC body-valid under the independent byte calculation: 35/35.
- No evidence of a Subgroup-2/Subgroup-3 folder crossing or filename/session mismatch was found.

This audit does not claim that the recording device metadata alone proves all cohort provenance; it establishes that the local bundles are internally consistent with the frozen Subgroup-1 subject/file structure and are not misidentified by an obvious folder/REC mismatch.

## 15. Excluded-Subject Channel Findings

All 18 subjects are listed exactly once in `reports/isruc_excluded_subject_channel_findings.csv` and `reports/isruc_channel_exclusion_root_causes.csv`:

- I011: C3-A2 absent; LOC-A2 absent; C3-M2 present; E1-M2/E2-M1 present; classified alternate source label.
- I013: C3-A2 absent; LOC-A2 absent; C3-M2 present; E1-M2/E2-M1 present; classified alternate source label.
- I014: C3-A2 absent; LOC-A2 absent; C3-M2 present; E1-M2/E2-M1 present; numeric/device extras; classified alternate source label.
- I017: same exact M1/M2 findings as I014; classified alternate source label.
- I019: same exact M1/M2 findings as I013; classified alternate source label.
- I020: same exact M1/M2 findings as I013; classified alternate source label.
- I021: same exact M1/M2 findings as I013; classified alternate source label.
- I023: same exact M1/M2 findings as I014; classified alternate source label.
- I025: same exact M1/M2 findings as I014; classified alternate source label.
- I027: same exact M1/M2 findings as I013; classified alternate source label.
- I028: same exact M1/M2 findings as I013; classified alternate source label.
- I029: same exact M1/M2 findings as I013; classified alternate source label.
- I030: same exact M1/M2 findings as I014; classified alternate source label.
- I031: same exact M1/M2 findings as I014; classified alternate source label.
- I032: same exact M1/M2 findings as I014; classified alternate source label.
- I033: same exact M1/M2 findings as I014; classified alternate source label.
- I034: same exact M1/M2 findings as I014; classified alternate source label.
- I035: same exact M1/M2 findings as I013; classified alternate source label.

No excluded subject has a parser disagreement, malformed label field, corrupt REC body, or missing scorer bundle in the audited evidence.

## 16. Root-Cause Classification

Every one of the 18 current schema exclusions appears exactly once in `reports/isruc_channel_exclusion_root_causes.csv`.

| Primary root cause | Subjects | Count |
|---|---|---:|
| ALTERNATE_SOURCE_LABEL | I011, I013, I014, I017, I019, I020, I021, I023, I025, I027, I028, I029, I030, I031, I032, I033, I034, I035 | 18 |
| PARSER_LABEL_BUG | none | 0 |
| REPRESENTATIONAL_PADDING_BUG | none | 0 |
| TRUE_CHANNEL_ABSENCE | not assigned as primary because the raw headers contain source-supported alternate montage labels rather than empty/missing signal positions | 0 |
| HEADER_VARIANT | not assigned as primary; header variants are subordinate characteristics of the alternate-label clusters | 0 |
| WRONG_COHORT_OR_FILE | none | 0 |
| CORRUPT_HEADER | none | 0 |
| OTHER | none | 0 |
| UNRESOLVED | none for the parsing diagnosis; scientific admissibility of alternates remains unresolved | 0 |

## 17. Primary Root Cause

ALTERNATE_SOURCE_LABEL

The root cause of the 18 apparent missing-channel exclusions is source-header montage/label variation: the exact A1/A2 labels are replaced by explicit M1/M2 and related EOG-side labels. This is not evidence that the signals are scientifically equivalent under the current contract.

## 18. Repair Performed

NONE

No parser, label, channel, rate, unit, annotation, or preprocessing repair was performed. No subjects were reprocessed. No fallback mapping was added.

## 19. Scientific Contract Impact

REVIEW_REQUIRED

The exact frozen contract remains unchanged:

- EEG: exact `C3-A2`.
- EOG: exact `LOC-A2`.
- Native ISRUC rate: 200 Hz.
- No M1/M2-to-A1/A2 mapping.
- No fallback to `C4-A1`, `ROC-A1`, `C3-M2`, or other channels.

The source evidence requires a future independent protocol-level channel-harmonization review before any alternate montage can be considered. Step 7.6 does not make that decision.

## 20. Before-vs-After Inclusion

Before:
17/35

After:
17/35

No repair was performed, so inclusion did not change. The 18 excluded subjects remain excluded under the frozen exact-channel contract.

## 21. Regression Validation

Subjects I001–I003 remain unchanged and pass the independent raw-header, pyedflib, and project-parser cross-checks:

- exact `C3-A2`: present in all three;
- exact `LOC-A2`: present in all three;
- 200 Hz native signal structure: retained;
- physical dimension: `uV` for the required channels;
- raw REC SHA-256 values are preserved in the pre-fix snapshot and existing provider-integrity audit.

No processed output was changed.

## 22. Tests Added

Added `tests/test_step_07_6_channel_audit.py` with tests for:

- stripping only legal EDF trailing ASCII padding;
- preserving embedded NUL bytes rather than treating them as semantic label matches.

No alias/fallback test was added because no alias behavior was implemented. Existing tests were retained.

## 23. Full Validation

Audit execution:

- Independent audit script: completed successfully.
- Subjects: 35.
- Signal fields: 672.
- Body-valid REC files: 35/35.
- Character audit rows: 672.
- Pre-fix snapshot rows: exactly 35.
- Parser cross-check rows: 672; exact matches: 672.
- Three-way parser audit rows: 35; `ALL_AGREE`: 35.
- Root-cause rows: exactly 18; duplicate subject IDs: none.
- Schema-cluster rows: exactly 35.
- Cohort identity rows: exactly 35.

Repository validation after report generation:

- `pytest -q`: passed.
- `python -m compileall -q src tests scripts`: passed.
- `git diff --check`: passed.
- Raw REC, annotation, temporary transfer, and processed-array tracking checks: no tracked data.
- Credential scan: no credentials added.
- GitHub push: not performed.

## 24. Files Created

- `scripts/step_07_6_channel_schema_audit.py`
- `tests/test_step_07_6_channel_audit.py`
- `reports/isruc_channel_exclusion_pre_fix_snapshot.csv`
- `reports/isruc_original_raw_header_labels.csv`
- `reports/isruc_channel_label_character_audit.csv`
- `reports/isruc_original_channel_inventory_35_diagnostic.csv`
- `reports/isruc_channel_schema_clusters.csv`
- `reports/isruc_channel_parser_crosscheck.csv`
- `reports/isruc_three_way_channel_parser_audit.csv`
- `reports/isruc_excluded_subject_channel_findings.csv`
- `reports/isruc_channel_exclusion_root_causes.csv`
- `reports/isruc_channel_header_side_by_side.csv`
- `reports/isruc_cohort_identity_audit.csv`
- `docs/isruc_channel_schema_evidence.md`
- `reports/STEP_07_6_ISRUC_CHANNEL_SCHEMA_AUDIT_REPORT.md`

## 25. Files Modified

- None in `src/`.
- The Step 7.6 audit tooling and tests are new files. Existing scientific configuration, frozen channel requirements, labels, scorer policy, and preprocessing code were not modified.

## 26. Explicitly Not Done

- No I036–I100 acquisition resumed.
- No MEGA partial transfer resumed.
- No fallback channels.
- No scientific channel change.
- No M1/M2-to-A1/A2 mapping.
- No label or scorer change.
- No splits.
- No models.
- No training.
- No normalization.
- No ML metrics.
- No SHHS access.
- No raw or processed data committed.
- No push.

## 27. Remaining ISRUC Issues

1. The original-provider migration remains partial: I001–I035 complete, I036 partial, I037–I100 unavailable.
2. The exact-channel accessible-core gate remains unresolved because 18/35 audited subjects have alternate source montages.
3. Published nominal documentation and observed raw exports are not identical; this is a scientific-contract review issue, not a parser defect.
4. The 18 alternate-label records cannot be added to the primary cohort without an independent protocol amendment.
5. The apparent schema transition is heterogeneous rather than a simple deterministic subject-number cutoff.
6. No conclusion has been made about whether M1/M2 signals are physiologically comparable for this study.

## 28. Recommended Next Step

Because the gate is `CHANNEL_CONTRACT_REVIEW_REQUIRED`, do not spend another approximately 9 GB on I036–I100 before channel design is reviewed.

Recommend exactly one next step:

**Conduct one independent protocol-level channel harmonization review of the observed A1/A2 versus M1/M2 montages, with explicit anatomical/reference equivalence criteria and a predeclared decision on whether the frozen exact-channel contract should remain primary.**

Do not execute that review in this step. Do not broaden eligibility based only on string similarity.

## 29. Git Status / Diff Summary

Step 7.6 is committed with subject `research: audit ISRUC original channel schema`; the working tree is clean. No source preprocessing code, raw data, processed arrays, credentials, or provider files were modified. No GitHub push was performed.
