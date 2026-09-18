# ShiftSleep-UQ Step 15.2.2 B0 Ranking-Bootstrap Provenance Audit

## 1. Status

`B0_RANKING_PROVENANCE_RESOLVED`

Step 15.2.2 is complete as a forensic audit. It confirms a metric-specific historical semantic defect in the B0 v1.1 AUPRC/AURC bootstrap path. No B0 artifact was repaired or overwritten.

## 2. Provenance Gate

`B0_V1_1_AUPRC_AURC_BOOTSTRAP_BUG_CONFIRMED`

The authoritative-version recommendation is:

`CREATE_VERSIONED_B0_V1_2_RANKING_STATISTICAL_REPAIR`

The engine remains blocked for production use until the separate repair step creates and audits versioned B0 v1.2 statistical outputs.

## 3. Current Scientific State

- Scientific evaluation gate: `B1_PRIMARY_EVALUATION_PARTIAL`.
- Weighted engine gate: `WEIGHTED_RANKING_ENGINE_BLOCKED` pending versioned B0 governance and remaining engine freeze work.
- Step 15.3: prohibited.
- Step 16: prohibited.
- This report is forensic provenance evidence, not a repaired scientific result.

## 4. Frozen Input Integrity

Repository preflight confirmed the ShiftSleep-UQ repository on `main`. The B0 v1.1 bootstrap artifact hash remains:

`47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022`

The 36-row B0 prediction manifest was verified: all 36 prediction file hashes matched. Temperature, APS, and normalization hash fields were present for all 36 rows. The B0 statistical hash manifest and prediction manifest were not modified. The frozen B1 draw schedules and input artifacts were not modified.

Preflight evidence:

- `reports/step15_2_2_b0_preflight_hashes.json`
- `reports/b0_statistical_hashes_v1_1.txt`
- `reports/b0_primary_prediction_hashes_v1.txt`

## 5. Step 11.1 Written Bootstrap Contract

The written Step 11.1 contract requires subject-cluster bootstrap reconstruction: if a sampled subject appears twice, its complete epoch cluster appears twice. The existing Step 11.1 test explicitly reconstructs the cluster with `reconstruct_cluster_indices`, and the written report describes duplicate-subject cluster preservation.

The intended `[A,A,C]` semantics are therefore physical `A + A + C`, not one weighted threshold contribution for A and one for C.

The identity case is a separate invariant: when every subject has multiplicity one, weighted and literal representations are identical.

## 6. Historical Code-Path Map

The exact function/file map is recorded in:

`reports/step15_2_2_b0_ranking_codepath_map.md`

The historical B0 v1.1 writer is `scripts/step11_1_statistical_qa.py`. It creates shared draws with `bootstrap_subject_draws`, calls `weighted_metric_replicates`, averages the three seed vectors with `np.nanmean`, and writes `bootstrap_replicates_v1_1.npz` with `np.savez_compressed`.

The historical implementation under audit is `src/shiftsleep_uq/step11_1_statistics.py:weighted_metric_replicates`.

## 7. Historical AUPRC Implementation

The point function is `src/shiftsleep_uq/evaluation_step11.py:auprc`. It uses descending stable uncertainty order, cumulative true positives and recall, and the repository-specific average-precision-style sum that omits the first recall increment.

The historical weighted bootstrap implementation at `step11_1_statistics.py:weighted_metric_replicates`, lines 189–190, computes one precision/recall point per original epoch after applying subject multiplicity to cumulative counts. It does not emit one sequential point for each of the repeated observations.

Thus a multiplicity `w=2` positive observation contributes one weighted threshold point, not two sequential duplicate observations. This is the specific semantic defect.

## 8. Historical AURC Implementation

The point function is `src/shiftsleep_uq/evaluation_step11.py:aurc`.

The historical weighted implementation at `step11_1_statistics.py:weighted_metric_replicates`, lines 185–186, computes one weighted prefix-risk contribution per original epoch. It multiplies the risk contribution by the epoch weight, but it does not generate the distinct retained-set prefix risks at each of the repeated observations.

Literal duplication requires all intermediate prefixes. A repeated error observation with weight three contributes three different prefix-risk values; the historical path collapses them into one weighted contribution.

## 9. Historical AUROC Control

AUROC passed the forensic control. The historical path, literal reconstruction, and exact engine agreed on the synthetic `[A,A,C]` fixture:

`H = L = E = 1.0`

