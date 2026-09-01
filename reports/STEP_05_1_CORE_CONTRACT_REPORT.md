# ShiftSleep-UQ Step 5.1 Core Contract Report

## 1. Status

COMPLETE

Step 5.1 closed the accessible two-dataset preprocessing contract while preserving the three-domain final-paper objective. No preprocessing or modeling was executed.

## 2. Core Gate

CORE_PREPROCESSING_FROZEN

The accessible core is Sleep-EDF SC plus ISRUC-S1. Both have deterministic subject identity, exact primary EEG/EOG selections, 30-second label semantics, primary scorer policy, primary exclusions, wake policy, synthetic missingness semantics, target sampling targets, and subject-level grouping rules.

## 3. Final Benchmark Gate

NO

SHHS1 remains an intended third primary domain, but raw/XML access is pending and per-record schema validation has not occurred.

## 4. Repository State

* repository: `C:\Users\rohan\ShiftSleep-UQ`
* branch: `main`
* pre-step HEAD verified: `1aef9253d4c8b7a08975b052a9caf0b50877e003`
* Step 5 substantive commit: `47e800495721cd5d1f70866ea5ef4f9137ac0ce9`
* Step 5 report commit: `cbf332d994e541e463617a3604a31e4ff32e8458`
* Step 5 reported final HEAD: `28990c4590a622df43309f5c150776cdace2b3d4`
* Step 5.1 commit: created after validation with message `research: freeze accessible PSG core contract`
* push status: not pushed
* final working tree: verified clean after the Step 5.1 commit

## 5. Scorer-Policy Correction

Step 5 listed `scorer_disagreement` as a primary exclusion while leaving ISRUC’s primary scorer unset. That was internally inconsistent: disagreement could not be both a secondary diagnostic and an automatic deletion rule without defining which annotation stream constituted primary gold.

The Step 5.1 policy is:

* primary ISRUC gold: scorer 1;
* secondary scorer: scorer 2;
* valid scorer-1 epochs remain in primary training/evaluation even when scorer 2 disagrees;
* scorer disagreement is not a primary exclusion;
* consensus-only evaluation is a secondary sensitivity analysis;
* scorer choice is predeclared and cannot be selected using model performance.

This is supported by the NEMAR v1.0.1 README, which states that scorer-1 Excel files generate the events and scorer-2 labels are retained in annotation extras. The official ISRUC site independently states that recordings were visually scored by two human experts.

Amendment IDs: `A-05.1-02` and `A-05.1-03`.

## 6. ISRUC Channel Evidence

### EEG inventory

The source-backed ISRUC-S1 inventory is:

* `F3-A2` — frontal-left EEG, reference A2;
* `C3-A2` — central-left EEG, reference A2;
* `O1-A2` — occipital-left EEG, reference A2;
* `F4-A1` — frontal-right EEG, reference A1;
* `C4-A1` — central-right EEG, reference A1;
* `O2-A1` — occipital-right EEG, reference A1.

### EOG inventory

* `LOC-A2` — left outer-canthus EOG, reference A2;
* `ROC-A1` — right outer-canthus EOG, reference A1.

### EMG inventory

* `X1` — chin/submental EMG source label;
* `X2` and `X3` — additional source EMG/auxiliary channels whose exact anatomical interpretation is not used by the primary contract.

### Rates

The peer-reviewed ISRUC description reports 200 Hz for the signals. Representative NEMAR S1, S2 session 1, S2 session 2, and S3 sidecars report `SamplingFrequency: 200.0` for the inspected records.

### References and sources

* Khalighi et al., “ISRUC-Sleep: A comprehensive public dataset for sleep researchers,” *Computer Methods and Programs in Biomedicine* 124 (2016), 180–192, DOI `10.1016/j.cmpb.2015.10.013`.
* Official ISRUC project: `https://sleeptight.isr.uc.pt/`.
* Peer-reviewed channel/rate description: PMC article `https://pmc.ncbi.nlm.nih.gov/articles/PMC8946692/`, Section 2.1.
* Independent peer-reviewed cross-check: Frontiers article `https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.973761/full`, Section 2.1.2.
* NEMAR ISRUC record: `https://data.nemar.org/nm000111/v1.0.1/` and its public README/metadata.
* Local representative evidence: `reports/isruc_channel_contract.csv` and `data/raw/metadata/isruc-nemar/v1.0.1/representative/`.

