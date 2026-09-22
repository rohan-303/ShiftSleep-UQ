from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import numpy as np,torch
from torch.utils.data import DataLoader
from shiftsleep_uq.training.datasets import build_source_dataset
from shiftsleep_uq.models.baseline_b0 import BaselineB0
from shiftsleep_uq.evaluation_step11 import softmax,aps_scores,aps_quantile
ROOT=Path(__file__).resolve().parents[1]; DEVICE=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']; SEEDS=[17,42,2026]; MODELS=['b0','b1_moddrop']; OUT=ROOT/'artifacts/remediation/r1/source_cal_reconstruction/R1_ATTEMPT_001'; OUT.mkdir(parents=True,exist_ok=False)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(exp,model):
 p=ROOT/'artifacts/normalization/b0'/f'{exp}.json'
 a=json.loads(p.read_text()); return {'EEG':{'mean':a['EEG_mean'],'std':a['EEG_std'],'std_epsilon':a['epsilon']},'EOG':{'mean':a['EOG_mean'],'std':a['EOG_std'],'std_epsilon':a['epsilon']}},sha(p)
def ckpt(model,exp,seed):
 p=ROOT/'artifacts/models'/model/exp/f'seed_{seed}'/'best.pt';return p,sha(p)
def run():
 rows=[]
 for exp in EXPS:
  for model_id,model_dir in [('B0','b0'),('B1','b1_moddrop')]:
   for seed in SEEDS:
    ds=build_source_dataset(exp,'CALIBRATION','calibration',root=ROOT);n,nh=norm(exp,model_dir);ds.set_normalization(n)
    p,ch=ckpt(model_dir,exp,seed);payload=torch.load(p,map_location=DEVICE,weights_only=False);m=BaselineB0().to(DEVICE).float().eval();m.load_state_dict(payload['model_state_dict'])
    logits=[];labels=[];subjects=[];recordings=[];epochs=[]
    for b in DataLoader(ds,batch_size=128,shuffle=False,num_workers=0):
     with torch.no_grad(): logits.append(m(b['eeg'].to(DEVICE),b['eog'].to(DEVICE),torch.ones(len(b['label']),2,device=DEVICE)).cpu().numpy())
     labels.append(b['label'].numpy());subjects.extend(b['subject_id']);recordings.extend(b['recording_id']);epochs.extend(b['epoch_index'].numpy().tolist())
    log=np.concatenate(logits).astype(np.float32);y=np.concatenate(labels).astype(np.int8);prob=softmax(log);scores=aps_scores(prob,y)
    assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=1e-7)
    d=OUT/model_id/exp/f'seed_{seed}';d.mkdir(parents=True)
    np.savez_compressed(d/'source_cal_probabilities.npz',probabilities=prob,labels=y,subject_id=np.asarray(subjects),recording_id=np.asarray(recordings),epoch_index=np.asarray(epochs,dtype=np.int32),scores=scores)
    hist=json.loads((ROOT/'artifacts/calibration'/model_dir/exp/f'seed_{seed}'/'aps.json').read_text())
    for alpha in [.10,.05]:
     q=aps_quantile(scores,alpha); expected=hist[f'alpha_{alpha:.2f}_qhat']; rows.append({'model_family':model_id,'direction':exp,'seed':seed,'alpha':alpha,'calibration_n':len(y),'quantile_rank_k':min(max(int(np.ceil((len(y)+1)*(1-alpha))),1),len(y)),'reconstructed_qhat':repr(q),'historical_qhat':repr(expected),'absolute_difference':repr(abs(q-expected)),'checkpoint_sha256':ch,'normalization_sha256':nh,'source_subject_count':len(set(subjects)),'source_recording_count':len(set(recordings)),'observation_identity_complete':True,'probability_rows_finite':True,'probability_row_sum_pass':True,'status':'PROVENANCE_EQUIVALENT_RECONSTRUCTION' if abs(q-expected)<=1e-10 else 'RECONSTRUCTION_MISMATCH'})
    del m;torch.cuda.empty_cache()
 with (ROOT/'reports/remediation/r1_source_cal_reconstruction_audit_v1.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 (OUT/'protocol_hash.txt').write_text('c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b\n');(OUT/'completion.marker').write_text(json.dumps({'status':'COMPLETED','scientific_execution':'ARTIFACT_RECONSTRUCTION_INFERENCE','rows':len(rows)}))
 print(json.dumps({'rows':len(rows),'equivalent':sum(r['status']=='PROVENANCE_EQUIVALENT_RECONSTRUCTION' for r in rows),'mismatches':sum(r['status']=='RECONSTRUCTION_MISMATCH' for r in rows)},indent=2))
if __name__=='__main__':run()
