# ShiftSleep-UQ Step 7.11 ISRUC and Accessible-Core Final Freeze Report

## 1. Status

Step 7.11 completed successfully after the official account-free MEGA quota reset. No personal login, quota bypass, mirror, VPN/proxy, or credential was used.

- ISRUC gate: `ISRUC_ORIGINAL_COHORT_FROZEN`
- Accessible-core gate: `CORE_DATA_FROZEN`
- Final benchmark gate: `NO` (SHHS remains unaccessed)
- Data contract: `1.2.0`
- Preprocessing: `0.1.0`

## 2. ISRUC Cohort Gate

`ISRUC_ORIGINAL_COHORT_FROZEN`

All 100 expected subjects have terminal statuses. The final frozen cohort is `configs/isruc_original_cohort_v3.yaml` with status `ACTIVE_FROZEN`.

## 3. Accessible-Core Gate

`CORE_DATA_FROZEN`

The accessible core is `configs/core_cohort_v2.yaml`. It contains Sleep-EDF SC and the frozen original-provider ISRUC cohort. No split assignments are present.

## 4. Final Benchmark Gate

`NO`. SHHS was not accessed and remains a separate future primary domain.

## 5. Acquisition Completion

I072-I100 were acquired sequentially after quota reset. All 100 primary acquisition-role sets are complete. Each subject has `N.rec`, `N_1.txt`, `N_1.xlsx`, `N_2.txt`, and `N_2.xlsx`. I095 also contains the inventoried extra provider file `95 fernandes.xlsx`; it does not replace or alter a primary role.

## 6. Final Provider Integrity

- Expected subjects: 100
- Complete primary bundles: 100
- Provider-integrity failures: 0
- Body-valid REC files: 100/100
- All validated REC files have `body_delta = 0`
- Scorer-1 annotation audits passing: 100/100
- Acquisition exclusions: 0

## 7. Final Montage Distribution

- `ISRUC_A1A2`: 17 subjects
- `ISRUC_M1M2`: 82 subjects
- Included subjects: 99
- Included recordings: 99
- Included valid epochs: 89,312

Frozen exact pairings remain:

- `C3-A2` + `LOC-A2` -> `ISRUC_A1A2`
- `C3-M2` + `E1-M2` -> `ISRUC_M1M2`

## 8. Unsupported Montage Findings

I040 is the sole unsupported-montage exclusion:

- Status: `EXCLUDED_UNSUPPORTED_MONTAGE`
- Failure code: `UNSUPPORTED_ISRUC_CHANNEL_LAYOUT`
- No repeated third montage family occurred among newly acquired subjects.
- No contract amendment, fallback channel, rereferencing, or fuzzy matching was used.

## 9. Annotation / Alignment Integrity

Scorer 1 remained primary and scorer 2 remained diagnostic. All 100 annotation audits passed. No NEMAR annotation substitution occurred. Alignment and duration artifacts were regenerated under the unchanged contract.

## 10. Epoch Accounting

- Included accounting rows passing: 99/99
- Excluded structural rows: 1
- Accounting delta: 0 for every included subject
- EEG/EOG/label row alignment: passing
- Processed arrays: finite and contract-shaped
- ISRUC valid epochs: 89,312

## 11. Montage QC

Final non-normalized montage-stratified QC was regenerated. The known amplitude-scale difference remains descriptive only; no montage normalization, amplitude rescaling, threshold fitting, or amplitude-based exclusion was performed.

## 12. Duplicate Audit

The final duplicate audit was regenerated across subject IDs, raw REC hashes, scorer-1 hashes, and processed-output hashes. No unexplained cross-subject exact duplicate blocked the freeze.

## 13. Determinism

The required 12-subject panel passed exactly:

- first 5 included A1/A2 subjects;
- first 5 included M1/M2 subjects;
- last 2 newly included subjects: I099 and I100.

All run-1/run-2 output hashes were identical.

## 14. ISRUC Viability

`VIABLE_WITH_EXCLUSIONS`.

