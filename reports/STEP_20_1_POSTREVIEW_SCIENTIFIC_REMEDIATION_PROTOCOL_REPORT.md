# ShiftSleep-UQ Step 20.1 Post-Review Scientific Remediation Protocol Report

## 1. Status
Step 20.1 completed as a read-only forensic audit plus protocol freeze. Historical B0/B1 results were not overwritten. No new model training, inference, calibration, bootstrap execution, or submission action occurred.

## 2. Remediation Gate
`SCIENTIFIC_REMEDIATION_PROTOCOL_FROZEN`.

The gate is supported by the Figure 2 diagnostic correction, APS audit and classification, estimator/CI documentation, duration and class-prior audit, frozen R1/R2/R3 protocol, strong-backbone selection, reference audit, manuscript revision maps, tests, and protocol hash.

## 3. Submission Suspension State
`SUBMISSION_SUSPENDED_FOR_SCIENTIFIC_REMEDIATION`. The JBHI package remains historical and is not submission-ready. No JBHI portal was opened.

## 4. Historical Evidence Integrity
The canonical manuscript, canonical PDFs, Step 20 package, B0 v1.2, B1 results, Step 15.3, Step 16, Step 17, and Step 19.1 artifacts were preserved. Corrections are versioned under `reports/step20_1_*` and `reports/remediation/`. The Step 20 venue package was not rewritten.

## 5. Figure 2 Forensic Audit
The plotting path in `scripts/step19_revision.py` passes the metric values as the `y` argument to `matplotlib.axes.Axes.plot`; the x labels C0--C5 are categorical condition labels only. The y values are read as numeric canonical point estimates. The suspected numeric-as-categorical y bug was not confirmed. The source-data audit is `reports/step20_1_fig2_plot_semantics_audit.csv`.

## 6. Figure 2 Macro-F1 Defect
`FIG2_NUMERIC_AS_CATEGORICAL_BUG_NOT_CONFIRMED`. The D1 sequence is non-monotonic, including the required C0--C5 values `0.7479976, 0.6633590, 0.4662659, 0.5948987, 0.5063910, 0.2895546`. The regression assertion passed. D2 and all plotted y values were also checked as floats. Test: `reports/step20_1_fig2_regression_test.txt`.

## 7. Figure 2 Conformal Defect
`FIG2_CONFORMAL_FIELD_BINDING_BUG_CONFIRMED`. The field named `gap_0.1` is computed as signed `nominal_coverage - empirical_coverage` (`1-alpha - coverage`), but the panel was labeled absolute coverage gap. Negative values were therefore displayed under an absolute-gap label. The exact wrong binding is recorded in the audit CSV.

## 8. Corrected Figure 2 Preview
A versioned corrected diagnostic was generated at `reports/remediation/fig2_b0_shift_landscape_corrected_preview.pdf`. It keeps numeric y coordinates and plots `abs(gap_0.1)` under an absolute-gap label. The canonical paper figure and manuscript were not replaced. A clean future caption is in `reports/step20_1_fig2_caption_recommendation.md`.

## 9. APS Implementation Audit
`src/shiftsleep_uq/evaluation_step11.py` uses cumulative uncalibrated softmax probability through the true class after deterministic descending-probability sorting. Calibration uses source CAL only, stores per-direction/per-seed q-hat values for alpha .10 and .05, and constructs the smallest prefix whose cumulative probability reaches q-hat. The finite-sample quantile is `k=ceil((n+1)(1-alpha))`, clamped to 1..n. No randomization, target calibration, or target tuning was found. Full component-level results are in `reports/step20_1_aps_implementation_audit.md`.

## 10. APS Published-Definition Comparison
The implementation matches the non-randomized APS cumulative-probability construction used in Romano, Sesia, and Candès, “Classification with Valid and Adaptive Coverage,” NeurIPS 2020. Sorting, score definition, quantile rule, source-only calibration, prefix construction, and deterministic ties are `MATCH`. No component was classified as `BUG`. The signed/absolute Figure 2 problem is a reporting-field defect, not an APS implementation defect.

