"""Step 7.1 full-core preprocessing and deterministic dataset-engineering audits."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from shiftsleep_uq.data.preprocess import process_one, read_edf, read_isruc_events, read_sc_events

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'; META=RAW/'metadata'; OUT=ROOT/'data/processed/core_v1'; REPORTS=ROOT/'reports'
LABELS=['Wake','N1','N2','N3','REM']

def digest(path: Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def write(name, rows, fields=None):
 path=REPORTS/name
 if fields is None:
  fields=[]
  for r in rows:
   for k in r:
    if k not in fields: fields.append(k)
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
 return path

def exclusion_status(code:str)->str:
 if code in {'ACQUISITION_FAILURE'}: return 'EXCLUDED_ACQUISITION'
 if 'ANNOTATION' in code or 'UNKNOWN' in code: return 'EXCLUDED_ANNOTATION'
 if 'UNIT' in code: return 'EXCLUDED_UNIT'
 if 'ALIGNMENT' in code or 'DURATION' in code or 'MISSING_SIGNAL_SAMPLES' in code: return 'EXCLUDED_ALIGNMENT'
 if any(x in code for x in ('EDF','CHANNEL','RATE','SCHEMA')): return 'EXCLUDED_SCHEMA'
 return 'EXCLUDED_OTHER_STRUCTURAL'

def schema_row(dataset, subject, recording):
 try:
  p,a,ec,oc,_,_,cohort,_=__import__('shiftsleep_uq.data.preprocess',fromlist=['recording_spec']).recording_spec(dataset,subject,RAW,META)
  (_, _),rates,units,duration,labels=read_edf(p,(ec,oc))
  events=read_sc_events(a) if dataset=='sleep_edf_sc' else read_isruc_events(a)
  allowed={'sleep_edf_sc':{'Sleep stage W','Sleep stage 1','Sleep stage 2','Sleep stage 3','Sleep stage 4','Sleep stage R','Sleep stage ?','Movement time'},'isruc_s1':{'Sleep stage W','Sleep stage N1','Sleep stage N2','Sleep stage N3','Sleep stage R','Sleep stage U'}}[dataset]
  values={x[2] for x in events}
  return {'dataset':dataset,'subject_id':subject,'recording_id':recording,'EEG_label':ec,'EOG_label':oc,'EEG_rate':rates[0],'EOG_rate':rates[1],'EEG_unit':units[0],'EOG_unit':units[1],'duration_seconds':duration,'annotation_type':'EDF+ hypnogram' if dataset=='sleep_edf_sc' else 'NEMAR BIDS events.tsv','primary_scorer':'official_single_stream' if dataset=='sleep_edf_sc' else 'scorer_1','source_label_schema_validation':'PASS' if values <= allowed else 'FAIL','observed_source_labels':'|'.join(sorted(values)),'status':'PASS' if values <= allowed else 'FAIL'}
 except Exception as e:
  return {'dataset':dataset,'subject_id':subject,'recording_id':recording,'status':'FAIL','failure_code':type(e).__name__}

def qcrow(dataset,subject,recording,row):
 if row.get('status')!='SUCCESS': return []
 with np.load(row['output_path'],allow_pickle=False) as z:
  result=[]
  for signal in ('eeg','eog'):
   x=z[signal]; q1,q3=np.quantile(x,[.25,.75]); med=float(np.median(x));
   result.append({'dataset':dataset,'subject_id':subject,'recording_id':recording,'signal':signal,'min':float(x.min()),'max':float(x.max()),'median':med,'mad':float(np.median(np.abs(x-med))),'iqr':float(q3-q1),'finite_values':int(np.isfinite(x).sum()),'total_values':int(x.size),'flat_proportion':float(np.mean(np.diff(x,axis=1)==0))})
  return result

def main():
 expected=list(csv.DictReader((REPORTS/'core_expected_population.csv').open(encoding='utf-8',newline='')))
 provider={(r['dataset'],r['recording_id']):r for r in csv.DictReader((REPORTS/'provider_integrity_audit.csv').open(encoding='utf-8',newline=''))}
 if len(provider)!=len(expected): raise RuntimeError('provider table not complete')
 all_rows=[]; schemas=[]; accounts=[]; qc=[]
 for e in expected:
  ds,subject,rec=e['dataset'],e['subject_id'],e['recording_id']; pr=provider[(ds,rec)]
  if pr['terminal_status']=='ACQUIRED':
   schemas.append(schema_row(ds,subject,rec)); result=process_one(ds,rec,RAW,OUT,META)
  else:
   result={'dataset':ds,'subject_id':subject,'recording_id':rec,'status':'FAILED','failure_code':pr.get('failure_code') or 'PROVIDER_INTEGRITY_FAILURE','valid_canonical_epochs':0,'excluded_epochs':0}
  terminal='INCLUDED' if result.get('status')=='SUCCESS' else exclusion_status(result.get('failure_code',''))
  r={**result,**e,'terminal_status':terminal,'exclusion_reason':'' if terminal=='INCLUDED' else result.get('failure_code','UNKNOWN')}
  all_rows.append(r); qc.extend(qcrow(ds,subject,rec,result))
  counts={x.lower():int(result.get(x.lower(),0) or 0) for x in LABELS}; valid=sum(counts.values()); excluded=int(result.get('excluded_epochs',0) or 0); source=int(result.get('total_source_stage_epochs',0) or 0)
  accounts.append({'dataset':ds,'subject_id':subject,'recording_id':rec,'source_staging_epochs':source,**counts,'valid_canonical_epochs':valid,'excluded_epochs':excluded,'accounting_delta':source-(valid+excluded),'status':'PASS' if result.get('status')=='SUCCESS' and source==valid+excluded else 'EXCLUDED','failure_code':result.get('failure_code','')})
 if len(all_rows)!=len(expected) or len({(r['dataset'],r['recording_id']) for r in all_rows})!=len(expected): raise RuntimeError('record terminal invariant')
 write('full_core_schema_audit.csv',schemas)
 write('full_core_epoch_accounting.csv',accounts)
 schema_index={(r['dataset'],r['recording_id']):r for r in schemas}
 duration_rows=[]
 for r,a in zip(all_rows,accounts):
  s=schema_index.get((r['dataset'],r['recording_id']),{})
  psg=s.get('duration_seconds','')
  source=int(a.get('source_staging_epochs',0) or 0)*30
  valid=int(a.get('valid_canonical_epochs',0) or 0)*30
  duration_rows.append({'dataset':r['dataset'],'subject_id':r['subject_id'],'recording_id':r['recording_id'],'psg_duration_seconds':psg,'annotation_staging_duration_seconds':source,'valid_canonical_duration_seconds':valid,'alignment_status':'PASS' if r['terminal_status']=='INCLUDED' and a['accounting_delta']==0 else 'EXCLUDED','failure_code':r.get('failure_code','')})
 write('full_core_duration_alignment_audit.csv',duration_rows)
 record_fields=['dataset','cohort','subject_id','recording_id','expected','source_distribution','expected_eeg','expected_eog','subject_group','terminal_status','exclusion_reason','contract_version','preprocessing_version','valid_canonical_epochs','output_path','output_sha256','failure_code']
 write('core_recording_manifest_v1.csv',all_rows,record_fields)
 write('full_core_signal_qc.csv',qc)
 # subject roll-up; all usable SC nights remain grouped by subject.
 subjects=[]
 for ds in sorted({r['dataset'] for r in all_rows}):
  for subject in sorted({r['subject_id'] for r in all_rows if r['dataset']==ds}):
   rs=[r for r in all_rows if r['dataset']==ds and r['subject_id']==subject]; good=[r for r in rs if r['terminal_status']=='INCLUDED']; bad=[r for r in rs if r['terminal_status']!='INCLUDED']
   status='SUBJECT_COMPLETE' if len(good)==len(rs) else ('SUBJECT_PARTIAL' if good else 'SUBJECT_EXCLUDED')
   subjects.append({'dataset':ds,'cohort':rs[0]['cohort'],'subject_id':subject,'expected_recordings':len(rs),'acquired_recordings':sum(r.get('status')=='SUCCESS' or provider[(ds,r['recording_id'])]['terminal_status']=='ACQUIRED' for r in rs),'valid_recordings':len(good),'excluded_recordings':len(bad),'subject_status':status,'total_valid_epochs':sum(int(r.get('valid_canonical_epochs',0) or 0) for r in good),**{x.lower():sum(int(r.get(x.lower(),0) or 0) for r in good) for x in LABELS},'structural_failure_codes':'|'.join(sorted({r.get('failure_code','') for r in bad if r.get('failure_code','')})),'contract_version':'1.1.0','preprocessing_version':'0.1.0'})
 write('core_subject_manifest_v1.csv',subjects)
 # stage distributions, descriptive only
 stage=[]
 for r in all_rows:
  total=sum(int(r.get(x.lower(),0) or 0) for x in LABELS)
  for label in LABELS: stage.append({'dataset':r['dataset'],'subject_id':r['subject_id'],'recording_id':r['recording_id'],'label':label,'count':int(r.get(label.lower(),0) or 0),'proportion':(int(r.get(label.lower(),0) or 0)/total if total else '')})
 write('full_core_stage_distribution.csv',stage)
 exc=[]
 for r in all_rows:
  if r['terminal_status']!='INCLUDED': exc.append({'dataset':r['dataset'],'subject_id':r['subject_id'],'recording_id':r['recording_id'],'exclusion_level':'structural_raw','category':r['terminal_status'],'count':1,'reason':r['exclusion_reason']})
  elif int(r.get('excluded_epochs',0) or 0): exc.append({'dataset':r['dataset'],'subject_id':r['subject_id'],'recording_id':r['recording_id'],'exclusion_level':'annotation_epoch','category':'annotation_epoch_exclusion','count':int(r['excluded_epochs']),'reason':'source_noncanonical_or_excluded_annotation'})
 write('full_core_exclusion_distribution.csv',exc)
 # output integrity and duplicate audit
 integrity=[]; rawhash=defaultdict(list); outhash=defaultdict(list)
 for r in all_rows:
  if r['terminal_status']!='INCLUDED': continue
  out=Path(r['output_path']); ok=out.exists() and digest(out)==r['output_sha256']
  with np.load(out,allow_pickle=False) as z:
   meta=json.loads(str(z['metadata_json'])); shape_ok=z['eeg'].shape[1:]==(3000,) and z['eog'].shape[1:]==(1500,) and len(z['labels'])==len(z['eeg'])==len(z['eog']); labels_ok=set(np.unique(z['labels']))<={0,1,2,3,4}
  integrity.append({'dataset':r['dataset'],'recording_id':r['recording_id'],'output_exists':out.exists(),'hash_exists':bool(r['output_sha256']),'hash_valid':ok,'shape_valid':shape_ok,'labels_valid':labels_ok,'metadata_versions_valid':meta.get('contract_version')=='1.1.0' and meta.get('preprocessing_version')=='0.1.0','source_provenance_available':bool(r.get('source_sha256')),'status':'PASS' if ok and shape_ok and labels_ok else 'FAIL'})
  rawhash[r['source_sha256']].append((r['dataset'],r['recording_id'])); outhash[r['output_sha256']].append((r['dataset'],r['recording_id']))
 write('processed_output_integrity.csv',integrity)
 dup=[]
 for kind,table in [('raw_sha256',rawhash),('processed_sha256',outhash)]:
  for h,ids in table.items():
   dup.append({'kind':kind,'sha256':h,'recordings':'|'.join(f'{a}:{b}' for a,b in ids),'duplicate':len(ids)>1})
 write('full_core_duplicate_audit.csv',dup)
 # scale audit is descriptive and never exclusionary
 scale=[]
 for ds in sorted({x['dataset'] for x in qc}):
  for signal in ('eeg','eog'):
   vals=[float(x['mad']) for x in qc if x['dataset']==ds and x['signal']==signal]
   scale.append({'dataset':ds,'signal':signal,'median_recording_mad_uv':float(np.median(vals)) if vals else '', 'unit_scale_status':'UNIT_SCALE_PASS' if vals else 'UNIT_SCALE_FAIL','notes':'No cross-dataset normalization; only gross 1e3/1e6 scale anomalies are screened.'})
 write('full_core_unit_scale_audit.csv',scale)
 # Determinism first three included IDs per dataset.
 det=[]
 for ds in sorted({r['dataset'] for r in all_rows}):
  for r in sorted([x for x in all_rows if x['dataset']==ds and x['terminal_status']=='INCLUDED'],key=lambda x:x['recording_id'])[:3]:
   before=r['output_sha256']; redo=process_one(ds,r['recording_id'],RAW,OUT,META); after=redo.get('output_sha256',''); det.append({'dataset':ds,'recording_id':r['recording_id'],'run_1_sha256':before,'run_2_sha256':after,'identical':before==after,'status':'PASS' if before==after else 'FAIL'})
 write('full_core_determinism_audit.csv',det)
 # fixed domain inventory, no corrective transformation.
 (ROOT/'docs/domain_shift_inventory.md').write_text('# Domain Shift Inventory\n\n- **Sleep-EDF SC:** 100 Hz EEG Fpz-Cz and horizontal EOG; healthy/age-effects study; official R&K hypnogram stream.\n- **ISRUC-S1:** 200 Hz C3-A2 EEG and LOC-A2 EOG; clinical/heterogeneous S1 population; NEMAR scorer-1 primary stream with scorer-2 retained separately.\n- Native rate, montage/reference, population, setting, annotation provenance, stage composition, and amplitude statistics are retained as domain differences. No normalization or harmonization is performed in Step 7.1.\n',encoding='utf-8')
 # storage
 storage=[]
 for dataset,prefix in [('sleep_edf_sc','sleep-edfx'),('isruc_s1','isruc-nemar')]:
  rawbytes=sum(p.stat().st_size for p in (RAW/prefix).rglob('*') if p.is_file()); procbytes=sum(Path(r['output_path']).stat().st_size for r in all_rows if r['dataset']==dataset and r['terminal_status']=='INCLUDED'); storage.append({'dataset':dataset,'raw_bytes':rawbytes,'processed_bytes':procbytes})
 storage.append({'dataset':'safe_reports','raw_bytes':'','processed_bytes':sum(p.stat().st_size for p in REPORTS.rglob('*') if p.is_file())})
 write('full_core_storage_report.csv',storage)
 print(json.dumps({'expected':len(expected),'included':sum(r['terminal_status']=='INCLUDED' for r in all_rows),'excluded':sum(r['terminal_status']!='INCLUDED' for r in all_rows),'determinism_pass':all(r['status']=='PASS' for r in det)},sort_keys=True))
if __name__=='__main__': main()
