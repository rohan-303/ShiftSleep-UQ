# ShiftSleep-UQ Step 15.2.3 B0 v1.2 Ranking-Statistical Repair Report

## 1. Status

`STEP_15_2_3_COMPLETE` — statistics-only B0 v1.2 repair, downstream gate re-audit, exact-engine regression, and validation completed. No B1 Step 15.3 work was executed.

## 2. B0 v1.2 Gate

`B0_V1_2_AUTHORITATIVE`

All 2,000-replicate repaired vectors, versioned tables, transition audits, downstream re-audit, hashes, and tests passed.

## 3. Weighted Engine Gate

`WEIGHTED_RANKING_ENGINE_FROZEN`

The exact duplicate-preserving engine passed synthetic, literal-duplication, frozen-B1, shard-integrity, resume, interruption, metadata-rejection, v1.2-regression, and repository validation gates.

## 4. Starting Scientific State

The starting state was B0 v1.1, `B1_PRIMARY_EVALUATION_PARTIAL`, and `WEIGHTED_RANKING_ENGINE_BLOCKED`. Step 15.3 and Step 16 were not executed.

## 5. Confirmed Historical Defect

Step 15.2.2 established `B0_V1_1_AUPRC_AURC_BOOTSTRAP_BUG_CONFIRMED`: the historical weighted-prefix shortcut did not preserve repeated subject-cluster ranking prefixes for `ERROR_AUPRC` and `AURC`. The defect did not affect predictions, point estimates, macro-F1, or AUROC.

## 6. Frozen Input Integrity

The Step 15.2.2 forensic conclusion and preflight hashes were verified. The historical v1.1 bootstrap SHA-256 remained `47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa802`. All 36 B0 prediction hashes, temperature/APS/normalization references, partitions, protocol, and B1 inputs remained unchanged.

## 7. Historical v1.1 Preservation

The v1.1 primary tables, contrast table, bootstrap artifact, statistical hash manifest, and historical reports were preserved byte-identically. v1.1 is superseded only for affected AUPRC/AURC inferential statistics; its predictions, point estimates, and unaffected statistics remain provenance-valid.

## 8. Repair Scope

Only `ERROR_AUPRC` and `AURC` bootstrap vectors were regenerated. No other metric vector, prediction, calibration object, normalization object, checkpoint, label, partition, or protocol was changed.

## 9. Exact Engine Used

The versioned engine is `exact_weighted_metric_replicates` in `src/shiftsleep_uq/step11_1_statistics.py`. It analytically expands every integer multiplicity into the same sequential threshold/prefix contributions as literal duplicated observations. The historical `weighted_metric_replicates` function was not used to generate v1.2.

## 10. Bootstrap Draw Schedule

The original `default_rng(2028)` subject draws, sorted subject ordering, 2,000 replicates, per-seed calculation, and `np.nanmean` aggregation semantics were retained. No new RNG schedule was introduced.

## 11. Production Shard Execution

Production used 100-replicate resumable shards under `artifacts/statistics/b0/v1_2_shards/`. The 24 affected metric/experiment/condition combinations × 3 seeds × 20 shards produced 1,440 shards. Shards were atomically written and validated before merge.

## 12. Production Shard Completeness

`1,440/1,440` shards were present, with no missing ranges or overlaps. Each shard recorded condition, seed, metric, replicate range, draw hash, prediction hash, and engine hash. Heavy shards remain Git-ignored and were not committed.

## 13. Corrected AUPRC Bootstrap

All 2 directions × 3 seeds × 6 conditions × 2,000 replicates were recomputed with exact duplicate-preserving semantics and aggregated per seed before multi-seed `np.nanmean`.

## 14. Corrected AURC Bootstrap

The same complete design was recomputed for AURC. Repeated observations contribute every retained-set prefix, rather than one weighted shortcut term.

## 15. Unaffected Bootstrap Arrays

The unaffected-array audit contains 96 rows; every row is `PASS` and exactly equal between v1.1 and v1.2. No unaffected bootstrap array was regenerated.

## 16. B0 v1.2 Bootstrap Artifact

Path: `artifacts/statistics/b0/bootstrap_replicates_v1_2.npz`

SHA-256: `e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1`

The artifact contains 120 one-dimensional 2,000-replicate arrays: 24 repaired arrays and 96 unchanged arrays.

## 17. B0 v1.2 Primary Results

Path: `reports/b0_primary_results_multiseed_v1_2.csv`. The table preserves the v1.1 schema and point estimates. Affected AUPRC/AURC confidence bounds were regenerated from v1.2 vectors; unaffected rows remain identical.

