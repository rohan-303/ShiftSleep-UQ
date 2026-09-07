# ShiftSleep-UQ Step 7.9 ISRUC Completion and Accessible-Core Freeze Report

## 1. Status

PARTIAL

Step 7.9 restored and verified the official MEGAcmd route, acquired I037-I071, validated the newly acquired REC bodies, and rebuilt the available original-provider population. MEGA bandwidth quota then blocked acquisition beginning at I072. The accessible core was not frozen.

A new isolated completed-bundle schema finding was also recorded: I040 is body-valid but contains neither frozen exact pairing. It was transparently excluded as `EXCLUDED_UNSUPPORTED_MONTAGE`. This isolated finding does not broaden the contract and does not by itself trigger a third-family review.

## 2. Acquisition Environment

Repository: `C:\Users\rohan\ShiftSleep-UQ`.

Branch: `main`.

Official client found at:

`C:\Users\rohan\AppData\Local\MEGAcmd\MEGAclient.exe`

Verified client version:

`MEGAcmd version: 2.6.0.0: code 2060000 (64 bits)`

The client was already installed; no reinstall was performed. The executable and its installation directory were inspected locally. No personal MEGA login was used. `mega-whoami` returned `Not logged in`.

Official source page:

`https://sleeptight.isr.uc.pt/?page_id=48`

Official Cohort-I public folder exposed by that page:

`https://mega.nz/folder/QJgDQDDZ#ZMDj3w82msavACurqP48IA`

Anonymous public access was verified through the client namespace: `mega-ls /` returned subject folders `1` through `100`; `mega-ls /37` returned `37_1.txt`, `37_1.xlsx`, `37_2.txt`, `37_2.xlsx`, and `37.rec`.

No unofficial mirror, reconstructed direct file URL, quota bypass, `--ignore-quota-warn`, private URL, credential, or personal account was used.

## 3. Acquisition Outcome

Expected: 100 subjects.

Previously complete: 36 subjects.

Newly acquired during Step 7.9: 35 subjects, I037-I071.

Total complete original-provider bundles: 71 subjects, I001-I071.

Newly acquired REC bodies body-valid: 35/35.

Total body-valid original-provider REC files: 71/71.

Included after contract and structural processing: 70 subjects.

Remaining acquisition-pending subjects: 29 subjects, I072-I100.

I040 is complete and body-valid but structurally excluded because its channel labels did not resolve through the frozen exact resolver.

The acquisition manifest contains exactly 500 rows: 100 expected subjects x 5 expected file roles. The provider supplied additional files in I065; they were retained locally and not silently discarded. The expected five-role accounting remains explicit.

The first blocked subject was I072. The official client returned exit code `11` with:

`Failed to get account details: Access denied`

`Transfer not started.`

`You have reached your bandwidth quota. To circumvent this limit, you can upgrade to Pro, which will give you your own bandwidth package and also ample extra storage space.`

`Alternatively, you can try again in 5 hours.`

No retry beyond the bounded attempt was made, and the remaining subjects were not marked scientifically excluded.

## 4. ISRUC Cohort Gate

`ISRUC_ORIGINAL_COHORT_PARTIAL`

The expected population is exactly I001-I100 and every expected subject appears exactly once in the v2 subject and recording manifests. Seventy-one subjects have complete original-provider bundles; 70 are included; I040 is a completed structural exclusion; I072-I100 remain acquisition-pending/failure because MEGA quota blocked transfer.

## 5. Accessible-Core Gate

`CORE_DATA_PARTIAL`

Sleep-EDF SC passed light independent revalidation. ISRUC original-provider acquisition and final structural accounting are not complete, so the two-domain accessible core cannot be frozen.

## 6. Final Benchmark Gate

Expected: `NO`.

Actual: `NO`.

SHHS was not accessed.

## 7. Repository State

The repository is `C:\Users\rohan\ShiftSleep-UQ` on branch `main`. Step 7.8 exists in local history, and `reports/STEP_07_8_ISRUC_REBUILD_AND_CORE_FREEZE_REPORT.md` exists. The frozen data-contract and preprocessing configuration remain present.

