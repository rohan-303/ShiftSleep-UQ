# ShiftSleep-UQ Step 7.8 ISRUC Rebuild and Accessible-Core Freeze Report

## 1. Status

PARTIAL

The original-provider rebuild was executed for every locally available official-provider bundle. I001-I036 are complete, body-valid, contract-valid, and rebuilt. I037-I100 remain unacquired because the approved account-free MEGA acquisition route is currently blocked/unavailable in this environment. No scientific freeze was claimed from incomplete acquisition.

## 2. ISRUC Original Cohort Gate

ISRUC_ORIGINAL_COHORT_PARTIAL

The authoritative expected population remains exactly I001-I100. The v2 artifacts contain 100 terminal subject rows, with 36 complete/included and 64 explicit acquisition exclusions.

## 3. Accessible-Core Gate

CORE_DATA_PARTIAL

Sleep-EDF SC was independently revalidated from its existing repaired artifacts, but the accessible two-domain core cannot be frozen while original-provider ISRUC acquisition remains incomplete.

## 4. Final Benchmark Gate

NO

SHHS raw/XML access was not requested or used. Accessible-core work is not a final three-domain benchmark freeze.

## 5. Repository State

Repository: `C:\Users\rohan\ShiftSleep-UQ`.

Branch: `main`.

The preflight HEAD was `4ecdfe2`, the Step 7.7 commit (`research: harmonize ISRUC source montage variants`). The Step 7.7 report and commit were present. No GitHub push was performed. Raw `.rec`, raw annotation files, transfer artifacts, and processed arrays remain ignored and untracked.

Storage preflight recorded 179,263,078,400 free bytes on C:. Current original-provider raw bytes were 5,400,940,535 bytes. Current v2 processed ISRUC bytes were 548,244,513 bytes after cleanup of temporary determinism outputs. No separate transfer directory was present. The observed complete-bundle mean was 149,935,857 bytes; the 64-subject remaining estimate was approximately 9,595,894,866 bytes, leaving approximately 169,667,183,534 bytes before other workspace overhead. Storage was not the blocker.

The current contract and preprocessing hashes were verified before execution. I036 was present as a complete five-file bundle when independently revalidated, despite the earlier quota-interrupted transfer log.

## 6. Frozen Scientific Contracts

Data contract: `1.2.0`.

Data-contract SHA-256: `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`.

Preprocessing: `0.1.0`.

