from __future__ import annotations
import csv,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; REPAIRED=ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'

def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def file_for(dataset,rec):
 if dataset=='sleep_edf_sc': return REPAIRED/f'sleep_edf_sc__{rec}__core_v1.npz'
 for d in ['data/processed/core_v1_1','data/processed/core_v1','data/processed/isruc_original_v2']:
  xs=list((ROOT/d).glob(f'isruc_s1__{rec}__*.npz'))
  if xs:return xs[0]
 raise FileNotFoundError(rec)
def main():
 core=rows(ROOT/'reports/core_recording_manifest_v1_1.csv')
 seen={(r['dataset'],r['recording_id']) for r in core if r['terminal_status']=='INCLUDED'}
 extra=[{'dataset':'isruc_s1','subject_id':r['subject_id'],'recording_id':r['subject_id'],'terminal_status':'INCLUDED'} for r in rows(ROOT/'reports/isruc_original_recording_manifest_v2.csv') if r['terminal_status']=='INCLUDED' and ('isruc_s1',r['subject_id']) not in seen]
 man=[r for r in core if r['terminal_status']=='INCLUDED']+extra
 win=[];prior=[];seq=[]
 for r in man:
  ds=r['dataset'];rec=r['recording_id'];p=file_for(ds,rec)
  with np.load(p,allow_pickle=False) as z:y=z['labels'].astype(int);idx=z['source_epoch_indices'].astype(int)
  assert len(y)==len(idx) and len(set(idx))==len(idx) and np.all(np.diff(idx)>0)
  counts=np.bincount(y,minlength=5);nw=np.flatnonzero(y!=0)
  if len(nw):
   lo=max(0,int(idx[nw[0]])-60);hi=int(idx[nw[-1]])+60;keep=(idx>=lo)&(idx<=hi);status='PASS'
  else:lo=hi='';keep=np.zeros(len(y),bool);status='EXCLUDE_NO_NONWAKE'
  ac=np.bincount(y[keep],minlength=5);dur=len(y)*30;adur=int(keep.sum())*30
  base={'dataset':ds,'subject_id':r['subject_id'],'recording_id':rec,'status':status,'original_valid_epochs':len(y),'retained_window_epochs':int(keep.sum()),'original_duration_seconds':dur,'retained_duration_seconds':adur,'original_wake_fraction':float(counts[0]/len(y)),'retained_wake_fraction':float(ac[0]/keep.sum()) if keep.any() else '','original_Wake':int(counts[0]),'original_N1':int(counts[1]),'original_N2':int(counts[2]),'original_N3':int(counts[3]),'original_REM':int(counts[4]),'retained_Wake':int(ac[0]),'retained_N1':int(ac[1]),'retained_N2':int(ac[2]),'retained_N3':int(ac[3]),'retained_REM':int(ac[4]),'window_first_physical_index':lo,'window_last_physical_index':hi}
  win.append(base)
  for phase,c in [('BEFORE',counts),('AFTER',ac)]:
   n=int(c.sum());prior.extend({'dataset':ds,'phase':phase,'Wake':int(c[0]),'N1':int(c[1]),'N2':int(c[2]),'N3':int(c[3]),'REM':int(c[4]),'total_epochs':n,'Wake_fraction':float(c[0]/n) if n else ''} for _ in [0])
  dif=np.diff(idx);gaps=int(np.sum(dif!=1));segments=1+gaps;short=0
  for seg in np.split(idx,np.flatnonzero(dif!=1)+1):
   if len(seg)<20:short+=len(seg)
  seq.append({'dataset':ds,'subject_id':r['subject_id'],'recording_id':rec,'valid_epochs':len(y),'covered_epochs':len(y),'excluded_short_segment_epochs':short,'excluded_short_segment_percent':100*short/len(y),'contiguous_segments':segments,'train_sequences_stride10':max(0,(len(y)-20)//10+1) if len(y)>=20 else 0,'evaluation_windows_stride1':len(y)-19 if len(y)>=20 else 0,'status':'PASS'})
 def w(p,rs):
  with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rs for k in x)));w.writeheader();w.writerows(rs)
 w(ROOT/'reports/remediation/r2_windowing_accounting_v1.csv',win);w(ROOT/'reports/remediation/r2_class_prior_before_after_v1.csv',prior);w(ROOT/'reports/remediation/r3_sequence_coverage_v1.csv',seq)
 print(json.dumps({'recordings':len(win),'sleepedf':sum(x['dataset']=='sleep_edf_sc' for x in win),'isruc':sum(x['dataset']=='isruc_s1' for x in win),'r2_pass':sum(x['status']=='PASS' for x in win),'r3_pass':sum(x['status']=='PASS' for x in seq)}))
if __name__=='__main__':main()
