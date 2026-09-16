# ShiftSleep-UQ Step 14 B1 Source Training Report

## 1. Status

`B1_SOURCE_TRAINING_COMPLETE`

Exactly six frozen B1 source-training runs completed. No calibration, source-test, target, prediction-bundle, or B0-vs-B1 evaluation was executed.

## 2. Training Gate

`B1_SOURCE_TRAINING_COMPLETE`

All six authorized runs completed with selected checkpoints, reloadable finite parameters/logits, zero forbidden masks, frozen normalization reuse, full-modality SOURCE DEV selection, and TRAIN/DEV-only signal access.

## 3. Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`;
- branch: `main`;
- preflight HEAD: `7226ad1`;
- Step 13 protocol gate: `B1_PROTOCOL_FROZEN`;
- historical lightweight-method gate: `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`.

The B0 and Step 13 protocol artifacts were clean and unchanged before training.

## 4. Frozen B1 Protocol Verification

Verified before training:

- B1 model config SHA-256: `b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6`;
- B1 training config SHA-256: `467ed74d465a65990388f4ac4f271311ccb156605cc1cfef1d4339057298bbc7`;
- B1 protocol SHA-256: `7db8bc63f21df1ea53fb58d881c8e4996651e57e1c8fd154283b1d273caa2c1c`;
- architecture: `B0_DUAL_BRANCH_RAW_CNN`;
- architecture change: `NONE`;
- expected trainable parameters: `654597`.

## 5. Environment

- OS: Windows-10-10.0.26200-SP0;
- Python: 3.11.15;
- PyTorch: 2.14.0+cu126;
- NumPy: 2.4.3;
- CUDA available: `True`;
- CUDA runtime: `12.6`;
- cuDNN: `91002`;
- GPU: `NVIDIA GeForce RTX 3060 Laptop GPU`;
- total GPU memory: approximately `6,441,926,656` bytes;
- device used: `cuda:0`;
- precision: FP32.

The environment was not upgraded or altered.

## 6. Architecture Integrity

Every run instantiated the existing `BaselineB0` implementation directly. No B1 architecture copy or alternate model file was created. The expected architecture identity and class order were recorded in checkpoints and manifests.

## 7. Normalization Reuse

No normalization fitting occurred. All runs reused the exact direction-level B0 objects:

- D1: `artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json` — `be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3`;
- D2: `artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json` — `3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e`.

Each run contains a normalization reference rather than a new normalization artifact.

## 8. Data Access Firewall

The deduplicated audit contains 191 allowed rows. Observed signal roles/purposes were exactly:

- `TRAIN` / `train`;
- `DEV` / `dev`.

Observed datasets were exactly `sleep_edf_sc` and `isruc_s1`. No CALIBRATION, TEST, TARGET, ORACLE, or SHHS signal access occurred.

Audit artifact:

`reports/step14_data_access_audit.csv`

SHA-256: `8631c02cac40b08c33f160db4d603a0f44814c8f91d2cf522564b347fdf12882`

## 9. Training Exposure Policy

The frozen mask policy was used for every SOURCE TRAIN example:

- FULL `[1,1]`: probability 0.50;
- EEG-only `[1,0]`: probability 0.25;
- EOG-only `[0,1]`: probability 0.25;
- `[0,0]`: forbidden.

The exposure seed was `2029`. No rebalancing or probability changes were made.

## 10. Mask Epoch Convention

The runner used the frozen `1_BASED` convention: training epoch numbers passed to the mask generator were `1..N`. The canonical key was the Step 13 frozen serialization of exposure seed, epoch, dataset, subject ID, recording ID, and epoch index. No zero-based/one-based shift occurred during a run.

## 11. D1 Source Population

D1 source dataset: `sleep_edf_sc`.

- SOURCE TRAIN: 47 subjects, 93 recordings, 252,742 epochs;
- SOURCE DEV: 12 subjects, 24 recordings, 65,042 epochs.

Only these D1 populations were loaded.

## 12. D2 Source Population

D2 source dataset: `isruc_s1`.

- SOURCE TRAIN: 59 subjects, 59 recordings, 53,037 epochs;
- SOURCE DEV: 15 subjects, 15 recordings, 13,785 epochs.

Only these D2 populations were loaded.

## 13. Frozen Training Recipe

All six runs used:

- AdamW;
- learning rate `3e-4`;
- weight decay `1e-4`;
- betas `(0.9, 0.999)`;
- epsilon `1e-8`;
- batch size `128`;
- FP32;
- global gradient clipping `1.0`;
- no scheduler;
- maximum 30 epochs;
- minimum 5 epochs;
- early-stopping patience 6;
- unweighted `CrossEntropyLoss(weight=None, label_smoothing=0.0)`;
- natural epoch-level sampling;
- no additional augmentation;
- no class, subject, montage, recording, or modality balancing.

## 14. D1 Seed 17

