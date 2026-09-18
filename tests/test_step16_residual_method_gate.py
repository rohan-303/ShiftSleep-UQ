from __future__ import annotations
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_step16_frozen_gates_and_counts():
    assert json.loads((ROOT/'reports/step15_3_b1_evaluation_gate.json').read_text())['evaluation_gate']=='B1_PRIMARY_EVALUATION_COMPLETE'
    assert json.loads((ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').read_text())['engine_gate']=='WEIGHTED_RANKING_ENGINE_FROZEN'
    assert json.loads((ROOT/'reports/step16_method_gate.json').read_text())['step16_gate']=='STEP16_METHOD_GATE_COMPLETE'
    assert json.loads((ROOT/'reports/step16_method_gate.json').read_text())['method_authorization_gate']=='RELIABILITY_METHOD_NOT_AUTHORIZED'
    assert len(list((ROOT/'artifacts/calibration/step16_source_mask').glob('*/seed_*/**/temperature.json')))==18
    assert len(list((ROOT/'artifacts/calibration/step16_source_mask').glob('*/seed_*/**/aps.json')))==18

def test_step16_source_oracle_firewall_and_mapping():
    with (ROOT/'reports/step16_source_mask_temperature_v1.csv').open() as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==18 and {r['source_role'] for r in rows}=={'CALIBRATION'} and {r['fit_scope'] for r in rows}=={'SOURCE_CALIBRATION_ONLY'}
    with (ROOT/'reports/step16_b1_oracle_diagnostics_v1.csv').open() as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==60 and {r['analysis_scope'] for r in rows}=={'DIAGNOSTIC_ORACLE_ONLY'}
    for r in rows: assert int(r['oracle_calibration_subjects']) > 0 and int(r['oracle_evaluation_subjects']) > 0
    with (ROOT/'reports/step16_method_authorization_matrix_v1.csv').open() as f: m=list(csv.DictReader(f))
    assert len(m)==4 and {r['method_authorization'] for r in m}=={'RELIABILITY_METHOD_NOT_AUTHORIZED'}

def test_step16_argmax_invariance_and_mask_mapping():
    import numpy as np
    from scipy.special import softmax
    mapping={'C0':'FULL','C1':'EEG_ONLY','C2':'EOG_ONLY','C3':'FULL','C4':'EEG_ONLY','C5':'EOG_ONLY'}
    for exp in ('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'):
        for seed in (17,42,2026):
            for c,mask in mapping.items():
                p=ROOT/'artifacts/predictions/b1_moddrop'/exp/f'seed_{seed}'/f'{c}.npz'
                with np.load(p,allow_pickle=False) as z: logits=z['logits']; labels=z['labels']
                pred=logits.argmax(1); t=json.loads((ROOT/'artifacts/calibration/step16_source_mask'/exp/f'seed_{seed}'/mask/'temperature.json').read_text())['temperature']
                assert np.array_equal(pred, (logits/t).argmax(1))

def test_step16_original_criteria_logic_and_no_target_source_mix():
    text=(ROOT/'reports/step16_original_method_gate_spec.md').read_text()
    for criterion in ('Criterion A','Criterion B','Criterion C','Criterion D'):
        assert criterion in text
    with (ROOT/'reports/step16_data_access_audit.csv').open() as f: rows=list(csv.DictReader(f))
    assert all(r['target_access']!='DIAGNOSTIC_ORACLE_ONLY' for r in rows if r['phase']=='SOURCE_CONTROL')
    assert all(r['target_access']=='DIAGNOSTIC_ORACLE_ONLY' for r in rows if r['phase']=='ORACLE')
    gate=json.loads((ROOT/'reports/step16_method_gate.json').read_text())
    assert gate['learned_method_implemented'] is False and gate['step17'] is False and gate['shhs_access'] is False
    assert (ROOT/'reports/STEP_16_B1_RESIDUAL_FAILURE_AND_METHOD_GATE_REPORT.md').stat().st_size>0
    assert (ROOT/'reports/step16_statistical_hashes_v1.txt').exists()
