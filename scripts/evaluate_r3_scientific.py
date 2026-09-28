from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import numpy as np,torch
from shiftsleep_uq.models.seqsleepnet_class import SeqSleepNetClass
from shiftsleep_uq.evaluation_step11 import softmax,fit_temperature,aps_scores,aps_quantile,compute_metric_rows
from shiftsleep_uq.remediation.datasets import RemediationManifestDataset,overlay_path
from shiftsleep_uq.training.datasets import source_dataset_for_experiment
from run_r3_scientific import SeqDS,eval_model
ROOT=Path(__file__).resolve().parents[1];PHASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b';EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];VARS=['S0','S1'];SEEDS=[17,42,2026];CONDS=['C0','C1','C2','C3','C4','C5']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ds_for(exp,role,purpose):
 dataset=source_dataset_for_experiment(exp) if role!='COMPLETE_TARGET' else ('isruc_s1' if exp=='D1_SLEEPEDF_TO_ISRUC' else 'sleep_edf_sc');d=RemediationManifestDataset(dataset,role,purpose,root=ROOT);d.records=[(overlay_path(p,d.dataset),i,s,r,m) for p,i,s,r,m in d.records];return d
def load(exp,var,seed,device):
 import csv
 rows=list(csv.DictReader((ROOT/'reports/remediation/r3_checkpoint_manifest_v1.csv').open()));r=next(x for x in rows if x['job_id']==f'R3_{exp}_{var}_SEED_{seed}' and x['status']=='COMPLETE');p=ROOT/'artifacts/remediation/r3'/r['job_id']/f"ATTEMPT_{int(r['attempt']):03d}"/'best.pt';z=torch.load(p,map_location=device,weights_only=False);m=SeqSleepNetClass().to(device).float();m.load_state_dict(z['model_state_dict']);m.eval();return m,r,p
def main():
 if sha(ROOT/'configs/postreview_remediation_protocol_v2.yaml')!=PHASH:raise RuntimeError('R3_PROTOCOL_HASH_FAILURE')
 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu');metrics=[];calrows=[];preds={};cal={}
 for exp in EXPS:
  norm=json.loads((ROOT/'artifacts/remediation/normalization/r3'/f'{exp}.json').read_text());calds=ds_for(exp,'CALIBRATION','calibration');test=ds_for(exp,'TEST','evaluation_test');target=ds_for(exp,'COMPLETE_TARGET','evaluation_target')
  for var in VARS:
   for seed in SEEDS:
    m,meta,cp=load(exp,var,seed,device);cd=SeqDS(calds,norm,1);c=eval_model(m,cd,device,exp,var,seed,int(meta['best_epoch']),condition='C0');t=fit_temperature(c['logits'],c['labels'],role='CALIBRATION');q={a:aps_quantile(aps_scores(softmax(c['logits']),c['labels']),a) for a in [.1,.05]};cal[(exp,var,seed)]={'temperature':t['temperature'],'q':q};calrows.append({'experiment':exp,'variant':var,'seed':seed,'temperature':t['temperature'],'calibration_NLL_before':t['initial_nll'],'calibration_NLL_after':t['final_nll'],'calibration_count':len(c['labels']),'checkpoint_sha256':sha(cp)})
    for cond in CONDS:
     d=test if cond in ('C0','C1','C2') else target;ed=SeqDS(d,norm,1);z=eval_model(m,ed,device,exp,var,seed,int(meta['best_epoch']),condition=cond);p=ROOT/'artifacts/remediation/r3'/f'R3_{exp}_{var}_SEED_{seed}'/f"ATTEMPT_{int(meta['attempt']):03d}"/'predictions'/f'{cond}.npz';p.parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(p,**z);preds[(exp,var,seed,cond)]=z
     rows,_=compute_metric_rows(z['logits'],z['labels'],cal[(exp,var,seed)]['temperature'],cal[(exp,var,seed)]['q'])
     for r in rows:metrics.append({'experiment':exp,'variant':var,'seed':seed,'condition':cond,'population':'SOURCE_TEST' if cond in ('C0','C1','C2') else 'COMPLETE_TARGET',**r,'prediction_sha256':sha(p)})
 with (ROOT/'reports/remediation/r3_temperature_calibration_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(calrows[0]));w.writeheader();w.writerows(calrows)
 with (ROOT/'reports/remediation/r3_primary_results_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in metrics for k in r)));w.writeheader();w.writerows(metrics)
 print(json.dumps({'calibration_groups':len(calrows),'metric_rows':len(metrics),'prediction_bundles':len(preds)}))
if __name__=='__main__':main()
