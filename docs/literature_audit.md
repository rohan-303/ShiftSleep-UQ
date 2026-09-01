# Source-verified literature audit

**Audit boundary:** 2026-09-01. This is a structured search and verification record, not a claim of exhaustive coverage. Peer-reviewed metadata was checked against Crossref where available; accessible abstracts/full pages were inspected for methodological claims. Publisher pages that returned bot checks/403s are explicitly marked `NOT_VERIFIED`.

## Evidence rules
A confidence/entropy output is recorded as uncertainty quantification, not as calibration. Removing low-confidence predictions is not recorded as formal selective prediction unless risk-versus-coverage is evaluated. New-subject evaluation is not recorded as cross-dataset generalization. Synthetic masking is not recorded as structural channel mismatch.

## Required seed works

### SleepTransformer
Phan, Huy; Mikkelsen, Kaare; Chen, Oliver Y.; Koch, Philipp; Mertins, Alfred; De Vos, Maarten. “SleepTransformer: Automatic Sleep Staging With Interpretability and Uncertainty Quantification.” *IEEE Transactions on Biomedical Engineering*, 2022. DOI: `10.1109/TBME.2022.3147187`. The accessible arXiv record describes a sequence-to-sequence Transformer, entropy-based uncertainty, and two databases of different sizes.[1][2] The accessible abstract does not establish cross-dataset testing, formal calibration metrics, risk-coverage/AURC, or conformal prediction; those fields remain `NOT_VERIFIED` pending full-paper inspection.

### SleepDG
Wang, Jiquan; Zhao, Sha; Jiang, Haiteng; Li, Shijian; Li, Tao; Pan, Gang. “Generalizable Sleep Staging via Multi-Level Domain Alignment.” *Proceedings of the AAAI Conference on Artificial Intelligence*, 2024, 38(1), DOI `10.1609/aaai.v38i1.27779`. The arXiv abstract explicitly defines generalizable sleep staging on unseen datasets, uses epoch- and sequence-level feature alignment, and reports validation on five public datasets.[3][4] The abstract does not establish uncertainty/calibration, missing-modality, or compound-shift evaluation; these are recorded as `NOT_VERIFIED` or `FALSE` only where the inspected source supports absence.

### CIMSleepNet
Shen, Qi; Xin, Junchang; Dai, Bing; Zhang, Shudi; Wang, Zhiqiong. “Robust Sleep Staging over Incomplete Multimodal Physiological Signals via Contrastive Imagination.” *NeurIPS 37*, 2024. DOI `10.52202/079017-3557`.[5] The official proceedings record verifies title, authors, venue, date, pages, and DOI. Missingness mechanism, datasets, natural versus synthetic missingness, cross-dataset testing, and calibration/selective/conformal evaluation require full-paper verification and are `NOT_VERIFIED` in the matrix.

### U-PASS
Heremans, Elisabeth R.M.; Seedat, Nabeel; Buyse, Bertien; Testelmans, Dries; van der Schaar, Mihaela; De Vos, Maarten. “U-PASS: An uncertainty-guided deep learning pipeline for automated sleep staging.” *Computers in Biology and Medicine*, 2024. DOI `10.1016/j.compbiomed.2024.108205`.[6] Crossref verifies the bibliographic record. PubMed’s accessible result describes uncertainty estimation during acquisition, training, and deployment, with supervised pre-training and recording-wise semi-supervised fine-tuning.[7] Full datasets, calibration methodology, formal selective evaluation, target-label use, and cross-dataset protocol remain `NOT_VERIFIED` because the publisher full text was inaccessible in this audit.

### DREAM
Lee, Seungyeon; Pham, Thai-Hoang; Cheng, Zhao; Zhang, Ping. “Domain-Invariant Representation Learning and Sleep Dynamics Modeling for Automatic Sleep Staging.” *ACM Transactions on Computing for Healthcare*, 2025. DOI `10.1145/3757066`.[8][9] The accessible arXiv abstract describes subject-invariant/domain-generalized representations, sleep dynamics, unlabeled data, and an uncertainty case study. The abstract specifically discusses new subjects and differences between training and testing subjects; it does not by itself establish cross-dataset evaluation or formal probability calibration. Those fields remain `NOT_VERIFIED` pending full-text verification.

### Direct Quantification of Uncertainty
Vainikka, Miika; Huttunen, Riku; Kainulainen, Samu; Korkalainen, Henri; Rusanen, Matias. “Direct Quantification of Uncertainty in Deep Learning-Based Automatic Sleep Staging.” *IEEE Transactions on Biomedical Engineering*, 2026. DOI `10.1109/TBME.2025.3623380`.[10] Crossref verifies the 2026 journal record. The accessible publisher page was blocked by a bot check; training/evaluation datasets, UQ method, calibration metrics, selective rejection, and target-label tuning are `NOT_VERIFIED`. This is a high-priority full-text constraint before any novelty conclusion.

### RMSSC
“Robust Multimodal Framework for Sleep Stage Classification with Noisy Labels and Missing Modalities” (RMSSC). Exact authors, venue, DOI, publication status, datasets, and methods were not verified from an authoritative source during this audit. The work is retained as a required collision target, but all matrix fields other than title/search identification are `NOT_VERIFIED`.

### Source-free/unsupervised adaptation
A targeted search was performed for source-free and unsupervised domain adaptation in automatic sleep staging, including the requested personalized sleep-staging direction. No authoritative record sufficiently verified the exact requested paper and its protocol during this audit. It remains an unresolved literature gate rather than evidence of absence.

## Initial synthesis
The accessible evidence supports three separate prior-work clusters: uncertainty/UQ in sleep staging (SleepTransformer, U-PASS, DREAM, Direct Quantification), cross-dataset/domain generalization (SleepDG and potentially DREAM), and incomplete multimodal signals (CIMSleepNet). The audit did not verify a single work that evaluates all three dimensions together with strict source-only calibration, formal risk-coverage analysis, and conformal empirical coverage. This is an apparent gap, not a “first” claim, because RMSSC, Direct Quantification, source-free adaptation, and inaccessible full texts remain collision risks.

## Sources
[1] https://arxiv.org/abs/2105.11043v3
[2] https://doi.org/10.1109/tbme.2022.3147187
[3] https://arxiv.org/abs/2401.05363v5
[4] https://doi.org/10.1609/aaai.v38i1.27779
[5] https://www.proceedings.com/079017-3557.html
[6] https://doi.org/10.1016/j.compbiomed.2024.108205
[7] https://pubmed.ncbi.nlm.nih.gov/?term=U-PASS+sleep+staging
[8] https://arxiv.org/abs/2312.03196v3
[9] https://doi.org/10.1145/3757066
[10] https://doi.org/10.1109/tbme.2025.3623380
