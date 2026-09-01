# ShiftSleep-UQ Step 6.1 Preprocessing Repair Report

## 1. Status

COMPLETE

Step 6.1 repaired the ISRUC annotation canonicalization defect, added strict record-level accounting, rebuilt the smoke outputs, validated the deterministic third Sleep-EDF SC subject, and completed the smoke gate without executing model work.

## 2. Pipeline Gate

PIPELINE_VALIDATED

The Step 6.1 smoke gate is validated for the accessible smoke cohort. The final benchmark remains separately unfrozen because SHHS1 authorized raw/XML access and per-record validation are still pending.

## 3. Repository State

* repository: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* pre-step HEAD: `7958b865264a89674ca1775cde95f965ba0b11a7`
* known Step 6 implementation commit: `0737d527967b482e69daf3c5abbdb6838f2880d7`
* Step 6 report commit before this step: `7958b865264a89674ca1775cde95f965ba0b11a7`
* push status: `NOT PUSHED`
* protected project check: no intentional changes made to `SHIFT-ICD`; one timed-out acquisition command was verified not to leave an artifact there
* frozen scientific decisions retained: EEG+EOG, required channels, scorer-1 primary, 30-second epochs, target rates, canonical labels, and target-free preprocessing

The final local Step 6.1 commit is recorded by the final `git rev-parse HEAD` and Git status verification after this report is committed.

## 4. Trigger for Repair

The NEMAR ISRUC v1.0.1 documentation states that the event mapping is:

* `0`: `Sleep stage W`
* `1`: `Sleep stage N1`
* `2`: `Sleep stage N2`
* `3`: `Sleep stage N3`
* `5`: `Sleep stage R`
* `6`: `Sleep stage U`

The previous implementation accepted `Sleep stage 1`, `Sleep stage 2`, and `Sleep stage 3`, which are Sleep-EDF-style numbered spellings, but did not accept the exact NEMAR strings `Sleep stage N1`, `Sleep stage N2`, and `Sleep stage N3`. Consequently, the previous ISRUC output retained only Wake and REM among valid labels and reported zero N1/N2/N3.

The previous Step 6 report also stated 955 valid ISRUC epochs but an aggregate canonical stage table totaling 725 epochs. The exact reconciliation is documented in Section 11.

## 5. Verified NEMAR Event Schema

Authoritative source checked:

* NEMAR repository README: `https://raw.githubusercontent.com/nemarDatasets/nm000111/main/README.md`
* NEMAR event metadata: `https://raw.githubusercontent.com/nemarDatasets/nm000111/main/sub-I003/eeg/sub-I003_task-sleep_events.json`
* local mirrored metadata: `data/raw/metadata/isruc-nemar/v1.0.1/README.md`

Verified schema:

* primary event field: `trial_type`
* exact primary labels: `Sleep stage W`, `Sleep stage N1`, `Sleep stage N2`, `Sleep stage N3`, `Sleep stage R`, `Sleep stage U`
* documented numeric codes: `0`, `1`, `2`, `3`, `5`, and `6`, respectively
* event duration: 30 seconds for staging epochs
* event onset: epoch start in seconds
* `value`: event code; retained as source evidence but not used as a generic numeric-label shortcut
* `sample`: event onset in sampling points
* scorer relationship: events are generated from scorer-1 Excel labels; scorer-2 labels are retained separately in `scorer2_label` and `scorer2_label_value` extras
* required event columns verified: `onset`, `duration`, `trial_type`, `value`, `sample`, `scorer2_label`, `scorer2_label_value`
* source field frozen in code as `ISRUC_PRIMARY_EVENT_FIELD = "trial_type"`

The terminal `Sleep stage U` rows in I003 and I005 have duration `0.0`. I004 has three `Sleep stage U` rows: two with duration `30.0` and one with duration `0.0`. Zero-duration events are BIDS impulse/non-stage events and are retained in the raw audit but do not enter the staging-epoch denominator.

## 6. Root Cause

Two independent defects were identified:

1. **ISRUC mapping defect.** `canonicalize_label()` in `src/shiftsleep_uq/data/preprocessing.py` lacked the exact strings `Sleep stage N1`, `Sleep stage N2`, and `Sleep stage N3`. The old implementation therefore classified those source-supported labels as unknown and excluded them.
2. **Historical aggregate audit defect.** The Step 6 per-record old values were Wake/REM counts of I003 `132/227`, I004 `28/230`, and I005 `296/42`. These sum to Wake `456` and REM `499`, and therefore to the old valid total `955`. The Step 6 report recorded aggregate REM as `269` instead of `499`, producing `456+269=725`. The missing `230` was exactly a stale aggregate reporting error, not an unaccounted persisted epoch in the old per-record rows.

