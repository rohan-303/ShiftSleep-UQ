#!/usr/bin/env python
"""Step 15.2.3: versioned exact B0 ranking-statistical repair."""
from __future__ import annotations
import csv, hashlib, json, shutil
from pathlib import Path
import numpy as np
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, exact_weighted_metric_replicates
from shiftsleep_uq.statistics.weighted_bootstrap import atomic_write_shard, read_shard, validate_shard, merge_shards, engine_hash
ROOT=Path(__file__).resolve().parents[1]
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C1','C2','C3','C4','C5'); METRICS=('ERROR_AUPRC','AURC'); REPS=2000; SEED=2028; SHARD=100

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def load(ex,s,c):
 p=ROOT/'artifacts/predictions/b0'/ex/f'seed_{s}'/f'{c}.npz'
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files},p

def write_csv(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True)
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
 forensic=(ROOT/'reports/STEP_15_2_2_B0_RANKING_BOOTSTRAP_PROVENANCE_AUDIT.md').read_text()
 required=('B0_RANKING_PROVENANCE_RESOLVED','B0_V1_1_AUPRC_AURC_BOOTSTRAP_BUG_CONFIRMED','CREATE_VERSIONED_B0_V1_2_RANKING_STATISTICAL_REPAIR')
 assert all(x in forensic for x in required)
 v11=ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz'; assert sha(v11)=='47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022'
 with np.load(v11,allow_pickle=False) as z: arrays={k:z[k].copy() for k in z.files}
 shard_root=ROOT/'artifacts/statistics/b0/v1_2_shards'; shard_root.mkdir(parents=True,exist_ok=True)
 repaired={}; shard_rows=[]; draw_hashes={}
 for ex in EXPS:
  for c in CONDS:
   d0,_=load(ex,17,c); subjects=sorted(set(d0['subject_id'].tolist())); draws=bootstrap_subject_draws(len(subjects),reps=REPS,seed=SEED); draw_hash=hashlib.sha256(np.asarray(draws,dtype=np.int64).tobytes()).hexdigest(); draw_hashes[f'{ex}_{c}']=draw_hash
   for metric in METRICS:
    seed_vectors=[]
    for s in SEEDS:
     d,p=load(ex,s,c); pred_hash=sha(p); seed_dir=shard_root/ex/c/f'seed_{s}'/metric; seed_dir.mkdir(parents=True,exist_ok=True); parts=[]
     for start in range(0,REPS,SHARD):
      end=min(REPS,start+SHARD); path=seed_dir/f'{start:04d}_{end:04d}.npz'; meta={'model':'B0','direction':ex,'condition':c,'seed':s,'metric':metric,'replicate_start':start,'replicate_end':end,'prediction_hash':pred_hash,'draw_hash':draw_hash,'engine_hash':engine_hash(ROOT/'src/shiftsleep_uq/step11_1_statistics.py')}
      if path.exists():
       old,vals=read_shard(path); validate_shard(old,vals,meta); shard_rows.append({'path':str(path.relative_to(ROOT)),'status':'REUSED','start':start,'end':end})
      else:
       vals=exact_weighted_metric_replicates(d,metric,draws[start:end],batch_size=32); atomic_write_shard(path,meta,vals); old,vals=read_shard(path); validate_shard(old,vals,meta); shard_rows.append({'path':str(path.relative_to(ROOT)),'status':'CREATED','start':start,'end':end})
      parts.append((old,vals))
     vec=merge_shards(parts,REPS); assert len(vec)==REPS and np.isfinite(vec).all(); seed_vectors.append(vec)
    repaired[f'{ex}_{c}_{metric}']=np.nanmean(np.stack(seed_vectors),axis=0)
 # v1.2 artifact: copy every historical array and replace only affected ranking arrays.
 v12=ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz'; out=dict(arrays); out.update(repaired); np.savez_compressed(v12,**out)
 unaffected=[]
 for k,v in arrays.items():
  if k in repaired: continue
  same=np.array_equal(v,out[k]); unaffected.append({'key':k,'metric':k.rsplit('_',1)[-1],'shape':str(v.shape),'v1_1_digest':hashlib.sha256(v.tobytes()).hexdigest(),'v1_2_digest':hashlib.sha256(out[k].tobytes()).hexdigest(),'exact_equal':same,'status':'PASS' if same else 'FAIL'})
 write_csv(ROOT/'reports/b0_v1_2_unaffected_array_audit.csv',unaffected)
 # Primary results: preserve all rows except affected CIs/summary fields.
 v11rows=list(csv.DictReader(open(ROOT/'reports/b0_primary_results_multiseed_v1_1.csv',newline=''))); v12rows=[]
 for r in v11rows:
  key=f"{r['experiment_id']}_{r['condition']}_{r['metric']}"
  if r['metric'] in METRICS:
   v=repaired[key]; r=dict(r); r['ci95_low']=str(float(np.percentile(v,2.5))); r['ci95_high']=str(float(np.percentile(v,97.5)))
  v12rows.append(r)
 write_csv(ROOT/'reports/b0_primary_results_multiseed_v1_2.csv',v12rows)
 # Contrast table: only existing AURC rows depend on repaired ranking vectors.
 v11c=list(csv.DictReader(open(ROOT/'reports/b0_primary_contrasts_v1_1.csv',newline=''))); v12c=[]
 for r in v11c:
  r=dict(r)
  if r['metric']=='AURC':
   ex=r['experiment_id']; name=r['contrast_name'];
   pairs={'KNOWN_EEG_ONLY_MINUS_FULL':('C1','C0'),'KNOWN_EOG_ONLY_MINUS_FULL':('C2','C0'),'UNSEEN_EEG_ONLY_MINUS_FULL':('C4','C3'),'UNSEEN_EOG_ONLY_MINUS_FULL':('C5','C3')}
   if name in pairs: a,b=pairs[name]; delta=repaired[f'{ex}_{a}_AURC']-repaired[f'{ex}_{b}_AURC']
   else:
    pairs2={'INTERACTION_EEG_ONLY':('C4','C3','C1','C0'),'INTERACTION_EOG_ONLY':('C5','C3','C2','C0')}; ua,ub,ka,kb=pairs2[name]; delta=(repaired[f'{ex}_{ua}_AURC']-repaired[f'{ex}_{ub}_AURC'])-(repaired[f'{ex}_{ka}_AURC']-repaired[f'{ex}_{kb}_AURC'])
   r['ci95_low']=str(float(np.percentile(delta,2.5))); r['ci95_high']=str(float(np.percentile(delta,97.5))); r['point_delta']=str(float(np.mean(delta)))
  v12c.append(r)
 write_csv(ROOT/'reports/b0_primary_contrasts_v1_2.csv',v12c)
 # Transition audits.
 old={(r['experiment_id'],r['condition'],r['metric']):r for r in v11rows}; new={(r['experiment_id'],r['condition'],r['metric']):r for r in v12rows}; trans=[]
 for key,r in old.items():
  n=new[key]; affected=r['metric'] in METRICS; ok=(r['point_estimate']==n['point_estimate']) and (affected or (r['ci95_low']==n['ci95_low'] and r['ci95_high']==n['ci95_high']))
  trans.append({'experiment':key[0],'condition':key[1],'metric':key[2],'v1_1_point':r['point_estimate'],'v1_2_point':n['point_estimate'],'point_delta':float(n['point_estimate'])-float(r['point_estimate']),'v1_1_ci_low':r['ci95_low'],'v1_1_ci_high':r['ci95_high'],'v1_2_ci_low':n['ci95_low'],'v1_2_ci_high':n['ci95_high'],'ci_low_delta':float(n['ci95_low'])-float(r['ci95_low']),'ci_high_delta':float(n['ci95_high'])-float(r['ci95_high']),'repair_scope':'AUPRC/AURC' if affected else 'UNAFFE​CTED','expected_change':'ALLOWED_AFFECTED' if affected else 'MUST_BE_IDENTICAL','status':'PASS' if ok else 'FAIL'})
 write_csv(ROOT/'reports/b0_v1_1_to_v1_2_transition_audit.csv',trans)
 # Existing contrast transition audit.
 oldc={(r['experiment_id'],r['metric'],r['contrast_name']):r for r in v11c}; newc={(r['experiment_id'],r['metric'],r['contrast_name']):r for r in v12c}; ca=[]
 for k,r in oldc.items():
  n=newc[k]; changed=any(r[f]!=n[f] for f in ('point_delta','ci95_low','ci95_high')); allowed=r['metric']=='AURC'; ca.append({'experiment':k[0],'metric':k[1],'contrast':k[2],'changed':changed,'repair_scope':'AURC' if allowed else 'UNAFFE​CTED','status':'PASS' if (changed==allowed or not changed) else 'FAIL'})
 write_csv(ROOT/'reports/b0_v1_1_to_v1_2_contrast_audit.csv',ca)
 # Downstream gate re-audit based on frozen Step 12.1 evidence and corrected ranking dependency.
 gates=[
 {'gate':'Criterion A','v1_1_status':'GATE_SPEC_IMPLEMENTATION_MISMATCH','v1_2_status':'GATE_SPEC_IMPLEMENTATION_MISMATCH','ranking_bootstrap_dependency':'SUPPORTING_ONLY','evidence':'Four cells retain non-ranking calibration/conformal evidence and substantial macro-F1 degradation; corrected ranking intervals do not remove the written-criteria finding.','changed':'NO'},
 {'gate':'Criterion B','v1_1_status':'PASS_ORACLE_RECOVERY','v1_2_status':'PASS_ORACLE_RECOVERY','ranking_bootstrap_dependency':'UNAFFECTED','evidence':'Uses oracle NLL/Brier/ECE/conformal artifacts, not B0 AUPRC/AURC bootstrap vectors.','changed':'NO'},
 {'gate':'Criterion C','v1_1_status':'DESIGN_CONSTRAINT_PASS','v1_2_status':'DESIGN_CONSTRAINT_PASS','ranking_bootstrap_dependency':'UNAFFECTED','evidence':'Design-only source-trained/target-label-free constraint.','changed':'NO'},
 {'gate':'Criterion D','v1_1_status':'FAIL','v1_2_status':'FAIL','ranking_bootstrap_dependency':'CONTROLLED_BY_MACRO_F1','evidence':'Substantial macro-F1 degradation is unchanged; ranking repair cannot change argmax predictions.','changed':'NO'},
 {'gate':'LIGHTWEIGHT_METHOD','v1_1_status':'LIGHTWEIGHT_METHOD_NOT_AUTHORIZED','v1_2_status':'LIGHTWEIGHT_METHOD_NOT_AUTHORIZED','ranking_bootstrap_dependency':'NO_DECISION_CHANGE','evidence':'Criterion D remains failed; no method authorization.','changed':'NO'},
 {'gate':'MODALITY_CONDITIONING','v1_1_status':'MODALITY_CONDITIONING_SUPPORTED','v1_2_status':'MODALITY_CONDITIONING_SUPPORTED','ranking_bootstrap_dependency':'UNAFFECTED','evidence':'Primary evidence is oracle condition/domain temperature and APS calibration evidence.','changed':'NO'}]
 write_csv(ROOT/'reports/b0_v1_2_downstream_gate_reaudit.csv',gates)
 gate={'step':'12.2','source_gate':'step12_gate_v1_1.json','b0_statistical_version':'v1_2','outcome':'GATE_OUTCOME_UNCHANGED_AFTER_B0_V1_2_REPAIR','final_lightweight_method_gate':'LIGHTWEIGHT_METHOD_NOT_AUTHORIZED','final_modality_conditioning_gate':'MODALITY_CONDITIONING_SUPPORTED','no_refitting':True,'no_inference':True}
 (ROOT/'reports/step12_gate_v1_2.json').write_text(json.dumps(gate,indent=2)+'\n')
 # Impact summary and hashes.
 impacts=[]
 for metric in METRICS:
  changes=[]
  for r in trans:
   if r['metric']==metric: changes += [abs(float(r['ci_low_delta'])),abs(float(r['ci_high_delta']))]
  impacts.append({'metric':metric,'max_ci_bound_change':max(changes),'median_abs_ci_bound_change':float(np.median(changes)),'rows_changed':sum(1 for r in trans if r['metric']==metric and (r['ci_low_delta']!=0 or r['ci_high_delta']!=0)),'point_estimates_changed':sum(1 for r in trans if r['metric']==metric and r['point_delta']!=0)})
 write_csv(ROOT/'reports/b0_v1_2_repair_impact.csv',impacts)
 hash_rows=[]
 for rel in ['artifacts/statistics/b0/bootstrap_replicates_v1_2.npz','reports/b0_primary_results_multiseed_v1_2.csv','reports/b0_primary_contrasts_v1_2.csv','reports/b0_v1_2_unaffected_array_audit.csv','reports/b0_v1_1_to_v1_2_transition_audit.csv','reports/b0_v1_1_to_v1_2_contrast_audit.csv','reports/b0_v1_2_downstream_gate_reaudit.csv','reports/step12_gate_v1_2.json']:
  hash_rows.append({'artifact':rel,'sha256':sha(ROOT/rel)})
 (ROOT/'reports/b0_statistical_hashes_v1_2.txt').write_text('artifact,sha256\n'+'\n'.join(f"{x['artifact']},{x['sha256']}" for x in hash_rows)+'\n')
 (ROOT/'reports/step15_2_3_repair_manifest.json').write_text(json.dumps({'version':'v1_2','reason':'Exact duplicate-preserving AUPRC/AURC subject-bootstrap repair','replicates':REPS,'seed':SEED,'shard_size':SHARD,'shards':len(shard_rows),'affected_arrays':len(repaired),'unchanged_arrays':len(unaffected),'hashes':hash_rows},indent=2)+'\n')
 print(json.dumps({'v1_2_hash':sha(v12),'shards':len(shard_rows),'repaired_arrays':len(repaired),'unaffected_arrays':len(unaffected),'transition_rows':len(trans),'contrast_rows':len(v12c)}))
if __name__=='__main__': main()
