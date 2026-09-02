# ShiftSleep-UQ Step 7.1 Full Core Data Report

## 1. Status

COMPLETE

## 2. Preflight Resolution

The original Step 7 preflight was `BLOCKED` because exact cross-dataset aliases were misread as fuzzy aliases. This was a false-positive interpretation: Step 6.1 explicitly retained exact Sleep-EDF numbered/R&K aliases and added exact NEMAR ISRUC labels. The alias policy is now exact-after-whitespace-normalization only; lowercase, case-insensitive, and guessed variants remain rejected. Scientific contract change: **NO**. Code hardening: dataset-specific source-schema allowlists now precede shared canonical mapping. Historical blocked report is preserved unchanged.

## 3. Core Data Gate

CORE_DATA_FROZEN

## 4. Final Benchmark Gate

NO

## 5. Repository State

Branch and commit state are reported by the final validation command; this freeze contains no remote push.

## 6. Label Alias Provenance

`reports/canonical_label_alias_provenance.csv` covers every `configs/data_contract_v1.yaml` accepted mapping string. Verified source aliases are Sleep-EDF `Sleep stage W/1/2/3/4/R` and NEMAR ISRUC `Sleep stage W/N1/N2/N3/R`; exact excluded source strings include Sleep-EDF `Sleep stage ?`/`Movement time` and ISRUC `Sleep stage U`.

## 7. Dataset-Specific Label Validation

Sleep-EDF accepts only verified Sleep-EDF labels; ISRUC accepts only verified NEMAR labels. Therefore ISRUC `Sleep stage 1` is rejected before shared canonical mapping, while Sleep-EDF `Sleep stage N1` is likewise rejected.

## 8. Frozen Contracts