NEMAR BIDS `type` is not used to infer modality because it incorrectly classifies the inspected physiological channels as EEG and reports zero EOG/EMG counts. Actual labels plus source documentation are used instead.

## 7. ISRUC Primary Channel Contract

PRIMARY EEG: `C3-A2`

PRIMARY EOG: `LOC-A2`

fallback: none

required-channel behavior: if either exact label is absent, has an unexpected rate, or fails per-record integrity validation, quarantine/exclude the record from the exact-channel condition and record a structural mismatch. No silent substitution is allowed.

The selection is pre-experimental, centrally referenced, widely recognized in sleep PSG, available in representative S1 records, and compatible with a one-channel-per-modality benchmark. S2 session 2 uses an M1/M2 montage (`F3-M2`, `C3-M2`, etc.) and therefore is not silently included in the S1 exact-channel core.

## 8. ISRUC Scorer Contract

PRIMARY: scorer 1, represented by the NEMAR event stream derived from original scorer-1 Excel files.

SECONDARY: scorer 2, retained where available in NEMAR annotation extras.

disagreement policy: a valid scorer-1 epoch is not excluded because scorer 2 disagrees. Disagreement is preserved for secondary agreement, sensitivity, and uncertainty-vs-human-disagreement analyses. Consensus-only evaluation is secondary.

## 9. Sleep-EDF Primary Channel Contract

PRIMARY EEG: `EEG Fpz-Cz`

PRIMARY EOG: `EOG horizontal`

rationale: these labels are present in the official Sleep-EDF SC inventory, both are native 100 Hz, and the pair is a predeclared single-channel EEG/EOG representation without performance-based selection. `EEG Pz-Oz` remains available only for a separately declared sensitivity analysis; it is not a fallback.

Sleep-EDF, ISRUC, and SHHS do not have exact anatomical/electrode equivalence. The contract therefore uses modality-family harmonization with retained montage/reference domain shift rather than pretending that `EEG Fpz-Cz`, `C3-A2`, and `C3-A2` are identical acquisitions.

## 10. SHHS1 Intended Channel Contract

PRIMARY EEG: `C3-A2`

PRIMARY EOG: `EOG(L)-PG1`

nominal rates: EEG 125 Hz; EOG 50 Hz.

per-record validation requirement: every EDF header must be checked for exact channel labels, reference semantics, sampling rates, duration, and annotation alignment. Official SHHS documentation warns that individual studies may deviate from nominal settings. Missing exact channels or unexpected rates are structural mismatches; no silent fallback is allowed.

## 11. SHHS Raw Access State

RAW_ACCESS_PENDING

The public schema/documentation is available, but local inspection found no NSRR/SHHS access variables and no local SHHS raw files. User action is required: visit the official NSRR/SleepData resource, create/sign in to an account, review current terms, and request/enable access through the official interface. No credentials or acceptance were requested, automated, stored, or exposed.

Required project description and eventual files are recorded in `docs/shhs_access_plan.md`.

## 12. Accessible Core

* Sleep-EDF SC: official open-access recording files, subject/night identity grouped by filename subject token, exact `EEG Fpz-Cz` and `EOG horizontal`.
* ISRUC-S1: 100 one-recording-per-subject cohort, NEMAR metadata/representative evidence, exact `C3-A2` and `LOC-A2`, scorer-1 primary events, scorer-2 secondary extras.

## 13. Planned Final Primary Benchmark

* Sleep-EDF SC — accessible and core-frozen.
* ISRUC-S1 — accessible and core-frozen.
* SHHS1 — intended third primary domain, pending authorized raw/XML access and per-record validation.

The three-domain paper goal is retained. No two-domain result is to be described as the final benchmark.

## 14. Label/Exclusion Correction

