# ShiftSleep-UQ Step 7.4 ISRUC Provider Replication Report

## 1. Status

**COMPLETE**

The predeclared two-subject replication panel was acquired and analyzed without acquiring subjects 4–100. The subject-level provider-integrity experiment is complete. The resulting migration policy is documented, but migration itself is not executed in Step 7.4.

## 2. Provider Decision

**MIGRATE_TO_ORIGINAL_ISRUC**

The three-subject panel establishes the required pattern: I001 and I002 are complete original recordings whose NEMAR objects are truncated but byte/physical-value faithful over the retained prefix; I003 is a complete NEMAR object whose full signal body is byte-identical to the original. The original provider is therefore selected for a future ISRUC-S1 signal/annotation rebuild. This decision does not authorize execution of that rebuild in this step.

## 3. Repository State

- Repository: `C:/Users/rohan/ShiftSleep-UQ`
- Branch: `main`
- Step 7.3 HEAD before this step: `01693c2e6af6604870f35d68ab622cd5d889cae2`
- Step 7.2 core gate: `CORE_DATA_BLOCKED`
- Step 7.3 report: `reports/STEP_07_3_ISRUC_PROVIDER_COMPARISON_REPORT.md`
- NEMAR release: `data/raw/isruc-nemar/v1.0.1/`
- Original source route: official ISRUC Cohort I public MEGA folder
- Original subject-2 bundle: `data/raw/isruc-original/subject-2/2/`
- Original subject-3 bundle: `data/raw/isruc-original/subject-3/3/`
- Raw data are ignored by `.gitignore` via `data/raw/**`.
- No personal MEGA account was used.
- No raw signal or annotation file was moved, replaced, staged, or committed.

## 4. Predeclared Replication Panel

The panel was recorded before original subject acquisition in `reports/isruc_provider_replication_panel.csv`:

| Subject | NEMAR ID | Role | Historical basis |
|---:|---|---|---|
| 2 | I002 | `KNOWN_TRUNCATED_REPLICATION` | Pre-existing NEMAR provider-body mismatch |
| 3 | I003 | `KNOWN_VALID_CONTROL` | Pre-existing NEMAR body-valid and preprocessing-included status |

The panel selection was based on historical provider-integrity status, not sleep-stage composition, signal appearance, or model performance. Both rows have `selected_before_original_download=true`.

## 5. Original Subject-2 Inventory

The official MEGAcmd listing contained exactly `2.rec`, `2_1.txt`, `2_1.xlsx`, `2_2.txt`, and `2_2.xlsx`. Inventory and hashes are recorded in `reports/isruc_original_subject2_inventory.csv`.

| File | Bytes | SHA-256 | Role/status |
|---|---:|---|---|
| `2.rec` | 157,619,120 | `adf2129c7a296a72d29a2b5f84955bfa4ad5b1913a9c741ebdbc261715ffd2b9` | original signal; body valid |
| `2_1.txt` | 2,892 | `08ed23beb35bfc821b319ea5674298efde4e6f623f3dafdf1d98a7d9ec80c11d` | scorer 1; unmodified |
| `2_1.xlsx` | 44,233 | `23690b1f559c55482ef600d261f669e231d7da1f9b0d3b5f3573d2cea77b7460` | scorer 1; unmodified |
| `2_2.txt` | 2,892 | `75ae479ead1defc3a0e9c36820f347870921977163f16040fbc1c39f420ba1f3` | scorer 2; unmodified |
| `2_2.xlsx` | 45,069 | `1595feb21e20bc8f9da015006a6ae0c15b5f3994382b9edd308e2b947b56d8fa` | scorer 2; unmodified |

## 6. Original Subject-3 Inventory

The official MEGAcmd listing contained exactly `3.rec`, `3_1.txt`, `3_1.xlsx`, `3_2.txt`, and `3_2.xlsx`. Inventory and hashes are recorded in `reports/isruc_original_subject3_inventory.csv`.

