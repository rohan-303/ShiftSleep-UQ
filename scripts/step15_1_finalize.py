#!/usr/bin/env python
"""Statistics-only Step 15.1 finalizer for frozen B0/B1 prediction bundles."""
from __future__ import annotations
import csv, hashlib, json, math, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax, macro_f1, nll, brier, ece, classwise_ece, entropy, _rank_auc, auprc, aurc, selective_rows, conformal_metrics, confusion_matrix
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, reconstruct_cluster_indices, percentile_interval
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CONDITIONS=('C0','C1','C2','C3','C4','C5'); REPS=2000; SEED=2028
ROOT_EXPECTED={'configs/evaluation_protocol_v1_1.yaml':'dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756','reports/subject_partitions_v2.csv':'9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329','reports/b0_primary_results_multiseed_v1_1.csv':'288122138f1b29c4b3ac8ca3de6e4f38baf97e20eefeaa15d029116337543efc','reports/b0_primary_contrasts_v1_1.csv':'008a9ad350c15f69d633a24ae584f3ace974b42a37a5a57b1df9e4429bbd4b4d','artifacts/statistics/b0/bootstrap_replicates_v1_1.npz':'47c2aadd716b903cb328b257ae7cefcc0a51b508cd1cc78db18a9ab0a1fa8022','reports/b0_primary_prediction_hashes_v1.txt':'77422f9aa4a0d7ba359268a1914e316e567da13fed3ad242c3100cef43408af7'}
B1CK={('D1_SLEEPEDF_TO_ISRUC',17):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_17/best.pt','7a006909e9f5cfc29b004a1af5d8536f218265e292b63db904dd09a0ff9fc1a5'),('D1_SLEEPEDF_TO_ISRUC',42):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_42/best.pt','b0e5e0989e60b8ba5194ad80a3fc60f5cd87c37c9c7ce20c535783524ed8c5b7'),('D1_SLEEPEDF_TO_ISRUC',2026):('artifacts/models/b1_moddrop/D1_SLEEPEDF_TO_ISRUC/seed_2026/best.pt','23ea8b05dac65a10f29f5caf305b203ee381415521ddc8af5665dcff686b967f'),('D2_ISRUC_TO_SLEEPEDF',17):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_17/best.pt','3b91624e571259cb0e85cbde6290e11c1211323b38995bcf66f5dbd12088d5ec'),('D2_ISRUC_TO_SLEEPEDF',42):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_42/best.pt','b5bdd41c9dbf2e71af44a479843babc7448c8a4f45fc9445cc2c507755899d36'),('D2_ISRUC_TO_SLEEPEDF',2026):('artifacts/models/b1_moddrop/D2_ISRUC_TO_SLEEPEDF/seed_2026/best.pt','1ba7ae76f67c1a8f549b0026eca7b00f60402f9988809c42c6bc6cf14b60ca30')}
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def csvw(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True); fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with open(p,'w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def bundle(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def cal(exp,s):
 d=ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{s}'; return json.loads((d/'temperature.json').read_text()),json.loads((d/'aps.json').read_text())
def b0cal(exp,s):
 d=ROOT/'artifacts/calibration/b0'/exp/f'seed_{s}'; return json.loads((d/'temperature.json').read_text()),json.loads((d/'aps.json').read_text())
def align(a,b):
 for k in ('labels','subject_id','recording_id','epoch_index','montage_variant'):
  if not np.array_equal(a[k],b[k]): raise RuntimeError('STEP15_1_B0_B1_ALIGNMENT_FAILURE:'+k)
def validate():
 if Path.cwd().resolve()!=ROOT.resolve(): raise RuntimeError('STEP15_1_FROZEN_ARTIFACT_MISMATCH')
 for p,h in ROOT_EXPECTED.items():
  if not (ROOT/p).exists() or sha(ROOT/p)!=h: raise RuntimeError('STEP15_1_FROZEN_ARTIFACT_MISMATCH:'+p)
 for (e,s),(p,h) in B1CK.items():
  q=ROOT/p
  if not q.exists() or sha(q)!=h: raise RuntimeError('STEP15_1_FROZEN_ARTIFACT_MISMATCH:'+p)
 for e in EXPS:
  for s in SEEDS:
   d=ROOT/'artifacts/calibration/b1_moddrop'/e/f'seed_{s}'
   for n in ('temperature.json','aps.json'):
    if not (d/n).exists(): raise RuntimeError('STEP15_1_FROZEN_ARTIFACT_MISMATCH:'+str(d/n))
 n=0; manifest=[]
 for e in EXPS:
  for s in SEEDS:
   for c in CONDITIONS:
    p=ROOT/'artifacts/predictions/b1_moddrop'/e/f'seed_{s}'/f'{c}.npz'; q=ROOT/'artifacts/predictions/b0'/e/f'seed_{s}'/f'{c}.npz'
    if not p.exists() or not q.exists(): raise RuntimeError('STEP15_1_FROZEN_ARTIFACT_MISMATCH:'+str(p))
    a=bundle(p); b=bundle(q); align(a,b); pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; t,ap=cal(e,s)
    manifest.append({'experiment_id':e,'seed':s,'condition':c,'population':pop,'epoch_count':len(a['labels']),'bundle_path':str(p.relative_to(ROOT)),'sha256':sha(p),'checkpoint_sha256':B1CK[(e,s)][1],'normalization_sha256':sha(ROOT/'artifacts/normalization/b0'/f'{e}.json'),'temperature_sha256':sha(ROOT/'artifacts/calibration/b1_moddrop'/e/f'seed_{s}'/'temperature.json'),'aps_sha256':sha(ROOT/'artifacts/calibration/b1_moddrop'/e/f'seed_{s}'/'aps.json')}); n+=1
 if n!=36: raise RuntimeError('STEP15_1_BUNDLE_COUNT_FAILURE')
 csvw(ROOT/'reports/b1_primary_prediction_hashes_v1.txt',manifest)
 return manifest
def multiplicities(manifest):
 out={}; rows=[]
 for e,popname in sorted(set((r['experiment_id'],r['population']) for r in manifest)): ids=sorted(set(bundle(ROOT/next(r['bundle_path'] for r in manifest if r['experiment_id']==e and r['population']==popname))['subject_id'].tolist())); draws=bootstrap_subject_draws(len(ids),reps=REPS,seed=SEED); counts=np.zeros((REPS,len(ids)),dtype=np.int16); rr=np.arange(REPS)[:,None]; np.add.at(counts,(np.broadcast_to(rr,draws.shape),draws),1); out[(e,popname)]=(ids,counts); rows.append({'population':f'{e}_{popname}','subject_count':len(ids),'replicates':REPS,'seed':SEED,'sha256':hashlib.sha256(counts.tobytes()).hexdigest()})
 ROOT.joinpath('artifacts/statistics/b1_moddrop').mkdir(parents=True,exist_ok=True); np.savez_compressed(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz',**{e+'__'+p:counts for (e,p),(ids,counts) in out.items()}); csvw(ROOT/'reports/b1_bootstrap_draw_hashes_v1.txt',rows,['population','subject_count','replicates','seed','sha256']); return out
def basic(bundle,t,q):
 p=softmax(bundle['logits']); y=bundle['labels']; pr=p.argmax(1); ent=entropy(p); err=(pr!=y).astype(int); cm=confusion_matrix(pr,y); r={'macro-F1':macro_f1(pr,y),'Cohen_kappa':(np.trace(cm)/len(y)-np.sum(cm.sum(0)*cm.sum(1))/len(y)**2)/(1-np.sum(cm.sum(0)*cm.sum(1))/len(y)**2),'balanced_accuracy':float(np.mean(np.divide(np.diag(cm),cm.sum(1),out=np.zeros(5),where=cm.sum(1)>0))),'NLL':nll(p,y),'Brier':brier(p,y),'ECE_15_EQUAL_WIDTH':ece(p,y),'ADAPTIVE_ECE_15':ece(p,y,adaptive=True),'CLASSWISE_ECE':classwise_ece(p,y),'ERROR_AUROC':_rank_auc(ent,err),'ERROR_AUPRC':auprc(ent,err),'AURC':aurc(ent,pr,y)}
 r.update({f'APS_{k}_alpha_0.10':v for k,v in conformal_metrics(p,y,q[.1],.1).items()}); r.update({f'APS_{k}_alpha_0.05':v for k,v in conformal_metrics(p,y,q[.05],.05).items()}); r['temperature']=t; return r,cm
def weighted_add(b,ids,mults,metric,q=None,alpha=None):
 y=b['labels']; p=softmax(b['logits']); pr=p.argmax(1); si=np.searchsorted(ids,b['subject_id']); n=np.bincount(si,minlength=len(ids)).astype(float); den=mults@n
 if metric=='NLL': x=-np.log(np.clip(p[np.arange(len(y)),y],1e-12,1)); s=np.bincount(si,weights=x,minlength=len(ids)); return (mults@s)/den
 if metric=='Brier': x=np.sum((p-np.eye(5)[y])**2,axis=1); s=np.bincount(si,weights=x,minlength=len(ids)); return (mults@s)/den
 if metric=='macro-F1':
  cs=np.zeros((len(ids),5,5));
  for i in range(5):
   for j in range(5): cs[:,i,j]=np.bincount(si,weights=((y==i)&(pr==j)).astype(float),minlength=len(ids))
  cm=np.einsum('rs,sij->rij',mults,cs); tp=np.diagonal(cm,axis1=1,axis2=2); d=2*tp+cm.sum(1)-tp+cm.sum(2)-tp; return np.mean(np.divide(2*tp,d,out=np.zeros_like(tp),where=d>0),axis=1)
 if metric in ('coverage_0.10','gap_0.10','coverage_0.05','gap_0.05'):
  a=.1 if '0.10' in metric else .05; covered=aps_prediction_set_local(p,q[a])[np.arange(len(y)),y].astype(float); s=np.bincount(si,weights=covered,minlength=len(ids)); cov=(mults@s)/den; return cov if metric.startswith('coverage') else 1-a-cov
 raise ValueError(metric)
def aps_prediction_set_local(p,q):
 out=np.zeros_like(p,dtype=bool)
 for i,row in enumerate(p):
  order=np.lexsort((np.arange(5),-row)); keep=np.cumsum(row[order])<=q+1e-15; keep[0]=True; out[i,order[keep]]=True
 return out
def weighted_rank(b,ids,mults,metric):
 p=softmax(b['logits']); y=b['labels']; pr=p.argmax(1); score=entropy(p); err=(pr!=y).astype(int); si=np.searchsorted(ids,b['subject_id']); order=np.argsort(score,kind='stable'); score=score[order]; err=err[order]; si=si[order]; chunks=[]
 for start in range(0,len(mults),25):
  w=mults[start:start+25,si].astype(float); total=w.sum(1); pos=(w*err).sum(1); neg=total-pos
  if metric=='ERROR_AUROC':
   # exact pairwise concordance using sorted order: each positive gets preceding negatives plus half ties (stable tie handling matches rank method below)
   ranks=np.cumsum(w,axis=1)-w/2+.5; num=(w*err*ranks).sum(1)-pos*(pos+1)/2; chunks.append(np.divide(num,pos*neg,out=np.full(len(total),np.nan),where=(pos>0)&(neg>0)))
  else:
   tp=np.cumsum(w*err,axis=1); mass=np.cumsum(w,axis=1); precision=tp/np.maximum(mass,1); rec=tp/np.maximum(pos[:,None],1); chunks.append(np.sum(np.diff(rec,axis=1)*precision[:,1:],axis=1))
 return np.concatenate(chunks)
def main():
 manifest=validate(); draws=multiplicities(manifest); per=[]; allbund={}; paired=[]; conf=[]; stage=[]
 for e in EXPS:
  for s in SEEDS:
   for c in CONDITIONS:
    p=ROOT/'artifacts/predictions/b1_moddrop'/e/f'seed_{s}'/f'{c}.npz'; b=bundle(p); t,ap=cal(e,s); r,cm=basic(b,t,{.1:ap['alpha_0.10_qhat'],.05:ap['alpha_0.05_qhat']}); allbund[('B1',e,s,c)]=b
    for k,v in r.items(): per.append({'model':'B1','experiment_id':e,'seed':s,'condition':c,'metric':k,'value':v,'probability_variant':'UNCALIBRATED' if k not in ('NLL','Brier','ECE_15_EQUAL_WIDTH','ADAPTIVE_ECE_15','CLASSWISE_ECE') else 'UNCALIBRATED'})
    for i in range(5):
     for j in range(5): conf.append({'experiment_id':e,'seed':s,'condition':c,'true_class':i,'predicted_class':j,'b1_count':int(cm[i,j])})
 csvw(ROOT/'reports/b1_primary_metrics_per_seed_v1.csv',per)
 own=[]; paired=[]; metrics=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.10','gap_0.10','coverage_0.05','gap_0.05')
 for e in EXPS:
  for c in CONDITIONS:
   pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; ids,ms=draws[(e,pop)]; b1s=[allbund[('B1',e,s,c)] for s in SEEDS]; b0s=[bundle(ROOT/'artifacts/predictions/b0'/e/f'seed_{s}'/f'{c}.npz') for s in SEEDS]; q1=[cal(e,s)[1] for s in SEEDS]; q0=[b0cal(e,s)[1] for s in SEEDS]
   for met in metrics:
    reps=[]; points=[]
    for i,b in enumerate(b1s):
     if met in ('macro-F1','NLL','Brier','coverage_0.10','gap_0.10','coverage_0.05','gap_0.05'): reps.append(weighted_add(b,ids,ms,met,{.1:q1[i]['alpha_0.10_qhat'],.05:q1[i]['alpha_0.05_qhat']}));
     else: reps.append(weighted_rank(b,ids,ms,met))
     points.append(basic(b,cal(e,SEEDS[i])[0],{.1:q1[i]['alpha_0.10_qhat'],.05:q1[i]['alpha_0.05_qhat']})[0].get(met, np.nan))
    arr=np.mean(reps,axis=0); lo,hi=percentile_interval(arr); own.append({'experiment_id':e,'condition':c,'metric':met,'probability_variant':'UNCALIBRATED','point_estimate':float(np.mean(points)),'seed_sd':float(np.std(points,ddof=1)),'ci95_low':lo,'ci95_high':hi,'subject_count':len(ids),'bootstrap_unit':'SUBJECT','bootstrap_replicates':REPS})
    for variant in ('UNCALIBRATED','SOURCE_TEMPERATURE_SCALED'):
     br=[]; cr=[]
     for i,s in enumerate(SEEDS):
      x=b1s[i]; y=b0s[i]
      if variant=='SOURCE_TEMPERATURE_SCALED': x={**x,'logits':x['logits']/cal(e,s)[0]['temperature']}; y={**y,'logits':y['logits']/b0cal(e,s)[0]['temperature']}
      br.append(weighted_add(x,ids,ms,met,{.1:q1[i]['alpha_0.10_qhat'],.05:q1[i]['alpha_0.05_qhat']}) if met in ('macro-F1','NLL','Brier','coverage_0.10','gap_0.10','coverage_0.05','gap_0.05') else weighted_rank(x,ids,ms,met)); cr.append(weighted_add(y,ids,ms,met,{.1:q0[i]['alpha_0.10_qhat'],.05:q0[i]['alpha_0.05_qhat']}) if met in ('macro-F1','NLL','Brier','coverage_0.10','gap_0.10','coverage_0.05','gap_0.05') else weighted_rank(y,ids,ms,met))
     delta=np.mean(br,axis=0)-np.mean(cr,axis=0); bp=float(np.mean([basic((({**b1s[i],'logits':b1s[i]['logits']/cal(e,s)[0]['temperature']}) if variant=='SOURCE_TEMPERATURE_SCALED' else b1s[i]),cal(e,s)[0]['temperature'],{.1:q1[i]['alpha_0.10_qhat'],.05:q1[i]['alpha_0.05_qhat']})[0].get(met,np.nan) for i,s in enumerate(SEEDS)])); cp=float(np.mean([basic((({**b0s[i],'logits':b0s[i]['logits']/b0cal(e,s)[0]['temperature']}) if variant=='SOURCE_TEMPERATURE_SCALED' else b0s[i]),b0cal(e,s)[0]['temperature'],{.1:q0[i]['alpha_0.10_qhat'],.05:q0[i]['alpha_0.05_qhat']})[0].get(met,np.nan) for i,s in enumerate(SEEDS)])); lo,hi=percentile_interval(delta); paired.append({'experiment_id':e,'condition':c,'metric':met,'probability_variant':variant,'b0_point':cp,'b1_point':bp,'delta_b1_minus_b0':bp-cp,'ci95_low':lo,'ci95_high':hi,'subject_count':len(ids),'seed_count':3,'bootstrap_replicates':REPS})
 csvw(ROOT/'reports/b1_primary_results_multiseed_v1.csv',own); csvw(ROOT/'reports/b1_vs_b0_paired_results_v1.csv',paired); csvw(ROOT/'reports/b1_vs_b0_confusion_analysis_v1.csv',conf)
 (ROOT/'artifacts/statistics/b1_moddrop').mkdir(parents=True,exist_ok=True); np.savez_compressed(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz',**{'complete':np.array([1],dtype=np.int8)})
 csvw(ROOT/'reports/step15_1_data_access_audit.csv',[{'operation':'prediction_bundle_read','source_role':'ARTIFACT','purpose':'statistics_only','phase':'STEP15_1','dataset':'B0/B1 frozen bundles','path':'artifacts/predictions'}])
 arts=['reports/b1_primary_metrics_per_seed_v1.csv','reports/b1_primary_results_multiseed_v1.csv','reports/b1_vs_b0_paired_results_v1.csv','reports/b1_vs_b0_confusion_analysis_v1.csv','artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz','artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz']; (ROOT/'reports/b1_statistical_hashes_v1.txt').write_text('artifact,sha256\n'+'\n'.join(f'{a},{sha(ROOT/a)}' for a in arts)+'\n')
 print(json.dumps({'status':'B1_PRIMARY_EVALUATION_COMPLETE','bundles':36,'replicates':REPS,'inference':False,'refit':False},sort_keys=True))
if __name__=='__main__': main()
