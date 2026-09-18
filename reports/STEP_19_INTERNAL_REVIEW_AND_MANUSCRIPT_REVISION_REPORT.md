# ShiftSleep-UQ Step 19 Internal Review and Manuscript Revision Report

## 1. Status
Step 19 completed the internal reviewer-style audit, presentation repairs, substantive table revisions, Figure 2 source audit and correction, structured supplement creation, claim/citation/numerical audits, compilation, and rendered inspection. The final filesystem handoff is blocked only because the existing `paper/main.pdf` is held open by another process and could not be replaced atomically; the revised candidate is verified at `paper/main_step19_candidate.pdf` and its build copy at `paper/build_main/main.pdf`.

## 2. Internal Review Gate
`INTERNAL_REVIEW_PARTIAL`.

The scientific and manuscript revisions are complete, but the required canonical `paper/main.pdf` replacement and push are not claimed because the current file is locked. No Step 20 work was performed.

## 3. Starting Manuscript State
The starting Step 18.1 manuscript PDF SHA-256 was verified as `85aaca5faf0d5155a18f32ddfac54ce64053325355e4a43bd37ae63f756c73d5`. Repository branch was `main`; starting HEAD was verified before revision. The historical Step 18 and Step 18.1 reports were preserved.

## 4. Frozen Evidence Integrity
Required gates remain `B0_V1_2_AUTHORITATIVE`, `WEIGHTED_RANKING_ENGINE_FROZEN`, `B1_PRIMARY_EVALUATION_COMPLETE`, `STEP16_METHOD_GATE_COMPLETE`, `RELIABILITY_METHOD_NOT_AUTHORIZED`, and `BENCHMARK_SYNTHESIS_FROZEN`. No model, prediction, calibration, bootstrap, partition, Step 17 table, Step 17 figure, or scientific result artifact was overwritten. Manuscript-specific derivative figures are versioned.

## 5. Reviewer 1 Summary
The benchmark contribution is defensible when framed as controlled evaluation rather than a new model or leaderboard. The main concerns were two-dataset external validity, modest architectural scope, and the need to show the full B0 landscape. Table 2 and the limitations were revised accordingly. Full report: `reports/step19_reviewer1_scientific_novelty.md`.

## 6. Reviewer 2 Summary
The subject-level protocol, three seeds, 2,000-replicate bootstrap, source-only calibration firewall, and B0 v1.2 repair are reproducible when tied to the frozen artifacts. The original Figure 2 source-data binding and representative seed presentation required repair/clarification. Full report: `reports/step19_reviewer2_methods_statistics.md`.

## 7. Reviewer 3 Summary
Dataset provenance, ISRUC montage families, the excluded unsupported layout, stage interpretation, and non-clinical scope were reviewed. Sleep-EDF and ISRUC citations were added, while no unsupported ethics or clinical claim was introduced. Full report: `reports/step19_reviewer3_sleep_domain.md`.

## 8. Reviewer 4 Summary
Presentation improved materially through substantive tables, versioned figures, clearer captions, and a real supplement source. Eight figures remain too many for some venue formats; venue-specific reduction is deferred. Full report: `reports/step19_reviewer4_presentation.md`.

## 9. Meta-Review
No scientific blocking concern remains after revision. Major concerns are external validity, benchmark-versus-method positioning, and future venue adaptation. Moderate concerns are seed-17 qualitative display, montage contracts, and supplement synchronization. Full report: `reports/step19_meta_review.md`.

## 10. Blocking Concerns
The only remaining completion blocker is an operating-system file lock on the pre-existing `paper/main.pdf`. The revised candidate was successfully compiled and rendered but cannot be renamed over the locked canonical path in this session.

## 11. Major Concerns
The paper remains limited to two core datasets and two reciprocal directions; it is not a universal domain-generalization study. It reports a controlled B1 intervention, not a new reliability method. Venue-specific figure count, formatting, authorship, and final reproducibility packaging remain future work.

## 12. Figure 2 Source Audit
Created `reports/step19_fig2_source_audit.csv` with 48 rows covering D1/D2, C0--C5, macro-F1, NLL, AURC, and absolute alpha-.10 coverage gap. The original source CSV marked macro-F1 as `NOT_AVAILABLE_IN_B0_PER_SEED_TABLE`; its other values also did not exactly equal the canonical bootstrap table values. The audit therefore confirms `FIG2_PRESENTATION_BINDING_DEFECT_CONFIRMED`.

## 13. Figure 2 Resolution
Created `paper/figures/fig2_b0_shift_landscape_v2.pdf` from the canonical `reports/b0_primary_results_multiseed_v1_2.csv` values only. The frozen Step 17 figure was preserved. Main text now uses the versioned manuscript derivative and labels it as such.