Canonical labels are Wake, N1, N2, N3, and REM. R&K stages 3 and 4 map to N3.

Exact primary exclusion list:

* Movement Time/non-stage event;
* unknown or `?` stage;
* unscored stage;
* explicit invalid artifact annotation;
* corrupt annotation;
* incomplete 30-second epoch;
* epoch without matching signal samples;
* irreconcilable annotation/signal alignment.

Do not exclude valid Wake, difficult transitions, or valid scorer-1 epochs merely because scorer 2 disagrees. Scorer disagreement is not a primary exclusion.

## 15. Human-Disagreement Diagnostic Plan

For ISRUC epochs with both scorers, a future secondary diagnostic will report:

* overall agreement rate;
* Cohen’s kappa;
* stage-specific disagreement;
* model confidence on agreement versus disagreement epochs;
* model error on agreement versus disagreement epochs.

No statistics or model outputs were computed in Step 5.1. The purpose is to preserve clinically and annotationally difficult epochs rather than deleting them.

## 16. Sampling Contract

Target rates are:

* EEG: 100 Hz;
* EOG: 50 Hz.

This is defensible because Sleep-EDF is native 100/100 Hz, ISRUC is native 200/200 Hz and requires only future downsampling, and SHHS1 is nominally 125/50 Hz and requires no EOG upsampling. The policy avoids EEG upsampling, avoids EOG upsampling, uses modality-specific input lengths, and preserves a fixed rate contract.

No resampling occurred. Step 6 must specify deterministic anti-aliasing before downsampling and validate every record’s actual native rate.

## 17. Shift Conditions

* C0: known domain, EEG+EOG;
* C1: known domain, EEG only through synthetic EOG loss;
* C2: known domain, EOG only through synthetic EEG loss;
* C3: unseen domain, EEG+EOG;
* C4: unseen domain, EEG only through synthetic EOG loss;
* C5: unseen domain, EOG only through synthetic EEG loss.

Synthetic missingness is valid only when the removed raw modality actually exists. No condition removes both primary modalities. Structural channel absence, unexpected native rate, corrupt required channel, and incompatible representation are separate structural conditions and are not assigned C1/C2/C4/C5 identifiers.

## 18. Dataset Roles

PRIMARY ACCESSIBLE CORE:

* Sleep-EDF SC;
* ISRUC-S1.

PLANNED PRIMARY:

* SHHS1 pending authorized raw/XML access and per-record schema validation.

SECONDARY:

* Sleep-EDF ST;
* ISRUC-S2;
* ISRUC-S3.

S2/S3 are not silently treated as the S1 exact-channel core; S2 session 2 demonstrates a distinct M1/M2 montage.

EXTERNAL:

* CAP Sleep Database, as an external pathology/device/schema stress domain pending identity and full-schema closure.

## 19. Core vs Final Freeze Semantics

`CORE_PREPROCESSING_FROZEN` authorizes implementation of a deterministic, contract-driven preprocessing and integrity pipeline for Sleep-EDF SC plus ISRUC-S1. It does not authorize execution in this step, model training, final splits, or results.

`FINAL_BENCHMARK_FROZEN` requires every intended primary domain, including SHHS1, to be legitimately acquired and per-record schema validated. It remains `NO`. Core engineering must not freeze models or claims before SHHS1 is incorporated, and future SHHS inclusion must not require changing the canonical modality, label, missingness, or target-free contract.

## 20. Machine-Readable Contract

version: `1.1.0`

file: `configs/data_contract_v1.yaml`

status: `CORE_PREPROCESSING_FROZEN`; `final_benchmark_frozen: false`.

hash: SHA-256 values for the machine-readable and human-readable contract are recorded in `reports/contract_hashes.txt`.

validation: contract loader/validator passed; it checks version, core datasets, exact ISRUC/Sleep-EDF channels, scorer-1 policy, non-exclusion of disagreement, SHHS pending state, freeze-level distinction, target rates, missingness, structural separation, target-free rules, and raw immutability.

## 21. Protocol Amendments

