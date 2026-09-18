# ShiftSleep-UQ Step 18.1 Manuscript Completion Report

## 1. Status
Step 18.1 completed the verified literature expansion, LaTeX compilation, rendered-paper inspection, figure/table QA, numerical consistency checks, and manuscript audit package. The frozen scientific evidence was preserved. The complete-draft gate is `MANUSCRIPT_DRAFT_COMPLETE`.

## 2. Manuscript Gate
`MANUSCRIPT_DRAFT_COMPLETE`.

The first complete draft is not a final submitted or publication-ready manuscript. Reviewer-style scientific audit and venue-specific revision remain future work.

## 3. Starting Step 18 State
The live repository was verified at `C:\Users\rohan\ShiftSleep-UQ`, branch `main`, starting HEAD `665a3afab1417910eabcb8dfd2077b7fce365428`. The Step 18 files were present before this pass. The historical report `reports/STEP_18_MANUSCRIPT_DRAFT_REPORT.md` was preserved and not overwritten.

## 4. Frozen Evidence Integrity
The Step 17 manifest was revalidated before manuscript changes. All 15 manifest artifact hashes matched. The verified gate is `BENCHMARK_SYNTHESIS_FROZEN`; B0 is v1.2; B1 Step 15.3 is frozen; Step 16 remains `STEP16_METHOD_GATE_COMPLETE` with `RELIABILITY_METHOD_NOT_AUTHORIZED`. No Step 17 tables, figures, numerical results, partitions, prediction bundles, checkpoints, bootstrap outputs, or diagnostics were modified.

## 5. Literature Search Strategy
A targeted metadata verification pass used Crossref DOI metadata and official publisher/proceedings metadata where needed. Exact title, author order, venue, year, publication type, peer-review status, DOI, and relevance were checked for every reference used. Search-result title similarity was not treated as sufficient evidence. Candidate works that could not be verified were recorded as `NOT_VERIFIED` and were not cited.

## 6. Final Bibliography Size
The final bibliography contains 17 verified references, all used in the manuscript. One verified conference paper, SelectiveNet, has `DOI_NOT_AVAILABLE` in the evidence matrix because no DOI was available in the verified publisher record. The bibliography contains no unresolved citation keys, placeholder entries, or fabricated DOI values.

## 7. Automatic Sleep-Staging Coverage
The Related Work section now covers DeepSleepNet, SeqSleepNet, TinySleepNet, TinySleepNet, U-Sleep, SleepTransformer, and direct uncertainty quantification in sleep staging. The final used set includes DeepSleepNet, SeqSleepNet, TinySleepNet, U-Sleep, SleepTransformer, and Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging. The section uses these papers to establish representative automatic, temporal, efficient, and uncertainty-aware sleep-staging work without presenting B0 as a state-of-the-art architecture.

## 8. Cross-Dataset / Domain-Generalization Coverage
The manuscript cites peer-reviewed sleep-staging domain-adaptation work covering unsupervised adaptation, source-free adaptation, and multi-source adaptation, together with a domain-generalization survey. The discussion is conservative: prior work is used to motivate reciprocal evaluation and shift-aware interpretation, not to claim that ShiftSleep-UQ is the first or only work combining these concerns.

## 9. Missing-Modality Coverage
The Related Work section cites verified multimodal sleep-staging work and connects it to the frozen B1 source-only modality-exposure control. The manuscript does not claim that Sleep CLIP or any cited prior work evaluated the ShiftSleep-UQ C0-C5 design. The project candidates CIMSleepNet and RMSSC could not be verified sufficiently and were not cited.

## 10. Sleep-Uncertainty Coverage
SleepTransformer and Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging are verified and used. They establish that sleep-staging uncertainty is an active research concern. The manuscript does not claim that either paper measured the frozen ShiftSleep-UQ benchmark.

