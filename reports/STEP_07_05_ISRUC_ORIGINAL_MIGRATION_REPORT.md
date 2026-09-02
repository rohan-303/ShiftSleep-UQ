# ShiftSleep-UQ Step 7.5 Original ISRUC Migration Report

## 1. Status

BLOCKED

The original-provider migration executed safely through the MEGA bandwidth quota boundary. Subjects I001–I035 were acquired and validated; subject I036 has a resumable partial signal transfer; subjects I037–I100 could not be acquired because the account-free public route reported its bandwidth quota was exhausted. No claim of a complete 100-subject migration is made.

## 2. ISRUC Migration Gate

ISRUC_ORIGINAL_COHORT_PARTIAL

All 100 expected subjects have terminal rows, but acquisition is incomplete and the resulting cohort is not frozen.

## 3. Accessible-Core Gate

CORE_DATA_BLOCKED

Sleep-EDF is credible after the Step 7.2 repair/audit, but ISRUC remains only 17/100 included and is affected by both incomplete acquisition and systematic schema/channel exclusions. The two-domain accessible core therefore cannot be frozen.

## 4. Final Benchmark Gate

NO

SHHS1 remains separate, unauthorized, and not benchmark-frozen.

## 5. Repository State

Repository: `C:\Users\rohan\ShiftSleep-UQ`. The Step 7.4 report, migration plan, frozen expected population, migration provenance, audits, and this report exist. Raw original data and processed arrays remain outside Git tracking under the repository ignore policy. No GitHub push was performed. The Step 7.4 commit was verified during preflight as present in repository history; Step 7.5 changes were not pushed.

## 6. Provider Migration Provenance

Old: NEMAR `nm000111 v1.0.1`.

New: `ORIGINAL_ISRUC_MEGA`, the official ISRUC-Sleep Cohort I public MEGA distribution.

Reason: the Step 7.3/7.4 predeclared panel demonstrated selective NEMAR provider-object truncation: I001 and I002 were truncated while original recordings were complete; I003 was complete and retained overlap was faithful. The scientific contract did not change. Provider/provenance changed only.

## 7. Disk / Acquisition Environment

The storage volume containing `data\raw` was checked before remaining acquisition. At preflight, the C: volume had ample free space; the later post-acquisition check reported exactly 198,921,408,512 bytes free. Current post-acquisition sizes are `data/raw` 27,832,010,766 bytes, `data/processed` 6,809,337,132 bytes, and `data/interim` 61,181 bytes. The source record and migration plan state the official Cohort I scale is approximately 14.12 GB. A conservative temporary headroom estimate of at least 28.24 GB (one source-scale copy plus one source-scale temporary/retry allowance), in addition to processed outputs and manifests, was available; storage was not the blocker.

MEGAcmd executable: `C:\Users\rohan\AppData\Local\MEGAcmd\MegaClient.exe` via `mega-get.bat` equivalent. Version: 2.6.0.0. Public-folder access was account-free and subject folders were individually addressable by numeric folder identifier. No personal MEGA login, browser automation, unofficial mirror, credential, or signed private URL was used. The provider returned a bandwidth-quota refusal after I035 and advised retrying in approximately four hours. One bounded retry of I036 returned `rc=11`; no unbounded retry or quota bypass was attempted.

## 8. Expected Population

Expected S1 subjects: **100**.

The frozen definition is `reports/isruc_original_expected_population.csv`, created before full acquisition results were known. It contains exactly I001–I100 and expected filenames `N.rec`, `N_1.txt`, `N_1.xlsx`, `N_2.txt`, and `N_2.xlsx`.

## 9. Acquisition Results

Subjects: expected **100**; complete bundles **35** (I001–I035); partial bundles **1** (I036, scorer files present but signal incomplete); failed/unacquired **64** (I037–I100). The bundle audit has exactly 100 rows.

Files: expected **500**; acquired **179**; failed/missing **321**. The 179 acquired files comprise 175 files from 35 complete bundles plus four I036 annotation files. The file-level acquisition manifest has exactly 500 rows.

Bytes: acquired file bytes total **5,240,301,165**. I036’s `.getxfer` partial is preserved as a resumable temporary and is not treated as a completed raw REC.

## 10. Original Provider Integrity

Of 100 expected subjects: body-valid **35**; truncated **0 completed REC files**; header-invalid **0 completed REC files**; other invalid/not acquired **65**. The 65 non-body-valid terminal rows represent absent/incomplete signal acquisition, not relaxed structural validation. For every completed REC, the exact EDF-compatible formula was applied: header length plus record count times the sum of per-signal samples per record times two bytes.

## 11. Bundle Completeness

