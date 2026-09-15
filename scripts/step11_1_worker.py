#!/usr/bin/env python
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from step11_1_statistical_qa import load,qhats
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws,weighted_metric_replicates
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026); METRICS=('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05')
ex,c=sys.argv[1:3]; ds=[load(ex,s,c) for s in SEEDS]; pop='SOURCE_TEST' if c in ('C0','C1','C2') else 'COMPLETE_TARGET'; subjects=len(set(ds[0]['subject_id'].tolist())); draws=bootstrap_subject_draws(subjects,reps=2000,seed=2028); out={}
for m in METRICS:
  reps=[weighted_metric_replicates(d,m,draws,qhat=qhats(ex,SEEDS[i])[float(m.split('_')[-1])] if m.startswith(('coverage_','gap_')) else None,alpha=float(m.split('_')[-1]) if m.startswith(('coverage_','gap_')) else None) for i,d in enumerate(ds)]
  out[m]=np.nanmean(np.stack(reps),axis=0)
np.savez_compressed(Path('artifacts/statistics/b0')/f'qa_worker_{ex}_{c}.npz',**out)
print(ex,c,'done')
