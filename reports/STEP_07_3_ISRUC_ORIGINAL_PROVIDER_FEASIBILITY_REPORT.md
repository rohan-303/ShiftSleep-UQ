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
4. Dataset paper linked by the official page: “ISRUC-Sleep: A comprehensive public dataset for sleep researchers” (Sleep and Breathing, 2016).

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

Run the same subject-1 comparison from a user-authorized environment with a functioning MEGA transfer client or browser download path. Preserve the original files immutably, record source URLs/MEGA identifiers, local byte sizes, SHA-256 hashes, REC/EDF header fields, annotation file hashes, and exact comparison outcomes. Do not perform a provider migration or change the frozen ISRUC contract until that comparison is complete.

## Repository artifact

This feasibility report is the only new research artifact from this follow-up. The Step 7.2 core gate remains `CORE_DATA_BLOCKED`; the original-provider comparison gate is `ACQUISITION_BLOCKED`.
