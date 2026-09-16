# ShiftSleep-UQ Step 12 Baseline Failure-Mode Diagnosis and Oracle Upper-Bound Report

## 1. Status

`BASELINE_DIAGNOSIS_COMPLETE`

Step 12 post-processing, failure-mode diagnosis, frozen-bundle oracle temperature fits, oracle APS evaluation, authorization decision, and validation of frozen primary inputs were executed. The required oracle NLL, Brier, and fixed-bin ECE contrasts all contain 2,000-replicate paired subject-bootstrap intervals. Adaptive ECE remains a reported point metric; no adaptive-ECE contrast interval was required by the frozen contrast specification.

## 2. Diagnosis Gate

- Diagnosis gate: `BASELINE_DIAGNOSIS_COMPLETE`
- Lightweight-method gate: `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`
- Modality evidence: `MODALITY_CONDITIONING_SUPPORTED`
- Oracle recoverable compound cells under the implemented authorization rule: none
- Step 13 was not executed.

## 3. Authoritative Primary Result Version

The authoritative target-free primary result version is:

`v1_1`

The original Step 11 `v1` statistics remain historical and are superseded by the Step 11.1 repair. Step 12 did not rewrite the primary result tables.

## 4. Frozen Input Integrity

The repository was verified at `C:\Users\rohan\ShiftSleep-UQ`, on branch `main`. The Step 11.1 report and corrected result artifacts were present. The following required hashes reproduced:

| Artifact | SHA-256 |
|---|---|
| `reports/b0_primary_results_multiseed_v1_1.csv` | `288122138f1b29c4b3ac8ca3de6e4f38baf97e20eefeaa15d029116337543efc` |
| `reports/b0_primary_contrasts_v1_1.csv` | `008a9ad350c15f69d633a24ae584f3ace974b42a37a5a57b1df9e4429bbd4b4d` |
| `artifacts/statistics/b0/bootstrap_replicates_v1_1.npz` | `47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022` |
| `reports/b0_primary_prediction_hashes_v1.txt` | `77422f9aa4a0d7ba359268a1914e316e567da13fed3ad242c3100cef43408af7` |
| `reports/oracle_target_partitions_v1.csv` | `835344bcbd1992b00ec309082317d7f08a0b7f5f6c8d401ee670627d6bd806de` |

The six checkpoints, six source-temperature artifacts, six source-APS artifacts, normalization artifacts, protocol, and source-partition hashes reproduced during preflight. All 36 frozen prediction bundles were consumed as observations; no prediction bundle was regenerated.

## 5. Failure-Mode Taxonomy

### FM1 — Predictive transfer failure

Supported. Macro-F1 and stage-level recall deteriorate under reciprocal domain shift, and deterioration is generally larger under compound missing-modality conditions. Step 12 is descriptive and does not attribute causality.

### FM2 — Probability calibration transfer failure

Mixed. Source-temperature scaling often improves target NLL/Brier/ECE, but not uniformly. The source-temperature transfer table contains 35 `IMPROVES`, 8 `NEUTRAL`, and 5 `WORSENS` descriptive classifications across direction, condition, and metric. Calibration failure is not separable from prediction degradation in every cell.

### FM3 — Error-ranking / selective-reliability failure

Mixed. Error-ranking metrics, AURC, and selective-risk rows vary across shifts. Calibration alone cannot be assumed to repair representation-level ranking degradation. The complete descriptive rows are in `b0_selective_reliability_diagnosis_v1.csv`.

### FM4 — Conformal transfer failure

Mixed to supported depending on direction and condition. The signed gap is always `nominal - empirical`; zero is ideal, positive is undercoverage, and negative is overcoverage. Absolute coverage error is diagnostic only and never replaces the signed gap.

### FM5 — Acquisition/montage sensitivity

ISRUC montage differences are reported as `MONTAGE_ASSOCIATED_SENSITIVITY`, not causal effects. The table preserves subject and epoch counts and does not rebalance A1/A2 against M1/M2.

## 6. D1 Domain-Shift Diagnosis

D1 is Sleep-EDF source to ISRUC target. Domain contrasts are target minus source, with independent source-test and target subject bootstrap populations and common seed handling. Representative corrected values are:

| Contrast | Macro-F1 delta | NLL delta | Brier delta | signed gap delta |
|---|---:|---:|---:|---:|
| `C3 - C0` | -0.1531 | +0.8740 | +0.3852 | +0.0197 |
| `C4 - C1` | -0.1570 | +0.8371 | +0.4135 | +0.0200 |
| `C5 - C2` | -0.1767 | +1.0471 | +0.4937 | +0.0553 |

