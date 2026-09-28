from __future__ import annotations

import csv
import hashlib
import json
import time
import traceback
from collections import OrderedDict
from pathlib import Path

import numpy as np
import torch
from scipy.signal import resample_poly, stft
from torch import nn
from torch.utils.data import DataLoader, Dataset

from shiftsleep_uq.evaluation_step11 import macro_f1, nll, softmax
from shiftsleep_uq.models.seqsleepnet_class import SeqSleepNetClass, count_trainable_parameters
from shiftsleep_uq.remediation.datasets import RemediationManifestDataset
from shiftsleep_uq.training.datasets import source_dataset_for_experiment
from shiftsleep_uq.training.reproducibility import seed_everything

ROOT=Path(__file__).resolve().parents[1];PHASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b';EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];VARS=['S0','S1'];SEEDS=[17,42,2026];CONDS=['C0','C1','C2','C3','C4','C5'];EXPOSURE_SEED=2029

CACHE_ROOT=ROOT/'artifacts/remediation/r3/spectrogram_cache'; STFT_CONFIG={'fs':100,'window':'hamming','nperseg':200,'noverlap':100,'nfft':256,'boundary':None,'padded':False,'log_eps':1e-8}; STFT_HASH=hashlib.sha256(json.dumps(STFT_CONFIG,sort_keys=True).encode()).hexdigest()

def _input_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def _cache_paths(p,input_hash):
 key=hashlib.sha256(f'{Path(p).resolve()}|{input_hash}|{PHASH}|{STFT_HASH}'.encode()).hexdigest()
 return CACHE_ROOT/f'{key}.npy',CACHE_ROOT/f'{key}.json'
def _build_or_open_cache(p):
 CACHE_ROOT.mkdir(parents=True,exist_ok=True); ih=_input_sha(p); data_path,meta_path=_cache_paths(p,ih)
 if data_path.exists() and meta_path.exists():
  meta=json.loads(meta_path.read_text())
  if meta.get('input_sha256')!=ih or meta.get('protocol_sha256')!=PHASH or meta.get('stft_config_sha256')!=STFT_HASH: raise RuntimeError('R3_CACHE_METADATA_MISMATCH')
  return np.load(data_path,mmap_mode='r'),meta
 with np.load(p,allow_pickle=False) as z:
  eeg=np.asarray(z['eeg']);eog=np.asarray(z['eog']); labels=np.asarray(z['labels'],dtype=np.int16);phys=np.asarray(z['source_epoch_indices'],dtype=np.int64)
  out=np.lib.format.open_memmap(data_path,mode='w+',dtype=np.float32,shape=(len(eeg),2,129,29))
  for i in range(len(eeg)): out[i]=spec_epoch(eeg[i],eog[i])
  out.flush();del out
 meta={'input_path':str(Path(p).resolve()),'input_sha256':ih,'protocol_sha256':PHASH,'stft_config_sha256':STFT_HASH,'shape':[len(eeg),2,129,29],'dtype':'float32','labels':labels.tolist(),'physical_epoch_indices':phys.tolist(),'cache_sha256':sha(data_path)}
 meta_path.write_text(json.dumps(meta,sort_keys=True)+'\n');return np.load(data_path,mmap_mode='r'),meta

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def spec_epoch(eeg,eog):
 eog=resample_poly(eog.astype(np.float32),2,1)
 def one(x):
  _,_,z=stft(x.astype(np.float32),fs=100,window='hamming',nperseg=200,noverlap=100,nfft=256,boundary=None,padded=False,return_onesided=True);return np.log(np.abs(z).astype(np.float64)**2+1e-8).astype(np.float32)
 out=np.stack([one(eeg),one(eog)]);assert out.shape==(2,129,29);return out

