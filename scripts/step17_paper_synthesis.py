#!/usr/bin/env python
"""Step 17: deterministic paper tables, figures, provenance, and evidence maps.
No training, inference, calibration fitting, oracle fitting, or new tests.
"""
from __future__ import annotations
import csv, hashlib, json, math, os, subprocess
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'; TABLE=REPORT/'paper_tables'; SUPP=TABLE/'supplement'; FIG=REPORT/'paper_figures'; FDIR=FIG/'figures'; FDATA=FIG/'source_data'
EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); CONDS=('C0','C1','C2','C3','C4','C5'); SEEDS=(17,42,2026)
EXP_LABEL={'D1_SLEEPEDF_TO_ISRUC':'D1 Sleep-EDF → ISRUC','D2_ISRUC_TO_SLEEPEDF':'D2 ISRUC → Sleep-EDF'}
COND_LABEL={'C0':'known/full','C1':'known/EEG-only','C2':'known/EOG-only','C3':'unseen/full','C4':'unseen/EEG-only','C5':'unseen/EOG-only'}

def readcsv(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def writecsv(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True); fields=fields or (list(rows[0]) if rows else [])
 with open(p,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def sha(p):
 h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def f(x): return f'{float(x):.6f}'
def figsave(fig, name):
 FDIR.mkdir(parents=True,exist_ok=True); fig.savefig(FDIR/f'{name}.pdf',bbox_inches='tight'); fig.savefig(FDIR/f'{name}.png',dpi=300,bbox_inches='tight'); plt.close(fig)
def record_fig(name,script,inputs,metric_version='frozen_step17_deterministic'):
 row={'figure_id':name,'script':script,'input_files':';'.join(inputs),'input_hashes':';'.join(f'{p}={sha(ROOT/p)}' for p in inputs),'output_pdf':str((FDIR/f'{name}.pdf').relative_to(ROOT)),'output_pdf_sha256':sha(FDIR/f'{name}.pdf'),'output_png':str((FDIR/f'{name}.png').relative_to(ROOT)),'output_png_sha256':sha(FDIR/f'{name}.png'),'generation_timestamp_utc':'2026-09-18','metric_version':metric_version,'b0_version':'v1_2'}; return row

def main():
 TABLE.mkdir(parents=True,exist_ok=True); SUPP.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True); FDATA.mkdir(parents=True,exist_ok=True)
 # Frozen input tables.
 b0seed=readcsv(REPORT/'b0_primary_metrics_per_seed_v1.csv'); b0res=readcsv(REPORT/'b0_primary_results_multiseed_v1_2.csv'); b1res=readcsv(REPORT/'b1_primary_results_multiseed_v1.csv'); pair=readcsv(REPORT/'b1_vs_b0_paired_results_v1.csv'); stage=readcsv(REPORT/'b1_vs_b0_stage_analysis_v1.csv'); conf=readcsv(REPORT/'b1_vs_b0_confusion_analysis_v1.csv'); inter=readcsv(REPORT/'b1_vs_b0_interaction_analysis_v1.csv'); montage=readcsv(REPORT/'b1_isruc_montage_sensitivity_v1.csv'); mask=readcsv(REPORT/'step16_source_mask_calibration_comparison_v1.csv'); oracle=readcsv(REPORT/'step16_b1_oracle_diagnostics_v1.csv'); residual=readcsv(REPORT/'step16_residual_failure_matrix_v1.csv')
 # Table 1: partition-derived design counts.
 parts=readcsv(REPORT/'subject_partitions_v2.csv'); counts={}
 for r in parts: counts[(r['dataset'],r['source_role'])]=counts.get((r['dataset'],r['source_role']),0)+1
 t1=[]
 for exp,src,tgt in [('D1_SLEEPEDF_TO_ISRUC','sleep_edf_sc','isruc_s1'),('D2_ISRUC_TO_SLEEPEDF','isruc_s1','sleep_edf_sc')]:
  t1.append({'direction':exp,'source_dataset':src,'target_dataset':tgt,'source_train_subjects':counts.get((src,'TRAIN'),0),'source_dev_subjects':counts.get((src,'DEV'),0),'source_calibration_subjects':counts.get((src,'CALIBRATION'),0),'source_test_subjects':counts.get((src,'SOURCE_TEST'),0),'target_subjects':counts.get((tgt,'TARGET'),0),'channels':'EEG + EOG','source_montage':'dataset-specific frozen montage','target_montage':'dataset-specific frozen montage','conditions':'C0 full-known; C1 EEG-known; C2 EOG-known; C3 full-unseen; C4 EEG-unseen; C5 EOG-unseen','seeds':'17, 42, 2026'})
 writecsv(TABLE/'table1_benchmark_design.csv',t1)
 # Table 2 from B0 per-seed metric means, frozen v1.2 primary source for inferential fields.
 wanted=[('macro-F1','UNCALIBRATED','macro_F1'),('NLL','SOURCE_TEMPERATURE_SCALED','NLL'),('Brier','SOURCE_TEMPERATURE_SCALED','Brier'),('ERROR_AUROC','UNCALIBRATED','ERROR_AUROC'),('ERROR_AUPRC','UNCALIBRATED','ERROR_AUPRC'),('AURC','UNCALIBRATED','AURC'),('APS_empirical_coverage_alpha_0.10','UNCALIBRATED','coverage_alpha_0.10'),('APS_coverage_gap_alpha_0.10','UNCALIBRATED','abs_gap_alpha_0.10'),('APS_mean_set_size_alpha_0.10','UNCALIBRATED','mean_set_size_alpha_0.10')]
 by={(r['experiment_id'],r['condition'],r['metric'],r['probability_variant']):[] for r in b0seed}
 for r in b0seed: by.setdefault((r['experiment_id'],r['condition'],r['metric'],r['probability_variant']),[]).append(float(r['value']))
 t2=[]
 for exp in EXPS:
  for c in CONDS:
   row={'direction':exp,'condition':c}
   for metric,var,col in wanted:
    vals=by.get((exp,c,metric,var),[])
    row[col]=f(np.mean(vals)) if vals else 'NOT_AVAILABLE_IN_B0_PER_SEED_TABLE'
   t2.append(row)
 writecsv(TABLE/'table2_b0_primary_shift_results.csv',t2)
 # Table 3 paired compound effects.
 pmap={(r['experiment_id'],r['condition'],r['metric'],r['probability_variant']):r for r in pair}
 labels={('D1_SLEEPEDF_TO_ISRUC','C4'):'MIXED_RELIABILITY_RESPONSE',('D1_SLEEPEDF_TO_ISRUC','C5'):'RELIABILITY_IMPROVES_WITH_PREDICTION',('D2_ISRUC_TO_SLEEPEDF','C4'):'RELIABILITY_IMPROVES_WITH_PREDICTION',('D2_ISRUC_TO_SLEEPEDF','C5'):'MIXED_RELIABILITY_RESPONSE'}
 t3=[]
 for exp,c in [('D1_SLEEPEDF_TO_ISRUC','C4'),('D1_SLEEPEDF_TO_ISRUC','C5'),('D2_ISRUC_TO_SLEEPEDF','C4'),('D2_ISRUC_TO_SLEEPEDF','C5')]:
  m=pmap[(exp,c,'macro-F1','UNCALIBRATED')]; n=pmap[(exp,c,'NLL','SOURCE_TEMPERATURE_SCALED')]; a=pmap[(exp,c,'AURC','UNCALIBRATED')]; u=pmap[(exp,c,'gap_0.1','UNCALIBRATED')]
  r=next(x for x in residual if x['experiment_id']==exp and x['condition']==c)
  t3.append({'direction':exp,'condition':c,'b0_macro_F1':f(m['b0_point']),'b1_macro_F1':f(m['b1_point']),'macro_F1_delta':f(m['delta_b1_minus_b0']),'macro_F1_ci95':f"[{float(m['ci95_low']):+.5f},{float(m['ci95_high']):+.5f}]",'predictive_status':'SUPPORTED_IMPROVEMENT' if float(m['ci95_low'])>0 else 'INCONCLUSIVE_DIRECTION','NLL_delta':f(n['delta_b1_minus_b0']),'NLL_ci95':f"[{float(n['ci95_low']):+.5f},{float(n['ci95_high']):+.5f}]",'AURC_delta':f(a['delta_b1_minus_b0']),'AURC_ci95':f"[{float(a['ci95_low']):+.5f},{float(a['ci95_high']):+.5f}]",'conformal_abs_gap_delta':f(u['delta_b1_minus_b0']),'residual_label':labels[(exp,c)]})
 writecsv(TABLE/'table3_b1_vs_b0_compound_effects.csv',t3)
 # Table 4.
 t4=[]
 for exp,c in labels:
  rr=next(x for x in residual if x['experiment_id']==exp and x['condition']==c); mm=next(x for x in readcsv(REPORT/'step16_method_authorization_matrix_v1.csv') if x['experiment_id']==exp and x['condition']==c)
  t4.append({'direction':exp,'condition':c,'predictive_confound_status':mm['predictive_confounded_status'],'b1_residual_label':labels[(exp,c)],'simple_mask_calibration':mm['simple_calibration_status'],'oracle_recoverability':mm['oracle_status'],'method_gate_implication':mm['method_authorization']})
 writecsv(TABLE/'table4_residual_diagnosis.csv',t4)
 # Supplementary copies / source evidence.
 supps={'all_b0_v1_2_results.csv':b0res,'all_b1_results.csv':b1res,'b1_vs_b0_paired_results.csv':pair,'stage_level_effects.csv':stage,'confusion_changes.csv':conf,'interaction_contrasts.csv':inter,'montage_sensitivity.csv':montage,'source_mask_calibration.csv':mask,'oracle_diagnostics.csv':oracle,'b0_v1_1_to_v1_2_repair_audit.csv':readcsv(REPORT/'b0_v1_2_affected_transition_audit.csv') if (REPORT/'b0_v1_2_affected_transition_audit.csv').exists() else [{'status':'SOURCE_ARTIFACT_NOT_PRESENT_IN_EXPECTED_NAME','source':'Step 15.2.3 repair report and v1.2 hashes'}]}
 for name,rows in supps.items(): writecsv(SUPP/name,rows)
 # Figure source data.
 writecsv(FDATA/'fig3_compound_macro_f1.csv',t3); writecsv(FDATA/'fig4_reliability_axes.csv',[{'direction':r['direction'],'condition':r['condition'],'NLL_delta':r['NLL_delta'],'AURC_delta':r['AURC_delta'],'conformal_abs_gap_delta':r['conformal_abs_gap_delta']} for r in t3]); writecsv(FDATA/'fig8_stage_recall_changes.csv',stage)
 # Fig 1 schematic.
 fig,ax=plt.subplots(figsize=(11,6)); ax.axis('off'); ax.set_xlim(0,11);ax.set_ylim(0,6)
 boxes=[(0.3,4.4,2.4,1.0,'Source dataset\nTRAIN / DEV / CAL / TEST'),(4.3,4.4,2.4,1.0,'Frozen B0 / B1\nFULL · EEG-only · EOG-only'),(8.3,4.4,2.4,1.0,'Target dataset\nC3 / C4 / C5'),(1.3,1.4,3.0,1.1,'D1\nSleep-EDF → ISRUC'),(6.7,1.4,3.0,1.1,'D2\nISRUC → Sleep-EDF')]
 for x,y,w,h,s in boxes: ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04',fc='#e8f0f7',ec='#34526f',lw=1.5)); ax.text(x+w/2,y+h/2,s,ha='center',va='center',fontsize=11)
 for x1,y1,x2,y2 in [(2.7,4.9,4.3,4.9),(6.7,4.9,8.3,4.9),(4.3,4.6,4.0,2.5),(6.7,4.6,7.0,2.5)]: ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='->',mutation_scale=15,color='#607d8b'))
 ax.text(5.5,3.3,'subject-level bootstrap\nB0 v1.2 + B1 control',ha='center',fontsize=12,fontweight='bold'); figsave(fig,'fig1_shift_design')
 # Fig 2 B0 landscape.
 metrics=[('macro-F1','macro-F1','UNCALIBRATED'),('NLL','NLL','SOURCE_TEMPERATURE_SCALED'),('AURC','AURC','UNCALIBRATED'),('abs gap','APS_coverage_gap_alpha_0.10','UNCALIBRATED')]
 fig,axs=plt.subplots(2,2,figsize=(12,8),sharex=True)
 for ax,(title,met,var) in zip(axs.flat,metrics):
  for exp,style in zip(EXPS,('-o','-s')):
   vals=[]
   for c in CONDS:
    candidates=[r for r in b0seed if r['experiment_id']==exp and r['condition']==c and r['metric']==met and r['probability_variant']==var]
    vals.append(np.mean([float(r['value']) for r in candidates]) if candidates else np.nan)
   ax.plot(CONDS,vals,style,label=exp[:2])
  ax.set_title(title);ax.grid(alpha=.25);ax.set_ylabel('value');ax.legend()
 fig.suptitle('B0 v1.2 shift landscape'); figsave(fig,'fig2_b0_shift_landscape')
 # Fig 3 forest.
 fig,ax=plt.subplots(figsize=(8,4.5)); y=np.arange(4); ds=[float(r['macro_F1_delta']) for r in t3]; lo=[float(r['macro_F1_ci95'].split(',')[0].strip('[')) for r in t3]; hi=[float(r['macro_F1_ci95'].split(',')[1].strip(']')) for r in t3]; ax.errorbar(ds,y,xerr=[np.array(ds)-lo,np.array(hi)-np.array(ds)],fmt='o',capsize=4,color='#1f5a7a');ax.axvline(0,color='black',lw=1);ax.set_yticks(y,[f"{r['direction'][:2]} {r['condition']}" for r in t3]);ax.set_xlabel('B1 − B0 macro-F1');ax.set_title('Compound predictive robustness');ax.grid(axis='x',alpha=.25);figsave(fig,'fig3_b1_compound_macro_f1')
 # Fig 4 reliability axes.
 fig,axs=plt.subplots(1,3,figsize=(12,4),sharey=True); names=['NLL_delta','AURC_delta','conformal_abs_gap_delta']; titles=['Calibrated NLL','Entropy AURC','α=.10 abs coverage gap']
 for ax,n,t in zip(axs,names,titles):
  vals=[float(r[n]) for r in t3]; ax.axhline(0,color='black',lw=.8); ax.bar(np.arange(4),vals,color=['#4c78a8','#f58518','#54a24b','#e45756']);ax.set_xticks(range(4),[r['direction'][:2]+' '+r['condition'] for r in t3],rotation=35,ha='right');ax.set_title(t);ax.grid(axis='y',alpha=.2)
 fig.suptitle('Reliability axes do not move uniformly');figsave(fig,'fig4_compound_reliability_axes')
 # Fig 5 decoupling.
 fig,axs=plt.subplots(1,3,figsize=(12,4)); x=np.array([float(r['macro_F1_delta']) for r in t3]); labs=[r['direction'][:2]+' '+r['condition'] for r in t3]
 for ax,n,t in zip(axs,['NLL_delta','AURC_delta','conformal_abs_gap_delta'],['NLL','AURC','abs coverage gap']):
  yv=np.array([float(r[n]) for r in t3]); ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8);ax.scatter(x,yv);[ax.text(xi,yi,la,fontsize=8) for xi,yi,la in zip(x,yv,labs)];ax.set_xlabel('macro-F1 delta');ax.set_ylabel(t);ax.grid(alpha=.2)
 fig.suptitle('Predictive–reliability decoupling');figsave(fig,'fig5_prediction_reliability_decoupling')
 # Curves from frozen bundles.
 def curve(exp,seed,c):
  with np.load(ROOT/'artifacts/predictions/b1_moddrop'/exp/f'seed_{seed}'/f'{c}.npz',allow_pickle=False) as z: bl={k:z[k] for k in z.files}
  with np.load(ROOT/'artifacts/predictions/b0'/exp/f'seed_{seed}'/f'{c}.npz',allow_pickle=False) as z: b0={k:z[k] for k in z.files}
  out=[]
  for name,d in [('B0',b0),('B1',bl)]:
   p=np.exp(d['logits']-d['logits'].max(1,keepdims=True));p/=p.sum(1,keepdims=True);u=-np.sum(p*np.log(np.clip(p,1e-12,1)),1); order=np.argsort(u); err=(p.argmax(1)!=d['labels']).astype(float)[order]; cov=np.arange(1,len(err)+1)/len(err); risk=np.cumsum(err)/np.arange(1,len(err)+1); ix=np.linspace(0,len(err)-1,101).astype(int);out.append((name,cov[ix],risk[ix]))
  return out
 fig,axs=plt.subplots(2,2,figsize=(10,8),sharex=True,sharey=True)
 curve_inputs=[]
 for ax,(exp,c) in zip(axs.flat,[(EXPS[0],'C4'),(EXPS[0],'C5'),(EXPS[1],'C4'),(EXPS[1],'C5')]):
  for name,cov,risk in curve(exp,17,c): ax.plot(cov,risk,label=name)
  ax.set_title(exp[:2]+' '+c);ax.set_xlabel('coverage');ax.set_ylabel('risk');ax.grid(alpha=.2);ax.legend();
 fig.suptitle('Selective risk–coverage, seed 17, frozen predictions');figsave(fig,'fig6_selective_risk_coverage')
 # Fig 7 coverage/set size from B0 table rows.
 fig,axs=plt.subplots(1,2,figsize=(11,4));
 for exp,style in zip(EXPS,('-o','-s')):
  cov=[];size=[]
  for c in CONDS:
   rr=[r for r in b0seed if r['experiment_id']==exp and r['condition']==c and r['metric']=='APS_empirical_coverage_alpha_0.10' and r['probability_variant']=='UNCALIBRATED']; ss=[r for r in b0seed if r['experiment_id']==exp and r['condition']==c and r['metric']=='APS_mean_set_size_alpha_0.10' and r['probability_variant']=='UNCALIBRATED'];cov.append(np.mean([float(x['value']) for x in rr]));size.append(np.mean([float(x['value']) for x in ss]))
  axs[0].plot(CONDS,cov,style,label=exp[:2]);axs[1].plot(CONDS,size,style,label=exp[:2])
 axs[0].axhline(.9,color='black',ls='--');axs[0].set_title('Empirical coverage (α=.10)');axs[1].set_title('Mean set size (α=.10)');
 for ax in axs: ax.grid(alpha=.2);ax.legend();ax.set_xlabel('condition')
 fig.suptitle('Conformal transfer is empirical under shift');figsave(fig,'fig7_conformal_transfer')
 # Fig 8 stage heatmap C3-C5.
 stages=[r for r in stage if r['condition'] in ('C3','C4','C5')]; order=['Wake','N1','N2','N3','REM']; mat=np.array([[float(next(r['delta'] for r in stages if r['experiment_id']==e and r['condition']==c and r['stage']==s)) for c in ('C3','C4','C5')] for e in EXPS for s in order]); fig,ax=plt.subplots(figsize=(7,6));im=ax.imshow(mat,cmap='coolwarm',vmin=-.15,vmax=.15);ax.set_xticks(range(3),['C3','C4','C5']);ax.set_yticks(range(10),[e[:2]+' '+s for e in EXPS for s in order]);fig.colorbar(im,ax=ax,label='B1 − B0 recall');ax.set_title('Stage-level recall changes');figsave(fig,'fig8_stage_recall_changes')
 # Complete source-data set for every figure, including schematic/curve inputs.
 writecsv(FDATA/'fig1_shift_design.csv',t1); writecsv(FDATA/'fig2_b0_shift_landscape.csv',t2); writecsv(FDATA/'fig3_b1_compound_macro_f1.csv',t3); writecsv(FDATA/'fig4_compound_reliability_axes.csv',[{'direction':r['direction'],'condition':r['condition'],'NLL_delta':r['NLL_delta'],'AURC_delta':r['AURC_delta'],'conformal_abs_gap_delta':r['conformal_abs_gap_delta']} for r in t3]); writecsv(FDATA/'fig5_prediction_reliability_decoupling.csv',[{'direction':r['direction'],'condition':r['condition'],'macro_F1_delta':r['macro_F1_delta'],'NLL_delta':r['NLL_delta'],'AURC_delta':r['AURC_delta'],'conformal_abs_gap_delta':r['conformal_abs_gap_delta']} for r in t3]); writecsv(FDATA/'fig8_stage_recall_changes.csv',stage)
 curve_rows=[]
 for exp,c in [(e,c) for e in EXPS for c in ('C4','C5')]:
  for seed in (17,):
   for name,cov,risk in curve(exp,seed,c):
    for q,rr in zip(cov,risk): curve_rows.append({'direction':exp,'condition':c,'seed':seed,'model':name,'coverage':float(q),'risk':float(rr)})
 writecsv(FDATA/'fig6_selective_risk_coverage.csv',curve_rows); writecsv(FDATA/'fig7_conformal_transfer.csv',t2)

 fig_rows=[]; inputs=['reports/b0_primary_metrics_per_seed_v1.csv','reports/b1_vs_b0_paired_results_v1.csv','reports/b1_vs_b0_stage_analysis_v1.csv']
 for name in ['fig1_shift_design','fig2_b0_shift_landscape','fig3_b1_compound_macro_f1','fig4_compound_reliability_axes','fig5_prediction_reliability_decoupling','fig6_selective_risk_coverage','fig7_conformal_transfer','fig8_stage_recall_changes']: fig_rows.append(record_fig(name,'scripts/step17_paper_synthesis.py',inputs))
 writecsv(REPORT/'step17_figure_provenance_v1.csv',fig_rows)
 # Table provenance.
 table_rows=[]
 for p in [TABLE/'table1_benchmark_design.csv',TABLE/'table2_b0_primary_shift_results.csv',TABLE/'table3_b1_vs_b0_compound_effects.csv',TABLE/'table4_residual_diagnosis.csv']+[SUPP/x for x in supps]: table_rows.append({'table_id':p.stem,'path':str(p.relative_to(ROOT)),'input_files':';'.join(inputs),'input_hashes':';'.join(f'{q}={sha(ROOT/q)}' for q in inputs),'output_sha256':sha(p),'metric_version':'frozen_step17_deterministic','b0_version':'v1_2'})
 writecsv(REPORT/'step17_table_provenance_v1.csv',table_rows)
 # Maps, nonclaims, narrative, methods, limitations, contribution, title, abstract.
 hyp=[['F1','Source-only modality dropout improves missing-modality robustness','reports/b1_vs_b0_paired_results_v1.csv','macro-F1','D1 C4; D1 C5; D2 C4','SUPPORTED_WITH_DIRECTIONAL_LIMIT','Supported in three primary cells; D2 C5 inconclusive.'],['F2','Robustness gains are direction/modality dependent','reports/b1_vs_b0_compound_failure_matrix_v1.csv','macro-F1','D1/D2 C4/C5','SUPPORTED','Heterogeneity is retained.'],['F3','Predictive improvement does not guarantee uniform reliability improvement','reports/step16_residual_failure_matrix_v1.csv','NLL/AURC/conformal gap','four compound cells','SUPPORTED','Reliability families respond differently.'],['F4','Residual reliability behavior is heterogeneous','reports/step16_method_authorization_matrix_v1.csv','residual labels','four compound cells','SUPPORTED','No universal reliability conclusion.'],['F5','The B1 control does not justify changing protocol or authorizing a method','reports/step16_method_gate.json','method gate','all','SUPPORTED','Final gate is not authorized.'],['F6','A new reliability method is efficacious','NOT TESTED — METHOD NOT AUTHORIZED','N/A','N/A','NOT TESTED — METHOD NOT AUTHORIZED','No learned method was implemented.']]
 writecsv(REPORT/'step17_hypothesis_evidence_map_v1.csv',[dict(zip(['hypothesis','original_expectation','primary_artifact','supporting_metric','direction_condition','evidence_status','final_interpretation'],r)) for r in hyp])
 claims=[('C1','Compound dataset × modality shift degrades predictive and reliability behavior relative to known-domain operation.','reports/b0_primary_results_multiseed_v1_2.csv','macro-F1/NLL/AURC/conformal','D1/D2 C0-C5','PRIMARY_SUPPORTED','Direction and metric dependent.'),('C2','The severity and type of degradation depend on modality and transfer direction.','reports/b0_primary_results_multiseed_v1_2.csv','primary metric families','D1/D2 C0-C5','PRIMARY_SUPPORTED','Not universal.'),('C3','B1 improves compound predictive robustness in three of four primary cells.','reports/b1_vs_b0_paired_results_v1.csv','macro-F1 paired CI','D1 C4/C5; D2 C4','PRIMARY_SUPPORTED','D2 C5 inconclusive.'),('C4','Predictive improvement does not guarantee uniform reliability improvement.','reports/step16_residual_failure_matrix_v1.csv','NLL/AURC/conformal','four compound cells','PRIMARY_SUPPORTED','Heterogeneous residual labels.'),('C5','No practically notable B1 full-modality target tradeoff was observed.','reports/b1_vs_b0_paired_results_v1.csv','macro-F1 C3','D1/D2 C3','PRIMARY_SUPPORTED','Prere gistered guardrail.'),('C6','Simple source mask-specific calibration does not uniformly resolve residual reliability failures.','reports/step16_source_mask_calibration_comparison_v1.csv','NLL/Brier/ECE/conformal','four compound cells','SECONDARY_SUPPORTED','Diagnostic baseline only.'),('C7','Target-oracle calibration shows partial recoverability but not source-only deployability.','reports/step16_b1_oracle_diagnostics_v1.csv','oracle deltas','C3/C4/C5','DIAGNOSTIC_ONLY','Target labels are diagnostic only.'),('C8','Evidence does not justify an additional learned reliability model.','reports/step16_method_gate.json','method gate','all','PRIMARY_SUPPORTED','Reliability method not authorized.')]
 writecsv(REPORT/'step17_claim_evidence_matrix_v1.csv',[{'claim_id':a,'exact_claim_wording':b,'evidence_artifact':c,'metric':d,'condition':e,'ci':'see source artifact' if a in ('C1','C3','C5') else 'not applicable','allowed_section':'Results/Discussion' if g!='DIAGNOSTIC_ONLY' else 'Supplement','caveat':h,'classification':g} for a,b,c,d,e,g,h in claims])
 (REPORT/'step17_nonclaims_v1.md').write_text('# Step 17 Non-Claims\n\nShiftSleep-UQ does not demonstrate universal uncertainty failure, universal modality-dropout superiority, causality from montage type, clinical safety, generalization to all sleep datasets, formal conformal coverage under arbitrary shift, target-free recovery from all shifts, a novel calibration method, state-of-the-art sleep staging, a new architecture, SHHS validation, or performance on unevaluated populations. It does not claim a learned reliability method was implemented or effective.\n')
 (REPORT/'step17_results_narrative_map.md').write_text('# Results Narrative Map\n\n## Result 1\nB0 establishes compound-shift failure. Source: Table 2; Figure 2. Caveat: direction and metric dependent.\n\n## Result 2\nReliability families degrade differently. Source: Table 2; Figure 4. Caveat: empirical target transfer, not arbitrary-shift guarantee.\n\n## Result 3\nB1 improves predictive robustness in three of four cells. Source: Table 3; Figure 3. Caveat: D2 C5 is inconclusive.\n\n## Result 4\nReliability does not uniformly track predictive improvement. Source: Table 3/4; Figures 4–5. Caveat: mixed cell-level response.\n\n## Result 5\nSimple source calibration does not universally repair residuals. Source: Table 4; supplementary mask-control table.\n\n## Result 6\nOracle diagnostics show partial recoverability but not source-only deployability. Source: supplementary oracle table.\n\n## Result 7\nA learned reliability method is not authorized. Source: Step 16 gate and claim matrix.\n')
 (REPORT/'step17_methods_evidence_map.md').write_text('# Methods Evidence Map\n\n- Datasets/cohorts: frozen cohort manifests, `reports/subject_partitions_v2.csv`, Table 1.\n- Preprocessing/partitions: frozen configs and partition manifests; no Step 17 changes.\n- B0 architecture/training: frozen B0 reports and checkpoint manifests.\n- B1 intervention: `reports/b1_training_summary_v1.csv`, frozen B1 protocol.\n- Calibration/conformal: frozen B1 artifacts; Step 16 mask-specific diagnostics are secondary.\n- Shift conditions: C0–C5 definitions in Table 1.\n- Metrics: frozen evaluation implementation and primary result tables.\n- Bootstrap: subject-level duplicate-preserving 2,000-replicate engine, seed 2028.\n- B0 v1.2 repair: Step 15.2.3 repair and engine-gate artifacts.\n- Step 16 diagnostics: residual matrix, source-mask comparison, oracle diagnostic table, method gate.\n')
 (REPORT/'step17_limitations_v1.md').write_text('# Step 17 Limitations\n\n- The benchmark uses two core datasets and two reciprocal directions.\n- Exact modality and montage contracts constrain generality.\n- B0/B1 are epoch-wise models without temporal context.\n- B1 is a simple source-only modality-dropout intervention.\n- Target-oracle results are diagnostic only.\n- There is no SHHS core validation.\n- Formal conformal coverage under arbitrary dataset shift is not established.\n- The architecture is deliberately simple.\n- Stage labels and harmonization remain dataset-dependent.\n- Some residual behavior is direction-specific.\n- D2 C5 predictive robustness remains unresolved.\n')
 (REPORT/'step17_contribution_statement_v1.md').write_text('# Step 17 Contribution Statement\n\n1. A controlled compound dataset-shift and missing-modality reliability benchmark.\n2. Subject-level target-free evaluation across calibration, selective, and conformal axes.\n3. A controlled modality-dropout robustness study showing predictive/reliability decoupling.\n4. A reproducible statistical and provenance framework with exact cluster bootstrap semantics and a versioned B0 correction.\n\nNo new architecture or learned reliability method is claimed.\n')
 (REPORT/'step17_title_candidates.md').write_text('# Step 17 Title Candidates\n\n1. ShiftSleep-UQ: Calibration and Selective Reliability of Multimodal Sleep Staging Under Compound Dataset and Missing-Modality Shift\n2. ShiftSleep-UQ: A Controlled Benchmark of Predictive and Reliability Robustness in Multimodal Sleep Staging\n3. Predictive Robustness and Reliability Decoupling Under Compound Shift in Multimodal Sleep Staging\n')
 (REPORT/'step17_abstract_evidence_skeleton.md').write_text('# Step 17 Abstract Evidence Skeleton\n\n- **Problem:** Multimodal sleep-staging systems may encounter dataset and missing-modality shift simultaneously.\n- **Gap:** Predictive robustness and reliability behavior require separate controlled evaluation.\n- **Benchmark/protocol:** ShiftSleep-UQ evaluates reciprocal dataset shift, known/unseen modality conditions, source-only calibration, subject-level bootstrap inference, and a source modality-dropout control.\n- **B0 finding:** Compound cells show direction- and modality-dependent predictive and reliability degradation.\n- **B1 finding:** Macro-F1 improves in D1 C4 (+0.03673), D1 C5 (+0.18587), and D2 C4 (+0.05992), while D2 C5 is inconclusive (+0.00063).\n- **Reliability:** Calibration, selective, and conformal responses remain heterogeneous; mask-specific source calibration does not uniformly resolve them.\n- **Conclusion:** Predictive robustness improvements do not guarantee uniform reliability improvement, and the evidence does not authorize an additional learned reliability method.\n')
 # Manifest after all non-figure/table evidence files are created.
 evidence_paths=[TABLE/'table1_benchmark_design.csv',TABLE/'table2_b0_primary_shift_results.csv',TABLE/'table3_b1_vs_b0_compound_effects.csv',TABLE/'table4_residual_diagnosis.csv',REPORT/'step17_figure_provenance_v1.csv',REPORT/'step17_table_provenance_v1.csv',REPORT/'step17_claim_evidence_matrix_v1.csv',REPORT/'step17_hypothesis_evidence_map_v1.csv',REPORT/'step17_nonclaims_v1.md',REPORT/'step17_results_narrative_map.md',REPORT/'step17_methods_evidence_map.md',REPORT/'step17_limitations_v1.md',REPORT/'step17_contribution_statement_v1.md',REPORT/'step17_title_candidates.md',REPORT/'step17_abstract_evidence_skeleton.md']
 manifest={'package':'ShiftSleep-UQ Step 17 paper evidence','gate':'BENCHMARK_SYNTHESIS_FROZEN','scientific_scope':'deterministic transformations of frozen artifacts only','b0_version':'v1_2','method_gate':'RELIABILITY_METHOD_NOT_AUTHORIZED','artifacts':[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in evidence_paths]}
 (REPORT/'paper_evidence').mkdir(exist_ok=True); (REPORT/'paper_evidence'/'paper_evidence_manifest_v1.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'gate':'BENCHMARK_SYNTHESIS_FROZEN','tables':len(table_rows)+4,'figures':len(fig_rows),'evidence_files':len(evidence_paths)},sort_keys=True))
if __name__=='__main__': main()