* `A-05.1-01`: freeze ISRUC-S1 `C3-A2` and `LOC-A2`.
* `A-05.1-02`: freeze ISRUC scorer 1 primary and scorer 2 secondary.
* `A-05.1-03`: remove scorer disagreement from primary exclusions.
* `A-05.1-04`: distinguish core preprocessing freeze from final benchmark freeze.
* `A-05.1-05`: freeze intended SHHS1 schema while retaining pending access.
* `A-05.1-06`: explicitly harmonize modality families while retaining montage/reference domain shift.

Full amendment text and evidence are in `docs/protocol_amendments.md`.

## 22. Tests

Added and passed tests for:

1. ISRUC primary EEG/EOG existence;
2. explicit ISRUC scorer policy;
3. disagreement not being an automatic primary exclusion;
4. accessible-core subject grouping;
5. exact accessible-core channels;
6. EEG 100/EOG 50 targets;
7. SHHS pending-access state;
8. distinct core/final freeze levels;
9. target-free prohibitions;
10. C0–C5 missingness states;
11. structural mismatch separation.

## 23. Validation

* `pytest -q`: `12 passed in 0.24s`.
* `python -m compileall -q src tests scripts`: exit `0`.
* `git diff --check`: exit `0`.
* contract validation: `PYTHONPATH=src python` loaded `1.1.0 CORE_PREPROCESSING_FROZEN False` and listed the six explicit dataset roles.
* forbidden-artifact scan: no private-key, API-key, password, token, or credential-pattern matches; no raw SHHS download; no credentials retained.

## 24. Files Created

* `reports/STEP_05_1_CORE_CONTRACT_REPORT.md`;
* `reports/isruc_channel_contract.csv`.

## 25. Files Modified

* `configs/data_contract_v1.yaml`;
* `docs/harmonization_contract_v1.md`;
* `docs/protocol_amendments.md`;
* `docs/shhs_access_plan.md`;
* `docs/benchmark_spec.md`;
* `docs/dataset_registry.md`;
* `src/shiftsleep_uq/data/contracts.py`;
* `tests/test_contracts.py`.

## 26. Explicitly Not Done

* no model;
* no training;
* no final preprocessing;
* no resampling;
* no normalization;
* no epoch tensors;
* no final splits;
* no experimental metrics;
* no target calibration;
* no unauthorized SHHS download;
* no raw PSG committed;
* no repository push.

## 27. Remaining Blockers for FINAL Benchmark

These do not block accessible-core preprocessing engineering:

1. authorized SHHS1 NSRR raw/XML access;
2. SHHS1 EDF/XML acquisition under current data-use terms;
3. SHHS1 per-record exact-channel, rate, duration, and annotation validation;
4. SHHS1 primary XML stream selection after authorized audit;
5. any final deterministic SHHS1 subset/scale policy;
6. ISRUC-S2/S3 secondary exact-channel contracts if those cohorts are used;
7. CAP subject identity and complete schema if CAP is retained as a quantitative external stress domain.

The final three-domain benchmark remains incomplete until item 1–4 are closed.

## 28. Recommended Next Step

Implement a deterministic, contract-driven preprocessing and integrity pipeline for Sleep-EDF SC + ISRUC-S1 only, with no model work, no final scientific claims, and no SHHS access bypass. Before final benchmark claims, complete the authorized SHHS1 access and per-record schema audit.

Do not execute that implementation in Step 5.1.

## 29. Git Status / Diff Summary

Step 5.1 was validated before commit. The local commit was created with message `research: freeze accessible PSG core contract`; no GitHub push was performed. The final working tree was verified clean.

The change set contains the 1.1.0 machine-readable contract, validator/tests, ISRUC channel evidence manifest, human-readable contract revision, scorer/disagreement amendment, SHHS human-action access plan, benchmark/registry updates, and this report. It contains no signal bodies, models, preprocessing outputs, final splits, metrics, credentials, or unauthorized SHHS data.

Exact Step 5.1 report path: `C:\Users\rohan\ShiftSleep-UQ\reports\STEP_05_1_CORE_CONTRACT_REPORT.md`
