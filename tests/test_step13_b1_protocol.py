import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import torch

from shiftsleep_uq.models.baseline_b0 import BaselineB0, count_trainable_parameters
from shiftsleep_uq.training.modality_exposure import (
    ALLOWED_MASKS,
    EXPOSURE_SEED,
    assign_mask,
    assign_masks,
    apply_missing_modality_zeroing,
    mask_distribution,
)
from shiftsleep_uq.training.reproducibility import seed_everything


ROOT = Path(__file__).parents[1]


def test_mask_assignment_is_deterministic_epoch_varying_and_allowed():
    keys = [f"sleep_edf|S{i:04d}|R{i % 7}|{i}" for i in range(2000)]
    first = [assign_mask(EXPOSURE_SEED, 3, key) for key in keys]
    second = [assign_mask(EXPOSURE_SEED, 3, key) for key in keys]
    changed = [assign_mask(EXPOSURE_SEED, 4, key) for key in keys]
    assert first == second
    assert all(mask in ALLOWED_MASKS for mask in first + changed)
    assert any(a != b for a, b in zip(first, changed))
    assert all(mask != (0, 0) for mask in first + changed)


def test_mask_assignment_is_label_and_order_independent():
    keys = [f"dataset|subject|recording|{i}" for i in range(100)]
    ordered = dict(zip(keys, assign_masks(EXPOSURE_SEED, 9, keys)))
    reversed_keys = list(reversed(keys))
    reversed_result = dict(zip(reversed_keys, assign_masks(EXPOSURE_SEED, 9, reversed_keys)))
    assert ordered == reversed_result
    assert assign_mask(EXPOSURE_SEED, 9, keys[0]) == assign_mask(EXPOSURE_SEED, 9, keys[0], label=0)
    assert assign_mask(EXPOSURE_SEED, 9, keys[0]) == assign_mask(EXPOSURE_SEED, 9, keys[0], label=4)


def test_mask_distribution_matches_frozen_probabilities():
    keys = [f"dataset|S{i:06d}|R{i % 31}|{i}" for i in range(100_000)]
    counts = mask_distribution(EXPOSURE_SEED, 0, keys)
    total = sum(counts.values())
    assert set(counts) == set(ALLOWED_MASKS)
    assert counts[(1, 1)] / total == pytest.approx(0.50, abs=0.01)
    assert counts[(1, 0)] / total == pytest.approx(0.25, abs=0.01)
    assert counts[(0, 1)] / total == pytest.approx(0.25, abs=0.01)


def test_b1_uses_b0_architecture_and_seeded_initialization():
    assert count_trainable_parameters(BaselineB0()) == 654597
    for seed in (17, 42, 2026):
        seed_everything(seed)
        b0 = BaselineB0()
        seed_everything(seed)
        b1 = BaselineB0()
        b0_hash = hashlib.sha256(torch.cat([p.detach().flatten().cpu() for p in b0.parameters()]).numpy().tobytes()).hexdigest()
        b1_hash = hashlib.sha256(torch.cat([p.detach().flatten().cpu() for p in b1.parameters()]).numpy().tobytes()).hexdigest()
        assert b0_hash == b1_hash


def test_missing_modality_zeroing_and_synthetic_training_smoke():
    seed_everything(2029)
    eeg = torch.randn(3, 1, 3000)
    eog = torch.randn(3, 1, 1500)
    masks = torch.tensor([[1, 1], [1, 0], [0, 1]])
    masked_eeg, masked_eog = apply_missing_modality_zeroing(eeg, eog, masks)
    assert torch.equal(masked_eog[1], torch.zeros_like(masked_eog[1]))
    assert torch.equal(masked_eeg[2], torch.zeros_like(masked_eeg[2]))
    model = BaselineB0()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
    logits = model(masked_eeg, masked_eog, masks)
    loss = torch.nn.CrossEntropyLoss()(logits, torch.tensor([0, 1, 4]))
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    assert torch.isfinite(logits).all()
    assert torch.isfinite(loss)
    assert torch.isfinite(norm)
    assert all(parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in model.parameters())


def test_b1_configs_reference_frozen_b0_and_no_training_outputs_exist():
    model = (ROOT / "configs/baseline_b1_moddrop_v1.yaml").read_text(encoding="utf-8")
    training = (ROOT / "configs/training_b1_moddrop_v1.yaml").read_text(encoding="utf-8")
    assert "B1_B0_ARCH_SOURCE_MODALITY_DROPOUT" in model
    assert "B0_DUAL_BRANCH_RAW_CNN" in model
    assert "architecture_change: NONE" in model
    assert "parameter_count: 654597" in model
    assert "FULL: 0.50" in training
    assert "EEG_ONLY: 0.25" in training
    assert "EOG_ONLY: 0.25" in training
    assert "modality_exposure_seed: 2029" in training
    assert hashlib.sha256((ROOT / "artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json").read_bytes()).hexdigest() == "be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3"
    assert hashlib.sha256((ROOT / "artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json").read_bytes()).hexdigest() == "3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e"
    # Step 14 may create B1 checkpoints; Step 13 invariants prohibit only
    # evaluation/calibration/normalization outputs at the protocol stage.
    # Authorized post-Step-14/15 frozen predictions are permitted; the
    # protocol invariant is that Step 13 itself did not create them.
    gate = ROOT / "reports/step15_b1_evaluation_gate.json"
    assert gate.exists() or not list((ROOT / "artifacts/predictions").glob("b1_moddrop/**/*"))
    assert gate.exists() or not list((ROOT / "artifacts/calibration").glob("b1_moddrop/**/*"))
    assert not list((ROOT / "artifacts/normalization").glob("b1/**/*"))
