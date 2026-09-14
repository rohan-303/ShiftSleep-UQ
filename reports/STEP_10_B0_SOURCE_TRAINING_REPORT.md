# ShiftSleep-UQ Step 10 B0 Source Training Report

## 1. Status

**COMPLETE**

Step 10 completed exactly the authorized source-training scope. Both direction-level SOURCE TRAIN-only normalization artifacts were fitted and verified. All six frozen B0 direction-seed runs completed, selected checkpoints were reloaded successfully, and provenance/hash records were written.

## 2. Training Gate

`B0_SOURCE_TRAINING_COMPLETE`

## 3. Repository State

- Repository: `C:\Users\rohan\ShiftSleep-UQ`
- Branch: `main`
- Step 8.1 upstream commit present: `bcbc20c research: add independent source test protocol`
- Step 9 freeze commit present: `f0da129 ml: freeze and implement B0 baseline`
- Step 10 neutral implementation revisions used:
  - `ac9a294 fix: wire Step 10 frozen source artifacts`
  - `a4cb539 perf: vectorize streaming normalization moments`
  - `11f89eb fix: make Step 10 launcher self-contained`
  - `240c5ee fix: align Step 10 gradient config key`
- Final Step 10 result commit: `ml: train frozen B0 source baselines`
- No GitHub push performed.
- Binary checkpoints remain ignored and untracked.
- No raw or processed data was tracked.

## 4. Frozen Protocol Verification

Authoritative protocol: `configs/evaluation_protocol_v1_1.yaml`

- Protocol version: `1.1.0`
- Amendment: `A-08.1-01`
- Protocol SHA-256: `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`
- Baseline ID: `B0_DUAL_BRANCH_RAW_CNN`
- Frozen parameter count: `654597`
- Model seeds: `17`, `42`, `2026`
- Source roles accessed during Step 10: `TRAIN`, `DEV` only
- Calibration, SOURCE TEST, and TARGET signal arrays were not accessed.

Frozen artifact hashes verified before execution and again after execution:

| Artifact | SHA-256 |
|---|---|
| `configs/evaluation_protocol_v1_1.yaml` | `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756` |
| `configs/baseline_b0_v1.yaml` | `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17` |
| `configs/training_b0_v1.yaml` | `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7` |
| `docs/baseline_b0_protocol_v1.md` | `dea145bb27fc61325c5c79653c625233bd107eb689d12e8d13fa65e8a71ca4df` |

## 5. Environment

Recorded execution environment:

- OS: Windows 10, build `10.0.26200`
- Python: `3.11.15`
- PyTorch: `2.14.0+cu126`
- NumPy: `2.4.3`
- CUDA available: `True`
- CUDA runtime: `12.6`
- cuDNN: `91002`
- GPU: `NVIDIA GeForce RTX 3060 Laptop GPU`
- GPU memory: `6144 MiB` total, approximately `646–660 MiB` observed during training

No package upgrade was performed.

## 6. Batch-128 Memory Preflight

One discarded real-data memory smoke was completed before fitting/training:

- Real SOURCE TRAIN data: Sleep-EDF source TRAIN
- Batch size: `128`
- Modalities: full EEG + EOG
- Precision: FP32
- Model: frozen B0
- Operations: forward, unweighted cross-entropy, backward, global gradient clipping at `1.0`
- Optimizer step: not performed
- Peak CUDA allocated memory: `317.94 MB`
- Peak CUDA reserved memory: `398.00 MB`
- Result: **PASS**

No AMP, gradient accumulation, or physical batch-size reduction was used.

## 7. Data Access Firewall

The final audit is `reports/step10_data_access_audit.csv` with `343` unique source-recording access rows.

Observed access classes:

| Dataset | Role | Access purpose |
|---|---|---|
| Sleep-EDF SC | TRAIN | normalization fit / training |
| Sleep-EDF SC | DEV | development evaluation |
| ISRUC-S1 | TRAIN | normalization fit / training |
| ISRUC-S1 | DEV | development evaluation |

