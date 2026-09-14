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

## Step 7.11 outcome

The official account-free MEGA quota reset and I072-I100 were acquired sequentially. All 100 expected original-provider bundles are terminally accounted for; 99 subjects are included and I040 remains the sole structural exclusion under the unchanged exact montage contract. I095 contains one inventoried extra provider file, while its five primary roles and REC body are valid. Final included montage counts are 17 `ISRUC_A1A2` and 82 `ISRUC_M1M2`, with 89,312 valid epochs. The original-provider v3 cohort is `ACTIVE_FROZEN`; the historical NEMAR cohort and original-provider v1/v2 partial artifacts are superseded. Sleep-EDF remains independently credible at 78 subjects, 153 recordings, and 414,961 epochs. The accessible core is frozen without splits. SHHS remains unaccessed, so the final benchmark gate remains `NO`.