def spec_recording(eeg,eog):
 eog=resample_poly(eog.astype(np.float32),2,1,axis=-1)
 def many(x):
  _,_,z=stft(x.astype(np.float32),fs=100,window='hamming',nperseg=200,noverlap=100,nfft=256,boundary=None,padded=False,return_onesided=True,axis=-1);return np.log(np.abs(z).astype(np.float64)**2+1e-8).astype(np.float32)
 a,b=many(eeg),many(eog);out=np.stack([a,b],axis=1);assert out.shape[1:]==(2,129,29);return out

def refs(ds,stride):
 grouped={}
 for p,row,s,r,m in ds.records:grouped.setdefault((p,s,r),[]).append(row)
 out=[]
 for (p,s,r),rows in grouped.items():
  with np.load(p,allow_pickle=False) as z:phys=z['source_epoch_indices'].astype(int)
  rows=sorted(rows);seg=[]
  for row in rows:
   if seg and phys[row]!=phys[seg[-1]]+1:
    if len(seg)>=20:
     out += [(p,tuple(seg[i:i+20]),s,r,int(phys[seg[i]])) for i in range(0,len(seg)-19,stride)]
    seg=[]
   seg.append(row)
  if len(seg)>=20:out += [(p,tuple(seg[i:i+20]),s,r,int(phys[seg[0]])) for i in range(0,len(seg)-19,stride)]
 return out

class SeqDS(Dataset):
 def __init__(self,ds,normalization,stride):
  self.refs=refs(ds,stride);self.norm=normalization;self.cache=OrderedDict();self.meta={};self.ds=ds
  for p,_,_,_,_ in ds.records:
   if p not in self.meta:
    with np.load(p,allow_pickle=False) as z:self.meta[p]={'labels':np.asarray(z['labels'],dtype=np.int16),'phys':np.asarray(z['source_epoch_indices'],dtype=np.int64)}
 def __len__(self):return len(self.refs)
 def _open(self,p):
  if p not in self.cache:self.cache[p]=_build_or_open_cache(p)[0]
  self.cache.move_to_end(p)
  while len(self.cache)>2:self.cache.popitem(last=False)
  return self.cache[p]
 def __getitem__(self,i):
  p,rows,s,r,start=self.refs[i];spec=self._open(p);a=self.meta[p];x=np.asarray(spec[list(rows)],dtype=np.float32);mean=np.asarray(self.norm['mean'],np.float32)[:,:,None];std=np.asarray(self.norm['std'],np.float32)[:,:,None];x=(x-mean)/std
  return {'x':torch.from_numpy(x),'y':torch.tensor(a['labels'][list(rows)],dtype=torch.long),'subject_id':s,'recording_id':r,'start_index':start,'ref_index':i}

def fit_norm(ds):
 total=np.zeros((2,129),np.float64);sq=np.zeros_like(total);n=0;seen=set()
 for p,row,s,r,m in ds.records:
  if p in seen:continue
  seen.add(p);cache,_meta=_build_or_open_cache(p)
  for i in range(0,cache.shape[0],64):
   z=np.asarray(cache[i:i+64],dtype=np.float64);total+=z.sum((0,3));sq+=(z*z).sum((0,3));n+=z.shape[0]*z.shape[3]
 mean=total/n;std=np.maximum(np.sqrt(np.maximum(sq/n-mean*mean,0)),1e-6);return {'scope':'SOURCE_TRAIN_ONLY','count':n,'mean':mean.tolist(),'std':std.tolist(),'cache_stft_config_sha256':STFT_HASH}
def mask_for(var,exp,seed,epoch,subject,recording,start):
 if var=='S0':return (1.,1.)
 h=hashlib.sha256(f'{EXPOSURE_SEED}\x1f{exp}\x1f{seed}\x1f{epoch}\x1f{subject}\x1f{recording}\x1f{start}'.encode()).digest();u=int.from_bytes(h[:8],'big')/2**64
 return (1.,1.) if u<.5 else ((1.,0.) if u<.75 else (0.,1.))
