from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import numpy as np,torch
from torch.utils.data import DataLoader
from sklearn.metrics import cohen_kappa_score,balanced_accuracy_score
from shiftsleep_uq.models.baseline_b0 import BaselineB0,condition_mask
from shiftsleep_uq.evaluation_step11 import softmax,macro_f1,nll,fit_temperature,aps_scores,aps_quantile
from shiftsleep_uq.remediation.datasets import build_overlay_dataset,build_overlay_evaluation_dataset
ROOT=Path(__file__).resolve().parents[1];PHASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b';EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];SEEDS=[17,42,2026];VARS=['B0_W','B1_W'];CONDS=['C0','C1','C2','C3','C4','C5']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load_model(exp,var,seed,device):
 p=ROOT/'artifacts/remediation/r2'/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'best.pt';z=torch.load(p,map_location=device,weights_only=False);m=BaselineB0().to(device).float();m.load_state_dict(z['model_state_dict']);m.eval();return m,sha(p)
def predict(m,ds,cond,device):
 out=[];lab=[];sub=[];rec=[];epoch=[];loader=DataLoader(ds,batch_size=128,shuffle=False,num_workers=0,pin_memory=True)
 with torch.no_grad():
  for b in loader:
   n=len(b['label']);mask=torch.tensor(condition_mask(cond),dtype=torch.float32,device=device).expand(n,-1);out.append(m(b['eeg'].to(device),b['eog'].to(device),mask).cpu().numpy());lab.append(b['label'].numpy());sub.extend(b['subject_id']);rec.extend(b['recording_id']);epoch.extend(b['epoch_index'].numpy().tolist())
 return {'logits':np.concatenate(out).astype(np.float32),'labels':np.concatenate(lab).astype(np.int64),'subject_id':np.asarray(sub),'recording_id':np.asarray(rec),'epoch_index':np.asarray(epoch,dtype=np.int64)}
def bootstrap_effect(a,b,reps=2000):
 subjects=np.asarray(sorted(set(a['subject_id'].tolist())&set(b['subject_id'].tolist())));mapsa={s:np.flatnonzero(a['subject_id']==s) for s in subjects};mapsb={s:np.flatnonzero(b['subject_id']==s) for s in subjects};rng=np.random.default_rng(2028);v=np.empty(reps)
 for r in range(reps):
  pick=rng.choice(len(subjects),len(subjects),replace=True);ia=np.concatenate([mapsa[subjects[i]] for i in pick]);ib=np.concatenate([mapsb[subjects[i]] for i in pick]);v[r]=macro_f1(softmax(b['logits'][ib]).argmax(1),b['labels'][ib])-macro_f1(softmax(a['logits'][ia]).argmax(1),a['labels'][ia])
 return v
def main():
 if sha(ROOT/'configs/postreview_remediation_protocol_v2.yaml')!=PHASH:raise RuntimeError('R2 eval protocol mismatch')
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu');pred={};cal={};rows=[]
 for exp in EXPS:
  norm=json.loads((ROOT/'artifacts/remediation/normalization/r2'/f'{exp}.json').read_text());calds=build_overlay_dataset(exp,'CALIBRATION','calibration',windowed=True);calds.set_normalization(norm);test=build_overlay_evaluation_dataset(exp,'SOURCE_TEST',windowed=True);target=build_overlay_evaluation_dataset(exp,'COMPLETE_TARGET',windowed=True);test.set_normalization(norm);target.set_normalization(norm)
  for seed in SEEDS:
   m,_=load_model(exp,'B0_W',seed,device);c=predict(m,calds,'C0',device);t=fit_temperature(c['logits'],c['labels'],role='CALIBRATION');q={a:aps_quantile(aps_scores(softmax(c['logits']),c['labels']),a) for a in [.1,.05]};cal[(exp,seed)]={'temperature':t['temperature'],'q':q};
   for var in VARS:
    m,ch=load_model(exp,var,seed,device)
    for cond in CONDS:
     ds=test if cond in {'C0','C1','C2'} else target;d=predict(m,ds,cond,device);path=ROOT/'artifacts/remediation/r2'/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'predictions'/f'{cond}.npz';path.parent.mkdir(exist_ok=True);np.savez_compressed(path,**d);pred[(exp,var,seed,cond)]=d
     p=softmax(d['logits']);pr=p.argmax(1);cm=np.bincount(d['labels']*5+pr,minlength=25).reshape(5,5);rows.append({'experiment':exp,'variant':var,'seed':seed,'condition':cond,'population':'SOURCE_TEST' if cond in {'C0','C1','C2'} else 'COMPLETE_TARGET','prediction_sha256':sha(path),'macro_f1':macro_f1(pr,d['labels']),'kappa':cohen_kappa_score(d['labels'],pr),'balanced_accuracy':balanced_accuracy_score(d['labels'],pr),'nll':nll(p,d['labels']),'temperature':cal[(exp,seed)]['temperature'],'aps_q_0.10':cal[(exp,seed)]['q'][.1],'aps_q_0.05':cal[(exp,seed)]['q'][.05],'epoch_count':len(d['labels']),'subject_count':len(set(d['subject_id']))})
 with (ROOT/'reports/remediation/r2_primary_results_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 effects=[];bootrows=[]
 for exp in EXPS:
  for cond in ['C4','C5']:
   vals=[];boots=[]
   for seed in SEEDS:
    a=pred[(exp,'B0_W',seed,cond)];b=pred[(exp,'B1_W',seed,cond)];vals.append(float(macro_f1(softmax(b['logits']).argmax(1),b['labels'])-macro_f1(softmax(a['logits']).argmax(1),a['labels'])));boots.append(bootstrap_effect(a,b))
   bv=np.mean(np.stack(boots),axis=0);hat=float(np.mean(vals));effects.append({'experiment':exp,'condition':cond,'effect_B1W_minus_B0W':hat,'ci_low':float(np.quantile(bv,.025)),'ci_high':float(np.quantile(bv,.975)),'p_unadjusted':float((1+np.sum(np.abs(bv)>=abs(hat)))/2001),'seed_effects':json.dumps(vals)});bootrows.append({'experiment':exp,'condition':cond,'bootstrap_replicates':2000,'seed': 'MEAN','effect_hat':hat,'ci_low':float(np.quantile(bv,.025)),'ci_high':float(np.quantile(bv,.975))})
 pvals=sorted((x['p_unadjusted'],i) for i,x in enumerate(effects));adj=[None]*4
 for rank,(p,i) in enumerate(pvals):adj[i]=min(1.,p*(4-rank))
 for i,x in enumerate(effects):x['holm_adjusted_p']=adj[i];x['holm_reject']=bool(adj[i]<.05)
 for name,data in [('r2_paired_results_v1.csv',effects),('r2_bootstrap_summary_v1.csv',bootrows),('r2_holm_v1.csv',effects)]:
  with (ROOT/'reports/remediation'/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 print(json.dumps({'prediction_bundles':len(pred),'primary_effects':effects},indent=2))
if __name__=='__main__':main()
