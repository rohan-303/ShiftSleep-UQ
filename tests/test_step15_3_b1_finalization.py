from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def test_authoritative_b0_v12_and_engine_gate():
    assert hashlib.sha256((ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz').read_bytes()).hexdigest()=='e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1'
    assert json.loads((ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').read_text())['engine_gate']=='WEIGHTED_RANKING_ENGINE_FROZEN'

def test_b1_artifact_completeness_after_finalization():
    p=ROOT/'artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz'
    if not p.exists(): return
    with np.load(p) as z:
        assert len(z.files)==120
        assert all(z[k].shape==(2000,) for k in z.files)

def test_b1_shards_and_manifest_after_finalization():
    p=ROOT/'reports/step15_3_shard_completeness_audit.csv'
    if not p.exists(): return
    rows=list(csv.DictReader(open(p))); assert len(rows)==7200
    assert all(int(r['end'])-int(r['start'])==100 for r in rows)

def test_no_step16_gate():
    p=ROOT/'reports/step15_3_b1_evaluation_gate.json'
    if p.exists(): assert json.loads(p.read_text())['step16'] is False