def eval_model(model,ds,device,exp,var,seed,epoch,condition=None):
 model.eval();logits=[];labels=[];keys=[]
 with torch.no_grad():
  for b in DataLoader(ds,batch_size=32,shuffle=False,num_workers=0):
   m=torch.tensor([((1.,1.) if condition in ('C0','C3') else ((1.,0.) if condition in ('C1','C4') else (0.,1.))) if condition else mask_for(var,exp,seed,epoch,s,r,st) for s,r,st in zip(b['subject_id'],b['recording_id'],b['start_index'])],dtype=torch.float32,device=device);z=model(b['x'].to(device),m).cpu().numpy();
   for bi in range(len(z)):
    for j in range(20):logits.append(z[bi,j]);labels.append(int(b['y'][bi,j]));keys.append((b['subject_id'][bi],b['recording_id'][bi],int(b['start_index'][bi])+j))
 d={};
 for z,y,k in zip(logits,labels,keys):d.setdefault(k,[[],y])[0].append(z)
 L=np.asarray([np.mean(v[0],axis=0) for v in d.values()],np.float32);Y=np.asarray([v[1] for v in d.values()]);S=np.asarray([k[0] for k in d]);R=np.asarray([k[1] for k in d]);E=np.asarray([k[2] for k in d]);return {'logits':L,'labels':Y,'subject_id':S,'recording_id':R,'epoch_index':E}
def existing_complete(jid):
 base=ROOT/'artifacts/remediation/r3'/jid
 for d in sorted(base.glob('ATTEMPT_*'),reverse=True):
  p=d/'run_manifest.json';cp=d/'best.pt';cm=d/'completion_marker.json';h=d/'training_history.json';n=d/'normalization.json'
  if not all(x.exists() for x in [p,cp,cm,h,n]):continue
  try:
   x=json.loads(p.read_text());z=json.loads(cm.read_text())
   if x.get('job_id')!=jid or x.get('status')!='COMPLETE' or z.get('status')!='COMPLETE' or len(json.loads(h.read_text()))!=10:continue
   if x.get('protocol_sha256')!=PHASH or sha(cp)!=x.get('checkpoint_sha256') or sha(n)!=x.get('normalization_sha256'):continue
   x['attempt']=int(d.name.split('_')[-1]);return x
  except (OSError,ValueError,KeyError):continue
 return None

def init_models(seed):
 seed_everything(seed);base=SeqSleepNetClass();state={k:v.detach().clone() for k,v in base.state_dict().items()};a=SeqSleepNetClass();b=SeqSleepNetClass();a.load_state_dict(state);b.load_state_dict(state);h=hashlib.sha256(b''.join(v.cpu().numpy().tobytes() for v in state.values())).hexdigest();return a,b,h
