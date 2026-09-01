# Conformal Audit — Step 3 Update

## Direct search result

No verified standard multiclass automatic sleep-staging conformal-prediction benchmark under simultaneous unseen-dataset and missing-modality shift was identified in the bounded search through 2026-09-01.

A search result did identify an arXiv work titled **Conformal Prediction for Compositional Data** whose abstract reports an application involving sleep stages. This is direct topical adjacency, but it is a compositional-data prediction formulation, not evidence of the ShiftSleep-UQ protocol: its calibration set, exchangeability analysis under dataset shift, missing-modality condition, and subject-level sleep-staging reliability interpretation require separate inspection. Therefore the project must not claim that no conformal work exists.

## What can be evaluated later

APS/RAPS-style multiclass prediction sets may be considered only after data and label semantics are frozen. Source calibration and target evaluation must be separated. Report empirical coverage, nominal-minus-empirical gap, and set size by domain and modality condition.

## Guarantee boundary

Nominal finite-sample coverage under calibration/test exchangeability does not automatically transfer to an unseen dataset, changed acquisition system, or changed missingness distribution. Empirical undercoverage under shift is a measurable result, not proof that all conformal guarantees fail universally. Epoch dependence requires subject-level uncertainty intervals and prevents naïve epoch-level significance claims.
