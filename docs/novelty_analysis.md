# Step 3 Novelty Collision Analysis

## Scope and evidence boundary

This is a bounded, source-verified audit through 2026-09-01, not a systematic review and not evidence of priority. Publisher access restrictions left two critical papers methodologically unresolved.

## Critical collision conclusions

### RMSSC

Crossref verifies: Luo, Miao, Guan, Li, Huang, and Li, “RMSSC: A Robust Multimodal Framework for Sleep Stage Classification with Noisy Labels and Missing Modalities,” ICASSP 2026, DOI `10.1109/ICASSP55912.2026.11461625`, published 2026-05-03; page range NOT_VERIFIED. The title establishes a missing-modality/multimodal collision, but IEEE full text was inaccessible. Datasets, ISRUC subsets, modality masks, synthetic/natural missingness, split policy, domain-generalization protocol, calibration, error detection, selective prediction, and conformal prediction are all NOT_VERIFIED. Collision: **NOT_VERIFIED** for the central contribution; definitely an established adjacent collision for missing-modality robustness.

### Direct Quantification

Crossref verifies Vainikka, Huttunen, Kainulainen, Korkalainen, and Rusanen, “Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging,” IEEE TBME, 2026, DOI `10.1109/TBME.2025.3623380`; Crossref publication date June 2026. Model, datasets, MC dropout, Hypnodensity Interval, rejection experiment, calibration metrics, risk-coverage, missing modalities, and conformal prediction remain NOT_VERIFIED because the accessible publisher page was blocked. Collision: **NOT_VERIFIED**.

### SF-UIDA

Zhou et al., “Personalized Sleep Staging Leveraging Source-free Unsupervised Domain Adaptation,” AAAI 2025, 39(13):14529–14537, DOI `10.1609/aaai.v39i13.33592`. Official AAAI abstract verifies source-free adaptation to newly appearing unlabeled individuals without source data, using pseudo-label fine-tuning and sequential cross-view contrasting, evaluated on three public datasets and three classic models. This is **not** pure target-free domain generalization: unlabeled target individuals are used for adaptation. Missing modality, calibration/UQ, formal selective prediction, and conformal prediction are not described in the official abstract. Collision with the strict main benchmark: **PARTIAL**.

## Direct calibration/selective/conformal findings

- Direct sleep-staging UQ is established. Direct probability calibration under cross-dataset × missing-modality shift was not verified.
- SleepTransformer and U-PASS support uncertainty/deferral concepts, but accessible evidence does not establish formal risk-versus-coverage/AURC under compound shift.
- A formal selective-prediction result requires risk-coverage or equivalent coverage-at-risk analysis; deleting uncertain predictions alone is insufficient.
- No verified standard multiclass sleep-staging conformal benchmark under compound dataset × modality shift was found. A search result identified a 2025/26 arXiv paper on conformal prediction for compositional data that includes a sleep-stage dataset, but it is an adjacent formulation rather than evidence of the proposed target-free shifted sleep-staging protocol.

## Decision

The project should proceed only with a qualified interaction-focused benchmark thesis. Because RMSSC and Direct Quantification remain critical unresolved collisions, Step 3 status is PARTIAL and research decision is MODIFY rather than GO.
