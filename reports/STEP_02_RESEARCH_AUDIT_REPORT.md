# ShiftSleep-UQ Step 2 Research Audit Report

## 1. Status

PARTIAL

The repository bootstrap, source-search, literature matrix, dataset audit, harmonization analysis, novelty collision analysis, and protocol updates were completed. The status is PARTIAL because several high-impact collision targets and dataset facts could not be fully verified from accessible primary full text without downloading datasets or bypassing publisher access controls. Those gaps are explicitly retained as `NOT_VERIFIED` and block a final benchmark freeze.

## 2. Research Decision

MODIFY

Based on the literature identified in this audit, continue ShiftSleep-UQ but narrow its claim. Cross-dataset sleep staging, multimodal sleep staging, missing/incomplete modalities, domain-invariant representations, and sleep-staging uncertainty are already established areas. The defensible remaining target is a leakage-safe reliability benchmark that evaluates the interaction between held-out dataset/domain and modality loss, separating source-only calibration from oracle target calibration and reporting calibration, error detection, selective risk-coverage, and empirical conformal coverage.

This is not a priority or “first” claim. RMSSC, the 2026 Direct Quantification paper, and source-free sleep-staging adaptation require a subsequent full-text collision audit. Dataset feasibility also requires a source/schema audit before preprocessing.

Recommended contribution:

- A subject- and dataset-leakage-safe benchmark of uncertainty reliability under dataset/domain shift crossed with synthetic and structural modality loss.
- A systematic analysis of calibration, uncertainty-based error detection, selective prediction, and empirical conformal coverage degradation.
- A later lightweight modality-conditioned calibration method only if a specific baseline failure mode is demonstrated and the method is separately pre-specified.

## 3. Git Baseline

* repository: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* Step 1 baseline commit: `b6dbbe4319538b799eb2537d0321892ff395df93` (`research: bootstrap ShiftSleep-UQ protocol`)
* Step 2 audit commit: `0f76fa63b8fe56090505f75ea908d6da06287dd0` (`research: complete literature and dataset audit`)
* push status: NOT PUSHED; no GitHub push was performed.

The report itself is being recorded as the final Step 2 report after the audit commit; its recording commit will be reported separately if created.

## 4. Literature Search Summary

* search date: 2026-09-01, local EDT.
* sources/databases searched: Crossref metadata API; arXiv abstract/API pages; PubMed search; official PhysioNet dataset pages; National Sleep Research Resource/NSRR dataset page; official NeurIPS proceedings page; DOI landing pages; targeted web search queries.
* search themes: automatic sleep staging domain generalization, cross-dataset staging, missing/incomplete multimodal signals, UQ, calibration, selective prediction, abstention, error detection, conformal prediction, source-free adaptation, and biomedical distribution shift.
* candidate works reviewed: 7 required seed works were bibliographically identified plus RMSSC and targeted source-free adaptation searches. The search also returned adjacent candidate topics, but they were not promoted to the detailed matrix without sufficient verification.
* works included in detailed matrix: 7 rows (the six bibliographically verified seed works plus RMSSC as an unresolved collision target).
* publication-year range in detailed matrix: 2022–2026; the arXiv versions for SleepDG and DREAM were also inspected.
* limitations: publisher pages for IEEE, Elsevier, ACM, and OpenReview were partly blocked by JavaScript/bot checks or HTTP 403; full methods for several papers were therefore not verifiable. The ISRUC official site was inaccessible from the audit environment. Search results are discovery evidence only and were not treated as sufficient support for detailed methodological claims. The search is not an exhaustive systematic review and does not establish priority.

## 5. Closest Prior Work

### SleepTransformer

* citation: Phan, Mikkelsen, Chen, Koch, Mertins, and De Vos, “SleepTransformer: Automatic Sleep Staging With Interpretability and Uncertainty Quantification,” IEEE Transactions on Biomedical Engineering, 2022, DOI `10.1109/TBME.2022.3147187`.
* what it already solves: sequence-to-sequence Transformer sleep staging, interpretability, entropy-based uncertainty, and a deferral motivation; the accessible record states evaluation on two databases of different sizes.
* what it does not establish from inspected sources: strict source-only calibration on unseen datasets, formal risk-coverage/AURC under dataset shift, missing-modality experiments, compound dataset×modality shift, or conformal coverage.
* collision severity: MEDIUM.

### SleepDG