| File | Bytes | SHA-256 | Role/status |
|---|---:|---|---|
| `3.rec` | 154,185,620 | `92c2dc2efde9a811b4b5e458bc20f184493fc8af58077f509e1220407c1ddef7` | original signal; body valid |
| `3_1.txt` | 2,829 | `45fac8a128b91a4abeacec2dec95646ade6c6e3c17013132a3ad2f1bb08907b0` | scorer 1; unmodified |
| `3_1.xlsx` | 43,085 | `a901d489686939f97b84cd95b792222962dc7905dd679a4e1636ae64c639ffc0` | scorer 1; unmodified |
| `3_2.txt` | 2,829 | `e60b8f46afb85840b01c0b5e1b951d919e08210253680868b99ee59deef04c5e` | scorer 2; unmodified |
| `3_2.xlsx` | 43,631 | `6cc43382ba03082eb8ba13190ca3d8aa693ade3bff41dea7228a88c1386ca2c6` | scorer 2; unmodified |

## 7. Original REC Integrity

The unchanged body formula was applied independently to both original recordings:

`expected_total = header_length + number_of_records × sum(samples_per_signal_per_record) × 2`

| Subject | Header | Signals | Records | Record duration | Expected bytes | Actual bytes | Delta | Classification |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | 5,120 | 19 | 14,460 | 2.0 s | 157,619,120 | 157,619,120 | 0 | `ORIGINAL_BODY_VALID` |
| 3 | 5,120 | 19 | 14,145 | 2.0 s | 154,185,620 | 154,185,620 | 0 | `ORIGINAL_BODY_VALID` |

Both originals use 400 samples/record for the primary 200-Hz signals and the same 19-signal layout. No original body truncation or other body-integrity failure was observed.

## 8. NEMAR I002 Integrity

Measured local NEMAR I002 values:

- Path: `data/raw/isruc-nemar/v1.0.1/sub-I002_task-sleep_eeg.edf`
- Bytes: 58,458,112
- SHA-256: `114113de6519253f3099c356d19ca674f3c1be19af14bda1a9e16759f99fa35c`
- Provider/manifest bytes: 58,458,112
- Header: 5,120 bytes
- Declared records: 14,460
- Record duration: 2.0 s
- Computed expected total: 157,619,120 bytes
- Actual-minus-expected delta: -99,161,008 bytes
- Complete records: 5,362
- Partial-record bytes: 7,192
- Existing historical audit: checksum `MATCH`, header `PASS`, body `FAIL`, `EXCLUDED_PROVIDER_INTEGRITY`
- Classification: **NEMAR_BODY_TRUNCATED**

## 9. NEMAR I003 Integrity

Measured local NEMAR I003 values:

- Path: `data/raw/isruc-nemar/v1.0.1/sub-I003_task-sleep_eeg.edf`
- Bytes: 154,185,620
- SHA-256: `92c2dc2efde9a811b4b5e458bc20f184493fc8af58077f509e1220407c1ddef7`
- Provider/manifest bytes: 154,185,620
- Header: 5,120 bytes
- Declared records: 14,145
- Record duration: 2.0 s
- Computed expected total: 154,185,620 bytes
- Actual-minus-expected delta: 0 bytes
- Complete records: 14,145
- Partial-record bytes: 0
- Existing historical audit: checksum `MATCH`, header `PASS`, body `PASS`, `ACQUIRED`
- Classification: **NEMAR_BODY_VALID**

## 10. Header Comparison

The pairwise header comparison is recorded in `reports/isruc_provider_replication_header_comparison.csv`.

For both I002 and I003:

- Header length is equal between original and NEMAR.
- Signal count is equal: 19.
- Channel order and full channel labels are equal.
- Declared data-record count and record duration are equal.
- Recording start date/time are equal within each pair.
- Subject/patient fields are equal within each pair.
- Samples per signal per record are equal.
- Physical dimensions and digital min/max are equal.
- Physical min/max calibration ranges are equal.

I002 has an incomplete body despite a header declaring the full expected recording. I003 has a complete body with the same header and calibration fields as the original.

## 11. Channel / Sampling Comparison

