# ShiftSleep-UQ Step 3 Novelty Gate Report

## 1. Status

PARTIAL

Critical method-level collision uncertainty remains for RMSSC and Direct Quantification because accessible IEEE pages were blocked. The project thesis was nevertheless narrowed and frozen with explicit qualifications.

## 2. Research Decision

MODIFY

The project remains worthwhile as an interaction-focused reliability benchmark, but it must not claim priority or claim that the critical collision papers do not evaluate the proposed setting. Proceed only to source-verified dataset acquisition and schema auditing.

## 3. Repository State

* path: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* Step 1 commit: `b6dbbe4319538b799eb2537d0321892ff395df93`
* Step 2 audit commit: `0f76fa63b8fe56090505f75ea908d6da06287dd0`
* Step 2 report commit: `07566b2598ea401d63dee2e22db7b002b7d6dda2`
* Step 3 commit: final hash recorded below after the report-recording amend; push status remains NOT PUSHED
* push status: NOT PUSHED

Repository preflight confirmed the expected project identity, clean starting tree, branch `main`, Step 2 report presence, and passing tests. No unrelated repository was modified.

## 4. Critical Collision Results

### RMSSC

* **verified bibliographic identity:** Crossref verifies the title `RMSSC: A Robust Multimodal Framework for Sleep Stage Classification with Noisy Labels and Missing Modalities`, authors Jiajie Luo, Liangjun Miao, Qiwen Guan, Jiguang Li, Zhao Huang, and Jichun Li, ICASSP 2026, DOI `10.1109/ICASSP55912.2026.11461625`, published date 2026-05-03. Pages and full-text methods were NOT_VERIFIED.
* **verified experimental scope:** The title verifies missing-modality and multimodal scope only. Datasets, ISRUC subsets, exact modalities, masks, natural versus synthetic missingness, training/validation/test protocol, subject split, subject-invariant definition, domain-generalization protocol, simultaneous compound shift, and reliability metrics are NOT_VERIFIED.
* **collision:** NOT_VERIFIED
* **evidence:** Crossref metadata endpoint was accessible; IEEE Xplore and stamp/PDF routes were inaccessible in this environment. The project therefore treats RMSSC as a critical unresolved collision, not as evidence of absence.

### Direct Quantification

* **verified bibliographic identity:** Crossref verifies Miika Vainikka, Riku Huttunen, Samu Kainulainen, Henri Korkalainen, and Matias Rusanen, `Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging`, IEEE Transactions on Biomedical Engineering, 2026, DOI `10.1109/TBME.2025.3623380`; Crossref publication date June 2026.
* **verified experimental scope:** The title and bibliographic record establish direct sleep-staging UQ as the topic. Architecture, datasets, subject/recording counts, MC dropout, Hypnodensity Interval, operational epistemic/aleatoric definitions, calibration metrics, rejection experiment, risk-coverage/AURC, missing channels, compound shift, and conformal prediction are NOT_VERIFIED.
* **collision:** NOT_VERIFIED
* **evidence:** IEEE page access was blocked by a JavaScript/robot verification page; no unsupported absence claim is made.

### SF-UIDA

* **verified bibliographic identity:** Yangxuan Zhou, Sha Zhao, Jiquan Wang, Haiteng Jiang, Shijian Li, Benyan Luo, Tao Li, and Gang Pan, `Personalized Sleep Staging Leveraging Source-free Unsupervised Domain Adaptation`, AAAI 2025, 39(13), 14529–14537, DOI `10.1609/aaai.v39i13.33592`, published 2025-04-11.
* **verified experimental scope:** The official AAAI abstract states a two-step source-free unsupervised individual domain-adaptation scheme using sequential cross-view contrasting and pseudo-label fine-tuning; it adapts to newly appeared unlabeled individuals without source data, and is evaluated on three public sleep datasets and three classic models.
* **collision:** PARTIAL
* **evidence:** It uses unlabeled target individuals at adaptation time, so it is not target-free domain generalization. Missing modalities, calibration/UQ, formal selective prediction, and conformal prediction were not described in the official abstract.

## 5. Other Major Competitor Boundaries