- selected epoch: `12`;
- epochs executed: `18`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.7557365298271179`;
- full-modality SOURCE DEV NLL: `0.30334229759745146`;
- FULL exposures: `2,273,949`;
- EEG-only exposures: `1,138,903`;
- EOG-only exposures: `1,136,504`;
- forbidden exposures: `0`;
- FULL fraction: `0.49983975753930887`;
- EEG-only fraction: `0.2503437849225253`;
- EOG-only fraction: `0.24981645753816584`;
- checkpoint SHA-256: `7a006909e9f5cfc29b004a1af5d8536f218265e292b63db904dd09a0ff9fc1a5`;
- training duration: `2007.9888875999986` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 15. D1 Seed 42

- selected epoch: `5`;
- epochs executed: `11`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.7478377819061279`;
- full-modality SOURCE DEV NLL: `0.24423308977189614`;
- FULL exposures: `1,389,785`;
- EEG-only exposures: `696,425`;
- EOG-only exposures: `693,952`;
- forbidden exposures: `0`;
- FULL fraction: `0.4998935313841424`;
- EEG-only fraction: `0.2504979925630233`;
- EOG-only fraction: `0.24960847605283434`;
- checkpoint SHA-256: `b0e5e0989e60b8ba5194ad80a3fc60f5cd87c37c9c7ce20c535783524ed8c5b7`;
- training duration: `1171.3892233000006` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 16. D1 Seed 2026

- selected epoch: `4`;
- epochs executed: `10`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.745132565498352`;
- full-modality SOURCE DEV NLL: `0.2782683274560051`;
- FULL exposures: `1,263,226`;
- EEG-only exposures: `633,009`;
- EOG-only exposures: `631,185`;
- forbidden exposures: `0`;
- FULL fraction: `0.49980850036796415`;
- EEG-only fraction: `0.2504565920978706`;
- EOG-only fraction: `0.24973490753416527`;
- checkpoint SHA-256: `23ea8b05dac65a10f29f5caf305b203ee381415521ddc8af5665dcff686b967f`;
- training duration: `1226.3073922000003` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 17. D2 Seed 17

- selected epoch: `9`;
- epochs executed: `15`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.7523154020309448`;
- full-modality SOURCE DEV NLL: `0.5884060568857559`;
- FULL exposures: `397,770`;
- EEG-only exposures: `198,943`;
- EOG-only exposures: `198,842`;
- forbidden exposures: `0`;
- FULL fraction: `0.49999057261911495`;
- EEG-only fraction: `0.2500681913884018`;
- EOG-only fraction: `0.24994123599248325`;
- checkpoint SHA-256: `3b91624e571259cb0e85cbde6290e11c1211323b38995bcf66f5dbd12088d5ec`;
- training duration: `328.12888810000004` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 18. D2 Seed 42

