# ShiftSleep-UQ Step 15.2 Exact Weighted Ranking-Bootstrap Engine Report

## 1. Status

`STEP15_2_STATISTICAL_ENGINE_QA_PARTIAL`

Step 15.2 added and exercised a reusable exact weighted-statistics module, focused unit tests, engine configuration, provenance hashes, and a worst-case QA benchmark. Production B1 bootstrap finalization was not executed.

## 2. Engine Gate

`WEIGHTED_RANKING_ENGINE_PARTIAL`

The implementation passes focused synthetic tests and the full repository suite, but the required real-data equivalence matrix, B0 v1.1 numerical regression, atomic shard interruption/resume test, and complete shard merge-validation suite were not completed. Therefore the engine is not promoted to `WEIGHTED_RANKING_ENGINE_FROZEN`.

## 3. Starting Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Starting HEAD: `bf8ce85`
- Branch: `main`
- Step 15: partial
- Step 15.1 gate: `B1_PRIMARY_EVALUATION_PARTIAL`
- Existing B1 calibration, prediction, manifest, and multiplicity artifacts were preserved.
- No reset, hard reset, or deletion of valid partial scientific artifacts was performed.

## 4. Why Step 15.2 Was Required

The earlier statistical finalizers reconstructed large epoch arrays repeatedly for subject-bootstrap ranking metrics. Step 15.2 isolates the reusable weighted-statistics problem from production scientific finalization and establishes exact subject-multiplicity semantics before Step 15.3.

## 5. Frozen Input Integrity

The existing Step 15/15.1 artifacts were reused. No model checkpoints, prediction bundles, calibration objects, normalization artifacts, raw signal files, or B0 authoritative result files were modified.

## 6. Bootstrap Multiplicity Integrity

The existing four-population multiplicity artifact was preserved. The engine accepts integer subject multiplicities and validates nonnegative integer weights through its weighted observation mapping. A separate complete hash/invariant audit of all four frozen populations was not accepted as complete in this step.

## 7. Engine Architecture

Implementation: `src/shiftsleep_uq/statistics/weighted_bootstrap.py`.

The module provides preparation of subject-indexed observations, weighted confusion metrics, additive metrics, conformal metrics, exact weighted ranking metrics, and deterministic shard metadata/validation/merge helpers.

## 8. Exact Weighted Semantics

Each epoch receives the multiplicity of its subject. Thus a subject sampled twice contributes all of its epochs twice. No subject is reduced to one representative epoch.

## 9. Weighted Confusion Metrics

Subject-weighted confusion matrices support accuracy, balanced accuracy, macro-F1, and per-class recall in the fixed five-class order. Zero-support classes use the frozen zero-valued convention.

## 10. Weighted NLL

NLL is accumulated in float64 from weighted epoch contributions and divided by the weighted epoch count.

## 11. Weighted Brier

Brier score is accumulated in float64 from weighted per-epoch squared probability error and divided by weighted epoch count.

## 12. Weighted ECE

ECE uses 15 equal-width confidence bins. Confidence and correctness are aggregated with subject multiplicities before the frozen absolute calibration-gap calculation.

## 13. Weighted Conformal Metrics

Coverage, signed gap, absolute gap, mean prediction-set size, singleton fraction, and empty fraction are computed from weighted conformal-set observations. Signed gap is `nominal - empirical`.

## 14. Exact AUROC

AUROC uses weighted pairwise concordance between error and correct observations, including 0.5 credit for equal uncertainty. Replicates containing only errors or only correct observations return `NaN`, not a fabricated score.

## 15. Exact AUPRC

The implementation uses average precision over the frozen uncertainty ordering. Weighted observations are processed in descending uncertainty order, with cumulative weighted positives and totals. Explicit authoritative B0 v1.1 numerical regression was not completed; this remains a freeze blocker.

## 16. Exact AURC

AURC uses ascending predictive entropy, risk `1 - accuracy`, and the weighted retained-population average. No smoothing or approximate ranking was introduced. The complete Step 11.1 numerical regression was not completed.

## 17. Tie Semantics

AUROC assigns exact 0.5 credit to ties. AUPRC and AURC use deterministic stable observation ordering. The focused tie test passed; the full cross-subject tied-score reference matrix was not completed.

## 18. `[A,A,C]` Regression Results

The focused synthetic duplicate-cluster regression passed for weighted confusion metrics, NLL, Brier, ECE, AUROC, AUPRC, AURC, and conformal calculations where exercised. The optimized results matched literal duplicated-cluster results within `1e-12` in the executed tests.

## 19. Synthetic Random Equivalence

Not fully completed. The focused synthetic suite passed, but the required minimum of 100 random cases per metric family was not executed and therefore is not claimed.

## 20. Real-Data Equivalence

Not fully completed. The required frozen B1 replicate-by-replicate literal duplicated-cluster comparison was not executed and remains a blocker to freezing the engine.

## 21. B0 v1.1 Regression

Not completed. The authoritative B0 v1.1 bootstrap artifact was not overwritten or modified. Required D1 C0/C3 and D2 C0/C3 metric comparisons remain for Step 15.2 completion.

## 22. Numerical Tolerances

Focused equivalence assertions use absolute tolerance `1e-12`. No relaxed tolerance was used to make a failing test pass.

