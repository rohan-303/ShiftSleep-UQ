# R3 Existing Attempt Reconciliation v1

## Authoritative status

`R3_D1_SLEEPEDF_TO_ISRUC_S0_SEED_17 / ATTEMPT_003` is classified as:

`ACCEPTED_EXISTING_R3_JOB`

## Evidence

- Attempt namespace: `artifacts/remediation/r3/R3_D1_SLEEPEDF_TO_ISRUC_S0_SEED_17/ATTEMPT_003/`
- Completion marker: present with `status=COMPLETE`.
- Run manifest: present with `status=COMPLETE`.
- Training history: present with 10 epochs.
- Checkpoint: present and non-empty.
- Best epoch: 9.
- DEV macro-F1: `0.793102551969719`.
- DEV NLL: `0.3046142043351252`.
- Trainable parameter count: `117062`.
- Protocol SHA-256: `c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b`.
- Checkpoint SHA-256: `fea0bfd46d9b537c76deab3938b26202cb49ceadf533abcd704b2238490d54fa`.
- Normalization SHA-256: `79bf105afa54d8ecd8f5bfd23b9e92321b3aa924eda4405c4c9e2f4092721017`.
- Initialization SHA-256: `c259adee1807211dc322e7b68cf92d2cecbae88e57ec75a28ec9f818123d457e`.
- Normalization scope: `SOURCE_TRAIN_ONLY`.

The checkpoint metadata independently records the job identity, selected epoch, initialization hash, and normalization hash. The existing job is retained and will be referenced by the R3 checkpoint manifest; it will not be blindly retrained.

## Prior reporting correction

The preceding Step 20.2.4 report simultaneously stated that zero R3 jobs were accepted and that one R3 job had completed. That was a reporting inconsistency. The authoritative corrected count is **1 accepted existing R3 job**, with the remaining 11 jobs not yet accepted.

## Scientific boundary

This reconciliation does not add target evaluation, calibration, prediction bundles, or new model selection. The existing DEV selection remains source-only. The frozen v2 protocol is unchanged.

## Remaining validation limitation

The current run manifest predates the explicit `attempt` field and therefore does not contain it. The attempt identity is unambiguous from its immutable filesystem namespace (`ATTEMPT_003`). The final checkpoint manifest will record `attempt=3` explicitly as a derived namespace field and preserve the original run manifest unchanged.
