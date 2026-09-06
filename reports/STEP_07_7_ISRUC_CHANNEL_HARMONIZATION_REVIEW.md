# ShiftSleep-UQ Step 7.7 ISRUC Channel Harmonization Review

## 1. Status

`COMPLETE`

Step 7.7 was completed as a protocol and contract decision using the existing 35 complete, body-valid original-provider ISRUC-S1 recordings and authoritative source/standards evidence. No new acquisition, preprocessing, modeling, splitting, or model-based evaluation was performed.

## 2. Channel Policy Decision

`ADOPT_SOURCE_SUPPORTED_CHANNEL_FAMILY`

The exact source-supported ISRUC family contract is adopted:

- EEG role: `LEFT_CENTRAL_EEG`
  - exact `C3-A2`
  - exact `C3-M2`
- EOG role: `LEFT_OCULAR_EOG`
  - exact `LOC-A2`
  - exact `E1-M2`

This is not alias replacement. `C3-M2` is never renamed `C3-A2`, and `E1-M2` is never renamed `LOC-A2`. Exact source derivations remain mandatory metadata. No re-referencing, numerical-equivalence claim, lowercasing, case-insensitive matching, regex matching, or fuzzy substitution is permitted.

## 3. Repository State

Repository: `C:\Users\rohan\ShiftSleep-UQ`

- Branch at preflight: `main`
- Step 7.6 report exists and was committed before this review:
  `reports/STEP_07_6_ISRUC_CHANNEL_SCHEMA_AUDIT_REPORT.md`
- Step 7.6 commit subject: `research: audit ISRUC original channel schema`
- Preflight working tree: clean
- Current data contract before amendment: `1.1.0`
- Current preprocessing version before amendment: `0.1.0`
- Pre-amendment data-contract SHA-256: `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9`
- Preprocessing SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`
- I036 partial `.getxfer` state was inspected and left untouched.
- I037–I100 were not acquired.
- No raw or processed data were modified.

The final repository state is recorded in Section 30 after validation and commit.

## 4. Trigger

Step 7.6 established from independent raw EDF/REC fixed-header parsing, pyEDFlib, and the project parser that the 18 exclusions were genuine source-header montage variation rather than parser, encoding, whitespace, header-index, body-size, or cohort-identification defects.

Among the 35 complete, body-valid original-provider recordings:

- 17/35 use exact A1/A2-style required derivations:
  - EEG `C3-A2`
  - EOG `LOC-A2`
- 18/35 use exact M1/M2-style source derivations:
  - EEG `C3-M2`
  - EOG `E1-M2`
  - companion EOG `E2-M1`

The Step 7.6 audit found the variants interspersed rather than representing one trivial subject-number cutoff. This review therefore treated the source derivations as a scientific acquisition-contract question and did not repeat parser debugging.

## 5. Evidence Reviewed

### 5.1 Primary technical/standards evidence

1. **AAST Standard Polysomnography Technical Guideline, updated December 2021**, pp. 4–5, which explicitly states that its technical specifications follow the AASM Manual for the Scoring of Sleep and Associated Events, version 2.6. The guideline identifies:
   - a central EEG channel referenced to an ear/mastoid site;
   - `C3-M2` as a recommended redundant central EEG derivation;
   - E1/E2 positions as 1 cm lateral and above/below the outer canthi;
   - M2 as the usual EOG reference and M1 as a fallback if M2 fails.
   - URL: `https://aastweb.org/wp-content/uploads/2025/03/AAST-PSG-Guideline-Final.pdf`

2. **Khalighi et al., “ISRUC-Sleep: A comprehensive public dataset for sleep researchers,” Computer Methods and Programs in Biomedicine 124 (2016), 180–192, PMID 26589468.** This is the original ISRUC-Sleep dataset publication and supports the dataset’s PSG/source-schema provenance.
   - URL: `https://pubmed.ncbi.nlm.nih.gov/26589468/`