This is expected because integer sample weights can exactly represent the pair/rank counts used by AUROC. The weighted rank-sum calculation preserves the same positive-negative ordering and tie semantics as physical duplication.

## 10. Historical Macro-F1 Control

Macro-F1 also passed. Weighted confusion-matrix cell counts are additive over epochs, so multiplying every epoch in a subject cluster by its integer subject multiplicity exactly reproduces physical duplication. The `[A,A,C]` macro-F1 control and the identity audit passed.

## 11. `[A,A,C]` AUPRC Forensic Test

Fixture observations were subjects `A,B,C`, with A and C error-positive and B non-error. The sampled subject sequence was `[A,A,C]`, giving multiplicities `[2,0,1]`. Uncertainty order was deterministic and non-tied.

| Path | ERROR_AUPRC |
|---|---:|
| H historical weighted path | `0.0` |
| L literal `A+A+C` | `0.5` |
| E exact weighted engine | `0.5` |

The historical path does not preserve the duplicated positive observation's sequential threshold contribution. L and E agree exactly.

Evidence: `reports/step15_2_2_b0_synthetic_counterexamples.csv`.

## 12. `[A,A,C]` AURC Forensic Test

The same fixture produced:

| Path | AURC |
|---|---:|
| H historical weighted path | `0.4444444444444444` = `4/9` |
| L literal `A+A+C` | `0.38888888888888884` = `7/18` |
| E exact weighted engine | `0.3888888888888889` |

The difference is caused by the missing intermediate retained-set prefix produced by the repeated observation.

## 13. AUPRC Minimal Counterexample

The minimal counterexample uses three subjects and one repeated subject. The duplicated positive observation creates two sequential positive threshold events in the literal sample. The historical weighted path has only one threshold event at that original epoch position. The exact engine expands the weighted positive contribution analytically and matches the literal result.

The discrepancy is `0.5`, far above any floating-point tolerance.

## 14. AURC Minimal Counterexample

The same three-subject fixture is sufficient. The literal retained-set path contains the intermediate prefix after the first copy of A and the next prefix after the second copy of A. The historical path contributes a single weighted term instead of those distinct terms.

The discrepancy is `1/18`, again far above numerical reduction error.

## 15. Draw-Schedule Alignment

All real-data forensic rows used `bootstrap_subject_draws(subject_count, reps=2000, seed=2028)`, with sorted subject ordering matching the historical and exact implementations. Each matrix row records the SHA-256 hash of the exact integer subject-index draw.

The seed-17 forensic matrix contains:

- D1 C0: 20 replicate indices;
- D1 C3: 10 replicate indices;
- D2 C0: 20 replicate indices;
- D2 C3: 10 replicate indices.

The same draw vector was passed to H, L, and E for each row. Draw alignment evidence is in `reports/step15_2_2_b0_ranking_forensic_matrix.csv`.

## 16. Seed-Aggregation Alignment

The historical writer averages per-seed bootstrap values with `np.nanmean` after using the same population draw schedule. A selected three-replicate, D1/D2 C0/C3 audit evaluated all B0 seeds `17`, `42`, and `2026`.

For every selected metric and replicate, the historical three-seed mean reproduced the stored artifact value within approximately `1e-15`:

- H mean vs A for AUROC: zero or machine roundoff;
- H mean vs A for AUPRC: at most machine roundoff;
- H mean vs A for AURC: at most machine roundoff.

Therefore H reproduces A, while L/E differ from H for non-identity multiplicities. Evidence: `reports/step15_2_2_b0_seed_aggregation_alignment.csv`.

## 17. D1 C0 Forensic Matrix

The D1 C0 matrix contains 20 replicate indices for seed 17 and all three ranking metrics. H reproduces the historical seed-specific computation. L and E agree to machine precision. The stored A column is the three-seed artifact aggregate and is therefore intentionally not compared to a single-seed H value in that matrix.

Representative replicate zero:

- H AUROC: `0.9367481943710596`;
- L/E AUROC: `0.9367481943710596`;
- H AUPRC: `0.5323956295057333`;
- L/E AUPRC: `0.532219250789937`;
- H AURC: `0.011297326004855274`;
- L/E AURC: `0.01129650440295`.

## 18. D1 C3 Forensic Matrix

The D1 C3 matrix contains 10 replicate indices. The same pattern is observed: H is the historical implementation, L and E agree, and the ranking discrepancies occur on resampled subject multiplicities. The matrix is complete for the required D1 C3 sample.