The audit contains zero `CALIBRATION`, `TEST`, or `TARGET` source roles. No target signal path was constructed or opened by the Step 10 execution layer. Calibration and SOURCE TEST were not used for signal access, training, checkpoint selection, or sanity inference.

## 8. D1 Source Population

Direction: `D1_SLEEPEDF_TO_ISRUC`

- Source dataset: Sleep-EDF SC
- Target dataset name retained only as protocol provenance: ISRUC-S1
- TRAIN: `47` subjects, `93` recordings, `252742` epochs
- DEV: `12` subjects, `24` recordings, `65042` epochs
- Source cohort SHA-256: `e8dbc91b04b4b54797e8d83be1866b28674fa2587e31507f94b3583e1f24f9ae`

## 9. D2 Source Population

Direction: `D2_ISRUC_TO_SLEEPEDF`

- Source dataset: ISRUC-S1
- Target dataset name retained only as protocol provenance: Sleep-EDF SC
- TRAIN: `59` subjects, `59` recordings, `53037` epochs
- DEV: `15` subjects, `15` recordings, `13785` epochs
- Source cohort SHA-256: `af4fb75be97df99443d5b7bc42d8f49bd55440702d07dffd49563356f7cece9d`

## 10. D1 Normalization

Artifact: `artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json`

Artifact SHA-256: `be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3`

- Source role: `TRAIN`
- Subjects: `47`
- Recordings: `93`
- EEG sample count: `758226000`
- EEG mean: `0.5552189785799693`
- EEG population standard deviation: `25.73285524449105`
- EOG sample count: `379113000`
- EOG mean: `-2.0231635080734183`
- EOG population standard deviation: `73.11381096319435`
- Epsilon: `1e-08`
- Data contract: `1.2.0`, SHA-256 `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`
- Preprocessing: `0.1.0`, SHA-256 `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`
- Subject partition SHA-256: `9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329`

## 11. D2 Normalization

Artifact: `artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json`

Artifact SHA-256: `3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e`

- Source role: `TRAIN`
- Subjects: `59`
- Recordings: `59`
- EEG sample count: `159111000`
- EEG mean: `0.05966135645658833`
- EEG population standard deviation: `26.830434995850137`
- EOG sample count: `79555500`
- EOG mean: `0.026554664780613038`
- EOG population standard deviation: `30.809566008653306`
- Epsilon: `1e-08`
- Data contract: `1.2.0`, SHA-256 `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`
- Preprocessing: `0.1.0`, SHA-256 `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`
- Subject partition SHA-256: `9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329`

## 12. Normalization Reproducibility

- Fitting was performed once per direction before seed-specific training.
- The same direction-level artifact was referenced by all three seeds in that direction.
- The streaming fitter used numerically stable vectorized parallel-moment updates over recording arrays.
- Each direction was independently recalculated in verification mode.
- Serialized means, standard deviations, and counts reproduced deterministically.
- All means and standard deviations were finite.
- All standard deviations exceeded epsilon.
- No DEV, CALIBRATION, TEST, or TARGET signal contributed to either artifact.

## 13. Frozen Training Recipe

- Architecture: `B0_DUAL_BRANCH_RAW_CNN`
- Input: raw canonical EEG/EOG epochs
- Training modality mask: `[1, 1]`
- Optimizer: AdamW
- Learning rate: `3e-4`
- Weight decay: `1e-4`
- Betas: `(0.9, 0.999)`
- Epsilon: `1e-8`
- Loss: unweighted multiclass cross-entropy
- Label smoothing: `0.0`
- Physical/effective batch size: `128` / `128`
- Precision: FP32
- Gradient clipping: global norm `1.0`
- Scheduler: none
- Maximum epochs: `30`
- Minimum epochs: `5`
- Early-stopping patience: `6`
- Selection: higher DEV macro-F1, then lower DEV NLL within `1e-6`, then earlier epoch
- Augmentation: none
- Class weighting: none
- Balancing: none
- Modality dropout: none
- Temporal context: none

## 14. D1 Seed 17

