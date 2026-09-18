#!/usr/bin/env python
from pathlib import Path
import sys,csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax,entropy
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates,bootstrap_subject_draws
from shiftsleep_uq.statistics.weighted_bootstrap import prepare,ranking
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C3'); METRICS=('ERROR_AUROC','ERROR_AUPRC','AURC')
def load(ex,s,c):
 with np.load(ROOT/'artifacts/predictions/b0'/ex/f'seed_{s}'/f'{c}.npz',allow_pickle=False) as z:return {k:z[k] for k in z.files}
rows=[]
with np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz',allow_pickle=False) as z: art={k:z[k] for k in z.files}
for ex in EXPS:
 for c in CONDS:
  d0=load(ex,17,c); n=len(set(d0['subject_id'].tolist())); draws=bootstrap_subject_draws(n,reps=2000,seed=2028)
  for r in range(3):
   vals={m:[] for m in METRICS}
   for s in SEEDS:
    d=load(ex,s,c)
    hs=[weighted_metric_replicates(d,m,draws[r:r+1])[0] for m in METRICS]
    for m,v in zip(METRICS,hs): vals[m].append(float(v))
   for m in METRICS:
    mean=float(np.mean(vals[m])); a=float(art[f'{ex}_{c}_{m}'][r]); rows.append({'experiment_id':ex,'condition':c,'replicate':r,'metric':m,'H_seed17':vals[m][0],'H_seed42':vals[m][1],'H_seed2026':vals[m][2],'H_mean':mean,'A_artifact':a,'H_mean_minus_A':mean-a})
with open(ROOT/'reports/step15_2_2_b0_seed_aggregation_alignment.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('rows',len(rows))
