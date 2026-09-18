# ShiftSleep-UQ Step 17 Benchmark Synthesis and Paper Evidence Report

## 1. Status

`BENCHMARK_SYNTHESIS_FROZEN`. Step 17 created the deterministic benchmark-only paper evidence package from frozen B0 v1.2, B1 Step 15.3, and Step 16 artifacts. No new model training, inference, calibration fitting, oracle fitting, or statistical test was performed.

## 2. Synthesis Gate

`BENCHMARK_SYNTHESIS_FROZEN`.

## 3. Starting Scientific State

The required starting gates were verified: `B0_V1_2_AUTHORITATIVE`, `WEIGHTED_RANKING_ENGINE_FROZEN`, `B1_PRIMARY_EVALUATION_COMPLETE`, `STEP16_METHOD_GATE_COMPLETE`, and `RELIABILITY_METHOD_NOT_AUTHORIZED`. The Step 16 tag `step16-method-gate-frozen` was verified to target scientific commit `e9d4cc8f59d4f791dad45c2fed3df8a5ffb67225`.

## 4. Final Benchmark Framing

ShiftSleep-UQ is a controlled benchmark and reliability study of multimodal sleep staging under dataset shift, missing-modality shift, and their compound interaction. The contribution is the controlled benchmark design, reciprocal domain evaluation, subject-level reliability analysis, source-only modality-dropout control, separation of predictive from reliability behavior, target-free deployment evaluation, and reproducible statistical/provenance treatment. It is not a new architecture, calibration network, uncertainty model, or state-of-the-art classifier claim.

## 5. Final Research Questions

- **RQ1 — Predictive robustness:** How do predictive performance and stage-level behavior change under dataset shift, missing-modality shift, and compound interaction?
- **RQ2 — Reliability robustness:** How do calibration, error ranking, and selective prediction behave under the same shifts?
- **RQ3 — Conformal robustness:** How do source-calibrated conformal coverage and set efficiency transfer under compound shift?
- **RQ4 — Robustness control:** Does source-only modality-dropout training mitigate compound-shift failures, and do reliability improvements track predictive improvements?

## 6. Final Hypothesis Status

`reports/step17_hypothesis_evidence_map_v1.csv` maps frozen hypotheses F1–F5 to artifacts and evidence. F1 is supported in three primary compound cells but not universally. F2–F5 are supported with directional and reliability-family caveats. F6 is `NOT TESTED — METHOD NOT AUTHORIZED`.

## 7. Canonical Main Claims

The evidence supports these bounded claims:

1. Compound dataset × modality shift produces direction- and modality-dependent predictive and reliability degradation.
2. B1 source modality-dropout training improves compound macro-F1 in three of four primary cells: D1 C4, D1 C5, and D2 C4.
3. D2 C5 remains inconclusive for predictive improvement.
4. Predictive improvement does not guarantee uniform calibration, selective, or conformal improvement.
5. No practically notable full-modality target tradeoff was observed under the preregistered C3 guardrail.
6. Source-only mask-specific calibration does not uniformly resolve residual reliability behavior.
7. Target-oracle diagnostics show partial recoverability but do not establish source-only deployability.
8. The evidence does not justify an additional learned reliability model.

The claim/evidence matrix is `reports/step17_claim_evidence_matrix_v1.csv`.

## 8. Explicit Non-Claims

`reports/step17_nonclaims_v1.md` prohibits claims of universal uncertainty failure, universal modality-dropout superiority, montage causality, clinical safety, generalization to all sleep datasets, formal conformal coverage under arbitrary shift, target-free recovery from all shifts, a novel calibration method, state-of-the-art sleep staging, a new architecture, SHHS validation, or performance on unevaluated populations.

## 9. B0 v1.2 Summary

Table 2 and Figure 2 use B0 v1.2 only. B0 establishes the compound-shift landscape across C0–C5, with predictive and reliability metrics moving differently across transfer direction and missing-modality condition. Historical B0 v1.1 inferential tables were not used.

## 10. B1 Robustness Summary

The canonical paired macro-F1 effects are:

- **D1 C4:** `+0.03673`, 95% CI `[+0.03141,+0.04215]`, `SUPPORTED_IMPROVEMENT`, `PRACTICALLY_NOTABLE_GAIN`.
- **D1 C5:** `+0.18587`, 95% CI `[+0.16786,+0.20296]`, `SUPPORTED_IMPROVEMENT`, `PRACTICALLY_NOTABLE_GAIN`.
- **D2 C4:** `+0.05992`, 95% CI `[+0.05308,+0.06667]`, `SUPPORTED_IMPROVEMENT`, `PRACTICALLY_NOTABLE_GAIN`.
- **D2 C5:** `+0.00063`, 95% CI `[-0.01255,+0.01451]`, `INCONCLUSIVE_DIRECTION`, `SMALL_MAGNITUDE`.

