# ShiftSleep-UQ Step 15.2.1 Weighted Ranking-Engine Freeze Report

## 1. Status

`STEP15_2_1_QA_BLOCKED`

Step 15.2.1 completed the frozen-draw audit, deterministic synthetic equivalence, frozen B1 real-data equivalence, atomic shard QA, resume/merge checks, and measured worst-case benchmark. The engine was not frozen because the required B0 v1.1 numerical regression fails for authoritative AUPRC and AURC values.

## 2. Engine Gate

`WEIGHTED_RANKING_ENGINE_BLOCKED`

The exact engine matches literal duplicate-cluster reconstruction, but the authoritative B0 v1.1 artifact is not numerically reproducible by the corrected exact engine for AUPRC and AURC. The conflict must be resolved before a freeze commit.

## 3. Starting State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Starting HEAD: `bf8ce85`
- Starting scientific gate: `B1_PRIMARY_EVALUATION_PARTIAL`
- Starting engine gate: `WEIGHTED_RANKING_ENGINE_PARTIAL`
- Existing Step 15/15.1/15.2 artifacts were preserved.
- No hard reset, inference rerun, calibration refit, training rerun, or Step 15.3 execution occurred.

## 4. Frozen Input Integrity

Verified without modification:

- four B1 subject-multiplicity matrices;
- 2,000 rows per matrix;
- B1 draw-hash manifest;
- B0 v1.1 bootstrap artifact;
- B0 v1.1 hash manifest;
- B1 prediction bundles used for the required real-data checks;
- B0 prediction bundles used for regression checks.

Authoritative B0 v1.1 bootstrap SHA-256 remained:

`47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa802`

No frozen scientific input was overwritten.

## 5. Bootstrap Draw Audit

Created:

`reports/step15_2_1_bootstrap_draw_audit.csv`

All four populations passed:

| Population | Subjects | Replicates | Seed | Draw SHA-256 | Status |
|---|---:|---:|---:|---|---|
| D1 Sleep-EDF → ISRUC SOURCE TEST | 11 | 2,000 | 2028 | `968b2c2d1d42a82c308bc12cb9725e8c71ca2d34eefbcc457aa7e283d9a58cd5` | PASS |
| D1 Sleep-EDF → ISRUC COMPLETE TARGET | 99 | 2,000 | 2028 | `8e70f4086d15e2e8405cba95c24fbe5c9471734e69b37459a603a518b777ddc5` | PASS |
| D2 ISRUC → Sleep-EDF SOURCE TEST | 15 | 2,000 | 2028 | `7ae334ec89fbe65e7e73f1233b829dad2a8cd95ebc59115e3ed950c3b1806294` | PASS |
| D2 ISRUC → Sleep-EDF COMPLETE TARGET | 78 | 2,000 | 2028 | `db7b0a002c2474238d26043f89a23a3821db49c4693349e98d78c8fbad1ea109` | PASS |

The audit verified shape, integer dtype, nonnegative multiplicities, row sums, seed provenance, and byte hashes. Subject ordering was verified through the frozen prediction-bundle subject ordering used by the real-data equivalence runner.

## 6. Authoritative AUPRC Definition

The authoritative implementation is:

`src/shiftsleep_uq/evaluation_step11.py:auprc`

It:

- converts labels to integer error labels;
- returns `NaN` when there are no positive errors;
- sorts descending uncertainty with `np.argsort(-scores, kind="stable")`;
- computes cumulative true positives and false positives;
- computes precision and recall at each observation;
- returns `sum((recall[1:] - recall[:-1]) * precision[1:])` for more than one observation;
- returns the final precision for a one-observation input.

Therefore the frozen convention is the repository's average-precision-style step calculation, including its omission of the first recall increment. It is not trapezoidal PR-AUC.

## 7. AUPRC Tie Semantics

The authoritative implementation is stable observation-order based, not threshold-group invariant. Equal uncertainty values retain their original observation order. A subject duplicated multiple times contributes repeated observations in that order.

The corrected weighted engine reproduces this exact behavior, including the authoritative omission of the first recall increment. The duplicate-cluster tests and B1 real-data equivalence checks passed within `1e-12`.

## 8. Authoritative AUROC Definition

The authoritative implementation is `_rank_auc` in `src/shiftsleep_uq/evaluation_step11.py`.

- Positive class: `ERROR = 1`.
- Scores: predictive entropy.
- Sorting: ascending score, stable ordering.
- Ties: stable ordering, not explicit 0.5 threshold grouping.
- Undefined single-class populations: `NaN`.

The weighted engine now uses exact stable duplicate ordering. Its weighted rank-sum formula matches literal duplicated observations, including repeated observations within one subject.

