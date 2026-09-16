# B1 Source-Only Modality-Dropout Robustness Baseline

## Purpose

B1 tests whether B0's missing-modality degradation is partly explained by complete-modality-only source training. It keeps the frozen B0 architecture and changes only source-training modality exposure. B1 is a predictive-robustness baseline, not a reliability or calibration method.

## Frozen intervention

Every source-training epoch-level sample receives one deterministic mask from:

- FULL `[1,1]`: 0.50;
- EEG_ONLY `[1,0]`: 0.25;
- EOG_ONLY `[0,1]`: 0.25;
- `[0,0]`: forbidden.

The exposure seed is `2029`. Assignment uses the UTF-8 canonical string `{seed}\\x1f{epoch}\\x1f{dataset|subject_id|recording_id|epoch_index}`, SHA-256, the first 64 bits interpreted big-endian, and division by `2**64`. Values below 0.50 select FULL, values below 0.75 select EEG_ONLY, and all remaining values select EOG_ONLY. Labels, signal values, model outputs, montage, and loader order are not inputs. Including epoch makes exposure vary across epochs.

After frozen source normalization, unavailable normalized branches are replaced with zeros and their availability mask is zero. No noise, imputation, learned token, mask embedding, auxiliary loss, or signal synthesis is used.

## B0 invariance

B1 instantiates `B0_DUAL_BRANCH_RAW_CNN` directly. The expected trainable parameter count is `654597`, and same-seed fresh B0/B1 construction must produce identical initial state hashes. B1 reuses the exact B0 normalization artifacts for D1 and D2; it does not fit normalization.

All B0 optimizer, loss, data ordering, batch-size, precision, clipping, stopping, seed, partition, and evaluation definitions remain unchanged. The loss is ordinary unweighted FP32 cross-entropy. Checkpoint selection uses only full-modality SOURCE DEV macro-F1, then lower NLL, then earlier epoch. Missing-modality DEV metrics are not computed for selection.

## Future runs

The future matrix has exactly six runs: D1 and D2 with model seeds 17, 42, and 2026. Selected checkpoints will later be evaluated under frozen C0–C5 masks. Future calibration, APS, oracle analysis, and corrected subject bootstrap follow the existing B0/Step 11.1 protocols; none is executed by Step 13.

## Interpretation cases

- **Case A:** predictive robustness and reliability improve — missing-modality exposure explains a meaningful portion of compound failure.
- **Case B:** predictive robustness improves but reliability/ranking/conformal failures persist — reliability failure is not merely a missing-exposure artifact.
- **Case C:** compound predictive performance does not materially improve — simple dropout is insufficient.
- **Case D:** missing-modality performance improves but full-modality C0/C3 falls beyond the 0.02 descriptive guardrail — report the tradeoff rather than claiming uniform superiority.

## Execution boundary

Step 13 freezes the protocol and performs deterministic/synthetic/read-only source-mask validation only. It does not train the six B1 runs, create checkpoints or predictions, fit calibration or conformal objects, access TEST/TARGET/CALIBRATION signal, or execute Step 14.