* **SleepDG:** Cross-dataset/generalizable sleep staging and multi-level domain alignment. Overlap is unseen-domain evaluation; missing-modality reliability and formal calibration/selective/conformal analysis were not verified.
* **CIMSleepNet:** Incomplete multimodal physiological signals and contrastive imagination. Overlap is missing modalities; compound reliability and formal calibration/selective/conformal analysis were not verified.
* **SleepTransformer:** Sleep staging with interpretability and entropy-based uncertainty/deferral motivation across two databases. Overlap is UQ; target-free compound reliability was not verified.
* **U-PASS:** Uncertainty-guided pipeline spanning acquisition, training, and deployment. Overlap is operational UQ; strict source-only shift calibration and formal selective/conformal analysis were not verified.
* **DREAM:** Domain-invariant representation learning, sleep dynamics, and generalization/uncertainty analysis. Overlap is domain/subject invariance; leave-one-dataset-out reliability under missing modalities was not verified.

Full boundaries, including prohibited claims, are in `docs/competitor_boundary.md`.

## 6. New Literature Found

* Zhou et al., `Personalized Sleep Staging Leveraging Source-free Unsupervised Domain Adaptation`, AAAI 2025, DOI `10.1609/aaai.v39i13.33592`. This materially changes the terminology boundary: source-free adaptation is not target-free domain generalization.
* `Conformal Prediction for Compositional Data` was identified in an arXiv search as an adjacent conformal work whose abstract mentions a sleep-stage dataset. It was not verified as a conventional multiclass sleep-staging compound-shift benchmark and is not treated as such.

## 7. Calibration Literature Finding

Direct sleep-staging UQ work was verified, but only limited direct probability-calibration evidence was verified. The audited accessible records did not establish a strict source-only calibration protocol evaluated on an unseen dataset crossed with modality loss. RMSSC and Direct Quantification remain unresolved, so this is a qualified finding rather than an exhaustive absence claim.

## 8. Selective Prediction Literature Finding

SleepTransformer and U-PASS establish uncertainty/deferral as relevant sleep-staging concepts. The audit did not verify formal compound-shift risk-coverage or AURC in the accessible records. Removing uncertain predictions is not by itself formal selective prediction; formal evidence requires risk-versus-coverage, AURC or equivalent fixed-risk/fixed-coverage analysis. Direct Quantification's rejection details remain NOT_VERIFIED.

## 9. Conformal Literature Finding

* **direct sleep-staging work found?** An adjacent compositional-data paper mentioning a sleep-stage dataset was found; no verified standard multiclass sleep-staging conformal benchmark under simultaneous dataset/domain and missing-modality shift was identified.
* **adjacent work:** conformal prediction for compositional data; general conformal prediction methodology; source-calibrated prediction-set evaluation under explicit exchangeability assumptions.
* **remaining apparent gap:** empirical coverage and set-size degradation when source-calibrated multiclass prediction sets are transferred across unseen PSG datasets and modality-loss conditions.
* **confidence:** MEDIUM, because this was a bounded search and critical papers were not fully accessible.

## 10. Updated Novelty Matrix N6-N18

| ID | Classification | Confidence | Strongest evidence |
|---|---|---|---|
| N6 | PARTIALLY_ESTABLISHED | MEDIUM | SleepTransformer/U-PASS/Direct Quantification establish UQ; formal post-hoc calibration under shift not verified. |
| N7 | UNCERTAIN | MEDIUM | UQ and cross-dataset clusters were separate in accessible evidence; Direct Quantification unresolved. |
| N8 | UNCERTAIN | MEDIUM | Deferral motivation exists; formal cross-dataset risk-coverage not verified. |
| N9 | APPARENT_GAP | MEDIUM | CIMSleepNet establishes missing-modality robustness; risk-coverage under missingness not verified. |
| N10 | UNCERTAIN | LOW | No verified compound risk-coverage result; RMSSC/Direct Quantification method scope unresolved. |
| N11 | APPARENT_GAP | MEDIUM | SF-UIDA uses unlabeled target adaptation rather than source-only target-free calibration; strict calibration evidence not verified. |
| N12 | UNCERTAIN | LOW | No verified compound calibration degradation study; critical collision papers unresolved. |
| N13 | APPARENT_GAP | MEDIUM | No verified direct standard sleep-staging conformal benchmark under dataset shift. |
| N14 | APPARENT_GAP | MEDIUM | No verified direct conformal analysis under missing-modality shift. |
| N15 | UNCERTAIN | LOW | No verified compound conformal study; bounded search and unresolved papers prevent high confidence. |
| N16 | UNCERTAIN | MEDIUM | No verified target-free modality-conditioned calibrator collision; requires re-audit before method work. |
| N17 | PARTIALLY_ESTABLISHED | HIGH | SF-UIDA establishes source-free unsupervised target adaptation, which is distinct from target-free DG; target-free shift-aware calibration remains unresolved. |
| N18 | UNCERTAIN | LOW | No verified unified benchmark, but RMSSC/Direct Quantification are not fully inspected. |