## 11. Source-Domain Conformal Sanity
Existing source TEST prediction artifacts were read without new inference. The audit contains 36 rows: 2 directions × 3 source conditions × 3 seeds × 2 alpha values. Source coverage is approximately 0.9996--1.000 in the audited C0--C2 rows, with q-hat effectively 1.0 and non-trivial set sizes. This is conservative but expected from the implemented non-randomized APS behavior; exact values are in `reports/step20_1_source_conformal_sanity.csv`.

## 12. Prediction-Set Size Distribution
`reports/step20_1_aps_set_size_distribution.csv` reports coverage, mean and median set size, and P(size=1) through P(size=5) for every direction, source condition, seed, and alpha .10/.05. The distribution confirms that coverage alone is insufficient: high coverage can coexist with large prediction sets and low singleton fractions.

## 13. Conformal Metric Interpretation
Absolute distance from nominal coverage is a descriptive axis, not a complete reliability score. If source coverage is far above .90, a target condition moving closer to .90 can look favorable even while set size increases or predictive/selective quality worsens. Future reporting must pair coverage gap with set-size distribution, predictive metrics, and selective metrics. Full note: `reports/step20_1_conformal_metric_interpretation_audit.md`.

## 14. Conformal Audit Classification
`APS_PRIMARY_AXIS_REQUIRES_REFRAMING`. APS is valid, but the absolute coverage-gap axis cannot be interpreted alone under strong source conservatism.

## 15. R1 Conformal Sensitivity Protocol
R1 is frozen as a secondary method sensitivity. It will use randomized APS if compatible with the discrete implementation; otherwise it will use RAPS with hyperparameters frozen from published defaults or source-only tuning. Calibration remains source CAL only. No target labels or target hyperparameter selection are allowed. Historical APS results remain primary historical evidence until future execution determines otherwise.

## 16. Weighted-Conformal Literature Positioning
Tibshirani et al., “Conformal Prediction Under Covariate Shift,” is required related work. It addresses covariate shift through importance weighting. It is conceptually relevant, but adoption would require target-covariate or density-ratio information and is not automatically compatible with the strict source-only deployment setting. Weighted conformal was not implemented.

## 17. Ovadia Literature Positioning
Ovadia et al., “Can You Trust Your Model’s Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift,” will be added to the positioning. It establishes prior evaluation of predictive uncertainty under dataset shift. The manuscript must not claim that uncertainty/predictive decoupling under generic shift is itself novel.

## 18. Novelty Repositioning
The frozen narrower claim is: controlled reciprocal evaluation of dataset shift × missing-modality shift in sleep staging across predictive performance, calibration, uncertainty ranking, selective prediction, and conformal behavior, together with a controlled missing-modality exposure intervention. Full wording: `reports/step20_1_novelty_repositioning.md`.

## 19. Table 2 / Table 3 Estimator Provenance
Table 2 uses the full-population point estimate from the canonical B0 multiseed result table. Table 3's B0 value is the mean of the frozen subject-bootstrap replicate values used in the paired B1-minus-B0 estimator. The paired procedure computes each seed's metric within a subject bootstrap replicate, averages the three seed-specific values, and forms B1 minus B0 within that replicate. These are not merely display-rounding variants.

## 20. Point-Estimate Decision
`DIFFERENT_VALID_ESTIMANDS`. Both estimates are defensible for their purposes, but future manuscript tables must label Table 2 as the full-population seed-mean point estimate and Table 3 as the paired bootstrap-mean point estimate. Historical artifacts remain unchanged.

## 21. Bootstrap Estimand
Each replicate resamples subjects with replacement using the exact duplicate-preserving multiplicities, computes the metric independently for seeds 17, 42, and 2026, averages those seed-specific values, and then forms the paired B1-minus-B0 difference within the replicate. Percentile limits use the resulting 2,000 paired replicates. Details: `reports/step20_1_bootstrap_estimand.md`.

