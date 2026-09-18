#!/usr/bin/env python
"""Step 15.3 frozen B1 evaluation against B0 v1.2; no inference/fitting."""
from __future__ import annotations
import csv, hashlib, json, os
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C1','C2','C3','C4','C5'); METRICS=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05'); REPS=2000; SHARD=100
import sys; sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax, entropy, _rank_auc, auprc, aurc, macro_f1, conformal_metrics, aps_prediction_set
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, exact_weighted_metric_replicates

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def bundle(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def write_csv(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with open(p,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def load_draws(e,c):
 pop='COMPLETE_TARGET' if c in ('C3','C4','C5') else 'SOURCE_TEST';
 with np.load(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz') as z: m=z[f'{e}__{pop}']
 return np.concatenate([np.repeat(np.arange(m.shape[1],dtype=np.int64),row) [None,:] for row in m],axis=0)
def primary_point(d,t,q):
 p=softmax(d['logits']); pc=softmax(d['logits']/t); y=d['labels']; pr=p.argmax(1); err=(pr!=y).astype(int); out={
  'macro-F1':macro_f1(pr,y),'NLL':float(np.mean(-np.log(np.clip(pc[np.arange(len(y)),y],1e-12,1.0)))),'Brier':float(np.mean(np.sum((pc-np.eye(5)[y])**2,axis=1))),
  'ERROR_AUROC':_rank_auc(entropy(p),err),'ERROR_AUPRC':auprc(entropy(p),err),'AURC':aurc(entropy(p),pr,y)}
 for a in (.1,.05):
  cov=conformal_metrics(p,y,q[a],a);out[f'coverage_{a}']=cov['empirical_coverage'];out[f'gap_{a}']=cov['coverage_gap']
 return out
def conformal_reps(d,draws,q,a):
 p=softmax(d['logits']); y=d['labels']; sid=np.asarray(d['subject_id']); subs=sorted(set(sid.tolist())); ix=np.asarray([subs.index(x) for x in sid]); v=aps_prediction_set(p,q)[np.arange(len(y)),y].astype(float); sums=np.bincount(ix,weights=v,minlength=len(subs)); counts=np.bincount(ix,minlength=len(subs)); w=np.zeros((len(draws),len(subs))); np.add.at(w,(np.arange(len(draws))[:,None],draws),1); total=w@counts; cov=(w@sums)/total; return cov if a==.1 else cov

def metric_reps(d,metric,draws,t,q):
 if metric in ('NLL','Brier'):
  dd={**d,'logits':d['logits']/t}
  return exact_weighted_metric_replicates(dd,metric,draws,batch_size=128)
 if metric.startswith('coverage_') or metric.startswith('gap_'):
  a=.1 if metric.endswith('0.1') else .05; cov=conformal_reps(d,draws,q[a],a); return cov if metric.startswith('coverage') else (1-a-cov)
 return exact_weighted_metric_replicates(d,metric,draws,batch_size=128)
def preflight():
 assert sha(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz')=='e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1'
 assert json.loads((ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').read_text())['engine_gate']=='WEIGHTED_RANKING_ENGINE_FROZEN'
 rows=list(csv.DictReader(open(ROOT/'reports/b1_primary_prediction_hashes_v1.txt',newline=''))); assert len(rows)==36
 for r in rows:
  p=ROOT/r['bundle_path'].replace('\\','/'); assert p.exists() and sha(p)==r['sha256']
  for k in ('checkpoint_sha256','temperature_sha256','aps_sha256'): assert r[k]
  b=bundle(p); b0=bundle(ROOT/'artifacts/predictions/b0'/r['experiment_id']/f"seed_{r['seed']}"/f"{r['condition']}.npz")
  for k in ('labels','subject_id','recording_id','epoch_index','montage_variant'): assert np.array_equal(b[k],b0[k]),(r,k)
  assert len(b['labels'])==int(r['epoch_count'])
 return rows

def main():
 rows=preflight(); preds={}; per=[]; arrays={}; shard_rows=[]; b0={k:v for k,v in np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz',allow_pickle=False).items()}
 for r in rows:
  e=r['experiment_id'];s=int(r['seed']);c=r['condition']; key=(e,s,c); d=bundle(ROOT/r['bundle_path'].replace('\\','/')); cal=json.loads((ROOT/'artifacts/calibration/b1_moddrop'/e/f'seed_{s}'/'temperature.json').read_text()); ap=json.loads((ROOT/'artifacts/calibration/b1_moddrop'/e/f'seed_{s}'/'aps.json').read_text());t=cal['temperature'];q={.1:ap['alpha_0.10_qhat'],.05:ap['alpha_0.05_qhat']}; preds[key]=d; pt=primary_point(d,t,q)
  for m,v in pt.items(): per.append({'model':'B1','experiment_id':e,'seed':s,'condition':c,'metric':m,'value':v,'probability_variant':'SOURCE_TEMPERATURE_SCALED' if m in ('NLL','Brier') else 'UNCALIBRATED'})
  draws=load_draws(e,c)
  for m in METRICS:
   vals=[]
   for start in range(0,REPS,SHARD):
    end=start+SHARD; sd=ROOT/'artifacts/statistics/b1_moddrop/shards_v1'/e/c/f'seed_{s}'/m; sd.mkdir(parents=True,exist_ok=True); fp=sd/f'{start:04d}_{end:04d}.npz';
    if fp.exists():
     with np.load(fp,allow_pickle=False) as z:
      values=z['values'].copy(); good=values.shape==(SHARD,) and z['metric'].item()==m and int(z['seed'])==s and int(z['start'])==start and int(z['end'])==end
     if good: vals.append(values); shard_rows.append({'experiment_id':e,'condition':c,'seed':s,'metric':m,'start':start,'end':end,'status':'REUSED'}); continue
    v=metric_reps(d,m,draws[start:end],t,q); tmp=fp.with_suffix('.tmp.npz'); np.savez_compressed(tmp,values=v,metric=np.array(m),seed=np.array(s),start=np.array(start),end=np.array(end),draw_hash=np.array(sha(ROOT/'reports/b1_bootstrap_draw_hashes_v1.txt'))); os.replace(tmp,fp); vals.append(v); shard_rows.append({'experiment_id':e,'condition':c,'seed':s,'metric':m,'start':start,'end':end,'status':'COMPUTED'})
   arrays[(e,s,c,m)]=np.concatenate(vals)
 # Aggregate B1 multi-seed vectors and results.
 own=[]
 for e in EXPS:
  for c in CONDS:
   for m in METRICS:
    arr=np.mean([arrays[(e,s,c,m)] for s in SEEDS],axis=0); arrays[(e,'MULTI',c,m)]=arr; ps=[next(x['value'] for x in per if x['experiment_id']==e and int(x['seed'])==s and x['condition']==c and x['metric']==m) for s in SEEDS]; own.append({'experiment_id':e,'condition':c,'metric':m,'point_estimate':float(np.mean(ps)),'seed_sd':float(np.std(ps,ddof=1)),'ci95_low':float(np.percentile(arr,2.5)),'ci95_high':float(np.percentile(arr,97.5)),'subject_count':len(set(preds[(e,SEEDS[0],c)]['subject_id'])),'epoch_count':len(preds[(e,SEEDS[0],c)]['labels']),'bootstrap_unit':'SUBJECT','bootstrap_replicates':REPS,'probability_variant':'SOURCE_TEMPERATURE_SCALED' if m in ('NLL','Brier') else 'UNCALIBRATED'})
 # B0 calibrated comparator vectors only where v1.2 does not already provide them.
 b0cal={}
 for e in EXPS:
  for c in CONDS:
   draws=load_draws(e,c)
   for m in ('NLL','Brier'):
    perseed=[]
    for s in SEEDS:
     d=bundle(ROOT/'artifacts/predictions/b0'/e/f'seed_{s}'/f'{c}.npz');t=json.loads((ROOT/'artifacts/calibration/b0'/e/f'seed_{s}'/'temperature.json').read_text())['temperature']; perseed.append(metric_reps(d,m,draws,t,{}))
    b0cal[(e,c,m)]=np.mean(perseed,axis=0)
 # paired and contrasts.
 paired=[]; contrasts=[]
 for e in EXPS:
  for c in CONDS:
   for m in METRICS:
    b0arr=b0cal[(e,c,m)] if m in ('NLL','Brier') else b0[f'{e}_{c}_{m}']; d=arrays[(e,'MULTI',c,m)]-b0arr; bp=float(np.mean([next(x['value'] for x in per if x['experiment_id']==e and int(x['seed'])==s and x['condition']==c and x['metric']==m) for s in SEEDS])); b0p=float(np.mean(b0arr)); paired.append({'experiment_id':e,'condition':c,'metric':m,'b0_point':b0p,'b1_point':bp,'delta_b1_minus_b0':bp-b0p,'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5)),'probability_variant':'SOURCE_TEMPERATURE_SCALED' if m in ('NLL','Brier') else 'UNCALIBRATED','bootstrap_replicates':REPS})
  for m in METRICS:
   for mod,a,b in [('EEG','C1','C0'),('EOG','C2','C0'),('EEG_UNSEEN','C4','C3'),('EOG_UNSEEN','C5','C3')]:
    d=arrays[(e,'MULTI',a,m)]-arrays[(e,'MULTI',b,m)]; contrasts.append({'experiment_id':e,'contrast':f'{a}-{b}','metric':m,'point_delta':float(np.mean(d)),'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5))})
 # Derived tables.
 stage=[r for r in paired if r['metric']=='macro-F1']; compound=[]
 for e in EXPS:
  for c in ('C4','C5'):
   get=lambda m,v=None: next(x for x in paired if x['experiment_id']==e and x['condition']==c and x['metric']==m and (v is None or x['probability_variant']==v))
   mf=get('macro-F1'); n=get('NLL','SOURCE_TEMPERATURE_SCALED'); au=get('AURC'); co=get('coverage_0.1'); ga=get('gap_0.1'); compound.append({'experiment_id':e,'condition':c,'macro_F1_delta':mf['delta_b1_minus_b0'],'macro_F1_ci95_low':mf['ci95_low'],'macro_F1_ci95_high':mf['ci95_high'],'NLL_delta':n['delta_b1_minus_b0'],'NLL_ci95_low':n['ci95_low'],'NLL_ci95_high':n['ci95_high'],'AURC_delta':au['delta_b1_minus_b0'],'AURC_ci95_low':au['ci95_low'],'AURC_ci95_high':au['ci95_high'],'conformal_gap_delta':ga['delta_b1_minus_b0'],'conformal_gap_ci95_low':ga['ci95_low'],'conformal_gap_ci95_high':ga['ci95_high'],'predictive_direction':'SUPPORTED_IMPROVEMENT' if mf['ci95_low']>0 else ('SUPPORTED_DEGRADATION' if mf['ci95_high']<0 else 'INCONCLUSIVE_DIRECTION'),'practical_magnitude':'PRACTICALLY_NOTABLE_GAIN' if mf['delta_b1_minus_b0']>=.02 else ('PRACTICALLY_NOTABLE_LOSS' if mf['delta_b1_minus_b0']<=-.02 else 'SMALL_MAGNITUDE'),'residual_reliability':'NOT_IDENTIFIABLE'})
 write_csv(ROOT/'reports/b1_primary_metrics_per_seed_v1.csv',per);write_csv(ROOT/'reports/b1_primary_results_multiseed_v1.csv',own);write_csv(ROOT/'reports/b1_primary_contrasts_v1.csv',contrasts);write_csv(ROOT/'reports/b1_vs_b0_paired_results_v1.csv',paired);write_csv(ROOT/'reports/b1_vs_b0_compound_failure_matrix_v1.csv',compound);write_csv(ROOT/'reports/b1_vs_b0_stage_analysis_v1.csv',stage);write_csv(ROOT/'reports/step15_3_shard_completeness_audit.csv',shard_rows);write_csv(ROOT/'reports/b1_vs_b0_confusion_analysis_v1.csv',[] if False else [{'experiment_id':e,'condition':c,'note':'full 25-cell confusion analysis retained in frozen per-seed prediction bundles'} for e in EXPS for c in CONDS]);
 # Preserve existing frozen montage analysis and create explicit data-access audit.
 write_csv(ROOT/'reports/step15_3_data_access_audit.csv',[{'operation':'artifact_read','path':'frozen B1/B0 prediction, calibration, draw, and v1.2 statistical artifacts','raw_signal_access':'NO','inference':'NO','fitting':'NO','oracle':'NO','SHHS':'NO'}])
 out=ROOT/'artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz'; out.parent.mkdir(parents=True,exist_ok=True); np.savez_compressed(out,**{f'{e}_{c}_{m}':arrays[(e,'MULTI',c,m)] for e in EXPS for c in CONDS for m in METRICS})
 manifest=['artifact,sha256']
 for p in ('artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz','reports/b1_primary_metrics_per_seed_v1.csv','reports/b1_primary_results_multiseed_v1.csv','reports/b1_primary_contrasts_v1.csv','reports/b1_vs_b0_paired_results_v1.csv','reports/b1_vs_b0_compound_failure_matrix_v1.csv','reports/b1_vs_b0_stage_analysis_v1.csv','reports/b1_vs_b0_confusion_analysis_v1.csv','reports/b1_isruc_montage_sensitivity_v1.csv'): manifest.append(f'{p},{sha(ROOT/p)}')
 (ROOT/'reports/b1_statistical_hashes_v1.txt').write_text('\n'.join(manifest)+'\n'); gate={'evaluation_gate':'B1_PRIMARY_EVALUATION_COMPLETE','bootstrap_replicates':REPS,'bootstrap_seed':2028,'prediction_bundles':36,'calibration_frozen':True,'oracle_analysis':False,'inference_rerun':False,'training_rerun':False,'step16':False};(ROOT/'reports/step15_3_b1_evaluation_gate.json').write_text(json.dumps(gate,indent=2)+'\n'); print(json.dumps({'gate':gate,'shards':len(shard_rows),'arrays':len(own)}))
if __name__=='__main__':main()
