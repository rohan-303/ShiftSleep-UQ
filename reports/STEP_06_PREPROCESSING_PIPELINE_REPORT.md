# ShiftSleep-UQ Step 6 Preprocessing Pipeline Report

## 1. Status

PARTIAL

The deterministic core preprocessing implementation and six-record signal smoke execution completed. The requested three-subject Sleep-EDF SC smoke cohort was not fully acquired because the next deterministic replacement record, `SC4021E0`, was unavailable during the final acquisition attempts due to repeated PhysioNet DNS failure. The record is explicitly represented as failed; no substitute was selected based on stage composition or signal behavior.

## 2. Pipeline Gate

PIPELINE_PARTIAL

The implementation, tests, unit handling, resampling, annotation alignment, output integrity, and deterministic repeated-run checks passed. The gate is partial only because the subject-level SC smoke target could not be fully acquired and validated after applying the frozen selection rule and replacement rule.

## 3. Final Benchmark Gate

NO

The final benchmark remains unfrozen. SHHS1 raw/XML access and per-record validation remain pending and were not bypassed.

## 4. Repository State

* path: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* Step 5.1 commit: `31966e93f65f82027cae297893f721e35dc500e0`
* Step 6 implementation commit: `0737d527967b482e69daf3c5abbdb6838f2880d7`
* Step 6 report-finalization commit: recorded by the final HEAD verification below
* push status: not pushed; no GitHub push was performed
* repository preflight: clean before Step 6 implementation

## 5. Dependency Environment

Exact versions observed in the project Python environment:

* Python 3.11.15
* numpy 2.4.3 — array storage, finite-value checks, deterministic signal slicing, and NPZ serialization
* scipy 1.17.1 — `scipy.signal.resample_poly` continuous anti-aliased downsampling
* pandas 3.0.5 — existing metadata inspection only; not required by the runtime pipeline
* PyYAML 6.0.3 — contract/config loading and validation
* pyedflib 0.1.42 — EDF/EDF+ signal and annotation reading
* xlrd 2.0.2 — existing legacy spreadsheet inspection; not required by the runtime pipeline

Declared runtime dependencies were added to `pyproject.toml`: numpy, scipy, PyYAML, and pyedflib. No PyTorch, TensorFlow, MNE, or training framework was installed.

## 6. Data Contract

* version: `1.1.0`
* status: `CORE_PREPROCESSING_FROZEN`
* `final_benchmark_frozen`: `false`
* SHA256: `38d14605d8fa9dbc107e4f54e08ace2d3bce6e9b32417d1b83ba19b2c2a1bcee`
* source: `configs/data_contract_v1.yaml`

The frozen contract was not changed during Step 6.

## 7. Preprocessing Contract

* version: `0.1.0`
* SHA256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`
* source: `configs/preprocessing_v1.yaml`
* code commit at initial hash stage: `31966e93f65f82027cae297893f721e35dc500e0`

The preprocessing config references data-contract version `1.1.0` and contains implementation parameters only.

## 8. Canonical Output

* EEG shape: `[n_epochs, 3000]`
* EOG shape: `[n_epochs, 1500]`
* dtype: `float32` for persisted signal arrays
* unit: canonical microvolts (`uV`/`µV`)
* labels: integer mapping obtained from the frozen canonical order `Wake=0, N1=1, N2=2, N3=3, REM=4`
* output format: one compressed NPZ per recording under ignored `data/processed/core_v1/`
* persisted data are unnormalized, unstandardized, and contain no model-specific transforms

## 9. Unit Harmonization

Sleep-EDF SC signal headers reported `uV` for both `EEG Fpz-Cz` and `EOG horizontal`; the adapter accepts the explicit microvolt unit and applies factor `1.0`.

ISRUC-S1 NEMAR EDF headers reported `uV` for `C3-A2` and `LOC-A2`; the adapter accepts the explicit microvolt unit and applies factor `1.0`.

The conversion layer separately validates `V -> 1e6`, `mV -> 1e3`, and `uV/µV -> 1`. Unknown units raise `STRUCTURAL_UNIT_MISMATCH`; no unit was guessed. No contract amendment was necessary.

## 10. Sleep-EDF Adapter

* file matching: exact PSG filename `<recording>-PSG.edf`; exact official hypnogram pairing using the same subject/night token and the source suffix present (`C` or `H`)
* subject/night identity: frozen Sleep-EDF filename rule; all nights retain the shared subject identity for grouping
* channels: `EEG Fpz-Cz` and `EOG horizontal`
* annotations: official Sleep-EDF hypnogram EDF+ annotations
* native rates: EEG 100 Hz and EOG 100 Hz
* unit behavior: explicit `uV` validation and conversion to canonical microvolts
* processed successful records: `SC4001E0`, `SC4002E0`, `SC4011E0`
* deterministic failed replacement: `SC4021E0`, acquisition failure due PhysioNet DNS unavailability; no output was written

The invalid `SC4012E0` download was not used as a valid input because its file-size/header relationship failed EDF validation.

## 11. ISRUC Adapter

* source/distribution: NEMAR BIDS derivative `nm000111`, version `v1.0.1`
* subject identity: `sub-I###` participant identifier
* channels: EEG `C3-A2`; EOG `LOC-A2`
* scorer policy: scorer 1 is primary; scorer 2 remains diagnostic metadata and never modifies or deletes a valid scorer-1 epoch
* annotations: NEMAR `events.tsv`, using the scorer-1 primary `trial_type` stream
* native rates: 200 Hz for both required channels
* unit behavior: explicit `uV` validation and conversion factor `1.0`
* processed successful records: `I003`, `I004`, `I005`
* `I001` and `I002` were acquired but quarantined as `SIGNAL_DURATION_MISMATCH` because their downloaded EDF body sizes were smaller than the sample count declared by their EDF headers

