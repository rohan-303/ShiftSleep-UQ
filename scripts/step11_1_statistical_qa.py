#!/usr/bin/env python
"""Step 11.1 statistics-only QA and repair from frozen prediction bundles."""
from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from shiftsleep_uq.evaluation_step11 import softmax, entropy, macro_f1, nll, brier, conformal_metrics, _rank_auc, auprc, aurc, ece
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, reconstruct_cluster_indices, _metric, percentile_interval, weighted_metric_replicates
ROOT=Path(__file__).resolve().parents[1]
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C1','C2','C3','C4','C5'); METRICS=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05'); REPS=2000; SEED=2028

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1<<20),b''): h.update(x)
 return h.hexdigest()

def load(ex, seed, cond):
 p=ROOT/'artifacts/predictions/b0'/ex/f'seed_{seed}'/f'{cond}.npz'; z=np.load(p,allow_pickle=False)
 return {k:z[k] for k in z.files}|{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}

def slice_bundle(d, idx):
 n=len(d['labels']); return {k:(v[idx] if isinstance(v,np.ndarray) and len(v)==n else v) for k,v in d.items()}

def qhats(ex, seed):
 a=json.loads((ROOT/'artifacts/calibration/b0'/ex/f'seed_{seed}'/'aps.json').read_text())
 return {0.1:a['alpha_0.10_qhat'],0.05:a['alpha_0.05_qhat']}

def metric(d, m, q):
 if m.startswith('coverage_') or m.startswith('gap_'):
  a=float(m.split('_')[-1]); return _metric(d,m,q[a],a)
 return _metric(d,m)

