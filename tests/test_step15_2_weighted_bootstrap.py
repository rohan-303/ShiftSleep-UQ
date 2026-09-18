import numpy as np
import json
from pathlib import Path
from shiftsleep_uq.statistics.weighted_bootstrap import *

def fixture():
 y=np.array([0,1,2,0,1,2]); p=np.array([[.8,.1,.05,.03,.02],[.1,.7,.1,.05,.05],[.1,.2,.5,.1,.1],[.4,.2,.1,.2,.1],[.2,.3,.2,.2,.1],[.1,.2,.2,.2,.3]])
 sid=np.array(['A','A','B','C','C','C']); return prepare(y,p,sid)
def test_multiplicity_and_duplicate_equivalence():
 x=fixture(); m=np.array([2,0,1]); z=literal(x,m); assert np.allclose(list(confusion_metrics(weighted_confusion(x,m)).values()),list(confusion_metrics(weighted_confusion(z,np.ones(len(z.subject_ids)))).values()),equal_nan=True)
def test_additive_metrics_duplicate_equivalence():
 x=fixture(); m=np.array([2,0,1]); z=literal(x,m)
 assert abs(nll(x,m)-nll(z,np.ones(len(z.subject_ids))))<1e-12; assert abs(brier(x,m)-brier(z,np.ones(len(z.subject_ids))))<1e-12; assert abs(ece(x,m)-ece(z,np.ones(len(z.subject_ids))))<1e-12
def test_ranking_metrics_duplicate_equivalence():
 x=fixture(); m=np.array([2,0,1]); z=literal(x,m); a=ranking(x,m); b=ranking(z,np.ones(len(z.subject_ids)))
 assert np.allclose(list(a.values()),list(b.values()),atol=1e-12,equal_nan=True)
def test_ties_and_undefined():
 x=fixture(); r=ranking(x,np.ones(len(x.subject_ids))); assert np.isfinite(r['ERROR_AUROC']); assert np.isnan(r['ERROR_AUPRC']) or np.isfinite(r['ERROR_AUPRC'])
def test_shard_merge_rejects_overlap():
 m={'replicate_start':0,'replicate_end':2}; assert np.allclose(merge_shards([(m,np.array([1.,2.]))],2),[1,2])
 try: merge_shards([(m,np.array([1.,2.])),(m,np.array([1.,2.]))],2); assert False
 except ValueError: pass
def test_draw_invariants():
 assert validate_multiplicities(np.array([[1,0,2],[0,3,0]],dtype=np.int16))

def test_atomic_shard_roundtrip_and_validation(tmp_path):
 meta=shard_metadata('B1','D1','C0',17,'AUPRC',0,2,'p','d','e')
 path=tmp_path/'s.npz'; atomic_write_shard(path,meta,np.array([.1,.2]))
 assert path.exists() and not list(tmp_path.glob('*.tmp'))
 assert validate_shard_file(path,meta)
 bad=dict(meta); bad['metric']='AURC'
 try: validate_shard_file(path,bad); assert False
 except ValueError: pass

def test_shard_resume_and_reject_missing_range(tmp_path):
 m1=shard_metadata('B1','D1','C0',17,'AUPRC',0,2,'p','d','e'); m2=shard_metadata('B1','D1','C0',17,'AUPRC',2,4,'p','d','e')
 p1=tmp_path/'1.npz'; p2=tmp_path/'2.npz'; atomic_write_shard(p1,m1,np.array([1.,2.])); atomic_write_shard(p2,m2,np.array([3.,4.]))
 assert np.allclose(merge_shards([read_shard(p1),read_shard(p2)],4),[1,2,3,4])
 try: merge_shards([read_shard(p1)],4); assert False
 except ValueError: pass

from shiftsleep_uq.step11_1_statistics import exact_weighted_metric_replicates


def test_versioned_exact_replicates_match_literal_ranking():
    p=np.array([[.99,.0025,.0025,.0025,.0025],[.0025,.99,.0025,.0025,.0025],[.0025,.0025,.99,.0025,.0025]])
    b={'subject_id':np.array(['A','B','C']), 'labels':np.array([1,0,2]), 'logits':np.log(p)}
    x=prepare(b['labels'],p,b['subject_id']); m=np.array([2,0,1]); z=literal(x,m); draws=np.array([[0,0,2]])
    for metric in ('ERROR_AUROC','ERROR_AUPRC','AURC'):
        exact=float(exact_weighted_metric_replicates(b,metric,draws)[0])
        assert np.isclose(exact,ranking(z,np.ones(len(z.subject_ids),dtype=int))[metric],atol=1e-12,equal_nan=True)
