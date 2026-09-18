from __future__ import annotations
import numpy as np
from shiftsleep_uq.evaluation_step11 import softmax, entropy
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates
from shiftsleep_uq.statistics.weighted_bootstrap import prepare, ranking

def fixture():
    p=np.array([[.99,.0025,.0025,.0025,.0025],[.0025,.99,.0025,.0025,.0025],[.0025,.0025,.99,.0025,.0025]])
    return {'subject_id':np.array(['A','B','C']),'labels':np.array([1,0,2]),'logits':np.log(p)}

def paths(metric):
    b=fixture(); sampled=np.array([0,0,2]); probs=softmax(b['logits']);
    h=float(weighted_metric_replicates(b,metric,sampled[None,:])[0])
    idx=np.array([0,0,2]);literal={'subject_id':b['subject_id'][idx],'labels':b['labels'][idx],'logits':b['logits'][idx]}
    l=float(__import__('shiftsleep_uq.step11_1_statistics',fromlist=['_metric'])._metric(literal,metric))
    pre=prepare(b['labels'],probs,b['subject_id'],entropy(probs)); e=float(ranking(pre,np.array([2,0,1]))[metric])
    return h,l,e

def test_historical_auprc_aa_c_differs_from_literal_and_exact():
    h,l,e=paths('ERROR_AUPRC'); assert h==0.0 and np.isclose(l,0.5) and np.isclose(e,0.5)

def test_historical_aurc_aa_c_differs_from_literal_and_exact():
    h,l,e=paths('AURC'); assert np.isclose(h,4/9) and np.isclose(l,7/18) and np.isclose(e,7/18)

def test_historical_auroc_control_agrees():
    h,l,e=paths('ERROR_AUROC'); assert np.isclose(h,l) and np.isclose(l,e)

def test_historical_macro_f1_control_agrees():
    b=fixture(); sampled=np.array([0,0,2]); h=float(weighted_metric_replicates(b,'macro-F1',sampled[None,:])[0])
    p=softmax(b['logits']); pre=prepare(b['labels'],p,b['subject_id'],entropy(p)); e=float(__import__('shiftsleep_uq.statistics.weighted_bootstrap',fromlist=['weighted_confusion','confusion_metrics']).confusion_metrics(__import__('shiftsleep_uq.statistics.weighted_bootstrap',fromlist=['weighted_confusion']).weighted_confusion(pre,np.array([2,0,1])))['macro-F1'])
    assert np.isclose(h,e)

def test_identity_point_estimate_is_unchanged():
    b=fixture(); p=softmax(b['logits']); pre=prepare(b['labels'],p,b['subject_id'],entropy(p)); m=np.ones(3,dtype=int)
    for metric in ('ERROR_AUROC','ERROR_AUPRC','AURC'):
        h=float(weighted_metric_replicates(b,metric,np.array([[0,1,2]],dtype=int))[0]); e=float(ranking(pre,m)[metric]); assert np.isclose(h,e)