## 19. D2 C0 Forensic Matrix

The D2 C0 matrix contains 20 replicate indices. H, L, and E were evaluated with identical subject draws. The larger D2 source population does not remove the discrepancy; repeated subject clusters still create different sequential ranking prefixes.

## 20. D2 C3 Forensic Matrix

The D2 C3 matrix contains 10 replicate indices. The exact weighted engine agrees with literal duplicated-cluster reconstruction, while the historical H path differs for AUPRC/AURC on non-identity draws. The required D2 target sample is complete.

## 21. Other-Condition Spot Checks

After the defect was confirmed, one seed-17 replicate was audited for C1, C2, C4, and C5 in both directions, covering all three ranking metrics. The resulting artifact is:

`reports/step15_2_2_b0_other_condition_spot_checks.csv`

The same metric-specific pattern was observed: AUROC is compatible with exact duplication; AUPRC and AURC differ whenever multiplicities create repeated ranking observations. These checks establish that the defect is general to the ranking bootstrap implementation rather than specific to C0/C3.

## 22. Point-Estimate Audit

The identity/full-population point audit covered all 2 experiments × 3 seeds × 6 conditions × 3 ranking metrics. Historical identity values and exact identity values matched within floating-point precision.

Result:

`POINT_ESTIMATES_UNCHANGED`

This is expected because the full-population point has multiplicity one for every subject. The defect affects resampled bootstrap replicates, not the identity point estimate.

Evidence: `reports/step15_2_2_b0_point_identity_audit.csv`.

## 23. Bootstrap CI Impact

No corrected authoritative CI table was generated. The bounded forensic matrix demonstrates that the resampled AUPRC/AURC vectors are changed, so their percentile centers, widths, and bounds are potentially affected. Point-inside-CI status is also potentially affected and must be recomputed in the future repair.

The current audit does not claim corrected CI values, contrast decisions, or revised scientific conclusions.

## 24. Contrast Dependency Map

Created:

`reports/step15_2_2_b0_ranking_dependency_map.csv`

The map identifies AUPRC/AURC bootstrap CI fields in the B0 primary results and contrast tables as potentially affected. Point-estimate fields are not affected by the demonstrated multiplicity defect. Any paired, modality, interaction, or hypothesis field consuming those ranking CIs requires re-audit after repair.

## 25. Step 12 / 12.1 Impact

No Step 12 or 12.1 gate was recomputed in this audit. The affected ranking-bootstrap CIs are upstream evidence for any gate or diagnostic that used B0 AUPRC/AURC intervals.

Classification:

- failure-mode matrix entries based only on point estimates: `UNAFFECTED_BY_RANKING_BOOTSTRAP`;
- Criterion A/B/D entries using AUPRC/AURC bootstrap intervals: `MUST_BE_REAUDITED_AFTER_REPAIR`;
- `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`: `MUST_BE_REAUDITED_AFTER_REPAIR` if its evidence included affected ranking intervals;
- `MODALITY_CONDITIONING_SUPPORTED`: `MUST_BE_REAUDITED_AFTER_REPAIR` if its evidence included affected ranking intervals;
- no gate is changed by this audit.

## 26. Future B1 Comparison Impact

B1-vs-B0 paired analysis cannot safely proceed using the historical B0 AUPRC/AURC bootstrap vectors as if they satisfied the frozen subject-cluster contract. Step 15.3 remains blocked until a versioned B0 v1.2 repair and downstream re-audit are complete.

## 27. Why Step 11.1 Tests Did Not Catch It

The inspected Step 11.1 tests verify cluster-index reconstruction and identity invariants. They do not execute a ranking-metric `[A,A,C]` comparison through `weighted_metric_replicates` against a physically expanded cluster for AUPRC and AURC.

The identity test uses multiplicity one, where the historical formulas and literal formulas necessarily coincide. The duplicate-cluster test checks reconstruction and macro-F1 behavior, not the historical weighted ranking formulas. Therefore the tests were insensitive to the repeated-prefix defect.

## 28. Root Cause

`B0_V1_1_AUPRC_AURC_BOOTSTRAP_BUG_CONFIRMED`

The classification satisfies all required conditions:

1. the historical code reproduces the stored v1.1 artifact after the same three-seed aggregation;
2. the historical AUPRC/AURC weighted formulas differ from literal duplicate-cluster evaluation;
3. the exact engine agrees with literal reconstruction on synthetic and frozen B1/B0 checks;
4. the discrepancy is explained by collapsing repeated observations into one weighted threshold/prefix term;
5. draw schedules, subject order, seed identity, and aggregation have been independently aligned.

## 29. Authoritative-Version Recommendation

`CREATE_VERSIONED_B0_V1_2_RANKING_STATISTICAL_REPAIR`

B0 v1.1 remains preserved as historical provenance, but it should not remain the authoritative version for subject-bootstrap AUPRC/AURC inference after this confirmed contract violation.

## 30. What a Future Repair Would Change

A separate Step 15.2.3 must:

- preserve v1.1 files and hashes;
- recompute only statistical post-processing affected by ranking semantics;
- use exact literal duplicate-preserving AUPRC/AURC semantics;
- generate versioned B0 v1.2 outputs and hashes;
- rerun the complete B0 ranking regression and downstream gate-impact audit;
- rerun the required engine freeze checks against the versioned authoritative reference.

## 31. What a Future Repair Would NOT Change

The repair must not change:

- B0 prediction bundles;
- checkpoints;
- calibration objects;
- normalization artifacts;
- labels or subject partitions;
- model inference;
- training;
- bootstrap count or seed schedule;
- B1 prediction/calibration artifacts;
- the historical v1.1 files;
- the preregistered metric direction or scientific protocol.

## 32. Tests Added

Created:

`tests/test_step15_2_2_b0_ranking_provenance.py`

It tests historical/literal/exact AUPRC and AURC `[A,A,C]` behavior, AUROC and macro-F1 agreement controls, and identity point equivalence. The historical artifact, draw, and seed-alignment checks are backed by the generated forensic CSV artifacts.

## 33. Full Validation

Repository-wide validation completed after the new test/report files:

- focused provenance tests: `5 passed`;
- full repository tests: `139 passed in 36.13s`;
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed;
- immutable B0 v1.1 bootstrap hash verification: passed;
- 36-row B0 prediction hash verification: passed.

No historical B0/B1 input artifact changed during validation.

## 34. Files Created

- `reports/STEP_15_2_2_B0_RANKING_BOOTSTRAP_PROVENANCE_AUDIT.md`
- `reports/step15_2_2_b0_ranking_codepath_map.md`
- `reports/step15_2_2_b0_ranking_forensic_matrix.csv`
- `reports/step15_2_2_b0_synthetic_counterexamples.csv`
- `reports/step15_2_2_b0_seed_aggregation_alignment.csv`
- `reports/step15_2_2_b0_other_condition_spot_checks.csv`
- `reports/step15_2_2_b0_point_identity_audit.csv`
- `reports/step15_2_2_b0_ranking_dependency_map.csv`
- `reports/step15_2_2_b0_preflight_hashes.json`
- `scripts/step15_2_2_b0_provenance_audit.py`
- `scripts/step15_2_2_seed_alignment.py`
- `scripts/step15_2_2_other_conditions.py`
- `tests/test_step15_2_2_b0_ranking_provenance.py`

## 35. Files Modified

No B0 authoritative result, contrast, bootstrap, prediction, calibration, normalization, checkpoint, or draw artifact was modified.

The Step 15.2.2 audit and preserved prior Step 15 artifacts are committed locally in the audit commit listed below.

## 36. Explicitly Not Done

- no B0 result repair;
- no B0 overwrite;
- no B1 finalization;
- no training;
- no inference;
- no calibration fit;
- no new method;
- no Step 15.3;
- no Step 16;
- no SHHS;
- no raw PSG access;
- no corrected v1.2 result tables;
- no GitHub push;
- no tag.

## 37. Local Audit Commit

Commit message: `eval: audit B0 ranking bootstrap provenance`

Commit SHA: the current local `HEAD` (verified with `git rev-parse HEAD`; embedding a SHA inside the committed report would change that SHA).

## 38. GitHub Status

`NO_PUSH`

No remote branch or tag was changed.

## 39. Recommended Next Step

# Step 15.2.3 — Create the Versioned B0 v1.2 AUPRC/AURC Statistical Repair and Reaudit Downstream Gates

Do not execute it as part of Step 15.2.2.

## 40. Git Status / Diff Summary

The worktree is clean after the local audit commit. The historical B0 v1.1 artifacts remain byte-identical to their preflight hashes. No push, tag, B0 repair, or Step 15.3 execution occurred.