`BUNDLE_COMPLETE`: 35. `BUNDLE_MISSING_SIGNAL`: 65, including I036’s incomplete signal transfer and I037–I100 with no completed signal. No completed subject was silently dropped. Scorer-1 and scorer-2 were available for 36 subjects because I036’s annotation files arrived; scorer-1 absence was treated as a primary blocker where applicable.

## 12. Channel Inventory

Among the 35 body-valid original RECs, C3-A2 was present in 17/35, LOC-A2 was present in 17/35, and both required channels were present in 17/35. No fallback channel was used. The complete inventory is `reports/isruc_original_channel_inventory.csv`; it records full labels, signal counts, indices, native rates, and units.

## 13. Rate / Unit Inventory

The required adapter gate was C3-A2 and LOC-A2 at 200 Hz with microvolt units, then EEG resampling to 100 Hz and EOG resampling to 50 Hz. No normalization, new filtering, channel substitution, or contract rewrite was performed. Exact observed schema combinations are in `reports/isruc_original_schema_variation_audit.csv` and its summary. Deviations were explicit and caused schema exclusions where required channels were absent.

## 14. Scorer-1 Annotation Audit

Original scorer-1 TXT was selected as the primary annotation source: `N_1.txt`, resolved programmatically by `read_original_scorer1` and retained with the corresponding workbook as semantic/provenance cross-check. The audit covers every available annotation file. Numeric source labels were mapped only through the existing source-verified mapping to Wake, N1, N2, N3, and REM. No fuzzy aliases or NEMAR `events.tsv` primary labels were used. Complete acquired subjects had deterministic 30-second scorer-1 epoch sequences; the exact per-subject audit is `reports/isruc_original_annotation_audit.csv`.

## 15. Scorer-2 Diagnostic Audit

Scorer-2 TXT/XLSX was audited separately and retained for diagnostic provenance. Its absence does not invalidate a primary subject when scorer-1, signal, and alignment are valid. The primary rebuilt labels use original scorer-1 only.

## 16. Original Adapter Regression

Original subjects I001, I002, and I003 passed the real parser/adapter smoke and were processed through the original-provider path. For I003, original-provider output and the previous validated NEMAR I003 output were identical for EEG arrays, EOG arrays, labels, source epoch indices, and epoch onsets: each had shape EEG `(943, 3000)`, EOG `(943, 1500)`, labels `(943,)`, and all comparisons were `np.array_equal=True` with maximum numeric difference `0.0`. The only provenance difference was intentional: `original ISRUC scorer-1 TXT` versus `NEMAR_BIDS_DERIVATIVE v1.0.1`; the scientific output was identical.

## 17. Full Preprocessing Results

Expected: **100**. Included: **17**. Excluded: **83**. Processing reused the frozen data contract 1.1.0 and preprocessing version 0.1.0. Acquired body-valid subjects lacking both required channels were excluded by `MISSING_REQUIRED_CHANNEL`; subjects without completed signal acquisition were excluded by acquisition status. No model or ML metric computation occurred.

## 18. Structural Exclusions

`EXCLUDED_ACQUISITION`: 65. `EXCLUDED_SCHEMA`: 18. `EXCLUDED_UNIT`: 0. `EXCLUDED_ANNOTATION`: 0. `EXCLUDED_ALIGNMENT`: 0. `EXCLUDED_OUTPUT_INTEGRITY`: 0. `EXCLUDED_OTHER_STRUCTURAL`: 0. The 18 schema exclusions are among body-valid original recordings that did not contain both exact required channels. The acquisition exclusions are not evidence that those subjects are scientifically invalid; they remain unresolved until official acquisition can resume.

## 19. Epoch Accounting

Across included processed subjects: source staging **15,429**; valid canonical **15,429**; excluded **0**; aggregate delta **0**. Every included subject has `valid = Wake + N1 + N2 + N3 + REM`, equal EEG/EOG/label row counts, finite outputs, reconciled exclusions, and no valid canonical stage in unknown exclusions. `reports/isruc_original_epoch_accounting.csv` has exactly 100 terminal subject rows; unacquired subjects have zero observed staging epochs and explicit exclusion status.

## 20. Stage Distribution

Descriptive only. The stage distribution file contains five rows per included subject plus five `ALL_INCLUDED` aggregate rows. Aggregate counts are preserved in `reports/isruc_original_stage_distribution.csv`; no eligibility decision was made from stage proportions and Wake was not trimmed.

## 21. Signal QC

`reports/isruc_original_signal_qc.csv` records recording-level EEG/EOG min, max, median, MAD, IQR, finite counts, total counts, and flat proportions for included outputs. No amplitude-based exclusion was applied. All included outputs were finite.

## 22. Unit-Scale Audit

**PASS** for the processed original-provider outputs relative to prior validated original subjects 1–3 and the existing Sleep-EDF SC included-cohort unit-scale reference. No unexplained 1e3 or 1e6 conversion factor was observed. Domain amplitude differences were not normalized away. Detailed values remain in the generated QC/audit artifacts.