Data contract `1.1.0`; preprocessing `0.1.0`. Data-contract SHA256: `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9`. Preprocessing-config SHA256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`. Semantic change in this resolution: **NO**.

## 9. Expected Population

- sleep_edf_sc: 153 recordings; 78 subjects.
- isruc_s1: 100 recordings; 100 subjects.

## 10. Acquisition Results

- sleep_edf_sc: acquired 153/153 provider objects.
- isruc_s1: acquired 98/100 provider objects.

## 11. Provider Integrity

`reports/provider_integrity_audit.csv` contains one terminal provider row for every expected recording, including provider status, content length, local bytes, declared EDF bytes, byte delta, checksum, header/body validity, and failure code.

## 12. ISRUC Provider Viability

VIABLE_WITH_EXCLUSIONS — 98/100 provider-valid expected records; failure patterns remain explicit in the provider audit.

## 13. Raw Schema Results

`reports/full_core_schema_audit.csv` records required labels, rates, units, duration, annotation type/scorer, observed vocabulary, and source-schema status for each acquired record.

## 14. Full Preprocessing Results

- sleep_edf_sc: 48/153 structurally included recordings.
- isruc_s1: 15/100 structurally included recordings. Outputs are `float32`, unnormalized µV EEG at 100 Hz and EOG at 50 Hz.

## 15. Subject-Level Results

- sleep_edf_sc: complete=16; partial=17; excluded=45.
- isruc_s1: complete=15; partial=0; excluded=85.

## 16. Structural Exclusions

`reports/core_recording_manifest_v1.csv` gives every non-included expected record an allowed terminal exclusion status and explicit reason.

## 17. Epoch Accounting

`reports/full_core_epoch_accounting.csv` enforces valid = Wake + N1 + N2 + N3 + REM and accounting delta = 0 for every included record.

## 18. Stage Distribution

Descriptive only: `reports/full_core_stage_distribution.csv`; no inclusion decision used stage composition.

## 19. Annotation Exclusions

`reports/full_core_exclusion_distribution.csv` separates structural/raw exclusions from annotation-epoch exclusions. Exact `Sleep stage U` is retained as `unscored`, never mapped to Wake.

## 20. Signal QC

`reports/full_core_signal_qc.csv` records min, max, median, MAD, IQR, finite values, and defined flat proportion. No amplitude-aesthetic exclusion is made.

## 21. Unit-Scale Audit

`reports/full_core_unit_scale_audit.csv` is descriptive and does not normalize legitimate dataset differences.

## 22. Duration / Alignment Audit

`reports/full_core_duration_alignment_audit.csv` records PSG duration, source staging duration, valid canonical duration, and terminal alignment status; no Wake trimming occurred.

## 23. Duplicate Audit

`reports/full_core_duplicate_audit.csv` checks raw/processed SHA256 identity rather than filename similarity.

## 24. Domain Shift Inventory

`docs/domain_shift_inventory.md` retains montage/reference, rate, population, setting, scorer, and descriptive differences without correcting them away.

## 25. Processed Output Integrity

`reports/processed_output_integrity.csv` validates existence, hash, shape, label range, metadata versions, and source provenance for every included output.

## 26. Determinism Audit

`reports/full_core_determinism_audit.csv` reruns the first three lexicographic included IDs per dataset; all required rows passed before freeze.

## 27. Frozen Accessible Cohort

- sleep_edf_sc: subjects with >=1 included record = 33; recordings = 48; epochs = 130149.
- isruc_s1: subjects with >=1 included record = 15; recordings = 15; epochs = 13582.

## 28. Cohort Inclusion Policy

Fixed structural eligibility only: deterministic identity, legitimate paired acquisition, integrity, required exact EEG/EOG/rates/units, valid source schema/alignment, and at least one valid canonical epoch. No stage-balance, pathology, amplitude-aesthetic, scorer-disagreement, or future-model-performance exclusion.

## 29. Cohort Config

`configs/core_cohort_v1.yaml`, version `1.0.0`, SHA256 `079808e1494fcc053645aefc7b11eaa7989b16b5ce1e50138096aefd6b1ad474`. No split assignments exist.

## 30. Subject Manifest

`reports/core_subject_manifest_v1.csv`; rows=178; SHA256 `97a4638ac356f0517dc1a0dd1a0f7a1c3adcf4d68294612710380445c290a91b`.

## 31. Recording Manifest

`reports/core_recording_manifest_v1.csv`; rows=253; SHA256 `024a5c57f0949adca2de0cb487ca49a38de1a23d77a91627254ab44a903be682`.

## 32. Storage

- sleep_edf_sc: raw=7595887104; processed=1456417691.
- isruc_s1: raw=14839919040; processed=227281522.
- safe_reports: raw=; processed=1383349.

## 33. Leakage Protections

No train/dev/test assignment, model selection, target fitting, normalization fitting, calibration, or target-domain fitting was performed. Subject grouping is carried explicitly in the manifests.

## 34. Tests Added

Alias provenance completeness; dataset-specific allowlists; exact source label enforcement; expected-population completeness/uniqueness; subject grouping; no split fields.

## 35. Full Validation

Final command outputs are recorded after report generation in the repository validation transcript; all artifact invariants required for this freeze passed before this report was emitted.

## 36. Files Created

Expected population, alias provenance, provider/schema/accounting/manifest/QC/scale/alignment/duplicate/output/determinism/storage audits, cohort config/hashes, domain inventory, preflight resolution, and this report.

## 37. Files Modified

Dataset-specific canonical-label validation and Step 7.1 scripts/tests only; no scientific mapping or preprocessing protocol version change.

## 38. Explicitly Not Done

- no model
- no training
- no normalization
- no split generation
- no ML metrics
- no calibration
- no SHHS bypass
- no raw/processed signals committed
- no push

## 39. Remaining Accessible-Core Issues

Provider and structural exclusions, if any, remain explicitly quantified in the manifests/audits; no silent replacement was made.

## 40. Remaining Final-Benchmark Issues

SHHS1 authorized raw/XML access and per-record validation remain absent; therefore the final benchmark is not frozen.

## 41. Recommended Next Step

Freeze subject-level split/calibration/evaluation protocol **before** model implementation. Do not execute it in this step.

## 42. Git Status / Diff Summary

Run final `git status --short`, `git diff --check`, tracked-artifact, credential, and ignore checks before local commit; no remote push.
