from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def find(ds,rec):
 if ds=='sleep_edf_sc':return ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'/f'sleep_edf_sc__{rec}__core_v1.npz'
 for d in ['data/processed/core_v1_1','data/processed/core_v1','data/processed/isruc_original_v2']:
  xs=list((ROOT/d).glob(f'isruc_s1__{rec}__*.npz'))
  if xs:return xs[0]
 raise FileNotFoundError(rec)
def main():
 manifest=rows(ROOT/'reports/core_recording_manifest_v1_1.csv');seen={(r['dataset'],r['recording_id']) for r in manifest if r['terminal_status']=='INCLUDED'}
 manifest += [{'dataset':'isruc_s1','recording_id':r['subject_id'],'subject_id':r['subject_id'],'terminal_status':'INCLUDED'} for r in rows(ROOT/'reports/isruc_original_recording_manifest_v2.csv') if r['terminal_status']=='INCLUDED' and ('isruc_s1',r['subject_id']) not in seen]
 out=[];win=[]
 for r in manifest:
  if r['terminal_status']!='INCLUDED':continue
  ds,rec,sub=r['dataset'],r['recording_id'],r['subject_id'];p=find(ds,rec)
  with np.load(p,allow_pickle=False) as z:
   y=z['labels'].astype(int);idx=z['source_epoch_indices'].astype(int);eeg=z['eeg'];eog=z['eog']
  assert len(y)==len(idx) and np.all(np.diff(idx)>0) and np.all(idx>=0)
  nw=np.flatnonzero(y!=0);lo=max(0,int(idx[nw[0]])-60);hi=min(int(idx[-1]),int(idx[nw[-1]])+60);keep=(idx>=lo)&(idx<=hi)
  out.append({'dataset':ds,'subject_id':sub,'recording_id':rec,'source_role_contract':'OVERLAY_ONLY','path':str(p.relative_to(ROOT)),'epoch_count':len(y),'index_sha256':hashlib.sha256(idx.tobytes()).hexdigest(),'signal_reference_sha256':hashlib.sha256(eeg.tobytes()+eog.tobytes()+y.tobytes()).hexdigest(),'strictly_increasing':True,'labels_finite':bool(np.isfinite(y).all()),'status':'PASS'})
  c=np.bincount(y,minlength=5);a=np.bincount(y[keep],minlength=5)
  win.append({'dataset':ds,'subject_id':sub,'recording_id':rec,'original_valid_count':len(y),'retained_count':int(keep.sum()),'original_Wake':int(c[0]),'original_N1':int(c[1]),'original_N2':int(c[2]),'original_N3':int(c[3]),'original_REM':int(c[4]),'retained_Wake':int(a[0]),'retained_N1':int(a[1]),'retained_N2':int(a[2]),'retained_N3':int(a[3]),'retained_REM':int(a[4]),'source_role':'OVERLAY_DERIVATIVE','index_sha256':hashlib.sha256(idx.tobytes()).hexdigest(),'status':'PASS'})
 def write(path,rs):
  with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
 write(ROOT/'reports/remediation/remediation_data_overlay_audit_v1.csv',out);write(ROOT/'reports/remediation/r2_windowed_dataset_manifest_v1.csv',win)
 print(json.dumps({'overlay_rows':len(out),'sleepedf':sum(r['dataset']=='sleep_edf_sc' for r in out),'isruc':sum(r['dataset']=='isruc_s1' for r in out),'window_rows':len(win)}))
if __name__=='__main__':main()
