# ShiftSleep-UQ Step 13 B1 Modality-Dropout Robustness Protocol Report

## 1. Status

`B1_PROTOCOL_FROZEN`

Step 13 froze and implemented the B1 source-only modality-dropout robustness protocol. No full B1 training run was executed.

## 2. B1 Protocol Gate

`B1_PROTOCOL_FROZEN`

The architecture, parameter count, initialization pairing, normalization reuse, exposure distribution, exposure seed, deterministic mask generator, source-only access boundary, checkpoint-selection rule, synthetic smoke, real SOURCE TRAIN mask smoke, tests, and frozen hashes passed.

## 3. Scientific Motivation

B0 was trained only with complete EEG+EOG but was evaluated with missing modalities. B1 tests whether source-training exposure to missing modalities reduces the observed missing-modality and compound-shift predictive degradation. B1 is a controlled predictive-robustness baseline, not a calibration method or architectural innovation.

## 4. Upstream Frozen State

Verified upstream hashes:

- evaluation protocol: `configs/evaluation_protocol_v1_1.yaml` — `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`;
- subject partitions: `reports/subject_partitions_v2.csv` — `9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329`;
- B0 model config: `configs/baseline_b0_v1.yaml` — `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`;
- B0 training config: `configs/training_b0_v1.yaml` — `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7`;
- D1 B0 normalization: `be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3`;
- D2 B0 normalization: `3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e`.

Step 11.1 primary results and Step 12.1 gates were preserved. The historical gates remain `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED` and `MODALITY_CONDITIONING_SUPPORTED`.

## 5. B1 Identity

- ID: `B1_B0_ARCH_SOURCE_MODALITY_DROPOUT`;
- name: `B1 Source-Only Modality-Dropout Robustness Baseline`;
- version: `1.0.0`;
- future directions: D1 and D2;
- future model seeds: 17, 42, and 2026.

## 6. Exact Difference from B0

`SOURCE TRAIN MODALITY EXPOSURE ONLY`

B1 changes only the mask distribution presented during SOURCE TRAIN optimization. It does not change architecture, normalization, loss, optimizer, data partitions, initialization policy, checkpoint selection, or evaluation protocol.

## 7. Architecture Invariance

B1 directly reuses `B0_DUAL_BRANCH_RAW_CNN` from the existing B0 model implementation. The EEG encoder, EOG encoder, residual blocks, GroupNorm, GELU, dropout, late concatenation, deterministic embedding zeroing, five-class head, and no-context design are unchanged.

## 8. Parameter Count

Expected and verified trainable parameter count:

`654597`

## 9. Initialization Pairing

For seeds 17, 42, and 2026, fresh B0 and B1 references instantiated with the same seed produced identical initial state hashes. B1 introduces no alternate initialization path.

## 10. Normalization Reuse

B1 references the frozen B0 normalization artifacts without refitting:

- D1: `artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json`, SHA-256 `be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3`;
- D2: `artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json`, SHA-256 `3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e`.

## 11. Training Exposure Distribution

The frozen source-training mixture is:

| Exposure | Mask | Probability |
|---|---|---:|
| FULL | `[1,1]` | 0.50 |
| EEG_ONLY, EOG missing | `[1,0]` | 0.25 |
| EOG_ONLY, EEG missing | `[0,1]` | 0.25 |

`[0,0]` is forbidden. No loss reweighting or balanced sampler is introduced.

## 12. Exposure Seed

`MODALITY_EXPOSURE_SEED = 2029`

The exposure seed is independent of model seeds, split seed 2026, oracle seed 2027, and bootstrap seed 2028.

## 13. Deterministic Mask Algorithm

The canonical UTF-8 serialization is:

`{exposure_seed}\x1f{epoch}\x1f{dataset|subject_id|recording_id|epoch_index}`

SHA-256 is applied to this byte string. The first 64 digest bits are interpreted as an unsigned big-endian integer and divided by `2**64` to obtain `u` in `[0,1)`. Assignment is:

- `u < 0.50`: `[1,1]`;
- `0.50 <= u < 0.75`: `[1,0]`;
- otherwise: `[0,1]`.

The implementation does not depend on Python `hash()`, batch position, worker order, model output, signal values, labels, montage, or target outcomes.

## 14. Epoch-Varying Exposure

Epoch is part of the canonical key. The same physiological epoch can receive different masks in different epochs. This is intentional and allows repeated optimization exposure to all permitted modality configurations.

## 15. Label Independence

The public assignment API consumes only exposure seed, epoch, and stable sample key. A regression test confirmed that changing an optional audit-only label value does not change the mask. Labels are not used by the implementation.

## 16. Missing-Modality Tensor Semantics

After frozen source normalization, an unavailable branch is multiplied by zero and its availability-mask component is zero. Available branches retain their normalized values. No noise, imputation, copied signal, learned missing token, mask embedding, or synthetic physiology is used.

## 17. Training Loss

The future B1 training loss remains ordinary unweighted:

`CrossEntropyLoss(weight=None, label_smoothing=0.0)`

No auxiliary, consistency, contrastive, distillation, reconstruction, or modality-specific loss is added.

## 18. Optimizer / Hyperparameters

B1 reuses B0 exactly:

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
- patience 6;
- no class, subject, montage, or recording balancing;
- no additional augmentation.

## 19. Data Ordering

B1 preserves the B0 natural epoch-level data order and deterministic per-epoch shuffle mechanism. It adds masks by stable sample identity rather than by batch position. No modality-balanced sampler is used.

## 20. DEV Checkpoint Selection

Future checkpoint selection uses SOURCE DEV with mask `[1,1]` only. The primary criterion is higher full-modality DEV macro-F1. Tie-breaks are lower full-modality DEV NLL and earlier epoch, with tolerance `1e-6`.

## 21. Why Missing-Modality DEV Is Not Used

Missing-modality DEV selection would introduce a second scientific intervention beyond source-training exposure. B1 therefore does not compute or use C1/C2-like DEV metrics during training and does not use target or test metrics for selection.

## 22. Future Experiment Count

Exactly six future B1 checkpoints are planned:

- D1 seed 17;
- D1 seed 42;
- D1 seed 2026;
- D2 seed 17;
- D2 seed 42;
- D2 seed 2026.

No extra seeds are authorized.

## 23. Future C0–C5 Evaluation

Each future selected checkpoint will eventually use the frozen conditions:

- C0 `[1,1]` SOURCE TEST;
- C1 `[1,0]` SOURCE TEST;
- C2 `[0,1]` SOURCE TEST;
- C3 `[1,1]` COMPLETE TARGET;
- C4 `[1,0]` COMPLETE TARGET;
- C5 `[0,1]` COMPLETE TARGET.

No condition-specific retraining or checkpoint is permitted.

## 24. Future Source Calibration / APS

Future B1 evaluation will reuse the B0 source-only calibration protocol: source-calibration temperature and source-calibration APS transferred unchanged to source test and complete target. Any later oracle analysis must remain separately labeled. No calibration or APS fit occurred in Step 13.

## 25. Corrected Statistical Procedure

Future B1 statistics will use the corrected Step 11.1 subject-cluster bootstrap:

- 2,000 replicates;
- bootstrap seed 2028;
- duplicate cluster multiplicity preserved;
- metric-level multi-seed averaging;
- common subject resamples across seeds;
- paired conditions where applicable.

No statistics were computed in Step 13.

## 26. B0-vs-B1 Paired Comparison

Future comparisons will use authoritative B0 `v1_1` against B1 on the same populations, conditions, seeds, and metrics. The primary contrast is `B1 - B0`, using paired subject bootstrap and matched model-seed labels. Independent confidence-interval comparison is prohibited.

## 27. Primary Robustness Question

The primary question is whether source-only modality exposure reduces predictive degradation in D1 C4, D1 C5, D2 C4, and D2 C5.

