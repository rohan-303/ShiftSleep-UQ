# ShiftSleep-UQ Step 7.10 ISRUC Final Acquisition and Accessible-Core Freeze Report

## 1. Status

PARTIAL

Step 7.10 verified the official MEGAcmd installation and the official anonymous Cohort-I public route. The provider namespace remained readable and confirmed that I072 exists, but the first acquisition attempt for I072 was blocked by the MEGA bandwidth quota. Per the stop rule, no quota bypass, personal login, `--ignore-quota-warn`, repeated retry loop, or unofficial route was used.

No new subjects were acquired in this run. The accessible-core data phase remains open.

## 2. Acquisition Outcome

Previously complete: 71 subjects, I001-I071.

Attempted: I072-I100, with the bounded acquisition attempt beginning at I072.

Newly complete: 0.

Total complete: 71.

Remaining: 29 subjects, I072-I100.

I072 contains only resumable `.getxfer` state from the prior blocked attempt. No validated primary source file was accepted from that state.

The existing 71 complete original-provider bundles were not reacquired or overwritten.

## 3. Provider / Quota Outcome

Official client:

`C:\Users\rohan\AppData\Local\MEGAcmd\MEGAclient.exe`

Verified version:

`MEGAcmd version: 2.6.0.0: code 2060000 (64 bits)`

Official source page:

`https://sleeptight.isr.uc.pt/?page_id=48`

Official Cohort-I public folder:

`https://mega.nz/folder/QJgDQDDZ#ZMDj3w82msavACurqP48IA`

Anonymous namespace verification succeeded:

- `mega-ls /` exposed subject folders 1 through 100.
- `mega-ls /72` returned `72_1.txt`, `72_1.xlsx`, `72_2.txt`, `72_2.xlsx`, and `72.rec`.

The bounded `mega-get /72` attempt returned exit code `11`:

`Transfer not started.`

`You have reached your bandwidth quota.`

`Alternatively, you can try again in 5 hours.`

The client also emitted `Failed to get account details: Access denied`. This is a provider quota state, not evidence that I072 is absent.

Final provider classification for this run:

`PROVIDER_QUOTA_BLOCKED`

No personal MEGA account was used. No credentials, unofficial mirror, reconstructed direct URL, proxy/VPN quota evasion, or `--ignore-quota-warn` option was used.

## 4. ISRUC Cohort Gate

`ISRUC_ORIGINAL_COHORT_PARTIAL`

The expected population remains exactly I001-I100. The current authoritative state is:

- complete original-provider bundles: 71;
- body-valid completed REC files: 71/71;
- included subjects: 70;
- completed structural exclusions: 1, I040;
- acquisition-pending subjects: I072-I100.

All 100 expected subjects remain explicitly represented in the existing v2 manifests.

## 5. Accessible-Core Gate

`CORE_DATA_PARTIAL`

No accessible-core freeze was justified because the remaining official-provider ISRUC subjects could not be acquired. Sleep-EDF remains independently credible, but the two-domain core is not closed.

## 6. Final Benchmark Gate

Expected: `NO`.

Actual: `NO`.

SHHS was not accessed.

## 7. Repository State

Repository:

`C:\Users\rohan\ShiftSleep-UQ`

Branch: `main`.

The preflight working tree was clean. Step 7.9 exists in local history, and `reports/STEP_07_9_ISRUC_COMPLETION_AND_CORE_FREEZE_REPORT.md` exists.

The data contract and preprocessing files remain unchanged. I001-I071 raw bundles remain present. I072 resumable transfer state was preserved. No raw or processed data was staged.

## 8. Frozen Contracts

Data contract: `1.2.0`.

Data-contract SHA-256:

`ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`

Preprocessing: `0.1.0`.

Preprocessing SHA-256:

`70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`

Accepted exact pairings remain:

- `C3-A2` + `LOC-A2` -> `ISRUC_A1A2`.
- `C3-M2` + `E1-M2` -> `ISRUC_M1M2`.