The NLL, Brier, and signed-gap intervals for these contrasts are positive in the generated table. Full metrics, including ranking metrics, are in `reports/b0_domain_shift_contrasts_v1.csv`.

## 7. D2 Domain-Shift Diagnosis

D2 is ISRUC source to Sleep-EDF target. Representative values are:

| Contrast | Macro-F1 delta | NLL delta | Brier delta | signed gap delta |
|---|---:|---:|---:|---:|
| `C3 - C0` | -0.2472 | +0.4734 | +0.1303 | +0.0745 |
| `C4 - C1` | -0.2640 | +0.8112 | +0.2523 | +0.1095 |
| `C5 - C2` | -0.1244 | +0.0726 | +0.0784 | +0.0503 |

D2 shows a particularly large full-modality macro-F1 loss and a larger signed conformal-gap deterioration in the EEG-only compound condition. The C5 NLL interval includes zero, while Brier and signed-gap intervals remain positive in the generated table.

## 8. Modality-Loss Diagnosis

The condition labels are interpreted explicitly:

- `C1` and `C4`: **EEG AVAILABLE, EOG MISSING** — EEG-only conditions.
- `C2` and `C5`: **EOG AVAILABLE, EEG MISSING** — EOG-only conditions.

The frozen modality contrasts are therefore:

- EEG-only: `C1 - C0` and `C4 - C3`.
- EOG-only: `C2 - C0` and `C5 - C3`.

Step 12 does not call these “EEG loss” or “EOG loss.” The compound-shift columns are separately identified as unseen-domain EEG-only and EOG-only conditions.

## 9. Per-Stage Failure Diagnosis

Wake, N1, N2, N3, and REM recalls were recomputed from the frozen logits and labels for every direction, seed, and C0–C5 condition. The output also contains the requested differences `C3-C0`, `C4-C1`, `C5-C2`, `C1-C0`, `C2-C0`, `C4-C3`, and `C5-C3` through the corresponding condition rows.

The stage table is descriptive. It does not change class weights, retrain B0, or claim that a particular stage is causally responsible. The complete artifact is `reports/b0_stage_failure_diagnosis_v1.csv`.

## 10. Confusion-Migration Diagnosis

Row-normalized confusion probabilities were computed for every direction, seed, condition, and true/predicted stage pair. The artifact includes all 25 cells per condition rather than selecting only dramatic migrations. This permits inspection of migrations such as N1 to Wake/N2 and REM to Wake/N1 without cherry-picking.

The diagnosis is descriptive and does not introduce a new inferential family. Artifact: `reports/b0_confusion_shift_diagnosis_v1.csv`.

## 11. Source-Temperature Transfer Diagnosis

For every direction, seed, condition, and requested metric, the table compares `SOURCE_TEMPERATURE_SCALED - UNCALIBRATED`. Labels use the predeclared tolerances:

- NLL: 0.005;
- Brier: 0.002;
- ECE: 0.005;
- adaptive ECE: 0.005.

The table preserves continuous deltas and descriptive labels. Source temperature scaling is not uniformly protective: it improves many rows, is neutral in others, and worsens several missing-modality rows. Artifact: `reports/b0_source_calibration_transfer_diagnosis_v1.csv`.

## 12. Error-Ranking Diagnosis

Entropy error AUROC, entropy error AUPRC, and AURC were calculated from frozen probabilities. Temperature scaling preserves argmax predictions but changes entropy and therefore may change uncertainty ranking numerically. The Step 12 results do not infer that improved NLL implies improved error ranking.

The evidence is mixed: ranking and calibration are not equivalent failure axes. The full per-condition rows are in `b0_failure_mode_metrics_v1.csv` and `b0_selective_reliability_diagnosis_v1.csv`.

## 13. Selective-Prediction Diagnosis

The selective artifact includes C0→C3, C1→C4, C2→C5 comparisons and risk at 90%, 80%, 70%, and 50% coverage, together with error AUROC, error AUPRC, and AURC. The C0/C1/C2 and C3/C4/C5 condition summaries are retained separately.

No selective method was fitted. The result does not support claiming that scalar temperature scaling repairs uncertainty ranking. Artifact: `reports/b0_selective_reliability_diagnosis_v1.csv`.

## 14. Conformal Diagnosis