These values are verified against `reports/b1_vs_b0_paired_results_v1.csv` and are presented in Table 3 and Figure 3.

## 11. Residual Reliability Summary

The frozen residual labels remain heterogeneous:

- D1 C4: `MIXED_RELIABILITY_RESPONSE`.
- D1 C5: `RELIABILITY_IMPROVES_WITH_PREDICTION`.
- D2 C4: `RELIABILITY_IMPROVES_WITH_PREDICTION`.
- D2 C5: `MIXED_RELIABILITY_RESPONSE`.

Figures 4 and 5 preserve this decoupling across calibrated NLL, entropy AURC, and alpha-.10 conformal absolute coverage gap. The result is not simplified to either universal reliability improvement or universal reliability failure.

## 12. Simple Source Calibration Summary

Step 16 source mask-specific temperature and APS objects are retained as a `SECONDARY DIAGNOSTIC BASELINE`. Exactly 18 temperature fits and 18 APS objects were created using SOURCE CALIBRATION subjects only. The comparison is in `reports/step16_source_mask_calibration_comparison_v1.csv`. The control does not uniformly resolve the residual pattern and does not replace the primary target-free B1 deployment evaluation.

## 13. Oracle Diagnostic Summary

The Step 16 oracle package is a `DIAGNOSTIC UPPER BOUND`. It reuses the frozen disjoint oracle calibration/evaluation partition and is not deployable evidence. It supports partial target-label recoverability for selected calibration and conformal quantities but does not support target adaptation, target-free deployment, improved prediction, or authorization of a learned method.

## 14. Final Method-Gate Interpretation

`RELIABILITY_METHOD_NOT_AUTHORIZED`. The final gate is based on the combined frozen B1 predictive control, source-only mask-specific calibration control, and diagnostic oracle evidence. A learned reliability calibrator was deliberately not implemented because the prerequisite evidence did not justify it.

## 15. Final Contribution Statement

The frozen contribution statement contains four bounded contributions:

1. A controlled compound dataset-shift and missing-modality reliability benchmark.
2. Subject-level target-free evaluation across calibration, selective, and conformal axes.
3. A controlled modality-dropout robustness study showing predictive/reliability decoupling.
4. A reproducible statistical/provenance framework with exact cluster-bootstrap semantics and a versioned B0 correction.

The canonical text is `reports/step17_contribution_statement_v1.md`.

## 16. Table 1

`reports/paper_tables/table1_benchmark_design.csv` contains the two reciprocal directions, source-role counts, target counts, modality channels, montage description, C0–C5 definitions, and seeds. The table is derived from `reports/subject_partitions_v2.csv`.

## 17. Table 2

`reports/paper_tables/table2_b0_primary_shift_results.csv` contains 12 D1/D2 × C0–C5 rows with B0 v1.2 primary metrics: macro-F1, SOURCE-temperature NLL/Brier, uncalibrated error AUROC/AUPRC/AURC, alpha-.10 empirical coverage, absolute coverage gap, and mean set size.

## 18. Table 3

`reports/paper_tables/table3_b1_vs_b0_compound_effects.csv` contains the four primary compound cells, B0/B1 macro-F1, paired macro-F1 delta and CI, predictive status, NLL delta and CI, AURC delta and CI, conformal absolute-gap delta, and residual label.

## 19. Table 4

`reports/paper_tables/table4_residual_diagnosis.csv` contains predictive-confound status, Step 15.3 residual label, simple mask-calibration result, oracle recoverability classification, and final method-gate implication for each primary cell.

## 20. Supplementary Tables

The supplementary package under `reports/paper_tables/supplement/` preserves all B0 v1.2 results, all B1 results, paired comparisons, stage-level effects, confusion changes, interaction contrasts, montage sensitivity, source mask calibration, oracle diagnostics, and the available B0 v1.1→v1.2 repair audit reference. Negative and mixed results were not discarded.

## 21. Figure 1

`fig1_shift_design` is a schematic of D1/D2 reciprocal transfer, source roles, target evaluation, C0–C5, modality masks, and B0/B1. It encodes no fabricated numerical values.

## 22. Figure 2

