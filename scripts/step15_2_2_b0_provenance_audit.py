#!/usr/bin/env python
"""Step 15.2.2 forensic comparison of historical and exact B0 ranking paths."""
from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax, entropy, _rank_auc, auprc, aurc, macro_f1, nll, brier
from shiftsleep_uq.step11_1_statistics import (_metric, weighted_metric_replicates, bootstrap_subject_draws)
from shiftsleep_uq.statistics.weighted_bootstrap import prepare, literal, ranking, weighted_confusion, confusion_metrics
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,); CONDS=('C0','C1','C2','C3','C4','C5'); METRICS=('ERROR_AUROC','ERROR_AUPRC','AURC')

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(1<<20),b''): h.update(x)
 return h.hexdigest()

def load(ex,seed,cond):
 p=ROOT/'artifacts/predictions/b0'/ex/f'seed_{seed}'/f'{cond}.npz'
 with np.load(p,allow_pickle=False) as z: return {k:z[k] for k in z.files}

def bundle(d): return {'subject_id':d['subject_id'],'labels':d['labels'],'logits':d['logits']}

def values(d, sampled):
 b=bundle(d); subjects=sorted(set(b['subject_id'].tolist())); m=np.bincount(sampled,minlength=len(subjects)).astype(np.int64)
 probs=softmax(b['logits']); pre=prepare(b['labels'],probs,b['subject_id'],entropy(probs))
 h={}; l={}; e={}
 idx=np.concatenate([np.flatnonzero(b['subject_id']==subjects[int(i)]) for i in sampled])
 lb={k:np.asarray(v)[idx] for k,v in b.items()}
 for metric in METRICS:
  h[metric]=float(weighted_metric_replicates(b,metric,np.asarray([sampled]))[0])
  l[metric]=float(_metric(lb,metric))
  e[metric]=float(ranking(pre,m)[metric])
 return h,l,e,m

def csv_write(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True)
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
 # Immutable preflight hashes.
 hash_rows=[]
 for rel in ['reports/b0_statistical_hashes_v1_1.txt','reports/b0_primary_prediction_hashes_v1.txt','artifacts/statistics/b0/bootstrap_replicates_v1_1.npz']:
  p=ROOT/rel; hash_rows.append({'path':rel,'sha256':sha(p),'exists':p.exists()})
 with np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz',allow_pickle=False) as z: artifact={k:z[k] for k in z.files}
 rows=[]
 specs=[('D1_SLEEPEDF_TO_ISRUC','C0',range(20)),('D1_SLEEPEDF_TO_ISRUC','C3',range(10)),('D2_ISRUC_TO_SLEEPEDF','C0',range(20)),('D2_ISRUC_TO_SLEEPEDF','C3',range(10))]
 for ex,cond,inds in specs:
  pop_n=len(set(load(ex,17,cond)['subject_id'].tolist())); draws=bootstrap_subject_draws(pop_n,reps=2000,seed=2028)
  for seed in SEEDS:
   d=load(ex,seed,cond); keybase=f'{ex}_{cond}'
   for r in inds:
    h,l,e,m=values(d,draws[r]);
    for metric in METRICS:
     a=float(artifact[f'{keybase}_{metric}'][r])
     rows.append({'experiment_id':ex,'condition':cond,'seed':seed,'replicate':r,'metric':metric,'draw_sha256':hashlib.sha256(np.asarray(draws[r],dtype=np.int64).tobytes()).hexdigest(),'subject_count':pop_n,'H_historical':h[metric],'L_literal':l[metric],'E_exact':e[metric],'A_artifact':a,'H_minus_L':h[metric]-l[metric],'L_minus_E':l[metric]-e[metric],'H_minus_A':h[metric]-a,'status':'PASS' if max(abs(h[metric]-a),abs(l[metric]-e[metric]))<=1e-10 else 'FAIL'})
 csv_write(ROOT/'reports/step15_2_2_b0_ranking_forensic_matrix.csv',rows)
 # Small, human-readable [A,A,C] control.
 probs=np.array([[.99,.0025,.0025,.0025,.0025],[.0025,.99,.0025,.0025,.0025],[.0025,.0025,.99,.0025,.0025]])
 syn={'subject_id':np.array(['A','B','C']),'labels':np.array([1,0,2]),'logits':np.log(probs)}; sampled=np.array([0,0,2]); h,l,e,m=values(syn,sampled)
 synrows=[]
 for metric in METRICS: synrows.append({'metric':metric,'observations':'A,B,C','sampled_subjects':'A,A,C','multiplicities':'[2,0,1]','H_historical':h[metric],'L_literal':l[metric],'E_exact':e[metric]})
 csv_write(ROOT/'reports/step15_2_2_b0_synthetic_counterexamples.csv',synrows)
 # Point identity audit on all bundles: historical point, literal identity, exact identity.
 points=[]
 for ex in EXPS:
  for seed in SEEDS:
   for cond in CONDS:
    d=load(ex,seed,cond); b=bundle(d); subjects=sorted(set(d['subject_id'].tolist())); m=np.ones(len(subjects),dtype=np.int64); p=softmax(d['logits']); pre=prepare(d['labels'],p,d['subject_id'],entropy(p));
    idx=np.arange(len(d['labels']))
    for metric in METRICS:
     hv=float(_metric(b,metric)); ev=float(ranking(pre,m)[metric]); points.append({'experiment_id':ex,'seed':seed,'condition':cond,'metric':metric,'historical_point':hv,'exact_identity':ev,'difference':hv-ev})
 csv_write(ROOT/'reports/step15_2_2_b0_point_identity_audit.csv',points)
 # Dependency map is deliberately derived from the written Step 11.1 writer.
 dep=[]
 for art,metric,field,affected,down in [
 ('reports/b0_primary_results_multiseed_v1_1.csv','ERROR_AUPRC','ci95_low/high',True,'future B0/B1 comparison'),('reports/b0_primary_results_multiseed_v1_1.csv','AURC','ci95_low/high',True,'future B0/B1 comparison'),('reports/b0_primary_results_multiseed_v1_1.csv','ERROR_AUPRC','point_estimate',False,'future B0/B1 comparison'),('reports/b0_primary_results_multiseed_v1_1.csv','AURC','point_estimate',False,'future B0/B1 comparison'),('reports/b0_primary_contrasts_v1_1.csv','AUPRC/AURC','contrast CI fields',True,'Step 12.1 downstream audit')]:
  dep.append({'artifact':art,'table_field':field,'metric':metric,'uses_point':not affected,'uses_bootstrap':affected,'potentially_affected':affected,'downstream_step':down})
 csv_write(ROOT/'reports/step15_2_2_b0_ranking_dependency_map.csv',dep)
 (ROOT/'reports/step15_2_2_b0_preflight_hashes.json').write_text(json.dumps(hash_rows,indent=2)+'\n')
 print(json.dumps({'forensic_rows':len(rows),'synthetic_rows':len(synrows),'point_rows':len(points),'hashes':hash_rows},indent=2))
if __name__=='__main__': main()