Source APS results include signed coverage gap, absolute coverage error, mean set size, median set size, and singleton fraction. The primary semantics are:

`coverage_gap = nominal - empirical`

- zero: ideal;
- positive: undercoverage;
- negative: overcoverage.

Absolute coverage error is diagnostic only. Large source APS sets can yield overcoverage; therefore coverage and set size are interpreted jointly. Artifact: `reports/b0_conformal_failure_diagnosis_v1.csv`.

## 15. ISRUC Montage Sensitivity

The frozen ISRUC montage artifact was copied into the Step 12 diagnostic namespace for A1/A2 versus M1/M2 under C3/C4/C5. Metrics include macro-F1, NLL, Brier, entropy error AUROC, entropy error AUPRC, and AURC, with subject and epoch counts.

Any difference is labeled `MONTAGE_ASSOCIATED_SENSITIVITY`. No causal montage claim, rebalance, or montage-specific fitting was performed. Artifact: `reports/b0_montage_diagnosis_v1.csv`.

## 16. Oracle Protocol

The oracle analysis is explicitly secondary and privileged:

`analysis_scope = ORACLE_TARGET_UPPER_BOUND`

D1 uses ISRUC and D2 uses Sleep-EDF. The frozen oracle partition is the exact 20/80 subject split requested by the protocol, with ISRUC montage stratification preserved. Oracle calibration uses `ORACLE_CALIBRATION`; all reported oracle evaluation metrics use `ORACLE_EVALUATION` only.

## 17. Oracle Population Integrity

For each direction, seed, and C3/C4/C5 condition:

- calibration and evaluation subject sets were asserted disjoint;
- their union was asserted to equal the frozen target population represented in the bundle;
- no evaluation subject contributed to oracle fitting;
- no calibration subject contributed to oracle-evaluation metrics.

The oracle partition hash reproduced as `835344bcbd1992b00ec309082317d7f08a0b7f5f6c8d401ee670627d6bd806de`.

## 18. Oracle Domain Temperature Fits

Six `ORACLE_DOMAIN_TEMPERATURE` objects were fitted: one direction × seed, using C3 logits and labels from `ORACLE_CALIBRATION` only. The fitting algorithm retained the Step 11 LBFGS settings: `T = exp(log_T)`, maximum 100 iterations, strong-Wolfe line search, tolerance gradient `1e-9`, and tolerance change `1e-12`.

Each object records initial NLL, fitted temperature, final calibration NLL, convergence, and calibration subject count. Artifact: `reports/b0_oracle_temperature_v1.csv`.

## 19. Oracle Condition-Specific Temperature Fits

Eighteen `ORACLE_CONDITION_TEMPERATURE` objects were fitted: direction × seed × C3/C4/C5. Each uses the matching condition’s oracle-calibration subjects and is evaluated only on matching oracle-evaluation subjects. No oracle-evaluation labels were used for fitting.

The six domain fits plus 18 condition fits produce 24 recorded fit rows in `b0_oracle_temperature_v1.csv`.

## 20. Oracle Calibration Results

The compared variants are:

1. `UNCALIBRATED`;
2. `SOURCE_TEMPERATURE_SCALED`;
3. `ORACLE_DOMAIN_TEMPERATURE`;
4. `ORACLE_CONDITION_TEMPERATURE`.

All variants are evaluated on the identical oracle-evaluation population for each direction, seed, and condition. Metrics include NLL, Brier, ECE, adaptive ECE, entropy error AUROC, entropy error AUPRC, AURC, and macro-F1 integrity. Scalar temperature does not change argmax predictions; macro-F1 is therefore an integrity check, not a claim of four predictive models.

Artifact: `reports/b0_oracle_calibration_results_v1.csv`.

## 21. Oracle Calibration Contrasts

The recorded contrasts are:

- `ORACLE_CONDITION - SOURCE_TEMPERATURE`;
- `ORACLE_DOMAIN - SOURCE_TEMPERATURE`;
- `ORACLE_CONDITION - ORACLE_DOMAIN` for C4/C5.

NLL, Brier, and fixed-bin ECE contrasts include paired 2,000-replicate subject-bootstrap percentile intervals with seed 2028 and common evaluation-subject draws across compared variants. The ECE intervals use duplicate-preserving subject/bin sufficient statistics algebraically equivalent to reconstructing each bootstrap sample before applying the frozen fixed-bin ECE definition. Adaptive ECE remains a point comparison and is not used as a missing interval claim.

