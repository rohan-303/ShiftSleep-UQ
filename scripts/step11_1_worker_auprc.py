import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from step11_1_statistical_qa import load,qhats
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws,weighted_metric_replicates
ex,c=sys.argv[1:3]; seeds=(17,42,2026); ds=[load(ex,s,c) for s in seeds]; n=len(set(ds[0]['subject_id'].tolist())); draws=bootstrap_subject_draws(n,reps=2000,seed=2028)
a=[]
for i,d in enumerate(ds): a.append(weighted_metric_replicates(d,'ERROR_AUPRC',draws))
z=np.load(Path('artifacts/statistics/b0')/f'qa_worker_{ex}_{c}.npz',allow_pickle=False); out={k:z[k] for k in z.files}; out['ERROR_AUPRC']=np.nanmean(np.stack(a),axis=0); np.savez_compressed(Path('artifacts/statistics/b0')/f'qa_worker_{ex}_{c}.npz',**out)
print('updated',ex,c)
