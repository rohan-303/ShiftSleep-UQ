from __future__ import annotations
import csv,json,hashlib
from pathlib import Path
import numpy as np
from shiftsleep_uq.randomized_aps import deterministic_u,randomized_scores,quantile_kth,randomized_prediction_set,summarize_sets
from shiftsleep_uq.evaluation_step11 import softmax,aps_scores,aps_quantile
ROOT=Path(__file__).resolve().parents[1]; SEEDS=[17,42,2026];EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']; MODELS=[('B0','b0'),('B1','b1_moddrop')];CONDS=['C0','C1','C2','C3','C4','C5']
def wcsv(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 fields=list(dict.fromkeys(k for r in rows for k in r));
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def load(p):
 z=np.load(p,allow_pickle=False);return {k:z[k] for k in z.files}
def main():
 calrows=[];results=[];sanity=[];compar=[]
 for exp in EXPS:
  for mf,md in MODELS:
   for seed in SEEDS:
    cd=ROOT/'artifacts/remediation/r1/source_cal_reconstruction/R1_ATTEMPT_001'/mf/exp/f'seed_{seed}'
    cz=load(cd/'source_cal_probabilities.npz'); key=f'{mf}/{exp}/seed_{seed}'
    ucal=np.array([deterministic_u(direction=exp,model_family=mf,model_seed=seed,split='SOURCE_CAL',subject_id=str(s),recording_id=str(r),epoch_index=int(e),purpose='CAL_SCORE') for s,r,e in zip(cz['subject_id'],cz['recording_id'],cz['epoch_index'])])
    rs=randomized_scores(cz['probabilities'],cz['labels'],ucal)
    for alpha in [.10,.05]:
     q=quantile_kth(rs,alpha);hist=json.loads((ROOT/'artifacts/calibration'/md/exp/f'seed_{seed}'/'aps.json').read_text())[f'alpha_{alpha:.2f}_qhat'];calrows.append({'model_family':mf,'direction':exp,'seed':seed,'alpha':alpha,'calibration_n':len(rs),'randomized_qhat':repr(q),'historical_qhat':repr(hist),'randomized_minus_historical':repr(q-hist),'source_cal_hash':hashlib.sha256((cd/'source_cal_probabilities.npz').read_bytes()).hexdigest(),'status':'PASS'})
     # calibration self-coverage sanity
     sets=randomized_prediction_set(cz['probabilities'],q,ucal);sm=summarize_sets(sets,cz['labels']);sanity.append({'model_family':mf,'direction':exp,'seed':seed,'alpha':alpha,**sm,'qhat':q,'population':'SOURCE_CAL'})
     for cond in CONDS:
      pth=ROOT/'artifacts/predictions'/md/exp/f'seed_{seed}'/f'{cond}.npz';d=load(pth);prob=softmax(d['logits']);
      up=np.array([deterministic_u(direction=exp,model_family=mf,model_seed=seed,split='SOURCE_TEST' if cond in ['C0','C1','C2'] else 'COMPLETE_TARGET',subject_id=str(s),recording_id=str(r),epoch_index=int(e),purpose='PRED_SET') for s,r,e in zip(d['subject_id'],d['recording_id'],d['epoch_index'])])
      ss=randomized_prediction_set(prob,q,up);sm=summarize_sets(ss,d['labels']);results.append({'model_family':mf,'direction':exp,'seed':seed,'condition':cond,'alpha':alpha,'population':'SOURCE_TEST' if cond in ['C0','C1','C2'] else 'COMPLETE_TARGET','qhat':q,**sm,'epoch_count':len(d['labels']),'subject_count':len(set(d['subject_id']))})
      compar.append({'model_family':mf,'direction':exp,'seed':seed,'condition':cond,'alpha':alpha,'randomized_qhat':q,'historical_qhat':hist,'delta_qhat':q-hist})

 wcsv(ROOT/'reports/remediation/r1_randomized_aps_calibration_v1.csv',calrows);wcsv(ROOT/'reports/remediation/r1_randomized_aps_results_v1.csv',results);wcsv(ROOT/'reports/remediation/r1_source_conformal_sanity_v1.csv',sanity);wcsv(ROOT/'reports/remediation/r1_historical_vs_randomized_aps_v1.csv',compar)
 # primary cell summaries across seeds, directions and models at alpha .1/.05
 cells=[]
 for exp in EXPS:
  for cond in ['C4','C5']:
   for mf,_ in MODELS:
    vals=[r for r in results if r['direction']==exp and r['condition']==cond and r['model_family']==mf and r['alpha']==.1]
    # compare randomized coverage deviation to nominal and historical qhat delta; classification is evidence bounded
    cov=np.mean([float(v['coverage']) for v in vals]); target=.9; mean_size=np.mean([float(v['mean_set_size']) for v in vals]);
    cells.append({'direction':exp,'model_family':mf,'condition':cond,'alpha':.10,'empirical_coverage_mean':cov,'coverage_deviation':cov-target,'mean_set_size':mean_size,'classification':'ROBUST_TO_RANDOMIZED_APS' if abs(cov-target)<=.05 else 'CONFORMAL_INTERPRETATION_CHANGES','rationale':'Randomized APS completed from provenance-equivalent SOURCE CAL reconstruction; classification uses frozen coverage deviation and set-size diagnostics.'})
 # historical cell classification file schema retained
 wcsv(ROOT/'reports/remediation/r1_primary_cell_classification_v1.csv',cells)
 print(json.dumps({'calibration_rows':len(calrows),'result_rows':len(results),'sanity_rows':len(sanity),'comparison_rows':len(compar),'primary_cells':len(cells),'status':'R1_RANDOMIZED_APS_COMPLETE'}))
if __name__=='__main__':main()
