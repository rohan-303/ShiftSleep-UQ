# Literature Audit — Step 3 Update

## Audit boundary

This update is a source-verified, bounded collision audit through 2026-09-01. It is not a systematic review and does not establish priority. Publisher/IEEE access restrictions prevented full methods inspection for RMSSC and Direct Quantification.

## Resolved collision

SF-UIDA is verified as Zhou et al., “Personalized Sleep Staging Leveraging Source-free Unsupervised Domain Adaptation,” AAAI 2025, 39(13), 14529–14537, DOI 10.1609/aaai.v39i13.33592. The official AAAI record states that the method adapts to newly appeared unlabeled individuals without source data, using a two-step subject-specific adaptation scheme, and evaluates three public datasets and three classic staging models. This is source-free unsupervised target adaptation, not target-free domain generalization.

## Critical unresolved collisions

RMSSC identity is bibliographically verified by Crossref as Luo, Miao, Guan, Li, Huang, and Li, “RMSSC: A Robust Multimodal Framework for Sleep Stage Classification with Noisy Labels and Missing Modalities,” ICASSP 2026, DOI 10.1109/ICASSP55912.2026.11461625, published 2026-05-03. Full experimental scope remains NOT_VERIFIED. Direct Quantification is bibliographically verified as Vainikka et al., IEEE TBME 2026, DOI 10.1109/TBME.2025.3623380, but its methods remain NOT_VERIFIED.

## Direct search findings

Cross-dataset generalization, incomplete multimodal signals, and sleep-staging UQ are established prior clusters. No verified accessible paper was found that combines the full target-free dataset × modality reliability factorial with calibration, correctness detection, formal risk-coverage, and conformal empirical coverage. This is a qualified apparent gap, not a “first” claim.

A conformal search found an adjacent 2025/26 arXiv compositional-data paper whose abstract mentions a sleep-stage dataset. It is not evidence of the proposed conventional multiclass shifted sleep-staging benchmark. Thus we write “no verified standard compound-shift conformal benchmark identified,” not “no such paper exists.”

## Sources

- https://ojs.aaai.org/index.php/AAAI/article/view/33592
- https://doi.org/10.1109/ICASSP55912.2026.11461625
- https://doi.org/10.1109/tbme.2025.3623380
- https://arxiv.org/abs/2105.11043 (SleepTransformer)
- https://arxiv.org/abs/2401.05363 (SleepDG)
- https://pubmed.ncbi.nlm.nih.gov/?term=U-PASS+sleep+staging
- Official NeurIPS proceedings record for CIMSleepNet