* citation: Wang, Zhao, Jiang, Li, Li, and Pan, “Generalizable Sleep Staging via Multi-Level Domain Alignment,” AAAI, 2024, DOI `10.1609/aaai.v38i1.27779`.
* what it already solves: explicitly frames generalizable sleep staging on unseen datasets; uses epoch-level and sequence-level feature alignment; the accessible abstract states validation on five public datasets.
* what it does not establish from inspected sources: uncertainty/calibration evaluation, missing-modality evaluation, simultaneous compound shift, or formal selective/conformal analysis.
* collision severity: HIGH for cross-dataset generalization; LOW for the reliability interaction.

### CIMSleepNet

* citation: Shen, Xin, Dai, Zhang, and Wang, “Robust Sleep Staging over Incomplete Multimodal Physiological Signals via Contrastive Imagination,” NeurIPS 37, 2024, DOI `10.52202/079017-3557`.
* what it already solves: directly targets incomplete multimodal physiological signals using contrastive imagination; official proceedings verify the title, authors, venue, date, pages, and DOI.
* what it does not establish from inspected sources: the exact missingness patterns and whether they are synthetic or natural, strict cross-dataset generalization, calibration, formal selective prediction, or conformal coverage.
* collision severity: HIGH for missing-modality robustness; MEDIUM for the proposed compound reliability benchmark.

### U-PASS

* citation: Heremans, Seedat, Buyse, Testelmans, van der Schaar, and De Vos, “U-PASS: An uncertainty-guided deep learning pipeline for automated sleep staging,” Computers in Biology and Medicine, 2024, DOI `10.1016/j.compbiomed.2024.108205`.
* what it already solves: uncertainty is incorporated during acquisition, training, and deployment; PubMed’s accessible record describes supervised pre-training and recording-wise semi-supervised fine-tuning.
* what it does not establish from inspected sources: exact datasets, formal post-hoc calibration, cross-dataset protocol, strict target-free calibration, risk-coverage, and conformal coverage.
* collision severity: HIGH for end-to-end sleep-staging UQ; MEDIUM for the proposed shift-reliability analysis.

### DREAM

* citation: Lee, Pham, Cheng, and Zhang, “Domain-Invariant Representation Learning and Sleep Dynamics Modeling for Automatic Sleep Staging,” ACM Transactions on Computing for Healthcare, 2025, DOI `10.1145/3757066`.
* what it already solves: domain/subject-invariant representation learning, sleep-dynamics modeling, use of unlabeled data, and an uncertainty case study. The accessible abstract emphasizes generalization to new subjects and differences between training and testing subjects.
* what it does not establish from inspected sources: that its domain split is a cross-dataset leave-one-domain-out protocol, formal probability calibration, missing-modality robustness, or compound-shift selective/conformal evaluation.
* collision severity: HIGH for domain/subject-invariant representation and UQ; LOW to MEDIUM for the benchmark interaction.

### Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging

* citation: Vainikka, Huttunen, Kainulainen, Korkalainen, and Rusanen, “Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging,” IEEE Transactions on Biomedical Engineering, 2026, DOI `10.1109/TBME.2025.3623380`.
* what it already solves: exact methodological contribution NOT_VERIFIED because the publisher page was blocked; Crossref verifies the 2026 journal record.
* what it does not establish: NOT_VERIFIED. This paper is a major collision constraint and must be read in full before narrowing claims further.
* collision severity: CRITICAL pending full-text audit.

### RMSSC

* citation: “Robust Multimodal Framework for Sleep Stage Classification with Noisy Labels and Missing Modalities.” Exact bibliographic identity was NOT_VERIFIED.
* what it may already solve: the title indicates noisy-label and missing-modality robustness, but no methodological claim is accepted until the exact paper is located and verified.
* what it does not establish: NOT_VERIFIED, including whether held-out dataset generalization, simultaneous missingness plus domain shift, calibration, selective prediction, or conformal prediction are included.
* collision severity: CRITICAL pending identity and full-text verification.

## 6. Novelty Matrix