- Selected epoch: `7`
- Epochs executed: `13`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7389875650405884`
- SOURCE DEV NLL: `0.35900652582039694`
- Final TRAIN cross-entropy: `0.14683781746068034`
- Checkpoint SHA-256: `3e0ca3d3d7a345a4b2add8900499485bf2cf72afccb522de64d5d3115a9a5f9c`

## 15. D1 Seed 42

- Selected epoch: `5`
- Epochs executed: `11`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7381162643432617`
- SOURCE DEV NLL: `0.2699650688747758`
- Final TRAIN cross-entropy: `0.17508745572982257`
- Checkpoint SHA-256: `380496b69b5622944d259a0abd163325daecf39638ca3af4a1f6c01a9738d8fb`

## 16. D1 Seed 2026

- Selected epoch: `7`
- Epochs executed: `13`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7369469404220581`
- SOURCE DEV NLL: `0.3389765566513412`
- Final TRAIN cross-entropy: `0.1479199169114067`
- Checkpoint SHA-256: `edf8d12f40c33d3096de3dffd0c6fcfc5028b3923bb2e6894fc9e2a83e96ce45`

## 17. D2 Seed 17

- Selected epoch: `9`
- Epochs executed: `15`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7462037801742554`
- SOURCE DEV NLL: `0.6161431382271392`
- Final TRAIN cross-entropy: `0.23692873547644805`
- Checkpoint SHA-256: `bb82549b8860d07c83c85f27cd65a72b905d60ff220eab5942da9966c4d3afe6`

## 18. D2 Seed 42

