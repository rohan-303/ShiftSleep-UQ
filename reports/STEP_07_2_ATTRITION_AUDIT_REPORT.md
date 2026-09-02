# ShiftSleep-UQ Step 7.2 Attrition Audit Report

## 1. Status

BLOCKED

## 2. Previous Cohort State

Step 7.1 reported `CORE_DATA_FROZEN`: Sleep-EDF SC 48/153 recordings and 33/78 subjects; ISRUC-S1 15/100 recordings and 15/100 subjects. Its v1 manifests/config/hashes are preserved as historical provenance.

## 3. Freeze Reassessment

CORE_DATA_BLOCKED

## 4. Repository State

Preflight verified repository `C:\Users\rohan\ShiftSleep-UQ`, branch `main`, Step 7.1 commit `dd35375938fd3bb1f83115c5fb0557091067a2f9`, Step 7.1 report, v1 manifests, provider audit, frozen contract/configs, and a clean pre-Step-7.2 state. Data-contract SHA-256: `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9`; preprocessing-config SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`.

## 5. Retention Verification

| Dataset | Expected subjects | Included subjects | Subject retention | Expected recordings | Included recordings | Recording retention | Partial subjects | Excluded subjects | Excluded recordings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sleep-EDF SC, Step 7.1 | 78 | 33 | 42.31% | 153 | 48 | 31.37% | 15 | 45 | 105 |
| Sleep-EDF SC, v1.1 candidate | 78 | 78 | 100.00% | 153 | 153 | 100.00% | 0 | 0 | 0 |
| ISRUC-S1, Step 7.1 and v1.1 candidate | 100 | 15 | 15.00% | 100 | 15 | 15.00% | 0 | 85 | 85 |

The Step 7.1 report and v1 manifests agree numerically. The corrected v1.1 values are independently derived from `core_recording_manifest_v1_1.csv`.

## 6. Failure-Code Distribution

`reports/core_attrition_failure_distribution.csv` contains every terminal exclusion in the rebuilt candidate:

| Dataset | Failure code | Recordings | Subjects affected | % expected recordings | % all exclusions |
|---|---|---:|---:|---:|---:|
| ISRUC-S1 | `MISSING_REQUIRED_EEG` | 83 | 83 | 83.00% | 97.65% |
| ISRUC-S1 | `EDF_DECLARED_BYTE_MISMATCH` | 2 | 2 | 2.00% | 2.35% |

There are no rebuilt Sleep-EDF terminal exclusions. No reasons were combined into `other`.

## 7. First-Failure-Stage Distribution

`reports/core_attrition_stage_distribution.csv` assigns exactly one first failure to all 85 exclusions: required-channel lookup = 83; provider-byte integrity = 2.

## 8. Sleep-EDF Root-Cause Audit

The original 105/153 exclusions were pipeline false positives, not failed acquisition: all 153 PSG objects were acquired and checksum-valid. The matcher accepted only `C/H` annotation endings and incorrectly marked official variants as unavailable. Actual official pairs use source-specific final suffixes across E/F/G PSG series. The repaired matcher finds one exact local official hypnogram by the shared PSG prefix and accepts it only when unique. Full 153-record rerun: 153 included.

## 9. Sleep-EDF Pairing Audit

`reports/sleep_edf_pairing_audit.csv`: 153 expected PSGs; 153 exact successful pairs; 0 ambiguous pairs; 0 unpaired PSGs; 0 orphan hypnograms. Examples of previously missed valid forms include `SC4261F0-PSG` -> `SC4261FC-Hypnogram` and E-series suffixes such as J/P/U/V/W/Y. No heuristic rematching was used.

## 10. Sleep-EDF Alignment Audit

Sleep-EDF hypnograms can span 86,400 s while PSG bodies end earlier. A record is not invalid merely because trailing annotation time is unknown or outside PSG duration. `SC4362F0` showed a real pipeline false positive: PSG duration 67,980 s, annotation span 86,400 s, and 504 canonical epochs beyond available signal. The repair retains the signal-backed prefix and records those 504 epochs as `missing_signal_samples`; its rebuilt accounting is 2,880 = 2,266 valid + 614 excluded (110 unknown + 504 unsupported). No Wake trimming occurred.

## 11. Sleep-EDF Manual Failure Review

The two former major categories were inspected programmatically at raw-file level:

| Category | Raw evidence | Validator expectation/result | Classification |
|---|---|---|---|
| `ACQUISITION_FAILURE` (105 pre-fix) | Unique official PSG/hypnogram file pair exists and provider checksum passes | Prior fixed C/H suffix lookup returned absent; exact local pairing passes | PIPELINE_FALSE_POSITIVE |
| `MISSING_SIGNAL_SAMPLES` (`SC4362F0`) | Valid staging continues after physical PSG end | Prior extractor attempted unsupported epochs and failed record; rebuilt accounting excludes only unsupported epochs | PIPELINE_FALSE_POSITIVE |

Full-category inspection, not selective repair, was performed through the all-153 reruns and `sleep_edf_attrition_audit.csv`.

## 12. ISRUC Root-Cause Audit

All 100 expected subjects are present in `reports/isruc_attrition_audit.csv`. Of 98 provider-body-valid EDFs, only 15 expose exact frozen `C3-A2` and `LOC-A2`; 83 fail before annotation/preprocessing at required-channel lookup. The remaining two objects are explicit integrity exclusions.

## 13. ISRUC Provider Integrity

`reports/isruc_provider_integrity_distribution.csv`: `PROVIDER_BODY_VALID` 98/100 (98%); `PROVIDER_BODY_TRUNCATED` 2/100 (2%); unavailable/other-invalid 0. I001 body = 91,778,304 bytes vs EDF-declared 143,885,120 (delta -52,106,816); I002 body = 58,458,112 vs EDF-declared 157,619,120 (delta -99,161,008). Each matches NEMAR metadata size/SHA-256 but fails the EDF declared-body invariant and remains excluded.

## 14. ISRUC Download-Mechanism Finding

NEMAR metadata identifies content-addressed immutable S3 objects, exposed through its official bytes endpoint; NEMAR documents DataLad/git-annex metadata with immutable S3 data blobs and selective `datalad get` access. Local provider bytes, NEMAR manifest size, and SHA-256 agree for I001/I002. Thus these are not ordinary HTTP partial-response/download-resume failures; the published provider objects themselves are inconsistent with their EDF headers. No unofficial mirror or bypass was used.

## 15. ISRUC Channel/Rate/Unit Audit

Exact channels: `C3-A2` present 15/100; `LOC-A2` present 15/100; both 15/100. Across all 98 provider-valid diagnostic channel pairs, native rates are 200 Hz EEG and 200 Hz EOG with uV/uV units. Excluded records commonly expose `C3-M2` with `E1-M2`/`E2-M1`, or separated electrode labels (for example I040). These are source/BIDS schema variants, not case/whitespace parser mistakes. No fallback channel was introduced.

## 16. ISRUC Annotation Audit

`isruc_attrition_audit.csv` records event count, staging-event count, raw vocabulary, duration vocabulary, primary `trial_type` field, and scorer-2 field presence for every subject. Raw primary labels are within the documented `Sleep stage W/N1/N2/N3/R/U` vocabulary where present. Scorer-2 columns are heterogeneous (present for 42, absent for 58); this does not affect the earlier required-channel exclusion and scorer-1 remains the only primary gold source.

## 17. ISRUC Viability Decision

UNUSABLE as the current primary cross-domain core dataset. The retained 15/100 subjects are not a minor/random provider loss: 83% fail a systematic source-schema mismatch, and 2% are provider-body-invalid.

## 18. Overall Root Causes

- **Sleep-EDF SC: PIPELINE_BUG (100% of the pre-fix 105 recording exclusions).** 104 were invalid pairing-path exclusions; one was signal-boundary epoch-extraction behavior. Both are repaired without scientific-contract change.
- **ISRUC-S1: MIXED.** 83% of expected recordings are `SOURCE_HETEROGENEITY`/frozen-contract mismatch at exact channel lookup; 2% are `PROVIDER_FAILURE` (EDF-body truncation); 15% meet the current exact contract.

## 19. Pre-Fix Snapshot

`reports/core_attrition_pre_fix_snapshot.csv`, SHA-256 `9f6510d8ed8b43088a31fcf598d321f5bdc0e8f378d2f9596b3cf33c4fb50a6a`, freezes the Step 7.1 48/153 and 15/100 state before repair.

## 20. Repairs Performed

1. Source-supported unique Sleep-EDF PSG/hypnogram pairing across official suffix variants.
2. Schema-audit lookup corrected to resolve Sleep-EDF paths from `recording_id`, preserving expected `subject_id` in audit rows.
3. Signal-boundary handling excludes only canonical epochs beyond physical PSG data and retains accounting.

## 21. Scientific Contract Changes

NONE. Required EEG/EOG channels, rates, units, labels, scorer policy, and no-normalization policy remain unchanged.

## 22. Post-Repair Sleep-EDF Population

153/153 recordings and 78/78 subjects; all structurally included.

## 23. Post-Repair ISRUC Population

15/100 recordings and 15/100 subjects; unchanged after diagnosis because no justified non-contract repair exists.

## 24. Before-vs-After Retention

Sleep-EDF increased from 48/153 (31.37%) to 153/153 (100.00%) through verified pipeline repairs. ISRUC stayed 15/100 (15.00%).

## 25. Structural Exclusions

Rebuilt candidate structural exclusions total 85, all ISRUC: 83 `MISSING_REQUIRED_EEG`, 2 `EDF_DECLARED_BYTE_MISMATCH`.

## 26. Subject-Level Population

Rebuilt candidate manifests contain 178 expected source subjects: 78 Sleep-EDF (all complete) and 100 ISRUC (15 complete; 85 excluded).

## 27. Epoch Accounting

All 168 included records have `accounting_delta = 0`; for every included record, valid equals Wake + N1 + N2 + N3 + REM. `SC4362F0` independently demonstrates the repaired boundary accounting.

## 28. Representativeness / Selection Risk

Sleep-EDF repaired failures were filename-suffix and signal-boundary implementation effects, not subject/source selection. ISRUC failures cluster strongly after I010 and by montage/reference schema (`C3-M2`/E1-M2 or separated labels), creating severe systematic selection risk. Provider size/body corruption affects only I001/I002; file-size corruption is not the dominant mechanism.

## 29. Split Feasibility

Sleep-EDF alone can support future subject-level protocol design. The current 15-subject ISRUC subset cannot credibly support independent train/dev/source-calibration/test roles, stable multi-seed comparisons, subject-level confidence intervals, or a representative cross-domain evaluation. No partitions were generated.

## 30. Determinism

`reports/full_core_determinism_audit.csv` reran the first three lexicographic included records per dataset. All six output hashes matched.

## 31. Cohort Versioning

Old cohort: `core_cohort_v1.yaml`, status **SUPERSEDED** for the Step 7.1 false-positive implementation defects; historical copies/hashes are retained (`*_v1_step_07_1`).

New candidate: `configs/core_cohort_v1_1.yaml`, status **UNDER_REVIEW**, gate `CORE_DATA_BLOCKED`, SHA-256 `b9938fceafe843d5e95bfa3f81a845bf43c8fe28263e5ab66f9ea4e59701b243`. Candidate recording-manifest SHA-256: `417286a0b5562c80693c4c410f64b3dcf773c8328568f5123deecca34c92a806`; subject-manifest SHA-256: `2a80d240fd4967df970785a1030f9c6f80e7cc5a171707961cc28dc4603f5817`.

## 32. Updated Core Data Gate

CORE_DATA_BLOCKED. Internal terminal accounting is complete, and Sleep-EDF is credible, but the two-domain core cannot be frozen while ISRUC retention is 15% through systematic contract/source incompatibility.

## 33. Final Benchmark Gate

NO. SHHS remains separate; no SHHS raw/XML authorization, processing, or bypass occurred.

## 34. Tests Added

- Official non-C/H Sleep-EDF pairing variant resolution.
- Signal-boundary exclusion retains supported epochs and counts unsupported canonical epochs.

## 35. Full Validation

Rebuilt expected population and v1.1 manifest identities reconcile 253/253 with one terminal state each. Provider audit covers 253 identities. All 168 included accounting rows have zero delta. Output integrity and six deterministic hashes pass. Compilation, test suite, diff check, ignored-artifact, and credential scans are run after report generation before local commit.

## 36. Files Created

`core_attrition_pre_fix_snapshot.csv`, failure/stage distributions, Sleep-EDF pairing/attrition audits, ISRUC attrition/provider/rate-unit audits, manual-failure review, v1.1 manifests, `core_cohort_hashes_v1_1.txt`, historical v1 copies, `core_cohort_v1_1.yaml`, `step_07_2_attrition_audit.py`, and this report.

## 37. Files Modified

`src/shiftsleep_uq/data/preprocess.py`; `scripts/step_07_1_process_and_audit.py`; `tests/test_preprocessing.py`; regenerated generic full-core audit tables; Step 7.2 audit generator.

## 38. Explicitly Not Done

- no model
- no training
- no normalization
- no split generation
- no calibration partition
- no ML metrics
- no SHHS bypass
- no raw/processed signals committed
- no push

## 39. Remaining Core Issues

ISRUC original-provider comparison is not yet performed. The official ISRUC site exposes a public 14.12 GB Cohort I MEGA archive with 100 PSGs and two-expert annotations but no documented per-file route on the inspected page. A provider migration requires a separately authorized, provenance-validated feasibility step.

## 40. Remaining Final-Benchmark Issues

SHHS1 raw/XML access and per-record validation are absent; final-benchmark protocol remains unfrozen.

## 41. Recommended Next Step

Perform exactly one data repair: **acquire and provenance-validate a small, authorized original ISRUC Cohort I comparison set before any provider migration or scientific contract decision.** Do not execute it in this step.

## 42. Git Status / Diff Summary

This step is locally committed after validation as `research: audit accessible-core attrition`; no remote push is performed. The diff contains source-supported pairing/boundary repair, regression tests, regenerated safe reports/manifests, and Step 7.2 evidence only.
