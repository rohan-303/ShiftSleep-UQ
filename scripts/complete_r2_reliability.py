from __future__ import annotations
import csv,json,hashlib
from pathlib import Path
import numpy as np,torch
from torch.utils.data import DataLoader
from shiftsleep_uq.models.baseline_b0 import BaselineB0,condition_mask
from shiftsleep_uq.evaluation_step11 import softmax,fit_temperature,aps_scores,aps_quantile,compute_metric_rows
from shiftsleep_uq.remediation.datasets import build_overlay_dataset
ROOT=Path(__file__).resolve().parents[1];EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];VARS=['B0_W','B1_W'];SEEDS=[17,42,2026];CONDS=['C0','C1','C2','C3','C4','C5']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(exp,var,seed,device):
 p=ROOT/'artifacts/remediation/r2'/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'best.pt';z=torch.load(p,map_location=device,weights_only=False);m=BaselineB0().to(device).float();m.load_state_dict(z['model_state_dict']);m.eval();return m,sha(p)
def predict(m,ds,cond,device):
 logits=[];labels=[];subjects=[]
 with torch.no_grad():
  for b in DataLoader(ds,batch_size=128,shuffle=False,num_workers=0,pin_memory=True):
   n=len(b['label']);mask=torch.tensor(condition_mask(cond),dtype=torch.float32,device=device).expand(n,-1);logits.append(m(b['eeg'].to(device),b['eog'].to(device),mask).cpu().numpy());labels.append(b['label'].numpy());subjects.extend(b['subject_id'])
 return np.concatenate(logits).astype(np.float32),np.concatenate(labels).astype(np.int64),np.asarray(subjects)
def main():
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu');metrics=[];cal_rows=[];cal={}
 for exp in EXPS:
  norm=json.loads((ROOT/'artifacts/remediation/normalization/r2'/f'{exp}.json').read_text());ds=build_overlay_dataset(exp,'CALIBRATION','calibration',windowed=True);ds.set_normalization(norm)
  for var in VARS:
   for seed in SEEDS:
    m,ch=load(exp,var,seed,device);logits,labels,_=predict(m,ds,'C0',device);before=float(compute_metric_rows(logits,labels,1.,{})[0][0]['value']) if False else None;t=fit_temperature(logits,labels,role='CALIBRATION');q={a:aps_quantile(aps_scores(softmax(logits),labels),a) for a in [.1,.05]};cal[(exp,var,seed)]={'temperature':t['temperature'],'q':q};cal_rows.append({'experiment':exp,'variant':var,'seed':seed,'temperature':t['temperature'],'calibration_NLL_before':t['initial_nll'],'calibration_NLL_after':t['final_nll'],'calibration_count':len(labels),'checkpoint_sha256':ch})
 for exp in EXPS:
  norm=json.loads((ROOT/'artifacts/remediation/normalization/r2'/f'{exp}.json').read_text());test=build_overlay_dataset(exp,'TEST','evaluation_test',windowed=True);target='isruc_s1' if exp=='D1_SLEEPEDF_TO_ISRUC' else 'sleep_edf_sc'
  # evaluation bundles already contain canonical target/source rows; consume them without rerunning inference.
  for var in VARS:
   for seed in SEEDS:
    for cond in CONDS:
     pop='SOURCE_TEST' if cond in {'C0','C1','C2'} else 'COMPLETE_TARGET';p=ROOT/'artifacts/remediation/r2'/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'predictions'/f'{cond}.npz'
     with np.load(p,allow_pickle=False) as z:logits=z['logits'];labels=z['labels']
     t=cal[(exp,var,seed)];rows,_=compute_metric_rows(logits,labels,t['temperature'],t['q'])
     for r in rows:metrics.append({'experiment':exp,'variant':var,'seed':seed,'condition':cond,'population':pop,**r,'prediction_sha256':sha(p)})
 fields=list(cal_rows[0]);
 with (ROOT/'reports/remediation/r2_temperature_calibration_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(cal_rows)
 with (ROOT/'reports/remediation/r2_reliability_results_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in metrics for k in r)));w.writeheader();w.writerows(metrics)
 print(json.dumps({'calibration_groups':len(cal_rows),'metric_rows':len(metrics),'bundles':len(EXPS)*len(VARS)*len(SEEDS)*len(CONDS)}))
if __name__=='__main__':main()
