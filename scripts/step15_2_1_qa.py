import csv,hashlib,json
from pathlib import Path
import numpy as np
from shiftsleep_uq.statistics.weighted_bootstrap import *
from shiftsleep_uq.evaluation_step11 import softmax,aps_prediction_set
root=Path('.')
# frozen draw audit
audit=[]
for line in Path('reports/b1_bootstrap_draw_hashes_v1.txt').read_text().splitlines()[1:]:
 pop,n,reps,seed,expected=line.split(',')
 if pop.endswith('_SOURCE_TEST'): direction=pop[:-len('_SOURCE_TEST')]; condition='SOURCE_TEST'
 else: direction=pop[:-len('_COMPLETE_TARGET')]; condition='COMPLETE_TARGET'
 key=direction+'__'+condition
 with np.load('artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz') as z: a=z[key]
 digest=hashlib.sha256(a.tobytes()).hexdigest()
 ok=(a.shape==(int(reps),int(n)) and a.dtype.kind in 'iu' and np.all(a>=0) and np.all(a.sum(1)==int(n)) and seed=='2028' and digest==expected)
 audit.append(dict(population=key,subject_count=n,replicates=reps,seed=seed,sha256=digest,status='PASS' if ok else 'FAIL'))
with open('reports/step15_2_1_bootstrap_draw_audit.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=audit[0]); w.writeheader(); w.writerows(audit)
# deterministic synthetic equivalence
rng=np.random.default_rng(1521); metrics=['macro-F1','NLL','Brier','ECE','ERROR_AUROC','ERROR_AUPRC','AURC']
errs={m:[] for m in metrics+['coverage','gap','mean_set_size']}
for _ in range(100):
 ns=int(rng.integers(3,8)); n=int(rng.integers(ns*2,ns*5)); sid=np.array([f'S{i}' for i in np.concatenate([np.arange(ns),rng.integers(0,ns,size=n-ns)])]); p=rng.dirichlet(np.ones(5),size=n); y=rng.integers(0,5,size=n); x=prepare(y,p,sid); m=rng.integers(0,4,size=ns,dtype=np.int64); m[0]=0; m[1]=1; m[2]=2; z=literal(x,m); ones=np.ones(len(z.subject_ids),dtype=np.int64)
 vals={'macro-F1':confusion_metrics(weighted_confusion(x,m))['macro-F1'],'NLL':nll(x,m),'Brier':brier(x,m),'ECE':ece(x,m),**ranking(x,m)}
 ref={'macro-F1':confusion_metrics(weighted_confusion(z,ones))['macro-F1'],'NLL':nll(z,ones),'Brier':brier(z,ones),'ECE':ece(z,ones),**ranking(z,ones)}
 for k in metrics: errs[k].append(abs(vals[k]-ref[k]))
 sets=rng.random((n,5))>.5; sets[np.arange(n),y]=True; cz=conformal(x,m,sets,.1); zz=conformal(z,ones,np.repeat(sets,m[x.subject_index],axis=0),.1)
 for k,a,b in [('coverage',cz['empirical_coverage'],zz['empirical_coverage']),('gap',cz['coverage_gap'],zz['coverage_gap']),('mean_set_size',cz['mean_set_size'],zz['mean_set_size'])]: errs[k].append(abs(a-b))
with open('reports/step15_2_1_synthetic_equivalence.csv','w',newline='') as f:
 fields=['metric','cases','max_absolute_error','mean_absolute_error','failures','status']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
 for k,v in errs.items(): w.writerow(dict(metric=k,cases=100,max_absolute_error=max(v),mean_absolute_error=np.mean(v),failures=sum(e>1e-12 for e in v),status='PASS' if max(v)<=1e-12 else 'FAIL'))
# real B1 and B0 checks
real=[]; b0=[]
configs=[('D1_SLEEPEDF_TO_ISRUC','C0',20),('D1_SLEEPEDF_TO_ISRUC','C3',10),('D2_ISRUC_TO_SLEEPEDF','C0',20),('D2_ISRUC_TO_SLEEPEDF','C3',10)]
with np.load('artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz') as draws_npz: 
 for direction,cond,reps in configs:
  pth=root/f'artifacts/predictions/b1_moddrop/{direction}/seed_17/{cond}.npz'; q=np.load(pth,allow_pickle=False); probs=softmax(q['logits']); x=prepare(q['labels'],probs,q['subject_id']); key=direction+'__'+('SOURCE_TEST' if cond=='C0' else 'COMPLETE_TARGET'); draws=draws_npz[key][:reps]; aps=json.loads((root/f'artifacts/calibration/b1_moddrop/{direction}/seed_17/aps.json').read_text()); sets=aps_prediction_set(probs,aps['alpha_0.10_qhat'])
  for r,m in enumerate(draws):
   z=literal(x,m); ones=np.ones(len(z.subject_ids),dtype=np.int64); cx=conformal(x,m,sets,.1); zs=np.repeat(sets,m[x.subject_index],axis=0); cz=conformal(z,ones,zs,.1); a={'macro-F1':confusion_metrics(weighted_confusion(x,m))['macro-F1'],'NLL':nll(x,m),'Brier':brier(x,m),'ECE':ece(x,m),**ranking(x,m),'coverage':cx['empirical_coverage'],'mean_set_size':cx['mean_set_size']}; bb={'macro-F1':confusion_metrics(weighted_confusion(z,ones))['macro-F1'],'NLL':nll(z,ones),'Brier':brier(z,ones),'ECE':ece(z,ones),**ranking(z,ones),'coverage':cz['empirical_coverage'],'mean_set_size':cz['mean_set_size']}
   for metric in a: real.append(dict(model='B1',experiment=direction,seed=17,condition=cond,replicate=r,metric=metric,optimized_value=a[metric],literal_value=bb[metric],absolute_error=abs(a[metric]-bb[metric]),tolerance=1e-12,pass_=abs(a[metric]-bb[metric])<=1e-12))
with open('reports/step15_2_1_real_equivalence.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=real[0]); w.writeheader(); w.writerows(real)
with np.load('artifacts/statistics/b0/bootstrap_replicates_v1_1.npz',allow_pickle=False) as ref, np.load('artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz') as draws_npz:
 for direction,cond,reps in configs:
  key=direction+'__'+('SOURCE_TEST' if cond=='C0' else 'COMPLETE_TARGET'); draws=draws_npz[key][:reps]
  bundles=[]
  for bseed in (17,42,2026):
   q=np.load(root/f'artifacts/predictions/b0/{direction}/seed_{bseed}/{cond}.npz',allow_pickle=False); bundles.append(prepare(q['labels'],softmax(q['logits']),q['subject_id']))
  for r,m in enumerate(draws):
   vals={'macro-F1':np.mean([confusion_metrics(weighted_confusion(xb,m))['macro-F1'] for xb in bundles])}
   for metric in ['ERROR_AUROC','ERROR_AUPRC','AURC']: vals[metric]=np.mean([ranking(xb,m)[metric] for xb in bundles])
   wanted=['macro-F1','ERROR_AUROC','ERROR_AUPRC','AURC'] if cond=='C0' else ['ERROR_AUROC','ERROR_AUPRC','AURC']
   for metric in wanted:
    auth=ref[f'{direction}_{cond}_{metric}'][r]; err=abs(vals[metric]-auth); b0.append(dict(experiment=direction,condition=cond,metric=metric,replicate=r,authoritative_value=auth,engine_value=vals[metric],absolute_error=err,tolerance=1e-10,status='PASS' if err<=1e-10 else 'FAIL'))
with open('reports/step15_2_1_b0_v1_1_regression.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=b0[0]); w.writeheader(); w.writerows(b0)
print('DRAW',all(r['status']=='PASS' for r in audit),audit)
print('SYN',[(k,max(v),sum(e>1e-12 for e in v)) for k,v in errs.items()])
print('REAL',len(real),sum(not r['pass_'] for r in real))
print('B0',len(b0),sum(r['status']=='FAIL' for r in b0),max(r['absolute_error'] for r in b0))