## 11. Calibration Literature
Guo et al., “On Calibration of Modern Neural Networks,” was verified through ACM/Crossref metadata and added to the manuscript. It supports the general distinction between confidence calibration and classification accuracy. It is not used to claim that Guo et al. evaluated sleep staging.

## 12. Selective-Prediction Literature
SelectiveNet was verified from official CVPR proceedings metadata and used to contextualize reject-option and coverage-risk concepts. Its DOI is recorded as `DOI_NOT_AVAILABLE` rather than guessed. The manuscript continues to describe entropy as the preregistered ShiftSleep-UQ score, not as an optimal uncertainty score.

## 13. Conformal-Prediction Literature
Angelopoulos and Bates remains verified and used. Dey et al., “Conformal Prediction Sets for Ordinal Classification,” was added from verified NeurIPS/Crossref metadata. The manuscript explains exchangeability assumptions and explicitly avoids claiming formal arbitrary-shift coverage guarantees.

## 14. Previously Identified Candidate Verification

- **SleepDG:** `NOT_VERIFIED`. No authoritative exact metadata sufficient for citation was located in this pass.
- **CIMSleepNet:** `NOT_VERIFIED`. Exact title/metadata and relevance were not sufficiently verified.
- **U-PASS:** `NOT_VERIFIED`. Exact title/metadata and relevance were not sufficiently verified.
- **DREAM:** `NOT_VERIFIED`. The exact intended sleep-staging paper was not sufficiently verified.
- **Direct Quantification of Uncertainty:** `VERIFIED_AND_USED`. Exact title, authors, IEEE TBME venue, 2026 publication metadata, and DOI `10.1109/TBME.2025.3623380` were verified.
- **RMSSC:** `NOT_VERIFIED`. Exact title/metadata and incomplete-modality relevance were not sufficiently verified.
- **SF-UIDA:** `NOT_VERIFIED`. Exact title/metadata and intended relevance were not sufficiently verified.

All candidate statuses are recorded in `reports/step18_1_literature_evidence_matrix.csv`.

## 15. Literature Evidence Matrix
Created `reports/step18_1_literature_evidence_matrix.csv`. It contains every bibliography entry plus the previously identified candidates, with citation key, exact title, authors, venue, year, DOI or `DOI_NOT_AVAILABLE`, publication type, peer-review status, category, exact relevance, manuscript section, supported claim, verification source, and verification status.

## 16. Related Work Revision
`paper/main.tex` now contains five evidence-supported Related Work subsections: Automatic Sleep Staging; Cross-Dataset Generalization; Missing-Modality Robustness; Uncertainty, Calibration, and Selective Prediction; and Conformal Prediction Under Shift. The final positioning paragraph states that prior work addresses overlapping but non-identical strands and that ShiftSleep-UQ contributes a controlled reciprocal interaction study. No unsupported priority claim was added.

## 17. Introduction Citation Revision
The Introduction now uses citations for automatic sleep staging, temporal models, dataset/domain shift, uncertainty under shift, and conformal prediction. The four frozen ShiftSleep-UQ contributions remain unchanged. No new method contribution was introduced.

## 18. Discussion Citation Revision
The Discussion remains anchored in the frozen Step 17 claim matrix and uses external literature only for contextual interpretation. It distinguishes “our results show” from “prior work has reported,” retains the method-gate decision, and does not merge external results with ShiftSleep-UQ results.

## 19. Citation Audit
Created `reports/step18_1_citation_audit.csv`. All 17 used citation keys are marked `VERIFIED`. Citation keys resolve against `paper/references.bib`. The final LaTeX pass emitted no undefined citation warnings.

## 20. Manuscript Claim Audit
Created `reports/step18_1_manuscript_claim_audit.csv`. Major claims are classified as `SUPPORTED_REPOSITORY`, `SUPPORTED_LITERATURE`, `SUPPORTED_BOTH`, or `QUALIFIED`. No `REMOVE` row remains. D2 C5, target-oracle interpretation, conformal transfer, clinical implications, and non-authorization of a learned method remain qualified.

