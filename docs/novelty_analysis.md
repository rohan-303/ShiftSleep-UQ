# Novelty collision analysis

**Positioning rule:** classifications below mean “based on the literature identified in this audit,” not an exhaustive novelty guarantee. The search boundary is 2026-09-01. `UNCERTAIN` is used where required full text or exact bibliographic identity was not verified.

| ID | Proposed area | Classification | Evidence and collision note | Confidence |
|---|---|---|---|---|
| N1 | Cross-dataset sleep-stage generalization | ALREADY_ESTABLISHED | SleepDG explicitly targets unseen datasets and reports five public datasets.[1] | HIGH |
| N2 | Multimodal sleep staging | ALREADY_ESTABLISHED | CIMSleepNet and the candidate literature directly study multimodal physiological signals.[2] | HIGH |
| N3 | Arbitrary missing modalities | PARTIALLY_ESTABLISHED | CIMSleepNet directly addresses incomplete multimodal signals; arbitrary real-world masks and structural mismatch remain unresolved.[2] | MEDIUM |
| N4 | Domain/subject-invariant representations | ALREADY_ESTABLISHED | SleepDG and DREAM explicitly use domain/subject-invariant representation language.[1][3] | HIGH |
| N5 | Sleep-staging UQ | ALREADY_ESTABLISHED | SleepTransformer, U-PASS, and DREAM explicitly describe uncertainty mechanisms.[4][5][3] | HIGH |
| N6 | Post-hoc sleep-staging probability calibration | UNCERTAIN | Candidate sources verify UQ/confidence, but formal post-hoc calibration protocol was not verified. | LOW |
| N7 | Uncertainty error detection under cross-dataset shift | APPARENT_GAP | Cross-dataset generalization and UQ are separately evidenced; their formal error-detection intersection was not verified.[1][3][4] | LOW |
| N8 | Selective prediction under cross-dataset shift | APPARENT_GAP | SleepTransformer mentions deferral, but formal cross-dataset risk-coverage remains unverified.[4] | LOW |
| N9 | Risk-coverage under missing-modality shift | APPARENT_GAP | Incomplete-modality work was identified, but formal risk-coverage was not verified.[2] | LOW |
| N10 | Risk-coverage under compound shift | APPARENT_GAP | No verified work in this audit combines unseen dataset, missing modality, and formal risk-coverage. | LOW |
| N11 | Source-only calibration on unseen datasets | APPARENT_GAP | No verified direct sleep-staging paper established this strict regime; inaccessible papers remain collision risks. | LOW |
| N12 | Calibration degradation under compound shift | APPARENT_GAP | No verified direct study measured source-calibrated reliability across dataset and modality interaction. | LOW |
| N13 | Conformal coverage under cross-dataset sleep shift | APPARENT_GAP | No direct sleep-staging conformal paper was verified in this search; this is not proof of absence. | LOW |
| N14 | Conformal coverage under missing modality | APPARENT_GAP | No direct sleep-staging conformal result was verified. | LOW |
| N15 | Conformal coverage under compound shift | APPARENT_GAP | No direct result was verified; guarantee claims would be invalid without exchangeability. | LOW |
| N16 | Modality-conditioned calibration | UNCERTAIN | Concept is plausible but direct sleep-staging evidence and comparator were not verified. | LOW |
| N17 | Target-free shift-aware calibration | APPARENT_GAP | No verified direct sleep-staging implementation was found; source-free adaptation is an unresolved collision area. | LOW |
| N18 | Unified dataset × modality × uncertainty benchmark | APPARENT_GAP | The identified works cover separate axes; a unified, leakage-safe reliability benchmark was not verified. | LOW |

## Interpretation

The strongest collisions are N1, N2, N4, and N5: these must not be presented as new contributions. N3 is already materially occupied by CIMSleepNet. The defensible candidate is narrower: an evaluation benchmark and analysis of reliability under the interaction of held-out dataset/domain and modality loss, with strict source-only calibration and empirical (not guaranteed) conformal coverage. This remains provisional because RMSSC and the 2026 uncertainty paper were not fully method-audited.

## Sources
[1] https://arxiv.org/abs/2401.05363v5
[2] https://www.proceedings.com/079017-3557.html
[3] https://arxiv.org/abs/2312.03196v3
[4] https://arxiv.org/abs/2105.11043v3
[5] https://pubmed.ncbi.nlm.nih.gov/?term=U-PASS+sleep+staging
