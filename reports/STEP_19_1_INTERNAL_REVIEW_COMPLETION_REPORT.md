# ShiftSleep-UQ Step 19.1 Internal Review Completion Report

## 1. Status
Step 19.1 corrected the source TEST cohort counts, reverified all required frozen manuscript numbers, completed the canonical PDF handoff, recompiled the supplement, reran claim/citation/numerical/render audits, and froze the internal-review submission candidate.

## 2. Internal Review Gate
`INTERNAL_REVIEW_COMPLETE`.

## 3. Starting Step 19 State
Starting gate: `INTERNAL_REVIEW_PARTIAL`. The prior Step 19 candidate and canonical PDF were verified before correction. The old canonical SHA-256 was `85aaca5faf0d5155a18f32ddfac54ce64053325355e4a43bd37ae63f756c73d5`.

## 4. Frozen Evidence Integrity
The required gates remain `B0_V1_2_AUTHORITATIVE`, `WEIGHTED_RANKING_ENGINE_FROZEN`, `B1_PRIMARY_EVALUATION_COMPLETE`, `STEP16_METHOD_GATE_COMPLETE`, `RELIABILITY_METHOD_NOT_AUTHORIZED`, and `BENCHMARK_SYNTHESIS_FROZEN`. No model, prediction, calibration, bootstrap, protocol, condition, B0/B1 result, Step 17 table, or Step 17 figure was modified.

## 5. Cohort-Count Defect
Step 19 had incorrectly displayed source TEST counts as zero in both Table 1 and supplement Table S1. The authoritative partition artifact shows D1 Sleep-EDF source counts `47/12/8/11` for TRAIN/DEV/CAL/TEST and D2 ISRUC source counts `59/15/10/15`. Held-out target cohort totals are ISRUC `99` for D1 and Sleep-EDF `78` for D2.

## 6. Authoritative Partition Audit
Created `reports/step19_1_cohort_count_audit.csv`. It contains 10 rows covering D1/D2 TRAIN, DEV, CAL, TEST, and target roles. All rows are `PASS`. Authoritative source-role counts were reconstructed from `reports/subject_partitions_v2.csv`; target totals come from the frozen cohort accounting.

## 7. Corrected Main Table 1
Table 1 now has separate columns for Direction, Source, Target, TRAIN, DEV, CAL, TEST, and Target cohort. It displays D1 `47 / 12 / 8 / 11 / 99` and D2 `59 / 15 / 10 / 15 / 78`.

## 8. Corrected Supplement Table S1
The supplement now has separate TEST and Target cohort columns and displays the same authoritative counts. The previous ambiguous `TEST / target cohort` combined cell and both stale `0 / 99` and `0 / 78` values were removed.

## 9. Partition Reference Audit
Created `reports/step19_1_partition_reference_audit.csv`. The manuscript and supplement role references were searched for stale combined counts and source-role terminology. No `0 / 99`, `0 / 78`, or `TEST / target cohort` stale reference remains. All reviewed role-reference rows are `PASS`.

## 10. Table 2 Reverification
Created `reports/step19_1_table2_reverification.csv`. All 48 checks pass: D1/D2 C0--C5, each for macro-F1, NLL, AURC, and alpha-.10 absolute coverage gap. Values remain unchanged from the Step 19 canonical B0 v1.2 derivative.

## 11. Table 3 Provenance Audit
Created `reports/step19_1_table3_provenance_audit.csv`. All four compound cells pass exact provenance checks against `reports/b1_vs_b0_paired_results_v1.csv`. B0, B1, delta, and CI endpoints use the frozen paired artifact, displayed to five decimal places with signed CI endpoints. No close-but-different value was accepted.

## 12. Reliability Number Reverification
Created `reports/step19_1_numerical_audit.csv` with 68 PASS rows, including the complete displayed Table 1/Table 2/Table 3 values, abstract effects, and reliability examples. The D1 C4 values are NLL `-0.02724`, AURC `-0.02970`, and conformal absolute-gap delta `+0.00235`. The D2 C5 values are NLL `+0.16300`, AURC `-0.05022`, and conformal absolute-gap delta `+0.00673`.

## 13. Figure 1 Verification
`paper/figures/fig1_shift_design_v2.pdf` remains the manuscript-specific derivative. Its source-role box explicitly includes `TRAIN / DEV / CAL / TEST`; it does not alter the frozen Step 17 Figure 1.

## 14. Figure 2 Verification
`paper/main.tex` continues to use `figures/fig2_b0_shift_landscape_v2.pdf`. The frozen Step 17 Figure 2 remains preserved. Created `reports/step19_1_fig2_source_audit.csv` with 48 PASS rows using canonical B0 v1.2 values and zero deltas. The original Step 19 defect audit remains preserved separately.

## 15. Full Figure Audit Status
The existing Step 19 full figure source audit remains preserved. Figures 3--8 continue to use frozen source data. Figure 6 remains a seed-17 representative qualitative visualization, while inferential AURC uses all three frozen seeds. Created `reports/step19_1_figure_derivative_audit.csv`; both manuscript-specific derivative checks pass.

