# ShiftSleep-UQ Step 7.3 ISRUC Provider Comparison Report

## 1. Status

**COMPLETE**

The authorized subject-1 original-provider bundle was acquired and compared against the locally retained NEMAR I001 artifacts. The subject-level engineering comparison is complete. Full-cohort migration has not been performed and is outside this step.

## 2. Provider Decision

**COMPARISON_INCONCLUSIVE**

The comparison confirms a defective NEMAR I001 signal object and demonstrates that the retained NEMAR prefix is numerically identical to the original provider for both primary channels. However, one subject is insufficient to approve a 100-subject provider migration or to establish full-cohort reproducibility, annotation preservation, and schema behavior.

## 3. Repository State

- Repository: `C:/Users/rohan/ShiftSleep-UQ`
- Branch: `main`
- Step 7.2 gate: `CORE_DATA_BLOCKED`
- Original bundle: `data/raw/isruc-original/subject-1/1/`
- NEMAR I001 signal: `data/raw/isruc-nemar/v1.0.1/sub-I001_task-sleep_eeg.edf`
- NEMAR I001 events: `data/raw/isruc-nemar/v1.0.1/sub-I001_task-sleep_events.tsv`
- Existing NEMAR audit: `reports/provider_integrity_audit.csv`
- Existing NEMAR attrition audit: `reports/isruc_attrition_audit.csv`
- Working tree was preflighted on `main`; raw data are ignored by `.gitignore`.
- No personal MEGA account was used.

## 4. Original Provider Inventory

Provider is `ORIGINAL_ISRUC_MEGA` for every row. The acquired bundle contains the expected five files:

| File | Bytes | SHA-256 | Interpretation |
|---|---:|---|---|
| `1.rec` | 143,885,120 | `4ff7c64f79131213e15107a4f53d40db0081ec2246142b67d2343b2b8dbbb42f` | complete signal recording |
| `1_1.txt` | 2,640 | `24793ceba5ee9845d6913a209ac423fd20e9e541f47f67356e89f19d26a4b085` | scorer 1 stage labels |
| `1_1.xlsx` | 41,524 | `8c665f5f8316c15edfbc5a7ca669e59cb537e185fb7747cdef04ad39e48c0c26` | scorer 1 workbook |
| `1_2.txt` | 2,640 | `d3bb8ac5afd08664d8d1a28a04826076cb53afc8878f1e186620daec527831fe` | scorer 2 stage labels |
| `1_2.xlsx` | 41,012 | `ce34a7a0e1da1f53c0973fc8d80a3921de0ee12d7e7d6fe086af83211cfd5e31` | scorer 2 workbook |

Machine-readable inventory: `reports/isruc_original_subject1_inventory.csv`.

## 5. Original REC Integrity

The original file was validated using the existing EDF/REC body-size formula:

`expected_total = header_length + number_of_records × sum(samples_per_signal_per_record) × 2`

Measured values:

- Header length: 5,120 bytes
- Signals: 19
- Data records: 13,200
- Duration per data record: 2.0 s
- Samples per signal per record: `400|400|400|400|400|400|400|400|400|400|400|400|400|25|50|50|50|25|50`
- Computed expected total: 143,885,120 bytes
- Actual local bytes: 143,885,120 bytes
- Actual-minus-expected delta: 0 bytes
- SHA-256: `4ff7c64f79131213e15107a4f53d40db0081ec2246142b67d2343b2b8dbbb42f`
- Classification: **ORIGINAL_BODY_VALID**

## 6. NEMAR I001 Integrity

Measured local NEMAR values:

- Path: `data/raw/isruc-nemar/v1.0.1/sub-I001_task-sleep_eeg.edf`
- Actual bytes: 91,778,304
- SHA-256: `900755de373ff9045c9ad758236c6f304dd3bb8f39dbbade55b56b6be454968f`
- Header length: 5,120 bytes
- Signals: 19
- Declared data records: 13,200
- Duration per data record: 2.0 s
- Computed expected total: 143,885,120 bytes
- Actual-minus-expected delta: -52,106,816 bytes
- Complete records: 8,419, followed by 6,084 bytes of a partial record
- Existing audit: checksum `MATCH`, header `PASS`, body `FAIL`, terminal status `EXCLUDED_PROVIDER_INTEGRITY`
- Classification: **NEMAR_I001_TRUNCATION_CONFIRMED**

The provider manifest records the same 91,778,304-byte object and SHA-256. This is not a local naming or parser-only discrepancy.

## 7. File-Size Comparison

