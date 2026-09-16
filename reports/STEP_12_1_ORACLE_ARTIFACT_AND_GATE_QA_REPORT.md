# ShiftSleep-UQ Step 12.1 Oracle Artifact and Method-Gate QA Report

## 1. Status

`STEP12_GATE_DECISION_REPAIRED`

Step 12.1 was executed as a read-only integrity and gate-QA step. The original Step 12 v1 artifacts were preserved. One export defect was confirmed and repaired in a versioned artifact namespace. The final lightweight-method decision remains unchanged:

`LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`

## 2. QA Outcome

The QA identified two issues:

1. `b0_oracle_aps_v1.csv` and `b0_oracle_conformal_results_v1.csv` were byte-identical because the Step 12 writer sent the same conformal-results object to both output paths.
2. The Step 12 runner’s Criterion A/B operationalization was narrower than the written authorization criteria. Independent reconstruction found four threshold-qualified oracle-recoverable compound cells, while the original runner’s narrower conjunction reported zero.

The final method gate remains `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED` because the predictive-component criterion fails. No method was implemented and no Step 13 execution occurred.

## 3. Frozen Input Integrity

Repository identity and frozen inputs were verified:

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Step 12 commit: `7d41e4c` (`research: diagnose B0 failures and oracle bounds`)
- Working tree was clean before Step 12.1 additions.
- Primary result SHA-256: `288122138f1b29c4b3ac8ca3de6e4f38baf97e20eefeaa15d029116337543efc`
- Primary contrast SHA-256: `008a9ad350c15f69d633a24ae584f3ace974b42a37a5a57b1df9e4429bbd4b4d`
- Corrected bootstrap SHA-256: `47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022`
- Prediction manifest SHA-256: `77422f9aa4a0d7ba359268a1914e316e567da13fed3ad242c3100cef43408af7`
- Oracle partition SHA-256: `835344bcbd1992b00ec309082317d7f08a0b7f5f6c8d401ee670627d6bd806de`

All authoritative frozen hashes reproduced. No frozen upstream artifact differed.

## 4. Oracle APS Artifact Hash

Original artifact:

- Path: `reports/b0_oracle_aps_v1.csv`
- Bytes: `20,998`
- Rows: `108`
- Columns: `experiment_id`, `seed`, `condition`, `variant`, `alpha`, `qhat`, `empirical_coverage`, `signed_coverage_gap`, `absolute_coverage_error`, `mean_set_size`, `median_set_size`, `singleton_fraction`, `analysis_scope`
- SHA-256: `cfe82bc68f917efa07e8b7f6165d23dbb37a838572082c8584604620337a32ea`

The original file is an evaluation-results table, not a distinct APS calibration-object table.

Versioned repaired artifact:

- Path: `reports/b0_oracle_aps_v1_1.csv`
- Bytes: `7,147`
- Rows: `48`
- Columns: `experiment_id`, `seed`, `fit_scope`, `fit_condition`, `alpha`, `qhat`, `calibration_role`, `calibration_subject_count`, `calibration_epoch_count`, `fit_type`, `analysis_scope`
- SHA-256: `0dd422dc0d908c823a06bdf89eeac958e89b93d2ecde4627619243284f63bb41`

The repaired v1.1 artifact was deterministically reconstructed from frozen q-hat rows, the oracle partition, and frozen prediction-bundle metadata. No APS fitting was performed.

## 5. Oracle Conformal Result Artifact Hash

- Path: `reports/b0_oracle_conformal_results_v1.csv`
- Bytes: `20,998`
- Rows: `108`
- Columns: `experiment_id`, `seed`, `condition`, `variant`, `alpha`, `qhat`, `empirical_coverage`, `signed_coverage_gap`, `absolute_coverage_error`, `mean_set_size`, `median_set_size`, `singleton_fraction`, `analysis_scope`
- SHA-256: `cfe82bc68f917efa07e8b7f6165d23dbb37a838572082c8584604620337a32ea`

This file is the valid conformal evaluation-results table. Its v1 bytes were preserved unchanged.

## 6. Duplicate-Content Audit

The two Step 12 oracle files are `BYTE_IDENTICAL`.

Duplicate hash:

`cfe82bc68f917efa07e8b7f6165d23dbb37a838572082c8584604620337a32ea`

The all-report CSV audit found:

- suspicious Step 12 duplicate: `b0_oracle_aps_v1.csv` and `b0_oracle_conformal_results_v1.csv`;
- legitimate pre-existing manifest duplicates outside Step 12: `core_recording_manifest_v1.csv` / `core_recording_manifest_v1_step_07_1.csv`, and `core_subject_manifest_v1.csv` / `core_subject_manifest_v1_step_07_1.csv`.

