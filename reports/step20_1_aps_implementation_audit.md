# APS implementation forensic audit

Implementation: `src/shiftsleep_uq/evaluation_step11.py` (`aps_prediction_set`, `conformal_metrics`) and frozen calibration artifacts under `artifacts/calibration/b0`.

| Component | Finding | Status |
|---|---|---|
| conformity score | cumulative uncalibrated softmax probability through the true label after descending probability sorting | MATCH |
| class sorting | descending probability; ties broken by ascending class index | MATCH |
| calibration quantile | k=ceil((n+1)(1-alpha)), clamped to 1..n, kth ascending score | MATCH |
| set construction | smallest prefix whose cumulative probability reaches qhat | MATCH |
| inequality | cumulative score <= qhat, with prefix inclusion at threshold | MATCH |
| randomization | none | MATCH (non-randomized APS) |
| calibration population | source CAL only | MATCH |
| source TEST population | held-out source TEST, never calibration | MATCH |
| target population | held-out complete target, used only for evaluation | MATCH |
| qhat alpha=.10/.05 | stored per direction/seed in frozen APS calibration JSON | MATCH |
| tie handling | deterministic class-index tie break | MATCH |

No unambiguous APS implementation bug was found. The procedure is valid as implemented but can be conservative because it is non-randomized and finite-sample quantile/set construction can produce large sets. The Figure 2 signed/absolute field mismatch is separate from APS set construction.

Published-definition reference for future manuscript positioning: Romano, Sesia, and Candès, “Classification with Valid and Adaptive Coverage,” NeurIPS 2020, official proceedings record. The frozen implementation uses the APS cumulative-probability score and does not implement weighted conformal prediction.