- Selected epoch: `10`
- Epochs executed: `16`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7569921612739563`
- SOURCE DEV NLL: `0.6016836287212579`
- Final TRAIN cross-entropy: `0.20595578203758805`
- Checkpoint SHA-256: `3d12a02aeccbf0d5ffab2b5864b5c8ace5b51f27ca641dc6c5f1981831258574`

## 19. D2 Seed 2026

- Selected epoch: `3`
- Epochs executed: `9`
- Stop reason: `EARLY_STOPPING`
- SOURCE DEV macro-F1: `0.7347095608711243`
- SOURCE DEV NLL: `0.6094748663831547`
- Final TRAIN cross-entropy: `0.4717228336960607`
- Checkpoint SHA-256: `7af6ab439225b24fe1b2cb00c1285b88a54a527fe07be70b17d042418a203744`

## 20. Six-Run Summary

| Experiment | Seed | Selected epoch | Epochs executed | Stop reason | DEV macro-F1 | DEV NLL | Final TRAIN CE | Status |
|---|---:|---:|---:|---|---:|---:|---:|---|
| D1_SLEEPEDF_TO_ISRUC | 17 | 7 | 13 | EARLY_STOPPING | 0.7389875650405884 | 0.35900652582039694 | 0.14683781746068034 | COMPLETE |
| D1_SLEEPEDF_TO_ISRUC | 42 | 5 | 11 | EARLY_STOPPING | 0.7381162643432617 | 0.2699650688747758 | 0.17508745572982257 | COMPLETE |
| D1_SLEEPEDF_TO_ISRUC | 2026 | 7 | 13 | EARLY_STOPPING | 0.7369469404220581 | 0.3389765566513412 | 0.1479199169114067 | COMPLETE |
| D2_ISRUC_TO_SLEEPEDF | 17 | 9 | 15 | EARLY_STOPPING | 0.7462037801742554 | 0.6161431382271392 | 0.23692873547644805 | COMPLETE |
| D2_ISRUC_TO_SLEEPEDF | 42 | 10 | 16 | EARLY_STOPPING | 0.7569921612739563 | 0.6016836287212579 | 0.20595578203758805 | COMPLETE |
| D2_ISRUC_TO_SLEEPEDF | 2026 | 3 | 9 | EARLY_STOPPING | 0.7347095608711243 | 0.6094748663831547 | 0.4717228336960607 | COMPLETE |

These are source-development diagnostics only and are not domain-shift performance results.

## 21. Checkpoint Integrity

All six selected checkpoints:

- loaded into a fresh B0 instance;
- passed state-dict compatibility;
- retained parameter count `654597`;
- had finite parameters;
- produced finite logits on a SOURCE DEV smoke batch;
- retained class order `[Wake, N1, N2, N3, REM]`;
- referenced the correct direction-level normalization hash;
- retained experiment and seed metadata;
- matched their recorded SHA-256 values.

No checkpoint was tested on SOURCE TEST or TARGET.

## 22. Checkpoint Hash Manifest

Manifest: `reports/b0_checkpoint_hashes_v1.txt`

| Experiment | Seed | Relative checkpoint | SHA-256 |
|---|---:|---|---|
| D1_SLEEPEDF_TO_ISRUC | 17 | `artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_17/best.pt` | `3e0ca3d3d7a345a4b2add8900499485bf2cf72afccb522de64d5d3115a9a5f9c` |
| D1_SLEEPEDF_TO_ISRUC | 42 | `artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_42/best.pt` | `380496b69b5622944d259a0abd163325daecf39638ca3af4a1f6c01a9738d8fb` |
| D1_SLEEPEDF_TO_ISRUC | 2026 | `artifacts/models/b0/D1_SLEEPEDF_TO_ISRUC/seed_2026/best.pt` | `edf8d12f40c33d3096de3dffd0c6fcfc5028b3923bb2e6894fc9e2a83e96ce45` |
| D2_ISRUC_TO_SLEEPEDF | 17 | `artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_17/best.pt` | `bb82549b8860d07c83c85f27cd65a72b905d60ff220eab5942da9966c4d3afe6` |
| D2_ISRUC_TO_SLEEPEDF | 42 | `artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_42/best.pt` | `3d12a02aeccbf0d5ffab2b5864b5c8ace5b51f27ca641dc6c5f1981831258574` |
| D2_ISRUC_TO_SLEEPEDF | 2026 | `artifacts/models/b0/D2_ISRUC_TO_SLEEPEDF/seed_2026/best.pt` | `7af6ab439225b24fe1b2cb00c1285b88a54a527fe07be70b17d042418a203744` |

## 23. Training Reproducibility Controls

- Seeds fixed to `17`, `42`, and `2026` only.
- Python, NumPy, and PyTorch deterministic controls were applied.
- DataLoader shuffle generators were derived deterministically per seed and epoch.
- One model was trained per direction and seed.
- Direction-level normalization was reused across all three seeds.
- Source TRAIN controlled optimizer updates.
- SOURCE DEV alone controlled checkpoint selection and early stopping.
- No target observation, target label, SOURCE TEST signal, or SOURCE CALIBRATION signal entered training or selection.
- Run manifests record configuration hashes, cohort hashes, normalization hashes, environment, Git revision, duration, and restart count.

## 24. Restarts / Failures

Two launcher-level infrastructure failures occurred before valid model training output:

1. The first direct launcher invocation lacked `PYTHONPATH` and stopped on `ModuleNotFoundError` before fitting/training.
2. The self-contained launcher reached the first D1 run but stopped before the first completed epoch because it referenced a non-existent wrapper key for gradient clipping. The frozen YAML was unchanged; the wrapper was corrected to read `gradient.max_norm`.

The exact D1 seed-17 run was restarted from scratch with the same frozen configuration, seed, normalization, data, architecture, batch size, precision, and optimizer. No scientific parameter was changed. All six final manifests record `restart_count: 0` for their completed run instance. No persistent numerical, CUDA, or memory failure occurred.

## 25. Tests Added

Added `tests/test_step10_training.py` with five focused tests covering:

- normalization artifact schema and direction-level reuse across seeds;
- six-row summary and seed/direction invariant;
- checkpoint hash consistency, metadata, reload, finite logits, and parameter count;
- run-manifest frozen config hashes and forbidden metric fields;
- TRAIN/DEV-only data-access firewall.

## 26. Full Validation

Actual final outputs:

- `pytest -q` → **91 passed in 14.58s**
- `PYTHONPATH=src python -m compileall -q src tests scripts` → passed
- `git diff --check` → passed
- Exactly six successful run manifests → verified
- Exactly six selected checkpoint binaries → verified
- Exactly six checkpoint hash records → verified
- Exactly two normalization artifacts → verified
- Normalization reused across three seeds per direction → verified
- Access audit rows: `343` → verified
- CALIBRATION signal access: zero
- SOURCE TEST signal access: zero
- TARGET signal access: zero
- TEST/TARGET prediction outputs: none
- Step 8.1 protocol hash: unchanged
- Step 9 model/training config hashes: unchanged
- Frozen cohorts and subject partitions: unchanged
- Raw data newly tracked: none
- Processed epoch arrays newly tracked: none
- Checkpoint binaries tracked by Git: none
- GitHub push: none

## 27. Frozen Upstream Artifact Integrity

- Protocol SHA-256: `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`
- B0 model-config SHA-256: `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`
- B0 training-config SHA-256: `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7`
- Baseline protocol document SHA-256: `dea145bb27fc61325c5c79653c625233bd107eb689d12e8d13fa65e8a71ca4df`
- Data contract SHA-256: `ea8b2774a02192b1dcdb7f0b9ccaaef4232fd0772d8b154c47d0e707f73be036`
- Preprocessing SHA-256: `70cd20ccee62b14a23e5996c9f76b6a708a4e69bde03f36bdf4ee8dffa9ef794`
- Subject partition SHA-256: `9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329`
- D1 source cohort SHA-256: `e8dbc91b04b4b54797e8d83be1866b28674fa2587e31507f94b3583e1f24f9ae`
- D2 source cohort SHA-256: `af4fb75be97df99443d5b7bc42d8f49bd55440702d07dffd49563356f7cece9d`

## 28. Files Created

Tracked or safe report/test outputs:

- `reports/STEP_10_B0_SOURCE_TRAINING_REPORT.md`
- `reports/step10_data_access_audit.csv`
- `reports/step10_normalization_summary.csv`
- `reports/b0_training_summary_v1.csv`
- `reports/b0_checkpoint_hashes_v1.txt`
- `reports/b0_normalization_hashes_v1.txt`
- `tests/test_step10_training.py`

Ignored, source-derived artifacts:

- `artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json`
- `artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json`
- six ignored `best.pt` checkpoint binaries;
- six ignored `training_history.csv` files;
- six ignored `run_manifest.json` files;
- six ignored normalization reference files.

## 29. Files Modified

- `src/shiftsleep_uq/training/datasets.py`: neutral frozen-manifest recording resolution, source access logging, and forbidden-role manifest-only counting.
- `src/shiftsleep_uq/training/normalization.py`: neutral vectorized parallel-moment streaming update preserving the frozen population-statistics contract.
- `scripts/step10_train_b0.py`: Step 10 execution, provenance, audit, checkpoint, and summary orchestration.
- `tests/test_step10_training.py`: focused Step 10 integrity tests.

Frozen experimental YAML files, protocol documents, cohorts, partitions, and B0 architecture configuration were not modified.

## 30. Explicitly Not Done

The following were not performed:

- architecture tuning;
- hyperparameter tuning;
- class weighting;
- modality dropout;
- calibration fitting;
- conformal fitting;
- SOURCE TEST signal access;
- TARGET signal access;
- C0–C5 evaluation;
- TEST metrics;
- TARGET metrics;
- uncertainty evaluation;
- SHHS access;
- cohort amendment;
- protocol amendment;
- checkpoint binaries committed;
- raw data committed;
- processed data committed;
- GitHub push.

## 31. Remaining Pre-Evaluation Issues

`NONE`

## 32. Recommended Next Step

# Step 11 — Freeze Selected B0 Checkpoints, Fit Source-Only Calibration/Conformal Objects, and Execute C0–C5 Evaluation

Do **not** execute Step 11 as part of this report.

## 33. Git Status / Diff Summary

Before the final Step 10 commit, final validation reported:

- branch: `main`
- frozen upstream hashes: unchanged
- `91 passed`
- compileall: passed
- `git diff --check`: passed
- six manifests/checkpoints: verified
- no forbidden evaluation outputs: verified
- no push performed

The generated safe reports, summaries, audit, and focused tests are committed locally with:

`ml: train frozen B0 source baselines`

The final worktree is clean after the local commit. Binary checkpoints remain ignored and are referenced by the SHA-256 manifests above.