At preflight, the working tree was clean. Step 7.9 generated updated lightweight manifests/audits, this report, and one regression-test adjustment. Raw provider files and processed arrays remain ignored and uncommitted.

No GitHub push occurred.

## 8. Frozen Contracts

Data contract: `1.2.0`.

Data-contract SHA-256: `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`.

Preprocessing: `0.1.0`.

Preprocessing SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`.

The exact pairings were unchanged:

- `C3-A2` + `LOC-A2` -> `ISRUC_A1A2`.
- `C3-M2` + `E1-M2` -> `ISRUC_M1M2`.

No rereferencing, signal renaming, fallback channels, fuzzy matching, alias expansion, annotation remapping, target-rate change, filtering, or normalization was introduced.

## 9. Provider Integrity

All 35 newly acquired REC bodies passed the existing EDF-compatible declared-byte/body-size validation with `body_delta = 0`. Combined with the prior 36 valid bodies, all 71 acquired REC bodies are body-valid.

| Provider-integrity state | Count |
|---|---:|
| Complete/body-valid bundles | 71 |
| Body-invalid completed bundles | 0 |
| Acquisition-pending subjects | 29 |
| Completed structural exclusions | 1 |

I040 has a valid REC body but is not contract-valid. It is not counted as a valid included recording.

## 10. Final Montage Inventory

| Montage/status | Subjects | Valid epochs |
|---|---:|---:|
| `ISRUC_A1A2` | 17 | 15,429 |
| `ISRUC_M1M2` | 53 | 47,650 |
| `UNSUPPORTED` | 1 | 0 |
| Acquisition failure/pending | 29 | 0 |
| Total included | 70 | 63,079 |

The counts are descriptive. No montage balancing or signal-scale exclusion was performed.

## 11. Unsupported/New Montage Findings

I040 is the only completed unsupported record. Its raw channel inventory was retained in the v2 schema audit. The labels include `ROC`, `A1`, `LOC`, `A2`, `C4`, `O2`, `C3`, `O1`, `F4`, `F3`, `X1`-`X8`, `DC8`, `DC3`, and `SaO2`; the frozen exact composite pair resolver did not find either accepted pairing.

I040 was recorded as:

`EXCLUDED_UNSUPPORTED_MONTAGE`

Operationally, the existing artifact uses failure code `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT` and montage status `UNSUPPORTED`.

This is one isolated completed record, not a substantial third montage family. The contract remains `1.2.0`; no contract `1.3.0` was created.

## 12. Annotation Audit

Original-provider scorer 1 remained primary. Scorer 2 remained diagnostic only. The 71 complete bundles had scorer-1 source files available and passed the existing source-vocabulary, file-integrity, and 30-second interpretation path. The 29 pending subjects have no acquired source annotations and remain acquisition failures, not annotation exclusions.

No NEMAR event file was used as primary for the rebuilt original-provider cohort. No fuzzy mapping or unknown-to-Wake mapping was added.

## 13. Full Preprocessing Results

The v2 rebuild was regenerated from the full expected population, not appended to the prior partial rows.

| Metric | Result |
|---|---:|
| Expected subjects | 100 |
| Complete acquired bundles | 71 |
| Included subjects | 70 |
| Structural exclusions | 1 |
| Acquisition-pending subjects | 29 |
| EEG target | 100 Hz / 3000 samples per epoch |
| EOG target | 50 Hz / 1500 samples per epoch |
| Dtype | float32 |
| Unit | canonical microvolt |
| Normalization | none |
| Additional filtering | none |

All 70 included subjects were processed under contract `1.2.0` and preprocessing `0.1.0`.

## 14. Structural Exclusions

Exactly one completed subject was structurally excluded: I040, `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`.

No completed body was excluded for truncation, missing scorer 1, finite-value failure, target shape failure, stage distribution, amplitude, or model performance.

## 15. Epoch Accounting

The 70 included subjects produced 63,079 valid canonical epochs.

For every included subject:

`valid = Wake + N1 + N2 + N3 + REM`

`source_staging = valid + excluded_staging`

`EEG rows = EOG rows = labels rows = valid`

`accounting_delta = 0`

All 70 included accounting rows passed. The one structural exclusion and 29 acquisition-pending rows are explicit `EXCLUDED` rows and are not represented as valid canonical epochs.

## 16. Stage Distribution

Descriptive only.

Aggregate canonical counts for the 70 included subjects are retained in `reports/isruc_original_epoch_accounting_v2.csv`. No stage-balance threshold, subject selection, or montage optimization was performed.

## 17. Montage Distribution

The final available original-provider distribution is:

- `ISRUC_A1A2`: 17 subjects and 15,429 epochs.
- `ISRUC_M1M2`: 53 subjects and 47,650 epochs.
- Unsupported completed montage: 1 subject, I040.
- Acquisition-pending: 29 subjects, I072-I100.

## 18. Montage QC

The existing raw-scale, montage-stratified QC was regenerated over the 70 included subjects. No montage normalization, rescaling, threshold fitting, or amplitude-based exclusion was performed.

The previously observed A1/A2 versus M1/M2 amplitude-scale difference remains descriptive and unresolved for later explicit analysis. It was not removed during Step 7.9.

The regenerated QC artifact is:

`reports/isruc_montage_qc_v2.csv`

SHA-256:

`027288bcd4f374bd27d4f05c0a26bb4399904169e34ac37f194f69d9b0bf74c0`

## 19. Unit / Rate Audit

All 71 body-valid completed records passed the provider header/body audit. The 70 included records passed the existing contract-processing path with native 200 Hz source rates and canonical target rates of EEG 100 Hz and EOG 50 Hz. Units remained canonical microvolt. I040 was not treated as contract-valid merely because its body was valid.

## 20. Duration / Alignment

All 70 included recordings passed the existing duration and 30-second alignment checks. No incomplete canonical epoch was fabricated. I040 has no valid canonical output because it was excluded before preprocessing. I072-I100 have no acquired source files.

## 21. Duplicate Audit

The rebuilt duplicate audit found no duplicate included raw REC SHA-256 values and no duplicate included processed-output SHA-256 values. The audit was regenerated from the full available v2 population.

## 22. Determinism

The rebuild deterministically reprocessed every included available subject, including the required first five included subjects in each accepted montage family. All 70 included subjects passed complete-output hash equality between the original v2 output and the deterministic rerun.

Determinism rows: 70.

Determinism passes: 70.

The temporary deterministic NPZ files were removed after the audit and remain untracked.

## 23. ISRUC Viability

`VIABLE_WITH_EXCLUSIONS`

The acquired original-provider subset is viable with transparent exclusions: 71 complete body-valid bundles, 70 included subjects, one isolated unsupported completed record, and 29 acquisition-pending subjects. The full expected population is not yet acquired, so this viability assessment does not authorize a frozen final ISRUC cohort.

## 24. Final Provider Migration Outcome

The provider migration outcome is partial:

- historical NEMAR-derived included subjects: 15;
- original-provider complete bundles: 71;
- original-provider included subjects: 70;
- original-provider A1/A2: 17;
- original-provider M1/M2: 53;
- completed structural exclusions: 1;
- acquisition exclusions/pending: 29;
- subjects recovered relative to the historical included count: 55.

The current outcome is recorded as `PARTIAL`, not complete or frozen.

## 25. Final ISRUC Cohort

No new frozen v3 config was created because the 100-subject migration did not close.

The active artifact remains:

`configs/isruc_original_cohort_v2.yaml`

Its scientific state remains partial and inactive as a final primary cohort. The regenerated v2 manifest hashes are:

- `isruc_original_acquisition_manifest_v2.csv`: `bd55383e087afd868a71f258511fa424673b1def1bff9ef57e7b56e410e89557`
- `isruc_original_recording_manifest_v2.csv`: `63f035fc168ad80f641e84e7e6dfe714e55e48b64331561a5c9eb2704fae9245`
- `isruc_original_subject_manifest_v2.csv`: `97ef91504916b2b4cac60f8e9ba67b436cc1f789c0ba46aba06812df01f12d86`
- `isruc_montage_distribution_v2.csv`: `b3840d0980febaa1bd6b34027cee7141b97694bc277ad1acff6d79ee2e6a0a97`
- `isruc_montage_qc_v2.csv`: `027288bcd4f374bd27d4f05c0a26bb4399904169e34ac37f194f69d9b0bf74c0`

The manifest hash file is:

`reports/isruc_original_cohort_v2_hashes.txt`

## 26. Historical Cohort Supersession

Historical cohorts were preserved. The NEMAR-derived cohort and the earlier original-provider partial artifacts were not deleted and were not falsely marked superseded by a complete frozen replacement.

Because Step 7.9 remains partial, historical-provider supersession is deferred until a successful full original-provider freeze.

## 27. Recording Manifest

File:

`reports/isruc_original_recording_manifest_v2.csv`

Rows: 100.

All expected subjects appear exactly once. Included rows: 70. I040 is an explicit structural exclusion. I072-I100 are explicit acquisition exclusions/pending rows.

SHA-256:

`63f035fc168ad80f641e84e7e6dfe714e55e48b64331561a5c9eb2704fae9245`

## 28. Subject Manifest

File:

`reports/isruc_original_subject_manifest_v2.csv`

Rows: 100.

No duplicate subject IDs were found.

SHA-256:

`97ef91504916b2b4cac60f8e9ba67b436cc1f789c0ba46aba06812df01f12d86`

## 29. Sleep-EDF Revalidation

Expected: 78 subjects / 153 recordings.

The existing authoritative repaired artifacts were lightly revalidated without rebuilding Sleep-EDF.

| Check | Result |
|---|---:|
| Subjects | 78 |
| Recordings | 153 |
| Manifest epochs | 414,961 |
| Loaded epochs | 414,961 |
| Shape passes | 153/153 |
| Finite-value passes | 153/153 |
| Output-hash passes | 153/153 |

Sleep-EDF remains scientifically credible. Its preprocessing was not changed.

## 30. Final Accessible-Core Population

Sleep-EDF SC:

- subjects: 78;
- recordings: 153;
- valid epochs: 414,961.

ISRUC original-provider available population:

- expected subjects: 100;
- complete acquired bundles: 71;
- included subjects: 70;
- included recordings: 70;
- valid epochs: 63,079;
- A1/A2 subjects: 17;
- M1/M2 subjects: 53;
- structural exclusions: 1;
- acquisition-pending subjects: 29.

This is not a final accessible-core freeze because the ISRUC expected population is incomplete and contains an unresolved terminal acquisition gate.

## 31. Accessible-Core Config

No `configs/core_cohort_v2.yaml` was created. The accessible-core gate remains `CORE_DATA_PARTIAL`, so the historical `core_cohort_v1_1.yaml` was not promoted or overwritten.

## 32. Split Feasibility

No subject assignments, split fields, seeds, folds, calibration partitions, or train/dev/test artifacts were created.

A later split-feasibility assessment must wait for completion of I072-I100 and resolution of the final ISRUC inclusion population.

## 33. Leakage / Target-Free Protections

Confirmed:

- no models;
- no training;
- no split generation;
- no normalization fitting;
- no calibration;
- no model metrics;
- no outcome-based inclusion;
- no stage-composition selection;
- no montage balancing optimization;
- no use of SHHS;
- no NEMAR substitution for missing official-provider subjects.

## 34. Tests Added

No new audit framework was created. The existing Step 7.8 artifact tests were minimally updated to support legitimate full-cohort growth: stale assertions requiring exactly 36 included/deterministic rows now require at least the established minimum and reconcile determinism rows with the current included manifest rows.

The tests continue to verify exact montage resolution, artifact structure, subject-row uniqueness, processed-output metadata/shapes, accounting deltas, determinism, and absence of split fields.

## 35. Full Validation

Actual results:

- `pytest -q` -> **64 passed in 7.53s**.
- `PYTHONPATH=src python -m compileall -q src tests scripts` -> passed.
- `git diff --check` -> passed.

Acquisition/rebuild validation:

- acquisition manifest rows: 500;
- recording manifest rows: 100;
- subject manifest rows: 100;
- complete body-valid REC files: 71/71;
- included original-provider subjects: 70;
- structural exclusions: 1;
- pending acquisition subjects: 29;
- included accounting rows with delta zero: 70/70;
- deterministic reruns passed: 70/70;
- accepted montage counts: 17 A1/A2 and 53 M1/M2;
- Sleep-EDF hash/shape/finite passes: 153/153;
- raw and processed data tracked by Git: none;
- credentials/private URLs/personal MEGA session: none;
- GitHub push: none.

## 36. Files Created

- `reports/STEP_07_9_ISRUC_COMPLETION_AND_CORE_FREEZE_REPORT.md`

The Step 7.9 rebuild also regenerated the existing lightweight v2 audit/manifests in place:

- `reports/isruc_original_acquisition_manifest_v2.csv`
- `reports/isruc_original_recording_manifest_v2.csv`
- `reports/isruc_original_subject_manifest_v2.csv`
- `reports/isruc_original_annotation_audit_v2.csv`
- `reports/isruc_original_epoch_accounting_v2.csv`
- `reports/isruc_original_duration_alignment_v2.csv`
- `reports/isruc_full_schema_unit_rate_audit_v2.csv`
- `reports/isruc_montage_distribution_v2.csv`
- `reports/isruc_montage_qc_v2.csv`
- `reports/isruc_duplicate_audit_v2.csv`
- `reports/isruc_determinism_audit_v2.csv`
- `reports/isruc_provider_migration_final_outcome.csv`
- `reports/isruc_original_cohort_v2_hashes.txt`

## 37. Files Modified

- `tests/test_isruc_step78_artifacts.py` — removed stale exact-36 assumptions and reconciled determinism rows with the current included manifest.
- Existing v2 lightweight audit/manifests listed in Section 36 were regenerated from the full available population.

No frozen scientific contract file was modified. No raw or processed data file is intended for Git tracking.

## 38. Explicitly Not Done

Confirmed:

- no splits;
- no model;
- no training;
- no normalization fitting;
- no ML metrics;
- no calibration;
- no conformal evaluation;
- no SHHS access;
- no raw/processed data committed;
- no push.

## 39. Remaining Accessible-Core Issues

The remaining official acquisition IDs are:

`I072-I100`

MEGA account-free bandwidth quota blocked the official transfer beginning at I072. The 29 subjects remain acquisition-pending/failure and are not scientifically excluded.

I040 is a completed body-valid structural exclusion under the unchanged exact contract. Its isolated unsupported layout must remain explicitly accounted for in any later full freeze.

## 40. Remaining Final-Benchmark Issues

The final benchmark gate remains `NO`. SHHS remains a separate planned domain and was not accessed in Step 7.9.

## 41. Recommended Next Step

Continue the same official account-free MEGA transfer after the provider quota reset, beginning at I072 and continuing sequentially through I100. Do not reacquire I001-I071 unless a later integrity audit finds a specific defect. Do not use `--ignore-quota-warn`, personal login, unofficial mirrors, reconstructed URLs, or quota circumvention.

After I072-I100 are acquired, regenerate the full v2 rebuild, reassess I040 and any additional unsupported layouts, then determine whether a new frozen ISRUC cohort and accessible-core config are justified. Do not execute Step 8, split design, calibration, or modeling before that gate.

## 42. Git Status / Diff Summary

Step 7.9 was committed locally with subject `data: continue original ISRUC acquisition`. The final working tree is clean; raw provider files and processed arrays remain ignored. No GitHub push occurred.