The remaining LOW-confidence critical entries N10, N12, N15, and N18 require the status PARTIAL rather than false certainty.

## 11. Claim-to-Evidence Results

* C1 SUPPORTED, HIGH: cross-dataset generalization is established.
* C2 SUPPORTED_WITH_QUALIFICATION, HIGH: missing-modality staging is established; RMSSC full scope remains unresolved.
* C3 SUPPORTED, HIGH: sleep-staging UQ is established.
* C4 SUPPORTED_WITH_QUALIFICATION, MEDIUM: formal cross-dataset calibration remains insufficiently characterized in accessible evidence.
* C5 UNRESOLVED, MEDIUM: correctness ranking under compound shift remains incompletely audited.
* C6 UNRESOLVED, MEDIUM: formal selective risk-coverage under compound shift remains incompletely audited.
* C7 SUPPORTED_WITH_QUALIFICATION, MEDIUM: no verified standard compound-shift conformal benchmark was found; adjacent sleep-stage conformal work exists.
* C8 SUPPORTED, HIGH: synthetic masking and structural mismatch must be separated.
* C9 SUPPORTED_WITH_QUALIFICATION, MEDIUM: unified domain × modality reliability benchmark remains defensible but not priority-claim ready.
* C10 UNRESOLVED, LOW: modality-conditioned calibration remains conditional and unauthorized.

The full ledger is `docs/claim_evidence_ledger.md`.

## 12. Defensible Novelty Boundary

ShiftSleep-UQ is not a new sleep-staging architecture and does not own cross-dataset generalization, missing-modality robustness, or uncertainty as standalone areas. Its defensible boundary is a pre-experimental, leakage-safe reliability benchmark that crosses held-out dataset/domain with modality availability, distinguishes synthetic masking from structural mismatch, and jointly reports calibration, correctness ranking, formal selective risk-coverage, and empirical conformal coverage. This boundary remains qualified until RMSSC and Direct Quantification are inspected at method depth.

## 13. Frozen Paper Thesis

Existing work separately addresses cross-dataset sleep staging, incomplete multimodal signals, and sleep-staging uncertainty, but the accessible evidence does not verify a unified target-free analysis of probability calibration, correctness detection, formal selective risk-coverage, and empirical conformal coverage under the interaction of unseen PSG dataset/domain and modality loss. ShiftSleep-UQ will test this qualified thesis without priority claims, while treating channel/label incompatibility and target-data access as explicit threats to validity.

## 14. Frozen Contributions

1. A subject- and dataset-leakage-safe benchmark crossing held-out PSG dataset/domain and modality availability.
2. A systematic subject-level analysis of calibration, uncertainty-based error detection, selective risk-coverage, and empirical conformal coverage as shift changes.
3. A conditional lightweight modality-aware/shift-aware calibration method only after a reproducible baseline failure is demonstrated.

## 15. Frozen Research Questions

1. How do predictive performance and probability calibration change across known-domain/full-modality, missing-modality, unseen-domain/full-modality, and compound-shift conditions?
2. How effectively do uncertainty scores identify incorrect predictions and support formal selective prediction as shift severity changes, and can ranking quality dissociate from probability calibration?
3. How does empirical conformal coverage and prediction-set size change when source-calibrated sets are transferred to unseen domains and modality-loss conditions?
4. Are reliability failures attributable primarily to domain shift, modality loss, or their interaction after accounting for subject clustering, dataset heterogeneity, and channel/label confounds?

## 16. Frozen Hypotheses

* F1: The domain × modality interaction for reliability is non-zero and may be super-additive; direction is not assumed.
* F2: Uncertainty-score ranking and probability calibration can degrade at different rates.
* F3: High-confidence retention may improve selective risk, but gain and monotonicity may vary under compound shift.
* F4: Source-calibrated conformal sets may under-cover or otherwise deviate from nominal coverage after shift.
* F5: Domain shift, modality loss, and their interaction have distinguishable contributions after confound controls.
* F6: A lightweight conditional calibrator may help only after a diagnosed, reproducible baseline failure.

All are UNTESTED. H1–H7 remain preserved as historical candidates in `docs/hypothesis_registry.md`; F1–F6 supersede them for the frozen protocol.

## 17. Statistical Analysis Direction

Treat known/unseen domain and full/missing modality as factorial factors and estimate their DOMAIN × MODALITY interaction rather than only isolated pairwise differences. Include dataset heterogeneity, mask type, and seed. Use paired comparisons where predictions are paired. Use subject-level bootstrap intervals and hierarchical/cluster-robust analysis with recordings/nights nested within subjects. PSG epochs from the same participant are correlated and must not be treated as statistically independent observations for confidence intervals or significance tests.