## 22. Seed Variability
`reports/step20_1_primary_seed_variability.csv` contains D1 C4, D1 C5, D2 C4, and D2 C5 seed-specific deltas, mean, sample SD, minimum, maximum, and a pointer to the frozen three-seed bootstrap CI. No new runs were made. Seed variability is treated separately from subject-sampling uncertainty.

## 23. Multiplicity Audit
The primary inferential family is the four compound macro-F1 B1-minus-B0 contrasts: D1 C4, D1 C5, D2 C4, and D2 C5. Reliability and other contrasts are secondary. The historical analysis did not preregister a multiplicity correction, so no retrospective correction is presented as the original primary result.

## 24. Multiplicity Sensitivity Protocol
A post-hoc sensitivity is frozen for the four primary predictive contrasts using the frozen paired-bootstrap p-value construction and Holm correction at family-wise alpha .05. It will be labeled sensitivity only and will not replace historical confidence intervals. Future R2/R3 confirmatory families will declare multiplicity prospectively.

## 25. Sleep-EDF Duration Audit
Using the frozen processed recording ledgers, 153 Sleep-EDF SC recordings were audited. Included duration median was 22.92 hours, IQR 22.25--23.33 hours, range 17.00--24.00 hours, and total included epochs 414,961. Class counts and per-recording duration/class counts are in `reports/step20_1_dataset_duration_class_distribution.csv`.

## 26. ISRUC Duration Audit
Using the frozen ISRUC v2 ledger, 99 ISRUC recordings were audited. Included duration median was 7.48 hours, IQR 7.18--7.86 hours, range 6.23--8.85 hours, and total included epochs 89,312. The audit uses only `isruc_s1` recordings and excludes determinism fixtures.

## 27. Class-Prior Shift Audit
The audited Wake proportions are 0.688 for Sleep-EDF and 0.229 for ISRUC; the absolute Wake difference is 0.459. Stage-wise absolute proportion differences are recorded in `reports/step20_1_class_prior_shift_audit.csv`; the five-class Jensen--Shannon divergence is 0.1194. This is a descriptive composition difference, not a causal claim.

## 28. Sleep-Window Literature Review
The official PhysioNet Sleep-EDF page states that the Sleep Cassette recordings are whole-night polysomnographic recordings, with two recordings of about 20 hours each at subjects' homes, and that the expanded resource contains 153 SC files. It also provides the Kemp et al. original publication and a standard PhysioNet citation. The long recording-duration concern is therefore supported, not dismissed.

## 29. R2 Harmonized-Window Protocol
`SLEEP_WINDOW_HARMONIZED_SENSITIVITY_V1` is frozen. For each recording in both datasets, onset is the first scored non-Wake sleep epoch and termination is the last scored non-Wake sleep epoch. Retain exactly 30 minutes of scored epochs before onset, the complete scored interval between bounds, and exactly 30 minutes after termination. Apply the same rule in both datasets, exclude invalid/unscored epochs under the original label rules, reuse frozen subject partitions, and refit normalization on source TRAIN only. No target result may choose the window.

## 30. Strong-Backbone Candidate Review
DeepSleepNet, SeqSleepNet, U-Sleep, and SleepTransformer were considered. DeepSleepNet has limited sequence context relative to the request; U-Sleep has a larger temporal/architectural footprint and greater implementation burden; SleepTransformer has higher memory and tuning risk. SeqSleepNet is peer-reviewed, established for sleep staging, recurrent/sequence-to-sequence, compatible with EEG/EOG inputs, already represented by a verified DOI in the bibliography, and has a public implementation lineage.

## 31. Selected Strong Backbone
`SeqSleepNet_class` was selected for R3. Selection is based on reproducibility and protocol compatibility, not expected result direction. It is not being executed in Step 20.1.

## 32. Hardware Feasibility
On the RTX 3060 Laptop GPU with 6 GB VRAM, the provisional plan is sequence length 20, batch size 8 with mixed precision where supported, and gradient accumulation if required. The estimate is a feasible starting configuration, not a completed benchmark. A short implementation preflight must verify memory before any R3 training. The stop rule is `STRONG_BACKBONE_CONFIRMATION_BLOCKED` if reproducibility or memory requires material protocol change.