Both pairs contain the same full 19-channel inventory in the same order:

`LOC-A2, ROC-A1, F3-A2, C3-A2, O1-A2, F4-A1, C4-A1, O2-A1, X1, X2, X3, X4, X5, X6, DC3, X7, X8, SaO2, DC8`

For both subjects:

| Required channel | Original presence/order | NEMAR presence/order | Native rate | Unit |
|---|---|---|---:|---|
| `C3-A2` | present, index 3 | present, index 3 | 200 Hz | `uV` |
| `LOC-A2` | present, index 0 | present, index 0 | 200 Hz | `uV` |

Classification for both pairs: **SAMPLING_EQUIVALENT**. No fallback channels, renaming, or scientific-contract change was introduced.

## 12. Subject-2 Signal Comparison

NEMAR I002 is truncated. The comparison used all 5,362 complete overlapping records.

- Common raw bytes compared: 58,450,920 bytes, including the common header and complete records.
- Raw prefix equality: `TRUE`.
- `C3-A2`: 2,144,800 common samples; max absolute difference 0.0 uV; mean absolute difference 0.0 uV; Pearson `r=1.0`.
- `LOC-A2`: 2,144,800 common samples; max absolute difference 0.0 uV; mean absolute difference 0.0 uV; Pearson `r=1.0`.
- Classification: **ACCURATE_TRUNCATED_PREFIX**.

The NEMAR I002 object retains an exact raw and calibrated physical-value prefix of the original subject-2 signal.

## 13. Subject-3 Signal Comparison

NEMAR I003 is complete. The entire signal body was compared.

- Full raw body equality after the common header convention: `TRUE`.
- Original and NEMAR signal SHA-256 values are identical.
- `C3-A2`: 5,658,000 samples; max absolute difference 0.0 uV; mean absolute difference 0.0 uV; Pearson `r=1.0`.
- `LOC-A2`: 5,658,000 samples; max absolute difference 0.0 uV; mean absolute difference 0.0 uV; Pearson `r=1.0`.
- Classification: **COMPLETE_EQUIVALENT** for signal content.

I003 is a complete, faithful NEMAR copy of the original signal object under the tested EDF/REC representation.

## 14. Original Annotation Audit

For both subjects, files with `_1` are scorer 1 and files with `_2` are scorer 2. The XLSX workbook IDs and source naming support this assignment.

| Subject | Scorer | TXT epochs | TXT vocabulary | XLSX nonempty rows | XLSX sheets | Workbook stage vocabulary |
|---:|---:|---:|---|---:|---|---|
| 2 | 1 | 964 | `{0,1,2,3,5}` | 965 including header | Sheet1 populated | `N1,N2,N3,R,W` |
| 2 | 2 | 964 | `{0,1,2,3,5}` | 965 including header | Sheet1 populated; Sheet2/3 empty | `N1,N2,N3,R,W,n2` |
| 3 | 1 | 943 | `{0,1,2,3,5}` | 944 including header | Sheet1 populated | `N1,N2,N3,R,W` |
| 3 | 2 | 943 | `{0,1,2,3,5}` | 944 including header | Sheet1 populated; Sheet2/3 empty | `N1,N2,N3,R,U,W` |

The XLSX archives passed ZIP integrity checks. Original raw annotation files were not modified.

## 15. Scorer-1 Comparison

The frozen exact stage-code mapping was used: `0=W`, `1=N1`, `2=N2`, `3=N3`, `5=R`.

| Subject | Original epochs | NEMAR events | Overlap matches | Mismatches | First mismatch | Missing NEMAR epochs | Extra NEMAR epochs |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 964 | 358 | 358 | 0 | none | 606 | 0 |
| 3 | 943 | 944 total / 943 positive-duration | 943 | 0 | none | 0 | 0 positive-duration; 1 zero-duration metadata row |

For I002, NEMAR contains 357 30-second events and one 14-second final event, ending at 10,724 s. For I003, NEMAR contains 943 positive-duration 30-second events and one zero-duration event; the positive-duration sequence matches all 943 original scorer-1 epochs.

