# ISRUC Original-Provider Migration Provenance

## Step 7.5 scope

This record documents the full original-provider ISRUC-S1 migration and cohort-rebuild attempt. The expected population is frozen at 100 numbered Cohort I subjects before acquisition outcomes are used.

## Provider change

- Old primary ISRUC signal provider: **NEMAR nm000111 v1.0.1**.
- New primary ISRUC signal provider: **official ISRUC-Sleep Cohort I MEGA distribution**.
- Reason: Step 7.3/7.4 demonstrated selective NEMAR provider-object truncation. I001 and I002 were truncated while retaining faithful prefixes; I003 was complete and fully signal-equivalent.
- Scientific contract change: **NO**.
- Provider/provenance change: **YES**.
- Old NEMAR cohort status: **SUPERSEDED_PENDING_SUCCESSFUL_ORIGINAL_REBUILD**.

The old cohort is not called fully superseded until the new original-provider cohort has passed acquisition, validation, preprocessing, and cohort-gate checks.

## Expected population freeze

The expected ISRUC-S1 population is exactly subjects 1 through 100, one recording per subject. The frozen population is recorded in `reports/isruc_original_expected_population.csv`. Failed, missing, or structurally invalid subjects remain represented with terminal statuses and are not removed from the expected-population file.

## Acquisition route

Acquisition uses the same account-free public-folder MEGAcmd mechanism validated in Step 7.4:

- MEGAcmd version: 2.6.0.0, 64-bit.
- Public-folder addressing: individually numbered official subject folders.
- Local client: `C:/Users/rohan/AppData/Local/MEGAcmd/mega-get.bat`.
- No personal MEGA account, credentials, private URLs, or signed URLs are used or recorded.

## Raw-directory contract

Existing subject 1–3 bytes remain at their established paths. Newly acquired subjects use deterministic directories under `data/raw/isruc-original/subject-N/N/`. All raw files remain Git-ignored and immutable after successful validation.

## Scientific-contract guard

The migration preserves the frozen contract: scorer 1 is primary; scorer 2 is diagnostic; required channels are `C3-A2` and `LOC-A2`; native rates are 200 Hz; targets are EEG 100 Hz and EOG 50 Hz; units are microvolts; epochs are 30 seconds; outputs remain unnormalized and unstandardized; and canonical labels remain Wake, N1, N2, N3, and REM.

## Status semantics

This provenance record is created before full acquisition and does not itself assert that the migration succeeded. Final status is determined by the Step 7.5 report and authoritative manifests.
