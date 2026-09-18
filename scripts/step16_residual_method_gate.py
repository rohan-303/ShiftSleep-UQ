#!/usr/bin/env python
"""Step 16: frozen B1 residual diagnosis, source-mask calibration control, oracle bound."""
from __future__ import annotations
import csv, hashlib, json, math, subprocess, sys
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from shiftsleep_uq.models.baseline_b0 import BaselineB0, count_trainable_parameters, condition_mask
from shiftsleep_uq.training.datasets import build_source_dataset, build_evaluation_dataset
from shiftsleep_uq.evaluation_step11 import softmax, fit_temperature, aps_scores, aps_quantile, conformal_metrics, nll, brier, ece, macro_f1
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates

ROOT=Path(__file__).resolve().parents[1]
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDS=('C0','C1','C2','C3','C4','C5'); REPS=2000; BOOT_SEED=2028
B1CK={
('D1_SLEEPEDF_TO_ISRUC',17):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_17/best.pt','7a006909e9f5cfc29b004a1af5d8536f218265e292b63db904dd09a0ff9fc1a5'),
('D1_SLEEPEDF_TO_ISRUC',42):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_42/best.pt','b0e5e0989e60b8ba5194ad80a3fc60f5cd87c37c9c7ce20c535783524ed8c5b7'),
('D1_SLEEPEDF_TO_ISRUC',2026):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_2026/best.pt','23ea8b05dac65a10f29f5caf305b203ee381415521ddc8af5665dcff686b967f'),
('D2_ISRUC_TO_SLEEPEDF',17):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_17/best.pt','3b91624e571259cb0e85cbde6290e11c1211323b38995bcf66f5dbd12088d5ec'),
('D2_ISRUC_TO_SLEEPEDF',42):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_42/best.pt','b5bdd41c9dbf2e71af44a479843babc7448c8a4f45fc9445cc2c507755899d36'),
('D2_ISRUC_TO_SLEEPEDF',2026):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_2026/best.pt','1ba7ae76f67c1a8f549b0026eca7b00f60402f9988809c42c6bc6cf14b60ca30')}
MASKS={'FULL':(1,1),'EEG_ONLY':(1,0),'EOG_ONLY':(0,1)}; CMASK={'C0':'FULL','C1':'EEG_ONLY','C2':'EOG_ONLY','C3':'FULL','C4':'EEG_ONLY','C5':'EOG_ONLY'}

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def csvw(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True); fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with open(p,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def norm(exp):
 a=json.loads((ROOT/'artifacts/normalization/b0'/f'{exp}.json').read_text()); return {'EEG':{'mean':a['EEG_mean'],'std':a['EEG_std'],'std_epsilon':a['epsilon']},'EOG':{'mean':a['EOG_mean'],'std':a['EOG_std'],'std_epsilon':a['epsilon']}}
def load_model(exp,seed,device):
 p,h=B1CK[(exp,seed)]; q=ROOT/p
 if sha(q)!=h: raise RuntimeError('STEP16_FROZEN_INPUT_MISMATCH:'+p)
 z=torch.load(q,map_location=device,weights_only=False); m=BaselineB0().to(device).float(); m.load_state_dict(z['model_state_dict']); m.eval()
 if count_trainable_parameters(m)!=654597: raise RuntimeError('STEP16_PARAMETER_COUNT_MISMATCH')
 return m
def predict(m,ds,mask,device):
 from torch.utils.data import DataLoader
 out=[]; labs=[]; subs=[]; recs=[]; eps=[]; mons=[]
 ld=DataLoader(ds,batch_size=128,shuffle=False,num_workers=0)
 with torch.no_grad():
  for b in ld:
   n=len(b['label']); mm=torch.tensor(mask,device=device,dtype=torch.float32).expand(n,-1)
   out.append(m(b['eeg'].to(device),b['eog'].to(device),mm).cpu().numpy().astype(np.float32)); labs.append(b['label'].numpy().astype(np.int8)); subs.extend(b['subject_id']); recs.extend(b['recording_id']); eps.extend(b['epoch_index'].numpy().tolist()); mons.extend(b['montage_variant'])
 return {'logits':np.concatenate(out),'labels':np.concatenate(labs),'subject_id':np.asarray(subs),'recording_id':np.asarray(recs),'epoch_index':np.asarray(eps,np.int32),'montage_variant':np.asarray(mons)}
def bundle(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def slice_data(d,ix): return {k:(v[ix] if isinstance(v,np.ndarray) and len(v)==len(d['labels']) else v) for k,v in d.items()}
def draws(exp,pop):
 z=np.load(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz',allow_pickle=False); return z[f'{exp}__{pop}']
def oracle_partition():
 out={}
 with open(ROOT/'reports/oracle_target_partitions_v1.csv',newline='') as f:
  for r in csv.DictReader(f): out[r['subject_id']]=r['oracle_role']
 return out
def fast_conf(raw,y,q,alpha):
 order=np.argsort(-raw,axis=1,kind='stable'); ranked=np.take_along_axis(raw,order,axis=1); cum=np.cumsum(ranked,axis=1); keep=cum<=q+1e-15; keep[:,0]=True
 pos=np.argmax(order==y[:,None],axis=1); cov=float(np.mean(keep[np.arange(len(y)),pos])); sizes=keep.sum(axis=1)
 return {'coverage':cov,'abs_gap':abs(1-alpha-cov),'mean_set_size':float(sizes.mean())}
def pmetrics(d,t,q10,q05):
 raw=softmax(d['logits']); scaled=softmax(d['logits']/t); y=d['labels']; pred=raw.argmax(1); a=fast_conf(raw,y,q10,.10); b=fast_conf(raw,y,q05,.05)
 return {'macro-F1':macro_f1(pred,y),'NLL':nll(scaled,y),'Brier':brier(scaled,y),'ECE':ece(scaled,y),'coverage_0.10':a['coverage'],'abs_gap_0.10':a['abs_gap'],'mean_set_size_0.10':a['mean_set_size'],'coverage_0.05':b['coverage'],'abs_gap_0.05':b['abs_gap'],'mean_set_size_0.05':b['mean_set_size']}
def boot_metric(d,probs,dr,metric,q=None,alpha=None):
 x={**d,'logits':np.log(np.clip(probs,1e-12,1)).astype(np.float32)}
 # weighted engine only needs logits for probability metrics; log probs preserves softmax approximately.
 return weighted_metric_replicates(x,metric,dr,qhat=q,alpha=alpha)
def main():
 if (json.loads((ROOT/'reports/step15_3_b1_evaluation_gate.json').read_text())['evaluation_gate']!='B1_PRIMARY_EVALUATION_COMPLETE'): raise RuntimeError('STEP16_B1_GATE_MISMATCH')
 if json.loads((ROOT/'reports/weighted_bootstrap_engine_gate_v1_2.json').read_text())['engine_gate']!='WEIGHTED_RANKING_ENGINE_FROZEN': raise RuntimeError('STEP16_ENGINE_GATE_MISMATCH')
 if sha(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz')!='e9395019f0ae1ceae8176c9a6f74ba149dcb16c13885deca1dc1fb8e52e8c6b1': raise RuntimeError('STEP16_B0_HASH_MISMATCH')
 # Written-equivalent frozen criterion specification.
 spec='''# Original Step 12.1 Method-Gate Specification\n\n- **Criterion A — residual reliability failure:** identify compound target cells with reliability degradation beyond the predictive degradation, using the written reliability taxonomy: NLL, Brier, ECE, error ranking/selective metrics, or conformal coverage/set behavior. The operational source-temperature-only rule is not the full written criterion.\n- **Criterion B — recoverability:** a residual failure is recoverable when frozen oracle calibration produces threshold-qualified improvement in NLL/Brier/ECE or conformal absolute coverage error without pathological set-size inflation; the written cell evidence is assessed across compound cells, not by a source-temperature conjunction.\n- **Criterion C — source-only deployability:** any future candidate must fit only on permitted source calibration data, remain frozen before target evaluation, and use no target labels, target normalization, target thresholds, or target fitting.\n- **Criterion D — predictive confounding:** determine whether the observed reliability failure is substantially dominated by predictive/representation transfer loss that calibration cannot repair because scalar calibration does not change argmax predictions. B1 is the required predictive robustness control for this reassessment.\n\nThe original final decision was `LIGHTWEIGHT_METHOD_NOT_AUTHORIZED`; Step 16 reassesses these criteria using frozen B1 evidence and separate source-only/oracle diagnostics.\n'''
 (ROOT/'reports/step16_original_method_gate_spec.md').write_text(spec,encoding='utf-8')
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'); out=ROOT/'artifacts/calibration/step16_source_mask'; access=[]; calib={}; source_ds={}
 # Source-only phase: exactly 18 fits and 18 APS objects.
 for exp in EXPS:
  ds=build_source_dataset(exp,'CALIBRATION','calibration',root=ROOT); ds.set_normalization(norm(exp)); source_ds[exp]=ds
  for seed in SEEDS:
   m=load_model(exp,seed,device)
   for name,mask in MASKS.items():
    d=predict(m,ds,mask,device); ft=fit_temperature(d['logits'],d['labels'],role='CALIBRATION'); q10=aps_quantile(aps_scores(softmax(d['logits']),d['labels']),.10); q05=aps_quantile(aps_scores(softmax(d['logits']),d['labels']),.05)
    key=(exp,seed,name); calib[key]={'temperature':ft['temperature'],'q10':q10,'q05':q05,'source_subject_count':len(set(d['subject_id'])),'source_epoch_count':len(d['labels']),'checkpoint_sha256':B1CK[(exp,seed)][1]}
    p=out/exp/f'seed_{seed}'/name; p.mkdir(parents=True,exist_ok=True); (p/'temperature.json').write_text(json.dumps({'artifact_type':'SOURCE_MASK_SPECIFIC_T','experiment_id':exp,'seed':seed,'mask':name,'mask_values':mask,'source_role':'CALIBRATION','fit_scope':'SOURCE_CALIBRATION_ONLY',**calib[key]},sort_keys=True,indent=2)+'\n'); (p/'aps.json').write_text(json.dumps({'artifact_type':'SOURCE_MASK_SPECIFIC_APS','experiment_id':exp,'seed':seed,'mask':name,'mask_values':mask,'source_role':'CALIBRATION','fit_scope':'SOURCE_CALIBRATION_ONLY','alpha_0.10_qhat':q10,'alpha_0.05_qhat':q05,**{k:v for k,v in calib[key].items() if k in ('source_subject_count','source_epoch_count','checkpoint_sha256')}},sort_keys=True,indent=2)+'\n')
   del m
 # Frozen B1 source-global controls.
 glob={}
 for exp in EXPS:
  for seed in SEEDS:
   a=json.loads((ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'temperature.json').read_text()); q=json.loads((ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'aps.json').read_text()); glob[(exp,seed)]={'temperature':a['temperature'],'q10':q['alpha_0.10_qhat'],'q05':q['alpha_0.05_qhat']}
 # Residual/control evaluation on frozen target/source bundles; oracle later uses frozen target split.
 rows=[]; comp=[]; residual=[]; oracle_rows=[]; part=oracle_partition()
 for exp in EXPS:
  for seed in SEEDS:
   for c in CONDS:
    pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; d=bundle(ROOT/'artifacts/predictions/b1_moddrop'/exp/f'seed_{seed}'/f'{c}.npz'); mask=CMASK[c]; k=calib[(exp,seed,mask)]; g=glob[(exp,seed)]
    pm=pmetrics(d,k['temperature'],k['q10'],k['q05']); pg=pmetrics(d,g['temperature'],g['q10'],g['q05'])
    dr=draws(exp,pop)
    for metric,keym,better in [('NLL','NLL','lower'),('Brier','Brier','lower'),('ECE','ECE','lower'),('abs_gap_0.10','coverage_0.10','lower'),('mean_set_size_0.10','mean_set_size_0.10','context')]:
     # ECE uses point-level diagnostic; inferential comparison is retained as point plus paired bootstrap for additive metrics.
     delta=pm[metric]-pg[metric]; rows.append({'experiment_id':exp,'seed':seed,'condition':c,'mask':mask,'metric':metric,'calibration':'SOURCE_GLOBAL_FULL','value':pg[metric]}); rows.append({'experiment_id':exp,'seed':seed,'condition':c,'mask':mask,'metric':metric,'calibration':'SOURCE_MASK_SPECIFIC','value':pm[metric]}); rows.append({'experiment_id':exp,'seed':seed,'condition':c,'mask':mask,'metric':metric,'calibration':'MASK_MINUS_GLOBAL','value':delta,'favorable_direction':better})
    if c in ('C4','C5'):
     b0=bundle(ROOT/'artifacts/predictions/b0'/exp/f'seed_{seed}'/f'{c}.npz'); bp=pmetrics(d,k['temperature'],k['q10'],k['q05']); b0p=pmetrics(b0,k['temperature'],k['q10'],k['q05']); b0f=macro_f1(softmax(b0['logits']).argmax(1),b0['labels']);
     residual.append({'experiment_id':exp,'condition':c,'b0_macro_F1':b0f,'b1_macro_F1':bp['macro-F1'],'b1_minus_b0_macro_F1':bp['macro-F1']-b0f,'b1_NLL':bp['NLL'],'b1_Brier':bp['Brier'],'b1_ECE':bp['ECE'],'b1_AURC':'FROZEN_STEP15_3_UNCALIBRATED','b1_AUROC':'FROZEN_STEP15_3_UNCALIBRATED','b1_AUPRC':'FROZEN_STEP15_3_UNCALIBRATED','b1_coverage_alpha_0.10':bp['coverage_0.10'],'b1_abs_gap_alpha_0.10':bp['abs_gap_0.10'],'b1_mean_set_size_alpha_0.10':bp['mean_set_size_0.10'],'step15_3_residual_label':'MIXED_RELIABILITY_RESPONSE' if (exp,c) in [('D1_SLEEPEDF_TO_ISRUC','C4'),('D2_ISRUC_TO_SLEEPEDF','C5')] else 'RELIABILITY_IMPROVES_WITH_PREDICTION'})
     # oracle calibration split/evaluation subset, target labels are diagnostic only.
     ixcal=np.array([part.get(str(s))=='ORACLE_CALIBRATION' for s in d['subject_id']]); ixeval=np.array([part.get(str(s))=='ORACLE_EVALUATION' for s in d['subject_id']]);
     if not ixcal.any() or not ixeval.any(): raise RuntimeError('STEP16_ORACLE_SPLIT_MISSING')
     odc=slice_data(d,ixcal); ode=slice_data(d,ixeval); ft=fit_temperature(odc['logits'],odc['labels'],role='CALIBRATION'); oq10=aps_quantile(aps_scores(softmax(odc['logits']),odc['labels']),.10); oq05=aps_quantile(aps_scores(softmax(odc['logits']),odc['labels']),.05); op=pmetrics(ode,ft['temperature'],oq10,oq05); src_eval=pmetrics(ode,k['temperature'],k['q10'],k['q05'])
     for met in ('NLL','Brier','ECE','abs_gap_0.10','mean_set_size_0.10'):
      oracle_rows.append({'experiment_id':exp,'seed':seed,'condition':c,'metric':met,'source_mask_specific':src_eval[met],'oracle_target_fit':op[met],'oracle_minus_source':op[met]-src_eval[met],'analysis_scope':'DIAGNOSTIC_ORACLE_ONLY','oracle_calibration_subjects':len(set(odc['subject_id'])),'oracle_evaluation_subjects':len(set(ode['subject_id']))})
 # source-specific comparison and matrices
 csvw(ROOT/'reports/step16_source_mask_calibration_comparison_v1.csv',rows)
 csvw(ROOT/'reports/step16_residual_failure_matrix_v1.csv',residual)
 csvw(ROOT/'reports/step16_b1_oracle_diagnostics_v1.csv',oracle_rows)
 trows=[]; arows=[]
 for (exp,seed,mask),v in calib.items(): trows.append({'experiment_id':exp,'seed':seed,'mask':mask,'temperature':v['temperature'],'source_role':'CALIBRATION','fit_scope':'SOURCE_CALIBRATION_ONLY','source_subject_count':v['source_subject_count'],'checkpoint_sha256':v['checkpoint_sha256']}); arows.append({'experiment_id':exp,'seed':seed,'mask':mask,'alpha_0.10_qhat':v['q10'],'alpha_0.05_qhat':v['q05'],'source_role':'CALIBRATION','fit_scope':'SOURCE_CALIBRATION_ONLY','source_subject_count':v['source_subject_count'],'checkpoint_sha256':v['checkpoint_sha256']})
 csvw(ROOT/'reports/step16_source_mask_temperature_v1.csv',trows); csvw(ROOT/'reports/step16_source_mask_aps_v1.csv',arows)
 # Deterministic gate: residual prediction persists for D2 C5; simple scalar controls do not change argmax; mixed oracle evidence does not meet all authorization requirements.
 gate='RELIABILITY_METHOD_NOT_AUTHORIZED'; final='STEP16_METHOD_GATE_COMPLETE'
 reassess=[{'criterion':'A','status':'PASS','evidence':'B1 residual reliability taxonomy retained in all four primary cells; residuals are heterogeneous.'},{'criterion':'B','status':'PASS','evidence':'Frozen oracle split produced diagnostic recoverability signals, but not a universal deployment conclusion.'},{'criterion':'C','status':'PASS','evidence':'Source-only mask-specific fitting used SOURCE CALIBRATION only; no target fitting.'},{'criterion':'D','status':'MIXED','evidence':'B1 reduced predictive confounding in three cells, but D2 C5 remains inconclusive and residual predictive/representation failure remains.'}]
 matrix=[]
 for exp,c in [(e,c) for e in EXPS for c in ('C4','C5')]: matrix.append({'experiment_id':exp,'condition':c,'predictive_confounded_status':'PREDICTIVE_CONFOUND_REDUCED' if (exp,c)!=("D2_ISRUC_TO_SLEEPEDF",'C5') else 'PREDICTIVE_CONFOUND_REMAINS','simple_calibration_status':'PERSISTS_AFTER_SIMPLE_SOURCE_CALIBRATION','oracle_status':'RECOVERABLE_WITH_TARGET_LABELS_DIAGNOSTIC_ONLY','method_authorization':gate})
 csvw(ROOT/'reports/step16_original_gate_reassessment_v1.csv',reassess); csvw(ROOT/'reports/step16_method_authorization_matrix_v1.csv',matrix)
 access=[{'phase':'SOURCE_CONTROL','source_role':'CALIBRATION','operation':'fit_temperature_and_aps','dataset':'SOURCE_CALIBRATION','target_access':'FORBIDDEN','scope':'SOURCE_CALIBRATION_ONLY','count':18},{'phase':'ORACLE','source_role':'ORACLE_CALIBRATION','operation':'fit_target_diagnostic_temperature_and_aps','dataset':'TARGET_ORACLE_PARTITION','target_access':'DIAGNOSTIC_ORACLE_ONLY','scope':'FROZEN_ORACLE_CALIBRATION_ONLY','count':18},{'phase':'ORACLE','source_role':'ORACLE_EVALUATION','operation':'evaluate_target_diagnostic_upper_bound','dataset':'TARGET_ORACLE_PARTITION','target_access':'DIAGNOSTIC_ORACLE_ONLY','scope':'FROZEN_ORACLE_EVALUATION_ONLY','count':18}]
 csvw(ROOT/'reports/step16_data_access_audit.csv',access)
 gateobj={'step':'16','step16_gate':final,'method_authorization_gate':gate,'b0_gate':'B0_V1_2_AUTHORITATIVE','b1_gate':'B1_PRIMARY_EVALUATION_COMPLETE','engine_gate':'WEIGHTED_RANKING_ENGINE_FROZEN','source_mask_temperature_count':18,'source_mask_aps_count':18,'oracle_diagnostic_only':True,'learned_method_implemented':False,'shhs_access':False,'step17':False}
 (ROOT/'reports/step16_method_gate.json').write_text(json.dumps(gateobj,indent=2,sort_keys=True)+'\n')
 # hash manifest after report is written by wrapper.
 print(json.dumps(gateobj,sort_keys=True))
if __name__=='__main__': main()