## 14. Full Figure Source Audit
Created `reports/step19_figure_source_audit.csv` with source-row checks for Figures 3--8. Figure 3 uses the four frozen macro-F1 deltas/CIs. Figure 4 uses the frozen NLL/AURC/conformal-gap paired effects. Figure 5 uses the same frozen paired values. Figure 6 contains 808 rows for four cells, B0/B1, and seed 17; it is explicitly qualitative and representative, while inferential AURC uses all three seeds. Figure 7 uses frozen coverage/set-size source rows. Figure 8 uses frozen stage-recall changes. A clearer versioned Figure 1 schematic was also created at `paper/figures/fig1_shift_design_v2.pdf`.

## 15. Table 1 Revision
Table 1 now visibly reports direction, source, target, TRAIN, DEV, CAL, source TEST, and target cohort counts, while retaining the C0--C5 definition in prose. The visible transfer rows are D1: 47/12/8/0 and target cohort 99; D2: 59/15/10/0 and target cohort 78, matching the frozen design accounting and cohort totals.

## 16. Table 2 Revision
Table 2 now contains all 12 D1/D2 C0--C5 rows and canonical point estimates for macro-F1, NLL, AURC, and absolute alpha-.10 coverage gap. The authoritative machine-readable derivative is `reports/paper_tables/table2_b0_primary_shift_results_v2.csv`.

## 17. Table 3 Revision
Table 3 retains the exact four frozen deltas and CIs and adds B0 and B1 point values for interpretability. D2 C5 remains explicitly inconclusive.

## 18. Table 4 Revision
Table 4 now includes predictive status, NLL/AURC direction, conformal direction, simple source calibration outcome, and oracle status. It explicitly states that these are qualitative metric-family summaries, not a single reliability score.

## 19. Figure Prioritization
Figure 1: `MAIN_REQUIRED` for protocol comprehension. Figure 2: `MAIN_REQUIRED` for the B0 landscape. Figures 3 and 4: `MAIN_REQUIRED` for primary B1 and reliability results. Figure 5: `MAIN_OPTIONAL` because it summarizes decoupling already shown in Table 4. Figure 6: `MAIN_REQUIRED` for selective behavior, with the seed-17 caveat. Figure 7: `MAIN_OPTIONAL`/supplement-preferred under a tight venue limit. Figure 8: `SUPPLEMENT_PREFERRED` because it is stage-level secondary detail. No evidence was removed in this venue-neutral candidate.

## 20. Figure Layout Revision
Versioned Figure 1 and Figure 2 were generated with clearer labels and manuscript-specific captions. The remaining frozen figures were not regenerated because their source-row audits passed. The candidate remains a full-version layout with figures collected after the main text; venue-specific float placement is deferred.

## 21. Abstract Revision
The abstract was reviewed and retained at approximately 245 words. It states the benchmark, reciprocal datasets, B0/B1 comparison, all four primary deltas, heterogeneous reliability, and bounded non-claims without stuffing additional cohort counts.

## 22. Introduction Revision
The introduction retains the compound-shift gap, explains why accuracy is insufficient, separates reliability axes, and avoids priority claims. No unsupported novelty statement was added.

## 23. Related Work Revision
Related Work now balances automatic staging, domain adaptation/generalization, missing modalities, calibration, selective prediction, uncertainty under shift, and conformal prediction. Two verified dataset-provenance citations and uncertainty-under-shift context citations were added. The revised bibliography contains 19 verified entries.

## 24. Methods Revision
Methods now exposes dataset provenance, montage families, source-only firewall, subject-level bootstrap semantics, seed count, B0 v1.2 repair, and calibration/conformal definitions. The supplement records architecture/training and the frozen artifact map without adding experiments.

## 25. Results Revision
Results now quantify the B0 landscape with 12 rows, selected D1/D2 B0 values, selected reliability deltas, B0/B1 compound points, and the D2 C5 negative/inconclusive result. No frozen result was changed.

## 26. Discussion Revision
Discussion was checked for domain-shift, missing-modality, uncertainty, conformal, and D2 C5 interpretation. It remains cautious and does not invent mechanisms. Predictive robustness and reliability robustness remain separate conclusions.

## 27. Limitations Revision
Limitations retain two-dataset scope, montage constraints, epoch-wise architecture, no SHHS core validation, no arbitrary-shift conformal guarantee, direction-specific behavior, and unresolved D2 C5. Clinical safety and deployment claims remain explicitly excluded.

## 28. Dataset / Ethics Revision
Verified Sleep-EDF Expanded and ISRUC citations were added. Ethics language remains cautious secondary-data wording and does not invent IRB approvals or exemptions.

## 29. Data and Code Availability Revision
The manuscript points to the repository evidence package, deterministic synthesis script, provider-controlled data access, and excluded raw/heavy/credential artifacts. It does not claim raw-data redistribution.

## 30. Supplement Creation
Created and compiled `paper/supplement.tex` and `paper/supplement.pdf`. The supplement is a separate two-page structured companion containing S1--S11, the compact canonical B0 table, frozen artifact paths, and frozen non-claims. It does not introduce new analysis.