| ID | Classification | Strongest supporting/colliding papers | Confidence |
|---|---|---|---|
| N1 | ALREADY_ESTABLISHED | SleepDG | HIGH |
| N2 | ALREADY_ESTABLISHED | CIMSleepNet and related multimodal work | HIGH |
| N3 | PARTIALLY_ESTABLISHED | CIMSleepNet | MEDIUM |
| N4 | ALREADY_ESTABLISHED | SleepDG, DREAM | HIGH |
| N5 | ALREADY_ESTABLISHED | SleepTransformer, U-PASS, DREAM | HIGH |
| N6 | UNCERTAIN | UQ papers identified, formal calibration not verified | LOW |
| N7 | APPARENT_GAP | Cross-dataset and UQ clusters are separate in inspected evidence | LOW |
| N8 | APPARENT_GAP | SleepTransformer deferral motivation; formal cross-dataset risk-coverage unverified | LOW |
| N9 | APPARENT_GAP | CIMSleepNet missing-modality collision; risk-coverage unverified | LOW |
| N10 | APPARENT_GAP | No verified compound risk-coverage analysis | LOW |
| N11 | APPARENT_GAP | No verified strict source-only calibration on unseen datasets | LOW |
| N12 | APPARENT_GAP | No verified compound calibration degradation study | LOW |
| N13 | APPARENT_GAP | No direct sleep-staging conformal work verified | LOW |
| N14 | APPARENT_GAP | No direct sleep-staging conformal work verified | LOW |
| N15 | APPARENT_GAP | No direct compound conformal study verified | LOW |
| N16 | UNCERTAIN | Direct comparator not verified | LOW |
| N17 | APPARENT_GAP | Source-free sleep-staging collision search unresolved | LOW |
| N18 | APPARENT_GAP | No verified unified dataset×availability×reliability benchmark | LOW |

The apparent-gap classifications are supported only by the bounded search and the inspected source content. They are not priority claims. The collision analysis is recorded in full in `docs/novelty_analysis.md`.

## 7. Defensible Research Gap

A defensible target remains: characterize how source-calibrated predictive reliability changes when a model is evaluated on an unseen PSG dataset/domain and simultaneously loses one or more modality families, distinguishing synthetic masking from structural channel mismatch. The analysis should use subject-level resampling, formal risk-coverage rather than informal rejection, and conformal empirical coverage with explicit guarantee limitations.

## 8. Dataset Audit

### Sleep-EDF Expanded v1.0.0

* verified subjects: SC subject count NOT_VERIFIED; ST has 22 subjects.
* recordings: 197 total; 153 SC files and 44 ST files. These are recordings/files, not people.
* modalities: Fpz-Cz and Pz-Oz EEG, horizontal EOG, submental chin EMG; some SC records additionally have respiration and temperature.
* channel information: official page states EEG/EOG at 100 Hz and SC chin EMG as a filtered, rectified, low-pass-derived 1-Hz RMS envelope. ST EEG/EOG/EMG are stated as 100 Hz.
* sampling: as above; exact all-signal inventory remains to be audited from headers.
* scoring: manually scored R&K; W, R, 1, 2, 3, 4, M, and ?.
* access: PhysioNet open access under Open Data Commons Attribution License v1.0; official page states 8.1 GB uncompressed.
* caveats: repeated nights, different study/device settings, temazepam/placebo in ST, and non-equivalent EMG representation. SC and ST should not be silently merged.

### ISRUC-Sleep

* verified subjects, recordings, modalities, channel information, sampling, scoring, access details: NOT_VERIFIED.
* major caveat: official site was blocked as a private/internal target by the extraction environment. It is excluded from the primary configuration until official verification.

### Sleep Heart Health Study / SHHS

* verified subjects: NSRR page reports 6,441 Visit 1 enrollees and a second PSG for 3,295 participants at Visit 2. The exact usable PSG subject count was NOT_VERIFIED.
* recordings: exact available recording count NOT_VERIFIED. Visit 1 and Visit 2 PSGs must be treated as potentially repeated observations from participants.
* modalities/channel information/sampling/scoring: exact inventory NOT_VERIFIED in this audit; NSRR exposes montage and sampling-rate manuals that must be audited before inclusion.
* access: hosted by NSRR; account/request and current terms require a dedicated access audit.
* caveats: multi-center cohort, repeated visits, cohort and age/population structure, and possible participant overlap across visits.

### CAP Sleep Database v1.0.0

* verified subjects: 16 healthy subjects are stated; unique pathological subject count NOT_VERIFIED.
* recordings: 108 polysomnographic recordings. Do not equate 108 recordings with 108 subjects.
* modalities: at least three EEG channels, two EOG channels, submentalis and bilateral anterior tibial EMG, respiration, SaO2, and ECG.
* channel information: official page states F3/F4, C3/C4, and O1/O2 referenced to A1/A2, plus bipolar traces.
* sampling: exact per-signal rates NOT_VERIFIED in this audit.
* scoring: R&K macrostructure plus CAP annotations using Terzano’s rules; W, S1-S4, REM, and MT are documented.
* access: PhysioNet open access; exact license text should be rechecked before redistribution.
* caveats: 92 pathological recordings across several disorders and 16 healthy controls; pathology, clinical setting, and channel richness make CAP better suited as an external stress test than as an unqualified primary domain.