The Step 12 duplicate is an export defect, not a hash collision.

## 7. Diagnostic Hash Manifest Audit

All 14 artifacts listed in `reports/b0_diagnostic_hashes_v1.txt` exist, are nonempty, readable, and match their expected hashes.

Machine-readable audit:

`reports/step12_1_artifact_integrity_audit.csv`

SHA-256:

`b637be3685711f994ce231fe71814f94a69810399d26cc2edfa56943d7e4b339`

The two duplicate v1 oracle rows are explicitly marked `UNEXPECTED_DUPLICATE_CONTENT`; other rows pass normally.

## 8. Report Hash Audit

Every hash printed in the original Step 12 report was compared with the corresponding file on disk.

Result:

`PASS — no report-only transcription errors detected.`

The original Step 12 report remains historical and was not overwritten.

## 9. Oracle Temperature Artifact Integrity

`reports/b0_oracle_temperature_v1.csv` contains 6 `ORACLE_DOMAIN_TEMPERATURE` rows, 18 `ORACLE_CONDITION_TEMPERATURE` rows, and 24 total fit rows.

All temperatures are positive and finite. Every final oracle-calibration NLL is less than or equal to its initial NLL within tolerance. No temperature was refit during Step 12.1.

## 10. Oracle APS Reference Integrity

The repaired APS artifact contains 48 frozen q-hat records:

- domain-scope APS: one C3-fit q-hat per direction × seed × alpha;
- condition-specific APS: one matching-condition q-hat per direction × seed × condition × alpha.

For every fit scope, `qhat(alpha=0.05) >= qhat(alpha=0.10)`. The table records `ORACLE_CALIBRATION` and `analysis_scope = ORACLE_TARGET_UPPER_BOUND`.

No q-hat was recalculated, refit, or selected using evaluation outcomes.

## 11. Oracle Population Integrity

All 18 direction × seed × C3/C4/C5 bundles were independently checked.

For every bundle:

- `ORACLE_CALIBRATION` and `ORACLE_EVALUATION` subject sets are disjoint;
- their union equals the complete target subject population;
- subject roles are complete and valid;
- no evaluation subject is used for fitting;
- no calibration subject is used as an evaluation-only subject.

Result: `PASS — 18 oracle bundles.`

## 12. Criterion A Independent Audit

The four compound cells were evaluated:

| Cell | Macro-F1 delta | NLL delta | Brier delta | ECE delta | Error AUROC delta | Error AUPRC delta | AURC delta | Signed gap delta | Written reliability flag | Original implemented flag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| D1 C4 | -0.156968 | +0.837095 | +0.413512 | +0.115032 | -0.235247 | +0.025722 | +0.243674 | +0.019954 | `True` | `False` |
| D1 C5 | -0.176711 | +1.047115 | +0.493702 | +0.221644 | -0.254837 | +0.170035 | +0.508597 | +0.055312 | `True` | `False` |
| D2 C4 | -0.263972 | +0.811242 | +0.252268 | +0.145952 | -0.071185 | +0.096637 | +0.189203 | +0.109527 | `True` | `False` |
| D2 C5 | -0.124351 | +0.072572 | +0.078442 | +0.121425 | -0.086165 | -0.012329 | +0.127720 | +0.050325 | `True` | `False` |

The original implementation operationalized Criterion A as source-temperature worsening beyond metric tolerance. None of the four cells had source-temperature worsening; source temperature improved all four cells descriptively.

The written Criterion A allows calibration, ranking/selective, or conformal degradation beyond predictive degradation. All four cells show reliability evidence in addition to large macro-F1 deterioration.

Result:

`GATE_SPEC_IMPLEMENTATION_MISMATCH`

## 13. Criterion B Independent Audit

Oracle condition-minus-source results:

| Cell | NLL delta | NLL CI | NLL pass | Brier delta | Brier CI | Brier pass | ECE delta | ECE CI | ECE pass |
|---|---:|---|---|---:|---|---|---:|---|---|
| D1 C4 | -0.025516 | [-0.038511, -0.013904] | `True` | -0.007711 | [-0.011852, -0.003937] | `True` | -0.052198 | [-0.058028, -0.031561] | `True` |
| D1 C5 | -0.155845 | [-0.193348, -0.121664] | `True` | -0.069513 | [-0.081329, -0.058598] | `True` | -0.154935 | [-0.159349, -0.140676] | `True` |
| D2 C4 | -0.198367 | [-0.284461, -0.112683] | `True` | -0.010400 | [-0.031106, +0.010984] | `False` | -0.018004 | [-0.071881, +0.038980] | `True` |
| D2 C5 | -0.043495 | [-0.066785, -0.024568] | `True` | -0.028658 | [-0.033394, -0.023847] | `True` | -0.053178 | [-0.064168, -0.042264] | `True` |