def write_csv(path, rows):
 path.parent.mkdir(parents=True,exist_ok=True)
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
 bundles={(ex,s,c):load(ex,s,c) for ex in EXPS for s in SEEDS for c in CONDS}
 # Cluster integrity and condition/seed identity.
 integrity=[]
 for ex in EXPS:
  for popconds in (('C0','C1','C2'),('C3','C4','C5')):
   ref=bundles[(ex,17,popconds[0])]
   ref_keys={(str(a),str(b),int(c)) for a,b,c in zip(ref['subject_id'],ref['recording_id'],ref['epoch_index'])}
   ref_sub=sorted(set(ref['subject_id'].tolist())); counts={s:int(np.sum(ref['subject_id']==s)) for s in ref_sub}
   for s in SEEDS:
    for c in popconds:
     d=bundles[(ex,s,c)]; keys={(str(a),str(b),int(c0)) for a,b,c0 in zip(d['subject_id'],d['recording_id'],d['epoch_index'])}
     assert keys==ref_keys and sorted(set(d['subject_id'].tolist()))==ref_sub
     assert {x:int(np.sum(d['subject_id']==x)) for x in ref_sub}==counts
     integrity.append({'experiment_id':ex,'condition':c,'seed':s,'subject_count':len(ref_sub),'epoch_count':len(d['labels']),'keys_match':True})
 # Identity invariant and per-seed recomputation audit.
 perseed=[]; identity=[]; undefined=[]
 for ex in EXPS:
  for c in CONDS:
   for s in SEEDS:
    d=bundles[(ex,s,c)]; q=qhats(ex,s); p=softmax(d['logits']); y=d['labels']; pred=p.argmax(1); e=(pred!=y).astype(int)
    vals={'macro-F1':macro_f1(pred,y),'NLL':nll(p,y),'Brier':brier(p,y),'ERROR_AUROC':_rank_auc(entropy(p),e),'ERROR_AUPRC':auprc(entropy(p),e),'AURC':aurc(entropy(p),pred,y),'coverage_0.1':conformal_metrics(p,y,q[.1],.1)['empirical_coverage'],'gap_0.1':conformal_metrics(p,y,q[.1],.1)['coverage_gap'],'coverage_0.05':conformal_metrics(p,y,q[.05],.05)['empirical_coverage'],'gap_0.05':conformal_metrics(p,y,q[.05],.05)['coverage_gap']}
    perseed += [{'experiment_id':ex,'condition':c,'seed':s,'metric':m,'value':float(v)} for m,v in vals.items()]
    id_draws=np.arange(len(set(d['subject_id'].tolist())),dtype=np.int64)[None,:]
    for m in METRICS:
     iv=weighted_metric_replicates(d,m,id_draws,qhat=q[float(m.split('_')[-1])] if m.startswith(('coverage_','gap_')) else None,alpha=float(m.split('_')[-1]) if m.startswith(('coverage_','gap_')) else None)[0]
     identity.append({'experiment_id':ex,'condition':c,'seed':s,'metric':m,'difference':float(iv-vals[m])})
     if not np.isfinite(iv): undefined.append({'experiment_id':ex,'condition':c,'seed':s,'metric':m})
 # Correct cluster bootstrap, reusing one draw matrix per population across conditions and seeds.
 arrays={}; diagnostics=[]; result_rows=[]
 for ex in EXPS:
  pop_draws={'SOURCE_TEST':bootstrap_subject_draws(len(set(bundles[(ex,17,'C0')]['subject_id'].tolist())),reps=REPS,seed=SEED),'COMPLETE_TARGET':bootstrap_subject_draws(len(set(bundles[(ex,17,'C3')]['subject_id'].tolist())),reps=REPS,seed=SEED)}
  for c in CONDS:
   pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; ds=[bundles[(ex,s,c)] for s in SEEDS]; subjects=sorted(set(ds[0]['subject_id'].tolist())); draws=pop_draws[pop]
   worker=ROOT/'artifacts/statistics/b0'/f'qa_worker_{ex}_{c}.npz'
   if worker.exists():
    wz=np.load(worker,allow_pickle=False); worker_arrays={m:wz[m] for m in METRICS}
   else: worker_arrays=None
   for m in METRICS:
    if worker_arrays is not None: reps=worker_arrays[m]
    else:
     reps_by_seed=[weighted_metric_replicates(d,m,draws,qhat=qhats(ex,SEEDS[i])[float(m.split('_')[-1])] if m.startswith(('coverage_','gap_')) else None,alpha=float(m.split('_')[-1]) if m.startswith(('coverage_','gap_')) else None) for i,d in enumerate(ds)]
     reps=np.nanmean(np.stack(reps_by_seed),axis=0)
    key=f'{ex}_{c}_{m}'; arrays[key]=reps
    point=np.array([next(x['value'] for x in perseed if x['experiment_id']==ex and x['condition']==c and x['seed']==s and x['metric']==m) for s in SEEDS],float)
    finite=int(np.isfinite(reps).sum()); low,high=percentile_interval(reps) if finite==REPS else (float('nan'),float('nan'))
    diagnostics.append({'experiment_id':ex,'condition':c,'metric':m,'point':float(point.mean()),'bootstrap_mean':float(np.nanmean(reps)),'bootstrap_median':float(np.nanmedian(reps)),'bootstrap_sd':float(np.nanstd(reps,ddof=1)),'bias':float(np.nanmean(reps)-point.mean()),'ci_low':low,'ci_high':high,'point_inside_CI':bool(low<=point.mean()<=high) if finite==REPS else False,'finite_replicates':finite,'undefined_replicates':REPS-finite})
    result_rows.append({'experiment_id':ex,'condition':c,'metric':m,'probability_variant':'UNCALIBRATED','point_estimate':float(point.mean()),'seed_sd':float(point.std(ddof=1)),'ci95_low':low,'ci95_high':high,'subject_count':len(subjects),'epoch_count':len(ds[0]['labels']),'bootstrap_unit':'SUBJECT','bootstrap_replicates':REPS})
 # Paired contrasts and interactions use shared draws within each population.
 contrasts=[]
 for ex in EXPS:
  source=bootstrap_subject_draws(len(set(bundles[(ex,17,'C0')]['subject_id'].tolist())),reps=REPS,seed=SEED); target=bootstrap_subject_draws(len(set(bundles[(ex,17,'C3')]['subject_id'].tolist())),reps=REPS,seed=SEED)
  for name,a,b,draws in (('KNOWN_EEG_ONLY_MINUS_FULL','C1','C0',source),('KNOWN_EOG_ONLY_MINUS_FULL','C2','C0',source),('UNSEEN_EEG_ONLY_MINUS_FULL','C4','C3',target),('UNSEEN_EOG_ONLY_MINUS_FULL','C5','C3',target)):
   for m in ('macro-F1','NLL','AURC','gap_0.1'):
    delta=arrays[f'{ex}_{a}_{m}']-arrays[f'{ex}_{b}_{m}']; contrasts.append({'experiment_id':ex,'metric':m,'contrast_name':name,'probability_variant':'UNCALIBRATED','point_delta':float(delta.mean()),'ci95_low':float(np.percentile(delta,2.5)),'ci95_high':float(np.percentile(delta,97.5)),'orientation':'higher_is_better' if m=='macro-F1' else ('zero_is_ideal_signed_gap' if m=='gap_0.1' else 'lower_is_better'),'bootstrap_replicates':REPS})
  for name,ua,ub,ka,kb in (('INTERACTION_EEG_ONLY','C4','C3','C1','C0'),('INTERACTION_EOG_ONLY','C5','C3','C2','C0')):
   for m in ('macro-F1','NLL','AURC','gap_0.1'):
    # independent source and target draws are already distinct matrices; subtract population deltas.
    delta=(arrays[f'{ex}_{ua}_{m}']-arrays[f'{ex}_{ub}_{m}'])-(arrays[f'{ex}_{ka}_{m}']-arrays[f'{ex}_{kb}_{m}'])
    contrasts.append({'experiment_id':ex,'metric':m,'contrast_name':name,'probability_variant':'UNCALIBRATED','point_delta':float(delta.mean()),'ci95_low':float(np.percentile(delta,2.5)),'ci95_high':float(np.percentile(delta,97.5)),'orientation':'higher_is_better' if m=='macro-F1' else ('zero_is_ideal_signed_gap' if m=='gap_0.1' else 'lower_is_better'),'bootstrap_replicates':REPS})
 # APS invariants.
 aps_audit=[]
 for ex in EXPS:
  for s in SEEDS:
   q=qhats(ex,s); assert q[.05]>=q[.1];
   for c in CONDS:
    d=bundles[(ex,s,c)]; p=softmax(d['logits']); s90=conformal_metrics(p,d['labels'],q[.1],.1); s95=conformal_metrics(p,d['labels'],q[.05],.05)
    from shiftsleep_uq.evaluation_step11 import aps_prediction_set
    z90=aps_prediction_set(p,q[.1]); z95=aps_prediction_set(p,q[.05]); assert np.all(~z90|z95) and z90.any(1).all() and z95.any(1).all()
    assert s95['empirical_coverage']+1e-12>=s90['empirical_coverage'] and s95['mean_set_size']+1e-12>=s90['mean_set_size']
    aps_audit.append({'experiment_id':ex,'seed':s,'condition':c,'qhat90':q[.1],'qhat95':q[.05],'coverage90':s90['empirical_coverage'],'coverage95':s95['empirical_coverage'],'mean_size90':s90['mean_set_size'],'mean_size95':s95['mean_set_size'],'nested':True})
 # Independent primary references.
 refs=[]
 for ex,c,m in (('D1_SLEEPEDF_TO_ISRUC','C0','macro-F1'),('D1_SLEEPEDF_TO_ISRUC','C3','macro-F1'),('D1_SLEEPEDF_TO_ISRUC','C5','macro-F1'),('D1_SLEEPEDF_TO_ISRUC','C3','NLL'),('D1_SLEEPEDF_TO_ISRUC','C5','AURC'),('D2_ISRUC_TO_SLEEPEDF','C0','macro-F1'),('D2_ISRUC_TO_SLEEPEDF','C3','macro-F1'),('D2_ISRUC_TO_SLEEPEDF','C4','AURC'),('D2_ISRUC_TO_SLEEPEDF','C5','NLL')):
  vals=[metric(bundles[(ex,s,c)],m,qhats(ex,s)) for s in SEEDS]; refs.append({'experiment_id':ex,'condition':c,'metric':m,'seed17':vals[0],'seed42':vals[1],'seed2026':vals[2],'point':float(np.mean(vals))})
 out=ROOT/'reports'; write_csv(out/'step11_1_bootstrap_diagnostics.csv',diagnostics); write_csv(out/'b0_primary_results_multiseed_v1_1.csv',result_rows); write_csv(out/'b0_primary_contrasts_v1_1.csv',contrasts)
 np.savez_compressed(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz',**arrays)
 status={'identity_max_abs_difference':float(max(abs(x['difference']) for x in identity)),'undefined_replicates':len(undefined),'integrity_rows':len(integrity),'diagnostic_rows':len(diagnostics),'contrast_rows':len(contrasts),'aps_rows':len(aps_audit),'reference_rows':len(refs),'point_outside_ci':sum(not x['point_inside_CI'] for x in diagnostics),'original_v1_bootstrap_hash':sha(ROOT/'artifacts/statistics/b0/bootstrap_replicates.npz'),'v1_1_bootstrap_hash':sha(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz'),'v1_1_results_hash':sha(out/'b0_primary_results_multiseed_v1_1.csv'),'v1_1_contrasts_hash':sha(out/'b0_primary_contrasts_v1_1.csv'),'integrity':integrity,'identity':identity,'undefined':undefined,'aps':aps_audit,'references':refs}
 (out/'step11_1_qa_summary.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
 (out/'b0_statistical_hashes_v1_1.txt').write_text('artifact,sha256\n'+f'reports/b0_primary_results_multiseed_v1_1.csv,{status["v1_1_results_hash"]}\n'+f'reports/b0_primary_contrasts_v1_1.csv,{status["v1_1_contrasts_hash"]}\n'+f'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz,{status["v1_1_bootstrap_hash"]}\n')
 print(json.dumps({k:v for k,v in status.items() if k not in ('integrity','identity','undefined','aps','references')},sort_keys=True))
if __name__=='__main__': main()
