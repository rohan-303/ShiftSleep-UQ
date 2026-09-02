# ISRUC Original-Provider Migration Plan

## Scope and status

This is a planning artifact only. It does not acquire subjects, migrate provider files, preprocess signals, rebuild the cohort, create splits, or alter the scientific contract.

Migration is not executed in Step 7.4. The plan becomes actionable only after explicit approval and a final pre-acquisition review.

## Expected population

- Dataset: ISRUC-Sleep Cohort I / ISRUC-S1.
- Expected recordings: 100 numbered subject folders, subject 1 through subject 100.
- Expected source route: official ISRUC public MEGA Cohort I folder.
- No unofficial mirrors or reconstructed file URLs.
- Selection must follow the frozen expected-population manifest, not stage composition, signal appearance, or model performance.

## Per-subject acquisition contract

For each numbered folder `N`, use the official MEGAcmd public-folder route and store only under:

`data/raw/isruc-original/subject-N/N/`

Expected source-style files are:

- `N.rec`
- `N_1.txt`
- `N_1.xlsx`
- `N_2.txt`
- `N_2.xlsx`

The folder must be listed before acquisition. Unexpected names must be retained and audited, not silently discarded. Existing NEMAR files must not be moved, replaced, or overwritten.

## Acquisition procedure

1. Freeze the expected 100-subject manifest and source identity.
2. Verify the public MEGA folder and client version.
3. Create each subject destination before invoking `get`.
4. Acquire one subject folder at a time with MEGAcmd.
5. Permit bounded retry/resume of the same remote folder only.
6. Write a per-file acquisition manifest containing subject, remote folder, filename, source identity, local path, bytes, SHA-256, timestamp, and status.
7. Treat a nonzero command result, missing file, partial file, or failed hash/body check as an explicit terminal exclusion—not as a valid acquisition.
8. Never log into a personal MEGA account for this public source.

## Validation gates per subject

Every subject must pass independent checks before it can enter the migrated cohort:

- all acquired files inventoried and SHA-256 hashed;
- REC/EDF header parsed;
- body-size formula passes exactly;
- required `C3-A2` and `LOC-A2` channels present;
- native primary rates and units verified;
- full source channel inventory retained;
- scorer-1 TXT/XLSX relationship validated;
- scorer-2 TXT/XLSX relationship validated;
- scorer-1 stage sequence audited;
- scorer-2 sequence audited as diagnostic provenance;
- original and derived-provider integrity status recorded where a NEMAR counterpart exists;
- no silent fallback channel, label, subject, or annotation substitution.

## Restart and resume policy

- Resume only the same subject folder and same destination after an interrupted transfer.
- Do not resume into a different subject directory.
- Do not treat an existing partial file as complete.
- Recompute byte count, SHA-256, and REC body integrity after every resumed transfer.
- Preserve failed attempts in the audit log without committing raw data.
- If the remote listing changes, stop and record the discrepancy for review.

## Storage estimate

The official Cohort I distribution is approximately 14.12 GB. This is the source-scale estimate; exact per-subject totals must be measured during acquisition.

- Minimum raw-source storage: approximately 14.12 GB.
- Operational raw-storage requirement: **NOT COMPUTED**; reserve additional temporary space for resumable transfers and verification copies according to the final acquisition environment.
- Expected processed storage: **NOT COMPUTED**; it depends on the finalized preprocessing output representation and must be measured from validated pilot subjects without changing the frozen contract.
- Do not begin acquisition unless available space is checked and sufficient headroom is reserved.

## Cohort rebuild after acquisition

Only after all 100 subjects have terminal acquisition and validation statuses:

1. Reconcile the acquisition manifest against the frozen 100-subject population.
2. Require exactly one terminal status and reason per expected subject.
3. Build a versioned original-provider cohort manifest.
4. Preprocess eligible subjects using the unchanged EEG/EOG channels, labels, units, epoch duration, target rates, and missingness semantics.
5. Run determinism, QC, attrition, provider-integrity, and accounting audits.
6. Compare the rebuilt original-provider cohort against the superseded NEMAR-derived cohort.
7. Record the final accessible-core decision before any split design.

## Provenance and Git policy

- Keep all `.rec`, `.edf`, raw `.txt`, raw `.xlsx`, processed signal arrays, and temporary archives outside Git tracking.
- Commit only manifests, hashes, lightweight audit tables, code, and reports.
- Never commit credentials, MEGA session material, private keys, or signed URLs.
- Do not push automatically.

## Scientific-contract guard

Migration is provenance repair only. It must not change:

- primary EEG `C3-A2`;
- primary EOG `LOC-A2`;
- scorer-1 primary status;
- scorer-2 diagnostic status;
- stage mapping;
- 30-second epoch duration;
- EEG/EOG target rates of 100/50 Hz;
- microvolt units;
- unnormalized/unstandardized outputs;
- missingness semantics;
- target-free protocol.

Any proposed contract change requires a separate protocol decision and must not be hidden inside acquisition or cohort rebuild work.
