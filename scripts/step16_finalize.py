import csv,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src')); sys.path.insert(0,str(ROOT/'scripts'))
from shiftsleep_uq.evaluation_step11 import softmax, nll,brier,ece,conformal_metrics
from shiftsleep_uq.step11_1_statistics import weighted_metric_replicates,percentile_interval
from step12_baseline_diagnosis import bootstrap_ece
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); CMASK={'C0':'FULL','C1':'EEG_ONLY','C2':'EOG_ONLY','C3':'FULL','C4':'EEG_ONLY','C5':'EOG_ONLY'}
def bundle(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def loadj(p):return json.loads(p.read_text())
def probdata(d,p):return {**d,'logits':np.log(np.clip(p,1e-12,1)).astype(np.float32)}
def main():
 z=np.load(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz'); rows=[]
 for exp in EXPS:
  for c in ('C0','C1','C2','C3','C4','C5'):
   pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; dr=z[f'{exp}__{pop}'];
   for metric in ('NLL','Brier','ECE','abs_gap_0.10'):
    seed_d=[]
    for seed in SEEDS:
     d=bundle(ROOT/'artifacts/predictions/b1_moddrop'/exp/f'seed_{seed}'/f'{c}.npz'); g=loadj(ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'temperature.json'); ga=loadj(ROOT/'artifacts/calibration/b1_moddrop'/exp/f'seed_{seed}'/'aps.json'); m=CMASK[c]; s=loadj(ROOT/'artifacts/calibration/step16_source_mask'/exp/f'seed_{seed}'/m/'temperature.json'); sa=loadj(ROOT/'artifacts/calibration/step16_source_mask'/exp/f'seed_{seed}'/m/'aps.json');
     pg=softmax(d['logits']/g['temperature']); ps=softmax(d['logits']/s['temperature']); y=d['labels'];
     if metric=='NLL': ag=weighted_metric_replicates(probdata(d,pg),'NLL',dr); ass=weighted_metric_replicates(probdata(d,ps),'NLL',dr); pointg=nll(pg,y); points=nll(ps,y)
     elif metric=='Brier': ag=weighted_metric_replicates(probdata(d,pg),'Brier',dr); ass=weighted_metric_replicates(probdata(d,ps),'Brier',dr); pointg=brier(pg,y); points=brier(ps,y)
     elif metric=='ECE': ag=bootstrap_ece(d,pg,dr); ass=bootstrap_ece(d,ps,dr); pointg=ece(pg,y); points=ece(ps,y)
     else:
      def gap(q):
       return weighted_metric_replicates({**d,'logits':np.log(np.clip(softmax(d['logits']),1e-12,1)).astype(np.float32)},'gap_0.1',dr,qhat=q,alpha=.10)
      ag=gap(ga['alpha_0.10_qhat']); ass=gap(sa['alpha_0.10_qhat']); pointg=abs(conformal_metrics(softmax(d['logits']),y,ga['alpha_0.10_qhat'],.1)['coverage_gap']); points=abs(conformal_metrics(softmax(d['logits']),y,sa['alpha_0.10_qhat'],.1)['coverage_gap'])
     seed_d.append((ag,ass,pointg,points))
    diff=np.mean([x[1]-x[0] for x in seed_d],axis=0); lo,hi=percentile_interval(diff); rows.append({'experiment_id':exp,'condition':c,'metric':metric,'original_b1_source_global_full':float(np.mean([x[2] for x in seed_d])),'b1_source_mask_specific':float(np.mean([x[3] for x in seed_d])),'delta_mask_minus_global':float(np.mean([x[3]-x[2] for x in seed_d])),'paired_ci95_low':float(lo),'paired_ci95_high':float(hi),'favorable_direction':'LOWER_IS_BETTER','bootstrap_replicates':2000,'bootstrap_seed':2028,'calibration_scope':'SOURCE_CALIBRATION_ONLY'})
 with open(ROOT/'reports/step16_source_mask_calibration_comparison_v1.csv','w',newline='') as f:
  fields=list(rows[0]); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
 # enrich residual matrix with aggregate B1 ranking values from frozen Step 15.3 paired result
 p=[]
 with open(ROOT/'reports/b1_vs_b0_paired_results_v1.csv') as f:
  for r in csv.DictReader(f):
   if r['condition'] in ('C4','C5') and r['probability_variant']=='UNCALIBRATED' and r['metric'] in ('ERROR_AUROC','ERROR_AUPRC','AURC'): p.append(r)
 rank={(r['experiment_id'],r['condition'],r['metric']):float(r['b1_point']) for r in p}
 with open(ROOT/'reports/step16_residual_failure_matrix_v1.csv') as f:r=list(csv.DictReader(f))
 for x in r:
  for m,col in [('ERROR_AUROC','b1_AUROC'),('ERROR_AUPRC','b1_AUPRC'),('AURC','b1_AURC')]: x[col]=rank[(x['experiment_id'],x['condition'],m)]
 with open(ROOT/'reports/step16_residual_failure_matrix_v1.csv','w',newline='') as f:
  fields=list(r[0]); w=csv.DictWriter(f,fieldnames=fields); w.writeheader();w.writerows(r)
if __name__=='__main__':main()
