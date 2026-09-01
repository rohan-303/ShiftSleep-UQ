"""Build Step 4 machine-readable registries from official metadata/header audits."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'reports'

def read(p): return list(csv.DictReader(open(p,encoding='utf-8')))
def write(name, fields, rows):
 with (R/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

write('dataset_access_registry.csv',['dataset','version','official_source','doi','access_type','license','account_required','approval_required','raw_access_status','redistribution_allowed','verification_date','notes'],[
 {'dataset':'Sleep-EDF Expanded','version':'1.0.0','official_source':'https://physionet.org/content/sleep-edfx/1.0.0/','doi':'10.13026/C2X676','access_type':'open','license':'ODC Attribution License v1.0','account_required':'NO','approval_required':'NO','raw_access_status':'RANGE_HEADER_VERIFIED; FULL_NOT_DOWNLOADED','redistribution_allowed':'LICENSE_REVIEW_REQUIRED','verification_date':'2026-09-01','notes':'SC/ST audited separately; official page says anyone may access subject to license.'},
 {'dataset':'ISRUC-Sleep','version':'NOT_VERIFIED','official_source':'https://sleeptight.isr.uc.pt/','doi':'NOT_VERIFIED','access_type':'official site inaccessible','license':'NOT_VERIFIED','account_required':'NOT_VERIFIED','approval_required':'NOT_VERIFIED','raw_access_status':'ACCESS_UNRESOLVED','redistribution_allowed':'NOT_VERIFIED','verification_date':'2026-09-01','notes':'Requested official resource returned 404 at audited URL; no unofficial mirror used.'},
 {'dataset':'SHHS','version':'SHHS1/SHHS2','official_source':'https://sleepdata.org/datasets/shhs','doi':'NOT_VERIFIED','access_type':'NSRR account/access controls','license':'NOT_VERIFIED','account_required':'YES/VERIFY','approval_required':'NOT_VERIFIED','raw_access_status':'RAW_ACCESS_PENDING','redistribution_allowed':'NOT_VERIFIED','verification_date':'2026-09-01','notes':'Public documentation and access state require further official verification; credentials not requested.'},
 {'dataset':'CAP Sleep Database','version':'1.0.0','official_source':'https://physionet.org/content/capslpdb/1.0.0/','doi':'NOT_VERIFIED','access_type':'open','license':'ODC/license terms VERIFY','account_required':'NO','approval_required':'NO','raw_access_status':'RANGE_HEADER_PARTIAL','redistribution_allowed':'LICENSE_REVIEW_REQUIRED','verification_date':'2026-09-01','notes':'108 records listed officially; 13 headers parsed in current network window; remaining failures preserved.'},
])

sleep=read(R/'sleep_edf_channel_inventory.csv'); cap=read(R/'cap_channel_inventory.csv'); rows=[]
for src in sleep+cap:
 if src['status']!='VERIFIED': continue
 labels=src['labels'].split('|'); rates=src['sampling_hz'].split('|'); dims=src['physical_dimensions'].split('|')
 for i,label in enumerate(labels):
  low=label.lower(); mod='EEG' if 'eeg' in low or any(x in low for x in ['fp','f3','f4','c3','c4','o1','o2']) else ('EOG' if 'eog' in low or low in ['roc-loc','loc-roc'] else ('EMG' if 'emg' in low or 'tib' in low else 'OTHER'))
  rows.append({'dataset':src['dataset'],'substudy':'SC' if '/sleep-cassette/' in src['recording_path'] else ('ST' if '/sleep-telemetry/' in src['recording_path'] else 'NOT_VERIFIED'),'recording_id':src['recording_path'].split('/')[-1],'subject_id':'NOT_VERIFIED','signal_label':label,'modality_family':mod,'reference':'encoded in label; anatomical/reference interpretation requires contract review','sampling_hz':rates[i] if i<len(rates) else 'NOT_VERIFIED','physical_dimension':dims[i] if i<len(dims) else 'NOT_VERIFIED','signal_representation':'SC EMG envelope documented; CAP representation NOT_VERIFIED per channel','schema_source':src['url'],'verified':'TRUE','notes':'Header-only; no signal samples read.'})
write('dataset_schema_manifest.csv',['dataset','substudy','recording_id','subject_id','signal_label','modality_family','reference','sampling_hz','physical_dimension','signal_representation','schema_source','verified','notes'],rows)

rec=[]
for r in read(R/'sleep_edf_subject_manifest.csv'):
 rec.append({'dataset':r['dataset'],'substudy':r['substudy'],'subject_id':r['subject_id'],'recording_id':r['recording_id'],'night_or_visit':r['night'],'treatment':r['treatment_condition_if_verified'],'pathology_group':'healthy / mild difficulty falling asleep; source-specific','psg_file':r['psg_filename'],'annotation_file':r['annotation_filename'],'repeat_subject':'TRUE' if r['substudy']=='SC' or r['substudy']=='ST' else 'NOT_VERIFIED','identity_source':'official filename convention','identity_confidence':r['identity_confidence'],'notes':r['notes']})
for r in cap:
 stem=r['recording_path']; p=stem.rsplit('/',1)[-1].replace('.edf','')
 group='healthy' if p.startswith('n') and not p.startswith('nfle') else ('pathology-coded filename; exact subject mapping not verified')
 rec.append({'dataset':r['dataset'],'substudy':'NOT_APPLICABLE','subject_id':'NOT_VERIFIED','recording_id':p,'night_or_visit':'NOT_VERIFIED','treatment':'NOT_APPLICABLE','pathology_group':group,'psg_file':stem,'annotation_file':p+'.txt / '+p+'.edf.st','repeat_subject':'NOT_VERIFIED','identity_source':'official filename pathology code only','identity_confidence':'LOW','notes':'CAP official page identifies 16 healthy subjects and 92 pathological recordings, but recording-to-subject mapping is not established.'})
write('dataset_recording_manifest.csv',['dataset','substudy','subject_id','recording_id','night_or_visit','treatment','pathology_group','psg_file','annotation_file','repeat_subject','identity_source','identity_confidence','notes'],rec)

write('acquisition_manifest.csv',['official_url','dataset_version','filename','byte_size','sha256','acquisition_date','license_access_category','checksum_status'],[
 {'official_url':'https://physionet.org/files/sleep-edfx/1.0.0/RECORDS','dataset_version':'Sleep-EDF 1.0.0','filename':'RECORDS','byte_size':'6348','sha256':'444cb5be68f22dfcc1a4114e6b8b8f99319e28ce7cdd130750d75109b1408286','acquisition_date':'2026-09-01','license_access_category':'official metadata / ODC terms','checksum_status':'MATCH'},
 {'official_url':'https://physionet.org/files/sleep-edfx/1.0.0/SHA256SUMS.txt','dataset_version':'Sleep-EDF 1.0.0','filename':'SHA256SUMS.txt','byte_size':'NOT_RECORDED','sha256':'1bc88e19e2e921f7851d7cf61e31ceb8f6d670211ca546a323e9db5a77525edf','acquisition_date':'2026-09-01','license_access_category':'official checksum metadata','checksum_status':'NO_OFFICIAL_CHECKSUM_FOR_CHECKSUM_FILE'},
 {'official_url':'https://physionet.org/files/sleep-edfx/1.0.0/SC-subjects.xls','dataset_version':'Sleep-EDF 1.0.0','filename':'SC-subjects.xls','byte_size':'NOT_RECORDED','sha256':'93d65494096d375ee302f1ce3a0506575b17a918b93d7cdaa5a2b32727366080','acquisition_date':'2026-09-01','license_access_category':'official metadata / ODC terms','checksum_status':'MATCH'},
 {'official_url':'https://physionet.org/files/sleep-edfx/1.0.0/ST-subjects.xls','dataset_version':'Sleep-EDF 1.0.0','filename':'ST-subjects.xls','byte_size':'NOT_RECORDED','sha256':'b377133e03897559e9e9fa8ef468f4505becaecebe1bc0c988d39a9158267758','acquisition_date':'2026-09-01','license_access_category':'official metadata / ODC terms','checksum_status':'MATCH'},
 {'official_url':'https://physionet.org/files/capslpdb/1.0.0/RECORDS','dataset_version':'CAP 1.0.0','filename':'RECORDS','byte_size':'1044','sha256':'b794825833c98285c6e9f6052af79837afc1ac1939f7e410fdfc88dded52f945','acquisition_date':'2026-09-01','license_access_category':'official metadata / license terms','checksum_status':'MATCH'},
 {'official_url':'https://physionet.org/files/capslpdb/1.0.0/gender-age.xlsx','dataset_version':'CAP 1.0.0','filename':'gender-age.xlsx','byte_size':'NOT_RECORDED','sha256':'9d7a4c54f352412e1b0a8793f6124d1aef7b318a13b027a2f88e497719654f36','acquisition_date':'2026-09-01','license_access_category':'official metadata / license terms','checksum_status':'NO_OFFICIAL_CHECKSUM'},
])
print('generated registries:',len(rows),'schema rows;',len(rec),'recording rows')