3. **Peer-reviewed ISRUC sleep-staging description**, which describes ISRUC Subgroup 1 as the 100-subject group with nominal EEG/EOG/EMG channels and 200 Hz recording. It supports the nominal A1/A2-style schema but does not establish that every raw provider export has identical derivation strings.
   - URL: `https://pmc.ncbi.nlm.nih.gov/articles/PMC8946692/`

### 5.2 Repository and acquisition evidence

4. `docs/isruc_channel_schema_evidence.md`, which records the nominal-versus-observed ISRUC distinction and source documentation reviewed during Step 7.6.

5. `reports/isruc_original_channel_inventory_35_diagnostic.csv`, which records the independently parsed channel inventory for I001–I035.

6. `reports/isruc_channel_schema_clusters.csv`, which records heterogeneous observed schema clusters.

7. `reports/isruc_channel_parser_crosscheck.csv`, `reports/isruc_three_way_channel_parser_audit.csv`, and `reports/isruc_channel_header_side_by_side.csv`, which cross-check project parsing against independent raw-header evidence.

8. `reports/STEP_07_6_ISRUC_CHANNEL_SCHEMA_AUDIT_REPORT.md`, which records the complete Step 7.6 root-cause audit.

### 5.3 Library corroboration

9. TorchEEG ISRUC documentation was used only as established-library corroboration for dataset organization, nominal channels, and observed representation variation:
   - URL: `https://torcheeg.readthedocs.io/en/stable/generated/torcheeg.datasets.ISRUCDataset.html`

Evidence strength is **strong for shared physiological acquisition roles and distinct conventional derivations**, but not for exact electrode identity or numerical signal equality.

## 6. EEG Semantics

### 6.1 `C3-A2`

`C3` denotes the left-central scalp active site in the International 10–20 electrode nomenclature. `A2` is an ear/mastoid-family reference label used in the nominal ISRUC derivation. The derivation is a conventional central sleep EEG channel.

### 6.2 `C3-M2`

`C3` remains the left-central scalp active site. `M2` denotes the right mastoid reference convention used in standard PSG nomenclature. The AAST technical guideline explicitly lists `C3-M2` as a recommended central EEG derivation for sleep PSG.

### 6.3 Relationship

The two derivations share the same broad central EEG active-site role and are both conventional sleep EEG derivations. Their reference labels are not interchangeable evidence of identical physical electrode placement in every source export. Reference choice changes the recorded voltage relationship; the derivations must therefore remain distinct.

Conclusion: `C3-A2` and `C3-M2` are `SAME_ROLE_DISTINCT_DERIVATION`. The evidence supports coexistence as explicitly tracked source variants, not renaming or numerical identity.

## 7. EOG Semantics

### 7.1 `LOC-A2`

`LOC` is the ISRUC nominal naming convention for the left outer-canthus ocular electrode. The ISRUC nominal schema records `LOC-A2` as the left EOG derivation. `A2` is the nominal ear/mastoid-family reference label.

### 7.2 `E1-M2`

AASM/PSG terminology identifies E1 as the EOG electrode positioned 1 cm lateral and below the outer canthus, with E2 positioned 1 cm lateral and above the outer canthus. The AAST guideline identifies M2 as the usual reference for both EOG electrodes. Thus `E1-M2` is a conventional left-ocular EOG derivation with a standard PSG reference convention.

### 7.3 Relationship

`LOC-A2` and `E1-M2` support the same broad left-ocular sleep-EOG role: they measure an ocular potential from the left outer-canthus region relative to an ear/mastoid-family reference. However, `LOC` and `E1` are not asserted to be literal identical electrode placements, and `A2` and `M2` are not asserted to be the same physical reference in every ISRUC export.

The observed `E2-M1` companion channel supports the interpretation that the M1/M2 recordings are a coherent EOG montage family rather than an isolated label corruption. It is contextual montage evidence only and is not accepted as a replacement for the required left-ocular role.

Conclusion: `LOC-A2` and `E1-M2` are `SAME_ROLE_DISTINCT_DERIVATION`.

## 8. Numeric Equivalence