The pipeline does not call the NEMAR derivative byte-identical to the original ISRUC provider files.

## 12. Resampling Implementation

* method: `scipy.signal.resample_poly`
* EEG 100 -> 100 Hz: up `1`, down `1` (copy, no resampling)
* EOG 100 -> 50 Hz: up `1`, down `2`
* EEG 200 -> 100 Hz: up `1`, down `2`
* EOG 200 -> 50 Hz: up `1`, down `4`
* window/filter: explicit Kaiser window `("kaiser", 5.0)`; anti-aliasing inherent to polyphase downsampling only
* padding: explicit `padtype="constant"`
* continuous-before-epoch rule: signals are converted and resampled as continuous recordings before epoch extraction
* additional filtering: none; no band-pass, notch, smoothing, clipping, artifact removal, or normalization

## 13. Annotation Canonicalization

Exact mapping:

* `Sleep stage W`, `W`, `Wake` -> `Wake`
* `Sleep stage 1`, `Stage 1`, `N1` -> `N1`
* `Sleep stage 2`, `Stage 2`, `N2` -> `N2`
* `Sleep stage 3`, `Sleep stage 4`, `Stage 3`, `Stage 4`, `N3` -> `N3`
* `Sleep stage R`, `Stage R`, `REM` -> `REM`

Excluded annotations include movement, `Sleep stage ?`, unknown, unscored, artifact, corrupt annotation, alignment errors, incomplete epochs, and epochs without matching signal samples. Unknown labels raise an explicit failure and never map to Wake.

Sleep-EDF multi-epoch event durations are expanded only when positive and divisible into 30-second intervals within the configured tolerance. ISRUC 30-second events retain their source event index and onset provenance.

## 14. Alignment Rules

Annotation onsets are converted to target sample indices using deterministic integer rounding. An EEG epoch is `[round(t*100), round(t*100)+3000)` and an EOG epoch is `[round(t*50), round(t*50)+1500)`.

A non-integral sample onset, negative index, short signal segment, or non-30-second ambiguous event is rejected or excluded explicitly. The configured annotation timing tolerance is `0.001` seconds. Ordinary epochs are never padded or silently truncated.

## 15. Structural Failure Taxonomy

Implemented or represented stable codes:

* `MISSING_REQUIRED_EEG`
* `MISSING_REQUIRED_EOG`
* `UNEXPECTED_EEG_RATE`
* `UNEXPECTED_EOG_RATE`
* `UNKNOWN_EEG_UNIT`
* `UNKNOWN_EOG_UNIT`
* `STRUCTURAL_UNIT_MISMATCH`
* `ANNOTATION_UNKNOWN_LABEL`
* `ANNOTATION_ALIGNMENT_ERROR`
* `INCOMPLETE_EPOCH`
* `SIGNAL_DURATION_MISMATCH`
* `ANNOTATION_DURATION_MISMATCH`
* `MISSING_SIGNAL_SAMPLES`
* `CORRUPT_EDF`
* `ACQUISITION_FAILURE`