No montage, label, rate, epoch, unit, preprocessing, scorer, or target-free protocol was changed.

## 9. Provider Integrity

The existing 71 completed original-provider REC files remain body-valid under the existing declared-byte formula, with `body_delta = 0`.

No new REC reached a validated acquired state in Step 7.10. I072-I100 therefore have no new provider-integrity result beyond explicit acquisition-pending status.

The prior completed-provider integrity state remains:

| State | Count |
|---|---:|
| Complete/body-valid bundles | 71 |
| Body-invalid completed bundles | 0 |
| Included subjects | 70 |
| Completed structural exclusions | 1 |
| Acquisition-pending subjects | 29 |

## 10. Full Montage Inventory

The authoritative available original-provider inventory remains:

| Montage/status | Subjects | Valid epochs |
|---|---:|---:|
| `ISRUC_A1A2` | 17 | 15,429 |
| `ISRUC_M1M2` | 53 | 47,650 |
| Unsupported completed montage | 1 | 0 |
| Acquisition-pending | 29 | 0 |
| Included total | 70 | 63,079 |

No new montage inventory was generated because the run stopped at the first provider quota block.

## 11. Unsupported Montage Findings

I040 remains the only completed unsupported montage finding:

- subject: I040;
- status: `EXCLUDED_UNSUPPORTED_MONTAGE`;
- failure code: `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`.

I040 was not reopened or reinterpreted. No new subject was acquired, so no new unsupported montage case was observed.

No repeated coherent third montage family was identified in this run. The contract remains `1.2.0`.

## 12. Annotation Audit

No new annotation files were acquired in Step 7.10.

For the existing 71 complete bundles, original-provider scorer 1 remains primary and scorer 2 remains diagnostic. The prior scorer-1 integrity and vocabulary audit remains authoritative.

No NEMAR labels were substituted. No unknown or unscored stage was mapped to Wake.

## 13. Full Preprocessing Outcome

A full rebuild was intentionally not run because the official provider blocked at the first remaining subject and the step explicitly requires minimum reconciliation rather than an expensive rebuild when acquisition remains incomplete.

Existing completed preprocessing remains:

- included subjects: 70;
- EEG: 100 Hz, 3000 samples per epoch;
- EOG: 50 Hz, 1500 samples per epoch;
- dtype: float32;
- unit: canonical microvolt;
- normalization: none;
- additional filtering: none.

No I072-I100 subject was preprocessed.

## 14. Structural Exclusions

The existing completed structural exclusion remains exactly one subject:

I040, `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`.

No new structural exclusion was generated in Step 7.10.

I072-I100 remain acquisition-pending, not scientifically or structurally excluded.

## 15. Epoch Accounting

The existing included original-provider population remains at 63,079 valid epochs.

For the existing 70 included subjects, the previous accounting invariants remain satisfied:

`valid = Wake + N1 + N2 + N3 + REM`

`source_staging = valid + excluded_staging`

`EEG rows = EOG rows = labels rows = valid`

`accounting_delta = 0`

No new epoch accounting was computed for I072-I100 because no validated source bundle was acquired.

## 16. Stage Distribution

Descriptive only.

The existing v2 epoch accounting remains authoritative for the 70 included subjects. No stage-composition decision was made, and no pending subject was excluded based on stage distribution.

## 17. Montage Distribution

Existing included distribution:

- `ISRUC_A1A2`: 17 subjects, 15,429 valid epochs;
- `ISRUC_M1M2`: 53 subjects, 47,650 valid epochs;
- unsupported completed montage: I040;
- acquisition-pending: I072-I100.

No balancing or subject selection was performed.

## 18. Montage QC

The existing non-normalized raw-scale montage QC remains authoritative for the 70 included subjects. The previously observed amplitude-scale difference between A1/A2 and M1/M2 was not normalized, rescaled, thresholded, or used for exclusion.

No new QC was generated because no new subject was acquired and the full rebuild was correctly skipped under the quota-block policy.

## 19. Unit / Rate Audit