| Quantity | Original | NEMAR I001 | Equal | Finding |
|---|---:|---:|---|---|
| Actual file bytes | 143,885,120 | 91,778,304 | No | NEMAR is 52,106,816 bytes shorter |
| Computed expected bytes | 143,885,120 | 143,885,120 | Yes | identical headers imply identical expected size |
| Actual-minus-expected | 0 | -52,106,816 | No | original complete; NEMAR truncated |
| Complete data records | 13,200 | 8,419 | No | NEMAR ends during the next record |
| NEMAR partial-record bytes | N/A | 6,084 | N/A | incomplete body tail |

## 8. EDF/REC Header Comparison

The fixed and signal headers were parsed independently from both local files.

- Header lengths are equal: 5,120 bytes.
- Signal counts are equal: 19.
- Data-record counts are equal in the headers: 13,200.
- Record duration is equal: 2.0 s.
- Declared recording duration is equal: 26,400 s.
- Record start date is equal: `18.05.09`.
- Record start time is equal: `23.37.00`.
- Subject/patient field is equal: `1`.
- Samples per signal per record are identical.
- Physical dimensions, digital ranges, and physical ranges are identical for every signal.

Therefore, the NEMAR object preserves the original header but not the full body.

## 9. Channel Comparison

The complete documented source signal-label inventory in both headers is identical and in identical order:

`LOC-A2, ROC-A1, F3-A2, C3-A2, O1-A2, F4-A1, C4-A1, O2-A1, X1, X2, X3, X4, X5, X6, DC3, X7, X8, SaO2, DC8`

Required channels are preserved:

- `C3-A2`: present in original and NEMAR, same order.
- `LOC-A2`: present in original and NEMAR, same order.

No channel renaming, reordering, or channel removal was observed for I001. This finding does not establish that every S1 subject has the same behavior.

## 10. Sampling Comparison

For the primary channels:

| Channel | Original native rate | NEMAR native rate | Result |
|---|---:|---:|---|
| `C3-A2` | 200 Hz | 200 Hz | sampling equivalent |
| `LOC-A2` | 200 Hz | 200 Hz | sampling equivalent |

Both channels have 400 samples per two-second record and the same `uV` physical dimension. Classification: **SAMPLING_EQUIVALENT** for subject 1.

The project preprocessing contract remains unchanged: EEG target 100 Hz, EOG target 50 Hz, 30-second epochs, unnormalized `float32` outputs in microvolts.

## 11. Signal Prefix / Content Comparison

The common raw prefix was compared before physical-value conversion. It is byte-identical through the NEMAR body extent corresponding to the 8,419 complete records:

- Common raw bytes compared: 91,772,220 bytes, including the 5,120-byte header and complete records.
- Raw prefix equality: `TRUE`.

After EDF calibration to physical values, using only complete overlapping records:

| Channel | Common samples | Max absolute difference | Mean absolute difference | Pearson r |
|---|---:|---:|---:|---:|
| `C3-A2` | 3,367,600 | 0.0 uV | 0.0 uV | 1.0 |
| `LOC-A2` | 3,367,600 | 0.0 uV | 0.0 uV | 1.0 |

This supports the precise conclusion: **NEMAR I001 is an accurate but truncated prefix of the original ISRUC recording for the two tested primary channels.** It is not evidence that the NEMAR object is complete.

## 12. Original Annotation Inventory

`1_1.txt` and `1_1.xlsx` are scorer 1; `1_2.txt` and `1_2.xlsx` are scorer 2, based on the matching workbook IDs (`1_1` and `1_2`) and the corresponding source naming.

- Each TXT file contains 880 integer stage labels.
- Stage-code vocabulary in each TXT: `{0, 1, 2, 3, 5}`.
- Each annotation workbook contains 880 epoch rows plus its header row.
- Workbook stage vocabulary is the source representation `{W, N1, N2, N3, R}`.
- `1_1.xlsx` has one populated worksheet and passes ZIP integrity.
- `1_2.xlsx` has three worksheets, two empty, and passes ZIP integrity.
- No raw annotation file was modified.

## 13. Scorer-1 Comparison

The local NEMAR events file contains 562 primary event rows with labels `Sleep stage W`, `N1`, `N2`, `N3`, and `R`.

- Original scorer-1 epochs: 880.
- NEMAR primary events: 562.
- NEMAR event durations: 561 events of 30.0 s and one event of 8.0 s.
- NEMAR event span: 16,838.0 s.
- Direct canonical stage-code comparison over the first 562 retained events: 562 matches, 0 mismatches.
- First mismatch index: none.
- Missing NEMAR epochs relative to original: 318 full original epochs are not represented after the retained prefix; the final NEMAR event is shorter than a full epoch.
- Extra NEMAR epochs: 0.

The canonical comparison used the frozen verified stage mapping represented by the shared values: `0=W`, `1=N1`, `2=N2`, `3=N3`, `5=R`. No new label mapping was introduced.

## 14. Scorer-2 Preservation Comparison