## 16. Supplement Revision
`paper/supplement.tex` was corrected, recompiled, and rendered. It retains concise S1--S11 coverage: dataset/channel contract, architecture/training, canonical B0 table, full-result artifact locations, stage analysis, confusion changes, interactions, montage sensitivity, source-mask calibration, oracle diagnostics, B0 repair, and reproducibility hashes. No new analysis was added.

## 17. Main Compilation
The revised candidate was compiled in `paper/build_step19_1/` using TinyTeX. `latexmk`, BibTeX, and the final two `pdflatex` passes returned zero. Final logs contain no undefined citations, undefined references, overfull boxes, or fatal errors.

## 18. Supplement Compilation
The corrected supplement was compiled in `paper/supp_step19_1/`. `latexmk` returned zero. Final supplement logs contain no undefined references, overfull boxes, or fatal errors.

## 19. Candidate PDF Hash
Verified candidate: `paper/main_step19_1_candidate.pdf`.

SHA-256: `54139b8b076fa887dc7ed09a8345fbc4cf86af94873439db38f9dfaf3c3d0250`.

## 20. Canonical PDF Replacement
The previous file lock cleared without terminating any user process. The verified candidate was copied to `paper/main.pdf`.

## 21. Canonical PDF Hash
`paper/main.pdf` SHA-256: `54139b8b076fa887dc7ed09a8345fbc4cf86af94873439db38f9dfaf3c3d0250`.

## 22. Canonical/Candidate Equality
`PASS`: canonical and candidate hashes are identical.

## 23. Main PDF Page Count
The canonical revised `paper/main.pdf` contains 18 pages.

## 24. Supplement PDF Page Count
The canonical revised `paper/supplement.pdf` contains 2 pages.

## 25. Numerical Audit
`reports/step19_1_numerical_audit.csv` contains 68 rows, all `PASS`. Table 2 has 48 PASS metric checks; Table 3 has four PASS provenance rows in `reports/step19_1_table3_provenance_audit.csv`.

## 26. Claim Audit
Created `reports/step19_1_claim_audit.csv`. All nine previously audited claims are rechecked and marked `PASS`. The cohort correction did not alter any scientific claim or conclusion.

## 27. Citation Audit
Created `reports/step19_1_citation_audit.csv`. All 19 bibliography entries are used, resolve, and are marked `PASS`. Verified reference count remains 19.

## 28. Rendered QA
Created `reports/step19_1_render_audit.csv`. The 18-page canonical main candidate and 2-page supplement were rendered page by page. Table 1, Table 2, Table 3, Table 4, Figures 1--8, references, and supplement pages were inspected. No clipping, blank page, overflow, unreadable table/figure, or broken page break was observed.

## 29. Submission Candidate Status
`SUBMISSION_CANDIDATE_V1`.

## 30. Manuscript Provenance
Updated `reports/step19_manuscript_provenance_v1.json` with Step 19.1 status, main and supplement hashes, source hashes, frozen manifest hash, cohort-audit hash, Table 3 provenance hash, and all required scientific gates. `canonical_candidate_equal` is `true`.

## 31. Files Created
- `reports/STEP_19_1_INTERNAL_REVIEW_COMPLETION_REPORT.md`
- `reports/step19_1_cohort_count_audit.csv`
- `reports/step19_1_partition_reference_audit.csv`
- `reports/step19_1_table2_reverification.csv`
- `reports/step19_1_table3_provenance_audit.csv`
- `reports/step19_1_numerical_audit.csv`
- `reports/step19_1_fig2_source_audit.csv`
- `reports/step19_1_figure_derivative_audit.csv`
- `reports/step19_1_claim_audit.csv`
- `reports/step19_1_citation_audit.csv`
- `reports/step19_1_render_audit.csv`
- `paper/main.pdf`
- `paper/supplement.pdf`
- `scripts/step19_1_audit.py`
- `scripts/step19_1_numerical_full.py`
- `scripts/step19_1_finalize.py`

## 32. Files Modified
- `paper/main.tex`
- `paper/supplement.tex`
- `reports/step19_manuscript_provenance_v1.json`

Existing Step 19 manuscript derivatives and reviewer reports were preserved. Frozen Step 17 source figures and tables were not modified.

## 33. Explicitly Not Done
- no training;
- no inference;
- no calibration fit;
- no new statistics;
- no new model;
- no SHHS analysis;
- no protocol change;
- no scientific-result modification;
- no Step 20.

## 34. Remaining Blockers
`NONE`.

## 35. Recommended Next Step
# Step 20 — Select the Target Venue and Adapt the Frozen Submission Candidate to Its Requirements

Do NOT execute Step 20.

## 36. Git Commit
Created commit `30114c23a4752909d8312fffc233fd55c524cf31` with message `paper: revise ShiftSleep-UQ after internal scientific review`. The commit includes the corrected canonical manuscript, supplement, versioned derivatives, reviewer reports, audits, and provenance.

## 37. GitHub Push Status
`PUSH_COMPLETE`: local `main` and `origin/main` both resolve to `30114c23a4752909d8312fffc233fd55c524cf31`.

## 38. Git Status / Diff Summary
The Step 19/19.1 manuscript, supplement, versioned derivatives, reviewer reports, audits, and provenance files were committed and pushed. Temporary LaTeX build directories and rendered contact sheets were excluded. Historical Step 18 untracked files remain preserved and were not bundled.
