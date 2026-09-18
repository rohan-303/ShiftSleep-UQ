from pathlib import Path
import sys,csv,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax,entropy
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates,_metric,bootstrap_subject_draws
from shiftsleep_uq.statistics.weighted_bootstrap import prepare,ranking
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF');CONDS=('C1','C2','C4','C5');METRICS=('ERROR_AUROC','ERROR_AUPRC','AURC')
def load(e,c):
 with np.load(ROOT/'artifacts/predictions/b0'/e/'seed_17'/f'{c}.npz',allow_pickle=False) as z:return {k:z[k] for k in z.files}
rows=[]
with np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz',allow_pickle=False) as z: a={k:z[k] for k in z.files}
for e in EXPS:
 for c in CONDS:
  d=load(e,c); n=len(set(d['subject_id'].tolist()));draw=bootstrap_subject_draws(n,reps=2000,seed=2028)[0];m=np.bincount(draw,minlength=n);p=softmax(d['logits']);pre=prepare(d['labels'],p,d['subject_id'],entropy(p));
  idx=np.concatenate([np.flatnonzero(d['subject_id']==sorted(set(d['subject_id'].tolist()))[int(i)]) for i in draw]);lb={k:v[idx] for k,v in d.items() if isinstance(v,np.ndarray) and len(v)==len(d['labels'])}
  for metric in METRICS:
   h=float(weighted_metric_replicates(d,metric,draw[None,:])[0]);l=float(_metric(lb,metric));x=float(ranking(pre,m)[metric]);rows.append({'experiment_id':e,'condition':c,'seed':17,'replicate':0,'metric':metric,'H_historical':h,'L_literal':l,'E_exact':x,'H_minus_L':h-l,'L_minus_E':l-x,'A_artifact_seed_aggregate':float(a[f'{e}_{c}_{metric}'][0])})
with open(ROOT/'reports/step15_2_2_b0_other_condition_spot_checks.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('rows',len(rows))