NEMAR includes `scorer2_label` and `scorer2_label_value` columns in its events file.

- Original scorer-2 epochs: 880.
- NEMAR scorer-2 values available: 562.
- First 562 scorer-2 values: 562 matches, 0 mismatches.
- Missing scorer-2 epochs: 318 relative to the 880-epoch original annotation.
- Extra scorer-2 epochs: 0.

This supports preservation of the retained scorer-2 prefix. It does not establish complete scorer-2 preservation for the full night or all subjects. Scorer 1 remains the primary annotation contract.

## 15. Duration / Truncation Finding

- Original signal duration: 13,200 × 2.0 s = 26,400.0 s.
- NEMAR declared signal duration from its unchanged header: 26,400.0 s.
- NEMAR complete signal duration: 8,419 × 2.0 s = 16,838.0 s.
- NEMAR partial body extends approximately 1.1163 s into the next two-second record.
- NEMAR actual body endpoint: approximately 16,839.1163 s.
- Original scorer-1 annotation duration: 880 × 30 s = 26,400 s.
- NEMAR event span: 16,838.0 s.
- Annotation beyond NEMAR event span: approximately 9,562 s.

The NEMAR event file ends at the complete-record boundary, while the EDF body has a partial next record. This is consistent with delivery of an incomplete signal body and incomplete event coverage rather than a valid full-night recording.

## 16. NEMAR Failure Classification

**PROVIDER_DELIVERY_TRUNCATION**

Evidence:

1. The original provider object is complete at exactly 143,885,120 bytes.
2. The NEMAR local object is exactly 91,778,304 bytes and has a matching NEMAR manifest checksum.
3. NEMAR preserves the original header and calibration metadata but fails the body-size check by 52,106,816 bytes.
4. The common signal prefix is byte-identical and physically identical for `C3-A2` and `LOC-A2`.
5. Therefore, the available evidence points to a shortened NEMAR/provider object, not local download truncation and not a value-conversion error.

The exact upstream mechanism—conversion writer failure versus publication of a shortened provider object—cannot be distinguished from this single object; `PROVIDER_DELIVERY_TRUNCATION` describes the observed provider-level state without claiming the internal cause.

## 17. Original Provider Feasibility

Subject-1 evidence is favorable but not sufficient for full migration approval.

- **Official provenance:** favorable; source is the official ISRUC Cohort I public MEGA distribution.
- **Accessibility:** demonstrated for one public subject using official MEGAcmd without a personal account.
- **One-folder-per-subject:** demonstrated for subject 1.
- **Deterministic filenames:** demonstrated: `1.rec`, `1_1.*`, `1_2.*`.
- **Scale:** the official Cohort I archive is approximately 14.12 GB; a full acquisition was intentionally not performed.
- **Download reliability:** subject 1 completed successfully, but 99-subject reliability and resumability remain untested.
- **Channel schema:** correct for subject 1 and consistent with NEMAR I001.
- **Annotations:** two original scorer bundles are present and usable for subject 1.
- **Checksum availability:** local SHA-256 hashes are recorded; a per-file official MEGA checksum inventory was not available in the shell output.
- **Processing compatibility:** original REC parses under the existing EDF/REC formula and contains required channels/rates.
- **Reproducibility:** one bounded public-client acquisition is reproducible in principle; full-cohort reproducibility remains unresolved.

## 18. Migration Decision Evidence

Evidence supporting eventual original-provider migration:

- Original I001 body is complete.
- NEMAR I001 is structurally incomplete by 52,106,816 bytes.
- NEMAR retains an exact, physically identical prefix for both primary channels.
- Required channels and native rates are preserved in the tested subject.
- Original scorer-1 and scorer-2 prefixes align exactly with NEMAR’s retained events.

Evidence preventing approval now:

- Only one original subject has been acquired.
- Full original-provider acquisition reliability and resumability are not established.
- Cross-subject channel, annotation, and integrity variation is untested.
- No full-cohort reacquisition, validation, or accounting has been performed.
- The Step 7.2 core gate remains `CORE_DATA_BLOCKED`.

Decision: **COMPARISON_INCONCLUSIVE**, with strong subject-1 evidence of NEMAR provider truncation. Do not migrate yet.

## 19. Scientific Contract Impact

**NO SCIENTIFIC CONTRACT CHANGE.**

The comparison does not change:

- primary EEG channel contract (`C3-A2`);
- primary EOG channel contract (`LOC-A2`);
- label mapping;
- scorer-1 primary status;
- scorer-2 diagnostic status;
- 30-second epoch duration;
- target sampling rates (EEG 100 Hz, EOG 50 Hz);
- microvolt units;
- missingness semantics;
- target-free protocol;
- normalization or standardization policy.