The corrected runner regenerates stage counts directly from each persisted label array and uses explicit source-stage, valid, and exclusion fields.

## 7. Code Correction

Changed files/functions:

* `src/shiftsleep_uq/data/preprocessing.py`
  * added exact NEMAR labels `Sleep stage N1`, `Sleep stage N2`, and `Sleep stage N3`
  * added explicit `Sleep stage U` unknown handling
  * retained exact Sleep-EDF numbered/R&K aliases
  * made label matching exact after whitespace normalization; lowercase/fuzzy variants are not silently accepted
  * changed zero-duration event handling so impulse/non-stage events do not become staging epochs
  * added `summarize_epoch_accounting()` in the orchestration boundary
* `src/shiftsleep_uq/data/preprocess.py`
  * validates the complete NEMAR event-table schema
  * continues to use only `trial_type` for primary labels
  * persists per-stage and per-exclusion counts in processing rows
  * enforces accounting invariant D for expanded staging epochs
* `src/shiftsleep_uq/data/adapters/isruc.py`
  * added `ISRUC_PRIMARY_EVENT_FIELD`, scorer-2 field declarations, and the verified label-code table
* `configs/data_contract_v1.yaml`
  * recorded the verified NEMAR string representations without changing canonical labels, channels, scorer policy, rates, epoch duration, or missingness semantics
* `tests/test_preprocessing.py`
  * added exact NEMAR labels, strict unknown/fuzzy rejection, zero-duration handling, and accounting tests
* `tests/test_isruc_integration.py`
  * added non-network integration validation against the locally acquired public NEMAR event files
* `scripts/step_06_1_repair.py`
  * reproducibly regenerates raw annotation audits, smoke manifests, accounting audits, signal comparisons, and determinism evidence

## 8. Raw ISRUC Annotation Audit

Artifact: `reports/isruc_raw_annotation_audit.csv`

| subject | raw value | count | duration values |
|---|---|---:|---|
| I003 | Sleep stage W | 132 | 30 |
| I003 | Sleep stage N1 | 165 | 30 |
| I003 | Sleep stage N2 | 246 | 30 |
| I003 | Sleep stage N3 | 173 | 30 |
| I003 | Sleep stage R | 227 | 30 |
| I003 | Sleep stage U | 1 | 0 |
| I004 | Sleep stage W | 28 | 30 |
| I004 | Sleep stage N1 | 63 | 30 |
| I004 | Sleep stage N2 | 426 | 30 |
| I004 | Sleep stage N3 | 214 | 30 |
| I004 | Sleep stage R | 230 | 30 |
| I004 | Sleep stage U | 3 | 0; 30 |
| I005 | Sleep stage W | 296 | 30 |
| I005 | Sleep stage N1 | 108 | 30 |
| I005 | Sleep stage N2 | 265 | 30 |
| I005 | Sleep stage N3 | 164 | 30 |
| I005 | Sleep stage R | 42 | 30 |
| I005 | Sleep stage U | 1 | 0 |

All rows use `trial_type` and include the source event-file SHA256 in the CSV.

## 9. Corrected ISRUC Stage Counts

| subject | source staging epochs | Wake | N1 | N2 | N3 | REM | excluded unknown | valid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| I003 | 943 | 132 | 165 | 246 | 173 | 227 | 0 | 943 |
| I004 | 963 | 28 | 63 | 426 | 214 | 230 | 2 | 961 |
| I005 | 875 | 296 | 108 | 265 | 164 | 42 | 0 | 875 |

The two I004 unknown exclusions are the two 30-second `Sleep stage U` events. The zero-duration U event in each relevant file is not a staging epoch.

## 10. Accounting Reconciliation

Artifact: `reports/preprocessing_accounting_audit.csv`

| source | recording | source epochs | valid | excluded | accounted | delta | status |
|---|---|---:|---:|---:|---:|---:|---|
| Sleep-EDF SC | SC4001E0 | 2880 | 2650 | 230 | 2880 | 0 | PASS |
| Sleep-EDF SC | SC4002E0 | 2880 | 2829 | 51 | 2880 | 0 | PASS |
| Sleep-EDF SC | SC4011E0 | 2880 | 2802 | 78 | 2880 | 0 | PASS |
| Sleep-EDF SC | SC4021E0 | 2880 | 2804 | 76 | 2880 | 0 | PASS |
| ISRUC-S1 | I003 | 943 | 943 | 0 | 943 | 0 | PASS |
| ISRUC-S1 | I004 | 963 | 961 | 2 | 963 | 0 | PASS |
| ISRUC-S1 | I005 | 875 | 875 | 0 | 875 | 0 | PASS |

