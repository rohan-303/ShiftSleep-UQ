# Step 7 Preflight Resolution

## Previous decision

`BLOCKED` in `reports/STEP_07_FULL_CORE_DATA_REPORT.md`.

## Root cause

The prior preflight interpreted the presence of exact Sleep-EDF/R&K aliases (`Sleep stage 1`, `Sleep stage 2`, `Sleep stage 3`, `Sleep stage 4`) together with exact NEMAR ISRUC aliases (`Sleep stage N1`, `Sleep stage N2`, `Sleep stage N3`) in the shared canonical mapping as proof that the contract allowed fuzzy or unsupported matching.

## Evidence reviewed

The committed Step 6.1 report states that the repair:

* added exact NEMAR labels `Sleep stage N1`, `Sleep stage N2`, and `Sleep stage N3`;
* retained exact Sleep-EDF numbered/R&K aliases;
* uses exact matching after whitespace normalization;
* does not silently accept lowercase/fuzzy variants; and
* recorded verified source strings without changing canonical scientific decisions.

The local official Sleep-EDF hypnogram audit observed exact labels `Sleep stage W`, `Sleep stage 1`, `Sleep stage 2`, `Sleep stage 3`, `Sleep stage 4`, `Sleep stage R`, `Sleep stage ?`, and, where present, `Movement time`.

The NEMAR v1.0.1 documentation and local ISRUC events audits observed exact labels `Sleep stage W`, `Sleep stage N1`, `Sleep stage N2`, `Sleep stage N3`, `Sleep stage R`, and `Sleep stage U` in the primary `trial_type` field.

See `reports/canonical_label_alias_provenance.csv` for the complete accepted mapping inventory.

## Correct interpretation

The blocked conclusion was a **false-positive preflight interpretation**. The shared canonicalizer intentionally retains source-supported exact aliases from both datasets. Exact aliases are not fuzzy aliases.

Whitespace normalization is limited to collapsing/removing outer whitespace. It does not lower case, approximate-match, infer stage labels, or change source spelling semantics.

## Contract change required

**NO.**

The scientific contract remains version `1.1.0`. Its accepted canonical labels, primary modalities, channels, rates, unit policy, scorer policy, epoch duration, Wake policy, and exact source-specific aliases are unchanged.

* old data-contract SHA256: `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9`
* new data-contract SHA256: `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9`
* semantic change: `NO`

## Code hardening

Dataset-specific source-label allowlists were added at preprocessing ingestion:

* `sleep_edf_sc` permits only observed/verified official Sleep-EDF labels;
* `isruc_s1` permits only verified NEMAR scorer-1 `trial_type` labels;
* shared canonical mapping is applied only after the dataset allowlist;
* a cross-dataset label, such as ISRUC `Sleep stage 1`, now fails with `ANNOTATION_SOURCE_LABEL_NOT_ALLOWED` rather than being accepted because it is valid in Sleep-EDF;
* internal aliases remain available only to explicit canonical-mapper/test contexts and are not accepted by dataset adapters.

## Preservation of history

`reports/STEP_07_FULL_CORE_DATA_REPORT.md` remains unmodified as historical evidence of the prior blocked decision. This document corrects its interpretation without erasing that provenance.

## Preflight result

The alias-policy blocker is resolved. Step 7 full accessible-core work may proceed only after the remaining Step 7 preflight checks, expected-population freeze, and source-manifest verification pass.
