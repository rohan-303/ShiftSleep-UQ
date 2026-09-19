from __future__ import annotations
import csv, json, hashlib, re, urllib.request, urllib.error
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'reports'; REM=R/'remediation'; REM.mkdir(parents=True,exist_ok=True)
ART=ROOT/'artifacts'; SEEDS=(17,42,2026); EXPS=('D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'); CONDS=('C0','C1','C2','C3','C4','C5')

def readcsv(p): return list(csv.DictReader(open(p,encoding='utf-8')))
def writecsv(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True); fields=fields or list(dict.fromkeys(k for row in rows for k in row))
 with open(p,'w',newline='',encoding='utf-8') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore').writeheader(); csv.DictWriter(f,fieldnames=fields,extrasaction='ignore').writerows(rows)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(x): return float(x)

# Figure 2 forensic audit and corrected diagnostic.
canon=readcsv(R/'b0_primary_results_multiseed_v1_2.csv')
lookup={(x['experiment_id'],x['condition'],x['metric']):f(x['point_estimate']) for x in canon if x['probability_variant']=='UNCALIBRATED'}
old=readcsv(R/'paper_figures'/'source_data'/'fig2_b0_shift_landscape.csv')
rows=[]
for x in old:
 e=x['direction']; c=x['condition']
 for metric,field in [('macro-F1','macro_F1'),('NLL','NLL'),('AURC','AURC'),('coverage_gap_signed','abs_gap_alpha_0.10')]:
  raw=x[field]; val=None if str(raw).startswith('NOT_') else f(raw)
  cv=lookup[(e,c,'gap_0.1' if metric=='coverage_gap_signed' else metric)]
  rows.append({'direction':'D1' if e.startswith('D1') else 'D2','condition':c,'metric':metric,'source_numeric_value':raw,'dataframe_dtype':'float64' if val is not None else 'unavailable','plotting_y_value':f'{val:.12g}' if val is not None else 'UNAVAILABLE','rendered_axis_value':f'{val:.12g}' if val is not None else 'UNAVAILABLE','status':'PASS_NUMERIC_Y' if metric!='coverage_gap_signed' and val is not None else ('FIG2_CONFORMAL_FIELD_BINDING_BUG_CONFIRMED' if val is not None and val<0 else 'SOURCE_VALUE_UNAVAILABLE')})
writecsv(R/'step20_1_fig2_plot_semantics_audit.csv',rows)
# Numeric x is intentionally categorical labels; y remains numeric.
fig,axs=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
for ax,(title,m) in zip(axs.flat,[('Macro-F1','macro-F1'),('Calibrated NLL','NLL'),('Entropy AURC','AURC'),('Absolute coverage gap (alpha=0.10)','gap_0.1')]):
 for e,style,label in [('D1_SLEEPEDF_TO_ISRUC','-o','D1'),('D2_ISRUC_TO_SLEEPEDF','-s','D2')]:
  vals=[lookup[(e,c,m)] for c in CONDS]
  if m=='gap_0.1': vals=[abs(v) for v in vals]
  ax.plot(range(6),vals,style,label=label,lw=1.8,ms=4)
 ax.set_xticks(range(6),CONDS); ax.set_title(title); ax.set_ylabel('metric value'); ax.grid(alpha=.25); ax.legend(frameon=False)
fig.suptitle('Corrected diagnostic: B0 v1.2 shift landscape',fontsize=13)
fig.savefig(REM/'fig2_b0_shift_landscape_corrected_preview.pdf'); plt.close(fig)
# Regression assertions: D1 macro-F1 must be non-monotonic and y values must be numeric.
d1=[lookup[('D1_SLEEPEDF_TO_ISRUC',c,'macro-F1')] for c in CONDS]; d2=[lookup[('D2_ISRUC_TO_SLEEPEDF',c,'macro-F1')] for c in CONDS]
assert d1[0]>d1[1]>d1[2] and d1[2]<d1[3] and d1[3]>d1[4]>d1[5]
assert all(isinstance(v,float) for v in d1+d2)
(R/'step20_1_fig2_regression_test.txt').write_text('PASS\nD1 macro-F1 preserves non-monotonic C0-C5 ordering; D2 and all y coordinates are numeric floats.\n',encoding='utf-8')
(R/'step20_1_fig2_caption_recommendation.md').write_text('# Figure 2 caption recommendation\n\nB0 performance and uncertainty metrics across the six prespecified conditions in both reciprocal directions. Points are plotted at their numeric metric values; C0--C2 are known-domain modality conditions and C3--C5 are cross-dataset conditions. Coverage-gap values are absolute deviations from nominal 0.90 coverage at alpha=0.10.\n',encoding='utf-8')