## 16. Smoke Selection Rule

Selection was deterministic and outcome-independent: choose the lexicographically first valid subject IDs with exact required files and structural schema. All nights for a selected Sleep-EDF subject remain grouped. If a candidate fails structural acquisition/schema validation, choose the next lexicographic subject; do not select based on stage composition, pathology, signal amplitude, or model behavior.

For SC, `SC_00` was represented by `SC4001E0` and `SC4002E0`; `SC_01` by `SC4011E0`; `SC4012E0` failed structural file validation; `SC_02` replacement `SC4021E0` could not be acquired because PhysioNet DNS failed. ISRUC candidates `I001` and `I002` failed EDF body-size integrity, so `I003`, `I004`, and `I005` were used by the next-subject rule.

## 17. Smoke Cohort

| dataset | subject | recording | acquisition | preprocessing | status |
|---|---|---|---|---|---|
| Sleep-EDF SC | `SC_00` | `SC4001E0` | acquired | success | SUCCESS |
| Sleep-EDF SC | `SC_00` | `SC4002E0` | acquired | success | SUCCESS |
| Sleep-EDF SC | `SC_01` | `SC4011E0` | acquired | success | SUCCESS |
| Sleep-EDF SC | `SC_02` | `SC4021E0` | PhysioNet DNS failure | not attempted | FAILED / ACQUISITION_FAILURE |
| ISRUC-S1 | `I003` | `I003` | acquired | success | SUCCESS |
| ISRUC-S1 | `I004` | `I004` | acquired | success | SUCCESS |
| ISRUC-S1 | `I005` | `I005` | acquired | success | SUCCESS |

## 18. Smoke Results

Data engineering only; no ML metrics were computed.

| dataset | recording | source epochs | valid epochs | excluded | EEG shape | EOG shape | NaN/Inf | output SHA256 |
|---|---|---:|---:|---:|---|---|---|---|
| Sleep-EDF SC | `SC4001E0` | 2880 | 2650 | 230 | `(2650,3000)` | `(2650,1500)` | `0/0` | `dcfccecdcebecc9767d82e4339753528545dfe5db2f9d23a8c4ef30aa6ccc4f7` |
| Sleep-EDF SC | `SC4002E0` | 2880 | 2829 | 51 | `(2829,3000)` | `(2829,1500)` | `0/0` | `93ad61a3b099242672e8889ac872ab75b77de1bbab130bc7b27e9cf505a8a9ba` |
| Sleep-EDF SC | `SC4011E0` | 2880 | 2802 | 78 | `(2802,3000)` | `(2802,1500)` | `0/0` | `e7ced5911b7270104e30bd27acf8f3bdae8635db42cecf6cc73eca5b13fb4828` |
| ISRUC-S1 | `I003` | 944 | 359 | 585 | `(359,3000)` | `(359,1500)` | `0/0` | `a05b7ef11e32466b1aaac252b603d3d9bf17494b6fc0ec8129ec634b216dc2b7` |
| ISRUC-S1 | `I004` | 964 | 258 | 706 | `(258,3000)` | `(258,1500)` | `0/0` | `b778ce37e73e5c2ca8bd6e3190e7ba2d44a16d40e02aa98146084f57400bb502` |
| ISRUC-S1 | `I005` | 876 | 338 | 538 | `(338,3000)` | `(338,1500)` | `0/0` | `da91aff1ed222078d5124e6be2f5efeaf45158bc5219c7f9bb579f3d5602d2e6` |

## 19. Stage/Exclusion Audit

Aggregate audit artifact: `reports/preprocessing_epoch_audit.csv`, seven rows including the failed SC replacement.

Successful-record aggregate canonical labels:

* Sleep-EDF SC: Wake 5,738; N1 226; N2 1,185; N3 622; REM 510
* ISRUC-S1: Wake 456; N1 0; N2 0; N3 0; REM 269

The ISRUC smoke labels reflect the source events selected by scorer 1 and are an engineering audit, not a scientific performance or representativeness claim. Excluded epochs are retained as explicit aggregate counts; no stage distribution was optimized.

## 20. Determinism Verification

Repeated execution from the same raw input produced identical persisted hashes:

* Sleep-EDF `SC4001E0`: `dcfccecdcebecc9767d82e4339753528545dfe5db2f9d23a8c4ef30aa6ccc4f7` on both runs
* ISRUC-S1 `I003`: `a05b7ef11e32466b1aaac252b603d3d9bf17494b6fc0ec8129ec634b216dc2b7` on both runs

Full determinism evidence is in `reports/determinism_hashes.txt`.

## 21. Physical-Unit Sanity Check

No suspicious `1e3` or `1e6` conversion discrepancy was found in the successful smoke outputs. Source headers explicitly reported microvolts for the selected EEG/EOG channels, and the conversion factor was `1.0` for both datasets. Legitimate domain amplitude differences were not normalized away or interpreted as errors.

## 22. QC Findings

* `SC4012E0` was structurally invalid by EDF body-size validation and was not processed.
* NEMAR `I001` and `I002` EDF objects were smaller than their declared EDF sample bodies and were quarantined as `SIGNAL_DURATION_MISMATCH`.
* The PhysioNet DNS outage prevented acquisition of the deterministic `SC4021E0` replacement.
* ISRUC smoke records exposed only Wake and REM among valid canonical epochs in this source subset; this was recorded, not corrected or used for selection.
* No NaN or Inf values occurred in successful persisted epochs.
* No amplitude-based epoch exclusion was applied.

## 23. Visual QC

Three deterministic SVG figures were generated under ignored `data/interim/qc_figures/`:

* `sleep_edf_sc_SC4001E0_first_epoch.svg`
* `isruc_s1_I003_first_epoch.svg`
* `stage_counts_smoke.svg`

The signal figures use the first valid persisted epoch from predeclared records `SC4001E0` and `I003`. The stage-count figure uses aggregate smoke counts. Every figure is labeled `PREPROCESSING QC — NOT EXPERIMENTAL RESULT`; no accuracy or other model metric is shown.

## 24. Provenance

`reports/acquisition_manifest.csv` records source path, official base URL, byte size, SHA256, acquisition date, dataset version, distribution, status, and failure code where applicable.

* Sleep-EDF SC: official PhysioNet Sleep-EDF Expanded v1.0.0 distribution; original-provider EDF/EDF+ files and hypnograms
* ISRUC-S1: NEMAR `nm000111` v1.0.1 BIDS derivative; source URLs are represented without signed credentials; signal files are explicitly not called byte-identical originals
* No credentials, signed URLs, cookies, tokens, or secrets were retained
* Raw EDF/TSV/JSON files remain under ignored `data/raw/`

## 25. Leakage Protections

Confirmed:

* no target-derived normalization
* no subject splitting; subject identity remains available for grouping
* no outcome-based smoke selection
* no scorer cherry-picking; scorer 1 is predeclared primary and scorer 2 disagreement does not delete primary epochs
* no label-derived Wake trimming
* no final train/dev/test split
* no target calibration or model-selection operation

## 26. Tests Added

`tests/test_preprocessing.py` adds coverage for:

* canonical labels and unknown-label rejection
* R&K stage 3/4 to N3 mapping
* unit conversion and unknown-unit quarantine
* continuous 200->100, 200->50, and 100->50 resampling
* forbidden upsampling
* exact 3000/1500 sample extraction
* duration expansion and ambiguous-duration rejection
* scorer-2 non-interference with scorer-1 labels
* required-channel contract literals and missing-channel failure code
* output schema, label range, finite-value checks
* deterministic resampling
* atomic NPZ implementation presence
* target-free contract state
* raw-path ignore behavior

Existing contract tests were retained.

## 27. Validation Results

Actual final validation results before report/commit finalization:

* `pytest -q`: `32 passed in 2.26s`
* `python -m compileall -q src tests scripts`: passed with exit code 0
* `git diff --check`: passed
* config validation: contract version `1.1.0`, status `CORE_PREPROCESSING_FROZEN`, final benchmark `false`; preprocessing version `0.1.0`, referenced contract `1.1.0`
* manifest validation: six successful NPZ rows plus one explicit failed deterministic replacement; all successful rows passed shape, label, finite-value, and output-hash checks
* repeated determinism validation: SC and ISRUC hashes identical across repeated runs
* forbidden artifact scan: no credential-like artifacts found outside ignored raw/generated data
* raw ignore validation: `git check-ignore` confirmed raw EDF, processed NPZ, and interim QC figure paths are ignored