## 23. Duration / Alignment Audit

`reports/isruc_original_duration_alignment.csv` records signal duration, scorer-1 epoch count, annotation duration, valid duration, alignment delta, and status. Included recordings passed exact 30-second staging/alignment requirements; no Wake trimming occurred. Unacquired subjects have explicit unresolved/excluded status rather than inferred duration.

## 24. Duplicate Audit

`reports/isruc_original_duplicate_audit.csv` audits duplicate raw REC hashes, processed output hashes, subject IDs, and the available scorer-1 hashes. No duplicate subject ID or identical full signal across different included subjects was accepted as valid without audit. Similar file sizes were not treated as duplicates.

## 25. Determinism Audit

The first five included IDs in numeric order— I001, I002, I003, I004, and I005—were reprocessed from immutable raw sources. All five complete output hashes matched their first-run hashes. `reports/isruc_original_determinism_audit.csv` contains exactly five PASS rows.

## 26. ISRUC Viability

QUESTIONABLE.

The official original provider removes the demonstrated NEMAR truncation mechanism for acquired subjects, and 17 subjects are internally valid. However, the observed 17/100 inclusion rate is not a completed-population viability result: acquisition stopped at the provider quota boundary, and the acquired body-valid population has systematic required-channel variation. The migration must not optimize retention or infer that the remaining 65 subjects would fail. A full viability decision requires resumed official acquisition and re-audit of I036–I100.

## 27. NEMAR vs Original Migration Outcome

Historical NEMAR: expected **100**, included **15**, retention **15.00%**. Current original-provider run: expected **100**, included **17**, retention **17.00%**. Two subjects are currently recovered relative to the old included-ID set: I004 and I005. The comparison is not a claim of final recovery because original acquisition is incomplete and provider/schema causes differ. Current exclusions: 65 acquisition-blocked/unacquired and 18 required-channel schema exclusions. No model metrics were calculated.

## 28. Subjects Recovered

Current original included IDs: I001–I010, I012, I015, I016, I018, I022, I024, and I026. Relative to the historical 15-subject NEMAR included set, the safe recovered-ID set is **I004, I005**. This is provisional until all original subjects are acquired and reconciled.

## 29. Remaining Original-Provider Exclusions

I011, I013–I014, I017, I019–I021, I023, I025, I027–I035 are acquired but excluded for missing required channels. I036 has a partial signal acquisition and is blocked by quota. I037–I100 are unacquired and blocked by the same provider quota. Exact terminal reasons are in the recording, subject, provider-integrity, and acquisition manifests.

## 30. Provider Migration Record

`docs/isruc_provider_migration_record.md` records old provider NEMAR nm000111 v1.0.1, new provider ORIGINAL_ISRUC_MEGA, Step 7.3/7.4 evidence, the partial decision, old/new cohort references, and scientific-contract impact NONE.

## 31. Old Cohort Status

`SUPERSEDED_PENDING_SUCCESSFUL_ORIGINAL_REBUILD`.

The old NEMAR-derived cohort is preserved as historical provenance and is not the active primary rebuilt cohort. It is not labeled fully `SUPERSEDED` because the original-provider migration gate is partial/blocked rather than frozen.

## 32. New ISRUC Cohort Config

File: `configs/isruc_original_cohort_v1.yaml`.

Version: `isruc_original_v1`; status `PARTIAL_ACQUISITION_BANDWIDTH_BLOCKED`; 100 expected, 17 included, 83 excluded. SHA-256: `c2333f7474083756808e3ea5c4fc584a47f937719f7732187a3ca5c6b21cb8b7`.

## 33. Recording Manifest

File: `reports/isruc_original_recording_manifest_v1.csv`.

Rows: **100**. SHA-256: `3f016edba53c9f899868c63c03b7369707b409d159252998ff83a96671159e75`.

## 34. Subject Manifest

File: `reports/isruc_original_subject_manifest_v1.csv`.

Rows: **100**. SHA-256: `7771a9ce5f109a37f26acbd79ab982bec0ee2beb36b387a1e104d328648c635d`.

## 35. Split Feasibility

Assessment only: 17 currently included subjects are not sufficient to freeze credible source train/dev/calibration or held-out cross-domain roles under the project’s subject-level design requirements. The full expected ISRUC population cannot be assessed until acquisition completes. No split IDs, folds, or assignments were generated.

## 36. Accessible-Core Reassessment

Sleep-EDF SC is credible after the Step 7.2 repair: the v1.1 candidate state is 153/153 recordings and 78/78 subjects, with the historical pre-fix 48/153 and 33/78 attrition explained as repaired pipeline failures. ISRUC original-provider state is 17/100 included, with acquisition blocked at the MEGA bandwidth quota and systematic channel exclusions among acquired subjects. Therefore the overall accessible-core gate is **CORE_DATA_BLOCKED**, not frozen or partial: the ISRUC domain remains unresolved at cohort level and the two-domain core cannot support a final freeze.

