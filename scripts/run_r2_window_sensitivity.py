from __future__ import annotations
import csv,hashlib,json,platform,subprocess,time,traceback
from pathlib import Path
import numpy as np,torch
from torch import nn
from torch.utils.data import DataLoader
from shiftsleep_uq.models.baseline_b0 import BaselineB0,CLASS_ORDER,count_trainable_parameters
from shiftsleep_uq.training.checkpointing import CheckpointSelector
from shiftsleep_uq.training.modality_exposure import assign_masks,apply_missing_modality_zeroing
from shiftsleep_uq.training.reproducibility import seed_everything,make_epoch_generator
from shiftsleep_uq.evaluation_step11 import macro_f1,nll,softmax
from shiftsleep_uq.remediation.datasets import build_overlay_dataset,fit_windowed_normalization
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'src';PROTO=ROOT/'configs/postreview_remediation_protocol_v2.yaml';PHASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b';SEEDS=[17,42,2026];EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];VARS=['B0_W','B1_W'];BATCH=128;EXPOSURE_SEED=2029

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state_hash(model):
 h=hashlib.sha256()
 for k,v in model.state_dict().items():h.update(k.encode());h.update(v.detach().cpu().numpy().tobytes())
 return h.hexdigest()
def keys(batch):return [f"{d}|{s}|{r}|{int(e)}" for d,s,r,e in zip(batch['dataset'],batch['subject_id'],batch['recording_id'],batch['epoch_index'])]
def dev_eval(model,loader,device):
 model.eval();ys=[];ps=[];loss=0.;n=0
 with torch.no_grad():
  for b in loader:
   y=b['label'].to(device);m=torch.ones((len(y),2),device=device);z=model(b['eeg'].to(device),b['eog'].to(device),m);loss+=float(nn.CrossEntropyLoss()(z,y))*len(y);n+=len(y);ys.append(y.cpu().numpy());ps.append(z.cpu().numpy())
 y=np.concatenate(ys);p=np.concatenate(ps);return macro_f1(p.argmax(1),y),loss/n