## 18. Target-Free Protocol Definition

Before final target evaluation, target labels and target observations are prohibited for model fitting, hyperparameter selection, checkpoint selection, normalization fitting, feature selection, temperature fitting, calibration-model fitting, abstention-threshold tuning, conformal calibration, and model selection. The preferred primary protocol uses no target data, labeled or unlabeled, before evaluation. Unlabeled-target adaptation is a separate, explicitly labeled setting. Oracle target calibration is an upper bound only.

## 19. Conditional Method Policy

No proposed calibration method will be implemented now. It requires: a frozen benchmark; an independently reproduced baseline failure; evidence the failure is not leakage, label mapping, channel incompatibility, or threshold misuse; a preregistered lightweight method; no target labels/data in the primary setting; and a comparison against frozen baselines with subject-level uncertainty intervals.

## 20. Claims We May Make

* The audit supports a qualified interaction-focused reliability benchmark.
* The future study can report empirical calibration, correctness-ranking, selective-risk, and conformal-coverage behavior under explicitly defined conditions.
* Synthetic and structural modality loss are scientifically distinct conditions.
* SF-UIDA is target adaptation, not target-free domain generalization.
* Any method result will be conditional on a documented baseline failure.

## 21. Claims We Must Not Make

* No “first,” “novel,” or “state of the art” claims.
* No claim that RMSSC or Direct Quantification lacks a given evaluation until full methods are inspected.
* No claim that no conformal sleep-staging work exists.
* No unconditional conformal guarantee under dataset or modality shift.
* No conflation of confidence/entropy with calibrated probability.
* No conflation of informal rejection with formal selective prediction.
* No conflation of subjects, recordings, nights, or epochs.
* No clinical, diagnostic, or clinical-grade claims.

## 22. Thesis Falsification Conditions

* A verified paper evaluates essentially the same target-free domain × modality reliability factorial.
* RMSSC or Direct Quantification substantially subsumes the frozen benchmark.
* Candidate datasets cannot support meaningful modality comparison.
* Source-only calibration cannot be defined consistently.
* The apparent interaction is a channel, label, pathology, medication, or acquisition artifact.
* Legal/access constraints prevent a reproducible multi-domain configuration.
* Subject identity and duplicate-recording separation cannot be enforced.

## 23. Files Created

* `docs/claim_evidence_ledger.md`
* `docs/competitor_boundary.md`
* `docs/paper_thesis.md`
* `reports/STEP_03_NOVELTY_GATE_REPORT.md`

## 24. Files Modified

* `docs/conformal_audit.md`
* `docs/dataset_harmonization_audit.md`
* `docs/evaluation_protocol.md`
* `docs/hypothesis_registry.md`
* `docs/literature_audit.md`
* `docs/novelty_analysis.md`
* `docs/research_spec.md`
* `reports/literature_matrix.csv`

## 25. Validation Performed

* Repository preflight: correct path and repository, branch `main`, clean starting tree, expected Step 1/Step 2 commits, Step 2 report present.
* `pytest -q`: `1 passed in 0.01s`; exit 0.
* `python -m compileall -q src tests`: exit 0.
* `git diff --check`: exit 0.
* CSV validation: PASS; 8 data rows and 37 columns, all rows width-consistent.
* Forbidden tracked-artifact scan for PSG files, model/checkpoint files, archives, and PDFs: no matches.
* No dataset, model, or paper PDF files were added to the repository.

## 26. Explicitly Not Done

* no PSG dataset downloaded
* no preprocessing implemented
* no model implemented
* no model trained
* no experimental result fabricated
* no target labels used
* no repository push
* no copyrighted paper PDFs committed

## 27. Recommended Step 4

Perform a source-verified dataset acquisition and raw-schema audit only: obtain approved datasets under their official access terms, record immutable manifests and exact signal/annotation headers, verify subject/night identity and overlap handling, and propose a frozen channel/label harmonization contract before implementing preprocessing.

## 28. Git Status / Diff Summary

Before the Step 3 commit, `git status --short` showed the eight modified files in Section 24 and the four new files in Section 23. Before the Step 3 commit, `git diff --stat` reported 8 tracked files changed, 187 insertions and 191 deletions; untracked files were not included in that stat. Step 1 and Step 2 hashes are recorded in Section 3. The Step 3 commit is `research: freeze ShiftSleep-UQ paper thesis`, created after this report; its exact hash and final clean status must be recorded immediately after commit. Push status: NOT PUSHED.