- selected epoch: `11`;
- epochs executed: `17`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.7582172155380249`;
- full-modality SOURCE DEV NLL: `0.6049228675297968`;
- FULL exposures: `450,824`;
- EEG-only exposures: `225,209`;
- EOG-only exposures: `225,596`;
- forbidden exposures: `0`;
- FULL fraction: `0.5000105364845185`;
- EEG-only fraction: `0.2497801202046518`;
- EOG-only fraction: `0.2502093433108296`;
- checkpoint SHA-256: `b5bdd41c9dbf2e71af44a479843babc7448c8a4f45fc9445cc2c507755899d36`;
- training duration: `383.88884340000004` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 19. D2 Seed 2026

- selected epoch: `10`;
- epochs executed: `16`;
- stop reason: `EARLY_STOPPING`;
- full-modality SOURCE DEV macro-F1: `0.752487301826477`;
- full-modality SOURCE DEV NLL: `0.5894312817200689`;
- FULL exposures: `424,139`;
- EEG-only exposures: `212,147`;
- EOG-only exposures: `212,306`;
- forbidden exposures: `0`;
- FULL fraction: `0.49981498765013105`;
- EEG-only fraction: `0.24999882157738937`;
- EOG-only fraction: `0.2501861907724796`;
- checkpoint SHA-256: `1ba7ae76f67c1a8f549b0026eca7b00f60402f9988809c42c6bc6cf14b60ca30`;
- training duration: `367.7820948000008` seconds.

The DEV values are checkpoint-selection diagnostics, not B1-vs-B0 scientific results.

## 20. Six-Run Training Summary

`reports/b1_training_summary_v1.csv` contains exactly six rows, one for each authorized direction × seed run.

SHA-256: `3b75ed17e005596b8b2297d18734d349a287acf19a9b16678e768730316f38d8`

All six rows have status `COMPLETE` and zero forbidden exposures.

## 21. Modality Exposure Summary

`reports/b1_modality_exposure_summary_v1.csv` contains exactly six run-summary rows.

SHA-256: `d25e80bb471cefbfb081c350008942c385493d38d66371f043249b8a7ac8d71f`

Realized finite-run fractions remained close to the policy probabilities. No exposure rebalancing was performed. The six cumulative forbidden counts are all zero.

## 22. Exposure Determinism / Integrity

The Step 13 SHA-256 mask implementation was used unchanged. Epoch numbering was explicitly 1-based. Every run recorded cumulative FULL, EEG-only, EOG-only, total, and forbidden counts. For every run:

`total_exposures = full_count + eeg_only_count + eog_only_count`

and:

`forbidden_count = 0`.

## 23. Checkpoint Selection Integrity

Checkpoint selection used only full-modality SOURCE DEV macro-F1 and NLL under mask `[1,1]`, with the frozen tolerance, tie-breaks, patience, minimum epoch, and maximum epoch rules. No missing-modality DEV metrics were computed or logged. No TEST/TARGET metric was used.

## 24. Checkpoint Integrity

All six selected checkpoints were reloaded into fresh `BaselineB0` instances. Every state dict was compatible, every model had `654597` trainable parameters, parameters were finite, class order was preserved, normalization metadata matched the direction, exposure metadata was present, and full-modality SOURCE DEV smoke logits were finite.

## 25. Checkpoint Hash Manifest

`reports/b1_checkpoint_hashes_v1.txt` contains exactly six checkpoint entries.

SHA-256: `690a5811e9cff075a49797e624a65a7d12f4cfc30f1d46b884957e6829101160`

All six on-disk checkpoint hashes reproduce the manifest values. Checkpoint binaries remain outside the committed artifact set.

## 26. Restarts / Failures

No run restart was required. No persistent NaN, non-finite-gradient, deterministic-training, or OOM failure occurred. All six manifests record restart count `0`.

## 27. Tests Added

Added `tests/test_step14_training.py`, covering:

- exactly six summary rows and authorized direction × seed identity;
- exposure conservation and zero forbidden masks;
- checkpoint hash reproduction and reload;
- parameter count and architecture metadata;
- TRAIN/DEV-only access firewall;
- absence of missing-modality DEV fields;
- exact normalization reuse;
- absence of prediction, calibration, and B1 normalization outputs.

## 28. Full Validation

Fresh final validation passed:

- focused Step 14 artifact tests: **4 passed in 8.06s**;
- complete repository suite: **125 passed in 19.83s**;
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed;
- independent six-run artifact verification: passed;
- checkpoint reload verification: passed;
- data-access firewall verification: passed;
- no B1 prediction/calibration/normalization artifacts: passed.

## 29. Frozen Upstream Integrity

The following remained unchanged after training:

- Step 11.1 primary statistics;
- Step 12.1 gate metadata;
- B0 checkpoint and prediction namespaces;
- B0 normalization objects;
- B0 model/training configs;
- B1 protocol/config hashes;
- subject partitions;
- evaluation protocol.

No B1 prediction, calibration, conformal, SOURCE TEST, or TARGET artifact was created.

## 30. Files Created

- `scripts/step14_train_b1.py`;
- `tests/test_step14_training.py`;
- `reports/b1_training_summary_v1.csv`;
- `reports/b1_modality_exposure_summary_v1.csv`;
- `reports/b1_checkpoint_hashes_v1.txt`;
- `reports/step14_data_access_audit.csv`;
- `reports/step14_b1_training_gate.json`;
- `reports/STEP_14_B1_SOURCE_TRAINING_REPORT.md`;
- six local B1 run directories containing checkpoints, histories, manifests, and normalization references.

## 31. Files Modified

No B0, Step 11.1, Step 12.1, or Step 13 scientific artifact was modified. Step 14 added the training runner, focused tests, six-run source-training artifacts, gate metadata, summaries, access audit, and this report.

## 32. Explicitly Not Done

- no architecture change;
- no hyperparameter tuning;
- no normalization refit;
- no modality-probability change;
- no missing-modality DEV selection;
- no calibration;
- no conformal fit;
- no SOURCE TEST access;
- no TARGET access;
- no B1 prediction bundles;
- no B0-vs-B1 scientific comparison;
- no lightweight method;
- no SHHS;
- no checkpoint binaries committed;
- no raw/processed data committed;
- no push.

## 33. Remaining Pre-Evaluation Issues

`NONE`

The six B1 source-training checkpoints and provenance artifacts are complete and ready for the separately authorized evaluation/calibration step.

## 34. Recommended Next Step

# Step 15 — Fit B1 Source-Only Calibration/APS and Execute Frozen B1 C0–C5 Evaluation with Paired B0-vs-B1 Analysis

Step 15 must:

- freeze B1 SOURCE CALIBRATION objects before evaluation;
- evaluate all six B1 checkpoints under C0–C5;
- use authoritative corrected Step 11.1 bootstrap semantics;
- compare B1 against B0 v1.1 using paired subject bootstrap;
- assess predictive robustness and whether reliability failures persist;
- stop before any new method authorization or implementation.

Do NOT execute Step 15 here.

## 35. Git Status / Diff Summary

Step 14 artifacts are committed locally with:

`ml: train frozen B1 modality-dropout baselines`

Checkpoint binaries remain ignored and uncommitted. No remote push is authorized.