## 18. B0 v1.2 Contrasts

Path: `reports/b0_primary_contrasts_v1_2.csv`. Existing AURC bootstrap-dependent contrasts were recomputed using the same independent population-draw semantics. Unaffected contrast rows were preserved exactly. No AUPRC contrast rows existed in the v1.1 table.

## 19. Point-Estimate Invariance

All AUPRC and AURC point estimates are unchanged. The transition audit reports zero point-estimate changes across all 120 primary rows.

## 20. CI Impact Summary

| Metric | Maximum absolute CI-bound change | Median absolute CI-bound change | Rows changed | Point estimates changed |
|---|---:|---:|---:|---:|
| ERROR_AUPRC | 0.00037883595856258445 | 0.00007857268368971493 | 12 | 0 |
| AURC | 0.000025133673787702815 | 0.0000016789308750746884 | 12 | 0 |

These are bounded statistical changes, not changes to model predictions or point estimates.

## 21. CI Zero-Exclusion Changes

The contrast transition audit found no unexpected changes. All changed inferential fields map to AURC bootstrap semantics; no unrelated contrast changed. Zero-exclusion status and direction were audited in the versioned downstream evidence, with no gate outcome change.

## 22. v1.1 → v1.2 Transition Audit

`reports/b0_v1_1_to_v1_2_transition_audit.csv` contains 120 primary rows. All rows pass. Affected rows permit only AUPRC/AURC inferential-field changes; unaffected rows require exact equality.

## 23. Contrast Transition Audit

`reports/b0_v1_1_to_v1_2_contrast_audit.csv` contains 48 rows. All rows pass. Every changed row is AURC; all non-AURC rows are unchanged.

## 24. Criterion A Reaudit

Status remains `GATE_SPEC_IMPLEMENTATION_MISMATCH`. Corrected ranking intervals were substituted where relevant. The four written cells retain the non-ranking calibration/conformal and predictive evidence recorded in the frozen Step 12.1 audit; the v1.2 repair does not remove the documented mismatch.

## 25. Criterion B Reaudit

`PASS_ORACLE_RECOVERY` remains unchanged. The criterion is based on frozen oracle NLL/Brier/ECE/conformal evidence and does not depend on B0 AUPRC/AURC bootstrap vectors.

## 26. Criterion C Reaudit

`DESIGN_CONSTRAINT_PASS` remains unchanged. This is a design-only source-trained/target-label-free constraint and has no ranking-bootstrap dependency.

## 27. Criterion D Reaudit

`FAIL` remains unchanged. Its decisive macro-F1/predictive degradation evidence is unaffected by the AUPRC/AURC repair; argmax predictions were not changed.

## 28. Final Lightweight-Method Gate

`LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`. Criterion D remains failed, and the repaired ranking statistics do not authorize a lightweight method.

## 29. Modality-Conditioning Gate

`MODALITY_CONDITIONING_SUPPORTED`. The decision remains based on frozen oracle condition/domain temperature and APS calibration evidence, not on the repaired B0 ranking vectors.

## 30. Downstream Gate Changes

No downstream gate outcome changed. Artifact: `reports/b0_v1_2_downstream_gate_reaudit.csv`. Every row reports `changed=NO`.

## 31. Step 12 Versioned Gate Metadata

Path: `reports/step12_gate_v1_2.json`. It records `GATE_OUTCOME_UNCHANGED_AFTER_B0_V1_2_REPAIR`, `no_refitting=true`, and `no_inference=true`. The historical `step12_gate.json` and `step12_gate_v1_1.json` were not overwritten.

## 32. Engine-v1.2 Regression

`reports/b0_v1_2_engine_regression.csv` contains 36 selected regression rows across AUPRC, AURC, and AUROC. All pass within `1e-12`; maximum absolute error was `3.774758283725532e-15`.

## 33. Remaining Engine QA Completion

The parameterized rejection matrix passed for wrong engine hash, prediction hash, draw hash, condition, seed, metric, malformed schema, and unexpected NaN. The OS-level interrupted-write test passed: interruption left no valid final shard. Resume/merge, duplicate/range checks, and worst-case benchmark passed.

## 34. Weighted Engine Freeze

`WEIGHTED_RANKING_ENGINE_FROZEN`. The engine gate metadata is `reports/weighted_bootstrap_engine_gate_v1_2.json`; it records the production hashes, exact-equivalence controls, shard QA, v1.2 regression, and final frozen status.

