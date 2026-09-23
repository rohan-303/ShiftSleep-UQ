from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("r3_runner", ROOT / "scripts/run_r3_seqsleepnet.py")
r3 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = r3
spec.loader.exec_module(r3)


def test_stft_contract_and_source_only_normalization():
    epoch = r3.epoch_spectrogram(np.zeros(3000), np.zeros(1500))
    assert epoch.shape == (2, 129, 29)
    norm = r3.fit_source_normalization([epoch, epoch + 1])
    assert norm["scope"] == "SOURCE_TRAIN_ONLY"
    assert np.asarray(norm["mean"]).shape == (2, 129)
    assert r3.apply_source_normalization(epoch, norm).shape == epoch.shape


def test_physical_sequences_do_not_cross_gaps_or_recordings():
    records = [(Path("a.npz"), i, "s1", "r1", "NA") for i in range(21)]
    records += [(Path("a.npz"), 23, "s1", "r1", "NA")]
    records += [(Path("b.npz"), i, "s1", "r2", "NA") for i in range(20)]
    refs = r3.physical_contiguous_sequences(records, length=20, stride=1)
    assert [(ref.recording_id, ref.start_index) for ref in refs] == [("r1", 0), ("r1", 1), ("r2", 0)]
    assert all(np.diff(ref.indices).tolist() == [1] * 19 for ref in refs)


def test_s0_s1_exposure_is_deterministic_and_label_independent():
    ref = r3.SequenceRef(Path("a"), tuple(range(20)), "s", "r", 0)
    assert r3.sequence_mask("S0", "D1", 17, 1, ref) == (1, 1)
    first = r3.sequence_mask("S1", "D1", 17, 1, ref)
    second = r3.sequence_mask("S1", "D1", 17, 1, ref)
    assert first == second and first in {(1, 1), (1, 0), (0, 1)}
    with pytest.raises(ValueError):
        r3.sequence_mask("BAD", "D1", 17, 1, ref)


def test_matched_initialization_and_collision_failing_attempt(tmp_path):
    _, _, init_hash = r3.matched_initialization(17)
    assert len(init_hash) == 64
    attempt = r3.allocate_attempt("D1_SLEEPEDF_TO_ISRUC", "S0", 17, root=tmp_path)
    assert (attempt / "checkpoints").is_dir()
    second = r3.allocate_attempt("D1_SLEEPEDF_TO_ISRUC", "S0", 17, root=tmp_path)
    assert second != attempt
    metadata = r3.required_metadata(protocol_hash="x", direction="D1_SLEEPEDF_TO_ISRUC", variant="S0", seed=17, attempt=attempt, status="RUNNING")
    assert metadata["target_access"] == "FORBIDDEN"
