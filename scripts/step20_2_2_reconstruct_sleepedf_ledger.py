from __future__ import annotations
import csv,hashlib,json,urllib.request
from pathlib import Path
import numpy as np,pyedflib
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path(r'C:\Users\rohan\AppData\Local\hermes\cache\scratch\sleepedf_hypnograms');CACHE.mkdir(parents=True,exist_ok=True)
mp={'Sleep stage W':0,'Sleep stage 1':1,'Sleep stage 2':2,'Sleep stage 3':3,'Sleep stage 4':3,'Sleep stage R':4}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def load_raw(rec,pair_map):
 stem=pair_map[rec];p=CACHE/stem
 if not p.exists(): urllib.request.urlretrieve('https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/'+stem,p)
 f=pyedflib.EdfReader(str(p));o,d,a=f.readAnnotations();f.close();seq=[];idx=[];bad=[]
 for onset,dur,lab in zip(o,d,a):
  if lab not in mp: continue
  if abs(onset/30-round(onset/30))>1e-7 or abs(dur/30-round(dur/30))>1e-7: bad.append((float(onset),float(dur),lab));continue
  for j in range(round(dur/30)): seq.append(mp[lab]);idx.append(round(onset/30)+j)
 return np.asarray(seq,np.int8),np.asarray(idx,np.int64),p,bad
def main():
 rows=[];repaired=ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2';repaired.mkdir(parents=True,exist_ok=False)
 with (ROOT/'reports/sleep_edf_pairing_audit.csv').open() as f: pair_map={r['recording_id']:r['matched_hypnogram_filename'] for r in csv.DictReader(f)}
 with (ROOT/'reports/core_recording_manifest_v1_1.csv').open() as f: manifest=[r for r in csv.DictReader(f) if r['dataset']=='sleep_edf_sc' and r['terminal_status']=='INCLUDED']
 for r in manifest:
  rec=r['recording_id'];src=ROOT/'data/processed/core_v1_1'/f'sleep_edf_sc__{rec}__core_v1.npz';raw,idx,ann,bad=load_raw(rec,pair_map)
  with np.load(src,allow_pickle=False) as z: arrays={k:z[k] for k in z.files}
  labels=arrays['labels'];prefix_exact=len(raw)>=len(labels) and np.array_equal(raw[:len(labels)],labels); valid=prefix_exact and len(idx)>=len(labels) and np.all(np.diff(idx[:len(labels)])>0) and np.all(idx[:len(labels)]>=0)
  if not valid: raise RuntimeError(f'{rec} reconstruction mismatch n={len(labels)}/{len(raw)} exact={prefix_exact} bad={bad[:2]}')
  idx=idx[:len(labels)]; arrays['source_epoch_indices']=idx;out=repaired/f'{src.stem}.npz';np.savez_compressed(out,**arrays)
  with np.load(src,allow_pickle=False) as original: signal_same=all(np.array_equal(arrays[k],original[k]) for k in ('eeg','eog','labels','epoch_onsets_seconds'))
  rows.append({'dataset':'sleep_edf_sc','recording_id':rec,'subject_id':r['subject_id'],'source_file_sha256':sha(src),'annotation_file':ann.name,'annotation_sha256':sha(ann),'retained_epochs':len(labels),'reconstructed_first_index':int(idx[0]),'reconstructed_last_index':int(idx[-1]),'strictly_increasing_unique':True,'labels_exact_match':prefix_exact,'signal_label_epoch_invariance':signal_same,'non_boundary_annotations':len(bad),'status':'PASS'})
 with (ROOT/'reports/remediation/sleepedf_epoch_index_reconstruction_audit_v1.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 (ROOT/'reports/remediation/sleepedf_epoch_ledger_v2_manifest.json').write_text(json.dumps({'gate':'SLEEPEDF_EPOCH_LEDGER_RECONSTRUCTED','recordings':len(rows),'source':'PhysioNet sleep-edfx official hypnogram EDF+ annotations','derivative_dir':str(repaired.relative_to(ROOT))},indent=2)+'\n')
 print(json.dumps({'recordings':len(rows),'pass':sum(r['status']=='PASS' for r in rows),'total_epochs':sum(int(r['retained_epochs']) for r in rows)}))
if __name__=='__main__':main()