Preprocessing-config SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`.

The two exact ISRUC pairings were not changed:

- `C3-A2` + `LOC-A2` -> `ISRUC_A1A2`.
- `C3-M2` + `E1-M2` -> `ISRUC_M1M2`.

No fallback, alias, case normalization, re-referencing, or source-derivation renaming was introduced.

## 7. Acquisition Resume

I036 outcome: COMPLETE after the existing partial state was inspected. The final local bundle contains `36.rec`, `36_1.txt`, `36_1.xlsx`, `36_2.txt`, and `36_2.xlsx`. Independent EDF body validation produced body delta `0`; the subject was processed as `ISRUC_M1M2` and included.

The historical acquisition log records the approved MEGAcmd route reaching the I036 transfer and then returning the documented bandwidth-quota boundary. No quota bypass, private account login, unofficial mirror, signed URL, or credential was used.

## 8. Remaining Acquisition

I037-I100 outcome: NOT ACQUIRED.

No approved MEGA client executable was available in the current environment, and the prior account-free route was documented as bandwidth-quota blocked. No unofficial route or quota bypass was attempted. The 64 missing subjects remain in the expected population and in the v2 acquisition/recording/subject manifests with explicit terminal acquisition failure status.

## 9. Full Acquisition Summary

| Metric | Result |
|---|---:|
| Expected subjects | 100 |
| Complete bundles | 36 |
| Partial bundles | 0 |
| Failed/unacquired bundles | 64 |
| Current original-provider raw bytes | 5,400,940,535 |
| Acquisition manifest rows | 500 |

The 500-row acquisition manifest has five expected file-role rows for every expected subject. Existing files have bytes and SHA-256 values; missing roles have empty byte/hash fields and explicit terminal reasons.

## 10. Provider Integrity

| Integrity class | Subjects |
|---|---:|
| Body-valid original REC | 36 |
| Body-invalid REC | 0 |
| Unacquired signal/bundle | 64 |
| Other provider failures | 0 |

Every completed REC passed the independent EDF header/body-size audit with `body_delta = 0`. No completed body was weakened or accepted on approximate size.

## 11. Full Raw Montage Inventory

Among the 36 body-valid completed original-provider recordings:

- `ISRUC_A1A2`: 17 included subjects.
- `ISRUC_M1M2`: 19 included subjects.
- Unsupported completed montage: 0.
- Other completed schema failure: 0.
- Unacquired and therefore not schema-classifiable: 64.

## 12. Montage Contract Validation

All 36 completed recordings resolved through the authoritative exact resolver. No second hand-written acceptance list is used by the rebuilt processing path. The observed source derivations were exactly `C3-A2`/`LOC-A2` or `C3-M2`/`E1-M2`. The full schema/unit/rate audit reports only these two derivation families; no third supported or unsupported completed family appeared.

## 13. Original Adapter Integration

`src/shiftsleep_uq/data/montage_contract.py` now exposes the exact source-pair contract and channel-index resolver. The original-provider orchestration imports `resolve_isruc_channels()` and obtains EEG/EOG indices, exact derivation strings, anatomical roles, and `montage_variant` from that resolver. The preprocessing code does not rename, re-reference, or substitute source signals.

The output metadata retain:

- `source_eeg_derivation`;
- `source_eog_derivation`;
- `eeg_anatomical_role = LEFT_CENTRAL_EEG`;
- `eog_anatomical_role = LEFT_OCULAR_EOG`;
- `montage_variant`;
- scorer-1 source identity;
- contract `1.2.0` and preprocessing `0.1.0`.

## 14. Adapter Regression

A1/A2 panel: I001 and I003 resolved to `C3-A2` + `LOC-A2`, `ISRUC_A1A2`, native EEG/EOG rates 200 Hz, units `uV`, and target shapes `(n, 3000)` and `(n, 1500)`.

M1/M2 panel: I011 and I013, the first two numerically valid M1/M2 subjects, resolved to `C3-M2` + `E1-M2`, `ISRUC_M1M2`, native rates 200 Hz, units `uV`, and the same target shapes.

I003 historical regression: the new and historical original-provider outputs had identical EEG, EOG, label, epoch-onset, and source-epoch-index arrays. The full NPZ hash changed only because the new contract-1.2.0 provenance metadata were added.

## 15. Full Preprocessing Results

| Metric | Result |
|---|---:|
| Expected subjects | 100 |
| Included/rebuilt subjects | 36 |
| Acquisition-excluded subjects | 64 |
| Structural exclusions among completed bundles | 0 |
| EEG target | 100 Hz, 3000 samples/epoch |
| EOG target | 50 Hz, 1500 samples/epoch |
| Output dtype | float32 |
| Unit | canonical microvolt |
| Normalization | none |

All completed subjects were processed from original-provider inputs, not NEMAR signals.

## 16. Structural Exclusions

No completed original-provider bundle incurred a structural preprocessing exclusion. The 64 non-included subjects are acquisition failures, not stage-, channel-performance-, or model-based exclusions. Their terminal code in the v2 artifacts is `ACQUISITION_FAILURE`; the acquisition manifest records the more specific route/quota reason for missing file roles.

## 17. Montage Distribution

| Montage | Subjects | Valid epochs |
|---|---:|---:|
| `ISRUC_A1A2` | 17 | 15,429 |
| `ISRUC_M1M2` | 19 | 17,328 |
| Total | 36 | 32,757 |

These are descriptive source-stratum counts only. No stage distribution or model result was used for inclusion.

## 18. Annotation Audit

Thirty-six scorer-1 source files were present and parsed successfully with the frozen original ISRUC numeric vocabulary and 30-second interpretation. Scorer-1 remained primary. Scorer-2 files were retained as diagnostic provenance in every complete bundle. Sixty-four subjects had no acquired scorer files because the corresponding bundles were not acquired. No fuzzy label interpretation or unknown-code-to-Wake mapping was added.

## 19. Epoch Accounting

For every included recording:

`valid = Wake + N1 + N2 + N3 + REM`

and `accounting_delta = 0`.

Aggregate source staging epochs: 32,757. Aggregate valid canonical epochs: 32,757. Aggregate excluded staging epochs: 0. All 36 per-record accounting rows passed. The aggregate canonical stage counts were Wake 9,369; N1 4,213; N2 9,176; N3 5,569; REM 4,430.

## 20. Stage Distribution

Descriptive only. The stage totals above were generated after fixed structural inclusion and frozen annotation mapping. No stage-balance threshold, stage-based subject selection, or montage-specific stage optimization was performed.

## 21. Montage QC

Non-normalized recording-level QC is in `reports/isruc_montage_qc_v2.csv` with 72 rows (36 recordings x 2 signals). Median recording-level summaries were:

| Montage | Signal | Median of recording medians (uV) | Median MAD (uV) | Median IQR (uV) | Median valid epochs |
|---|---|---:|---:|---:|---:|
| ISRUC_A1A2 | EEG | 0.001103 | 0.750116 | 1.500241 | 897 |
| ISRUC_A1A2 | EOG | 0.006147 | 0.815705 | 1.631518 | 897 |
| ISRUC_M1M2 | EEG | 0.090172 | 9.759859 | 19.519555 | 906 |
| ISRUC_M1M2 | EOG | 0.075813 | 10.137004 | 20.278383 | 906 |

These values are descriptive only. No normalization, family alignment, or eligibility threshold was fitted.

## 22. Unit / Rate Audit

All 36 included recordings had native EEG and EOG rates of 200 Hz and `uV` physical units for the selected exact source channels. All output targets were EEG 100 Hz and EOG 50 Hz. The audit found no new rate/unit family.

## 23. Duration / Alignment Audit

All 36 included records passed signal-duration support and epoch alignment. No Wake trimming occurred. No incomplete canonical epoch was fabricated. The v2 duration/alignment manifest records zero alignment delta for every included record. The rebuild produced 32,757 valid 30-second epochs.

## 24. Duplicate Audit

`reports/isruc_duplicate_audit_v2.csv` checks raw REC SHA-256 and processed-output SHA-256. No cross-subject exact duplicate raw REC or processed output was detected. Similar file size was not treated as duplication.

## 25. Determinism Audit

All 36 included subjects were reprocessed into a deterministic comparison output. Every full-output hash comparison passed. The required first-three-per-montage panel was therefore covered: the first three `ISRUC_A1A2` subjects and first three `ISRUC_M1M2` subjects all passed.

## 26. ISRUC Viability

VIABLE_WITH_EXCLUSIONS

This is a provisional viability assessment for the acquired original-provider subset, not a cohort-freeze decision. The completed subjects have valid bodies, supported exact montage coverage, valid rates/units, scorer-1 annotations, zero accounting deltas, and deterministic outputs. The overall 100-subject ISRUC gate remains partial because 64 subjects are unacquired; therefore this viability label does not authorize the accessible-core freeze.

## 27. NEMAR vs Original Final Migration Outcome

The old NEMAR-derived cohort had 100 expected subjects and 15 included subjects, with an 85.00% exclusion rate and two provider-truncation exclusions in its historical provider-integrity record.

The original-provider contract-1.2.0 outcome currently has 100 expected subjects, 36 complete acquired bundles, 36 included subjects, 17 A1/A2 subjects, 19 M1/M2 subjects, zero completed structural exclusions, and 64 acquisition exclusions. The v2 migration outcome is recorded in `reports/isruc_provider_migration_final_outcome.csv`.

## 28. Subjects Recovered

Compared with the historical NEMAR included count of 15, the currently rebuilt original-provider subset contains 36 included subjects: 21 additional subjects are recovered relative to that historical count. This is a retention/provenance result, not a model result. It must not be interpreted as a completed 100-subject migration.

## 29. Remaining ISRUC Exclusions

I037-I100 remain excluded solely because their official original-provider bundles were not acquired. They remain expected subjects, not removed from the population. No subject was excluded for stage composition, amplitude, model performance, or montage-family preference.

## 30. Old ISRUC Cohort Status

The historical NEMAR cohort and the original-provider v1 partial cohort remain preserved. They are not deleted and are not falsely represented as the active frozen ISRUC cohort. They remain `SUPERSEDED_PENDING_SUCCESSFUL_ORIGINAL_REBUILD` / historical partial provenance until the full original-provider migration is complete.

## 31. New ISRUC Cohort Version

Config: `configs/isruc_original_cohort_v2.yaml`.

Version: `2.0.0`, cohort ID `isruc_original_v2`.

Config status: `PARTIAL_ACQUISITION`.

Gate: `ISRUC_ORIGINAL_COHORT_PARTIAL`.

The config records contract 1.2.0, preprocessing 0.1.0, the exact pairings, manifest paths, and safe manifest hash file. It does not claim `ACTIVE / FROZEN`.

## 32. Recording Manifest

File: `reports/isruc_original_recording_manifest_v2.csv`.

Rows: 100.

SHA-256: `fc3d03b00a05036edb0ed2128cd3f6e5894f14d995cc70b48bc56d84a694e2a5`.

## 33. Subject Manifest

File: `reports/isruc_original_subject_manifest_v2.csv`.

Rows: 100.

SHA-256: `ef9446a2e77bb1b4dcd3d378b44ea28bd9bd60e21426c8501798fa65de2d64c9`.

## 34. Sleep-EDF Revalidation

Authoritative current Sleep-EDF repaired artifacts were checked rather than blindly inherited. The v1.1 recording manifest contains 153 included Sleep-EDF SC recordings from 78 subjects. All 153 referenced processed outputs existed, matched their recorded SHA-256 values, had EEG shape `(n, 3000)`, EOG shape `(n, 1500)`, aligned label counts, and finite signal values. The validated epoch total is 414,961.

Historical Sleep-EDF freeze state: `CORE_DATA_FROZEN` under the previous core artifact/version. The old Sleep-EDF artifacts remain historical and were not re-downloaded or reprocessed because the ISRUC montage amendment does not alter Sleep-EDF signal processing. The overall new accessible-core gate remains partial because ISRUC is not frozen.

## 35. Accessible-Core Population

Sleep-EDF:

- subjects: 78;
- recordings: 153;
- valid epochs: 414,961;
- current revalidation: PASS for referenced hashes, shapes, alignment, and finite values.

ISRUC original provider:

- expected subjects: 100;
- included subjects: 36;
- included recordings: 36;
- valid epochs: 32,757;
- `ISRUC_A1A2`: 17 subjects / 15,429 epochs;
- `ISRUC_M1M2`: 19 subjects / 17,328 epochs;
- cohort gate: `ISRUC_ORIGINAL_COHORT_PARTIAL`.

## 36. Accessible-Core Config

No new accessible-core v2 config was created because the required two-domain freeze condition was not met. Historical `configs/core_cohort_v1_1.yaml` remains preserved and is not promoted to a new contract-1.2.0 frozen core. No new core hash was claimed.

## 37. Split Feasibility

No assignments were made. The currently accessible counts appear potentially sufficient for later subject-level train/dev/calibration and cross-dataset feasibility analysis, but ISRUC montage-stratum balance and the final 100-subject acquisition outcome must be reassessed before Step 8. This is an assessment only; no seeds, folds, calibration partitions, or split fields were generated.

## 38. Leakage / Target-Free Protections

Confirmed:

- no model;
- no outcome-based inclusion;
- no stage-based montage selection;
- no normalization fitting;
- no target fitting;
- no split generation;
- no model-performance decision;
- no SHHS access.

## 39. Tests Added

- Exact adapter channel-index resolution for A1/A2 and M1/M2 pairings.
- Mixed-pair rejection.
- Contract/provenance metadata persistence in v2 outputs.
- M1/M2 target shapes and scorer-1 metadata.
- 100-row subject manifest invariant.
- Accounting delta invariant.
- Full deterministic output hashes for the rebuilt acquired subset.

All previous tests were retained.

## 40. Full Validation

Actual command results:

- `pytest -q` -> **64 passed in 6.17s**.
- `python -m compileall -q src tests scripts` -> passed.
- `git diff --check` -> passed.

Additional checks passed:

- expected population exactly 100;
- acquisition manifest exactly 500 rows;
- recording manifest exactly 100 rows;
- subject manifest exactly 100 rows;
- body delta zero for all 36 completed RECs;
- exact montage contract for all 36 included recordings;
- 36 scorer-1 source files parsed successfully;
- 36 accounting rows passed with delta zero;
- no duplicate raw or processed hashes;
- 36 deterministic rebuild comparisons passed;
- Sleep-EDF 153/153 referenced output hash/shape/finite checks passed;
- no raw or processed artifacts tracked by Git;
- no credentials, signed/private provider URLs, or MEGA session material added;
- no GitHub push.

## 41. Files Created

- `configs/isruc_original_cohort_v2.yaml`
- `scripts/step_07_8_isruc_rebuild.py`
- `reports/isruc_original_acquisition_manifest_v2.csv`
- `reports/isruc_original_recording_manifest_v2.csv`
- `reports/isruc_original_subject_manifest_v2.csv`
- `reports/isruc_original_cohort_v2_hashes.txt`
- `reports/isruc_original_annotation_audit_v2.csv`
- `reports/isruc_original_epoch_accounting_v2.csv`
- `reports/isruc_original_duration_alignment_v2.csv`
- `reports/isruc_full_schema_unit_rate_audit_v2.csv`
- `reports/isruc_montage_distribution_v2.csv`
- `reports/isruc_montage_qc_v2.csv`
- `reports/isruc_duplicate_audit_v2.csv`
- `reports/isruc_determinism_audit_v2.csv`
- `reports/isruc_provider_migration_final_outcome.csv`
- `tests/test_isruc_step78_artifacts.py`
- `reports/STEP_07_8_ISRUC_REBUILD_AND_CORE_FREEZE_REPORT.md`

## 42. Files Modified

- `src/shiftsleep_uq/data/montage_contract.py` — added the exact contract-driven channel-index resolver.
- `scripts/step_07_5_original_migration.py` — original-provider preprocessing now uses the authoritative resolver and persists contract-1.2.0 montage metadata.
- `docs/isruc_original_migration_plan.md` — updated exact pair requirements and recorded Step 7.8 partial state.
- `docs/isruc_provider_migration_record.md` — appended the verified Step 7.8 migration outcome.

No raw files, provider files, processed arrays, credentials, or transfer artifacts were modified for Git inclusion.

## 43. Explicitly Not Done

Confirmed:

- no splits;
- no model;
- no training;
- no normalization;
- no ML metrics;
- no calibration;
- no conformal work;
- no SHHS bypass;
- no raw/processed data committed;
- no push.

## 44. Remaining Accessible-Core Issues

The accessible core remains partial because 64 expected official-provider ISRUC subjects are unacquired. Sleep-EDF is revalidated, but no new two-domain core config can honestly be frozen until ISRUC reaches a legitimate terminal full-population gate.

## 45. Remaining Final-Benchmark Issues

SHHS remains separate and unavailable under this step. No SHHS raw/XML data were accessed. The final three-domain benchmark remains unfrozen.

## 46. Recommended Next Step

Resume official account-free MEGA acquisition for I037-I100, beginning with a verified client/route and preserving the existing 100-subject manifest and per-file provenance. Do not use quota bypasses or unofficial mirrors. After acquisition, rerun the v2 rebuild and only then reassess the ISRUC and accessible-core gates.

## 47. Git Status / Diff Summary

Final post-commit verification was clean on `main`:

- latest local commit subject: `data: resume original ISRUC cohort migration`;
- commit contents: 21 safe implementation, test, manifest, config, documentation, and report files;
- `pytest -q`: 64 passed;
- `python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed;
- working tree: clean;
- raw/processed/REC/NPZ/transfer artifacts tracked by Git: none;
- remote push: none.

The repository remains intentionally unpushed.