## 21. LaTeX Toolchain
The existing user-local TinyTeX installation was used. Detected tools include:

- `latexmk`: `C:\Users\rohan\AppData\Roaming\TinyTeX\bin\windows\latexmk`
- `pdflatex`: `C:\Users\rohan\AppData\Roaming\TinyTeX\bin\windows\pdflatex`
- `xelatex`: available
- `lualatex`: available

No unrelated software was installed.

## 22. Compilation Result
Compilation passed with the complete multi-pass sequence:

1. `latexmk -C main.tex`
2. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
3. `bibtex main`
4. `pdflatex -interaction=nonstopmode -halt-on-error main.tex`
5. `pdflatex -interaction=nonstopmode -halt-on-error main.tex`

Observed results: `latexmk RC=0`, `bibtex RC=0`, second `pdflatex RC=0`, and third `pdflatex RC=0`. The final log contains no undefined citations, undefined references, missing figures, missing bibliography entries, overfull boxes, underfull boxes, float-too-large warnings, duplicate labels, or fatal package errors.

## 23. PDF Path and Hash
PDF path: `paper/main.pdf`

SHA-256:

`85aaca5faf0d5155a18f32ddfac54ce64053325355e4a43bd37ae63f756c73d5`

The PDF was generated from the current `paper/main.tex` and `paper/references.bib`.

## 24. Page Count
The compiled manuscript contains 17 pages, including references and the supplementary-material figure plan.

## 25. Main-Text Word Count
Approximate main-text source word count, excluding the bibliography and figure-plan material: 4,504 words. The abstract contains approximately 245 words. The draft is materially shorter than the original 8,000-10,000-word target, but it is scientifically dense rather than padded. Additional length would require substantive expansion during Step 19 or venue-specific revision, not filler added during completion QA.

## 26. Abstract Word Count
Approximately 245 words. It remains within the requested 200-300-word range and contains the exact four frozen compound macro-F1 effects without overloading the abstract with secondary metrics.

## 27. Figure Render Audit
Created `reports/step18_1_figure_render_audit.csv`. All eight frozen PDFs were resolved in the compiled manuscript and inspected page by page in rendered PNG output. Figures 1-8 were accepted for legibility, labels, markers/legends, caption consistency, and absence of clipping or overlap. Rendered figure pages were 13-17.

The rendered inspection showed no blank figure pages, clipping, overlapping content, or unreadable axes. Figure dimensions were constrained with `keepaspectratio` to remove the earlier float-height warning.

## 28. Table Render Audit
Created `reports/step18_1_table_render_audit.csv`. Tables 1-4 were compiled and inspected. All four have readable labels, captions, precision, confidence-interval formatting where applicable, and no margin overflow. Table 4 residual diagnosis was added as a compact in-manuscript table linked to the complete frozen Step 17 diagnostic artifact.

## 29. LaTeX Warning Audit
Created `reports/step18_1_latex_warning_audit.csv`. The final compilation has no blocking warnings. Earlier first-pass issues were repaired: the unescaped `R&K` text was changed to `R\&K`, bibliography processing was completed with BibTeX, figure heights were constrained, and emergency stretch removed the overfull-box warning. The final warning audit classifies all checked warning types as `ACCEPTED_BENIGN` with no observed unresolved issue.

## 30. Numerical Consistency Audit
The manuscript was checked against the frozen Step 17 values. It contains:

- D1 C4: `+0.03673`, 95% CI `[+0.03141,+0.04215]`;
- D1 C5: `+0.18587`, 95% CI `[+0.16786,+0.20296]`;
- D2 C4: `+0.05992`, 95% CI `[+0.05308,+0.06667]`;
- D2 C5: `+0.00063`, 95% CI `[-0.01255,+0.01451]`.

