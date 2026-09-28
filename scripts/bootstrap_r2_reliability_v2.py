from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from shiftsleep_uq.evaluation_step11 import _rank_auc, auprc, aurc, entropy, nll, softmax

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/remediation/r2';R=ROOT/'reports/remediation';EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];SEEDS=[17,42,2026];CELLS=[('D1_SLEEPEDF_TO_ISRUC','C4'),('D1_SLEEPEDF_TO_ISRUC','C5'),('D2_ISRUC_TO_SLEEPEDF','C4'),('D2_ISRUC_TO_SLEEPEDF','C5')];METRICS=['NLL','ERROR_AUROC','ERROR_AUPRC','AURC'];B=2000

def bundle(exp,var,seed,cond):
 p=next((A/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'predictions'/f'{cond}.npz' for _ in [0] if (A/f'R2_{exp}_{var}_SEED_{seed}'/'ATTEMPT_001'/'predictions'/f'{cond}.npz').exists()),None)
 if p is None: raise FileNotFoundError((exp,var,seed,cond))
 z=np.load(p,allow_pickle=False);return {k:z[k] for k in z.files}
def metric(name,z):
 p=softmax(z['logits']);y=z['labels'];pred=p.argmax(1);u=entropy(p);err=(pred!=y).astype(int)
 return {'NLL':nll(p,y),'ERROR_AUROC':_rank_auc(u,err),'ERROR_AUPRC':auprc(u,err),'AURC':aurc(u,pred,y)}[name]
def grouped(z):
 out={}
 for s in np.unique(z['subject_id']):
  idx=np.flatnonzero(z['subject_id']==s);out[str(s)]=idx
 return out
def resample_metric(name,z,groups,draw):
 idx=np.concatenate([groups[s] for s in draw]);return metric(name,{k:v[idx] for k,v in z.items()})
def main():
 rows=[]
 for exp,cond in CELLS:
  point={m:[] for m in METRICS};bs={m:np.empty(B) for m in METRICS};rng=np.random.default_rng(2028)
  for seed in SEEDS:
   b0=bundle(exp,'B0_W',seed,cond);b1=bundle(exp,'B1_W',seed,cond);keys0={(str(s),str(r),int(e)) for s,r,e in zip(b0['subject_id'],b0['recording_id'],b0['epoch_index'])};keys1={(str(s),str(r),int(e)) for s,r,e in zip(b1['subject_id'],b1['recording_id'],b1['epoch_index'])}
   if keys0!=keys1:raise RuntimeError(f'R2_PAIR_IDENTITY_MISMATCH {exp} {cond} {seed}')
   g0=grouped(b0);g1=grouped(b1);subjects=sorted(set(g0)&set(g1));draws=rng.choice(subjects,size=(B,len(subjects)),replace=True)
   for m in METRICS:
    point[m].append(metric(m,b1)-metric(m,b0))
    for i,draw in enumerate(draws):bs[m][i]+=resample_metric(m,b1,g1,draw)-resample_metric(m,b0,g0,draw)
  for m in METRICS:
   bs[m]/=len(SEEDS);hat=float(np.mean(point[m]));lo,hi=np.percentile(bs[m],[2.5,97.5]);p=(1+np.count_nonzero(np.abs(bs[m]-hat)>=abs(hat)))/(B+1);rows.append({'experiment':exp,'condition':cond,'metric':m,'effect':hat,'ci_lower':float(lo),'ci_upper':float(hi),'p_value_null_centered':float(p),'replicates':B,'bootstrap_seed':2028,'subjects':len(subjects),'seed_effects':','.join(str(x) for x in point[m])})
 out=R/'r2_reliability_paired_v2.csv';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print({'rows':len(rows),'replicates':B,'cells':len(CELLS),'metrics':len(METRICS)})
if __name__=='__main__':main()
