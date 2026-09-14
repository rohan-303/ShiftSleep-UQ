"""Focused post-execution checks for the Step 10 frozen training matrix."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import torch

from shiftsleep_uq.models import BaselineB0, count_trainable_parameters

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = {"D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF"}
SEEDS = {17, 42, 2026}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_normalization_artifact_schema_and_reuse() -> None:
    required = {"experiment_id", "source_dataset", "source_role", "subject_count", "recording_count", "EEG_sample_count", "EEG_mean", "EEG_std", "EOG_sample_count", "EOG_mean", "EOG_std", "epsilon", "data_contract_version", "data_contract_sha256", "preprocessing_version", "preprocessing_sha256", "evaluation_protocol_version", "evaluation_protocol_sha256", "subject_partition_sha256", "git_commit", "timestamp_utc"}
    for experiment in EXPERIMENTS:
        artifact = json.loads((ROOT / "artifacts/normalization/b0" / f"{experiment}.json").read_text(encoding="utf-8"))
        assert required <= artifact.keys()
        assert artifact["source_role"] == "TRAIN"
        assert float(artifact["EEG_std"]) > float(artifact["epsilon"])
        assert float(artifact["EOG_std"]) > float(artifact["epsilon"])
        assert artifact["EEG_sample_count"] > 0 and artifact["EOG_sample_count"] > 0
    summary = rows(ROOT / "reports/b0_training_summary_v1.csv")
    for experiment in EXPERIMENTS:
        hashes = {row["normalization_sha256"] for row in summary if row["experiment_id"] == experiment}
        assert len(hashes) == 1
        assert hashes == {sha256(ROOT / "artifacts/normalization/b0" / f"{experiment}.json")}


def test_summary_six_row_invariant_and_no_forbidden_metrics() -> None:
    summary_path = ROOT / "reports/b0_training_summary_v1.csv"
    summary = rows(summary_path)
    assert len(summary) == 6
    assert {(r["experiment_id"], int(r["seed"])) for r in summary} == {(e, s) for e in EXPERIMENTS for s in SEEDS}
    assert "TEST" not in summary[0] and "TARGET" not in summary[0] and "CALIBRATION" not in summary[0]
    assert all(r["status"] == "COMPLETE" for r in summary)


def test_checkpoint_metadata_reload_and_hashes() -> None:
    summary = rows(ROOT / "reports/b0_training_summary_v1.csv")
    hash_rows = rows(ROOT / "reports/b0_checkpoint_hashes_v1.txt")
    assert len(hash_rows) == 6
    for row in summary:
        checkpoint = ROOT / "artifacts/models/b0" / row["experiment_id"] / f"seed_{row['seed']}" / "best.pt"
        assert sha256(checkpoint) == row["checkpoint_sha256"]
        assert any(h["sha256"] == row["checkpoint_sha256"] for h in hash_rows)
        payload = torch.load(checkpoint, map_location="cpu", weights_only=False)
        metadata = payload["metadata"]
        assert metadata["experiment_id"] == row["experiment_id"]
        assert metadata["seed"] == int(row["seed"])
        assert metadata["class_order"] == ["Wake", "N1", "N2", "N3", "REM"]
        assert metadata["normalization_sha256"] == row["normalization_sha256"]
        model = BaselineB0()
        model.load_state_dict(payload["model_state_dict"])
        assert count_trainable_parameters(model) == 654597
        model.eval()
        with torch.no_grad():
            logits = model(torch.zeros(2, 1, 3000), torch.zeros(2, 1, 1500), torch.ones(2, 2))
        assert torch.isfinite(logits).all()


def test_run_manifest_hashes_and_no_forbidden_metrics() -> None:
    for experiment in EXPERIMENTS:
        for seed in SEEDS:
            run_dir = ROOT / "artifacts/models/b0" / experiment / f"seed_{seed}"
            manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
            assert manifest["model_config_sha256"] == "a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17"
            assert manifest["training_config_sha256"] == "2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7"
            assert manifest["evaluation_protocol_sha256"] == "dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756"
            forbidden_keys = {key.lower() for key in manifest if any(token in key.lower() for token in ("test_metric", "target_metric", "calibration_metric"))}
            assert not forbidden_keys


def test_data_access_firewall() -> None:
    audit = rows(ROOT / "reports/step10_data_access_audit.csv")
    assert audit
    assert {(r["dataset"], r["source_role"]) for r in audit} == {("sleep_edf_sc", "TRAIN"), ("sleep_edf_sc", "DEV"), ("isruc_s1", "TRAIN"), ("isruc_s1", "DEV")}
    assert not {r["source_role"] for r in audit}.intersection({"CALIBRATION", "TEST", "TARGET"})
    assert all("calibration" not in r["path"].lower() and "target" not in r["path"].lower() and "test" not in r["path"].lower() for r in audit)