`NOT CLAIMED`

No literal numerical equivalence is claimed between `C3-A2` and `C3-M2`, or between `LOC-A2` and `E1-M2`. A reference change can alter amplitude, polarity, common-mode behavior, artifact expression, and frequency-domain representation. The decision rests on defensible physiological acquisition role, not signal equality.

No amplitude summary was used as an equivalence test and no signal transformation was performed.

## 9. Relation to ShiftSleep-UQ Thesis

Within-ISRUC montage variation is a legitimate recording-system/acquisition nuisance variable for the ShiftSleep-UQ question, provided that it is observable, auditable, and never silently collapsed.

The project studies reliability under unseen populations and recording-system/domain shift. Excluding an interspersed source-supported montage family solely because its reference nomenclature differs would create a selection mechanism correlated with acquisition configuration. That would reduce cohort representativeness and remove a real source of acquisition shift from the benchmark. Conversely, pooling the families without metadata would conceal a plausible reliability-relevant nuisance variable.

Policy B addresses both requirements:

- it preserves exact raw derivation identities;
- it records montage family as mandatory metadata;
- it does not re-reference or numerically equate signals;
- it requires montage-stratified future sensitivity analyses;
- it treats montage as an acquisition stratum, not a C0–C5 missing-modality condition.

The variant remains a potential confound if not reported. It is therefore a controlled nuisance stratum, not an assumption of harmlessness.

## 10. Policy A Assessment

### `EXACT_A1_A2_ONLY`

Scientific cleanliness: high with respect to one nominal derivation family. This policy would minimize within-ISRUC reference heterogeneity in the primary selected subset.

Selection-bias risk: material. Step 7.6 found the 18 M1/M2 recordings interspersed rather than a simple corrupt batch. Exact-only eligibility would select 17/35 of the audited recordings and exclude 18/35 on source-reference nomenclature. The resulting selected population would be conditional on acquisition configuration.

Cohort representativeness: weakened. The nominal 100-subject ISRUC-S1 target would no longer represent all source-supported recordings admitted by the provider schema.

Relationship to the thesis: incomplete. The policy removes a real within-dataset recording-system variation from a study explicitly concerned with domain and recording-system shift.

Policy A remains defensible only if the scientific estimand is explicitly restricted to the A1/A2 source family. That is not the broader ShiftSleep-UQ reliability estimand adopted here.

## 11. Policy B Assessment

### `SOURCE_SUPPORTED_CHANNEL_FAMILY`

Scientific defensibility: supported for coexistence by the evidence reviewed. Both pairs are conventional PSG derivations with aligned broad physiological roles: left-central EEG and left-ocular EOG.

Identity discipline: preserved. Exact source labels are retained and cannot be replaced by aliases. The machine-readable contract accepts only two exact pairings:

- `C3-A2` + `LOC-A2` → `ISRUC_A1A2`
- `C3-M2` + `E1-M2` → `ISRUC_M1M2`

Confounding control: explicit. `montage_variant`, exact source EEG derivation, exact source EOG derivation, and anatomical role fields are mandatory metadata. Future reliability outputs must be reported by montage family.

Limit: this policy does not establish numerical equivalence, identical electrode placement, or identical noise/artifact distributions. It only establishes sufficient role alignment for coexistence under preserved derivation identity.

Policy B is selected because it matches the thesis without silently erasing acquisition heterogeneity.

## 12. Policy C Assessment

### `ISRUC_PRIMARY_ROLE_REVIEW`

Policy C is not required by the evidence. The source-supported EEG and EOG family roles are defensible, the exact derivations are auditable, and the observed variation can be represented as an explicit nuisance stratum. ISRUC does not need to be removed from the primary accessible role solely because its provider exports contain these two legitimate montage families.

Policy C would become appropriate only if later protocol review or stratum-specific validation showed that the family roles are not scientifically compatible for the declared estimand. No such model or outcome evidence was generated in Step 7.7.

## 13. Existing-35 Eligibility Projection