## 16. Scorer-2 Comparison

Scorer 2 remains diagnostic only. The comparison used the original XLSX stage representation when it carried information not preserved by the numeric TXT encoding, especially subject-3 `U` labels.

| Subject | Original epochs | NEMAR scorer-2 values | Matches | Mismatches | Missing tail |
|---:|---:|---:|---:|---:|---:|
| 2 | 964 | 358 | 358 | 0 | 606 epochs |
| 3 | 943 | 943 positive-duration | 943 | 0 | 0 |

For subject 3, the original scorer-2 workbook contains `U` at the two positions represented as numeric `0` in the TXT file; NEMAR encodes these as `U=6` under its documented unknown-label policy. Workbook-level comparison therefore matches all 943 epochs. No diagnostic annotation discrepancy was hidden or remapped into scorer 1.

## 17. Duration / Truncation Findings

| Subject | Original signal duration | NEMAR declared duration | NEMAR complete duration | NEMAR partial extension | Original scorer-1 duration | NEMAR event span |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 28,920.0 s | 28,920.0 s | 10,724.0 s | approximately 1.3196 s | 28,920 s | 10,724.0 s |
| 3 | 28,290.0 s | 28,290.0 s | 28,290.0 s | 0 s | 28,290 s | 28,290.0 s |

I002 missing signal duration relative to its declared recording is approximately 18,196.0 s before the partial tail, with a body endpoint approximately 10,725.3196 s. Its event file ends at the complete-record boundary and does not represent the missing annotation tail. I003 has no signal or event-duration truncation.

## 18. Three-Subject Evidence Matrix

The matrix is recorded in `reports/isruc_three_subject_provider_evidence.csv`.

| ID | Historical status | Original valid | NEMAR valid | Original expected bytes | NEMAR actual bytes | NEMAR delta | Header equivalent | Channels equivalent | Sampling equivalent | Signal overlap identical | Scorer-1 identical | Scorer-2 identical | Classification |
|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| I001 | excluded provider integrity | yes | no | 143,885,120 | 91,778,304 | -52,106,816 | yes | yes | yes | yes | yes | yes | `ACCURATE_TRUNCATED_PREFIX` |
| I002 | excluded provider integrity | yes | no | 157,619,120 | 58,458,112 | -99,161,008 | yes | yes | yes | yes | yes | yes | `ACCURATE_TRUNCATED_PREFIX` |
| I003 | acquired/body valid | yes | yes | 154,185,620 | 154,185,620 | 0 | yes | yes | yes | yes | yes | yes | `COMPLETE_EQUIVALENT` |

The I003 scorer-2 equality is workbook-semantic equality, including the documented `U` representation; the original TXT’s numeric encoding is separately retained in its inventory.

## 19. Selective-Truncation Hypothesis

**SUPPORTED**

`H_PROVIDER`: NEMAR v1.0.1 preserves original ISRUC signal and annotation content faithfully where present, but a subset of published provider objects are prematurely truncated.

Evidence:

- I001 independently shows complete original, truncated NEMAR, and identical retained signal/annotation prefixes.
- I002 replicates the same pattern with a separate complete original and a separately truncated NEMAR object.
- I003 is a complete NEMAR control whose entire signal body is byte-identical to the original and whose primary/scorer-2 workbook-aligned annotations match.
- I003 demonstrates that NEMAR is not generally value-corrupt or universally truncated.

This is an engineering/provider-integrity finding, not a model result.

## 20. NEMAR Conversion-Policy Comparison

The NEMAR-provided ISRUC v1.0.1 README states the intended behavior: original `.rec` files are symlinked, or copied if needed, to `.edf` **without modification**; scorer-1 Excel labels are converted to 30-second events, and scorer-2 labels are stored as annotation extras. The current public dataset page is `https://nemar.org/dataset/nm000111`; the local NEMAR-provided policy text is `data/raw/metadata/isruc-nemar/v1.0.1/README.md`.

Observed evidence:

