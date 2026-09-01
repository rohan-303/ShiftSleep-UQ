# SHHS Access Plan

## Current state

`PUBLIC_METADATA_VERIFIED`; `RAW_ACCESS_PENDING`. Local environment inspection found no NSRR/SHHS access variables and no local SHHS raw files. No credentials, cookies, tokens, or agreement acceptance were automated, requested, stored, or exposed.

## Intended primary channel contract

SHHS1 is a planned third domain with `C3-A2` EEG at nominal 125 Hz and `EOG(L)-PG1` at nominal 50 Hz. These are intended labels, not a claim that every file conforms. The future loader must inspect every EDF header and quarantine records missing an exact channel or having an unexpected native rate. No silent channel fallback is allowed.

## Required Human Action

1. Visit the official NSRR/SleepData SHHS resource.
2. Create or sign in to an account.
3. Review the current data-use terms.
4. Request/enable access as officially required.
5. Use this project description:

> Research on robust and uncertainty-aware automatic sleep staging under cross-dataset and missing-modality shift. The study will use de-identified polysomnography signals and sleep-stage annotations to evaluate calibration, selective prediction, and model reliability. No attempt will be made to re-identify participants.

Do not automate acceptance and do not provide credentials to this project.

## Minimum files eventually needed

* selected SHHS1 EDF recordings;
* corresponding official NSRR XML sleep-stage annotations;
* participant/file mapping needed for subject grouping;
* public schema metadata and per-record headers.

Do not download these files without legitimate authorized access.

## Role and freeze semantics

SHHS1 is `PLANNED_PRIMARY_DOMAIN_PENDING_RAW_ACCESS`. It remains part of the intended three-domain paper benchmark, but it is not acquired and cannot be represented as an accessible dataset. The accessible core may proceed to deterministic preprocessing engineering without model/result claims; the final benchmark remains unfrozen until SHHS1 is authorized, acquired, and per-record schema validated.
