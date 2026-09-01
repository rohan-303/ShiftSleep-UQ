# Conformal prediction audit

Split/conformal classification relies on an exchangeability condition between calibration and test examples (or an explicitly justified alternative). A source-calibrated score can have finite-sample nominal coverage for an exchangeable target distribution; that does not establish the same coverage on an unseen dataset, a different acquisition system, or a missing-modality distribution.

## What ShiftSleep-UQ may claim

- **Nominal coverage:** the requested target level, such as 90%.
- **Empirical coverage:** the observed fraction of test subjects/epochs whose true class is in the prediction set.
- **Coverage gap:** nominal minus empirical coverage, with subject-level uncertainty intervals.
- Under dataset/modality shift, report empirical behavior and violations/limitations; do not claim guaranteed 90% coverage on unseen domains.

## Candidate methods
APS and RAPS are reasonable multiclass conformal candidates if their score definitions, calibration unit, tie handling, and finite-sample conventions are frozen. A later implementation must compare at least source-only calibration against explicitly labeled ORACLE TARGET CALIBRATION. The target-free protocol cannot use held-out target labels for score, threshold, or method selection.

## Sleep-staging evidence
No direct sleep-staging conformal paper was verified in this audit. Adjacent conformal biomedical/time-series work was not sufficiently source-verified to support a direct collision claim. Therefore compound-shift conformal coverage remains an **APPARENT_GAP / LOW confidence**, not proof of priority.

## Guarantee boundary
Conformal guarantees must be conditioned on their assumptions and calibration design. Distribution shift, dependent PSG epochs, subject-level clustering, missingness mechanisms, and dataset overlap can invalidate naive interpretations. The statistical unit for uncertainty intervals remains the participant/recording cluster, not independent PSG epochs.