## 9. Channel Harmonization Decision

Level A modality-family harmonization is feasible as a planning abstraction. Level B approximate anatomical harmonization is scientifically preferable if the official SHHS/ISRUC manuals establish comparable leads and references. Level C exact channel harmonization is not currently defensible across all candidates.

No exact primary channel set is frozen. Currently defensible candidate families are: EEG as dataset-verified sleep EEG leads with reference metadata retained; EOG as dataset-verified horizontal or bilateral EOG with reference metadata retained; and EMG as dataset-verified chin/submentalis EMG, explicitly distinguishing raw signals from derived/envelope signals. Dataset/device/montage differences may be treated as part of domain shift, but cannot be erased by renaming channels.

## 10. Label Harmonization Decision

Provisional target space remains Wake, N1, N2, N3, REM. R&K S3+S4 → N3 is **QUESTIONABLE pending source-supported mapping audit**, not frozen solely by convention. Wake and REM are generally candidate mappings but still require annotation semantics. Movement Time, `?`, unknown, artifacts, unscored epochs, and disagreement must be excluded or handled under an explicit frozen policy; no policy is finalized here.

CAP’s R&K S1-S4 and CAP-specific annotations, and Sleep-EDF’s movement/not-scored labels, demonstrate why label transformation must preserve exclusions and provenance.

## 11. Dataset Configuration Recommendation

**PRIMARY BENCHMARK:** Two-source plus one held-out external target, selected only after official channel/label/access verification. Sleep-EDF SC and ST should be separate candidate domains rather than automatically pooled. A three-domain leave-one-dataset-out design is desirable only if ISRUC or SHHS passes the data audit.

**EXTERNAL STRESS TEST:** CAP Sleep Database, treated as a pathology/device/scoring stress test with separate interpretation and no unqualified pooling into the healthy primary benchmark.

**DEFERRED / EXCLUDED:** ISRUC until official access and channel/scoring facts are verified; SHHS until exact usable PSG/channel metadata and participant identity handling are verified; any dataset whose license or label semantics remain unclear.

Candidate A is scientifically strongest if three comparable datasets are verified but has the highest harmonization burden. Candidate B is the most defensible interim design because it isolates one target and reduces source heterogeneity, but its domain inference is narrower. Candidate C is useful for stress testing but pathology and acquisition confounding make it unsuitable as the only primary domain-shift test.

## 12. Compound-Shift Protocol

* **S0:** source/known domain + full modalities.
* **S1:** source/known domain + synthetic modality missingness.
* **S2:** unseen dataset/domain + full modalities.
* **S3:** unseen dataset/domain + one missing modality.
* **S4:** unseen dataset/domain + multiple missing modalities.

Synthetic missingness masks a modality that exists in the original record. Structural mismatch means the modality was never acquired, is unavailable, or cannot be harmonized. These conditions require different identifiers, analyses, and claims. The provisional mask vocabulary is recorded in `docs/benchmark_spec.md` but is not yet admissible for data execution.

## 13. Calibration Protocol Recommendation

### PRIMARY metrics

Multiclass Brier score, NLL, ECE with a predeclared binning rule, reliability diagrams, and calibration/error results by domain and modality condition. Report empirical conformal coverage and nominal-minus-empirical coverage gap when conformal methods are introduced.

### SECONDARY metrics

Adaptive/equal-mass ECE, class-wise calibration, per-stage recall, balanced accuracy, macro-F1, and Cohen’s kappa.

### DIAGNOSTIC plots/metrics

Confidence and entropy distributions, stage-wise reliability, confusion matrices, uncertainty by mask/domain, and subgroup slices only when metadata are verified. ECE is not sufficient by itself because it depends on binning, sample size, class imbalance, and aggregation.

## 14. Selective Prediction Protocol

Use confidence, predictive entropy, and any later MC-dropout/ensemble disagreement as uncertainty scores, but label them as scores rather than calibrated probabilities. The core analysis should report risk-coverage curves, AURC, selective macro-F1, risk at predefined coverage, and coverage at predefined risk. Use AUROC for correctness detection and AUPRC when correctness imbalance makes AUROC incomplete. Formal selective prediction requires the full risk-versus-coverage curve; merely removing low-confidence epochs is insufficient.

