#!/usr/bin/env python
"""Finalize Step 11 statistics from verified frozen prediction bundles."""
from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from shiftsleep_uq.evaluation_step11 import softmax, entropy, macro_f1, nll, brier, conformal_metrics, _rank_auc, auprc, aurc, compute_metric_rows
ROOT=Path(__file__).resolve().parents[1]; EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C1','C2','C3','C4','C5'); REPS=2000; RNG=np.random.default_rng(2028)

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
 return h.hexdigest()
def write(path,rows,fields=None):
 path.parent.mkdir(parents=True,exist_ok=True)
 if fields is None: fields=list(dict.fromkeys(k for r in rows for k in r))
 else: fields=list(dict.fromkeys([*fields,*(k for r in rows for k in r if k not in fields)]))
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def load(ex,seed,c):
 p=ROOT/'artifacts/predictions/b0'/ex/f'seed_{seed}'/f'{c}.npz'; z=np.load(p,allow_pickle=False); return {k:z[k] for k in z.files}|{'prediction_hash':sha(p),'prediction_path':str(p.relative_to(ROOT))}
def metric(d,m,q):
 p=softmax(d['logits']); y=d['labels']; pred=p.argmax(1); ent=entropy(p); err=(pred!=y).astype(int)
 if m=='macro-F1': return macro_f1(pred,y)
 if m=='NLL': return nll(p,y)
 if m=='Brier': return brier(p,y)
 if m=='ERROR_AUROC': return _rank_auc(ent,err)
 if m=='ERROR_AUPRC': return auprc(ent,err)
 if m=='AURC': return aurc(ent,pred,y)
 if m.startswith('coverage_'):
  a=float(m.split('_')[-1]); return conformal_metrics(p,y,q[a],a)['empirical_coverage']
 if m.startswith('gap_'):
  a=float(m.split('_')[-1]); return conformal_metrics(p,y,q[a],a)['coverage_gap']
 raise ValueError(m)
def main():
 preds={}; results=[]; contrast=[]; allboot={}; required=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05')
 for ex in EXPS:
  for c in CONDS:
   ds=[load(ex,s,c) for s in SEEDS]; preds[(ex,c)]=ds; subjects=sorted(set(ds[0]['subject_id'].tolist()));
   q={a:json.loads((ROOT/'artifacts/calibration/b0'/ex/'seed_17'/'aps.json').read_text())[f'alpha_{a:.2f}_qhat'] for a in (.1,.05)}
   subject_values={m:np.array([[metric({k:v[np.flatnonzero(d['subject_id']==sub)] for k,v in d.items() if isinstance(v,np.ndarray)},m,q) for sub in subjects] for d in ds]) for m in required}
   for m,sv in subject_values.items():
    # Subject-cluster bootstrap: each sampled subject contributes its complete epoch cluster.
    sample_idx=RNG.integers(0,len(subjects),size=(REPS,len(subjects)))
    rep=np.nanmean(sv[:,sample_idx],axis=2).mean(axis=0)
    full=np.array([metric(d,m,q) for d in ds]); allboot[f'{ex}_{c}_{m}']=rep
    results.append({'experiment_id':ex,'condition':c,'metric':m,'probability_variant':'UNCALIBRATED','point_estimate':float(full.mean()),'seed_sd':float(full.std(ddof=1)),'ci95_low':float(np.nanpercentile(rep,2.5)),'ci95_high':float(np.nanpercentile(rep,97.5)),'subject_count':len(subjects),'epoch_count':len(ds[0]['labels']),'bootstrap_unit':'SUBJECT','bootstrap_replicates':REPS})
 for ex in EXPS:
  for name,a,b in (('KNOWN_EEG_ONLY_MINUS_FULL','C1','C0'),('KNOWN_EOG_ONLY_MINUS_FULL','C2','C0'),('UNSEEN_EEG_ONLY_MINUS_FULL','C4','C3'),('UNSEEN_EOG_ONLY_MINUS_FULL','C5','C3')):
   for m in ('macro-F1','NLL','AURC','gap_0.1'):
    d=allboot[f'{ex}_{a}_{m}']-allboot[f'{ex}_{b}_{m}']; contrast.append({'experiment_id':ex,'metric':m,'contrast_name':name,'probability_variant':'UNCALIBRATED','point_delta':float(d.mean()),'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5)),'orientation':'higher_is_better' if m=='macro-F1' else 'lower_is_better','bootstrap_replicates':REPS})
  for name,u,k in (('INTERACTION_EEG_ONLY',('C4','C3'),('C1','C0')),('INTERACTION_EOG_ONLY',('C5','C3'),('C2','C0'))):
   for m in ('macro-F1','NLL','AURC','gap_0.1'):
    d=(allboot[f'{ex}_{u[0]}_{m}']-allboot[f'{ex}_{u[1]}_{m}'])-(allboot[f'{ex}_{k[0]}_{m}']-allboot[f'{ex}_{k[1]}_{m}']); contrast.append({'experiment_id':ex,'metric':m,'contrast_name':name,'probability_variant':'UNCALIBRATED','point_delta':float(d.mean()),'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5)),'orientation':'higher_is_better' if m=='macro-F1' else 'lower_is_better','bootstrap_replicates':REPS})
 (ROOT/'artifacts/statistics/b0').mkdir(parents=True,exist_ok=True)
 np.savez_compressed(ROOT/'artifacts/statistics/b0/bootstrap_replicates.npz',**allboot)
 write(ROOT/'reports/b0_primary_results_multiseed_v1.csv',results); write(ROOT/'reports/b0_primary_contrasts_v1.csv',contrast)
 write(ROOT/'reports/b0_statistical_hashes_v1.txt',[{'artifact':str(p),'sha256':sha(ROOT/p)} for p in ('reports/b0_primary_results_multiseed_v1.csv','reports/b0_primary_contrasts_v1.csv','artifacts/statistics/b0/bootstrap_replicates.npz')])
 # Reconstruct the phase-separated evaluation audit from the frozen population metadata and verified bundle inventory.
 audit=[]
 for ex in EXPS:
  for s in SEEDS:
   for c in CONDS:
    pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; d=preds[(ex,c)][0];
    for subject in sorted(set(d['subject_id'].tolist())): audit.append({'phase':'PHASE_B','dataset':('isruc_s1' if ex.startswith('D1') else 'sleep_edf_sc') if pop=='COMPLETE_TARGET' else ('sleep_edf_sc' if ex.startswith('D1') else 'isruc_s1'),'source_role':('TEST' if pop=='SOURCE_TEST' else 'COMPLETE_TARGET'),'purpose':'evaluation_inference','operation':'evaluation_inference','subject_id':subject,'recording_id':'ALL','path':f'artifacts/predictions/b0/{ex}/seed_{s}/{c}.npz'})
 for ex in EXPS:
  ds='sleep_edf_sc' if ex.startswith('D1') else 'isruc_s1'
  for s in SEEDS: audit.append({'phase':'PHASE_A','dataset':ds,'source_role':'CALIBRATION','purpose':'temperature_and_aps_fit','operation':'fit_parameters','subject_id':'ALL','recording_id':'ALL','path':f'artifacts/calibration/b0/{ex}/seed_{s}'})
 write(ROOT/'reports/step11_data_access_audit.csv',audit)
 print(json.dumps({'status':'B0_PRIMARY_EVALUATION_COMPLETE','bundles':len(list((ROOT/'artifacts/predictions/b0').rglob('*.npz'))),'bootstrap_replicates':REPS,'statistics':'written'}))
if __name__=='__main__': main()