## 9. Authoritative AURC Definition

The authoritative implementation is `aurc` in `src/shiftsleep_uq/evaluation_step11.py`.

- Sort uncertainty ascending.
- Define risk after each retained observation as cumulative error divided by retained count.
- Return the unweighted mean of the per-observation prefix risks.
- No smoothing is applied.

The weighted engine uses the exact harmonic closed form for repeated observations. This reproduces literal duplicated observations within `1e-12` in synthetic and B1 real-data checks.

## 10. `[A,A,C]` Regression

The explicit duplicate-cluster regression remained in:

`tests/test_step15_2_weighted_bootstrap.py`

It covers weighted confusion, NLL, Brier, ECE, AUROC, AUPRC, AURC, and conformal metrics. The optimized result for `A+A+C` matched literal expansion within `1e-12`. The test also retains the multiplicity-sensitive fixture rather than replacing it with only identity sampling.

## 11. 100-Case Synthetic Random Equivalence

Created:

`reports/step15_2_1_synthetic_equivalence.csv`

Every metric family completed 100 deterministic random cases. Multiplicities included zero, one, and values greater than one.

| Metric | Cases | Maximum absolute error | Mean absolute error | Failures | Status |
|---|---:|---:|---:|---:|---|
| macro-F1 | 100 | 0.0 | 0.0 | 0 | PASS |
| NLL | 100 | `8.881784197001252e-16` | machine-roundoff | 0 | PASS |
| Brier | 100 | `4.440892098500626e-16` | machine-roundoff | 0 | PASS |
| ECE | 100 | `1.1102230246251565e-16` | machine-roundoff | 0 | PASS |
| ERROR_AUROC | 100 | 0.0 | 0.0 | 0 | PASS |
| ERROR_AUPRC | 100 | `5.551115123125783e-16` | machine-roundoff | 0 | PASS |
| AURC | 100 | `4.440892098500626e-16` | machine-roundoff | 0 | PASS |
| conformal coverage | 100 | 0.0 | 0.0 | 0 | PASS |
| signed coverage gap | 100 | 0.0 | 0.0 | 0 | PASS |
| mean set size | 100 | 0.0 | 0.0 | 0 | PASS |

## 12. D1 Source-Test Real Equivalence

B1 D1 seed 17 C0 was compared against literal duplicated-subject expansion for 20 frozen replicates. The comparison covered macro-F1, NLL, Brier, ECE, AUROC, AUPRC, AURC, conformal coverage, and mean set size.

- Rows: 180
- Failures: 0
- Maximum absolute error: `0.0` within recorded floating-point precision
- Status: PASS

## 13. D2 Source-Test Real Equivalence

B1 D2 seed 17 C0 was compared for 20 frozen replicates using the same metric set.

- Rows: 180
- Failures: 0
- Status: PASS

## 14. D1 Target Real Equivalence

B1 D1 seed 17 C3 was compared for 10 frozen replicates. Ranking metrics and additive/confusion/conformal spot checks were included.

- Rows: 90
- Failures: 0
- Status: PASS

## 15. D2 Target Real Equivalence

B1 D2 seed 17 C3 was compared for 10 frozen replicates. Ranking metrics and additive/confusion/conformal spot checks were included.

- Rows: 90
- Failures: 0
- Status: PASS

Combined real-equivalence artifact:

`reports/step15_2_1_real_equivalence.csv`

The required B1 cases were all covered:

- D1 seed17 C0;
- D1 seed17 C3;
- D2 seed17 C0;
- D2 seed17 C3.

## 16. B0 v1.1 Numerical Regression

Created:

`reports/step15_2_1_b0_v1_1_regression.csv`

The required B0 artifact schema was verified. All requested metrics were present for D1/D2 C0/C3.

Results:

- macro-F1: PASS;
- ERROR_AUROC: PASS;
- ERROR_AUPRC: FAIL;
- AURC: FAIL.

The B0 v1.1 artifact is reproduced by the pre-existing Step 11.1 weighted-reference path for AUPRC and AURC, but not by the corrected exact literal-equivalent engine. The corrected engine is intentionally required to agree with physical duplicate-cluster reconstruction. The discrepancy is therefore a provenance/semantic conflict between the frozen B0 v1.1 outputs and the exact duplicate-preserving ranking semantics.

Representative maximum absolute errors against B0 v1.1 were:

- ERROR_AUPRC: approximately `8.067934931126342e-04`;
- AURC: approximately `1.6389021747414967e-05`.

These exceed both `1e-12` and the permitted `1e-10` reduction-order allowance.

