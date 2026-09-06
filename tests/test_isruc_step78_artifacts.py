import csv
import json
from pathlib import Path

import numpy as np

from shiftsleep_uq.data.montage_contract import resolve_isruc_channels

ROOT = Path(__file__).parents[1]


def test_adapter_resolves_exact_a1a2_indices_without_fallback():
    result = resolve_isruc_channels(["E1-M2", "C3-A2", "LOC-A2"])
    assert result["eeg_index"] == 1
    assert result["eog_index"] == 2
    assert result["montage_variant"] == "ISRUC_A1A2"


def test_adapter_resolves_exact_m1m2_indices_without_fallback():
    result = resolve_isruc_channels(["C3-M2", "E2-M1", "E1-M2"])
    assert result["eeg_index"] == 0
    assert result["eog_index"] == 2
    assert result["montage_variant"] == "ISRUC_M1M2"


def test_adapter_rejects_mixed_pair():
    import pytest
    with pytest.raises(ValueError):
        resolve_isruc_channels(["C3-A2", "E1-M2"])


def test_v2_manifests_have_100_expected_subject_rows_and_no_split_fields():
    path = ROOT / "reports/isruc_original_subject_manifest_v2.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert len(rows) == 100
    assert {r["subject_id"] for r in rows} == {f"I{i:03d}" for i in range(1, 101)}
    assert not {k for k in rows[0] if "split" in k.lower() or "fold" in k.lower()}


def test_v2_outputs_preserve_contract_metadata_and_shapes():
    manifest = list(csv.DictReader((ROOT / "reports/isruc_original_recording_manifest_v2.csv").open(encoding="utf-8")))
    included = [r for r in manifest if r["terminal_status"] == "INCLUDED"]
    assert len(included) == 36
    for row in included:
        p = ROOT / "data/processed/isruc_original_v2" / f"isruc_s1__{row['subject_id']}__original_v2.npz"
        with np.load(p, allow_pickle=False) as z:
            meta = json.loads(z["metadata_json"].item())
            assert meta["contract_version"] == "1.2.0"
            assert meta["preprocessing_version"] == "0.1.0"
            assert meta["scorer"] == "scorer_1"
            assert meta["source_eeg_derivation"] in {"C3-A2", "C3-M2"}
            assert meta["source_eog_derivation"] in {"LOC-A2", "E1-M2"}
            assert meta["montage_variant"] in {"ISRUC_A1A2", "ISRUC_M1M2"}
            assert z["eeg"].shape[1:] == (3000,)
            assert z["eog"].shape[1:] == (1500,)


def test_v2_accounting_and_determinism_pass():
    accounting = list(csv.DictReader((ROOT / "reports/isruc_original_epoch_accounting_v2.csv").open(encoding="utf-8")))
    included = [r for r in accounting if r["status"] == "PASS"]
    assert len(included) == 36
    assert all(int(r["accounting_delta"]) == 0 for r in included)
    det = list(csv.DictReader((ROOT / "reports/isruc_determinism_audit_v2.csv").open(encoding="utf-8")))
    assert len(det) == 36
    assert all(r["status"] == "PASS" and r["identical"] == "True" for r in det)