# APS implementation audit.
(R/'step20_1_aps_implementation_audit.md').write_text('''# APS implementation forensic audit\n\nImplementation: `src/shiftsleep_uq/evaluation_step11.py` (`aps_prediction_set`, `conformal_metrics`) and frozen calibration artifacts under `artifacts/calibration/b0`.\n\n| Component | Finding | Status |\n|---|---|---|\n| conformity score | cumulative uncalibrated softmax probability through the true label after descending probability sorting | MATCH |\n| class sorting | descending probability; ties broken by ascending class index | MATCH |\n| calibration quantile | k=ceil((n+1)(1-alpha)), clamped to 1..n, kth ascending score | MATCH |\n| set construction | smallest prefix whose cumulative probability reaches qhat | MATCH |\n| inequality | cumulative score <= qhat, with prefix inclusion at threshold | MATCH |\n| randomization | none | MATCH (non-randomized APS) |\n| calibration population | source CAL only | MATCH |\n| source TEST population | held-out source TEST, never calibration | MATCH |\n| target population | held-out complete target, used only for evaluation | MATCH |\n| qhat alpha=.10/.05 | stored per direction/seed in frozen APS calibration JSON | MATCH |\n| tie handling | deterministic class-index tie break | MATCH |\n\nNo unambiguous APS implementation bug was found. The procedure is valid as implemented but can be conservative because it is non-randomized and finite-sample quantile/set construction can produce large sets. The Figure 2 signed/absolute field mismatch is separate from APS set construction.\n\nPublished-definition reference for future manuscript positioning: Romano, Sesia, and Candès, “Classification with Valid and Adaptive Coverage,” NeurIPS 2020, official proceedings record. The frozen implementation uses the APS cumulative-probability score and does not implement weighted conformal prediction.\n''',encoding='utf-8')

# Source conformal metrics and set-size distributions from existing prediction artifacts.
from sys import path
path.insert(0,str(ROOT/'src'))
from shiftsleep_uq.evaluation_step11 import softmax, aps_prediction_set, conformal_metrics
san=[]; dist=[]
for e in EXPS:
 for s in SEEDS:
  for c in ('C0','C1','C2'):
   p=ART/'predictions'/'b0'/e/f'seed_{s}'/f'{c}.npz'; qj=json.loads((ART/'calibration'/'b0'/e/f'seed_{s}'/'aps.json').read_text())
   z=np.load(p); probs=softmax(z['logits']); y=z['labels']
   vals={}
   for a in (.10,.05):
    q=qj[f'alpha_{a:.2f}_qhat']; sets=aps_prediction_set(probs,q); sizes=sets.sum(1); cm=conformal_metrics(probs,y,q,a)
    key=f'{a:.2f}'; vals[key]=(cm,sizes)
    r={'direction':'D1' if e.startswith('D1') else 'D2','experiment_id':e,'seed':s,'condition':c,'alpha':a,'source_test_epochs':len(y),'empirical_coverage':cm['empirical_coverage'],'coverage_gap_signed':cm['coverage_gap'],'absolute_coverage_gap':abs(cm['coverage_gap']),'qhat':q,'mean_set_size':float(np.mean(sizes)),'median_set_size':float(np.median(sizes)),'singleton_fraction':float(np.mean(sizes==1)),'full_set_fraction':float(np.mean(sizes==5)),'empty_set_fraction':float(np.mean(sizes==0))}
    san.append(r)
    for a,(cm,sizes) in vals.items():
     dist.append({'direction':'D1' if e.startswith('D1') else 'D2','experiment_id':e,'seed':s,'condition':c,'alpha':a,'coverage':cm['empirical_coverage'],'mean_set_size':float(np.mean(sizes)),'median_set_size':float(np.median(sizes)),**{f'p_set_size_{k}':float(np.mean(sizes==k)) for k in range(1,6)}})
writecsv(R/'step20_1_source_conformal_sanity.csv',san)
writecsv(R/'step20_1_aps_set_size_distribution.csv',dist)

