from __future__ import annotations
import csv,hashlib,json,random,time,traceback
from pathlib import Path
import numpy as np,torch
from scipy.signal import stft,resample_poly
from torch import nn
from torch.utils.data import Dataset,DataLoader
from shiftsleep_uq.models.seqsleepnet_class import SeqSleepNetClass,count_trainable_parameters
from shiftsleep_uq.remediation.datasets import RemediationManifestDataset
from shiftsleep_uq.training.datasets import source_dataset_for_experiment
from shiftsleep_uq.training.reproducibility import seed_everything
from shiftsleep_uq.evaluation_step11 import macro_f1,nll,softmax
ROOT=Path(__file__).resolve().parents[1];PHASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b';EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];VARS=['S0','S1'];SEEDS=[17,42,2026];CONDS=['C0','C1','C2','C3','C4','C5'];EXPOSURE_SEED=2029

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
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
  with np.load(p,allow_pickle=False) as z:phys=z['source_epoch_indices'].astype(int);labels=z['labels'].astype(int)
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
 def __init__(self,ds,normalization,stride):self.refs=refs(ds,stride);self.norm=normalization;self.cache={};self.ds=ds
 def __len__(self):return len(self.refs)
 def __getitem__(self,i):
  p,rows,s,r,start=self.refs[i]
  if p not in self.cache:
   with np.load(p,allow_pickle=False) as z:self.cache[p]={'spec':spec_recording(z['eeg'],z['eog']),'labels':z['labels'],'phys':z['source_epoch_indices']}
  a=self.cache[p];x=a['spec'][list(rows)].astype(np.float32);mean=np.asarray(self.norm['mean'],np.float32)[:,:,None];std=np.asarray(self.norm['std'],np.float32)[:,:,None];x=(x-mean)/std
  return {'x':torch.from_numpy(x),'y':torch.tensor(a['labels'][list(rows)],dtype=torch.long),'subject_id':s,'recording_id':r,'start_index':start,'ref_index':i}

def fit_norm(ds):
 total=np.zeros((2,129),np.float64);sq=np.zeros_like(total);n=0;seen=set()
 for p,row,s,r,m in ds.records:
  if p in seen:continue
  seen.add(p)
  with np.load(p,allow_pickle=False) as z:eeg=z['eeg'];eog=z['eog']
  z=spec_recording(eeg,eog).astype(np.float64);total+=z.sum((0,3));sq+=(z*z).sum((0,3));n+=z.shape[0]*z.shape[3]
 mean=total/n;std=np.maximum(np.sqrt(np.maximum(sq/n-mean*mean,0)),1e-6);return {'scope':'SOURCE_TRAIN_ONLY','count':n,'mean':mean.tolist(),'std':std.tolist()}
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
    m=torch.tensor([mask_for(var,exp,seed,epoch,s,r,st) for s,r,st in zip(b['subject_id'],b['recording_id'],b['start_index'])],dtype=torch.float32,device=device);z=model(b['x'].to(device),m);loss=nn.CrossEntropyLoss()(z.reshape(-1,5),b['y'].to(device).reshape(-1));opt.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step();total+=float(loss)*len(b['y']);n+=len(b['y'])
   q=eval_model(model,dv,device,exp,var,seed,epoch);f=macro_f1(softmax(q['logits']).argmax(1),q['labels']);nv=nll(softmax(q['logits']),q['labels']);hist.append({'epoch':epoch,'dev_macro_f1':f,'dev_nll':nv,'train_loss':total/n});
   if best is None or (f>best['f'] or (f==best['f'] and (nv<best['n'] or (nv==best['n'] and epoch<best['e'])))):best={'f':f,'n':nv,'e':epoch};torch.save({'model_state_dict':model.state_dict(),'metadata':{'job_id':jid,'best_epoch':epoch,'init_hash':ih,'normalization_sha256':sha(d/'normalization.json')}},d/'best.pt')
  manifest={'job_id':jid,'status':'COMPLETE','best_epoch':best['e'],'dev_macro_f1':best['f'],'dev_nll':best['n'],'checkpoint_sha256':sha(d/'best.pt'),'normalization_sha256':sha(d/'normalization.json'),'initialization_sha256':ih,'protocol_sha256':PHASH,'wall_clock_seconds':time.time()-start};(d/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(d/'training_history.json').write_text(json.dumps(hist,indent=2)+'\n');(d/'completion_marker.json').write_text(json.dumps({'status':'COMPLETE'})+'\n');return manifest
 except Exception as e:
  (d/'failure.json').write_text(json.dumps({'status':'FAILED','error':repr(e),'traceback':traceback.format_exc()},indent=2)+'\n');return {'job_id':jid,'status':'FAILED','error':repr(e)}
def main():
 if sha(ROOT/'configs/postreview_remediation_protocol_v2.yaml')!=PHASH:raise RuntimeError('R3_PROTOCOL_HASH_FAILURE')
 rows=[]
 for exp in EXPS:
  source=source_dataset_for_experiment(exp);train=RemediationManifestDataset(source,'TRAIN','train',root=ROOT);dev=RemediationManifestDataset(source,'DEV','dev',root=ROOT);norm=fit_norm(train);nd=ROOT/'artifacts/remediation/normalization/r3';nd.mkdir(parents=True,exist_ok=True);(nd/f'{exp}.json').write_text(json.dumps(norm,sort_keys=True)+'\n')
  train.records=[(p if train.dataset!='sleep_edf_sc' else ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'/p.name,i,s,r,m) for p,i,s,r,m in train.records];dev.records=[(p if dev.dataset!='sleep_edf_sc' else ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'/p.name,i,s,r,m) for p,i,s,r,m in dev.records]
  for var in VARS:
   for seed in SEEDS:print(json.dumps({'start':exp,var:var,'seed':seed}),flush=True);rows.append(train_job(exp,var,seed,train,dev,norm));print(json.dumps(rows[-1]),flush=True)
 with (ROOT/'reports/remediation/r3_checkpoint_manifest_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
 print(json.dumps({'jobs':len(rows),'complete':sum(r.get('status')=='COMPLETE' for r in rows),'failed':sum(r.get('status')=='FAILED' for r in rows)}))
if __name__=='__main__':main()