`fig2_b0_shift_landscape` shows B0 v1.2 C0–C5 shift behavior for macro-F1, calibrated NLL, entropy AURC, and alpha-.10 absolute coverage gap in two direction panels.

## 23. Figure 3

`fig3_b1_compound_macro_f1` is a forest plot of paired B1–B0 macro-F1 deltas and 95% confidence intervals for D1 C4, D1 C5, D2 C4, and D2 C5, with a zero reference line.

## 24. Figure 4

`fig4_compound_reliability_axes` shows the four-cell paired effects for calibrated NLL, entropy AURC, and alpha-.10 conformal absolute coverage gap using native metric scales.

## 25. Figure 5

`fig5_prediction_reliability_decoupling` plots macro-F1 delta against NLL, AURC, and conformal absolute-gap delta. The four-cell display is descriptive and does not fit a causal or inferential regression.

## 26. Figure 6

`fig6_selective_risk_coverage` reconstructs representative B0/B1 risk-coverage curves from frozen prediction bundles for seed 17 in D1 C4, D1 C5, D2 C4, and D2 C5. No new inference or fitting was performed.

## 27. Figure 7

`fig7_conformal_transfer` shows empirical alpha-.10 coverage and mean set size across C0–C5 for both directions. Coverage is explicitly empirical under shift, not a formal arbitrary-shift guarantee.

## 28. Figure 8

`fig8_stage_recall_changes` shows frozen B1–B0 stage-recall changes for Wake, N1, N2, N3, and REM across C3–C5 in both directions.

## 29. Figure Provenance

`reports/step17_figure_provenance_v1.csv` records eight figures, the deterministic generation script, source input files and hashes, PDF/PNG hashes, metric version, and B0 version. Each figure has PDF, 300-dpi PNG, and source CSV outputs under `reports/paper_figures/`.

## 30. Table Provenance

`reports/step17_table_provenance_v1.csv` records the four canonical tables and supplementary tables, source paths and hashes, output hashes, metric version, and B0 v1.2 version.

## 31. Claim-Evidence Matrix

`reports/step17_claim_evidence_matrix_v1.csv` contains eight candidate claims C1–C8. Each is classified as `PRIMARY_SUPPORTED`, `SECONDARY_SUPPORTED`, `DIAGNOSTIC_ONLY`, or `NOT_SUPPORTED`, with artifact, metric, condition, allowed section, and caveat.

## 32. Hypothesis-Evidence Matrix

`reports/step17_hypothesis_evidence_map_v1.csv` maps F1–F5 to frozen evidence. F6 is explicitly marked `NOT TESTED — METHOD NOT AUTHORIZED`.

## 33. Results Narrative Map

`reports/step17_results_narrative_map.md` maps the Results sequence from B0 compound-shift failure through reliability-family divergence, B1 predictive robustness, residual diagnostics, oracle upper bounds, and the final non-authorization decision. Each result includes its source table/figure and caveat.

## 34. Methods Evidence Map

`reports/step17_methods_evidence_map.md` maps datasets, preprocessing, partitions, B0, B1, calibration, conformal evaluation, shift conditions, metrics, subject bootstrap, B0 v1.2 repair, and Step 16 diagnostics to frozen repository artifacts.

## 35. Limitations

`reports/step17_limitations_v1.md` freezes the following limitations: two core datasets; constrained modality/montage contracts; epoch-wise models without temporal context; simple source modality dropout; diagnostic-only target oracle; no SHHS core validation; no formal conformal guarantee under arbitrary shift; deliberately simple architecture; dataset-dependent stage labels/harmonization; direction-specific residuals; and unresolved D2 C5 predictive robustness.

## 36. Title Candidates

1. `ShiftSleep-UQ: Calibration and Selective Reliability of Multimodal Sleep Staging Under Compound Dataset and Missing-Modality Shift`
2. `ShiftSleep-UQ: A Controlled Benchmark of Predictive and Reliability Robustness in Multimodal Sleep Staging`
3. `Predictive Robustness and Reliability Decoupling Under Compound Shift in Multimodal Sleep Staging`

These are recorded in `reports/step17_title_candidates.md` without unsupported novelty language.

## 37. Abstract Evidence Skeleton

`reports/step17_abstract_evidence_skeleton.md` contains factual slots for the problem, gap, benchmark/protocol, B0 finding, B1 finding, reliability heterogeneity, and conclusion. It uses the exact frozen primary deltas and does not introduce invented percentages or sweeping claims.

## 38. Paper Evidence Manifest

