"""Exact subject-multiplicity weighted bootstrap statistics.

All functions operate on frozen epoch observations and integer subject weights.
No model, signal, or calibration access is performed here.
"""
from __future__ import annotations
import json
import os
import tempfile
import hashlib
from dataclasses import dataclass
from pathlib import Path
import numpy as np

CLASS_COUNT=5
@dataclass(frozen=True)
class Prepared:
    subject_ids: np.ndarray
    subject_index: np.ndarray
    labels: np.ndarray
    predictions: np.ndarray
    probabilities: np.ndarray
    uncertainty: np.ndarray
    errors: np.ndarray
    epoch_count: np.ndarray

def prepare(labels, probabilities, subject_ids, uncertainty=None):
    y=np.asarray(labels,dtype=np.int64); p=np.asarray(probabilities,dtype=np.float64); sid=np.asarray(subject_ids)
    subjects=np.asarray(sorted(set(sid.tolist())))
    si=np.searchsorted(subjects,sid); pred=p.argmax(1); u=(-np.sum(np.clip(p,1e-12,1)*np.log(np.clip(p,1e-12,1)),axis=1) if uncertainty is None else np.asarray(uncertainty,dtype=np.float64))
    return Prepared(subjects,si,y,pred,p,u,(pred!=y).astype(np.int8),np.bincount(si,minlength=len(subjects)).astype(np.int64))
def _weights(prepared,m):
    m=np.asarray(m,dtype=np.int64)
    if m.ndim!=1 or len(m)!=len(prepared.subject_ids) or np.any(m<0): raise ValueError('invalid subject multiplicities')
    return m[prepared.subject_index].astype(np.float64)
def weighted_confusion(prepared,m):
    w=_weights(prepared,m); cm=np.zeros((5,5),dtype=np.float64)
    np.add.at(cm,(prepared.labels,prepared.predictions),w); return cm
def confusion_metrics(cm):
    tp=np.diag(cm); den=2*tp+cm.sum(0)-tp+cm.sum(1)-tp; rec=np.divide(tp,cm.sum(1),out=np.zeros(5),where=cm.sum(1)>0)
    return {'accuracy':float(np.trace(cm)/cm.sum()) if cm.sum() else float('nan'),'balanced_accuracy':float(rec.mean()),'macro-F1':float(np.mean(np.divide(2*tp,den,out=np.zeros(5),where=den>0))),'recall_Wake':float(rec[0]),'recall_N1':float(rec[1]),'recall_N2':float(rec[2]),'recall_N3':float(rec[3]),'recall_REM':float(rec[4])}
def nll(prepared,m):
 w=_weights(prepared,m); return float(np.sum(w*(-np.log(np.clip(prepared.probabilities[np.arange(len(prepared.labels)),prepared.labels],1e-12,1))))/w.sum())
def brier(prepared,m):
 w=_weights(prepared,m); one=np.eye(5)[prepared.labels]; return float(np.sum(w*np.sum((prepared.probabilities-one)**2,axis=1))/w.sum())
def ece(prepared,m,bins=15):
 w=_weights(prepared,m); conf=prepared.probabilities.max(1); correct=(prepared.predictions==prepared.labels).astype(float); total=w.sum(); out=0.
 for i in range(bins):
  ix=(conf>=i/bins)&((conf<(i+1)/bins) if i<bins-1 else (conf<=1))
  if ix.any() and w[ix].sum()>0: out+=w[ix].sum()/total*abs(np.sum(w[ix]*correct[ix])/w[ix].sum()-np.sum(w[ix]*conf[ix])/w[ix].sum())
 return float(out)
def conformal(prepared,m,sets,alpha):
 w=_weights(prepared,m); covered=sets[np.arange(len(prepared.labels)),prepared.labels]; sizes=sets.sum(1); total=w.sum(); cov=float(np.sum(w*covered)/total)
 return {'empirical_coverage':cov,'coverage_gap':1-alpha-cov,'absolute_coverage_error':abs(1-alpha-cov),'mean_set_size':float(np.sum(w*sizes)/total),'singleton_fraction':float(np.sum(w*(sizes==1))/total),'empty_fraction':float(np.sum(w*(sizes==0))/total)}