No B0 artifact was changed.

## 17. Final Numerical Tolerances

- Default exact-equivalence tolerance: `1e-12`.
- Permitted reduction-order allowance: `1e-10` only with explicit justification.
- Synthetic and B1 real-data equivalence passed within the default tolerance.
- B0 AUPRC/AURC regression failed beyond the permitted tolerance.

## 18. AUPRC Repair

AUPRC repair was required and implemented in:

`src/shiftsleep_uq/statistics/weighted_bootstrap.py`

The prior implementation incorrectly used an observation-group formula that did not exactly reproduce repeated positive observations and initially used the wrong score direction. The correction:

- uses descending uncertainty for AUPRC;
- processes repeated observations exactly;
- retains stable order;
- omits the first recall increment exactly as the authoritative Step 11.1 function does.

The correction changes only the engine's post-processing implementation; it does not change the scientific metric contract or bootstrap count.

## 19. Atomic Shard Writer

Implemented:

- `atomic_write_shard`;
- `read_shard`;
- `validate_shard_file`.

The writer creates a temporary file in the destination directory, writes compressed metadata and float64 values, flushes and fsyncs the file, then atomically replaces the final path. Temporary files are removed if the operation fails.

## 20. Shard Metadata Schema

Shard metadata includes:

- model;
- direction;
- condition;
- seed;
- metric;
- replicate start;
- replicate end;
- prediction hash;
- bootstrap draw hash;
- engine hash.

The result vector is stored as float64. Undefined ranking replicates can be represented by `NaN` only when explicitly permitted by the validator.

## 21. Shard Validation Tests

Implemented tests cover:

- successful atomic round-trip;
- wrong metric metadata rejection;
- vector/range validation;
- duplicate range rejection;
- missing range rejection;
- temporary-file cleanup.

The complete requested matrix of every wrong-hash field and every malformed metadata category was not fully parameterized in the test file. This remains secondary evidence, but the B0 regression is already a hard freeze blocker.

## 22. Interrupted-Write Test

The atomic writer behavior was tested for temporary-file cleanup and final-file visibility. A separately instrumented process kill between fsync and rename was not executed. Therefore a full OS-level interrupted-write simulation is not claimed.

## 23. Resume Test

A three-shard-equivalent small resume path was tested by writing shards 1 and 2, re-reading and validating them, writing shard 3, and merging the complete vector. Missing-range rejection passed.

A real subprocess kill/restart orchestration was not executed; the deterministic shard reuse behavior was tested in-process.

## 24. Merge Validation

Implemented merge rejection for:

- duplicate ranges;
- overlapping ranges;
- missing ranges;
- out-of-bounds ranges;
- invalid vector lengths.

Wrong engine/prediction/draw hash and wrong condition/seed checks are enforced through shard metadata validation. A full 0..1999 production merge was not executed because Step 15.3 production finalization remains prohibited.

## 25. Worst-Case Benchmark

Population:

- D2 ISRUC → Sleep-EDF COMPLETE TARGET;
- B1 seed 17;
- C3;
- 414,961 epochs;
- 78 subjects;
- 100 frozen QA replicates;
- one worker;
- shard size 100.

Versioned benchmark:

`reports/step15_2_1_ranking_engine_benchmark.csv`

## 26. AUROC Benchmark

- QA replicates: 100
- Wall time: approximately 113.65 seconds
- Starting RSS: 550,379,520 bytes
- Peak RSS: 551,886,848 bytes
- Ending RSS: 552,779,776 bytes
- Reference error: 0.0 in the executed equivalence path
- Status: PASS QA

## 27. AUPRC Benchmark

- QA replicates: 100
- Wall time: approximately 109.37 seconds
- Starting RSS: 550,379,520 bytes
- Peak RSS: 553,697,280 bytes
- Ending RSS: 553,697,280 bytes
- Reference error: 0.0 in the executed equivalence path
- Status: PASS QA

## 28. AURC Benchmark

- QA replicates: 100
- Wall time: approximately 112.51 seconds
- Starting RSS: 550,379,520 bytes
- Peak RSS: 553,816,064 bytes
- Ending RSS: 553,816,064 bytes
- Reference error: 0.0 in the executed equivalence path
- Status: PASS QA

## 29. Peak Memory

Peak RSS was measured with `psutil.Process(...).memory_info().rss` during execution.

Maximum recorded peak RSS across the three metrics was:

`553,816,064 bytes`

The benchmark completed without an observed memory failure. No formal memory ceiling was imposed.

## 30. Frozen Production Shard Size

`100` replicates is the largest tested QA shard size and completed for all three ranking metrics. However, production shard size was not frozen because the B0 v1.1 regression gate remains blocked.

