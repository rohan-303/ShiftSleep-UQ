from pathlib import Path
import csv,json,numpy as np
ROOT=Path(__file__).resolve().parents[1]; EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); SEEDS=(17,42,2026);CONDS=('C0','C1','C2','C3','C4','C5')
def b(e,s,c,kind):
 with np.load(ROOT/f'artifacts/predictions/{kind}/{e}/seed_{s}/{c}.npz',allow_pickle=False) as z:return {k:z[k] for k in z.files}
def write(p,rows):
 with open(ROOT/p,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def cm(d):
 y=d['labels'];p=d['logits'].argmax(1);return np.array([[np.sum((y==i)&(p==j)) for j in range(5)] for i in range(5)],float)
def recall(d,i):
 q=cm(d);return q[i,i]/q[i].sum() if q[i].sum() else np.nan
# Full 25-cell row-normalized confusion deltas, mean across model seeds.
rows=[]
for e in EXPS:
 for c in CONDS:
  cb=np.mean([cm(b(e,s,c,'b1_moddrop'))/np.maximum(cm(b(e,s,c,'b1_moddrop')).sum(1,keepdims=True),1) for s in SEEDS],axis=0)
  ca=np.mean([cm(b(e,s,c,'b0'))/np.maximum(cm(b(e,s,c,'b0')).sum(1,keepdims=True),1) for s in SEEDS],axis=0)
  for i in range(5):
   for j in range(5): rows.append({'experiment_id':e,'condition':c,'true_class':i,'predicted_class':j,'b0_row_normalized':ca[i,j],'b1_row_normalized':cb[i,j],'b1_minus_b0':cb[i,j]-ca[i,j]})
write('reports/b1_vs_b0_confusion_analysis_v1.csv',rows)
# Stage recall bootstrap CIs using subject-level weighted class recall.
with np.load(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_subject_multiplicities_v1.npz') as dz: draws={k:dz[k] for k in dz.files}
def recall_reps(d,dr,i):
 sid=d['subject_id'];subs=sorted(set(sid.tolist()));ix=np.array([subs.index(x) for x in sid]); y=d['labels'];p=d['logits'].argmax(1); den=np.bincount(ix,weights=(y==i),minlength=len(subs));num=np.bincount(ix,weights=((y==i)&(p==i)),minlength=len(subs));w=dr;return (w@num)/np.maximum(w@den,1)
rows=[]
for e in EXPS:
 for c in CONDS:
  pop='COMPLETE_TARGET' if c in ('C3','C4','C5') else 'SOURCE_TEST'; dr=draws[f'{e}__{pop}'];
  for i,name in enumerate(('Wake','N1','N2','N3','REM')):
   bv=[recall(b(e,s,c,'b1_moddrop'),i) for s in SEEDS]; av=[recall(b(e,s,c,'b0'),i) for s in SEEDS]; d=np.mean([recall_reps(b(e,s,c,'b1_moddrop'),dr,i) for s in SEEDS],axis=0)-np.mean([recall_reps(b(e,s,c,'b0'),dr,i) for s in SEEDS],axis=0);rows.append({'experiment_id':e,'condition':c,'stage':name,'b0_point':float(np.mean(av)),'b1_point':float(np.mean(bv)),'delta':float(np.mean(bv)-np.mean(av)),'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5))})
write('reports/b1_vs_b0_stage_analysis_v1.csv',rows)
# B1-vs-B0 interactions from bootstrap vectors.
with np.load(ROOT/'artifacts/statistics/b1_moddrop/bootstrap_replicates_v1.npz') as z:b1={k:z[k] for k in z.files}
with np.load(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_2.npz') as z:b0={k:z[k] for k in z.files}
rows=[]
for e in EXPS:
 for m in ('macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1'):
  for mod,x,y,u,v in [('EEG','C4','C3','C1','C0'),('EOG','C5','C3','C2','C0')]:
   ib1=(b1[f'{e}_{x}_{m}']-b1[f'{e}_{y}_{m}'])-(b1[f'{e}_{u}_{m}']-b1[f'{e}_{v}_{m}']);ib0=(b0[f'{e}_{x}_{m}']-b0[f'{e}_{y}_{m}'])-(b0[f'{e}_{u}_{m}']-b0[f'{e}_{v}_{m}']);d=ib1-ib0;rows.append({'experiment_id':e,'modality':mod,'metric':m,'b1_interaction':float(np.mean(ib1)),'b0_interaction':float(np.mean(ib0)),'interaction_b1_minus_b0':float(np.mean(d)),'ci95_low':float(np.percentile(d,2.5)),'ci95_high':float(np.percentile(d,97.5))})
write('reports/b1_vs_b0_interaction_analysis_v1.csv',rows)
# Residual reliability classification from primary axes.
paired=list(csv.DictReader(open(ROOT/'reports/b1_vs_b0_paired_results_v1.csv'))); comp=[]
for e in EXPS:
 for c in ('C4','C5'):
  get=lambda m,v='UNCALIBRATED':next(r for r in paired if r['experiment_id']==e and r['condition']==c and r['metric']==m and r['probability_variant']==v)
  mf=get('macro-F1');n=get('NLL','SOURCE_TEMPERATURE_SCALED');a=get('AURC');g=get('gap_0.1'); axes={'calibration':float(n['ci95_high'])<0,'selective':float(a['ci95_high'])<0,'conformal':float(g['ci95_high'])<0}; wors={'calibration':float(n['ci95_low'])>0,'selective':float(a['ci95_low'])>0,'conformal':float(g['ci95_low'])>0}; good=sum(axes.values()); bad=sum(wors.values());
  if good>=2 and bad==0: lab='RELIABILITY_IMPROVES_WITH_PREDICTION'
  elif good>=1 and bad>=1: lab='MIXED_RELIABILITY_RESPONSE'
  elif (float(mf['ci95_low'])>0 or float(mf['delta_b1_minus_b0'])>=.02) and good<2: lab='RELIABILITY_FAILURE_PERSISTS'
  else: lab='NOT_IDENTIFIABLE'
  comp.append({'experiment_id':e,'condition':c,'macro_F1_delta':mf['delta_b1_minus_b0'],'macro_F1_ci95_low':mf['ci95_low'],'macro_F1_ci95_high':mf['ci95_high'],'NLL_delta':n['delta_b1_minus_b0'],'NLL_ci95_low':n['ci95_low'],'NLL_ci95_high':n['ci95_high'],'AURC_delta':a['delta_b1_minus_b0'],'AURC_ci95_low':a['ci95_low'],'AURC_ci95_high':a['ci95_high'],'conformal_gap_delta':g['delta_b1_minus_b0'],'conformal_gap_ci95_low':g['ci95_low'],'conformal_gap_ci95_high':g['ci95_high'],'calibration_axis':'IMPROVES' if axes['calibration'] else ('WORSENS' if wors['calibration'] else 'INCONCLUSIVE'),'selective_axis':'IMPROVES' if axes['selective'] else ('WORSENS' if wors['selective'] else 'INCONCLUSIVE'),'conformal_axis':'IMPROVES' if axes['conformal'] else ('WORSENS' if wors['conformal'] else 'INCONCLUSIVE'),'predictive_direction':'SUPPORTED_IMPROVEMENT' if float(mf['ci95_low'])>0 else ('SUPPORTED_DEGRADATION' if float(mf['ci95_high'])<0 else 'INCONCLUSIVE_DIRECTION'),'practical_magnitude':'PRACTICALLY_NOTABLE_GAIN' if float(mf['delta_b1_minus_b0'])>=.02 else ('PRACTICALLY_NOTABLE_LOSS' if float(mf['delta_b1_minus_b0'])<=-.02 else 'SMALL_MAGNITUDE'),'residual_reliability':lab})
write('reports/b1_vs_b0_compound_failure_matrix_v1.csv',comp);print('postprocess',len(rows),len(comp))