def ranking(prepared,m):
 w=_weights(prepared,m); asc=np.argsort(prepared.uncertainty,kind='stable'); desc=np.argsort(-prepared.uncertainty,kind='stable'); wa=w[asc]; err_a=prepared.errors[asc].astype(float); total=wa.sum(); pos=np.sum(wa*err_a); neg=total-pos
 if pos==0 or neg==0: auroc=auprc_value=float('nan')
 else:
  starts=np.cumsum(wa)-wa+1; rank_sum=np.sum(err_a*(wa*starts+wa*(wa-1)/2)); auroc=float((rank_sum-pos*(pos+1)/2)/(pos*neg))
  wd=w[desc]; err_d=prepared.errors[desc].astype(np.int64); positives=int(pos); c=0; tpv=0.; ap=0.
  for wi,ei in zip(wd,err_d):
   wi=int(wi)
   if ei and wi:
    k=np.arange(1,wi+1,dtype=np.float64); keep=np.ones(wi,dtype=bool)
    if c==0: keep[0]=False
    ap+=float(np.sum(((tpv+k)/(c+k))[keep])/positives); tpv+=wi
   c+=wi
  auprc_value=float(ap)
 c=0; e=0.; h=np.zeros(int(total)+1,dtype=np.float64); h[1:]=np.cumsum(1/np.arange(1,int(total)+1,dtype=np.float64)); aurc_num=0.
 for wi,ei in zip(wa,err_a):
  wi=int(wi)
  if not wi: continue
  delta=h[c+wi]-h[c]
  aurc_num += e*delta if not ei else wi+(e-c)*delta
  c+=wi; e+=wi*int(ei)
 aurc_value=float(aurc_num/total)
 return {'ERROR_AUROC':auroc,'ERROR_AUPRC':auprc_value,'AURC':aurc_value}
def literal(prepared,m):
 idx=np.repeat(np.arange(len(prepared.labels)),_weights(prepared,m).astype(np.int64)); return prepare(prepared.labels[idx],prepared.probabilities[idx],prepared.subject_ids[prepared.subject_index[idx]],prepared.uncertainty[idx])
def validate_multiplicities(m):
 a=np.asarray(m)
 if a.ndim!=2 or not np.issubdtype(a.dtype,np.integer) or np.any(a<0): raise ValueError('invalid multiplicity matrix')
 if not np.all(a.sum(1)==a.shape[1]): raise ValueError('draw rows do not sum to subject count')
 return True
def shard_metadata(model,direction,condition,seed,metric,start,end,prediction_hash,draw_hash,engine_hash):
 return {'model':model,'direction':direction,'condition':condition,'seed':seed,'metric':metric,'replicate_start':start,'replicate_end':end,'prediction_hash':prediction_hash,'draw_hash':draw_hash,'engine_hash':engine_hash}
def validate_shard(meta,values,expected,allowed_undefined=False):
 required=('model','direction','condition','seed','metric','replicate_start','replicate_end','prediction_hash','draw_hash','engine_hash')
 if any(k not in meta for k in required) or any(meta.get(k)!=expected.get(k) for k in required): raise ValueError('invalid shard metadata')
 a,b=int(expected['replicate_start']),int(expected['replicate_end']); values=np.asarray(values,dtype=np.float64)
 if values.ndim!=1 or len(values)!=b-a or a<0 or b<=a: raise ValueError('invalid shard range/vector')
 if not allowed_undefined and not np.isfinite(values).all(): raise ValueError('nonfinite shard values')
 if allowed_undefined and np.any(~np.isfinite(values) & ~np.isnan(values)): raise ValueError('invalid undefined sentinel')
 return True

def engine_hash(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic_write_shard(path,metadata,values):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:
   np.savez_compressed(f,metadata=json.dumps(metadata,sort_keys=True,separators=(',',':')),values=np.asarray(values,dtype=np.float64)); f.flush(); os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)

def read_shard(path):
 with np.load(path,allow_pickle=False) as z: return json.loads(str(z['metadata'].item())),np.asarray(z['values'],dtype=np.float64)

def validate_shard_file(path,expected,allowed_undefined=False):
 meta,values=read_shard(path); return validate_shard(meta,values,expected,allowed_undefined)

def merge_shards(shards,reps):
 out=np.full(reps,np.nan); seen=np.zeros(reps,dtype=bool)
 for meta,values in shards:
  a,b=meta['replicate_start'],meta['replicate_end']
  if a<0 or b>reps or a>=b or seen[a:b].any() or len(values)!=b-a: raise ValueError('overlapping/missing shard')
  out[a:b]=values; seen[a:b]=True
 if not seen.all(): raise ValueError('missing shard range')
 return out