This is a metadata-only dry run. No newly admissible recording was preprocessed.

| Policy / family | Eligible subjects | Excluded / incompatible subjects |
|---|---:|---:|
| Policy A: exact `C3-A2` + `LOC-A2` | 17 | 18 |
| Policy B: A1/A2 family | 17 | — |
| Policy B: M1/M2 family | 18 | — |
| Policy B: family-compatible total | 35 | 0 |

Policy A excluded subject IDs: `I011, I013, I014, I017, I019, I020, I021, I023, I025, I027, I028, I029, I030, I031, I032, I033, I034, I035`.

The Policy B total is `35/35` because every audited recording belongs to one of the two exact accepted source pairings. This retention result is a consequence of the evidence-based allowlist, not the selection criterion for the decision.

## 14. Selection / Confounding Risk

Exact-only selection creates a substantial acquisition-conditioned selection risk in the currently observed population: 18 of 35 recordings would be excluded based on the reference/montage family despite being body-valid and source-supported PSG recordings.

Family adoption does not eliminate confounding. It makes the acquisition factor visible and reportable. The mandatory mitigation is:

1. retain exact source derivations;
2. record `ISRUC_A1A2` versus `ISRUC_M1M2`;
3. do not silently re-reference;
4. predeclare montage-stratified sensitivity analyses;
5. report stratum-specific predictive performance, calibration, and selective risk/AURC before any pooled interpretation.

No cohort, subject, stage, or model outcome was used to optimize this policy.

## 15. Descriptive Scale Check

Not executed.

The optional robust amplitude summaries were intentionally omitted. They were not needed to establish the source/standards-based role relationship, and amplitude similarity would not prove electrode or numerical equivalence. No normalization, exclusion threshold, amplitude-based selection, or signal comparison was performed.

## 16. Final Rationale

The decision is `ADOPT_SOURCE_SUPPORTED_CHANNEL_FAMILY`.

The decisive evidence is that:

- `C3-A2` and `C3-M2` share the left-central EEG acquisition role, and `C3-M2` is explicitly a conventional PSG central derivation;
- `LOC-A2` and `E1-M2` support the left-ocular EOG acquisition role, and E1/M2 is explicitly a conventional PSG EOG derivation;
- the raw exports contain coherent exact source montages rather than parser artifacts;
- exact physical placement and numerical equality cannot be claimed;
- exact identities and family membership can be retained in metadata;
- montage can be treated as a visible nuisance/acquisition stratum aligned with the ShiftSleep-UQ domain-shift thesis.

Policy B is therefore scientifically defensible without maximizing retention as its premise.

## 17. Scientific Contract Amendment

### A-07.7-01 — ISRUC Source-Supported Montage-Family Harmonization

**Discovered:** before modeling; no performance results existed.

**Decision basis:** source headers, ISRUC documentation/publication evidence, and sleep-PSG technical standards only.

**OLD**

- ISRUC primary EEG: exact `C3-A2`
- ISRUC primary EOG: exact `LOC-A2`
- M1/M2 records: structurally excluded

**NEW**

- ISRUC EEG role: `LEFT_CENTRAL_EEG`
  - accepted exact derivations: `C3-A2`, `C3-M2`
- ISRUC EOG role: `LEFT_OCULAR_EOG`
  - accepted exact derivations: `LOC-A2`, `E1-M2`

**Preservation rules**

- exact raw derivation retained;
- no source-label renaming;
- no alias replacement;
- no mathematical re-reference;
- no claim of signal equality or numerical equivalence;
- no fuzzy, case-insensitive, or regex matching;
- montage variant tracked as mandatory acquisition metadata;
- montage-stratified reliability sensitivity analysis mandatory.

**Unchanged:** canonical sleep labels, scorer-1 primary policy, 30-second epochs, EEG target 100 Hz, EOG target 50 Hz, microvolt policy, resampling implementation, normalization prohibition, C0–C5 missing-modality semantics, and target-free protocol.

## 18. Contract Version and Hashes