Primary metric:

`macro-F1`

Primary contrast:

`macro-F1_B1 - macro-F1_B0`

No B1 result has been computed.

## 28. Reliability Question

After predictive robustness is assessed in a future step, secondary reliability summaries will include NLL, Brier, entropy error AUROC, entropy error AUPRC, entropy AURC, conformal signed coverage gap, and conformal set size. Improving macro-F1 will not be interpreted as automatic reliability improvement.

## 29. Full-Modality Guardrail

Future D1 C3 and D2 C3 comparisons will report:

`Δ_full_target_macroF1 = B1 - B0`

A drop greater than `0.02` absolute macro-F1 is a practically notable descriptive tradeoff. Raw paired intervals will always be reported. This is not a hypothesis-test boundary.

## 30. Interpretation Cases A–D

- **Case A:** predictive robustness and reliability improve — missing-modality exposure explains a meaningful portion of compound failure.
- **Case B:** predictive robustness improves but calibration/ranking/conformal failures persist — reliability failure is not merely a consequence of never training on missing modalities.
- **Case C:** B1 does not materially improve compound predictive performance — simple source modality dropout is insufficient.
- **Case D:** missing-modality performance improves but full-modality C0/C3 falls beyond the guardrail — report the robustness tradeoff and do not claim uniform superiority.

These interpretations are frozen before B1 results.

## 31. Lightweight Method Gate

The historical gate remains:

`LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`

Step 13 does not reopen, implement, or evaluate the lightweight method.

## 32. Model Config

- Path: `configs/baseline_b1_moddrop_v1.yaml`;
- version: `1.0.0`;
- SHA-256: `b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6`;
- architecture reference: `B0_DUAL_BRANCH_RAW_CNN`;
- B0 model-config SHA-256: `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`;
- architecture change: `NONE`.

## 33. Training Config

- Path: `configs/training_b1_moddrop_v1.yaml`;
- version: `1.0.0`;
- SHA-256: `467ed74d465a65990388f4ac4f271311ccb156605cc1cfef1d4339057298bbc7`;
- B0 training-config SHA-256: `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7`;
- exposure seed: `2029`;
- exposure probabilities: 50/25/25;
- execution status: protocol-only, no full training.

## 34. Protocol Document

- Path: `docs/baseline_b1_moddrop_protocol_v1.md`;
- SHA-256: `7db8bc63f21df1ea53fb58d881c8e4996651e57e1c8fd154283b1d273caa2c1c`.

## 35. Mask Determinism Test

Passed. Repeated assignment with identical seed, epoch, and stable key produced identical masks. Changing epoch changed masks for some synthetic examples. Only `[1,1]`, `[1,0]`, and `[0,1]` occurred; `[0,0]` never occurred.

## 36. Mask Distribution Test

Passed on 100,000 synthetic sample-key/epoch combinations. Empirical proportions were within ±0.01 of the frozen 0.50/0.25/0.25 thresholds.

## 37. Label-Independence Test

Passed. Identical sample key, epoch, and exposure seed produced the same mask regardless of supplied audit label value. The production assignment path does not require labels.

## 38. Order/Worker Independence Test

Passed. Ordered and reversed stable-key collections produced identical per-key assignments. Assignment is a pure function of seed, epoch, and stable key and is independent of DataLoader order or worker scheduling.

## 39. Same-Initialization Test

Passed for model seeds 17, 42, and 2026. Fresh B0/B1 architecture references had identical initial parameter hashes and the expected parameter count.

## 40. Same-Normalization Test

Passed. The exact frozen B0 D1 and D2 normalization files and hashes are referenced. No B1 normalization file was created.

## 41. Synthetic Training Smoke

Passed. A discarded synthetic batch containing all three allowed masks completed one FP32 CE forward/backward/gradient-clipping/optimizer step with finite logits, loss, gradients, and update. No `[0,0]` mask was used.

This was an implementation smoke only, not a B1 experiment.