For every successful record:

* valid canonical epochs equal Wake + N1 + N2 + N3 + REM;
* source staging epochs equal valid plus excluded epochs;
* persisted EEG, EOG, and labels have the same first dimension as valid canonical epochs;
* mutually exclusive exclusion counts sum to total excluded epochs.

## 11. Previous 230-Epoch Discrepancy

The previous ISRUC valid counts were:

* I003: 359 = Wake 132 + REM 227
* I004: 258 = Wake 28 + REM 230
* I005: 338 = Wake 296 + REM 42
* total valid: 955

The previous per-record aggregate table contained:

* Wake: `132+28+296 = 456`
* REM: `227+230+42 = 499`
* correct represented total: `456+499 = 955`

The Step 6 report instead recorded aggregate REM as `269`. Therefore its aggregate table totaled `456+269 = 725`, exactly 230 below the valid total. The 230 was not a missing source epoch; it was an aggregate report-generation/count transcription error that omitted 230 REM epochs.

The separate label-mapping defect excluded the source-supported N1/N2/N3 epochs. Those excluded counts were 584 for I003, 703 for I004, and 537 for I005, with the remaining U/zero-duration behavior handled explicitly above.

## 12. ISRUC Exclusion-Rate Change

| subject | Step 6 valid | Step 6 excluded | Step 6.1 valid | Step 6.1 excluded | Step 6.1 exclusion reasons |
|---|---:|---:|---:|---:|---|
| I003 | 359 | 585 | 943 | 0 | none among staging epochs; one zero-duration U event is non-stage |
| I004 | 258 | 706 | 961 | 2 | two `Sleep stage U` 30-second epochs |
| I005 | 338 | 538 | 875 | 0 | none among staging epochs; one zero-duration U event is non-stage |

The large previous exclusion rates were caused primarily by the missing exact N1/N2/N3 mappings. Valid N1/N2/N3 labels are no longer classified as unknown. The remaining I004 unknown exclusions are source-declared U staging epochs and are not silently relabeled.

## 13. Signal Regression

Artifact: `reports/signal_annotation_repair_comparison.csv`

For I003, I004, and I005, old and new signal arrays were compared by the preserved common `source_epoch_indices`, not by output position. This is required because the corrected output contains newly restored source epochs and therefore has a different row count.

Results:

* I003 common source epochs: 359; EEG equal: `True`; EOG equal: `True`; labels equal: `False`
* I004 common source epochs: 258; EEG equal: `True`; EOG equal: `True`; labels equal: `False`
* I005 common source epochs: 338; EEG equal: `True`; EOG equal: `True`; labels equal: `False`

The annotation repair changed labels and output hashes but did not change signal preprocessing for comparable source epochs.

Signal contract remains unchanged: EEG target 100 Hz, EOG target 50 Hz, 3000/1500 samples per epoch, explicit microvolt units, continuous-before-epoch polyphase resampling, and no additional filtering or normalization.

## 14. I001/I002 Acquisition Investigation

Artifact: `reports/isruc_acquisition_integrity_audit.csv`

| subject | local/provider bytes | EDF-declared bytes | delta | provider evidence | result |
|---|---:|---:|---:|---|---|
| I001 | 91,778,304 | 143,885,120 | -52,106,816 | HTTP 200; Content-Length 91,778,304; ETag `sha256:900755de…` | invalid provider object |
| I002 | 58,458,112 | 157,619,120 | -99,161,008 | HTTP 200; Content-Length 58,458,112; ETag `sha256:114113de…` | invalid provider object |

Both files contain parseable EDF headers but their bodies terminate early relative to the declared record/sample counts. The provider itself advertises the shorter Content-Length, so this is not evidence of a local parser truncation or DataLad/git-annex pointer file. They remain quarantined and were not substituted into the smoke cohort. EDF body-size validation was not weakened. No resumable retry could establish a complete provider object; no invalid file was promoted or used.

## 15. Sleep-EDF Third Subject Repair

* requested candidate: `SC4021E0`
* result: successful bounded official PhysioNet acquisition
* PSG: `SC4021E0-PSG.edf`, validated body size `51,147,008` bytes
* exact matching hypnogram: `SC4021EH-Hypnogram.edf`, validated by `pyedflib`, 161 annotations
* deterministic rule: next lexicographic structurally valid subject after the prior failed candidate path; no stage or signal-property selection
* final unique SC subjects: 3
  * SC_00: SC4001E0 and SC4002E0
  * SC_01: SC4011E0
  * SC_02: SC4021E0