The machine-readable contract was bumped from `1.1.0` to `1.2.0`.

| Artifact | Version/state | SHA-256 |
|---|---|---|
| `configs/data_contract_v1.yaml` before Step 7.7 | `1.1.0` | `a9b05b22697fe8ba5cb3f03a6e35cca2fcbdb55971d6e565a7dc9b36ab68a0f9` |
| `configs/data_contract_v1.yaml` after Step 7.7 | `1.2.0` | `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036` |
| `configs/preprocessing_v1.yaml` | unchanged `0.1.0` | `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794` |
| `docs/harmonization_contract_v1_2.md` | new human contract | `c00e96525cb33903c8807a53b2b9d7d52d7ca0a6b90ec4cf245a730cbb633bd3` |

The old `docs/harmonization_contract_v1.md` remains historical. The new human contract is `docs/harmonization_contract_v1_2.md`.

## 19. Machine-Readable Montage Contract

The ISRUC section of `configs/data_contract_v1.yaml` now encodes:

- exact EEG derivation allowlist: `C3-A2`, `C3-M2`;
- exact EOG derivation allowlist: `LOC-A2`, `E1-M2`;
- exact accepted pairs and variants:
  - `C3-A2` + `LOC-A2` → `ISRUC_A1A2`;
  - `C3-M2` + `E1-M2` → `ISRUC_M1M2`;
- role names `LEFT_CENTRAL_EEG` and `LEFT_OCULAR_EOG`;
- mandatory source-derivation and montage metadata;
- no-fallback policy;
- exact-identity/no-referencing policy;
- required future sensitivity strata.

`src/shiftsleep_uq/data/montage_contract.py` implements the same exact two-pair allowlist for contract-level validation. It rejects lowercase/fuzzy strings, mixed references, `C4-M1`, `ROC-A1`, and unknown combinations.

## 20. Montage Metadata

For every accepted ISRUC recording, the contract requires:

- `source_eeg_derivation`
- `source_eog_derivation`
- `eeg_anatomical_role`
- `eog_anatomical_role`
- `montage_variant`

Recommended values are frozen as:

- A1/A2-style family: `ISRUC_A1A2`
- M1/M2-style family: `ISRUC_M1M2`

The metadata are descriptive provenance fields. They do not transform the signal.

## 21. Future Montage Sensitivity Requirement

Future ISRUC results must be reportable separately for:

- A1/A2 montage family: `ISRUC_A1A2`
- M1/M2 montage family: `ISRUC_M1M2`

This applies at minimum to:

- predictive performance;
- calibration;
- selective risk/AURC.

Any pooled result must be accompanied by stratum-specific estimates and a predeclared rationale. Montage is an acquisition nuisance stratum, not a new missing-modality condition and does not modify C0–C5.

No future metric was calculated here.

## 22. Target-Free Integrity

The decision used none of the following:

- model accuracy;
- validation performance;
- test performance;
- calibration;
- uncertainty estimates;
- stage-distribution optimization;
- target-domain fitting;
- normalization fitting;
- model selection;
- splits or held-out target data.

The decision was made before modeling from source/standards/acquisition evidence and existing metadata only.

## 23. Tests Added

Added `tests/test_isruc_montage_contract.py` with focused tests for:

1. exact `C3-A2` + `LOC-A2` acceptance;
2. exact `C3-M2` + `E1-M2` acceptance;
3. exact source derivations retained in returned metadata;
4. montage variant recording;
5. lowercase/fuzzy rejection;
6. rejection of `C4-M1` substitution;
7. rejection of `ROC-A1` substitution;
8. rejection of unknown/mixed combinations;
9. data-contract version and exact allowlist validation;
10. preservation of C0–C5 taxonomy;
11. target-free safeguards and unchanged target rates.

No giant testing subsystem was added.

## 24. Validation

Focused contract tests:

- `pytest -q tests/test_isruc_montage_contract.py` → `8 passed`

Final full validation was run after all Step 7.7 edits:

- `pytest -q` → `58 passed`
- `python -m compileall -q src tests scripts` → passed
- `git diff --check` → passed

Additional integrity checks:

- raw files are not tracked;
- processed files are not tracked;
- no credentials were added;
- preprocessing hash is unchanged;
- no acquisition process was started;
- no GitHub push was performed.

## 25. Files Created

- `reports/isruc_montage_harmonization_evidence.csv`
- `reports/STEP_07_7_ISRUC_CHANNEL_HARMONIZATION_REVIEW.md`
- `docs/harmonization_contract_v1_2.md`
- `src/shiftsleep_uq/data/montage_contract.py`
- `tests/test_isruc_montage_contract.py`

## 26. Files Modified

- `configs/data_contract_v1.yaml` — version `1.1.0` → `1.2.0`; exact source-family contract and metadata added.
- `docs/protocol_amendments.md` — amendment A-07.7-01 appended.
- `docs/decisions.md` — D008 decision record appended.
- `docs/evaluation_protocol.md` — montage-stratified reporting addendum added.
- `src/shiftsleep_uq/data/contracts.py` — contract loader/validator bumped to `1.2.0` and exact ISRUC allowlist validation added.
- `tests/test_contracts.py` — existing contract assertions updated for the amended version and source-family allowlist.

No source preprocessing implementation, raw data, processed arrays, manifests, provider files, scorer files, or acquisition state was modified.

## 27. Explicitly Not Done

Step 7.7 did not perform any of the following:

- no I036–I100 acquisition;
- no resumption of official provider transfer;
- no reprocessing of alternate-montage subjects;
- no rebuild of ISRUC manifests;
- no ISRUC cohort freeze;
- no split creation;
- no model installation;
- no model training;
- no normalization fitting;
- no ML metrics;
- no calibration;
- no uncertainty evaluation;
- no SHHS access;
- no raw data committed;
- no processed data committed;
- no credentials committed;
- no GitHub push.

## 28. ISRUC Migration Gate

The migration gate remains:

`ISRUC_ORIGINAL_COHORT_PARTIAL`

I001–I035 are complete and audited. I036 remains partial and untouched. I037–I100 remain unacquired. The policy amendment does not represent the ISRUC cohort as complete.

## 29. Recommended Next Step

Because `ADOPT_SOURCE_SUPPORTED_CHANNEL_FAMILY` was selected, the next protocol step is to resume I036–I100 acquisition only under the amended exact source-family contract, preserving exact derivation metadata and rejecting unsupported combinations. After acquisition, rebuild all 100 original-provider ISRUC subjects under the amended contract, validate each record, and freeze the ISRUC cohort before any split design.

This recommendation is not executed in Step 7.7.

## 30. Git Status / Diff Summary

The Step 7.7 artifacts and amendment were committed on `main` with subject:

`research: harmonize ISRUC source montage variants`

Final validation was run after the complete artifact set was present. The final working tree was clean after commit. No GitHub push occurred.

The final commit includes only the protocol decision, evidence table, contract amendment, exact contract validator, focused tests, and report. Raw `.rec`, `.txt`, `.xlsx`, transfer, provider, and processed-array files remain ignored and uncommitted. I036 remains untouched.

## Sources

- AAST. *Standard Polysomnography: AAST Technical Guideline*, updated December 2021. `https://aastweb.org/wp-content/uploads/2025/03/AAST-PSG-Guideline-Final.pdf`
- Khalighi et al. *ISRUC-Sleep: A comprehensive public dataset for sleep researchers*. PubMed PMID 26589468. `https://pubmed.ncbi.nlm.nih.gov/26589468/`
- Peer-reviewed ISRUC sleep-staging description, PMC8946692. `https://pmc.ncbi.nlm.nih.gov/articles/PMC8946692/`
- TorchEEG ISRUC dataset documentation. `https://torcheeg.readthedocs.io/en/stable/generated/torcheeg.datasets.ISRUCDataset.html`
- Local evidence record: `docs/isruc_channel_schema_evidence.md`