## 15. Conformal Prediction Findings

* assumptions: exchangeability or another explicitly justified condition between calibration and test observations; calibration procedure and score must be frozen.
* guarantee limitations under shift: source-domain finite-sample nominal coverage does not imply the same coverage on an unseen dataset, shifted acquisition system, or changed missingness distribution. PSG epoch dependence additionally invalidates treating epochs as independent statistical units for uncertainty intervals.
* candidate methods: APS or RAPS multiclass conformal prediction, subject/recording-aware evaluation, and clearly separated source-only versus ORACLE TARGET CALIBRATION.
* paper role: retain conformal coverage degradation as a secondary research axis, subject to implementation and data feasibility.
* novelty assessment: APPARENT_GAP / LOW confidence for direct sleep-staging compound-shift conformal analysis; no unconditional priority claim.

## 16. Leakage / Statistical Risks Discovered

* Sleep-EDF’s 197 recordings must not be reported as 197 subjects.
* SC and ST repeated nights can leak participants across splits if identifiers are mishandled.
* SHHS Visit 1 and Visit 2 may contain repeated participants.
* Dataset-derived benchmark collections can create duplicate or overlapping recordings.
* EMG envelope versus raw EMG is a representation mismatch, not ordinary missingness.
* Different montage/reference/device settings can become hidden dataset labels.
* R&K and AASM mappings, movement, unknown, artifact, and unscored epochs can create label leakage or selective exclusion.
* Target-domain labels must not enter strict source-only calibration or threshold selection.
* Confidence/entropy is not automatically calibrated uncertainty.
* Deferral is not automatically formal selective prediction.
* Conformal nominal coverage cannot be presented as unseen-domain coverage without assumptions.
* Epochs within a PSG and subjects with repeated recordings are correlated; subject/recording-level resampling is required.
* Pathology, medication/placebo, age, cohort, and recording setting may confound the interpretation of domain shift.
* Unverified access terms can prevent legal redistribution or reproducibility.

## 17. Changes Made to Step 1 Specification

### Change 1

**OLD:** Candidate datasets were listed without a substudy/domain recommendation, and Sleep-EDF was treated as a candidate dataset at a single level.

**NEW:** Sleep-EDF SC and ST are separate candidate domains/subdomains pending identity and channel audit; CAP is recommended as an external pathology/device stress test rather than automatically as a primary dataset.

**REASON:** The official PhysioNet page distinguishes 153 SC files from 44 ST files, identifies repeated nights, different study settings, temazepam/placebo in ST, and different EMG representations.

### Change 2

**OLD:** Candidate EEG/EOG/EMG families were proposed without an explicit harmonization level.

**NEW:** Level A family harmonization is a planning abstraction; Level B approximate anatomical harmonization is preferred if verified; Level C exact harmonization is not currently frozen.

**REASON:** Official Sleep-EDF and CAP pages show different leads, references, sampling, and EMG representations; SHHS/ISRUC exact inventories remain unresolved.

### Change 3

**OLD:** The five-class mapping was provisional without a source-audit warning.

**NEW:** Wake/N1/N2/N3/REM remains provisional; R&K S3+S4 → N3 is QUESTIONABLE pending verification, and movement/unknown/artifact/unscored policies remain unresolved.

**REASON:** Candidate datasets use R&K and include labels outside the five target classes; convention alone is insufficient for a frozen protocol.

### Change 4

**OLD:** The project’s central contribution was framed broadly around the proposed benchmark.

**NEW:** The contribution is narrowed to a reliability benchmark crossing held-out dataset/domain with modality loss; cross-dataset generalization, multimodal staging, and UQ are established context, not standalone novelty.

**REASON:** SleepDG, CIMSleepNet, SleepTransformer, U-PASS, and DREAM collide with those standalone areas.

## 18. Paper Thesis After Audit

Based on the literature identified in this audit, existing sleep-staging work has separately studied cross-dataset generalization, incomplete multimodal signals, domain/subject-invariant representation learning, and predictive uncertainty, but the reliability of source-calibrated predictions under the interaction of an unseen PSG domain and modality loss remains insufficiently characterized in the accessible evidence. ShiftSleep-UQ should therefore evaluate calibration, uncertainty-based error detection, selective prediction, and empirical conformal coverage across this interaction, while treating synthetic masking and structural channel mismatch as distinct conditions and making no unconditional coverage or priority claims.