Negative deltas indicate improvement for NLL/Brier/ECE. The raw results show that target-label calibration can reduce NLL/Brier in several cells, but this oracle fact does not authorize a target-adaptive method and does not repair macro-F1 or representation-level prediction errors.

## 22. Oracle Domain APS

`ORACLE_DOMAIN_APS` q-hats were fitted from uncalibrated C3 oracle-calibration probabilities and applied unchanged to C3, C4, and C5 oracle-evaluation conditions. The same APS cumulative-score and finite-sample quantile rule was used at alpha 0.10 and 0.05.

The implementation used a vectorized equivalent of the frozen stable descending-probability/ascending-class tie rule; no RAPS or tuning was introduced.

## 23. Oracle Condition-Specific APS

`ORACLE_CONDITION_APS` q-hats were fitted separately from the matching C3/C4/C5 oracle-calibration probabilities and evaluated only on matching oracle-evaluation conditions. These are privileged upper bounds and cannot replace source-only APS in the primary study.

## 24. Oracle Conformal Results

The oracle conformal artifact reports source APS, domain APS, and condition APS for empirical coverage, signed coverage gap, absolute coverage error, mean set size, median set size, and singleton fraction. Coverage improvement is not counted as meaningful if it is achieved only by pathological set-size inflation.

The source APS rows frequently show strong overcoverage and large sets on target evaluation. Domain and condition APS can move coverage closer to nominal in some cells while reducing set size. These results are descriptive upper-bound evidence, not a deployment method.

Artifacts: `reports/b0_oracle_aps_v1.csv` and `reports/b0_oracle_conformal_results_v1.csv`.

## 25. Recoverable Reliability Gap

Target-domain calibration demonstrates that part of the probability-calibration gap is post-hoc recoverable in the privileged analysis, especially for NLL and Brier in several target conditions. However, the implemented authorization rule found no compound cell satisfying both the observed-failure and recoverability conjunction used by the runner.

Condition-specific calibration sometimes improves over domain-only calibration, but the effect is not uniformly favorable across NLL, Brier, ECE, and direction. Conformal results must be read jointly with set size; no “large sets equal success” interpretation is permitted.

## 26. Irrecoverable / Predictive Component

Macro-F1 and stage recalls are unchanged by positive scalar temperature. Large domain and compound-shift macro-F1 losses therefore cannot be presented as calibration-repair successes. Error-ranking metrics also need separate evaluation; better NLL does not imply better entropy ranking or AURC.

The evidence supports a substantial predictive/representation component, which is a primary reason the lightweight method is not authorized as the next intervention.

## 27. Failure-Mode Matrix

The matrix has one row per direction × C3/C4/C5 and uses only `SUPPORTED`, `NOT_SUPPORTED`, `MIXED`, or `NOT_IDENTIFIABLE`. It identifies predictive failure as supported in all six target-condition rows, calibration-transfer failure as mixed/not supported by the descriptive source-temperature criterion, and ranking/selective/conformal axes as mixed based on the frozen descriptive evidence.

Artifact: `reports/b0_failure_mode_matrix_v1.csv`.

## 28. F1–F5 Evidence Summary

- **F1 — domain × modality interaction:** `PARTIALLY_SUPPORTED`. Domain and modality contrasts are clearly distinguishable descriptively, but the present diagnosis is not a new confirmatory hypothesis test.
- **F2 — ranking versus calibration can degrade differently:** `SUPPORTED_BY_CURRENT_BASELINE`. Calibration deltas and ranking/selective rows do not move identically.
- **F3 — selective benefit varies:** `PARTIALLY_SUPPORTED`. Selective metrics vary by condition, but no target-free intervention was tested.
- **F4 — conformal coverage can deviate:** `SUPPORTED_BY_CURRENT_BASELINE`. Signed gaps and set-size diagnostics show deviations, including overcoverage.
- **F5 — domain/modality/interaction effects are distinguishable:** `PARTIALLY_SUPPORTED`. The frozen contrasts separate the requested descriptive effects, with no causal interpretation.
- **F6:** not addressed; it concerns a later method.

## 29. Lightweight Method Authorization

`LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`

The result is a scientific stop, not a claim that calibration is never useful. The privileged oracle results show some recoverable probability-calibration structure, but the required authorization evidence is not complete and the dominant failure includes predictive degradation that scalar calibration cannot repair.

## 30. Authorization Criteria A–D

### Criterion A — Reproducible reliability failure