The prose preserves three supported improvements, one inconclusive cell, the absence of a practically notable C3 tradeoff under the `-0.02` guardrail, and `RELIABILITY_METHOD_NOT_AUTHORIZED`. No B0 v1.1 inferential value was added.

## 31. Non-Claims Audit
The manuscript was rechecked against `reports/step17_nonclaims_v1.md`. It does not claim universal uncertainty failure, universal B1 superiority, montage causality, clinical safety, universal generalization, arbitrary-shift conformal guarantees, target-free universal recovery, a new calibration method, state-of-the-art performance, a new architecture, SHHS validation, or performance on unevaluated populations.

## 32. Section Evidence Map
Created `reports/step18_1_section_evidence_map.md`. It maps the manuscript sections to frozen repository artifacts, verified external citations, tables, figures, and rendered-paper QA artifacts. Results remain repository-evidence-only; literature is used only for context.

## 33. Supplementary Plan
`paper/supplement_outline.md` remains unchanged in scope and covers S1 dataset/channel details, S2 architecture/training, S3 per-seed results, S4 stage-level analysis, S5 confusion matrices, S6 interaction analysis, S7 montage sensitivity, S8 source mask-specific calibration, S9 oracle diagnostics, S10 B0 v1.2 correction, and S11 reproducibility/hashes.

## 34. Files Created

- `reports/step18_1_literature_evidence_matrix.csv`
- `reports/step18_1_citation_audit.csv`
- `reports/step18_1_manuscript_claim_audit.csv`
- `reports/step18_1_related_work_coverage.csv`
- `reports/step18_1_figure_render_audit.csv`
- `reports/step18_1_table_render_audit.csv`
- `reports/step18_1_latex_warning_audit.csv`
- `reports/step18_1_section_evidence_map.md`
- `reports/STEP_18_1_MANUSCRIPT_COMPLETION_REPORT.md`
- `paper/main.pdf`

Build logs and rendered inspection images were generated locally for QA and excluded from the final commit.

## 35. Files Modified

- `paper/main.tex`
- `paper/references.bib`

The historical Step 18 report and Step 17 evidence files were not overwritten.

## 36. Explicitly Not Done

- no training;
- no inference;
- no new calibration;
- no new statistics;
- no method implementation;
- no SHHS analysis;
- no frozen evidence modification;
- no frozen numerical-result modification;
- no Step 19;
- no final manuscript/reproducibility tag.

## 37. Remaining Manuscript Work
The manuscript remains a first complete draft. Future work includes reviewer-style scientific audit, author metadata, acknowledgments, venue-specific formatting, possible substantive expansion beyond approximately 4,504 main-text words, and revision of any claims identified during Step 19. These are future manuscript tasks and do not block the Step 18.1 completion gate.

## 38. Recommended Next Step
# Step 19 — Conduct an Internal Reviewer-Style Scientific Audit and Revise the Manuscript

Do NOT execute Step 19 in this Step 18.1 run.

## 39. Git Commit
Created local commit:

`paper: complete first ShiftSleep-UQ manuscript draft`

The commit includes the manuscript source, verified bibliography, compiled PDF, supplementary outline, literature matrix, citation/claim/coverage audits, figure/table/warning audits, section evidence map, and completion report. LaTeX temporary files and rendered inspection images were excluded.

## 40. GitHub Push Status
`PUSH_COMPLETE`.

The completed draft was pushed to `origin/main` with a normal non-force push. No scientific milestone tag was moved or created.

## 41. Git Status / Diff Summary
The final tracked package contains the Step 18.1 manuscript and audit artifacts only. Frozen Step 17 evidence remains unchanged. Final repository verification included the focused Step 17 test suite, which passed `5 passed`, `git diff --check`, final LaTeX/BibTeX compilation, citation/reference resolution, PDF rendering, figure/table inspection, numerical consistency checks, and repository status verification. The worktree was clean after commit and push, with local `HEAD` verified against `origin/main`.
