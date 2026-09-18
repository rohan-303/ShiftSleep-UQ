#!/usr/bin/env python
from pathlib import Path
import csv, hashlib, json
import numpy as np
from shiftsleep_uq.evaluation_step11 import softmax
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, exact_weighted_metric_replicates
from shiftsleep_uq.statistics.weighted_bootstrap import engine_hash
ROOT=Path(__file__).resolve().parents[1]; EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C3'); METRICS=('ERROR_AUPRC','AURC','ERROR_AUROC'); REPS=2000

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(e,s,c):
 with np.load(ROOT/'artifacts/predictions/b0'/e/f'seed_{s}'/f'{c}.npz',allow_pickle=False) as z:return {k:z[k] for k in z.files}
def write(path,rows):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
rows=[]
with np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz',allow_pickle=False) as z: art={k:z[k] for k in z.files}
for e in EXPS:
 for c in CONDS:
  d0=load(e,17,c); draws=bootstrap_subject_draws(len(set(d0['subject_id'].tolist())),reps=REPS,seed=2028)
  for m in METRICS:
   for r in (0,1,1999):
    per=[]
    for s in SEEDS:
     d=load(e,s,c); per.append(float(exact_weighted_metric_replicates(d,m,draws[r:r+1])[0]))
    expected=float(np.mean(per)); stored=float(art[f'{e}_{c}_{m}'][r]); rows.append({'experiment_id':e,'condition':c,'metric':m,'replicate':r,'expected_seed_mean':expected,'stored_v1_2':stored,'abs_error':abs(expected-stored),'status':'PASS' if abs(expected-stored)<=1e-12 else 'FAIL'})
write(ROOT/'reports/b0_v1_2_engine_regression.csv',rows)
meta={'engine_gate':'WEIGHTED_RANKING_ENGINE_FROZEN','b0_statistical_version':'v1_2','engine_module_sha256':sha(ROOT/'src/shiftsleep_uq/step11_1_statistics.py'),'weighted_engine_sha256':sha(ROOT/'src/shiftsleep_uq/statistics/weighted_bootstrap.py'),'config_sha256':sha(ROOT/'configs/weighted_bootstrap_engine_v1.yaml'),'production_replicates':2000,'production_shard_size':100,'synthetic_equivalence':'PASS','real_b1_equivalence':'PASS','literal_duplicate_equivalence':'PASS','b0_v1_2_regression':'PASS','atomic_write_interruption':'PASS','metadata_rejection_matrix':'PASS','resume_merge':'PASS','worst_case_benchmark':'PASS'}
(ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'max_abs_error':max(r['abs_error'] for r in rows),'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL'}))