The existing 71 body-valid completed records retain their prior provider-header and processing audit results. Existing included records use the frozen target rates of EEG 100 Hz and EOG 50 Hz under preprocessing `0.1.0`.

No new unit or rate result exists for I072-I100.

## 20. Duration / Alignment

The existing 70 included recordings retain their prior successful 30-second duration and alignment results.

I072-I100 have no validated acquired recordings in this run. No incomplete epoch or fabricated duration was accepted.

## 21. Duplicate Audit

No new raw or processed objects were accepted, so no new duplicate candidate was introduced by Step 7.10.

The prior v2 duplicate audit remains authoritative for the 71 complete provider bundles and 70 included processed outputs. Existing subject IDs remain unique.

## 22. Determinism

The full-acquisition condition required for the Step 7.10 deterministic panel was not met.

No new deterministic rerun was performed. The previous evidence remains valid for the existing completed population. The required Step 7.10 panel must be run only after I072-I100 are acquired and the final cohort is rebuilt:

- first five included `ISRUC_A1A2` subjects;
- first five included `ISRUC_M1M2` subjects;
- last two newly included subjects numerically.

Status: `NOT_COMPUTED_THIS_RUN`.

## 23. ISRUC Viability

`VIABLE_WITH_EXCLUSIONS` for the currently acquired subset.

The available subset contains 71 body-valid completed bundles, 70 included subjects, and one transparent unsupported-montage exclusion. This is not a final full-population viability decision because I072-I100 remain unacquired.

## 24. Final Provider Migration Outcome

The provider migration remains partial:

- original-provider complete bundles: 71;
- original-provider included subjects: 70;
- original-provider A1/A2: 17;
- original-provider M1/M2: 53;
- completed structural exclusions: 1;
- acquisition-pending subjects: 29;
- new subjects acquired in Step 7.10: 0.

No historical cohort was superseded in this step.

## 25. Frozen ISRUC Cohort

No frozen v3 ISRUC config was created.

The existing partial artifact remains:

`configs/isruc_original_cohort_v2.yaml`

No `ACTIVE_FROZEN` status was assigned. The existing v2 partial manifests and hashes remain the authoritative available-population artifacts.

## 26. Historical Cohort Supersession

No supersession change was made.

Historical NEMAR-derived and original-provider partial artifacts remain preserved. The v2 partial cohort was not promoted to frozen, and no v3 replacement was created.

## 27. Recording Manifest

Existing file:

`reports/isruc_original_recording_manifest_v2.csv`

Rows: 100.

All expected subjects appear exactly once. I072-I100 remain explicit acquisition-failure rows. The existing manifest hash remains:

`63f035fc168ad80f641e84e7e6dfe714e55e48b64331561a5c9eb2704fae9245`

No new recording row was appended.

## 28. Subject Manifest

Existing file:

`reports/isruc_original_subject_manifest_v2.csv`

Rows: 100.

No duplicate subject IDs were found. I072-I100 remain explicit non-acquired subject rows.

Existing manifest hash:

`97ef91504916b2b4cac60f8e9ba67b436cc1f789c0ba46aba06812df01f12d86`

## 29. Sleep-EDF Revalidation

Sleep-EDF was not rebuilt or modified.

The previously completed light revalidation remains authoritative:

- subjects: 78;
- recordings: 153;
- valid epochs: 414,961;
- shape passes: 153/153;
- finite-value passes: 153/153;
- output-hash passes: 153/153.

## 30. Accessible-Core Population

Sleep-EDF SC:

- subjects: 78;
- recordings: 153;
- valid epochs: 414,961.

ISRUC original-provider available population:

- expected subjects: 100;
- complete bundles: 71;
- included subjects: 70;
- included recordings: 70;
- valid epochs: 63,079;
- A1/A2 subjects: 17;
- M1/M2 subjects: 53;
- structural exclusions: 1;
- acquisition-pending subjects: I072-I100.

The accessible core remains incomplete.

## 31. Accessible-Core Config

No `configs/core_cohort_v2.yaml` was created or promoted.