def train_one(exp,var,seed,train,dev,norm):
 jid=f'R2_{exp}_{var}_SEED_{seed}';d=ROOT/'artifacts/remediation/r2'/jid/'ATTEMPT_001';
 if (d/'completion_marker.json').exists(): return json.loads((d/'run_manifest.json').read_text())
 d.mkdir(parents=True,exist_ok=False);start=time.time();(d/'protocol_hash.txt').write_text(PHASH+'\n');(d/'config_snapshot.json').write_text(json.dumps({'job_id':jid,'experiment':exp,'variant':var,'seed':seed,'batch_size':BATCH,'max_epochs':30,'min_epochs':5,'patience':6,'windowed':True},indent=2)+'\n')
 try:
  if not torch.cuda.is_available():raise RuntimeError('R2_CUDA_UNAVAILABLE')
  device=torch.device('cuda:0');seed_everything(seed);base=BaselineB0().float();init=state_hash(base);model=BaselineB0().to(device).float();model.load_state_dict(base.state_dict());opt=torch.optim.AdamW(model.parameters(),lr=3e-4,weight_decay=1e-4,betas=(.9,.999),eps=1e-8);sel=CheckpointSelector(patience=6,min_epochs=5,tolerance=1e-6);hist=[];train_loader=None;dev_loader=DataLoader(dev,batch_size=BATCH,shuffle=False,num_workers=0,pin_memory=True)
  for epoch in range(1,31):
   train_loader=DataLoader(train,batch_size=BATCH,shuffle=True,generator=make_epoch_generator(seed,epoch),num_workers=0,pin_memory=True);model.train();tot=0.;n=0
   for b in train_loader:
    y=b['label'].to(device)
    if var=='B0_W':m=torch.ones((len(y),2),device=device)
    else:m=torch.tensor(assign_masks(EXPOSURE_SEED,epoch,keys(b)),dtype=torch.float32,device=device)
    eeg,eog=apply_missing_modality_zeroing(b['eeg'].to(device),b['eog'].to(device),m);opt.zero_grad(set_to_none=True);z=model(eeg,eog,m);loss=nn.CrossEntropyLoss()(z,y)
    if not torch.isfinite(loss):raise FloatingPointError('R2 nonfinite loss')
    loss.backward();gn=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step();tot+=float(loss)*len(y);n+=len(y)
   f,nllv=dev_eval(model,dev_loader,device);selected=sel.observe(epoch,f,nllv);hist.append({'epoch':epoch,'train_cross_entropy':tot/n,'dev_macro_f1':f,'dev_nll':nllv,'checkpoint_selected':selected,'gradient_norm':float(gn)})
   if selected:torch.save({'model_state_dict':model.state_dict(),'metadata':{'job_id':jid,'variant':var,'experiment':exp,'seed':seed,'selected_epoch':epoch,'init_hash':init,'normalization_sha256':sha(d/'normalization.json') if (d/'normalization.json').exists() else ''}},d/'best.pt')
   if sel.should_stop(epoch):break
  if sel.best is None:raise RuntimeError('R2 no selected checkpoint')
  (d/'normalization.json').write_text(json.dumps(norm,indent=2,sort_keys=True)+'\n'); best_ck=torch.load(d/'best.pt',map_location='cpu',weights_only=False); best_ck['metadata']['normalization_sha256']=sha(d/'normalization.json');torch.save(best_ck,d/'best.pt')
  # restore selected state from saved best and validate.
  ck=torch.load(d/'best.pt',map_location=device,weights_only=False);check=BaselineB0().to(device).float();check.load_state_dict(ck['model_state_dict']);check.eval();
  with torch.no_grad():z=check(next(iter(dev_loader))['eeg'].to(device),next(iter(dev_loader))['eog'].to(device),torch.ones((min(BATCH,len(dev)),2),device=device))
  if not torch.isfinite(z).all():raise FloatingPointError('R2 reload nonfinite')
  (d/'training_history.csv').write_text('epoch,train_cross_entropy,dev_macro_f1,dev_nll,checkpoint_selected,gradient_norm\n'+'\n'.join(','.join(str(x[k]) for k in ['epoch','train_cross_entropy','dev_macro_f1','dev_nll','checkpoint_selected','gradient_norm']) for x in hist)+'\n')
  manifest={'job_id':jid,'experiment':exp,'variant':var,'seed':seed,'selected_epoch':sel.best['epoch'],'selected_dev_macro_f1':sel.best['macro_f1'],'selected_dev_nll':sel.best['nll'],'epochs_executed':len(hist),'checkpoint_sha256':sha(d/'best.pt'),'normalization_sha256':sha(d/'normalization.json'),'initialization_sha256':init,'protocol_sha256':PHASH,'status':'COMPLETE','wall_clock_seconds':time.time()-start}
  (d/'run_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');(d/'completion_marker.json').write_text(json.dumps({'status':'COMPLETE','job_id':jid})+'\n');return manifest
 except Exception as e:
  (d/'failure.json').write_text(json.dumps({'status':'FAILED','job_id':jid,'error':repr(e),'traceback':traceback.format_exc()},indent=2)+'\n');return {'job_id':jid,'status':'FAILED','error':repr(e)}

def main():
 if sha(PROTO)!=PHASH:raise RuntimeError('R2_PROTOCOL_HASH_FAILURE')
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu');print({'cuda':torch.cuda.is_available(),'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None},flush=True)
 allrows=[]
 for exp in EXPS:
  train=build_overlay_dataset(exp,'TRAIN','train',windowed=True);dev=build_overlay_dataset(exp,'DEV','dev',windowed=True);norm=fit_windowed_normalization(train);nd=ROOT/'artifacts/remediation/normalization/r2';nd.mkdir(parents=True,exist_ok=True);(nd/f'{exp}.json').write_text(json.dumps(norm,indent=2,sort_keys=True)+'\n');train.set_normalization(norm);dev.set_normalization(norm)
  for var in VARS:
   for seed in SEEDS:
    print(json.dumps({'stage':'START','experiment':exp,'variant':var,'seed':seed}),flush=True);row=train_one(exp,var,seed,train,dev,norm);print(json.dumps(row,sort_keys=True),flush=True);allrows.append(row)
 with (ROOT/'reports/remediation/r2_checkpoint_manifest_v1.csv').open('w',newline='') as f:
  fields=list(dict.fromkeys(k for r in allrows for k in r));w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(allrows)
 print(json.dumps({'jobs':len(allrows),'complete':sum(r.get('status')=='COMPLETE' for r in allrows),'failed':sum(r.get('status')=='FAILED' for r in allrows)}))
if __name__=='__main__':main()
