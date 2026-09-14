import hashlib
from pathlib import Path

import numpy as np
import pytest
import torch

from shiftsleep_uq.models.baseline_b0 import BaselineB0, condition_mask, count_trainable_parameters
from shiftsleep_uq.training.checkpointing import CheckpointSelector, is_better
from shiftsleep_uq.training.datasets import RoleAccessError, assert_role_allowed
from shiftsleep_uq.training.normalization import StreamingMoments
from shiftsleep_uq.training.reproducibility import seed_everything


@pytest.mark.parametrize("batch", [1, 3])
def test_b0_shapes_and_logits(batch):
    model = BaselineB0()
    logits = model(
        torch.randn(batch, 1, 3000),
        torch.randn(batch, 1, 1500),
        torch.tensor([[1, 1]] * batch),
    )
    assert logits.shape == (batch, 5)
    assert torch.isfinite(logits).all()


def test_condition_masks_are_frozen_and_all_missing_is_rejected():
    assert condition_mask("C0") == (1, 1)
    assert condition_mask("C1") == (1, 0)
    assert condition_mask("C2") == (0, 1)
    assert condition_mask("C3") == (1, 1)
    assert condition_mask("C4") == (1, 0)
    assert condition_mask("C5") == (0, 1)
    with pytest.raises(ValueError):
        condition_mask("C9")
    with pytest.raises(ValueError):
        BaselineB0()(torch.randn(1, 1, 3000), torch.randn(1, 1, 1500), torch.tensor([[0, 0]]))


def test_missing_branch_values_cannot_change_logits():
    seed_everything(17)
    model = BaselineB0().eval()
    eeg = torch.randn(2, 1, 3000)
    eog_a = torch.randn(2, 1, 1500)
    eog_b = eog_a * 1000.0 + 5000.0
    eeg_only_a = model(eeg, eog_a, torch.tensor([[1, 0], [1, 0]]))
    eeg_only_b = model(eeg, eog_b, torch.tensor([[1, 0], [1, 0]]))
    assert torch.equal(eeg_only_a, eeg_only_b)
    eeg_a = torch.randn(2, 1, 3000)
    eeg_b = eeg_a * -777.0
    eog = torch.randn(2, 1, 1500)
    eog_only_a = model(eeg_a, eog, torch.tensor([[0, 1], [0, 1]]))
    eog_only_b = model(eeg_b, eog, torch.tensor([[0, 1], [0, 1]]))
    assert torch.equal(eog_only_a, eog_only_b)


def test_streaming_moments_and_role_firewall():
    moments = StreamingMoments()
    moments.update(np.array([1.0, 2.0, 3.0], dtype=np.float32))
    moments.update(np.array([4.0, 5.0], dtype=np.float32))
    mean, std = moments.finalize(std_epsilon=1e-8)
    assert mean == pytest.approx(3.0)
    assert std == pytest.approx(np.sqrt(2.0))
    assert_role_allowed("TRAIN", "train")
    with pytest.raises(RoleAccessError):
        assert_role_allowed("DEV", "train")
    with pytest.raises(RoleAccessError):
        assert_role_allowed("CALIBRATION", "train")
    with pytest.raises(RoleAccessError):
        assert_role_allowed("TEST", "train")
    with pytest.raises(RoleAccessError):
        assert_role_allowed("TARGET", "train")
    with pytest.raises(RoleAccessError):
        assert_role_allowed("TEST", "normalization_fit")


def test_checkpoint_selection_lexicographic_rule_and_patience():
    assert is_better({"macro_f1": 0.81, "nll": 1.0, "epoch": 4}, {"macro_f1": 0.80, "nll": 0.1, "epoch": 1})
    assert is_better({"macro_f1": 0.80 + 1e-7, "nll": 0.9, "epoch": 4}, {"macro_f1": 0.80, "nll": 1.0, "epoch": 3})
    assert is_better({"macro_f1": 0.80, "nll": 0.9, "epoch": 4}, {"macro_f1": 0.80, "nll": 1.0, "epoch": 3})
    assert is_better({"macro_f1": 0.80, "nll": 1.0, "epoch": 2}, {"macro_f1": 0.80, "nll": 1.0, "epoch": 3})
    selector = CheckpointSelector(patience=2, min_epochs=5)
    assert selector.observe(1, 0.70, 1.2) is True
    assert selector.observe(2, 0.69, 1.1) is False
    assert selector.observe(3, 0.69, 1.1) is False
    assert selector.should_stop(3) is False
    assert selector.should_stop(5) is True


def test_seeded_initialization_and_forward_are_reproducible():
    seed_everything(42)
    first = BaselineB0().eval()
    first_input = (torch.randn(1, 1, 3000), torch.randn(1, 1, 1500))
    first_logits = first(*first_input, torch.tensor([[1, 1]]))
    first_hash = hashlib.sha256(torch.cat([p.detach().flatten().cpu() for p in first.parameters()]).numpy().tobytes()).hexdigest()
    seed_everything(42)
    second = BaselineB0().eval()
    second_logits = second(*first_input, torch.tensor([[1, 1]]))
    second_hash = hashlib.sha256(torch.cat([p.detach().flatten().cpu() for p in second.parameters()]).numpy().tobytes()).hexdigest()
    assert first_hash == second_hash
    assert torch.equal(first_logits, second_logits)


def test_synthetic_forward_backward_and_optimizer_step():
    seed_everything(2026)
    model = BaselineB0()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
    logits = model(torch.randn(2, 1, 3000), torch.randn(2, 1, 1500), torch.tensor([[1, 1], [1, 1]]))
    loss = torch.nn.CrossEntropyLoss()(logits, torch.tensor([0, 4]))
    loss.backward()
    total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    assert torch.isfinite(loss)
    assert torch.isfinite(total_norm)
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
    before = [p.detach().clone() for p in model.parameters()]
    optimizer.step()
    assert any(not torch.equal(a, b) for a, b in zip(before, model.parameters()))


def test_b0_parameter_count_is_frozen():
    assert count_trainable_parameters(BaselineB0()) == 654597


def test_model_config_and_training_config_are_explicit():
    root = Path(__file__).parents[1]
    model_config = (root / "configs/baseline_b0_v1.yaml").read_text(encoding="utf-8")
    training_config = (root / "configs/training_b0_v1.yaml").read_text(encoding="utf-8")
    assert "version: 1.0.0" in model_config
    assert "B0_DUAL_BRANCH_RAW_CNN" in model_config
    assert "version: 1.0.0" in training_config
    assert "augmentation: NONE" in training_config
    assert "modality_mask: [1, 1]" in training_config
    assert "scheduler: NONE" in training_config