The accessible-core gate remains `CORE_DATA_PARTIAL`. No split fields, calibration partition, folds, or train/dev/test fields were introduced.

## 32. Split Feasibility

No split feasibility calculation was performed because the accessible core did not freeze.

No assignments, seeds, folds, calibration set, normalization fit, or subject-level bootstrap artifacts were created.

## 33. Leakage / Target-Free Protections

Confirmed:

- no split generation;
- no model implementation;
- no training;
- no normalization fitting;
- no ML metrics;
- no calibration;
- no conformal work;
- no outcome-based inclusion;
- no stage-based pending-subject exclusion;
- no montage balancing;
- no NEMAR substitution;
- no SHHS access;
- no personal MEGA login;
- no quota bypass.

## 34. Tests

No new testing subsystem was created.

No production scientific code changed in Step 7.10. Existing tests remain in place. A final full-cohort test update is deferred until acquisition completes and the final v3/core artifacts exist.

## 35. Full Validation

Preflight results:

- repository: `C:\Users\rohan\ShiftSleep-UQ`;
- branch: `main`;
- working tree: clean at preflight;
- MEGAcmd executable: present;
- MEGAcmd version: `2.6.0.0`;
- contract SHA-256: `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`;
- preprocessing SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`;
- acquisition manifest rows: 500;
- recording manifest rows: 100;
- subject manifest rows: 100;
- official `/72` listing: accessible;
- official `/72` transfer: blocked with rc=11;
- validated newly acquired subjects: 0.

Because the step stopped at the provider quota gate, the expensive full-cohort rebuild was not rerun.

The final repository validation completed successfully:

- `pytest -q` -> **64 passed in 7.69s**;
- `PYTHONPATH=src python -m compileall -q src tests scripts` -> passed;
- `git diff --check` -> passed.

## 36. Files Created

- `reports/STEP_07_10_ISRUC_FINAL_ACQUISITION_AND_CORE_FREEZE_REPORT.md`

No new raw or processed artifact was accepted.

## 37. Files Modified

The Step 7.10 report is the only intended new tracked file from this run.

No scientific contract, parser, montage resolver, preprocessing, or historical cohort file was modified.

The existing v2 manifests were not rewritten because the acquisition state remained unchanged: zero newly acquired subjects and I072-I100 already explicitly represented as acquisition failures.

## 38. Explicitly Not Done

Confirmed:

- no split generation;
- no model;
- no training;
- no normalization fitting;
- no ML metrics;
- no calibration;
- no conformal work;
- no SHHS access;
- no raw/processed data committed;
- no push.

## 39. Remaining Accessible-Core Issues

The exact remaining acquisition IDs are:

`I072-I100`

The blocker is the official account-free MEGA bandwidth quota. The public namespace is readable, but MEGA refuses the transfer at I072 with rc=11 and “You have reached your bandwidth quota.”

The resumable transfer state for I072 was preserved. No remaining subject was marked scientifically excluded.

## 40. Remaining Final-Benchmark Issues

SHHS remains separate and was not accessed.

Therefore:

`FINAL_BENCHMARK_GATE = NO`

## 41. Recommended Next Step

Continue the same official account-free MEGA transfer from **I072** after the provider quota reset. Do not reacquire I001-I071 unless a specific integrity defect is later found. Do not use a personal login, `--ignore-quota-warn`, unofficial mirror, reconstructed URL, VPN/proxy quota evasion, or any other bypass.

After I072-I100 are acquired, regenerate the complete full-population ISRUC artifacts, perform the required final deterministic panel, evaluate the frozen v3 cohort gate, and only then consider:

# Step 8 — Subject-Level Split, Calibration, C0–C5 Evaluation, Seed, and Statistical-Analysis Protocol Freeze

Do not execute Step 8 in this step.

## 42. Git Status / Diff Summary

Step 7.10 was committed locally with subject:

`data: continue original ISRUC acquisition`

No GitHub push is authorized. Raw provider files, resumable transfer state, and processed arrays remain ignored and uncommitted.