## 37. Scientific Contract Impact

NONE. The migration changed signal provider/provenance only. Canonical labels, scorer-1 policy, Wake policy, channels, rates, units, epoch length, missingness handling, preprocessing transforms, normalization policy, and eligibility semantics were not changed.

## 38. Tests Added

Added reusable tests in `tests/test_original_isruc.py` covering original bundle resolution, required filenames, and scorer-1 TXT parsing. The adapter implementation is in `src/shiftsleep_uq/data/preprocess.py`; orchestration is `scripts/step_07_5_original_migration.py`. Existing tests were retained.

## 39. Full Validation

Focused adapter tests: **30 passed**.

Final full validation: `pytest -q` returned **48 passed in 2.52s**; `python -m compileall -q src tests scripts` succeeded; `git diff --check` succeeded; exact 100-row checks for expected population, acquisition manifest, provider integrity, bundle audit, recording manifest, subject manifest, and epoch accounting succeeded; channel/schema/annotation audits; duplicate and determinism checks; cohort YAML/hash reproduction; raw-ignore and tracked-file checks; and credential scan succeeded. The migration runner itself exited 0 with `expected_subjects=100`, `included=17`, `excluded=83`, `source_epochs=15429`, `valid_epochs=15429`, `accounting_delta=0`, and `determinism_pass=true`.

## 40. Files Created

- `reports/isruc_original_migration_provenance.md`
- `reports/isruc_original_expected_population.csv`
- `reports/isruc_original_acquisition_run.log`
- `reports/isruc_original_bundle_audit.csv`
- `reports/isruc_original_acquisition_manifest.csv`
- `reports/isruc_original_provider_integrity.csv`
- `reports/isruc_original_channel_inventory.csv`
- `reports/isruc_original_schema_variation_audit.csv`
- `reports/isruc_original_schema_variation_summary.csv`
- `reports/isruc_original_annotation_audit.csv`
- `reports/isruc_original_recording_manifest_v1.csv`
- `reports/isruc_original_subject_manifest_v1.csv`
- `reports/isruc_original_epoch_accounting.csv`
- `reports/isruc_original_stage_distribution.csv`
- `reports/isruc_original_signal_qc.csv`
- `reports/isruc_original_duration_alignment.csv`
- `reports/isruc_original_duplicate_audit.csv`
- `reports/isruc_original_determinism_audit.csv`
- `reports/isruc_provider_migration_outcome.csv`
- `reports/isruc_original_cohort_hashes.txt`
- `docs/isruc_provider_migration_record.md`
- `configs/isruc_original_cohort_v1.yaml`
- `tests/test_original_isruc.py`
- `scripts/step_07_5_original_migration.py`
- `reports/STEP_07_5_ISRUC_ORIGINAL_MIGRATION_REPORT.md`

## 41. Files Modified

- `src/shiftsleep_uq/data/preprocess.py` — reusable original-provider bundle/scorer-1 resolution functions were added; scientific transforms were not changed.
- No frozen scientific contract or preprocessing configuration was modified.

## 42. Explicitly Not Done

- No splits.
- No models.
- No training.
- No normalization or normalization-parameter fitting.
- No ML metrics.
- No calibration.
- No SHHS bypass or unauthorized SHHS access.
- No raw or processed data committed.
- No push to GitHub.
- No NEMAR/original provider mixing in the rebuilt primary outputs.

## 43. Remaining Accessible-Core Issues

The exact remaining issue is completion of official original-provider ISRUC acquisition after the MEGA bandwidth quota resets, followed by validation of I036–I100 and reassessment of systematic channel/schema exclusions. Until that action is complete, ISRUC cannot support a frozen two-domain accessible core.

## 44. Remaining Final-Benchmark Issues

SHHS remains separate. Raw access is pending and the final benchmark is not frozen. No SHHS data were used or bypassed.

## 45. Recommended Next Step

Perform exactly one repair step: **resume the official account-free MEGA acquisition after the provider’s stated bandwidth-quota reset, beginning with I036’s preserved resumable transfer, then acquire I037–I100 with the same bounded manifest/retry protocol and rerun the original-provider audit.** Do not execute splits, modeling, calibration, or final-benchmark work before this repair and gate reassessment.

## 46. Git Status / Diff Summary

Step 7.5 artifacts and migration code are committed with subject `research: record ISRUC migration blocker`. Raw original files, `.getxfer` temporary data, and processed arrays are ignored and were not committed. `git diff --check` passed after the final documentation correction, the working tree is clean, and no push was performed.