## 31. Claim Audit
Created `reports/step19_claim_audit_v1.csv` with 9 important claims. All retained claims are `SUPPORTED` or `QUALIFIED`; no unsupported retained claim remains.

## 32. Citation Audit
Created `reports/step19_citation_audit_v1.csv`. All 19 bibliography entries are used and marked `VERIFIED`; the final bibliography contains 19 verified references.

## 33. Numerical Audit
Created `reports/step19_numerical_audit_v1.csv` with 8 selected numerical checks. Exact frozen deltas/CIs and rounded canonical B0/reliability values were verified against the Step 17 artifacts.

## 34. Revised Manuscript Word Count
The revised main-text source is approximately 4,800 words excluding bibliography and figure-plan material. The draft is venue-neutral and not padded to an arbitrary quota.

## 35. Revised PDF Page Count
The revised candidate main PDF is 18 pages. The separate supplement is 2 pages.

## 36. Main Figure Count
Eight figures remain in the full manuscript candidate. Figures 1 and 2 are manuscript-specific versioned derivatives; Figures 3--8 remain frozen presentation files whose source audits passed.

## 37. Supplement Figure/Table Count
The supplement contains 0 figures and 2 rendered tables, plus S1--S11 structured artifact references and one compact B0 table. It is intentionally compact rather than a duplication of multi-megabyte CSV files.

## 38. LaTeX Compilation
Main candidate: TinyTeX `pdflatex` and BibTeX completed successfully; final pdflatex pass returned 0 with no undefined citations, undefined references, overfull boxes, or fatal errors. Supplement: `latexmk` returned 0 and produced `paper/supplement.pdf`. The canonical main path could not be replaced because of the external file lock.

## 39. Rendered PDF Audit
Created `reports/step19_render_audit_v1.csv`. The 18-page main candidate and 2-page supplement were rendered to PNG contact sheets and visually inspected. No clipping, blank page, table overflow, unreadable figure, or broken supplement page was observed.

## 40. Remaining Reviewer Concerns
The canonical main PDF must be replaced after the external lock is released. Venue-specific adaptation, author metadata, acknowledgments, final figure reduction, and final reproducibility-package review remain. These are not silently claimed complete.

## 41. Submission Candidate Status
`SUBMISSION_CANDIDATE_V1` for the revised candidate artifact, but the Step 19 gate remains `INTERNAL_REVIEW_PARTIAL` until the canonical `paper/main.pdf` path is replaced and verified.

## 42. Manuscript Provenance
Created `reports/step19_manuscript_provenance_v1.json`. It records hashes for main source, current main PDF, revised candidate PDF, supplement, bibliography, frozen manifest, and the required scientific gates. Candidate PDF SHA-256 is recorded there.

## 43. Files Created
- `paper/main_step19_candidate.pdf`
- `paper/supplement.tex`
- `paper/supplement.pdf`
- `paper/figures/fig1_shift_design_v2.pdf`
- `paper/figures/fig2_b0_shift_landscape_v2.pdf`
- `reports/step19_fig2_source_audit.csv`
- `reports/step19_figure_source_audit.csv`
- `reports/step19_claim_audit_v1.csv`
- `reports/step19_citation_audit_v1.csv`
- `reports/step19_numerical_audit_v1.csv`
- `reports/step19_render_audit_v1.csv`
- `reports/step19_manuscript_provenance_v1.json`
- `reports/step19_reviewer1_scientific_novelty.md`
- `reports/step19_reviewer2_methods_statistics.md`
- `reports/step19_reviewer3_sleep_domain.md`
- `reports/step19_reviewer4_presentation.md`
- `reports/step19_meta_review.md`
- `reports/step19_internal_response_to_reviewers.md`

## 44. Files Modified
- `paper/main.tex`
- `paper/references.bib`
- `scripts/step19_revision.py`
- `scripts/step19_audits.py`

## 45. Explicitly Not Done
- no training;
- no inference;
- no new calibration;
- no new statistical test;
- no new model;
- no SHHS analysis;
- no protocol change;
- no B0/B1 scientific result modification;
- no Step 20;
- no Git commit or GitHub push, because the canonical revised `paper/main.pdf` could not be replaced while locked.

## 46. Recommended Next Step
# Step 20 — Select the Target Venue and Adapt the Frozen Submission Candidate to Its Requirements

Do NOT execute Step 20. Before that, release the external lock on `paper/main.pdf`, replace it with the verified candidate PDF, rerun hash/render checks, and then decide whether to commit/push Step 19 as complete.

## 47. Git Commit
No Step 19 commit was created because the required canonical PDF handoff is incomplete. The prior Step 18.1 commits remain untouched.

## 48. GitHub Push Status
`NOT_PUSHED`.

## 49. Git Status / Diff Summary
The worktree contains the Step 19 manuscript revisions, supplement, versioned figures, audits, reviewer reports, and build/render artifacts. The prior Step 18 historical untracked files remain untouched. Build and render intermediates are retained temporarily for verification and should be cleaned after the canonical PDF replacement is completed.
