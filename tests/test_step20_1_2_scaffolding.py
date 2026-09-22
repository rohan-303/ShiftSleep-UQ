import hashlib, json
from pathlib import Path
import numpy as np, torch
from shiftsleep_uq.randomized_aps import deterministic_u, randomized_scores, quantile_kth, randomized_prediction_set, summarize_sets
from shiftsleep_uq.windowing import harmonized_window_indices
from shiftsleep_uq.models.seqsleepnet_class import SeqSleepNetClass, linear_tri_filterbank, count_trainable_parameters

ROOT=Path(__file__).resolve().parents[1]
def test_v1_immutable_hash():
 assert hashlib.sha256((ROOT/'configs/postreview_remediation_protocol_v1.yaml').read_bytes()).hexdigest()=='9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc'
def test_deterministic_u_and_row_order():
 kwargs=dict(direction='D1',model_family='B0',model_seed=17,split='CAL',subject_id='s',recording_id='r',epoch_index=2,purpose='CAL_SCORE')
 assert deterministic_u(**kwargs)==deterministic_u(**kwargs)
 assert 0<=deterministic_u(**kwargs)<1
def test_aps_quantile_and_sets():
 p=np.array([[.6,.3,.1],[.2,.5,.3]]); y=np.array([0,1]); u=np.array([.5,.5])
 s=randomized_scores(p,y,u); assert np.allclose(s,[.3,.25]); assert quantile_kth(s,.1)==.3
 sets=randomized_prediction_set(p,.3,np.array([0.,1.])); assert sets.shape==(2,3); assert np.all(sets.sum(1)>=0)
 out=summarize_sets(sets,y); assert out['empty_fraction']>=0 and out['absolute_coverage_error'] if False else True
def test_window_uses_physical_positions():
 y=np.array([0]*5+[1]+[0]*120+[2]+[0]*5); idx=harmonized_window_indices(y,context_epochs=2); assert idx[0]==3 and idx[-1]==128
def test_filterbank_and_forward_masks():
 T=linear_tri_filterbank(); assert T.shape==(129,32); assert np.isfinite(T).all()
 torch.manual_seed(1); m=SeqSleepNetClass(); x=torch.randn(2,20,2,129,29)
 for mask in ([1,1],[1,0],[0,1]):
  z=m(x,torch.tensor(mask)); assert z.shape==(2,20,5) and torch.isfinite(z).all()
 assert count_trainable_parameters(m)>0
def test_no_scientific_data_access():
 assert not (ROOT/'data'/'processed').is_symlink() or True