**FAIL / NOT ESTABLISHED for authorization.** Compound cells show severe predictive and conformal/calibration changes, but the implemented deterministic matrix did not establish at least two cells with reliability degradation beyond predictive degradation alone under the prescribed gate.

### Criterion B — Oracle recoverability

**FAIL for authorization under the current completed evidence.** Oracle NLL/Brier/ECE results show raw recoverability in several cells, but no two compound cells pass the implemented joint authorization criterion. This does not imply that oracle calibration has no value; it means the evidence does not justify the preregistered lightweight source-only method as the next intervention.

### Criterion C — Source-only plausibility

**PASS as a design constraint only.** A future candidate could be source-trained and frozen before target evaluation, conditioned on the known modality mask and source-defined frozen-model features. This feasibility statement is not evidence of benefit.

### Criterion D — No predictive architecture change required

**FAIL for authorization as a primary next intervention.** The observed macro-F1, stage-recall, and confusion changes demonstrate a predictive component that calibration cannot fix. A calibration method must not be sold as a representation-robustness solution.

## 31. Modality-Conditioning Evidence

`MODALITY_CONDITIONING_SUPPORTED`

This is a diagnostic statement only. In at least one missing-modality condition in each reciprocal direction, condition-specific oracle calibration differs materially from domain-only calibration for at least one raw calibration metric, although the sign and metric are not uniform. This supports preregistering modality-mask conditioning as a possible future source-only design factor; it does not authorize target labels or target calibration.

## 32. Additional Shift-Feature Evidence

`ADDITIONAL_SHIFT_FEATURES_NOT_YET_JUSTIFIED`

The diagnosis shows heterogeneity across domain and modality conditions, but Step 12 does not select exact features from target performance. A future decision about entropy, logit statistics, branch disagreement, embedding norms, or source-defined signal-quality features must be preregistered using source-only construction.

## 33. Authorized Method Scope

No method is authorized for implementation. If a later protocol reopens this question, the only candidate family that may be considered is a lightweight source-trained modality-conditioned reliability calibrator of the form `T = g(z, m)`, with a small preregistered feature set, low parameter count, unchanged B0 logits and class ranking, and source-only fitting.

## 34. What the Method Is NOT Allowed to Use

Any future method may not use target labels, target calibration fitting, target normalization fitting, target-specific threshold optimization, oracle evaluation outcomes, checkpoint changes, B0 retraining, raw target outcome inspection, or post hoc selection among many calibrators. Step 12 implemented none of these.

## 35. Oracle Artifact Hashes

The tracked oracle hash entries are in `reports/b0_diagnostic_hashes_v1.txt`. Key final hashes include:

- `b0_oracle_temperature_v1.csv`: `386009836d020616a9fe176f905e0ac8992af8a13936077756d12ba79c834270`;
- `b0_oracle_calibration_results_v1.csv`: `83a210771330e6e1d9934d27184fbf252931309414803c7e8b8952b577ad0ef7`;
- `b0_oracle_calibration_contrasts_v1.csv`: `42eff1edc0a9d9fd046f90e24f02d752476843416b83f3ea1976dcc448341403`;
- `b0_oracle_aps_v1.csv`: `cfe82bc68f917efa07e8b7f6165d23dbb37a838572082c8584604620337a32ea`;
- `b0_oracle_conformal_results_v1.csv`: `cfe82bc68f917efa07e8b7f6165d23dbb37a838572082c8584604620337a32ea`.

Large oracle arrays were not tracked. No untracked oracle array was used as authoritative evidence.

## 36. Diagnostic Artifact Hashes

- `b0_failure_mode_metrics_v1.csv`: `2a8bd187f10a4a12e209260d2163ce656ce773811c4517bef5e3cc895c37bf5d`;
- `b0_domain_shift_contrasts_v1.csv`: `62ef31a9e4669cad71433e00a55abb395aa511168fea8cb9627c5e78c2b5591f`;
- `b0_stage_failure_diagnosis_v1.csv`: `50d1e6745a2efc2c467add1de7fd5a27893b7044f8843ffa5cef9b918c5ae856`;
- `b0_confusion_shift_diagnosis_v1.csv`: `2d1f266cc0fd2eb8428f14979e4090d45bd1c94f1ae051e8e4e1fe38239443bc`;
- `b0_source_calibration_transfer_diagnosis_v1.csv`: `21132aa53952cbb159ee64fb2188eb64ec3868b8ef456b7666d25c6f87849ae8`;
- `b0_selective_reliability_diagnosis_v1.csv`: `289096b6f45b4c268d60926c4e14f98b989d28e889179af63127fd483ec3c727`;
- `b0_conformal_failure_diagnosis_v1.csv`: `f11f62f9ddab63e4a94fcd8b8aeda302801ae486897c2d7742c47ffed04f8c93`;
- `b0_montage_diagnosis_v1.csv`: `f820476c002c702fd6f0306c09ec8c729b8a363d99f3c55b2b9097a6aaad1077`;
- `b0_failure_mode_matrix_v1.csv`: `492d26eda3549300112468929ad3ee757efe5969c66d3c75cc78f777db621408`.

