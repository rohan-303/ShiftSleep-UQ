"""Step 20.2.1 bounded R1 input audit, Figure 2 correction, and R2/R3 preflight.
No training, inference, calibration fitting, or scientific R1 computation is performed.
"""
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import stft, resample_poly

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/remediation'; OUT.mkdir(parents=True,exist_ok=True)
V2_HASH='c5cad2d75cdc5c6100caebaac2f1ea16d292b8d3a69d5d2bda283587dcfe004b'
SEEDS=[17,42,2026]; D=[('D1_SLEEPEDF_TO_ISRUC','b0','isruc_s1'),('D2_ISRUC_TO_SLEEPEDF','b0','sleep_edf_sc')]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return str(p.relative_to(ROOT)).replace('\\','/')

def r1_hash_audit():
 rows=[]
 for direction in ['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']:
  for model in ['b0','b1_moddrop']:
   for seed in SEEDS:
    for c in [f'C{i}' for i in range(6)]:
     p=ROOT/f'artifacts/predictions/{model}/{direction}/seed_{seed}/{c}.npz'
     rows.append({'direction':direction,'model_family':model,'seed':seed,'split_condition':c,'path':rel(p),'historical_expected_hash':'NOT_AVAILABLE_IN_FROZEN_MANIFEST','observed_hash':sha(p) if p.exists() else 'MISSING','status':'PASS_OBSERVED_FILE' if p.exists() else 'FAIL_MISSING'})
 with (OUT/'r1_input_hash_audit_v1.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 return rows

def figure2():
 src=pd.read_csv(ROOT/'reports/paper_figures/source_data/fig2_b0_shift_landscape.csv')
 b0=pd.read_csv(ROOT/'reports/b0_primary_metrics_per_seed_v1.csv')
 rows=[]
 metric_map={'macro-F1':('macro-F1','mean across frozen B0 seeds'),'calibrated NLL':('NLL','mean across frozen B0 seeds'),'entropy AURC':('AURC','mean across frozen B0 seeds'),'ABSOLUTE alpha-.10 coverage gap':('APS_coverage_gap_alpha_0.10','absolute value of mean frozen signed gap')}
 for _,r in src.iterrows():
  subset=b0[(b0.experiment_id==r.direction)&(b0.condition==r.condition)&(b0.metric.isin([v[0] for v in metric_map.values()]))]
  for label,(col,desc) in metric_map.items():
   q=subset[subset.metric==col].value.astype(float)
   if col=='APS_coverage_gap_alpha_0.10': value=abs(float(q.mean()))
   else: value=float(q.mean())
   rows.append({'direction':r.direction,'condition':r.condition,'metric':label,'numeric_value':value,'source_artifact':rel(ROOT/'reports/b0_primary_metrics_per_seed_v1.csv'),'source_column':'value','source_row_key':f'{r.direction}|{r.condition}|{col}|seed_mean|{desc}'})
 out=pd.DataFrame(rows); assert len(out)==48 and (out.numeric_value>=0).all()
 out.to_csv(OUT/'fig2_b0_shift_landscape_corrected_source_v1.csv',index=False)
 import matplotlib.pyplot as plt
 fig,axs=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
 for ax,(metric,_) in zip(axs.flat,metric_map.items()):
  for direction in src.direction.unique():
   q=out[(out.direction==direction)&(out.metric==metric)]
   ax.plot(q.condition,q.numeric_value,marker='o',label=direction.split('_')[0])
  ax.set_title(metric);ax.set_xlabel('condition');ax.set_ylabel('value');ax.grid(alpha=.25);ax.legend()
 fig.savefig(OUT/'fig2_b0_shift_landscape_corrected_v1.pdf'); plt.close(fig)
 return len(out)

def resolve_files():
 files=[]
 manifest=pd.read_csv(ROOT/'reports/core_recording_manifest_v1_1.csv')
 sleep_subject={str(r.recording_id):str(r.subject_id) for _,r in manifest[manifest.dataset=='sleep_edf_sc'].iterrows()}
 for p in sorted((ROOT/'data/processed/core_v1_1').glob('sleep_edf_sc__*.npz')):
  z=p.name.split('__'); files.append(('sleep_edf_sc',sleep_subject.get(z[1],'UNKNOWN'),z[1],p))
 for p in sorted((ROOT/'data/processed/isruc_original_v2').glob('isruc_s1__*__original_v2.npz')):
  z=p.name.split('__'); files.append(('isruc_s1',z[1],z[1],p))
 return files

def partitions():
 return pd.read_csv(ROOT/'reports/subject_partitions_v2.csv')

def preflight():
 part=partitions(); role={(r.dataset,r.subject_id):r.source_role for _,r in part.iterrows()}
 win=[]; classrows=[]; seqrows=[]
 for ds,sid,rid,p in resolve_files():
  z=np.load(p,allow_pickle=False); y=z['labels'].astype(int); n=len(y); valid=(y>=0)&(y<=4); orig=z['source_epoch_indices'].astype(int)
  index_ok=bool(len(orig)==0 or (np.all(np.diff(orig)>0) and np.all(np.diff(orig)==1)))
  nw=valid&(y!=0)
  if not index_ok:
   row={'dataset':ds,'subject':sid,'recording':rid,'original_total_epoch_positions':int(orig.max()+1) if len(orig) else n,'historical_valid_epochs':int(valid.sum()),'first_valid_nonwake_index':'NOT_COMPUTED','last_valid_nonwake_index':'NOT_COMPUTED','requested_window_start':'NOT_COMPUTED','requested_window_end':'NOT_COMPUTED','retained_valid_epochs':'NOT_COMPUTED','retained_Wake':'NOT_COMPUTED','retained_N1':'NOT_COMPUTED','retained_N2':'NOT_COMPUTED','retained_N3':'NOT_COMPUTED','retained_REM':'NOT_COMPUTED','original_Wake_fraction':float((y[valid]==0).mean()) if valid.any() else np.nan,'retained_Wake_fraction':'NOT_COMPUTED','source_role':role.get((ds,sid),'NOT_IN_PARTITION'),'path':rel(p),'index_contract_status':'BLOCKED_INVALID_SOURCE_EPOCH_INDICES'};win.append(row)
   before=[int((y[valid]==k).sum()) for k in range(5)]
   for k,name in enumerate(['Wake','N1','N2','N3','REM']): classrows.append({'dataset':ds,'stage':'BEFORE','class':name,'count':before[k]})
   seqrows.append({'dataset':ds,'subject':sid,'recording':rid,'population':role.get((ds,sid),'NOT_IN_PARTITION'),'valid_epochs':len(orig),'epochs_in_full_length20_window':'NOT_COMPUTED','excluded_short_segment_epochs':'NOT_COMPUTED','exclusion_percent':'NOT_COMPUTED','train_stride10_sequences':'NOT_COMPUTED','evaluation_stride1_windows':'NOT_COMPUTED','index_contract_status':'BLOCKED_INVALID_SOURCE_EPOCH_INDICES','path':rel(p)})
   continue
  if nw.any():
   first=int(orig[np.flatnonzero(nw)[0]]); last=int(orig[np.flatnonzero(nw)[-1]]); ws=max(0,first-60); we=min(int(orig[-1]),last+60); kept=np.flatnonzero(valid&(orig>=ws)&(orig<=we))
  else: first=last=ws=we=-1; kept=np.array([],int)
  counts=[int((y[kept]==k).sum()) for k in range(5)]; before=[int((y[valid]==k).sum()) for k in range(5)]
  row={'dataset':ds,'subject':sid,'recording':rid,'original_total_epoch_positions':int(orig[-1]+1) if len(orig) else n,'historical_valid_epochs':int(valid.sum()),'first_valid_nonwake_index':first,'last_valid_nonwake_index':last,'requested_window_start':ws,'requested_window_end':we,'retained_valid_epochs':len(kept),'retained_Wake':counts[0],'retained_N1':counts[1],'retained_N2':counts[2],'retained_N3':counts[3],'retained_REM':counts[4],'original_Wake_fraction':before[0]/sum(before) if sum(before) else np.nan,'retained_Wake_fraction':counts[0]/sum(counts) if sum(counts) else np.nan,'source_role':role.get((ds,sid),'NOT_IN_PARTITION'),'path':rel(p),'index_contract_status':'PASS'};win.append(row)
  for stage,arr in [('BEFORE',before),('AFTER',counts)]:
   for k,name in enumerate(['Wake','N1','N2','N3','REM']): classrows.append({'dataset':ds,'stage':stage,'class':name,'count':arr[k]})
  # contiguous valid original indices, no padding; compute sequence coverage
  segments=[]; start=0
  if len(orig):
   for j in range(1,len(orig)+1):
    if j==len(orig) or orig[j]!=orig[j-1]+1: segments.append((start,j));start=j
  eligible=sum(max(0,b-a-19) for a,b in segments); excluded=sum((b-a) for a,b in segments if b-a<20)
  train_seq=sum(max(0,(b-a-20)//10+1) for a,b in segments if b-a>=20); eval_win=sum(max(0,b-a-20+1) for a,b in segments if b-a>=20)
  seqrows.append({'dataset':ds,'subject':sid,'recording':rid,'population':role.get((ds,sid),'NOT_IN_PARTITION'),'valid_epochs':len(orig),'epochs_in_full_length20_window':eligible,'excluded_short_segment_epochs':excluded,'exclusion_percent':100*excluded/len(orig) if len(orig) else 0,'train_stride10_sequences':train_seq,'evaluation_stride1_windows':eval_win,'index_contract_status':'PASS','path':rel(p)})
 pd.DataFrame(win).to_csv(OUT/'r2_windowing_preflight_v1.csv',index=False)
 cdf=pd.DataFrame(classrows); totals=cdf.groupby(['dataset','stage','class'],as_index=False).count
 # recompute proportions and JS by dataset stage
 out=[]
 for (ds,stage),g in cdf.groupby(['dataset','stage']):
  total=g['count'].sum();
  for _,x in g.iterrows(): out.append({'dataset':ds,'stage':stage,'class':x['class'],'count':int(x['count']),'proportion':x['count']/total if total else np.nan})
 props=pd.DataFrame(out); props.to_csv(OUT/'r2_class_prior_preflight_v1.csv',index=False)
 # JS where both datasets have valid AFTER windows; otherwise preserve explicit blocker
 piv=props.pivot_table(index=['dataset','stage'],columns='class',values='proportion',fill_value=0); js=[]
 for stage in ['BEFORE','AFTER']:
  if ('sleep_edf_sc',stage) not in piv.index or ('isruc_s1',stage) not in piv.index:
   js.append({'stage':stage,'sleep_edf_sc_js_against_isruc_s1':'NOT_COMPUTED_INVALID_INDEX_CONTRACT'}); continue
  a=piv.loc[('sleep_edf_sc',stage)].to_numpy(); b=piv.loc[('isruc_s1',stage)].to_numpy();m=(a+b)/2
  js.append({'stage':stage,'sleep_edf_sc_js_against_isruc_s1':float(0.5*np.sum(np.where(a>0,a*np.log(a/m),0))+0.5*np.sum(np.where(b>0,b*np.log(b/m),0)))})
 pd.DataFrame(js).to_csv(OUT/'r2_class_prior_js_preflight_v1.csv',index=False)
 # partition integrity
 pr=[]
 for (ds,sid),g in part.groupby(['dataset','subject_id']): pr.append({'dataset':ds,'subject':sid,'roles_seen':'|'.join(sorted(g.source_role.unique())),'status':'PASS' if len(g)==1 and g.source_role.iloc[0] in ['TRAIN','DEV','CALIBRATION','TEST'] else 'FAIL'})
 pd.DataFrame(pr).to_csv(OUT/'r2_partition_preflight_v1.csv',index=False)
 # sequence aggregate
 sdf=pd.DataFrame(seqrows); sdf.to_csv(OUT/'r3_sequence_coverage_preflight_v1.csv',index=False)
 return pd.DataFrame(win),props,sdf

def r3_smoke():
 # first lexicographic source-train subject/recording in each dataset, real tensors only
 part=partitions(); result=[]
 for ds in ['isruc_s1','sleep_edf_sc']:
  sid=sorted(part[(part.dataset==ds)&(part.source_role=='TRAIN')].subject_id)[0]
  fs=[x for x in resolve_files() if x[0]==ds and x[1]==sid]
  ds0,sid,rid,p=sorted(fs,key=lambda x:x[2])[0]; z=np.load(p,allow_pickle=False)
  eeg=z['eeg'];eog=z['eog'];
  # real-data signal contract + deterministic EOG 50->100; use first 20 contiguous epochs if available
  eog100=resample_poly(eog[:20],2,1,axis=1) if len(eog)>=20 else resample_poly(eog,2,1,axis=1)
  epoch=eeg[:20]; frames=[]
  for c in [epoch,eog100[:len(epoch)]]:
   _,_,Z=stft(c,fs=100,nperseg=200,noverlap=100,nfft=256,window='hamming',boundary=None,padded=False,axis=-1)
   frames.append(np.log(np.abs(Z)**2+1e-8))
  arr=np.stack(frames,axis=1)
  result.append({'dataset':ds,'subject':sid,'recording':rid,'path':rel(p),'eeg_input_shape':str(eeg[:20].shape),'eog_input_shape':str(eog[:20].shape),'eog_resampled_shape':str(eog100.shape),'spectrogram_shape':str(arr.shape),'finite':bool(np.isfinite(arr).all()),'sequence_available':bool(len(arr)>=20)})
 pd.DataFrame(result).to_csv(OUT/'r3_real_data_smoke_v1.csv',index=False); return result

if __name__=='__main__':
 rows=r1_hash_audit(); n=figure2(); w,p,s=preflight(); sm=r3_smoke(); print(json.dumps({'r1_prediction_bundles':len(rows),'figure2_rows':n,'r2_window_rows':len(w),'r3_sequence_rows':len(s),'r3_smoke':sm},default=str))