Thresholds were applied exactly:

- NLL: relative reduction at least 5% OR 95% CI entirely below zero;
- Brier: relative reduction at least 3% OR 95% CI entirely below zero;
- ECE: absolute reduction at least 0.01 OR 95% CI entirely below zero.

Oracle conformal evidence was also checked. Absolute-error improvement and mean-set-size changes were:

| Cell | Alpha | Absolute-error improvement | Mean set-size change | Pathological inflation | Pass |
|---|---:|---:|---:|---|---|
| D1 C4 | 0.10 | +0.063356 | -1.275330 | `False` | `True` |
| D1 C4 | 0.05 | +0.017558 | -0.781997 | `False` | `True` |
| D1 C5 | 0.10 | +0.029185 | -0.528712 | `False` | `True` |
| D1 C5 | 0.05 | -0.002056 | -0.053091 | `False` | `False` |
| D2 C4 | 0.10 | -0.025260 | +1.806383 | `False` under the declared rule | `False` |
| D2 C4 | 0.05 | +0.037109 | +1.493842 | `False` under the declared rule | `True` |
| D2 C5 | 0.10 | +0.029203 | -0.263093 | `False` | `True` |
| D2 C5 | 0.05 | +0.016495 | -0.208800 | `False` | `True` |

The declared pathological rule is mean set-size increase greater than 1.0 **and** absolute-error improvement less than 0.02. D2 C4 alpha 0.05 is therefore not pathological because improvement exceeds 0.02.

Each compound cell has at least one meaningful NLL/Brier/ECE or conformal recovery signal.

## 14. Recoverable Compound Cell Count

Independent written-criteria result:

`RECOVERABLE_COMPOUND_CELLS = 4`

Cells:

- D1 C4
- D1 C5
- D2 C4
- D2 C5

The original Step 12 runner reported zero because it required the narrower conjunction:

`source-temperature-worsening AND oracle-improvement`

That conjunction is not equivalent to the written Criterion A/B requirements. This is the recorded `GATE_SPEC_IMPLEMENTATION_MISMATCH`.

## 15. Criterion C Independent Audit

Criterion C passes as a design constraint only. A future candidate can remain source-trained, frozen before target evaluation, target-label-free, target-normalization-free, and target-threshold-free.

This is feasibility evidence only and does not authorize implementation or imply efficacy.

## 16. Criterion D Independent Audit

Criterion D fails for authorization as a primary next intervention.

All four compound cells show substantial negative macro-F1 transfer:

- D1 C4: -0.156968
- D1 C5: -0.176711
- D2 C4: -0.263972
- D2 C5: -0.124351

The same cells show stage/predictive and confusion/ranking evidence. Calibration cannot change argmax predictions and cannot repair these macro-F1 losses. This is a substantial predictive/representation component rather than a calibration-only failure.

## 17. Modality-Conditioning Gate Audit

Condition-specific-minus-domain oracle calibration contrasts were independently checked:

| Cell | NLL delta | Brier delta | ECE delta | Support |
|---|---:|---:|---:|---|
| D1 C4 | -0.002068, CI [-0.007920, +0.004519] | -0.001065, CI [-0.003273, +0.001349] | -0.008182, CI [-0.029656, +0.014510] | `True` by point evidence |
| D1 C5 | -0.037322, CI [-0.051461, -0.024478] | -0.023747, CI [-0.029113, -0.018732] | -0.067651, CI [-0.070490, -0.055415] | `True` |
| D2 C4 | -0.018960, CI [-0.046806, +0.009535] | +0.006798, CI [-0.002633, +0.016535] | +0.030498, CI [+0.004705, +0.050846] | `False` |
| D2 C5 | -0.015269, CI [-0.018506, -0.011764] | +0.000818, CI [-0.000892, +0.002619] | +0.012662, CI [+0.004845, +0.020841] | `False` |

The analogous APS audit supplies the required D2 evidence. D2 C5 condition-specific APS reduces absolute coverage error versus domain-only APS at alpha 0.10 by `0.054556` and at alpha 0.05 by `0.020965`, while mean set size decreases by `0.584288` and `0.349952` classes respectively. D2 C4 alpha 0.05 is not counted because its absolute-error improvement is only `0.002243` while mean set size increases by `1.170449` classes, satisfying the pathological-inflation rule.

The final modality conclusion remains:

`MODALITY_CONDITIONING_SUPPORTED`

This is diagnostic evidence only and does not authorize target-label calibration.

## 18. Failure-Mode Matrix Audit

`reports/b0_failure_mode_matrix_v1.csv` contains six direction × condition rows and uses only the permitted evidence categories. Its descriptive fields are consistent with the source diagnostic and oracle point tables.