## 42. Real SOURCE TRAIN Mask Smoke

Passed read-only for both source directions:

- D1 loaded one SOURCE TRAIN sample using frozen D1 normalization, produced a valid stable key, assigned an allowed mask, and produced finite `[1,1,3000]` EEG and `[1,1,1500]` EOG tensors after zeroing;
- D2 loaded one SOURCE TRAIN sample using frozen D2 normalization, produced a valid stable key, assigned an allowed mask, and produced finite `[1,1,3000]` EEG and `[1,1,1500]` EOG tensors after zeroing.

No optimization, metrics, DEV, CALIBRATION, SOURCE TEST, or TARGET access occurred.

## 43. Tests Added

Added:

- `tests/test_step13_b1_protocol.py`;
- deterministic mask assignment and distribution tests;
- label/order independence tests;
- B0/B1 initialization and parameter-count tests;
- missing-modality zeroing and synthetic training smoke;
- normalization hash and output-boundary tests.

## 44. Full Validation

Fresh final validation passed:

- focused B1 protocol tests: **6 passed**;
- fail-closed protocol entrypoint: passed;
- real SOURCE TRAIN read-only mask smoke: passed for D1 and D2;
- frozen upstream hashes: passed;
- B1 protocol/config hashes: passed;
- full repository suite: **121 passed in 17.25s**;
- `PYTHONPATH=src python -m compileall -q src tests scripts`: passed;
- `git diff --check`: passed;
- all frozen upstream hashes: passed;
- B1 output-boundary scan: passed; no B1 checkpoints, predictions, or normalization artifacts;
- tracked raw/processed-data scan: passed.

No B1 scientific result table exists because no B1 training or evaluation was run.

## 45. Files Created

- `src/shiftsleep_uq/training/modality_exposure.py`;
- `scripts/train_b1.py`;
- `configs/baseline_b1_moddrop_v1.yaml`;
- `configs/training_b1_moddrop_v1.yaml`;
- `docs/baseline_b1_moddrop_protocol_v1.md`;
- `tests/test_step13_b1_protocol.py`;
- `reports/step13_b1_protocol_hashes.txt`;
- `reports/step13_b1_protocol_gate.json`;
- this report.

## 46. Files Modified

No B0 model, B0 config, B0 training config, B0 checkpoint, B0 prediction, B0 normalization, Step 11.1, or Step 12.1 artifact was modified. Step 13 added only its protocol implementation, configuration, tests, hashes, gate metadata, and report.

## 47. Explicitly Not Done

- no B1 full training;
- no B1 checkpoint;
- no B1 prediction;
- no normalization refit;
- no architecture change;
- no hyperparameter tuning;
- no missing-modality DEV selection;
- no calibration fit;
- no conformal fit;
- no TEST access;
- no TARGET access;
- no CALIBRATION signal access;
- no lightweight method;
- no SHHS;
- no Step 14;
- no push.

## 48. Remaining Pre-Experiment Issues

`NONE`

The protocol is frozen and ready for the separately authorized training step. Full B1 training remains intentionally unexecuted.

## 49. Recommended Next Step

# Step 14 — Train the Six Frozen B1 Source-Only Modality-Dropout Checkpoints

Step 14 must:

- reuse B0 normalization;
- train exactly six B1 runs;
- use SOURCE TRAIN only for optimization;
- use full-modality SOURCE DEV only for checkpoint selection;
- record modality-exposure counts;
- stop before CALIBRATION, SOURCE TEST, or TARGET evaluation.

Do NOT execute Step 14 here.

## 50. Git Status / Diff Summary

Step 13 was committed locally with the required message:

`ml: preregister B1 modality-dropout baseline`

No remote push is authorized.

## Scientific Stop Rule

B1 exists to test an alternative explanation for the B0 result. If later B1 results improve missing-modality performance, that evidence must be accepted. If B1 fails, that result must also be accepted. The 50/25/25 policy, architecture, loss, and checkpoint-selection rule must not be changed after observing results.