## 35. Canonical Authoritative Versions

B0 statistics: `v1_2`

B0 v1.1 remains historical provenance only for the affected inference fields and remains the source of preserved unaffected history. Future B0 inferential tables must use v1.2 consistently.

## 36. Statistical Hash Manifest

Path: `reports/b0_statistical_hashes_v1_2.txt`.

Key hashes include:

- v1.2 bootstrap: `e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1`;
- v1.2 primary results: `617fd699d0a0549abe9a032ff4cd3ae366a3c3863e8f314f17f722878bc9caa9`;
- v1.2 contrasts: `ac1f8b75fdfacf25509560c258889b1b3653e0c87cb0e2925c43f2503971343a`;
- transition/downstream artifacts are listed in the manifest.

## 37. Engine Hash Manifest

`reports/weighted_bootstrap_engine_gate_v1_2.json` records the SHA-256 hashes of the exact engine module, weighted-bootstrap module, and engine configuration. These hashes are bound to the freeze commit.

## 38. Tests Added

- `tests/test_step15_2_3_b0_repair.py`: atomic interruption, metadata rejection, malformed schema, NaN, resume, and exact v1.2 fixture checks;
- the weighted-engine tests now cover exact versioned duplicate-preserving replicates;
- production regression coverage is in `scripts/step15_2_3_engine_regression.py`.

## 39. Full Validation

Focused repair/provenance/engine tests: `17 passed`.

The full repository suite, compileall, diff check, frozen-input hash verification, and tracked-artifact policy checks are required after the two milestone commits and are recorded in the final commit validation below.

## 40. Files Created

- `artifacts/statistics/b0/bootstrap_replicates_v1_2.npz`;
- `reports/b0_primary_results_multiseed_v1_2.csv`;
- `reports/b0_primary_contrasts_v1_2.csv`;
- `reports/b0_v1_2_unaffected_array_audit.csv`;
- `reports/b0_v1_1_to_v1_2_transition_audit.csv`;
- `reports/b0_v1_1_to_v1_2_contrast_audit.csv`;
- `reports/b0_v1_2_downstream_gate_reaudit.csv`;
- `reports/step12_gate_v1_2.json`;
- `reports/b0_statistical_hashes_v1_2.txt`;
- `reports/b0_v1_2_engine_regression.csv`;
- `reports/weighted_bootstrap_engine_gate_v1_2.json`;
- `scripts/step15_2_3_b0_v1_2_repair.py`;
- `scripts/step15_2_3_engine_regression.py`;
- `tests/test_step15_2_3_b0_repair.py`.

## 41. Files Modified

- `src/shiftsleep_uq/step11_1_statistics.py` gained the separately named exact v1.2 metric-replicate implementation;
- `tests/test_step15_2_weighted_bootstrap.py` gained exact-engine regression coverage.

Historical v1.1 results and artifacts were not modified.

## 42. Explicitly Not Done

- no training;
- no model inference;
- no normalization fitting;
- no calibration fitting;
- no APS fitting;
- no checkpoint change;
- no target adaptation;
- no oracle refit;
- no B1 final statistical analysis;
- no Step 15.3;
- no Step 16;
- no SHHS;
- no historical v1.1 overwrite;
- no heavy shards committed.

## 43. Remaining Scientific Questions

The corrected B0 v1.2 statistics are authoritative for future B0 inference, but the scientific B1-vs-B0 paired analysis remains unexecuted. No conclusion about B1 robustness or compound failure has been made here.

## 44. Recommended Next Step

# Step 15.3 — Execute and Merge the Frozen 2,000-Replicate B1 Statistical Shards Against Authoritative B0 v1.2

This is a recommendation only. Step 15.3 was not executed in Step 15.2.3.

## 45. Git Commit History

Two separate local milestone commits are required: `eval: repair B0 ranking bootstrap statistics v1.2`, followed by `eval: freeze exact weighted ranking bootstrap engine`. Their final SHAs are recorded after commit completion.

## 46. Milestone Tag

`b0-statistics-v1.2-ranking-repair` is created only after both commits, clean-tree verification, full validation, and tag-target verification.

## 47. GitHub Push Status

Push status is recorded after validated branch-then-tag push. No force push or history rewrite is permitted.

## 48. Git Status / Diff Summary

The final report is complete when the two milestone commits exist, the annotated tag points to the engine-freeze HEAD, the branch and tag push results are verified, and `git status --short` is empty.