The matrix’s oracle recoverability labels are descriptive point-improvement labels. They are not equivalent to the written Criterion B requirement of threshold-qualified recovery in at least two compound cells.

The independent audit table, not stale/manual matrix values, determines the QA gate.

## 19. Root Cause of Duplicate Hash

The Step 12 generator contains:

```python
write_csv(out/"b0_oracle_aps_v1.csv", oracle_conf)
write_csv(out/"b0_oracle_conformal_results_v1.csv", oracle_conf)
```

The same `oracle_conf` object was written to both paths. It contains conformal evaluation rows. Therefore the APS path received the conformal-results object. The duplicate hash is a generation/export defect.

## 20. Repairs Performed

- Created `reports/b0_oracle_aps_v1_1.csv` as a distinct q-hat/calibration-object table.
- Created `reports/b0_diagnostic_hashes_v1_1.txt`.
- Created `reports/step12_gate_v1_1.json`.
- Created `reports/step12_1_artifact_integrity_audit.csv`.
- Created `reports/step12_1_authorization_gate_audit.csv`.
- Added focused Step 12.1 integrity tests.
- Recorded the Criterion A gate-specification/implementation mismatch.
- Preserved all Step 12 v1 artifacts unchanged.

No model outputs, calibrations, APS fits, or primary statistics were regenerated.

## 21. Authoritative Step 12 Artifact Versions After QA

The original Step 12 v1 artifacts remain historical and preserved.

The authoritative Step 12.1 corrected APS artifact is:

`reports/b0_oracle_aps_v1_1.csv`

The authoritative Step 12.1 gate metadata is:

`reports/step12_gate_v1_1.json`

The original primary target-free results remain authoritative as `v1_1`. Step 12.1 does not replace the primary result namespace.

## 22. Final Lightweight-Method Gate

`LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`

The independent audit found four threshold-qualified oracle-recoverable compound cells, but Criterion D fails because the compound-shift failure includes substantial predictive/representation degradation that calibration cannot repair. No method implementation is authorized.

## 23. Final Modality-Conditioning Gate

`MODALITY_CONDITIONING_SUPPORTED`

This remains a diagnostic design implication only. It does not authorize target labels, target calibration fitting, or target adaptation.

## 24. Tests Added

Added:

- `tests/test_step12_1_integrity.py`

The four focused tests verify:

1. duplicate v1 detection and distinct v1.1 APS schema;
2. Step 12.1 manifest path/hash correctness;
3. independent recoverable-cell count and final gate reproduction;
4. oracle temperature and APS reference integrity.

Existing tests were not weakened.

## 25. Full Validation

Fresh validation passed:

- focused Step 12.1 tests: **4 passed**;
- full repository tests: **115 passed in 17.59s**;
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed before Step 12.1 staging;
- Step 11.1 primary hashes: passed;
- prediction manifest hash: passed;
- oracle partition hash: passed;
- Step 12 diagnostic manifest: passed;
- oracle population integrity: passed for 18 bundles;
- oracle temperature integrity: passed for 24 fits;
- oracle APS q-hat ordering: passed for 48 rows.

## 26. Files Created

- `scripts/step12_1_integrity_audit.py`;
- `tests/test_step12_1_integrity.py`;
- `reports/b0_oracle_aps_v1_1.csv`;
- `reports/b0_diagnostic_hashes_v1_1.txt`;
- `reports/step12_gate_v1_1.json`;
- `reports/step12_1_artifact_integrity_audit.csv`;
- `reports/step12_1_authorization_gate_audit.csv`;
- this report.

## 27. Files Modified

No original Step 12 v1 artifact was modified. Step 12.1 added only versioned QA artifacts, the audit script, tests, and this report.

## 28. Explicitly Not Done

The following were not done:

- no training;
- no inference;
- no normalization refit;
- no source calibration refit;
- no oracle temperature refit;
- no oracle APS refit;
- no target adaptation;
- no new method;
- no SHHS;
- no raw PSG rereading;
- no oracle partition change;
- no primary result rewrite;
- no Step 13;
- no remote push.

## 29. Recommended Next Step

Because the final lightweight-method gate remains `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`, recommend exactly:

# Step 13 — Preregister the B1 Source-Only Modality-Dropout Robustness Baseline

This extension should keep the B0 architecture unchanged and alter ONLY the source-training modality-exposure policy, allowing the project to test whether predictive and selective failures persist after basic missing-modality robustness training.

Do NOT execute Step 13.

## 30. Git Status / Diff Summary

Step 12.1 additions are committed locally under `research: repair Step 12 oracle artifact integrity`. The prior Step 12 commit remains `7d41e4c`. The final commit hash is recorded by `git log -1` at validation time. No original Step 12 file was modified and no remote push is authorized.