SC4021E0 output: 2,804 valid canonical epochs; 76 explicit unknown exclusions; Wake 1,907; N1 94; N2 545; N3 95; REM 163.

## 16. Final Smoke Cohort

| dataset | subject group | recording | status |
|---|---|---|---|
| Sleep-EDF SC | SC_00 | SC4001E0 | SUCCESS |
| Sleep-EDF SC | SC_00 | SC4002E0 | SUCCESS |
| Sleep-EDF SC | SC_01 | SC4011E0 | SUCCESS |
| Sleep-EDF SC | SC_02 | SC4021E0 | SUCCESS |
| ISRUC-S1 | I003 | I003 | SUCCESS |
| ISRUC-S1 | I004 | I004 | SUCCESS |
| ISRUC-S1 | I005 | I005 | SUCCESS |

All nights/recordings are retained under their subject identity; no epoch-level subject splitting was performed.

## 17. Final Smoke Preprocessing Results

Data engineering only; no model results were produced.

| dataset | recording | valid epochs | EEG shape | EOG shape | canonical unit | NaN/Inf |
|---|---|---:|---|---|---|---|
| Sleep-EDF SC | SC4001E0 | 2650 | `(2650, 3000)` | `(2650, 1500)` | uV | 0/0 |
| Sleep-EDF SC | SC4002E0 | 2829 | `(2829, 3000)` | `(2829, 1500)` | uV | 0/0 |
| Sleep-EDF SC | SC4011E0 | 2802 | `(2802, 3000)` | `(2802, 1500)` | uV | 0/0 |
| Sleep-EDF SC | SC4021E0 | 2804 | `(2804, 3000)` | `(2804, 1500)` | uV | 0/0 |
| ISRUC-S1 | I003 | 943 | `(943, 3000)` | `(943, 1500)` | uV | 0/0 |
| ISRUC-S1 | I004 | 961 | `(961, 3000)` | `(961, 1500)` | uV | 0/0 |
| ISRUC-S1 | I005 | 875 | `(875, 3000)` | `(875, 1500)` | uV | 0/0 |

Persisted signals are float32, unnormalized, unstandardized, and stored as compressed NPZ files under ignored local data paths.

## 18. Stage/Exclusion Audit

Artifact: `reports/preprocessing_epoch_audit.csv`

The regenerated audit contains seven successful recording rows. Canonical stage counts are:

| recording | Wake | N1 | N2 | N3 | REM | explicit exclusions |
|---|---:|---:|---:|---:|---:|---:|
| SC4001E0 | 1997 | 58 | 250 | 220 | 125 | 230 other |
| SC4002E0 | 1885 | 59 | 373 | 297 | 215 | 51 other |
| SC4011E0 | 1856 | 109 | 562 | 105 | 170 | 78 other |
| SC4021E0 | 1907 | 94 | 545 | 95 | 163 | 76 unknown |
| I003 | 132 | 165 | 246 | 173 | 227 | 0 |
| I004 | 28 | 63 | 426 | 214 | 230 | 2 unknown |
| I005 | 296 | 108 | 265 | 164 | 42 | 0 |

No canonical class appears in unknown exclusions. The only ISRUC unknown exclusions are source label `Sleep stage U` staging epochs.

## 19. Determinism

Artifact: `reports/determinism_hashes.txt` and `reports/determinism_hashes.csv`

Repeated full output hashes were identical:

* SC4001E0: `dcfccecdcebecc9767d82e4339753528545dfe5db2f9d23a8c4ef30aa6ccc4f7` on both runs
* I003: `485ce6d4c077194f80017efd3666174e4f141f043fa0ff4bc35b0cef6a2ed0b8` on both runs

The persisted labels, EEG arrays, EOG arrays, shapes, and metadata are deterministic for repeated processing from the same raw inputs.

## 20. Accounting Invariants

All seven successful records passed:

* **Invariant A:** `valid_canonical_epochs = Wake + N1 + N2 + N3 + REM`
* **Invariant B:** `source_stage_epochs = valid_canonical_epochs + excluded_stage_epochs`
* **Invariant C:** `EEG.shape[0] = EOG.shape[0] = labels.shape[0] = valid_canonical_epochs`
* **Invariant D:** mutually exclusive exclusion counts sum to `excluded_stage_epochs`

All values in `reports/preprocessing_accounting_audit.csv` have `accounting_delta=0` and `status=PASS`.

## 21. Tests Added

