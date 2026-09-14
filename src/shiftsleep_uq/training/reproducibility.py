"""Deterministic seed and loader utilities."""
from __future__ import annotations

import os
import random
from typing import Any

import numpy as np
import torch


def seed_everything(seed: int, *, deterministic: bool = True) -> dict[str, Any]:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.use_deterministic_algorithms(True, warn_only=False)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    return {
        "seed": seed,
        "deterministic_requested": deterministic,
        "torch_deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "cuda_available": cuda_available,
    }


def make_epoch_generator(seed: int, epoch: int) -> torch.Generator:
    generator = torch.Generator()
    generator.manual_seed((int(seed) * 1_000_003 + int(epoch)) % (2**63 - 1))
    return generator


def seed_worker(worker_id: int) -> None:
    worker_seed = torch.initial_seed() % (2**32)
    np.random.seed(worker_seed)
    random.seed(worker_seed)