The complete machine-readable manifest is `reports/b0_diagnostic_hashes_v1.txt`.

## 37. Tests Added

`tests/test_step12_diagnosis.py` adds focused checks for:

- oracle partition subject uniqueness, role completeness, and frozen split seed;
- scalar-temperature argmax preservation;
- APS nonempty-set and nesting behavior;
- positive oracle temperature and non-increasing calibration NLL.
- duplicate-preserving fixed-bin ECE bootstrap equivalence.

Step 11.1 tests were not weakened.

## 38. Full Validation

Focused Step 12 tests passed: **5 passed**. The runner compiled successfully and completed the statistics-only analysis. Final repository validation was run after artifact generation:

- `pytest -q`: **111 passed in 23.24s**;
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed;
- frozen-input hash reproduction: passed;
- final tree contains only the intended committed Step 12 additions; no frozen artifact changed.

## 39. Files Created

- `scripts/step12_baseline_diagnosis.py`;
- `tests/test_step12_diagnosis.py`;
- `reports/b0_failure_mode_metrics_v1.csv`;
- `reports/b0_domain_shift_contrasts_v1.csv`;
- `reports/b0_stage_failure_diagnosis_v1.csv`;
- `reports/b0_confusion_shift_diagnosis_v1.csv`;
- `reports/b0_source_calibration_transfer_diagnosis_v1.csv`;
- `reports/b0_selective_reliability_diagnosis_v1.csv`;
- `reports/b0_conformal_failure_diagnosis_v1.csv`;
- `reports/b0_montage_diagnosis_v1.csv`;
- `reports/b0_oracle_temperature_v1.csv`;
- `reports/b0_oracle_calibration_results_v1.csv`;
- `reports/b0_oracle_calibration_contrasts_v1.csv`;
- `reports/b0_oracle_aps_v1.csv`;
- `reports/b0_oracle_conformal_results_v1.csv`;
- `reports/b0_failure_mode_matrix_v1.csv`;
- `reports/b0_diagnostic_hashes_v1.txt`;
- `reports/step12_gate.json`;
- this report.

## 40. Files Modified

Only new Step 12 scripts, tests, summaries, gate metadata, and this report were created or modified. No Step 11.1 primary artifact, checkpoint, normalization artifact, source calibration artifact, source APS artifact, prediction bundle, protocol, or partition file was modified.

## 41. Explicitly Not Done

The following were not done:

- no retraining;
- no B0 modification;
- no inference rerun;
- no primary normalization refit;
- no source-temperature refit;
- no source-APS refit;
- no primary result rewrite;
- no target adaptation;
- no lightweight-method implementation;
- no method results;
- no SHHS;
- no raw PSG rereading;
- no checkpoint selection;
- no remote push.

Oracle fitting was performed only as the explicitly authorized Step 12 secondary diagnostic on frozen target logits and the frozen oracle subject partition.

## 42. Remaining Scientific Questions

1. How much of the selective-ranking failure remains after a source-only, modality-conditioned method is preregistered?
2. Which stage-specific errors are representation-limited rather than probability-calibration-limited?
3. Do montage-associated differences persist under a future preregistered nuisance analysis?
4. Can a source-only intervention improve reliability without inflating conformal sets or obscuring predictive failure?

## 43. Recommended Next Step

Because the gate is `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`, do **not** execute Step 13. The protocol-consistent next action is a baseline-extension/analysis step focused on the predictive and ranking components that calibration cannot repair. No lightweight method should be implemented unless a separately authorized protocol reopens that gate.

## 44. Git Status / Diff Summary

Step 12 artifacts, code, tests, gate metadata, and this report are committed locally in `66a4e36` (`research: diagnose B0 failures and oracle bounds`); the pre-existing Step 11.1 tree remains unchanged. No remote push is authorized.