## 33. R3 Strong-Backbone Protocol
R3 compares S0, standard full-modality source training, with S1, the identical SeqSleepNet configuration using source modality exposure FULL 0.50, EEG-only 0.25, and EOG-only 0.25. Both directions, C0--C5, and seeds 17/42/2026 are required. Primary cells are D1 C4, D1 C5, D2 C4, and D2 C5. Primary prediction metric is macro-F1; calibrated NLL and entropy AURC are reliability axes. Conformal reporting is conditional on the Step 20.1 audit interpretation.

## 34. Bibliography Forensic Audit
All 19 current bibliography entries were reviewed against Crossref/publisher metadata where resolvable. Seventeen DOI entries resolved; one entry has no DOI and remains explicitly marked for publisher-record review; the Guo DOI failed resolution and is classified incorrect. The complete audit is `reports/step20_1_reference_forensic_audit.csv`. The audit does not silently modify the bibliography.

## 35. Guo DOI Resolution
The DOI `10.1145/3065386.3065389` on Guo et al. 2017 did not resolve in Crossref and is classified `FAIL_INCORRECT_DOI`. Future bibliography correction will remove the DOI unless an authoritative publisher record supplies a verified replacement. No replacement was invented.

## 36. Sleep-EDF Citation Resolution
The toolbox citation is insufficient as the primary dataset provenance citation. The future bibliography will add Kemp et al. (2000), “Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG,” and the official PhysioNet standard citation identified on the current Sleep-EDF provider page. The Imtiaz/Rodriguez-Villegas toolbox citation remains supplementary provenance.

## 37. New Required References
Future additions are frozen as required: Ovadia et al. 2019; Tibshirani et al. 2019; Romano, Sesia, and Candès 2020 APS; Kemp et al. 2000 Sleep-EDF provenance; and the current PhysioNet standard citation. No final manuscript bibliography was edited in Step 20.1.

## 38. Internal Workflow Language Audit
The manuscript and venue derivative contain workflow-oriented terms including Step identifiers, gate/frozen-artifact language, and machine-oriented identifiers. A future revision map replaces these with “prespecified post-hoc diagnostic analysis,” “decision rule,” and “prespecified result” where scientifically accurate. Full audit: `reports/step20_1_internal_language_audit.csv`.

## 39. Table 4 Redesign
Remove constant columns such as `Simple calibration = Persists` and `Oracle = Diagnostic` from the table body. Retain only cell-varying diagnosis and move global facts to caption/prose. Recommendation: `reports/step20_1_table4_redesign.md`.

## 40. Numeric Precision Policy
Future main-paper displays default to three decimals for macro-F1, deltas, CI endpoints, NLL, AURC, and related metrics. Full precision remains in machine-readable supplements and raw artifacts. No raw result files were altered. Policy: `reports/step20_1_precision_policy.md`.

## 41. Manuscript Tone Revision Map
Necessary limitations remain, including no prospective clinical validation, no target adaptation, no SHHS, and diagnostic/oracle status. Repetitive “does not claim,” “not safe,” and “not a method” disavowals should be consolidated into a concise limitations paragraph. Workflow terms should be removed from the reader-facing manuscript. Map: `reports/step20_1_manuscript_tone_revision_map.md`.

## 42. Positive Claim Freeze
Under reciprocal cross-dataset and missing-modality evaluation, source-side modality exposure improves predictive robustness in several compound conditions, while calibration, selective prediction, and conformal behavior do not improve uniformly.

## 43. Confirmatory / Exploratory Labels
Original B0/B1: `PRIMARY_HISTORICAL`. R2 harmonized-window B0/B1: `CONFIRMATORY_SENSITIVITY`. R3 SeqSleepNet S0/S1: `CONFIRMATORY_GENERALIZATION`. R1 randomized APS/RAPS: `SECONDARY_METHOD_SENSITIVITY`.