## 19. Claims We Can Potentially Make

* The project defines a pre-experimental, leakage-safe protocol for evaluating reliability under dataset/domain shift crossed with modality loss.
* The study can potentially provide empirical evidence about calibration, correctness ranking, selective risk, and conformal coverage gaps under specified conditions.
* Any later method claim can be conditional on a preregistered baseline failure mode and a separately controlled comparison.
* The work can report a transparent audit of channel, label, subject-identity, and access limitations.

## 20. Claims We Must NOT Make

* We must not claim first domain-generalized sleep staging.
* We must not claim first missing-modality sleep staging.
* We must not claim first sleep-staging UQ.
* We must not claim first calibration, selective prediction, or conformal sleep-staging study until the collision audit is complete.
* We must not call confidence or entropy calibration without calibration evidence.
* We must not call deferral formal selective prediction without risk-coverage analysis.
* We must not claim nominal conformal coverage on unseen domains.
* We must not equate recordings with subjects.
* We must not call synthetic masking natural channel absence.
* We must not claim clinical validity or diagnostic utility.

## 21. Remaining Unknowns

* Full methods, exact datasets, and calibration/selective/conformal results for RMSSC.
* Full methods and data protocol for the 2026 Direct Quantification paper.
* Exact source-free/personalized sleep-staging adaptation paper and collision status.
* ISRUC official dataset identity, access, channels, sampling, scoring, and terms.
* Exact usable SHHS PSG subject/recording counts, channel references, sampling, scoring, and access workflow.
* Sleep-EDF SC unique-subject count and robust subject/night mapping.
* Dataset overlap and derived benchmark duplication risks.
* Exact per-signal CAP sampling rates and licensing details.
* Final channel harmonization level and admissible mask set.
* R&K/AASM mapping support, unscored/artifact/movement policy, and scorer disagreement policy.
* Whether a three-domain primary benchmark is feasible after legal and channel review.

## 22. Files Created / Modified

### Created

* `docs/literature_audit.md`
* `docs/novelty_analysis.md`
* `docs/dataset_harmonization_audit.md`
* `docs/conformal_audit.md`
* `docs/metric_protocol.md`
* `reports/literature_matrix.csv`
* `reports/STEP_02_RESEARCH_AUDIT_REPORT.md`

### Modified

* `docs/dataset_registry.md`
* `docs/benchmark_spec.md`
* `docs/research_spec.md`

## 23. Validation

* Step 1 preflight: correct repository path, branch `main`, Step 1 report present, and `pytest -q` passed with `1 passed in 0.01s`.
* Step 1 baseline commit created: `b6dbbe4319538b799eb2537d0321892ff395df93`.
* Literature CSV parse: succeeded; 7 rows and 37 columns.
* `python -m compileall -q src tests`: exit 0.
* `pytest -q`: exit 0; `1 passed in 0.03s` before the audit commit.
* `git diff --check`: exit 0 before the audit commit.
* Source verification: Crossref, arXiv, PubMed, PhysioNet, NSRR, and official proceedings pages were accessed; inaccessible/blocked pages were marked `NOT_VERIFIED`.
* No large ML dependencies were installed.
* No model/data asset files were present or downloaded during the audit.
* Step 2 audit commit created: `0f76fa63b8fe56090505f75ea908d6da06287dd0`.

## 24. Explicitly Not Done

* no PSG dataset downloaded
* no preprocessing implemented
* no model implemented
* no model trained
* no experimental numbers fabricated
* no target labels used
* no GitHub push

## 25. Recommended Step 3

Perform one source-verified dataset acquisition and schema audit—without training—covering official access/terms, raw file manifests, subject/night identity, exact signal headers, annotation semantics, overlap checks, and a proposed frozen harmonization contract before any preprocessing implementation.

## 26. Git Diff Summary

At the audit commit, the working tree was clean. The Step 2 audit commit contained 9 files changed, with 233 insertions and 23 deletions relative to the Step 1 baseline. The final report was written after that commit and must be committed as the report-recording change; no push is authorized in Step 2.

A separate report-recording commit will contain this report; no scientific files are changed after the Step 2 audit commit. The audit commit hash reported in Section 3 remains the canonical Step 2 audit milestone.

`git diff --stat` before recording this report was clean at the audit commit.