- I001 and I002 preserve the original EDF header and exact retained signal prefix but publish incomplete body objects.
- I003 preserves the complete signal body byte-for-byte.
- Primary annotation conversion matches the original retained/full sequence in all tested pairs.
- Scorer-2 extras match the original workbook semantics in all tested pairs.

Therefore, intended conversion behavior is consistent with content fidelity where bytes exist, while published-object integrity is selective: two of three tested NEMAR signal objects are prematurely truncated. The data do not establish the internal upstream mechanism, and no misconduct is inferred.

## 21. Provider Migration Evidence

Evidence in favor of original-provider migration:

- All three tested original REC bodies are structurally complete.
- Both historical truncated NEMAR cases, I001 and I002, replicate as provider-body truncations.
- Both truncated NEMAR objects retain exact original signal prefixes for `C3-A2` and `LOC-A2`.
- The known-valid NEMAR control I003 is complete and fully signal-equivalent.
- Required channels, native rates, units, calibration, and channel order are preserved.
- Original scorer-1 annotations are usable and align with NEMAR wherever NEMAR events exist.
- Original scorer-2 annotations are preserved diagnostically when compared using the workbook representation.
- Official public MEGA acquisition succeeded reproducibly for three individually addressable folders using the same official MEGAcmd mechanism.
- No scientific contract change is needed.

Remaining operational work is full-cohort acquisition and validation, not further justification from these three subjects.

## 22. Full Migration vs Hybrid Analysis

### Full original migration

Advantages:

- one authoritative original-provider route for all S1 signal and annotation bundles;
- uniform provenance and fewer provider-dependent inclusion rules;
- avoids systematically excluding subjects because a NEMAR object is truncated;
- cleaner final cohort manifest and reproducibility story.

Costs:

- approximately 14.12 GB source-scale acquisition according to the official Cohort I source description;
- MEGAcmd public-folder operational dependency;
- per-subject body, channel, annotation, and checksum validation for all 100 subjects;
- temporary disk and transfer-retry requirements.

### Hybrid provider

Advantages:

- could retain independently body-valid NEMAR objects and reacquire only invalid cases.

Costs:

- mixed provenance and more complicated manifest logic;
- every retained NEMAR object still requires complete integrity validation;
- provider choice becomes correlated with integrity status;
- future reruns must preserve separate source-specific rules.

Decision: full original-provider migration is scientifically cleaner than a hybrid, provided the full acquisition and validation gates in the migration plan pass. The migration is approved as a future policy, not executed here.

## 23. Provider Decision Rationale

The decision is **MIGRATE_TO_ORIGINAL_ISRUC** because the three-subject panel satisfies the substantive evidence pattern required by this step: original viability, replicated selective NEMAR truncation, NEMAR content fidelity where present, and a complete faithful control. A hybrid is not preferred because it would retain a provider whose integrity failures are selective and would create source-dependent cohort membership.

This decision is not based on convenience or file size alone. It is based on body-integrity formulas, identical headers/calibration, raw-prefix equality, exact physical signal agreement, and annotation alignment. Full migration remains gated on the 100-subject acquisition and validation plan.

## 24. Scientific Contract Impact

**NO SCIENTIFIC CONTRACT CHANGE.**

Provider policy does not change:

- EEG channel: `C3-A2`;
- EOG channel: `LOC-A2`;
- scorer 1 as primary;
- scorer 2 as diagnostic;
- frozen stage labels and exact mapping;
- 30-second epochs;
- target sampling rates: EEG 100 Hz and EOG 50 Hz;
- microvolt units;
- missingness semantics;
- target-free protocol;
- unnormalized/unstandardized outputs.

## 25. Existing Cohort Impact

The Step 7.1 ISRUC cohort remains **UNDER_REVIEW / SUPERSEDED_PENDING_PROVIDER_DECISION**. No 100-subject cohort was rebuilt, no old 15-subject retention was promoted to final status, and no split or model artifact was created.