## 44. Remediation Protocol YAML
`configs/postreview_remediation_protocol_v1.yaml` freezes R1/R2/R3 rules, seeds, conditions, metrics, source-only calibration, subject bootstrap, 2,000 replicates, bootstrap seed 2028, Holm sensitivity, stop rules, and artifact namespaces. The YAML was created before any R2/R3 outcome.

## 45. Protocol Hash
SHA-256: `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`. Recorded in `reports/step20_1_remediation_protocol_hash.txt`.

## 46. Tests Added
Added deterministic Figure 2 regression assertions for numeric y coordinates and the required non-monotonic D1 macro-F1 sequence. Added generated source conformal sanity and prediction-set distribution audits. Added protocol hash verification artifact. No training or model-inference test was run.

## 47. Files Created
- `configs/postreview_remediation_protocol_v1.yaml`
- `scripts/step20_1_remediation.py`
- `scripts/step20_1_reference_audit.py`
- `reports/step20_1_fig2_plot_semantics_audit.csv`
- `reports/step20_1_fig2_regression_test.txt`
- `reports/remediation/fig2_b0_shift_landscape_corrected_preview.pdf`
- `reports/step20_1_aps_implementation_audit.md`
- `reports/step20_1_source_conformal_sanity.csv`
- `reports/step20_1_aps_set_size_distribution.csv`
- `reports/step20_1_conformal_metric_interpretation_audit.md`
- `reports/step20_1_novelty_repositioning.md`
- `reports/step20_1_point_estimator_provenance.csv`
- `reports/step20_1_bootstrap_estimand.md`
- `reports/step20_1_primary_seed_variability.csv`
- `reports/step20_1_dataset_duration_class_distribution.csv`
- `reports/step20_1_class_prior_shift_audit.csv`
- `reports/step20_1_reference_forensic_audit.csv`
- `reports/step20_1_internal_language_audit.csv`
- `reports/step20_1_table4_redesign.md`
- `reports/step20_1_precision_policy.md`
- `reports/step20_1_manuscript_tone_revision_map.md`
- `reports/step20_1_remediation_protocol_hash.txt`

## 48. Files Modified
No canonical manuscript, canonical PDF, supplement, Step 20 venue derivative, historical result, or raw artifact was modified. Only the new Step 20.1 generator scripts and versioned audit/report outputs were added. `reports/step20_1_point_estimator_provenance.csv` and `reports/step20_1_internal_language_audit.csv` are required named outputs and must be completed before commit if not already present.

## 49. Explicitly Not Done
- no new model training;
- no new model inference;
- no new calibration;
- no new bootstrap execution;
- no R2 execution;
- no R3 execution;
- no target adaptation;
- no SHHS analysis;
- no protocol change to historical experiments;
- no submission;
- no Step 21;
- no Step 20.2.

## 50. Remaining Risks
The APS alternative still requires future implementation and execution. The publisher record for one no-DOI reference and exact official proceedings metadata for the planned Ovadia/Tibshirani/APS additions must be finalized before manuscript revision. SeqSleepNet hardware feasibility is a preflight estimate until an implementation is exercised. Historical Table 2/Table 3 labels and manuscript workflow language remain unrevised by design. R2/R3 may weaken, overturn, or qualify the positive claim; their purpose is not to preserve it.

## 51. Recommended Next Step
# Step 20.2 — Execute the Frozen Post-Review Remediation Experiments

Do NOT execute Step 20.2 in this step.

## 52. Git Commit
Created commit `e1ae2798c14a6863bfc9e6a0578823d58593bd8d` with message `research: freeze post-review scientific remediation protocol`.

## 53. GitHub Push Status
The commit was pushed successfully to `origin/main`; local `main` and `origin/main` resolve to the same commit.

## 54. Git Status / Diff Summary
The Step 20.1 package is committed and synchronized. Canonical PDF hashes remain unchanged. Four unrelated historical Step 18 report files remain untracked and were deliberately not bundled: `reports/STEP_18_MANUSCRIPT_DRAFT_REPORT.md`, `reports/step18_citation_audit.csv`, `reports/step18_manuscript_claim_audit.csv`, and `reports/step18_section_evidence_map.md`. They are outside this step's scope.