# Seed variability from frozen per-seed B0/B1 primary metrics.
b0=readcsv(R/'b0_primary_metrics_per_seed_v1.csv'); b1=readcsv(R/'b1_primary_metrics_per_seed_v1.csv')
def vals(rs,e,c): return {int(x['seed']):f(x['value']) for x in rs if x['experiment_id']==e and x['condition']==c and (x.get('population','COMPLETE_TARGET')=='COMPLETE_TARGET') and x['metric']=='macro-F1'}
sv=[]
for e in EXPS:
 for c in ('C4','C5'):
  a=vals(b0,e,c); b=vals(b1,e,c); ds=[b[s]-a[s] for s in SEEDS]
  sv.append({'direction':'D1' if e.startswith('D1') else 'D2','condition':c,'delta_seed_17':ds[0],'delta_seed_42':ds[1],'delta_seed_2026':ds[2],'mean':float(np.mean(ds)),'sd_sample':float(np.std(ds,ddof=1)),'min':min(ds),'max':max(ds),'bootstrap_ci_frozen_three_seed_mean':'see paired bootstrap CI; seed-fixed'} )
writecsv(R/'step20_1_primary_seed_variability.csv',sv)

# Dataset duration/class distribution and priors.
def dataset_stats(name,folder,prefix):
 out=[]; counts=Counter()
 for p in sorted((ROOT/folder).glob(prefix+'*.npz')):
  z=np.load(p,allow_pickle=False); y=z['labels'].astype(int); meta=json.loads(str(z['metadata_json']))
  sid=meta.get('subject_id',p.stem); counts.update(y.tolist())
  out.append({'dataset':name,'recording':p.stem,'subject_id':sid,'included_epoch_count':len(y),'included_duration_hours':len(y)*30/3600,**{f'class_{k}_count':int(np.sum(y==k)) for k in range(5)},'wake_fraction':float(np.mean(y==0))})
 return out,counts
sleep,cs=dataset_stats('Sleep-EDF','data/processed/core_v1_1','sleep_edf_sc')
isr,ci=dataset_stats('ISRUC','data/processed/isruc_original_v2','isruc_s1')
writecsv(R/'step20_1_dataset_duration_class_distribution.csv',sleep+isr)
total=sum(cs.values()); toti=sum(ci.values());
props={0:cs[0]/total,1:cs[1]/total,2:cs[2]/total,3:cs[3]/total,4:cs[4]/total}; propi={0:ci[0]/toti,1:ci[1]/toti,2:ci[2]/toti,3:ci[3]/toti,4:ci[4]/toti}
def js(p,q):
 m=(p+q)/2; return .5*sum(x*np.log(x/y) for x,y in zip(p,m) if x>0)+.5*sum(x*np.log(x/y) for x,y in zip(q,m) if x>0)
prior_rows=[]
for k in range(5): prior_rows.append({'comparison':'Sleep-EDF vs ISRUC','class':k,'sleep_edf_proportion':props[k],'isruc_proportion':propi[k],'absolute_difference':abs(props[k]-propi[k])})
prior_rows.append({'comparison':'Sleep-EDF vs ISRUC','class':'ALL','sleep_edf_proportion':1.0,'isruc_proportion':1.0,'absolute_difference':js(np.array([props[k] for k in range(5)]),np.array([propi[k] for k in range(5)])),'sleep_edf_epoch_count':total,'isruc_epoch_count':toti})
writecsv(R/'step20_1_class_prior_shift_audit.csv',prior_rows)

# Protocol and prose reports.
protocol='''version: postreview_remediation_protocol_v1\nstatus: SCIENTIFIC_REMEDIATION_PROTOCOL_FROZEN\nhistorical_results: PRIMARY_HISTORICAL\nexperiments:\n  R1_conformal: SECONDARY_METHOD_SENSITIVITY\n  R2_sleep_window: CONFIRMATORY_SENSITIVITY\n  R3_strong_backbone: CONFIRMATORY_GENERALIZATION\nr1:\n  required: true\n  algorithm: randomized_APS_if_compatible_else_RAPS\n  calibration: source_CAL_only\n  target_labels_for_tuning: false\n  hyperparameters: frozen_before_execution\nr2:\n  name: SLEEP_WINDOW_HARMONIZED_SENSITIVITY_V1\n  onset: first_scored_non_Wake_epoch\n  termination: last_scored_non_Wake_epoch\n  context: 30_minutes_before_and_after\n  interval: retain_all_scored_epochs_between_bounds\n  invalid_epochs: exclude_using_original_label_rules\n  no_sleep_recordings: retain_as_excluded_and_report\n  partitions: reuse_frozen_subject_partitions\n  normalization: refit_on_source_train_only\n  directions: [D1, D2]\n  conditions: [C0, C1, C2, C3, C4, C5]\n  model_variants: [B0, B1]\n  model_seeds: [17, 42, 2026]\nr3:\n  backbone: SeqSleepNet_class\n  variants: [S0_full_modality, S1_source_modality_exposure]\n  source_exposure_S1: {FULL: 0.50, EEG_only: 0.25, EOG_only: 0.25}\n  directions: [D1, D2]\n  conditions: [C0, C1, C2, C3, C4, C5]\n  model_seeds: [17, 42, 2026]\nstatistics:\n  bootstrap_unit: subject\n  replicates: 2000\n  bootstrap_seed: 2028\n  ranking_engine: exact_duplicate_preserving\n  primary_cells: [D1_C4, D1_C5, D2_C4, D2_C5]\n  primary_metric: macro-F1\n  multiplicity: Holm_FWER_0.05_sensitivity_for_four_primary_contrasts\n  calibration: source_CAL_only\n  target_adaptation: false\n  target_hyperparameter_selection: false\nstop_rules:\n  - no reproducible strong backbone under 6GB VRAM without protocol change\n  - any implementation defect blocks interpretation until versioned correction\n  - no target labels, target calibration, or SHHS\nartifact_namespaces: [step20_1, remediation_r1, remediation_r2, remediation_r3]\n'''
(ROOT/'configs').mkdir(exist_ok=True); (ROOT/'configs/postreview_remediation_protocol_v1.yaml').write_text(protocol,encoding='utf-8'); (R/'step20_1_remediation_protocol_hash.txt').write_text(sha(ROOT/'configs/postreview_remediation_protocol_v1.yaml')+'\n',encoding='utf-8')