def train_job(exp,var,seed,train,dev,norm):
 jid=f'R3_{exp}_{var}_SEED_{seed}';base=ROOT/'artifacts/remediation/r3'/jid
 base.mkdir(parents=True,exist_ok=True)
 for an in range(1,4):
  d=base/f'ATTEMPT_{an:03d}'
  try:d.mkdir();break
  except FileExistsError:continue
 else:raise RuntimeError('R3_ATTEMPT_LIMIT_EXCEEDED')
 (d/'protocol_hash.txt').write_text(PHASH+'\n');(d/'normalization.json').write_text(json.dumps(norm,sort_keys=True)+'\n');start=time.time()
 try:
  if count_trainable_parameters(SeqSleepNetClass())!=117062:raise RuntimeError('R3_PARAMETER_COUNT_MISMATCH')
  device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu');s0,s1,ih=init_models(seed);model=(s0 if var=='S0' else s1).to(device).float();opt=torch.optim.Adam(model.parameters(),lr=1e-4,weight_decay=1e-3);best=None;hist=[];tr=SeqDS(train,norm,10);dv=SeqDS(dev,norm,1)
  for epoch in range(1,11):
   model.train();total=0.;n=0
   for b in DataLoader(tr,batch_size=32,shuffle=True,num_workers=0):
    m=torch.tensor([mask_for(var,exp,seed,epoch,s,r,st) for s,r,st in zip(b['subject_id'],b['recording_id'],b['start_index'])],dtype=torch.float32,device=device);z=model(b['x'].to(device),m);loss=nn.CrossEntropyLoss()(z.reshape(-1,5),b['y'].to(device).reshape(-1));opt.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step();total+=loss.detach().item()*len(b['y']);n+=len(b['y'])
   q=eval_model(model,dv,device,exp,var,seed,epoch);f=macro_f1(softmax(q['logits']).argmax(1),q['labels']);nv=nll(softmax(q['logits']),q['labels']);hist.append({'epoch':epoch,'dev_macro_f1':f,'dev_nll':nv,'train_loss':total/n});
   if best is None or (f>best['f'] or (f==best['f'] and (nv<best['n'] or (nv==best['n'] and epoch<best['e'])))):best={'f':f,'n':nv,'e':epoch};torch.save({'model_state_dict':model.state_dict(),'metadata':{'job_id':jid,'best_epoch':epoch,'init_hash':ih,'normalization_sha256':sha(d/'normalization.json')}},d/'best.pt')
  manifest={'job_id':jid,'attempt':int(d.name.split('_')[-1]),'status':'COMPLETE','best_epoch':best['e'],'dev_macro_f1':best['f'],'dev_nll':best['n'],'checkpoint_sha256':sha(d/'best.pt'),'normalization_sha256':sha(d/'normalization.json'),'initialization_sha256':ih,'protocol_sha256':PHASH,'wall_clock_seconds':time.time()-start};(d/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(d/'training_history.json').write_text(json.dumps(hist,indent=2)+'\n');(d/'completion_marker.json').write_text(json.dumps({'status':'COMPLETE'})+'\n');return manifest
 except Exception as e:  # noqa: BLE001
  (d/'failure.json').write_text(json.dumps({'status':'FAILED','error':repr(e),'traceback':traceback.format_exc()},indent=2)+'\n');return {'job_id':jid,'status':'FAILED','error':repr(e)}
def main():
 if sha(ROOT/'configs/postreview_remediation_protocol_v2.yaml')!=PHASH:raise RuntimeError('R3_PROTOCOL_HASH_FAILURE')
 rows=[]
 for exp in EXPS:
  source=source_dataset_for_experiment(exp);train=RemediationManifestDataset(source,'TRAIN','train',root=ROOT);dev=RemediationManifestDataset(source,'DEV','dev',root=ROOT)
  train.records=[(p if train.dataset!='sleep_edf_sc' else ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'/p.name,i,s,r,m) for p,i,s,r,m in train.records];dev.records=[(p if dev.dataset!='sleep_edf_sc' else ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'/p.name,i,s,r,m) for p,i,s,r,m in dev.records]
  norm=fit_norm(train);nd=ROOT/'artifacts/remediation/normalization/r3';nd.mkdir(parents=True,exist_ok=True);(nd/f'{exp}.json').write_text(json.dumps(norm,sort_keys=True)+'\n')
  for var in VARS:
   for seed in SEEDS:
    jid=f'R3_{exp}_{var}_SEED_{seed}';existing=existing_complete(jid)
    if existing is not None:
     rows.append(existing);print(json.dumps({'reuse':existing}),flush=True);continue
    print(json.dumps({'start':exp,var:var,'seed':seed}),flush=True);rows.append(train_job(exp,var,seed,train,dev,norm));print(json.dumps(rows[-1]),flush=True)
 with (ROOT/'reports/remediation/r3_checkpoint_manifest_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
 print(json.dumps({'jobs':len(rows),'complete':sum(r.get('status')=='COMPLETE' for r in rows),'failed':sum(r.get('status')=='FAILED' for r in rows)}))
if __name__=='__main__':main()