The provider is complete, integrity checks pass, the single structural exclusion is transparent and isolated, both frozen montage families are represented, and all included annotations/accounting checks pass.

## 15. Frozen ISRUC Cohort

Created without overwriting v1/v2:

`configs/isruc_original_cohort_v3.yaml`

- Status: `ACTIVE_FROZEN`
- Expected: 100
- Included: 99
- Structural exclusions: 1
- A1/A2: 17
- M1/M2: 82
- Valid epochs: 89,312
- Manifest hash file: `reports/isruc_original_cohort_v3_hashes.txt`

## 16. Historical Supersession

- Historical NEMAR-derived cohort: `SUPERSEDED`
- Original-provider v1 partial cohort: preserved as historical evidence and superseded
- Original-provider v2 partial cohort: preserved as historical evidence and superseded
- Original-provider v3: `ACTIVE_FROZEN`

The migration record was updated at `docs/isruc_provider_migration_record.md`.

## 17. Sleep-EDF Revalidation

Sleep-EDF was not rebuilt. Its existing credible state remains:

- 78 subjects
- 153 recordings
- 414,961 valid epochs
- existing manifest/hash/shape/finite-value checks retained

## 18. Frozen Accessible-Core Population

Created:

`configs/core_cohort_v2.yaml`

Sleep-EDF contributes 78 subjects, 153 recordings, and 414,961 epochs. ISRUC contributes 99 subjects, 99 recordings, and 89,312 epochs, with 17 A1/A2 subjects, 82 M1/M2 subjects, and one structural exclusion.

## 19. Accessible-Core Config / Hash

The core config records data contract `1.2.0`, preprocessing `0.1.0`, the Sleep-EDF manifest hash, the ISRUC v3 manifest hash, and `no_splits_or_models: true`.

## 20. Split Feasibility

The final subject populations appear structurally adequate for later train, development, calibration, held-out-dataset, subject-bootstrap, and montage-sensitivity analyses. No assignments, folds, seeds, or normalization parameters were created.

## 21. Leakage / Target-Free Protections

The target-free protocol, scorer policy, exact montage resolver, preprocessing contract, and no-normalization policy were unchanged. No outcome-based cohort selection or split construction occurred.

## 22. Tests / Validation

- `pytest -q`: **64 passed**
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed
- `git diff --check`: passed
- No raw files tracked
- No processed arrays tracked
- No credentials or private provider data committed
- No GitHub push performed

## 23. Files Created / Modified

Created:

- `configs/isruc_original_cohort_v3.yaml`
- `configs/core_cohort_v2.yaml`
- `reports/isruc_original_cohort_v3_hashes.txt`
- `reports/STEP_07_11_ISRUC_AND_ACCESSIBLE_CORE_FINAL_FREEZE_REPORT.md`

Updated or regenerated:

- final ISRUC v2 manifests and audits
- `reports/isruc_provider_migration_final_outcome.csv`
- `docs/isruc_provider_migration_record.md`
- `scripts/step_07_8_isruc_rebuild.py` for valid extra-file bundle acquisition accounting
- focused ISRUC artifact test for the declared 12-subject determinism panel

## 24. Explicitly Not Done

- no splits
- no model
- no training
- no normalization fitting
- no ML metrics
- no calibration
- no conformal evaluation
- no SHHS access
- no raw/processed data committed
- no push

## 25. Remaining Accessible-Core Issues

`NONE`.

## 26. Remaining Final-Benchmark Issues

SHHS remains unaccessed.

## 27. Recommended Next Step

# Step 8 — Subject-Level Split, Calibration, C0–C5 Evaluation, Seed, and Statistical-Analysis Protocol Freeze

This step is recommended only and was **not executed**.

## 28. Git Status / Diff Summary

The working tree contains the local Step 7.11 freeze artifacts and regenerated reports. Changes are ready for the authorized local commit:

`data: freeze original ISRUC and accessible PSG core`

No remote push is authorized or performed.