If the migration plan is executed later, the NEMAR-derived cohort must be superseded only after complete original-provider acquisition, validation, preprocessing, manifest regeneration, determinism/QC/accounting reruns, and a fresh accessible-core decision.

## 26. Full-Cohort Migration Plan

**Created, not executed:** `docs/isruc_original_migration_plan.md`.

The plan specifies:

- deterministic enumeration of all 100 expected S1 subject folders;
- per-subject source-file expectations;
- bounded/resumable official MEGAcmd acquisition;
- immutable ignored raw storage;
- SHA-256 and REC body-integrity validation;
- required-channel and rate checks;
- scorer-1/scorer-2 validation;
- restart/resume policy;
- acquisition manifest and terminal statuses;
- no unofficial mirrors or stage-based replacement;
- approximate official source scale of 14.12 GB;
- processed storage marked `NOT COMPUTED` until the frozen output representation is measured.

The plan was not run, and subjects 4–100 were not acquired.

## 27. Tests Added

No reusable production comparator was introduced, so no production tests were added. Existing tests were retained unchanged. The comparison itself was executed through deterministic validation scripts and its outputs were checked into lightweight audit CSVs only.

## 28. Validation

Final validation results:

- `pytest -q`: **PASS** — 46 passed.
- `python -m compileall -q src tests scripts`: **PASS**.
- `git diff --check`: **PASS**.
- Panel CSV: parsed successfully with 2 predeclared rows.
- Header comparison CSV: parsed successfully with pairwise fields.
- Three-subject evidence CSV: parsed successfully with 3 rows.
- Subject-2 inventory CSV: parsed successfully with 5 rows.
- Subject-3 inventory CSV: parsed successfully with 5 rows.
- Original subject-2 and subject-3 hashes/body sizes: verified.
- NEMAR I002 and I003 hashes/body sizes: independently verified.
- Signal-prefix/full-body comparisons: verified for both pairs.
- Scorer-1 and scorer-2 comparisons: verified with workbook-aware `U` handling.
- Representative original `.rec`, `.txt`, and `.xlsx` paths: ignored by Git.
- NEMAR raw EDF and processed signal tracking check: no raw/processed signal files tracked.
- Credential check: no credentials, signed URLs, or session material added to artifacts.
- No subjects 4–100 acquired.

## 29. Files Created

- `reports/isruc_provider_replication_panel.csv`
- `reports/isruc_original_subject2_inventory.csv`
- `reports/isruc_original_subject3_inventory.csv`
- `reports/isruc_provider_replication_header_comparison.csv`
- `reports/isruc_three_subject_provider_evidence.csv`
- `docs/isruc_original_migration_plan.md`
- `reports/STEP_07_4_ISRUC_PROVIDER_REPLICATION_REPORT.md`

## 30. Files Modified

- No scientific source code modified.
- No preprocessing configuration modified.
- No scientific channel, label, scorer, epoch, sampling, unit, missingness, or target-free contract modified.
- No existing NEMAR artifact modified or replaced.
- No raw original-provider file modified.

## 31. Explicitly Not Done

- No subjects 4–100 acquired.
- No full ISRUC migration.
- No full-core preprocessing.
- No splits.
- No models.
- No training.
- No normalization.
- No ML metrics.
- No calibration.
- No SHHS bypass.
- No raw or processed data committed.
- No push to GitHub.

## 32. Recommended Next Step

Because the provider decision is **MIGRATE_TO_ORIGINAL_ISRUC**, the next step is to execute the deterministic full original-provider ISRUC-S1 acquisition and validation plan for all 100 expected subject bundles, followed by a complete cohort rebuild and audit before split design.

That next step must be separately authorized and must use `docs/isruc_original_migration_plan.md`. It was not executed here.

## 33. Git Status / Diff Summary

Only safe reports, audit CSVs, and the non-executed migration-plan documentation are eligible for commit. Raw `.rec`, raw annotation `.txt/.xlsx`, NEMAR EDF, and processed signal files remain ignored and untracked.

Required commit message for this approved migration-policy decision:

`research: approve original ISRUC provider migration`

No push is permitted by this step.
