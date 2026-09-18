#!/usr/bin/env python
"""Step 15: freeze B1 source calibration, evaluate C0-C5, paired B0 comparison."""
from __future__ import annotations
import csv, hashlib, json, math, os, sys
from datetime import UTC, datetime
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import DataLoader
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.models.baseline_b0 import BaselineB0, count_trainable_parameters, condition_mask
from shiftsleep_uq.training.datasets import build_source_dataset, build_evaluation_dataset
from shiftsleep_uq.evaluation_step11 import (PhaseGate, fit_temperature, softmax, aps_scores, aps_quantile,
    aps_prediction_set, macro_f1, kappa, balanced_accuracy, nll, brier, ece, classwise_ece,
    entropy, _rank_auc, auprc, aurc, selective_rows, conformal_metrics, confusion_matrix)
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates, percentile_interval, bootstrap_subject_draws, reconstruct_cluster_indices
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDITIONS=('C0','C1','C2','C3','C4','C5'); REPS=2000; BOOT_SEED=2028
B1CFG={'configs/baseline_b1_moddrop_v1.yaml':'b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6','configs/training_b1_moddrop_v1.yaml':'467ed74d465a65990388f4ac4f271311ccb156605cc1cfef1d4339057298bbc7'}
# The complete training hash is checked from the frozen protocol manifest below.
EXPECTED={'configs/baseline_b1_moddrop_v1.yaml':'b9c40bad93c181fb10534cb5c1a945d4de66dd2c1ace41cef1f85a7646aaeff6','configs/training_b1_moddrop_v1.yaml':'467ed74d465a65990388f4ac4f271311ccb156605cc1cfef1d4339057298bbc7','docs/baseline_b1_moddrop_protocol_v1.md':'7db8bc63f21df1ea53fb58d881c8e4996651e57e1c8fd154283b1d273caa2c1c','reports/b1_training_summary_v1.csv':'3b75ed17e005596b8b2297d18734d349a287acf19a9b16678e768730316f38d8','reports/b1_modality_exposure_summary_v1.csv':'d25e80bb471cefbfb081c350008942c385493d38d66371f043249b8a7ac8d71f','reports/b1_checkpoint_hashes_v1.txt':'690a5811e9cff075a49797e624a65a7d12f4cfc30f1d46b884957e6829101160','configs/evaluation_protocol_v1_1.yaml':'dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756','reports/subject_partitions_v2.csv':'9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329','reports/b0_primary_results_multiseed_v1_1.csv':'288122138f1b29c4b3ac8ca3de6e4f38baf97e20eefeaa15d029116337543efc','reports/b0_primary_contrasts_v1_1.csv':'008a9ad350c15f69d633a24ae584f3ace974b42a37a5a57b1df9e4429bbd4b4d','artifacts/statistics/b0/bootstrap_replicates_v1_1.npz':'47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022','reports/b0_primary_prediction_hashes_v1.txt':'77422f9aa4a0d7ba359268a1914e316e567da13fed3ad242c3100cef43408af7','artifacts/normalization/b0/D1_SLEEPEDF_TO_ISRUC.json':'be93b208d5cd3bf5b567b55ea76030a132d78108b6c6167dba6bb0d1d0199fb3','artifacts/normalization/b0/D2_ISRUC_TO_SLEEPEDF.json':'3a56d5cbf37bba4a27d55b94251ed1a299b9449eaa31d2aa9d94e56b69aa967e'}
B1CK={('D1_SLEEPEDF_TO_ISRUC',17):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_17/best.pt','7a006909e9f5cfc29b004a1af5d8536f218265e292b63db904dd09a0ff9fc1a5'),('D1_SLEEPEDF_TO_ISRUC',42):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_42/best.pt','b0e5e0989e60b8ba5194ad80a3fc60f5cd87c37c9c7ce20c535783524ed8c5b7'),('D1_SLEEPEDF_TO_ISRUC',2026):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_2026/best.pt','23ea8b05dac65a10f29f5caf305b203ee381415521ddc8af5665dcff686b967f'),('D2_ISRUC_TO_SLEEPEDF',17):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_17/best.pt','3b91624e571259cb0e85cbde6290e11c1211323b38995bcf66f5dbd12088d5ec'),('D2_ISRUC_TO_SLEEPEDF',42):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_42/best.pt','b5bdd41c9dbf2e71af44a479843babc7448c8a4f45fc9445cc2c507755899d36'),('D2_ISRUC_TO_SLEEPEDF',2026):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_2026/best.pt','1ba7ae76f67c1a8f549b0026eca7b00f60402f9988809c42c6bc6cf14b60ca30')}
# Correct the two values from the authoritative manifest at runtime; no hard-coded path substitution is allowed.
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def csvw(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True); fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with open(p,'w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def norm(exp):
 a=json.loads((ROOT/'artifacts/normalization/b0'/f'{exp}.json').read_text()); return {'EEG':{'mean':a['EEG_mean'],'std':a['EEG_std'],'std_epsilon':a['epsilon']},'EOG':{'mean':a['EOG_mean'],'std':a['EOG_std'],'std_epsilon':a['epsilon']}}
def load_b1(exp,seed,device):
 p,h=B1CK[(exp,seed)]; q=ROOT/p
 if not q.exists() or sha(q)!=h: raise RuntimeError('STEP15_FROZEN_INPUT_MISMATCH:'+p)
 z=torch.load(q,map_location=device,weights_only=False); m=BaselineB0().to(device).float(); m.load_state_dict(z['model_state_dict']); m.eval()
 if count_trainable_parameters(m)!=654597: raise RuntimeError('STEP15_PARAMETER_COUNT_MISMATCH')
 return m
def predict(m,ds,mask,device):
 out=[]; labs=[]; subs=[]; recs=[]; eps=[]; mons=[]; ld=DataLoader(ds,batch_size=128,shuffle=False,num_workers=0,pin_memory=device.type=='cuda')
 with torch.no_grad():
  for b in ld:
   n=len(b['label']); mm=torch.tensor(mask,device=device,dtype=torch.float32).expand(n,-1); out.append(m(b['eeg'].to(device),b['eog'].to(device),mm).cpu().numpy().astype(np.float32)); labs.append(b['label'].numpy().astype(np.int8)); subs.extend(b['subject_id']); recs.extend(b['recording_id']); eps.extend(b['epoch_index'].numpy().tolist()); mons.extend(b['montage_variant'])
 return {'logits':np.concatenate(out),'labels':np.concatenate(labs),'subject_id':np.asarray(subs),'recording_id':np.asarray(recs),'epoch_index':np.asarray(eps,np.int32),'montage_variant':np.asarray(mons)}
def validate_alignment(a,b):
 for k in ('labels','subject_id','recording_id','epoch_index','montage_variant'):
  if not np.array_equal(a[k],b[k]): raise RuntimeError('B1_B0_EVALUATION_ALIGNMENT_FAILURE:'+k)
def metrics(data,t,q):
 raw=softmax(data['logits']); scaled=softmax(data['logits']/t); lab=data['labels']; pred=raw.argmax(1); rows=[]
 for var,p in [('UNCALIBRATED',raw),('SOURCE_TEMPERATURE_SCALED',scaled)]:
  base={'NLL':nll(p,lab),'Brier':brier(p,lab),'ECE_15_EQUAL_WIDTH':ece(p,lab),'ADAPTIVE_ECE_15':ece(p,lab,adaptive=True),'CLASSWISE_ECE':classwise_ece(p,lab)}
  for k,v in base.items(): rows.append((var,'',k,v))
  for score_name,score in [('PREDICTIVE_ENTROPY',entropy(p)),('ONE_MINUS_MAX',1-p.max(1))]:
   err=(pred!=lab).astype(int); rows += [(var,score_name,'ERROR_AUROC',_rank_auc(score,err)),(var,score_name,'ERROR_AUPRC',auprc(score,err))]
   rows += [(var,score_name,k,v) for k,v in selective_rows(score,pred,lab).items()]
 for alpha,qh in q.items():
  for k,v in conformal_metrics(raw,lab,qh,alpha).items(): rows.append(('UNCALIBRATED','',f'APS_{k}_alpha_{alpha:.2f}',v))
 cm=confusion_matrix(pred,lab); rows += [('ARGMAX_INVARIANT','',k,v) for k,v in {'macro-F1':macro_f1(pred,lab),'Cohen_kappa':kappa(pred,lab),'balanced_accuracy':balanced_accuracy(pred,lab)}.items()]
 for c in range(5): rows.append(('ARGMAX_INVARIANT','',f'recall_class_{c}',float(cm[c,c]/cm[c].sum()) if cm[c].sum() else float('nan')))
 return rows,cm
def b0_calib(exp,seed):
 d=ROOT/'artifacts/calibration/b0'/exp/f'seed_{seed}'; return json.loads((d/'temperature.json').read_text()),json.loads((d/'aps.json').read_text())
def bundle(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def main():
 if Path.cwd().resolve()!=ROOT.resolve(): raise RuntimeError('STEP15_FROZEN_INPUT_MISMATCH')
 for p,h in EXPECTED.items():
  if '?' in h or not (ROOT/p).exists() or sha(ROOT/p)!=h: raise RuntimeError('STEP15_FROZEN_INPUT_MISMATCH:'+p)
 # Recover exact B1 training/config hashes from the already frozen hash manifest, preserving literal hashes.
 manifest=(ROOT/'reports/step13_b1_protocol_hashes.txt').read_text().splitlines()
 for line in manifest:
  if line.startswith('configs/training_b1_moddrop_v1.yaml,'): EXPECTED['configs/training_b1_moddrop_v1.yaml']=line.split(',',1)[1].strip()
  if line.startswith('configs/baseline_b1_moddrop_v1.yaml,'): EXPECTED['configs/baseline_b1_moddrop_v1.yaml']=line.split(',',1)[1].strip()
 if '?' in EXPECTED['configs/training_b1_moddrop_v1.yaml']: raise RuntimeError('STEP15_FROZEN_INPUT_MISMATCH:protocol hash manifest')
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'); access=[]; temps={}; aps={}; gate=PhaseGate('PHASE_A_CALIBRATION')
 # Phase A only.
 for exp in EXPS:
  ds=build_source_dataset(exp,'CALIBRATION','calibration',root=ROOT); ds.set_normalization(norm(exp))
  for seed in SEEDS:
   m=load_b1(exp,seed,device); d=predict(m,ds,(1,1),device); fit=fit_temperature(d['logits'],d['labels'],role='CALIBRATION'); q={a:aps_quantile(aps_scores(softmax(d['logits']),d['labels']),a) for a in (.10,.05)}; key=f'{exp}/seed_{seed}'; out=ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'; out.mkdir(parents=True,exist_ok=True); nh=sha(ROOT/'artifacts/normalization/b0'/f'{exp}.json')
   t={'artifact_type':'SOURCE_CALIBRATION_TEMPERATURE','experiment_id':exp,'seed':seed,'checkpoint_sha256':B1CK[(exp,seed)][1],'normalization_sha256':nh,'source_dataset':ds.dataset,'source_role':'CALIBRATION','source_subject_count':len(ds.subject_ids),'source_epoch_count':len(ds),'fitted_temperature':fit['temperature'],'temperature':fit['temperature'],'initial_nll':fit['initial_nll'],'final_nll':fit['final_nll'],'converged':fit['converged'],'optimization':fit['optimization'],'b1_model_config_sha256':sha(ROOT/'configs/baseline_b1_moddrop_v1.yaml'),'b1_training_config_sha256':EXPECTED['configs/training_b1_moddrop_v1.yaml'],'protocol_sha256':EXPECTED['configs/evaluation_protocol_v1_1.yaml']}
   a={'artifact_type':'SOURCE_CALIBRATION_APS','experiment_id':exp,'seed':seed,'checkpoint_sha256':B1CK[(exp,seed)][1],'normalization_sha256':nh,'source_dataset':ds.dataset,'source_role':'CALIBRATION','source_subject_count':len(ds.subject_ids),'source_epoch_count':len(ds),'alpha_0.10_qhat':q[.10],'alpha_0.05_qhat':q[.05],'quantile_rule':'k=ceil((n+1)*(1-alpha)), clamped 1..n, kth ascending score','score_definition':'APS cumulative uncalibrated softmax probability','protocol_sha256':EXPECTED['configs/evaluation_protocol_v1_1.yaml']}
   (out/'temperature.json').write_text(json.dumps(t,indent=2,sort_keys=True)+'\n'); (out/'aps.json').write_text(json.dumps(a,indent=2,sort_keys=True)+'\n'); temps[key]=t; aps[key]=a; access.extend({**e,'phase':'PHASE_A','operation':'calibration_inference'} for e in ds.access_events); access.append({'dataset':ds.dataset,'source_role':'CALIBRATION','purpose':'temperature_and_aps_fit','phase':'PHASE_A','operation':'fit_parameters','subject_id':'ALL','recording_id':'ALL','path':'SOURCE_CALIBRATION_ONLY'}); del m
 gate=gate.freeze();
 if gate.phase!='PHASE_A_CALIBRATION' or not gate.closed: raise RuntimeError('STEP15_CALIBRATION_FREEZE_FAILURE')
 csvw(ROOT/'reports/b1_temperature_calibration_v1.csv',list(temps.values())); csvw(ROOT/'reports/b1_aps_calibration_v1.csv',list(aps.values()));
 hrows=[]
 for key in temps:
  exp,ss=key.split('/seed_'); d=ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{ss}'; hrows += [{'experiment_id':exp,'seed':ss,'artifact':'temperature','sha256':sha(d/'temperature.json')},{'experiment_id':exp,'seed':ss,'artifact':'aps','sha256':sha(d/'aps.json')}]
 csvw(ROOT/'reports/b1_calibration_hashes_v1.txt',hrows,['experiment_id','seed','artifact','sha256']); (ROOT/'artifacts/calibration/b1_moddrop/SOURCE_CALIBRATION_FROZEN.json').write_text(json.dumps({'gate':'B1_SOURCE_CALIBRATION_FROZEN','temperature_count':6,'aps_count':6,'phase_b_opened':True,'calibration_hashes':hrows},indent=2)+'\n')
 # Phase B only.
 preds={}; rows=[]; conf=[]; montage=[]; ph=[]
 for exp in EXPS:
  dsets={'SOURCE_TEST':build_evaluation_dataset(exp,'SOURCE_TEST',root=ROOT),'COMPLETE_TARGET':build_evaluation_dataset(exp,'COMPLETE_TARGET',root=ROOT)}
  for ds in dsets.values(): ds.set_normalization(norm(exp))
  for seed in SEEDS:
   m=load_b1(exp,seed,device); key=f'{exp}/seed_{seed}'; t=temps[key]['temperature']; q={.10:aps[key]['alpha_0.10_qhat'],.05:aps[key]['alpha_0.05_qhat']}; th=sha(ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'temperature.json'); ah=sha(ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'aps.json')
   for c in CONDITIONS:
    pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; path=ROOT/'artifacts/predictions/b1_moddrop'/exp/f'seed_{seed}'/f'{c}.npz'; data=bundle(path) if path.exists() else predict(m,dsets[pop],condition_mask(c),device); b0=bundle(ROOT/'artifacts/predictions/b0'/exp/f'seed_{seed}'/f'{c}.npz'); validate_alignment(data,b0); path.parent.mkdir(parents=True,exist_ok=True); phash=sha(path); preds[(exp,seed,c)]={**data,'prediction_hash':phash}; ph.append({'experiment_id':exp,'seed':seed,'condition':c,'population':pop,'epoch_count':len(data['labels']),'bundle_path':str(path.relative_to(ROOT)),'sha256':phash,'checkpoint_sha256':B1CK[(exp,seed)][1],'normalization_sha256':sha(ROOT/'artifacts/normalization/b0'/f'{exp}.json'),'temperature_sha256':th,'aps_sha256':ah})
    rr,cm=metrics(data,t,q); pr=softmax(data['logits']); lab=data['labels'];
    for var,score,metric,val in rr: rows.append({'baseline_id':'B1_B0_ARCH_SOURCE_MODALITY_DROPOUT','experiment_id':exp,'seed':seed,'condition':c,'population':pop,'probability_variant':var,'uncertainty_score':score,'metric':metric,'value':val,'subject_count':len(set(data['subject_id'])),'epoch_count':len(lab),'prediction_hash':phash,'temperature_hash':th,'aps_hash':ah})
    for i in range(5):
     for j in range(5): conf.append({'experiment_id':exp,'seed':seed,'condition':c,'true_class':i,'predicted_class':j,'count':int(cm[i,j]),'prediction_hash':phash})
    if dsets[pop].dataset=='isruc_s1':
     for mo in ('ISRUC_A1A2','ISRUC_M1M2'):
      ix=data['montage_variant']==mo
      if ix.any():
       pp=softmax(data['logits'][ix]); ll=lab[ix]; prd=pp.argmax(1); ee=(prd!=ll).astype(int); en=entropy(pp)
       for met,val in {'macro-F1':macro_f1(prd,ll),'NLL':nll(pp,ll),'Brier':brier(pp,ll),'error_entropy_AUROC':_rank_auc(en,ee),'error_entropy_AUPRC':auprc(en,ee),'entropy_AURC':aurc(en,prd,ll)}.items(): montage.append({'direction':exp,'seed':seed,'condition':c,'montage':mo,'metric':met,'probability_variant':'UNCALIBRATED','value':val,'subject_count':len(set(data['subject_id'][ix])),'epoch_count':int(ix.sum())})
   for ds in dsets.values(): access.extend({**e,'phase':'PHASE_B','operation':'evaluation_inference'} for e in ds.access_events)
   del m
 # outputs
 csvw(ROOT/'reports/b1_primary_metrics_per_seed_v1.csv',rows); csvw(ROOT/'reports/b1_primary_prediction_hashes_v1.txt',ph); csvw(ROOT/'reports/b1_vs_b0_confusion_analysis_v1.csv',conf); csvw(ROOT/'reports/b1_isruc_montage_sensitivity_v1.csv',montage)
 # B1 multiseed own primary and paired B0 contrasts.
 metric_names=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05'); own=[]; paired=[]; stage=[]; compound=[]
 for exp in EXPS:
  for c in CONDITIONS:
   bs=[preds[(exp,s,c)] for s in SEEDS]; qh=[aps[f'{exp}/seed_{s}']['alpha_0.10_qhat'] for s in SEEDS]
   draws=bootstrap_subject_draws(len(set(bs[0]['subject_id'])),reps=REPS,seed=BOOT_SEED); b0s=[bundle(ROOT/'artifacts/predictions/b0'/exp/f'seed_{s}'/f'{c}.npz') for s in SEEDS]; b0ts=[b0_calib(exp,s)[0]['temperature'] for s in SEEDS]; b0q=[b0_calib(exp,s)[1]['alpha_0.10_qhat'] for s in SEEDS]
   for met in metric_names:
    alpha=.1 if '0.1' in met else (.05 if '0.05' in met else None); q1=[aps[f'{exp}/seed_{s}'][f'alpha_{alpha:.2f}_qhat'] for s in SEEDS] if alpha else None; keymet=met.replace('coverage_','coverage_').replace('gap_','gap_')
    arr=np.mean([weighted_metric_replicates(d, keymet, draws, qhat=q1[i] if q1 else None, alpha=alpha) for i,d in enumerate(bs)],axis=0); point=[]
    for d in bs:
     p=softmax(d['logits']); y=d['labels']; pr=p.argmax(1); en=entropy(p); er=(pr!=y).astype(int); point.append({'macro-F1':macro_f1(pr,y),'NLL':nll(p,y),'Brier':brier(p,y),'ERROR_AUROC':_rank_auc(en,er),'ERROR_AUPRC':auprc(en,er),'AURC':aurc(en,pr,y),'coverage_0.1':conformal_metrics(p,y,aps[f'{exp}/seed_{SEEDS[0]}']['alpha_0.10_qhat'],.1)['empirical_coverage'],'gap_0.1':conformal_metrics(p,y,aps[f'{exp}/seed_{SEEDS[0]}']['alpha_0.10_qhat'],.1)['coverage_gap'],'coverage_0.05':conformal_metrics(p,y,aps[f'{exp}/seed_{SEEDS[0]}']['alpha_0.05_qhat'],.05)['empirical_coverage'],'gap_0.05':conformal_metrics(p,y,aps[f'{exp}/seed_{SEEDS[0]}']['alpha_0.05_qhat'],.05)['coverage_gap']}[met])
    own.append({'experiment_id':exp,'condition':c,'metric':met,'probability_variant':'UNCALIBRATED','point_estimate':float(np.mean(point)),'seed_sd':float(np.std(point,ddof=1)),'ci95_low':float(np.percentile(arr,2.5)),'ci95_high':float(np.percentile(arr,97.5)),'subject_count':len(set(bs[0]['subject_id'])),'bootstrap_unit':'SUBJECT','bootstrap_replicates':REPS})
   for met in ('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC'):
    for variant in ('UNCALIBRATED','SOURCE_TEMPERATURE_SCALED'):
     left=[]; right=[]
     for s in SEEDS:
      x=preds[(exp,s,c)]; y=b0s[SEEDS.index(s)];
      if variant=='SOURCE_TEMPERATURE_SCALED': x={**x,'logits':x['logits']/temps[f'{exp}/seed_{s}']['temperature']}; y={**y,'logits':y['logits']/b0ts[SEEDS.index(s)]}
      left.append(x); right.append(y)
     arr=np.mean([weighted_metric_replicates(x,met,draws) for x in left],axis=0)-np.mean([weighted_metric_replicates(x,met,draws) for x in right],axis=0); bp=np.mean([weighted_metric_replicates(z,met,draws[:1])[0] for z in left]); cp=np.mean([weighted_metric_replicates(z,met,draws[:1])[0] for z in right]); lo,hi=percentile_interval(arr)
     paired.append({'experiment_id':exp,'condition':c,'metric':met,'probability_variant':variant,'b0_point':float(cp),'b1_point':float(bp),'delta_b1_minus_b0':float(bp-cp),'ci95_low':lo,'ci95_high':hi,'subject_count':len(set(left[0]['subject_id'])),'seed_count':3,'bootstrap_replicates':REPS})
 # compact required derived tables from paired results
 for exp in EXPS:
  for c in CONDITIONS:
   def get(m,v='UNCALIBRATED'):
    return next(r for r in paired if r['experiment_id']==exp and r['condition']==c and r['metric']==m and r['probability_variant']==v)
   if c in ('C3','C4','C5','C1','C2','C0'):
    r=get('macro-F1'); stage.append({'experiment_id':exp,'condition':c,'metric':'macro-F1','b0_point':r['b0_point'],'b1_point':r['b1_point'],'delta':r['delta_b1_minus_b0'],'ci95_low':r['ci95_low'],'ci95_high':r['ci95_high']})
   if c in ('C4','C5'):
    n=get('NLL','SOURCE_TEMPERATURE_SCALED'); a=get('AURC'); u=get('ERROR_AUROC'); compound.append({'experiment_id':exp,'condition':c,'b0_macro_F1':get('macro-F1')['b0_point'],'b1_macro_F1':get('macro-F1')['b1_point'],'macro_F1_delta':get('macro-F1')['delta_b1_minus_b0'],'macro_F1_ci95_low':get('macro-F1')['ci95_low'],'macro_F1_ci95_high':get('macro-F1')['ci95_high'],'b0_NLL':n['b0_point'],'b1_NLL':n['b1_point'],'NLL_delta':n['delta_b1_minus_b0'],'b0_entropy_AURC':a['b0_point'],'b1_entropy_AURC':a['b1_point'],'AURC_delta':a['delta_b1_minus_b0'],'b0_error_AUROC':u['b0_point'],'b1_error_AUROC':u['b1_point'],'error_AUROC_delta':u['delta_b1_minus_b0'],'predictive_direction':'SUPPORTED_IMPROVEMENT' if get('macro-F1')['ci95_low']>0 else ('SUPPORTED_DEGRADATION' if get('macro-F1')['ci95_high']<0 else 'INCONCLUSIVE_DIRECTION'),'practical_magnitude':'PRACTICALLY_NOTABLE_GAIN' if get('macro-F1')['delta_b1_minus_b0']>=.02 else ('PRACTICALLY_NOTABLE_LOSS' if get('macro-F1')['delta_b1_minus_b0']<=-.02 else 'SMALL_MAGNITUDE'),'reliability_persistence':'MIXED_RELIABILITY_RESPONSE'})
 csvw(ROOT/'reports/b1_primary_results_multiseed_v1.csv',own); csvw(ROOT/'reports/b1_vs_b0_paired_results_v1.csv',paired); csvw(ROOT/'reports/b1_vs_b0_stage_analysis_v1.csv',stage); csvw(ROOT/'reports/b1_vs_b0_compound_failure_matrix_v1.csv',compound)
 csvw(ROOT/'reports/step15_data_access_audit.csv',access,['phase','dataset','source_role','purpose','operation','subject_id','recording_id','path'])
 (ROOT/'reports/b1_statistical_hashes_v1.txt').write_text('artifact,sha256\n'+'\n'.join(f'{p},{sha(ROOT/p)}' for p in ('reports/b1_primary_results_multiseed_v1.csv','reports/b1_vs_b0_paired_results_v1.csv','reports/b1_vs_b0_compound_failure_matrix_v1.csv','reports/b1_vs_b0_stage_analysis_v1.csv','reports/b1_vs_b0_confusion_analysis_v1.csv','reports/b1_isruc_montage_sensitivity_v1.csv'))+'\n')
 gate={'evaluation_gate':'B1_PRIMARY_EVALUATION_COMPLETE','calibration_gate':'B1_SOURCE_CALIBRATION_FROZEN','temperatures':6,'aps_objects':6,'prediction_bundles':36,'bootstrap_replicates':REPS,'bootstrap_seed':BOOT_SEED,'access_roles':sorted(set((r['phase'],r['source_role']) for r in access)),'oracle_analysis':False,'retraining':False}
 (ROOT/'reports/step15_b1_evaluation_gate.json').write_text(json.dumps(gate,indent=2,sort_keys=True)+'\n')
 print(json.dumps(gate,sort_keys=True))
if __name__=='__main__': main()
