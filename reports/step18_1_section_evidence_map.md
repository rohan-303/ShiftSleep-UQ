# Step 18.1 Section Evidence Map

## Title and abstract
- Repository evidence: `reports/step17_title_candidates.md`, `reports/step17_abstract_evidence_skeleton.md`, `reports/paper_tables/table3_b1_vs_b0_compound_effects.csv`.
- No external citation is used to strengthen the frozen title or abstract claims.

## Introduction
- External context: `supratak2017deepsleepnet`, `phan2019seqsleepnet`, `perslev2021usleep`, `zhou2022dgsurvey`, `thagaard2020uncertaintyshift`, `angelopoulos2023conformal`.
- Frozen contribution source: `reports/step17_contribution_statement_v1.md`.

## Related Work
- Automatic staging: DeepSleepNet, SeqSleepNet, TinySleepNet, U-Sleep, SleepTransformer.
- Cross-dataset/domain generalization: Zhao et al., Zhou et al., Zhu et al., Zhou et al. survey.
- Multimodal/missing-modality context: Sleep CLIP plus frozen B1 evidence.
- Uncertainty/calibration/selective prediction: SleepTransformer, Direct Quantification, Guo et al., SelectiveNet, Thagaard et al., JAWS.
- Conformal prediction: Angelopoulos and Bates; Dey et al.
- Full metadata and relevance: `reports/step18_1_literature_evidence_matrix.csv`.

## Methods
- Dataset and partitions: `reports/paper_tables/table1_benchmark_design.csv`, `reports/step17_methods_evidence_map.md`.
- B0/B1: frozen B0/B1 reports, `reports/b1_training_summary_v1.csv`.
- Calibration/conformal: frozen methods map and Step 16 diagnostics.
- Statistical engine: weighted-ranking gate and B0 v1.2 provenance.

## Results
- B0 shift landscape: Table 2 and Figure 2.
- B1 compound effects: Table 3 and Figure 3.
- Residual diagnosis: Table 4 and Figures 4-5.
- Selective prediction: Figure 6.
- Conformal transfer: Figure 7.
- Stage behavior: Figure 8 and supplementary artifacts.
- All results are from frozen Step 17 and earlier artifacts; no literature-derived result appears in Results.

## Discussion
- Repository evidence: `reports/step17_claim_evidence_matrix_v1.csv`, `reports/step17_nonclaims_v1.md`, `reports/step17_limitations_v1.md`, Step 16 method gate.
- External contextual citations: calibration, uncertainty-under-shift, selective prediction, and conformal references listed above.

## Limitations and conclusion
- Frozen sources: Step 17 limitations, non-claims, contribution statement, and claim matrix.
- The conclusion does not introduce a new method, clinical claim, SHHS result, or universal uncertainty claim.

## Rendered-paper QA
- Figure audit: `reports/step18_1_figure_render_audit.csv`.
- Table audit: `reports/step18_1_table_render_audit.csv`.
- Warning audit: `reports/step18_1_latex_warning_audit.csv`.
- Rendered pages: local QA images under `reports/step18_1_pdf_render/`; these are temporary inspection artifacts and are not manuscript evidence.