## 28. Machine-Readable Artifacts

* `reports/acquisition_manifest.csv`: 53 file-level provenance rows; columns include dataset, path, source URL, bytes, SHA256, acquisition date, dataset version, distribution, status, and failure code
* `reports/preprocessing_smoke_manifest.csv`: 7 recording-level rows; columns include dataset, cohort, subject, source/annotation paths and hashes, channels, rates, units, epoch counts, output path/hash, status, and failure code
* `reports/preprocessing_epoch_audit.csv`: aggregate per-successful-record stage/exclusion counts (6 rows)
* `reports/contract_hashes.txt`: frozen data-contract hashes from Step 5.1
* `reports/preprocessing_hashes.txt`: data-contract and preprocessing-config hashes
* `reports/determinism_hashes.txt`: repeated-run output hashes

## 29. Files Created

* `configs/preprocessing_v1.yaml`
* `reports/acquisition_manifest.csv` (updated for Step 6 acquisition)
* `reports/preprocessing_smoke_manifest.csv`
* `reports/preprocessing_epoch_audit.csv`
* `reports/preprocessing_hashes.txt`
* `reports/determinism_hashes.txt`
* `src/shiftsleep_uq/data/preprocess.py`
* `src/shiftsleep_uq/data/preprocessing.py`
* `src/shiftsleep_uq/data/adapters/__init__.py`
* `src/shiftsleep_uq/data/adapters/base.py`
* `src/shiftsleep_uq/data/adapters/sleep_edf.py`
* `src/shiftsleep_uq/data/adapters/isruc.py`
* `tests/test_preprocessing.py`
* `reports/STEP_06_PREPROCESSING_PIPELINE_REPORT.md`

## 30. Files Modified

* `pyproject.toml` — declared minimal preprocessing runtime dependencies

No frozen contract or scientific protocol file was modified. Raw signal files, processed NPZ files, and QC figures are ignored and are not commit candidates.

## 31. Explicitly Not Done

Confirmed:

* no model
* no training
* no final scientific results
* no normalization
* no bandpass filter
* no notch filter
* no artifact removal
* no final dataset splits
* no target calibration
* no SHHS bypass/download without access
* no full-core preprocessing
* no raw data committed
* no processed arrays committed
* no repository push

## 32. Pipeline Gate Decision

PIPELINE_PARTIAL

The core implementation is deterministic, contract-driven, provenance-preserving, subject-aware, architecture-independent, and validated on successful SC and ISRUC-S1 records. Both datasets have valid persisted representations, exact canonical shapes, explicit units, finite outputs, exact labels, deterministic repeated hashes, and passing tests. The gate remains partial because the frozen subject-level SC smoke rule required a third subject and the deterministic `SC4021E0` replacement could not be acquired during the final PhysioNet DNS outage. That failure is visible in the manifest and was not hidden by an outcome-based replacement.

## 33. Remaining Problems

### CORE PIPELINE BLOCKERS

* Complete the subject-level SC smoke cohort by acquiring and validating the deterministic `SC4021E0` replacement (or the next lexicographic structurally valid subject under the same rule) when the official PhysioNet endpoint is available.
* Re-run the full smoke manifest and repeated determinism check after the third SC subject is successfully acquired.

### FINAL BENCHMARK BLOCKERS

* SHHS1 authorized raw/XML access is still pending.
* SHHS1 exact channel/rate/unit and per-record annotation validation are not complete.
* The final three-domain benchmark remains `final_benchmark_frozen: false`.

## 34. Recommended Step 7

Not executed.

Because the pipeline gate is `PIPELINE_PARTIAL`, exactly one repair step is recommended before Step 7: acquire and validate the deterministic third SC subject replacement, then rerun the Step 6 smoke gate and update this report. No full-core processing or model training should begin from this report until that repair is independently reviewed.

## 35. Git Status / Diff Summary

The Step 6 implementation commit is `0737d527967b482e69daf3c5abbdb6838f2880d7`; this report is finalized in the subsequent local commit shown by final HEAD verification. Raw and processed data remain ignored and uncommitted. Push status is `NOT PUSHED`.

The final verification must confirm that only preprocessing code, configuration, tests, safe manifests/reports, and documentation are committed, with no EDF, TSV signal source, NPZ, archive, credential, or restricted file staged.
