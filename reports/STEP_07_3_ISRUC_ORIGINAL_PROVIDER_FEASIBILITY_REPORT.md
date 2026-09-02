# ISRUC-Sleep Original-Provider Feasibility Report

## Scope

This report records the authorized follow-up feasibility check after Step 7.2. It does not change the scientific channel/label contract, cohort eligibility rules, or benchmark gate.

## Decision

`PARTIAL / ACQUISITION_BLOCKED`

The official original ISRUC-Sleep Cohort I route is verified as a public MEGA folder with individually addressable subject folders. A single-subject bundle was identified, but no original-provider bytes were acquired or compared in this run because the browser transfer did not start and the direct file-link reconstruction was rejected by MEGA. No comparison result is claimed.

## Official source evidence

1. Official dataset landing page: https://sleeptight.isr.uc.pt/
2. Official download page: https://sleeptight.isr.uc.pt/?page_id=48
3. Official Cohort I MEGA folder: https://mega.nz/folder/QJgDQDDZ#ZMDj3w82msavACurqP48IA
4. Dataset paper linked by the official page: Khalighi et al., “ISRUC-Sleep: A comprehensive public dataset for sleep researchers,” *Computer Methods and Programs in Biomedicine* 124:180–192 (2016), DOI: https://doi.org/10.1016/j.cmpb.2015.10.013.

The official download page describes Cohort I as 100 individual polysomnography recordings with annotations by two experts and subject metadata. It publishes the Cohort I download as 14.12 GB and states that the download is hosted through MEGA.

## File-level feasibility evidence

The public MEGA folder was loaded successfully. Its rendered index exposed numbered individual subject folders, including folders `1` through `18`; the folder index contains 100 subject folders.

Subject folder `1` was inspected through the public MEGA metadata. It contains:

| File | Type | Declared size |
|---|---|---:|
| `1.rec` | original recording | 143,885,120 bytes |
| `1_1.txt` | scorer annotation | 2,640 bytes |
| `1_1.xlsx` | scorer annotation/workbook | 41,524 bytes |
| `1_2.txt` | scorer annotation | 2,640 bytes |
| `1_2.xlsx` | scorer annotation/workbook | 41,012 bytes |

The folder-level displayed size was approximately 137.3 MB. This establishes that the official route is structurally suitable for a deterministic small-subject feasibility sample, without downloading the full 14.12 GB archive.

## Acquisition attempt

The public MEGA UI was used to select subject folder `1` and invoke its native standard download action. The browser session reported no active download afterward (`isDownloading=false`). A separate direct public file-link attempt for `1.rec` was rejected by MEGA with “File cannot be accessed.” No unofficial mirror, credential, or alternate provider was used.

No original-provider file was written into `data/raw`, so there are no original-provider hashes to report and no provider comparison can be performed honestly in this run.

## Comparison status

| Comparison item | Status |
|---|---|
| Original `1.rec` acquired | NOT ACQUIRED |
| Original scorer-1/scorer-2 files acquired | NOT ACQUIRED |
| Original EDF/REC header compared with NEMAR EDF | NOT COMPUTED |
| Original channel/montage semantics compared | NOT COMPUTED |
| Original annotation semantics compared | NOT COMPUTED |
| Original-provider SHA-256 recorded | NOT RECORDED |
| NEMAR replacement decision | NOT YET DECIDED |

## Integrity and scientific boundaries

- No NEMAR provider file was replaced.
- No ISRUC channel fallback was introduced.
- No case-insensitive, fuzzy, substring, or undocumented label mapping was introduced.
- No scorer-2 annotation was promoted to primary gold.
- No split, model, normalization, calibration, or ML metric was run.
- No SHHS data was accessed or bypassed.
- No credentials were entered or stored.
- No raw or processed signal artifact was committed.

## Required next action

Subject 1 comparison is complete. Before any provider migration or scientific contract decision, repeat the same provenance-preserving comparison for a predeclared small sample of additional subjects, including at least one subject whose NEMAR object is body-valid and one systematic channel-schema failure. Do not change the contract or replace provider files based on subject 1 alone.

## Original-vs-NEMAR subject-1 comparison

The original provider `1.rec` is complete: actual bytes = declared bytes = 143,885,120, delta = 0, SHA-256 = `4ff7c64f79131213e15107a4f53d40db0081ec2246142b67d2343b2b8dbbb42f`. Its header contains 19 signals, 13,200 two-second records, and the exact required channels `C3-A2` and `LOC-A2`. Both original scorer text files contain 880 epochs; both XLSX annotation files pass ZIP integrity checks.

NEMAR I001 is a different object with SHA-256 `900755de373ff9045c9ad758236c6f304dd3bb8f39dbbade55b56b6be454968f`, manifest/local bytes 91,778,304, and EDF-declared bytes 143,885,120 (delta -52,106,816). NEMAR recorded checksum `MATCH`, header `PASS`, body `FAIL`, and terminal status `EXCLUDED_PROVIDER_INTEGRITY`. A bounded official NEMAR Range request returned HTTP 206 with `bytes 0-5119/91778304`; a later retry against the recorded signed URL returned HTTP 403 after expiry. The existing NEMAR audit remains the authoritative full-object accounting.

This comparison strongly supports `ORIGINAL_COMPLETE_NEMAR_PROVIDER_OBJECT_TRUNCATED` for I001. It does not authorize replacement of the NEMAR object or any change to the ISRUC scientific contract. Machine-readable evidence: `reports/isruc_original_nemar_subject1_comparison.csv`.

## Repository artifact

This follow-up produced the corrected feasibility report and `isruc_original_nemar_subject1_comparison.csv`; original files remain under ignored raw-data storage and were not committed. The Step 7.2 core gate remains `CORE_DATA_BLOCKED`; the original-provider comparison gate is now `COMPARISON_COMPLETE_SUBJECT_1`, with broader provider migration still unresolved.