## 31. Worker Configuration

The benchmark used one worker. No production parallel worker configuration was frozen. The single-worker path remains the validated reference path.

## 32. Engine Config

Path: `configs/weighted_bootstrap_engine_v1.yaml`

Version: `1.0.0`

The config records subject-level bootstrap semantics, 2,000 replicates, NumPy `default_rng`, seed `2028`, float64 accumulation, class order, metric conventions, ranking direction, undefined behavior, tolerance, shard size, and ordering policy.

## 33. Final Engine Hash Manifest

Path:

`reports/step15_2_weighted_bootstrap_engine_hashes.txt`

The final manifest hashes the repaired engine implementation, engine configuration, complete Step 15.2 test file, QA runner, draw audit, synthetic equivalence, real equivalence, B0 regression artifact, and versioned benchmark.

The manifest was regenerated after the AUPRC/AURC correction and benchmark completion.

## 34. Tests Added

- expanded `tests/test_step15_2_weighted_bootstrap.py`;
- `[A,A,C]` duplicate-preservation checks;
- weighted additive/ranking/conformal equivalence checks;
- atomic shard round-trip test;
- shard metadata rejection test;
- missing-range resume/merge test;
- authoritative AUPRC duplicate-equivalence test.

The QA execution script is:

`scripts/step15_2_1_qa.py`

## 35. Full Repository Validation

- Focused Step 15.2 tests: `9 passed`
- Full repository tests: `134 passed`
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed
- `git diff --check`: passed

The full repository test suite was rerun after the engine correction and QA additions.

## 36. Files Created

- `reports/STEP_15_2_1_WEIGHTED_RANKING_ENGINE_FREEZE_REPORT.md`
- `reports/step15_2_1_bootstrap_draw_audit.csv`
- `reports/step15_2_1_synthetic_equivalence.csv`
- `reports/step15_2_1_real_equivalence.csv`
- `reports/step15_2_1_b0_v1_1_regression.csv`
- `reports/step15_2_1_ranking_engine_benchmark.csv`
- `scripts/step15_2_1_qa.py`

## 37. Files Modified

- `src/shiftsleep_uq/statistics/weighted_bootstrap.py`
- `tests/test_step15_2_weighted_bootstrap.py`
- `reports/step15_2_weighted_bootstrap_engine_hashes.txt`

No frozen B0/B1 prediction, calibration, normalization, checkpoint, or bootstrap input artifact was modified.

## 38. Explicitly Not Done

- no training;
- no inference;
- no checkpoint reselection;
- no normalization fitting;
- no temperature fitting;
- no APS fitting;
- no target fitting;
- no oracle analysis;
- no changed scientific metric definition;
- no changed bootstrap count;
- no changed bootstrap seed;
- no approximation;
- no production 2,000-replicate finalization;
- no B1 confidence intervals;
- no paired scientific results;
- no compound classification;
- no interpretation case;
- no Step 16;
- no SHHS;
- no push;
- no tag.

## 39. Engine Freeze Commit

`NONE`

Commit message reserved for a future successful freeze:

`eval: freeze exact weighted ranking bootstrap engine`

The B0 v1.1 AUPRC/AURC compatibility failure prevents the required local freeze commit.

## 40. GitHub Status

`LOCAL_COMMIT_ONLY`

`NO_PUSH`

No GitHub push or tag was created.

## 41. Remaining Work

1. Resolve the semantic/provenance conflict between the corrected exact duplicate-preserving AUPRC/AURC engine and the frozen B0 v1.1 AUPRC/AURC outputs.
2. Decide, under the project’s scientific governance, whether B0 v1.1 must be regenerated as a versioned corrected artifact or whether the engine must reproduce the historical B0 implementation while separately preserving the exact duplicate-cluster regression.
3. Complete the OS-level interrupted-write subprocess test and parameterized wrong-hash/metadata rejection matrix.
4. Rerun the final hash manifest and full validation after the authoritative B0 decision.
5. Only after those gates pass may the Step 15.2 freeze commit be created.

## 42. Recommended Next Step

Do not execute Step 15.3.

First resolve the B0 v1.1 AUPRC/AURC regression conflict and complete the remaining shard-process QA. The next scientific execution remains blocked until the engine is frozen.

## 43. Git Status / Diff Summary

The worktree contains the intentional partial Step 15/15.1 artifacts, the repaired weighted engine, Step 15.2.1 QA artifacts, tests, benchmark, and report. No freeze commit was created because the engine gate is `WEIGHTED_RANKING_ENGINE_BLOCKED`. No remote state was changed.
