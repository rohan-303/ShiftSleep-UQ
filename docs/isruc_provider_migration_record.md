# ISRUC Provider Migration Record

## Old provider
NEMAR `nm000111 v1.0.1`.

## New provider
Official ISRUC-Sleep Cohort I public MEGA distribution, acquired account-free with MEGAcmd 2.6.0.0.

## Evidence
Step 7.3/7.4 predeclared provider replication demonstrated complete original I001/I002/I003 recordings, truncated NEMAR I001/I002 objects, complete NEMAR I003, and faithful retained overlap. Step 7.5 acquired original bundles for subjects I001–I035; 35 original REC bodies are valid and 17 pass the frozen required-channel/schema/annotation/output gates. MEGA bandwidth quota blocked continuation at I036 after a resumable partial transfer.

## Decision
The primary provider migration is authorized but the original-provider cohort is **PARTIAL**, not frozen. The old NEMAR cohort is historical provenance and cannot be marked fully superseded until all 100 expected subjects receive terminal validated decisions and the cohort gate is resolved.

## Old cohort
Historical NEMAR-derived ISRUC cohort: 15 included subjects out of 100 expected (15.00%); historical manifests and reports are preserved. The old active-primary status is `SUPERSEDED_PENDING_SUCCESSFUL_ORIGINAL_REBUILD`.

## New cohort
`configs/isruc_original_cohort_v1.yaml`, 17 included and 83 excluded, status `PARTIAL_ACQUISITION_BANDWIDTH_BLOCKED`.

## Scientific-contract impact
NONE. The provider/provenance layer changed; labels, scorer-1 policy, channels, rates, units, epoch semantics, Wake policy, preprocessing, and normalization policy did not.

## Step 7.8 outcome

I036 is now a complete original-provider bundle and validates with body delta 0. I001-I036 were rebuilt under contract `1.2.0`; 17 subjects are `ISRUC_A1A2` and 19 are `ISRUC_M1M2`. All 36 included outputs passed accounting and deterministic reprocessing. I037-I100 remain unacquired because the approved account-free MEGA client/route is unavailable in the current environment after the documented bandwidth-quota boundary. The v2 cohort is therefore `ISRUC_ORIGINAL_COHORT_PARTIAL`; the historical NEMAR cohort and v1 partial original-provider cohort remain preserved and are not marked fully superseded. No accessible-core freeze was performed.