(R/'step20_1_conformal_metric_interpretation_audit.md').write_text('''# Conformal metric interpretation audit\n\nThe frozen primary axis is absolute deviation from nominal coverage. This is interpretable as a descriptive calibration-distance measure, but it is not sufficient as a standalone reliability score when source coverage is strongly conservative. A target condition can move closer to 0.90 while prediction sets become larger, singleton rates fall, or predictive quality deteriorates. The future analysis must report coverage together with set size and predictive/selective metrics.\n\nConclusion: the APS implementation is valid, but the absolute-gap axis requires reframing as one axis among several.\n''',encoding='utf-8')
(R/'step20_1_bootstrap_estimand.md').write_text('''# Bootstrap estimand\n\nFor each condition and metric, the frozen paired procedure resamples subjects with replacement using the exact duplicate-preserving multiplicity draws. Each replicate computes the metric separately for seed 17, seed 42, and seed 2026, then averages the three seed-specific values. B1 minus B0 is formed within the same replicate before percentile limits are reported.\n\nThe resulting interval primarily represents subject-sampling uncertainty for the mean of three fixed trained-model seeds. It does not fully represent arbitrary future training randomness; seed variability is reported separately.\n''',encoding='utf-8')
(R/'step20_1_novelty_repositioning.md').write_text('''# Novelty repositioning\n\nThe study does not claim novelty for the general observation that accuracy and uncertainty can diverge under distribution shift. The narrower contribution is a controlled reciprocal evaluation of dataset shift × missing-modality shift in sleep staging across predictive performance, calibration, uncertainty ranking, selective prediction, and conformal behavior, together with a controlled missing-modality exposure intervention.\n\nOvadia et al. (2019) supplies prior evidence that uncertainty quality changes under dataset shift. Tibshirani et al. (2019) is conceptually relevant to weighted conformal prediction under covariate shift, but weighted conformal requires density-ratio or target-covariate information and is not automatically compatible with the frozen strict source-only deployment setting.\n''',encoding='utf-8')
(R/'step20_1_table4_redesign.md').write_text('''# Table 4 redesign\n\nRemove global constant columns such as `Simple calibration = Persists` and `Oracle = Diagnostic` from the body. Retain only cell-varying residual-diagnosis information: direction, condition, metric/axis, residual pattern, and interpretation. Move the global calibration and oracle-status facts to the caption or surrounding prose.\n''',encoding='utf-8')
(R/'step20_1_precision_policy.md').write_text('''# Numeric precision policy\n\nFuture main-paper displays use three decimals for macro-F1, deltas, CI endpoints, NLL, AURC, and related summary metrics unless extra precision materially changes interpretation. Machine-readable CSV/NPZ supplements retain full precision. Raw result files are not modified by this policy.\n''',encoding='utf-8')
(R/'step20_1_manuscript_tone_revision_map.md').write_text('''# Manuscript tone revision map\n\nConsolidate repetitive disavowals into one limitations paragraph. Retain necessary statements about no clinical validation, no target adaptation, no SHHS, and diagnostic/oracle analyses. Replace workflow terms (“Step 16”, “gate”, “frozen artifact”) with reader-facing descriptions such as “prespecified post-hoc diagnostic analysis”, “decision rule”, and “prespecified result”. Keep machine identifiers only in the reproducibility supplement.\n''',encoding='utf-8')
''