* exact `Sleep stage W` -> Wake
* exact `Sleep stage N1` -> N1
* exact `Sleep stage N2` -> N2
* exact `Sleep stage N3` -> N3
* exact `Sleep stage R` -> REM
* `Sleep stage U` -> explicit unknown exclusion
* arbitrary unknown labels never map to Wake
* lowercase/fuzzy variants are not silently accepted
* Sleep-EDF numbered mappings remain valid
* R&K Stage 3/4 -> N3 remains valid
* zero-duration events do not enter staging epochs
* record-level canonical and exclusion accounting
* real local NEMAR event-table integration for I003/I004/I005
* signal comparison by preserved source epoch identity
* deterministic output checks

## 22. Full Validation

Actual commands/results:

* `pytest -q tests/test_preprocessing.py tests/test_isruc_integration.py`: **27 passed**
* `pytest -q`: **39 passed**
* `python -m compileall -q src tests scripts`: passed, exit code 0
* `git diff --check`: passed
* manifest validation: 7 successful smoke rows; all required arrays, labels, finite values, hashes, and source/annotation paths validated
* raw annotation validation: 19 aggregate rows across I003/I004/I005; exact source labels and duration diversity recorded
* accounting validation: 7 rows; all `accounting_delta=0`; all `PASS`
* contract validation: version `1.1.0`; status `CORE_PREPROCESSING_FROZEN`; final benchmark frozen `false`; canonical labels/channels/scorer/rates unchanged
* preprocessing validation: target EEG 100 Hz, EOG 50 Hz; epoch lengths 3000/1500; unit uV; no normalization; no additional filtering
* determinism validation: SC4001E0 and I003 repeated output hashes identical
* signal regression validation: I003/I004/I005 common source epochs have identical EEG/EOG arrays; labels changed as expected
* forbidden artifact scan: no unignored `.edf`, `.rec`, or `.npz` signal artifacts detected
* credential scan: no retained credentials, signed URLs, cookies, tokens, or API keys
* GitHub push: not performed

## 23. Files Created

* `reports/STEP_06_1_PREPROCESSING_REPAIR_REPORT.md`
* `reports/isruc_raw_annotation_audit.csv`
* `reports/preprocessing_accounting_audit.csv`
* `reports/signal_annotation_repair_comparison.csv`
* `reports/isruc_acquisition_integrity_audit.csv`
* `reports/determinism_hashes.csv`
* `reports/determinism_hashes.txt`
* `scripts/step_06_1_repair.py`
* `tests/test_isruc_integration.py`
* corrected ignored local outputs under `data/processed/core_v1/` are not Git artifacts

## 24. Files Modified

* `src/shiftsleep_uq/data/preprocessing.py`
* `src/shiftsleep_uq/data/preprocess.py`
* `src/shiftsleep_uq/data/adapters/isruc.py`
* `configs/data_contract_v1.yaml` — source-label representation repair only; canonical scientific decisions unchanged
* `tests/test_preprocessing.py`
* `reports/preprocessing_smoke_manifest.csv`
* `reports/preprocessing_epoch_audit.csv`
* `reports/determinism_hashes.txt`

Raw EDF/TSV/JSON inputs and processed NPZ signals remain ignored and uncommitted.

## 25. Explicitly Not Done

Confirmed:

* no model
* no training
* no full-core preprocessing
* no normalization
* no new filtering
* no final train/dev/test splits
* no experimental ML metrics
* no target calibration
* no SHHS access bypass
* no SHHS processing
* no raw or processed signal files committed
* no GitHub push

## 26. Remaining Core Blockers

None for the Step 6.1 accessible smoke gate. The repaired ISRUC records and deterministic third SC subject passed the required smoke, accounting, signal-regression, and determinism checks.

I001 and I002 remain quarantined invalid provider objects and are not required for the frozen smoke cohort because I003–I005 are the selected valid deterministic ISRUC smoke records.

## 27. Remaining Final-Benchmark Blockers

* SHHS1 authorized raw/XML access remains pending.
* SHHS1 exact required-channel, sampling-rate, unit, identity, and annotation validation remain incomplete.
* The final benchmark remains `final_benchmark_frozen: false`.
* Full accessible-core acquisition and preprocessing have not been executed in this step.

## 28. Recommended Next Step

Full accessible-core acquisition and preprocessing with dataset-wide integrity auditing, still without model training, may be considered only after independent review of this Step 6.1 repair and the separate SHHS1 access gate. Step 7 was not executed.

## 29. Git Status / Diff Summary

The Step 6.1 changes are intended for one local commit with message:

`fix: repair ISRUC annotation preprocessing`

The final local commit hash, clean/dirty status, staged-file list, and diff-check result are recorded by the final post-commit verification. No push was performed. Raw EDF/TSV/JSON source files, processed NPZ files, and QC signal artifacts are ignored and are not commit candidates.