No provider replacement was performed.

## 20. Existing Cohort Impact

The existing Step 7.1 ISRUC cohort remains **UNDER_REVIEW / SUPERSEDED_PENDING_PROVIDER_DECISION**. No 100-subject cohort was rebuilt. If migration is later approved, the required sequence is:

1. Reacquire all 100 expected original S1 subjects.
2. Validate every REC body against its declared size.
3. Validate required channels, rates, units, and annotation bundles.
4. Preprocess all eligible subjects under the frozen contract.
5. Supersede the NEMAR-derived cohort with a new versioned manifest.
6. Rerun determinism, QC, attrition, and accounting audits.
7. Reassess ISRUC viability before any split design.

## 21. Bibliographic Correction

The prior incorrect venue was **Sleep and Breathing**. The verified venue is:

Sirvan Khalighi, Teresa Sousa, José Moutinho Santos, Urbano Nunes. “ISRUC-Sleep: A comprehensive public dataset for sleep researchers.” *Computer Methods and Programs in Biomedicine*, volume 124, 2016, pages 180–192. DOI: `10.1016/j.cmpb.2015.10.013`.

Repository search confirms that the Step 7.3 feasibility report now uses the corrected venue. No scientific finding was changed because of this correction.

## 22. Tests Added

No production tests were added. This step created deterministic audit CSVs and a report from direct file measurements; no reusable production comparator was introduced that would justify a new unit-test surface. Existing tests were retained unchanged.

## 23. Validation

Completed validations:

- original file inventory generated;
- SHA-256 hashes computed for all five original files;
- original REC fixed/header fields parsed;
- original body-size formula passed with delta 0;
- NEMAR EDF fixed/header fields parsed;
- NEMAR body-size formula failed with the measured negative delta;
- channel order and labels compared;
- primary sampling rates compared;
- physical signal prefix compared for both primary channels;
- original TXT and XLSX annotation inventories inspected;
- scorer-1 and scorer-2 retained-prefix sequences compared;
- raw-data ignore rules checked with `git check-ignore`;
- no raw signal, raw annotation, or processed signal files are Git-tracked;
- no credentials were added to repository artifacts;
- comparison CSV structure and hashes validated;
- `git diff --check` passed before commit.

The full `pytest -q` and compileall validation commands were run successfully before the final commit; the exact live results are recorded in Section 28 and the final Git state was verified after commit.

## 24. Files Created

- `reports/STEP_07_3_ISRUC_PROVIDER_COMPARISON_REPORT.md`
- `reports/isruc_original_subject1_inventory.csv`
- `reports/isruc_subject1_provider_comparison.csv`

## 25. Files Modified

- No scientific source code, configuration, preprocessing contract, cohort manifest, or raw data was modified.
- The previously corrected `reports/STEP_07_3_ISRUC_ORIGINAL_PROVIDER_FEASIBILITY_REPORT.md` was verified to contain the corrected citation; it was not changed by this comparison report.

## 26. Explicitly Not Done

- No full ISRUC migration.
- No download of the remaining 99 subjects.
- No full-core preprocessing.
- No model.
- No training.
- No split generation.
- No normalization.
- No ML metrics.
- No SHHS bypass.
- No raw or processed signals committed.
- No push to GitHub.
- No change to the scientific contract.

## 27. Recommended Next Step

Because the provider decision is **COMPARISON_INCONCLUSIVE**, perform exactly one additional provider-comparison action: acquire and compare original ISRUC subject 2 against its NEMAR I002 artifact using the same bounded inventory, body-integrity, header, channel, primary-signal-prefix, and scorer-1/scorer-2 annotation checks.

Do not execute that action in Step 7.3. Do not download the remaining cohort or approve migration until the predeclared comparison sample and full-cohort acquisition plan are reviewed.

## 28. Git Status / Diff Summary

The required Step 7.3 report and two lightweight audit CSVs were committed; all original provider files and NEMAR raw/processed files remain ignored and untracked. Final live validation results:

- `pytest -q`: **PASS** — 46 passed in 7.93 s.
- `python -m compileall -q src tests scripts`: **PASS**.
- `git diff --check`: **PASS**.
- Inventory CSV: **PASS** — 5 rows, 9 columns.
- Provider comparison CSV: **PASS** — 30 rows, 5 columns.
- Raw ignore checks: **PASS** for representative `.rec`, `.txt`, and `.xlsx` files.
- Raw tracking check: **PASS** — no raw signal, annotation, or processed signal files tracked.
- Credentials check: **PASS** — no credentials added to created artifacts.

The final Git status was inspected before commit; only the three intended Step 7.3 report/CSV artifacts are staged. No push was performed.

Commit message required for this completed comparison:

`research: compare original and NEMAR ISRUC providers`
