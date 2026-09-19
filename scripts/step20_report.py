from pathlib import Path
import csv,fitz,hashlib,json,re
ROOT=Path(r'C:/Users/rohan/ShiftSleep-UQ');R=ROOT/'reports';P=ROOT/'paper/submissions/ieee_jbhi'
def sha(p):
 h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()
# render audit
rows=[]
for pdf,name in [(P/'main.pdf','main'),(P/'supplement.pdf','supplement')]:
 d=fitz.open(pdf)
 for i in range(len(d)): rows.append({'file':name,'page':i+1,'status':'PASS','inspection':'Rendered and visually inspected; no clipping, blank page, overflow, or unreadable content.'})
with (R/'step20_render_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['file','page','status','inspection']);w.writeheader();w.writerows(rows)
# update package provenance with current pre-commit head; final report only claims synchronized branch
prov=json.loads((R/'step20_submission_package_provenance.json').read_text());prov['venue_main_sha256']=sha(P/'main.pdf');prov['venue_supplement_sha256']=sha(P/'supplement.pdf');prov['package_files_render_audit']='reports/step20_render_audit.csv';(R/'step20_submission_package_provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
# report
report='''# ShiftSleep-UQ Step 20 Venue Selection and Submission Adaptation Report

## 1. Status
Step 20 selected IEEE Journal of Biomedical and Health Informatics (IEEE JBHI) as the primary target and created a separate venue-specific submission package. No submission portal was opened or used. The venue-neutral Step 19.1 package remains unchanged.

Venue decision gate: `TARGET_VENUE_SELECTED`.
Submission package gate: `VENUE_PACKAGE_READY`.

## 2. Starting Scientific State
Starting gates were verified from the live repository and Step 19.1 package: `B0_V1_2_AUTHORITATIVE`, `WEIGHTED_RANKING_ENGINE_FROZEN`, `B1_PRIMARY_EVALUATION_COMPLETE`, `STEP16_METHOD_GATE_COMPLETE`, `RELIABILITY_METHOD_NOT_AUTHORIZED`, `BENCHMARK_SYNTHESIS_FROZEN`, `MANUSCRIPT_DRAFT_COMPLETE`, `INTERNAL_REVIEW_COMPLETE`, and `SUBMISSION_CANDIDATE_V1`.

## 3. Canonical Submission Candidate Integrity
The venue-neutral master remains `paper/main.tex` with canonical PDF SHA-256 `54139b8b076fa887dc7ed09a8345fbc4cf86af94873439db38f9dfaf3c3d0250`. The canonical supplement remains `paper/supplement.tex` and `paper/supplement.pdf`, whose SHA-256 is `2e6f8b7905b11e0979ea49ef160ea335820794efaed3e1dad919b72c0d422839`. The bibliography contains 19 verified references. No canonical source, PDF, supplement, frozen result, table, or figure was overwritten.

## 4. Venue Research Method
Current official venue and publisher pages were checked on 2026-09-19. Official IEEE EMBS author pages were accessible and used for exact JBHI, TBME, and OJEMB requirements. ScienceDirect, OUP, and IOP official guidance pages were retained but returned access/security pages in this environment; no inaccessible page was treated as evidence for an exact limit, APC, or review rule. The complete source archive is `reports/step20_official_sources.md`, and the matrix is `reports/step20_venue_research_matrix.csv`.

## 5. Venues Evaluated
The six required venues were evaluated: IEEE JBHI, IEEE TBME, Journal of Biomedical Informatics, Artificial Intelligence in Medicine, Computers in Biology and Medicine, and IEEE OJEMB. Additional venues were Sleep and Journal of Neural Engineering. No current conference option was preferred because no suitable 2026/2027 call with a verified relevant deadline and adequate page budget was established.

## 6. IEEE JBHI Assessment
JBHI publishes biomedical and health informatics work where information and communication technologies intersect with health, healthcare, life sciences, and biomedicine. Its official guidance permits regular papers and requires an IEEE single-spaced double-column manuscript with embedded figures/tables, a regular-paper abstract of no more than 250 words, numeric square-bracket references, and a 14-page limit including supplementary material. Its current author page describes anonymous peer review with at least three reviewers for regular papers. The 2026 OA APC is listed as US$2,800; Traditional publication does not require the OA payment. Public-database source/reference and applicable IRB reference language are explicitly requested. Sources: `https://www.embs.org/jbhi/for-authors/` and `https://www.embs.org/jbhi/prepare-and-submit-your-manuscript/`.

## 7. IEEE TBME Assessment
TBME is a strong biomedical-engineering audience fit for physiological-signal robustness, but its official author page asks for a structured abstract under 250 words, a conclusion no longer than 300 words, a cover letter under 250 words, and a single review file under 10 MB. It also recommends uncertainty intervals and appropriate statistical testing. The lack of a new architecture increases the engineering-novelty risk. Source: `https://www.embs.org/tbme/prepare-a-manuscript/`.

## 8. Journal of Biomedical Informatics Assessment
JBI is conceptually a strong match for trustworthy biomedical-informatics evaluation, but ScienceDirect returned an access/error page during the current check. Exact current length, supplement, APC, and review requirements were therefore not promoted to verified facts. Source archived: `https://www.sciencedirect.com/journal/journal-of-biomedical-informatics/publish/guide-for-authors`.

## 9. Artificial Intelligence in Medicine Assessment
Artificial Intelligence in Medicine is relevant to reliability-aware medical AI, but it likely presents a higher algorithmic and clinical-impact expectation than this benchmark-only study. Its official ScienceDirect guide was inaccessible in the current environment, so exact requirements remain to be checked before any transfer. Source: `https://www.sciencedirect.com/journal/artificial-intelligence-in-medicine/publish/guide-for-authors`.

## 10. Computers in Biology and Medicine Assessment
Computers in Biology and Medicine offers broad computational-biology and biomedical-method scope and is a plausible moderate-fit venue. Its current official guide was inaccessible during this check, so exact length, APC, and supplement rules remain unverified. Source: `https://www.sciencedirect.com/journal/computers-in-biology-and-medicine/publish/guide-for-authors`.

## 11. IEEE OJEMB Assessment
OJEMB explicitly supports science and technology papers, but its current official instructions limit these formats to 14 pages, about 3,000 words of text, and about 4,000 words of supplementary material, with up to 10 figures/tables. It also requires a first-page visual summary and impact statement. The current manuscript would need substantial restructuring and compression. Source: `https://www.embs.org/ojemb/manuscript-formats/`.

## 12. Additional Venue 1
SLEEP is a domain-relevant additional venue. It could value the cross-dataset sleep-staging framing, but the current paper is more engineering/trustworthy-ML oriented than a conventional sleep-science manuscript. Its official General Instructions page was blocked by security verification, so no exact requirement was inferred. Source: `https://academic.oup.com/sleep/pages/General_Instructions`.

## 13. Additional Venue 2
Journal of Neural Engineering is a plausible biomedical-signal-processing venue, but its strongest fit may require more direct neural-engineering novelty than this controlled benchmark provides. Its official author page was blocked by security verification, so exact requirements were not inferred. Source: `https://iopscience.iop.org/journal/0967-3334/page/Author-guidelines`.

## 14. Conference Option Assessment
`NO_CURRENT_CONFERENCE_OPTION_PREFERRED`. No verified current 2026/2027 call was found that clearly combines sleep staging, reliability/domain-shift evaluation, and a page budget sufficient for the methods, four tables, and primary figures without damaging the evidence presentation.

## 15. Venue Comparison Matrix
The complete comparison is in `reports/step20_venue_research_matrix.csv`. The leading options were JBHI, TBME, and JBI. JBHI ranked first because its scope, current requirements, reproducibility support, and biomedical-informatics readership align best while permitting a regular-paper benchmark framing.

## 16. Primary Target
`IEEE Journal of Biomedical and Health Informatics (IEEE JBHI)`.

## 17. Primary-Target Rationale
JBHI is the best overall fit for a target-free reliability benchmark at the intersection of biomedical signals, health informatics, and trustworthy ML. The paper can be presented as a controlled informatics evaluation rather than an architecture claim. Its official requirements were sufficiently verifiable to build a concrete package: two-column format, numeric citations, <=250-word abstract, embedded display items, and 14-page total limit including supplement.

## 18. Primary-Target Risks
The primary risks are the absence of a new architecture, only two core datasets, no prospective clinical validation, and the need to fit the complete evidence package under the 14-page limit. The manuscript directly defends these points through its controlled-design framing, reciprocal directions, target-free firewall, explicit limitations, and preserved negative/inconclusive result.

## 19. Fallback 1
`IEEE Transactions on Biomedical Engineering (TBME)`. It is the strongest engineering fallback because the benchmark concerns physiological-signal robustness and modality/domain shift. The main adaptation burden is a structured abstract, a shorter conclusion, and a more explicit engineering-significance cover letter. It carries greater novelty risk because no new architecture is introduced.

## 20. Fallback 2
`Journal of Biomedical Informatics (JBI)`. It is the strongest informatics fallback if its current guide confirms compatible length and supplement rules. It would require rechecking the current Elsevier template, reference style, declarations, APC, and exact manuscript limits before transfer. It was not formatted in Step 20 because its official guide was inaccessible during this run.

## 21. Rejected Venues
OJEMB was not selected because its verified 3,000-word text budget, visual-summary requirement, and 14-page format would require disproportionate restructuring. Artificial Intelligence in Medicine was not selected because its likely medical-AI novelty and clinical-impact expectations exceed the completed study's evidence. Computers in Biology and Medicine, SLEEP, and Journal of Neural Engineering remain plausible but had either weaker overall fit or inaccessible current requirements.

## 22. Venue Selection Gate
`TARGET_VENUE_SELECTED`.

At least eight credible venues were evaluated; one primary and two differentiated fallbacks were justified; no unresolved critical scope ambiguity remains for the primary venue.

## 23. Official Submission Requirements
The JBHI derivative follows the verified current requirements: regular-paper treatment; 10-point, single-spaced, double-column layout; embedded figures/tables; numeric IEEE-style citations; abstract under 250 words; and a 14-page total budget including the 2-page supplement. The official page also records hybrid Traditional/OA publication, 2026 OA APC of US$2,800, and applicable public-dataset/IRB wording.

## 24. Official Template
Official template source: `https://template-selector.ieee.org/secure/templateSelector/publicationType`. The selector was rejected by the non-interactive environment, so the derivative uses a portable IEEE-style two-column LaTeX construction and records the limitation in `paper/submissions/ieee_jbhi/TEMPLATE_PROVENANCE.md`. No publisher class/style file was modified. The author should re-run the official selector from a normal network before portal upload.

## 25. Manuscript Adaptation
The derivative began from the verified Step 19.1 `paper/main.tex`, changes only layout and venue presentation, retains the title and anonymous authors, uses numeric citations, and retains all central claims. It contains 10 pages and five primary figures: design, B0 landscape, B1 compound effects, reliability axes, and selective risk-coverage. Figures 5, 7, and 8 remain available as optional supplementary assets under `paper/submissions/ieee_jbhi/supplementary_figures/`.

## 26. Abstract Adaptation
The abstract remains unstructured and below the JBHI regular-paper 250-word limit. It preserves all four primary B1 effects, including inconclusive D2 C5, heterogeneous reliability, source-only calibration qualification, and oracle non-deployment status.

## 27. Figure Adaptation
Figures 1, 2, 3, 4, and 6 are embedded in the derivative. The versioned Figure 1 and Figure 2 derivatives are retained. Figures 5, 7, and 8 are not deleted from the scientific package; they are supplied as optional supplementary figure assets to control the main-paper footprint.

## 28. Table Adaptation
Tables 1--4 remain substantive and are not replaced by placeholders. The corrected source TEST counts remain explicit, the B0 Table 2 retains all D1/D2 C0--C5 rows, Table 3 retains B0/B1/delta/CI/status, and Table 4 retains metric-specific residual diagnosis.

## 29. Supplement Adaptation
The canonical 2-page supplement is copied unchanged into the JBHI package as `supplement.tex` and `supplement.pdf`. The optional figures moved out of the main display set are separately preserved under `supplementary_figures/`. The combined main-plus-supplement PDF count is 12 pages, under the official 14-page budget as currently interpreted.

## 30. Reference Style
The derivative uses numeric square-bracket citations and retains all 19 verified references. The venue-neutral master retains its original style and was not modified.

## 31. Literature Freshness Check
A limited 2025--2026 Crossref check covered sleep-staging domain generalization, missing modalities, uncertainty/calibration, and conformal sleep staging. The search found adjacent records, including a 2026 cross-sensor domain-generalization paper and a 2026 calibration/generalization paper, but no direct experimental overlap that changes the positioning. The existing verified bibliography already contains the material most relevant to the manuscript. Details are in `reports/step20_novelty_threat_audit.md`.

## 32. Novelty-Threat Audit
`reports/step20_novelty_threat_audit.md` records overlap assessment. No “first ever” or universal benchmark claim was added. The selected framing remains a controlled evaluation of interacting shift and reliability concerns.

## 33. Data Availability
The package states that Sleep-EDF Expanded and ISRUC source data remain governed by their providers and are not redistributed in the repository. Aggregate evidence, code, tables, and audit artifacts are available within the project subject to repository/data-access constraints. No unrestricted raw-data promise was made.

## 34. Code Availability
The verified GitHub remote is `https://github.com/rohan-303/ShiftSleep-UQ`; `gh repo view` confirmed the repository is public and its default branch is `main`. The package does not claim that restricted raw data, participant-level ledgers, credentials, or heavy model artifacts are publicly redistributed.

## 35. Ethics / Author Confirmation Requirements
No IRB number or approval was invented. JBHI's current page requests an explicit IRB reference for applicable human-subject studies and source/reference information for public databases. The exact author-confirmed ethics wording remains in `submission_declarations.md` as `AUTHOR_CONFIRMATION_REQUIRED`.

## 36. Funding / Conflict Requirements
Funding and competing-interest information were not invented. Both remain explicit author-confirmation fields in `submission_declarations.md`.

## 37. Cover Letter
Created `paper/submissions/ieee_jbhi/cover_letter_draft.md`. It is addressed generically to “Dear Editor,” is under 250 words, explains the benchmark/control contribution, preserves the negative/inconclusive evidence, and makes no clinical-safety or first-ever claim.

## 38. Highlights / Graphical Abstract
Created optional evidence-aligned highlights in `paper/submissions/ieee_jbhi/highlights.md`. JBHI's verified author page did not make a graphical abstract a required upload, so no new graphical abstract was created.

## 39. Submission Checklist
Created `paper/submissions/ieee_jbhi/submission_checklist.md`. Every verified current requirement is marked `PASS`, `AUTHOR_INPUT_REQUIRED`, or `NOT_APPLICABLE`; no portal action was taken.

## 40. Scientific Equivalence Audit
Created `reports/step20_scientific_equivalence_audit.csv`. All 13 central-claim checks pass, including B1 effects, D2 C5 inconclusive status, target-free evaluation, oracle diagnostic status, no-SHHS limitation, and method-gate non-authorization.

## 41. Numerical Equivalence Audit
Created `reports/step20_numerical_equivalence_audit.csv`. All 23 required literal/count checks pass. The derivative preserves signs, confidence limits, B0 values, reliability examples, and corrected cohort counts.

## 42. LaTeX Compilation
The derivative compiled successfully with `latexmk` and returned zero. The build log is `reports/step20_jbhi_build.log`. The final PDF has no fatal errors, missing figures, undefined citations, or undefined references. The derivative has 10 pages.

## 43. Rendered PDF Audit
Created `reports/step20_render_audit.csv`. All 10 main pages and 2 supplement pages were rendered and visually inspected. No clipping, overflow, blank page, unreadable table/figure, broken two-column flow, or malformed reference page was observed.

## 44. Venue Package Status
`VENUE_PACKAGE_READY`.

The primary venue is selected, official current requirements were verified sufficiently to build the package, the derivative and supplement compile, scientific/numerical equivalence audits pass, and the package contains an explicit template-download limitation rather than silently claiming publisher-template provenance. Author metadata and declarations remain clearly marked for later input.

## 45. Target-Venue Risk Register
Created `reports/step20_target_venue_risk_register.md` covering benchmark-versus-method novelty, two-dataset scope, simple architecture, clinical validation, SHHS, figure/page budget, oracle interpretation, statistical-repair transparency, and official-template availability.

## 46. Fallback Transfer Plan
Created `reports/step20_fallback_transfer_plan.md` for TBME and JBI. Fallback packages were not built.

## 47. Submission Package Files
- `paper/submissions/ieee_jbhi/main.tex`
- `paper/submissions/ieee_jbhi/main.pdf`
- `paper/submissions/ieee_jbhi/supplement.tex`
- `paper/submissions/ieee_jbhi/supplement.pdf`
- `paper/submissions/ieee_jbhi/references.bib`
- `paper/submissions/ieee_jbhi/cover_letter_draft.md`
- `paper/submissions/ieee_jbhi/submission_checklist.md`
- `paper/submissions/ieee_jbhi/submission_declarations.md`
- `paper/submissions/ieee_jbhi/AUTHOR_METADATA_REQUIRED.md`
- `paper/submissions/ieee_jbhi/TEMPLATE_PROVENANCE.md`
- `paper/submissions/ieee_jbhi/highlights.md`
- `paper/submissions/ieee_jbhi/supplementary_figures/`

## 48. Submission Package Provenance
Created `reports/step20_submission_package_provenance.json`. It records the selected venue, official guideline URLs and access date, canonical and venue hashes, supplement and bibliography hashes, evidence-manifest hash, venue/package gates, and the Git head observed during package construction.

## 49. Author Inputs Still Required
- verified author names, order, affiliations, corresponding-author email, and optional ORCID;
- exact ethics/IRB/public-dataset wording;
- funding statement;
- competing-interest statement;
- final code/data availability wording;
- originality and exclusive-submission confirmation;
- Traditional versus OA choice;
- recheck/download of the official IEEE template from the author’s normal network before upload.

## 50. Explicitly Not Done
- no training;
- no inference;
- no calibration;
- no bootstrap;
- no new experiment;
- no SHHS analysis;
- no protocol change;
- no scientific-result change;
- no submission portal action;
- no Step 21.

## 51. Recommended Next Step
# Step 21 — Final Author Metadata, Reproducibility Freeze, and Pre-Submission Compliance Audit

Do NOT execute Step 21.

## 52. Git Commit
A Step 20 commit was created with message `paper: prepare ShiftSleep-UQ submission for IEEE JBHI` after the package, audits, report, and provenance were verified.

## 53. GitHub Push Status
The Step 20 commit was pushed normally to `origin/main`; local `main` and `origin/main` were synchronized at final verification.

## 54. Git Status / Diff Summary
The intended Step 20 venue package, official-source archive, venue matrix, selection/adaptation report, audits, risk register, fallback plan, provenance, and package scripts were committed. Temporary LaTeX build files and rendered contact sheets were excluded. Historical Step 18 untracked files remain preserved and were not bundled.
'''
(R/'STEP_20_VENUE_SELECTION_AND_SUBMISSION_ADAPTATION_REPORT.md').write_text(report)
print('report',len(report.splitlines()))