`reports/paper_evidence/paper_evidence_manifest_v1.json` contains the `BENCHMARK_SYNTHESIS_FROZEN` gate, B0 v1.2 version, final method gate, and SHA-256 hashes for the canonical tables, figure/table provenance, claim matrix, hypothesis map, non-claims, narrative map, methods map, limitations, contribution statement, title candidates, and abstract skeleton.

## 39. Tests Added

`tests/test_step17_paper_synthesis.py` verifies B0 v1.2-only use, B1 and Step 16 gates, canonical table row counts, all four compound macro-F1 values, figure outputs and provenance, source-data presence, claim and hypothesis maps, F6 non-testing status, diagnostic-only oracle labeling, non-claims, evidence manifest, and absence of silent NaNs in canonical tables.

## 40. Full Validation

- Step 17 synthesis script executed successfully: `BENCHMARK_SYNTHESIS_FROZEN`.
- Full repository tests: `155 passed`.
- Compileall: passed.
- `git diff --check`: passed.
- Canonical tables: 4.
- Supplementary tables: 10.
- Figures: 8, each with PDF, PNG, and source CSV.
- Figure provenance: 8 complete rows.
- Canonical claim matrix: 8 claims.
- Hypothesis map: F1–F6, with F6 not tested.
- Source-mask calibration: retained as secondary diagnostic baseline.
- Oracle diagnostics: labeled diagnostic-only.
- B0 v1.2 and Step 15.3 source gates verified.
- No new scientific computation was run.

## 41. Files Created

- `scripts/step17_paper_synthesis.py`
- `tests/test_step17_paper_synthesis.py`
- `reports/paper_tables/`
- `reports/paper_figures/`
- `reports/step17_figure_provenance_v1.csv`
- `reports/step17_table_provenance_v1.csv`
- `reports/step17_hypothesis_evidence_map_v1.csv`
- `reports/step17_claim_evidence_matrix_v1.csv`
- `reports/step17_nonclaims_v1.md`
- `reports/step17_results_narrative_map.md`
- `reports/step17_methods_evidence_map.md`
- `reports/step17_limitations_v1.md`
- `reports/step17_contribution_statement_v1.md`
- `reports/step17_title_candidates.md`
- `reports/step17_abstract_evidence_skeleton.md`
- `reports/paper_evidence/paper_evidence_manifest_v1.json`
- `reports/STEP_17_BENCHMARK_SYNTHESIS_AND_PAPER_EVIDENCE_REPORT.md`

## 42. Files Modified

No B0 v1.2 artifact, B1 Step 15.3 artifact, Step 16 diagnostic artifact, checkpoint, prediction bundle, partition, protocol, calibration object, or oracle object was modified. The new package contains deterministic derived tables, figures, provenance, maps, and tests in the Step 17 namespace.

## 43. Explicitly Not Done

- no training;
- no inference;
- no new calibration;
- no new oracle fitting;
- no new statistical test;
- no method implementation;
- no SHHS analysis;
- no manuscript claim beyond evidence;
- no Step 18.

## 44. Remaining Work

The benchmark synthesis and evidence package are frozen. A publication-ready manuscript has not yet been drafted. Citation retrieval, manuscript prose, journal formatting, and final rendered-paper acceptance remain future work.

## 45. Recommended Next Step

# Step 18 — Draft the Publication-Ready Manuscript from the Frozen Paper Evidence Package

Step 18 is a recommendation only. It was not executed.

## 46. Git Commit

Scientific synthesis commit: `56d8b69e469e3e7e8331ac104b53b1003f8f96b8` — `paper: freeze benchmark synthesis and evidence package`. The commit contains the validated Step 17 paper evidence package.

## 47. Milestone Tag

Annotated tag: `step17-benchmark-synthesis-frozen`, targeting scientific commit `56d8b69e469e3e7e8331ac104b53b1003f8f96b8`, with annotation `ShiftSleep-UQ benchmark conclusions, figures, tables, and paper evidence frozen`. The tag was created after validation and was verified remotely.

## 48. GitHub Push Status

`PUSH_COMPLETE`. Remote `origin` received `main` and `step17-benchmark-synthesis-frozen` without force push or history rewrite.

## 49. Git Status / Diff Summary

The scientific synthesis commit and annotated tag were pushed successfully. A follow-up documentation-only commit records the final report text without changing the scientific tag target. Remote read-back verified the branch and tag targets. Heavy bootstrap shards, checkpoints, prediction bundles, raw data, and secrets remain outside the tracked synthesis package.