## 23. Shard Design

The module contains deterministic shard metadata, validation, and merge helpers. Production shard identity must include metric, replicate range, prediction hash, draw hash, and engine hash.

## 24. Atomic Shard Writes

An atomic temporary-file-to-final-file writer was not added as a complete production helper in this partial step.

## 25. Shard Validation

Basic metadata validation and overlap rejection are covered by focused tests. Full wrong-hash, missing-range, duplicate-range, finite-value, and sentinel validation remains incomplete.

## 26. Resume / Recovery Test

Not completed. No production shard was interrupted and resumed in this step.

## 27. Merge Validation

The focused merge test rejects duplicate ranges. Complete rejection tests for overlap, missing ranges, wrong engine hash, wrong prediction hash, and wrong draw hash remain outstanding.

## 28. Worst-Case Benchmark Population

Population: D2 ISRUC → Sleep-EDF COMPLETE TARGET, B1 seed 17, C3.

- Epochs: `414961`
- Subjects: `78`
- QA replicates: `100`
- Shard size: `100`
- Workers: `1`

## 29. AUROC Benchmark

Completed 100 QA replicates in approximately `10.12` seconds. Peak memory was not instrumented. Reference absolute error was not computed.

## 30. AUPRC Benchmark

Completed 100 QA replicates in approximately `10.05` seconds. Peak memory was not instrumented. Reference absolute error was not computed.

## 31. AURC Benchmark

Completed 100 QA replicates in approximately `9.97` seconds. Peak memory was not instrumented. Reference absolute error was not computed.

## 32. Memory Behavior

The benchmark completed without an observed process failure, but peak memory was not measured. A formal bounded-memory record is therefore not claimed.

## 33. Selected Production Shard Size

QA benchmark shard size: `100`. A production shard size was not frozen because the engine gate remains partial.

## 34. Engine Config

Path: `configs/weighted_bootstrap_engine_v1.yaml`

Version: `1.0.0`

The config records the subject bootstrap unit, 2,000-replicate protocol, NumPy seed 2028, float64 precision, class order, ranking definitions, tie handling, undefined behavior, tolerance, and ordering policies.

## 35. Engine Hash Manifest

Path: `reports/step15_2_weighted_bootstrap_engine_hashes.txt`.

It hashes the engine config, implementation, Step 15.2 test file, and benchmark CSV.

## 36. Tests Added

Path: `tests/test_step15_2_weighted_bootstrap.py`.

The focused tests cover weighted multiplicity, duplicate-cluster equivalence, additive metrics, ranking metrics, ties/undefined behavior, and basic shard overlap rejection.

## 37. Full Validation

- Focused Step 15.2 tests: `6 passed`
- Full repository tests: `131 passed`
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed
- `git diff --check`: passed

The full repository tests required two existing protocol assertions to recognize authorized post-Step-14/15 frozen B1 prediction and calibration artifacts. Those test-only compatibility changes do not alter scientific calculations.

## 38. Files Created

- `src/shiftsleep_uq/statistics/weighted_bootstrap.py`
- `configs/weighted_bootstrap_engine_v1.yaml`
- `tests/test_step15_2_weighted_bootstrap.py`
- `reports/step15_2_ranking_engine_benchmark.csv`
- `reports/step15_2_weighted_bootstrap_engine_hashes.txt`
- `reports/step15_2_data_access_audit.csv`
- `reports/STEP_15_2_WEIGHTED_RANKING_ENGINE_REPORT.md`

## 39. Files Modified

- `tests/test_step13_b1_protocol.py`
- `tests/test_step14_training.py`

No frozen scientific input artifact was modified.

## 40. Explicitly Not Done

- no training;
- no model inference;
- no normalization fitting;
- no temperature fitting;
- no APS fitting;
- no target fitting;
- no oracle analysis;
- no changed scientific metric;
- no changed bootstrap count;
- no changed bootstrap seed;
- no approximation claimed as production output;
- no reduced population;
- no final B1 confidence intervals;
- no B1-vs-B0 final paired results;
- no compound matrix;
- no interpretation case;
- no Step 16;
- no SHHS;
- no production 2,000-replicate ranking bootstrap;
- no push;
- no tag.

## 41. Engine Freeze Commit

`NONE`

The required freeze conditions were not all met, so no local Step 15.2 freeze commit was created.

## 42. GitHub Push Status

`LOCAL_COMMIT_ONLY`

`NO_PUSH`

## 43. Remaining Work

Complete the real-data literal equivalence matrix, 100-case synthetic random equivalence requirement, B0 v1.1 regression, formal tie tests, atomic shard write/recovery tests, complete shard merge validation, and measured memory validation. Only then can the engine be reconsidered for `WEIGHTED_RANKING_ENGINE_FROZEN`.

## 44. Recommended Next Step

Do not execute Step 15.3 yet. First complete the outstanding Step 15.2 QA blockers listed in Sections 19–27 and rerun full validation. Step 15.3 remains blocked until the engine is frozen.

## 45. Git Status / Diff Summary

The worktree contains the intentional partial Step 15/15.1 artifacts plus the Step 15.2 QA implementation, reports, and test compatibility edits. The worktree was not committed because the engine gate is `WEIGHTED_RANKING_ENGINE_PARTIAL`. No remote state was changed.
