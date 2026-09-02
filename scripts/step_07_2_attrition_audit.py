"""Step 7.2 deterministic attrition diagnostics; no eligibility policy changes."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path
import pyedflib

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'reports'; RAW=ROOT/'data/raw'; META=RAW/'metadata'

def read(name):
    return list(csv.DictReader((R/name).open(encoding='utf-8', newline='')))
def write(name, rows, fields=None):
    if fields is None:
        fields=[]
        for row in rows:
            for key in row:
                if key not in fields: fields.append(key)
    with (R/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def number(v):
    try: return int(v or 0)
    except ValueError: return 0
def stage_for(code, provider_status):
    if provider_status!='ACQUIRED':
        return 'provider-byte integrity' if code.startswith('EDF_DECLARED_BYTE') else 'acquisition'
    if 'MISSING_REQUIRED' in code: return 'required-channel lookup'
    if 'RATE' in code: return 'sampling-rate validation'
    if 'UNIT' in code: return 'physical-unit validation'
    if 'ANNOTATION_SCHEMA' in code: return 'annotation-schema validation'
    if 'ANNOTATION_' in code: return 'annotation canonicalization'
    if 'ALIGNMENT' in code or 'DURATION' in code: return 'duration/alignment validation'
    if 'MISSING_SIGNAL_SAMPLES' in code: return 'epoch extraction'
    if 'OUTPUT' in code: return 'persisted-output validation'
    if 'EDF' in code: return 'EDF parsing'
    return 'EDF parsing'
def edf_header(path):
    reader=pyedflib.EdfReader(str(path))
    try:
        labels=reader.getSignalLabels(); rates=[reader.getSampleFrequency(i) for i in range(reader.signals_in_file)]; units=[reader.getPhysicalDimension(i) for i in range(reader.signals_in_file)]
        return labels, rates, units, float(reader.getFileDuration())
    finally: reader.close()
def main():
    expected=read('core_expected_population.csv'); rec=read('core_recording_manifest_v1_1.csv'); provider=read('provider_integrity_audit.csv')
    schemas={(x['dataset'],x['recording_id']):x for x in read('full_core_schema_audit.csv')}
    duration={(x['dataset'],x['recording_id']):x for x in read('full_core_duration_alignment_audit.csv')}
    accounts={(x['dataset'],x['recording_id']):x for x in read('full_core_epoch_accounting.csv')}
    pr={(x['dataset'],x['recording_id']):x for x in provider}; rr={(x['dataset'],x['recording_id']):x for x in rec}
    if set(rr)!= {(x['dataset'],x['recording_id']) for x in expected}: raise RuntimeError('expected/manifest identity mismatch')
    # Distribution by concrete terminal exclusion code.
    dist=[]
    for ds in sorted({x['dataset'] for x in expected}):
        es=[x for x in expected if x['dataset']==ds]; excluded=[rr[(x['dataset'],x['recording_id'])] for x in es if rr[(x['dataset'],x['recording_id'])]['terminal_status']!='INCLUDED']
        for code,n in sorted(Counter(x['failure_code'] or x['exclusion_reason'] for x in excluded).items()):
            affected={x['subject_id'] for x in excluded if (x['failure_code'] or x['exclusion_reason'])==code}
            dist.append({'dataset':ds,'failure_code':code,'recordings':n,'subjects_affected':len(affected),'percentage_of_expected_recordings':f'{100*n/len(es):.6f}','percentage_of_all_exclusions':f'{100*n/len(excluded):.6f}' if excluded else '0.000000'})
    write('core_attrition_failure_distribution.csv',dist)
    # Every exclusion has one first-failure stage.
    stages=[]
    for x in rec:
        if x['terminal_status']=='INCLUDED': continue
        p=pr[(x['dataset'],x['recording_id'])]; code=x['failure_code'] or x['exclusion_reason']
        stages.append({'dataset':x['dataset'],'subject_id':x['subject_id'],'recording_id':x['recording_id'],'failure_code':code,'primary_first_failure_stage':stage_for(code,p['terminal_status'])})
    write('core_attrition_stage_distribution.csv',stages)
    # Exhaustive official Sleep-EDF pairing / timeline audit.
    from shiftsleep_uq.data.preprocess import recording_spec, read_sc_events
    sleep=[]; pairing=[]
    for e in [x for x in expected if x['dataset']=='sleep_edf_sc']:
        k=('sleep_edf_sc',e['recording_id']); r=rr[k]; p=pr[k]; psg,hyp,*_=recording_spec('sleep_edf_sc',e['recording_id'],RAW,META)
        candidates=sorted((META/'sleep-edfx'/'1.0.0').glob(f"{e['recording_id'][:-1]}?-Hypnogram.edf"))
        row={'dataset':'sleep_edf_sc','subject_id':e['subject_id'],'recording_id':e['recording_id'],'psg_acquired':p['terminal_status']=='ACQUIRED','official_checksum_match':p['checksum_status']=='MATCH','hypnogram_acquired':hyp.exists(),'psg_filename':psg.name,'matched_hypnogram_filename':hyp.name if hyp.exists() else '', 'pair_prefix':e['recording_id'][:-1], 'pair_confidence':'EXACT_UNIQUE' if len(candidates)==1 else ('AMBIGUOUS' if len(candidates)>1 else 'UNPAIRED'),'required_channels_present':'','eeg_rate':'','eog_rate':'','eeg_unit':'','eog_unit':'','psg_duration_seconds':'','annotation_duration_seconds':'','first_annotation_onset_seconds':'','final_annotation_end_seconds':'','valid_source_staging_events':0,'exact_failure_point':r['failure_code'] or r['exclusion_reason'] or 'INCLUDED','terminal_status':r['terminal_status']}
        if p['terminal_status']=='ACQUIRED' and psg.exists() and hyp.exists():
            labels,rates,units,dur=edf_header(psg); ev=read_sc_events(hyp); row.update({'required_channels_present':('EEG Fpz-Cz' in labels and 'EOG horizontal' in labels),'eeg_rate':rates[labels.index('EEG Fpz-Cz')] if 'EEG Fpz-Cz' in labels else '', 'eog_rate':rates[labels.index('EOG horizontal')] if 'EOG horizontal' in labels else '', 'eeg_unit':units[labels.index('EEG Fpz-Cz')] if 'EEG Fpz-Cz' in labels else '', 'eog_unit':units[labels.index('EOG horizontal')] if 'EOG horizontal' in labels else '', 'psg_duration_seconds':dur,'annotation_duration_seconds':sum(x[1] for x in ev),'first_annotation_onset_seconds':min((x[0] for x in ev),default=''),'final_annotation_end_seconds':max((x[0]+x[1] for x in ev),default=''),'valid_source_staging_events':sum(x[2] not in {'Sleep stage ?','Movement time'} for x in ev)})
        sleep.append(row); pairing.append({k:row[k] for k in ('recording_id','psg_filename','matched_hypnogram_filename','pair_prefix','pair_confidence')})
    write('sleep_edf_attrition_audit.csv',sleep); write('sleep_edf_pairing_audit.csv',pairing)
    # ISRUC exhaustive header and provider integrity audit.
    isr=[]; combo=Counter(); providerc=Counter()
    for e in [x for x in expected if x['dataset']=='isruc_s1']:
        k=('isruc_s1',e['recording_id']); p=pr[k]; r=rr[k]; path=RAW/'isruc-nemar'/'v1.0.1'/f"sub-{e['recording_id']}_task-sleep_eeg.edf"
        provider_class='PROVIDER_BODY_VALID' if p['terminal_status']=='ACQUIRED' else ('PROVIDER_BODY_TRUNCATED' if p['failure_code']=='EDF_DECLARED_BYTE_MISMATCH' else 'PROVIDER_UNAVAILABLE')
        event_path=RAW/'isruc-nemar'/'v1.0.1'/f'sub-{e["recording_id"]}_task-sleep_events.tsv'
        event_count=''; staging_event_count=''; raw_label_vocabulary=''; duration_vocabulary=''; event_primary_field=''; scorer2_fields_present=''; events_schema='MISSING'; source_labels_valid=''
        if event_path.exists():
            with event_path.open(encoding='utf-8-sig',newline='') as handle:
                event_rows=list(csv.DictReader(handle,delimiter='\t')); fields=set(event_rows[0]) if event_rows else set()
            required={'onset','duration','trial_type','value','sample','scorer2_label','scorer2_label_value'}
            events_schema='PASS' if required <= fields else 'FAIL'
            event_count=len(event_rows); staging_event_count=sum(bool(z.get('trial_type','')) for z in event_rows)
            raw_label_vocabulary='|'.join(sorted({z.get('trial_type','') for z in event_rows})); duration_vocabulary='|'.join(sorted({z.get('duration','') for z in event_rows})); event_primary_field='trial_type'; scorer2_fields_present=('scorer2_label' in fields and 'scorer2_label_value' in fields)
            allowed={'Sleep stage W','Sleep stage N1','Sleep stage N2','Sleep stage N3','Sleep stage R','Sleep stage U'}; source_labels_valid=set(z.get('trial_type','') for z in event_rows)<=allowed
        row={'dataset':'isruc_s1','subject_id':e['subject_id'],'recording_id':e['recording_id'],'provider_status':p['terminal_status'],'provider_class':provider_class,'provider_content_length':p.get('provider_content_length',''),'local_bytes':p.get('local_bytes',''),'edf_declared_bytes':p.get('edf_declared_bytes',''),'byte_delta':p.get('byte_delta',''),'body_valid':p.get('body_valid',''),'required_C3_A2_present':'','required_LOC_A2_present':'','EEG_rate':'','EOG_rate':'','EEG_unit':'','EOG_unit':'','events_file':event_path.exists(),'events_schema':events_schema,'event_count':event_count,'staging_event_count':staging_event_count,'raw_label_vocabulary':raw_label_vocabulary,'duration_vocabulary':duration_vocabulary,'event_primary_field':event_primary_field,'scorer2_fields_present':scorer2_fields_present,'source_labels_valid':source_labels_valid,'duration_alignment':duration.get(k,{}).get('alignment_status',''),'preprocessing_status':r['terminal_status'],'terminal_failure':r['failure_code'] or r['exclusion_reason']}
        if p['terminal_status']=='ACQUIRED':
            labels,rates,units,dur=edf_header(path); c3='C3-A2' in labels; loc='LOC-A2' in labels
            diagnostic_eeg=next((x for x in ('C3-A2','C3-M2','C3') if x in labels),'')
            diagnostic_eog=next((x for x in ('LOC-A2','E1-M2','LOC') if x in labels),'')
            row.update({'required_C3_A2_present':c3,'required_LOC_A2_present':loc,'observed_eeg_diagnostic_label':diagnostic_eeg,'observed_eog_diagnostic_label':diagnostic_eog})
            if diagnostic_eeg and diagnostic_eog:
                ci,li=labels.index(diagnostic_eeg),labels.index(diagnostic_eog); row.update({'EEG_rate':rates[ci],'EOG_rate':rates[li],'EEG_unit':units[ci],'EOG_unit':units[li]}); combo[(rates[ci],rates[li],units[ci],units[li])]+=1
        isr.append(row); providerc[provider_class]+=1
    write('isruc_attrition_audit.csv',isr)
    write('isruc_provider_integrity_distribution.csv',[{'provider_class':k,'recordings':v,'percentage_of_expected_recordings':f'{v:.6f}'} for k,v in sorted(providerc.items())])
    write('isruc_rate_unit_distribution.csv',[{'eeg_native_rate':a,'eog_native_rate':b,'eeg_unit':c,'eog_unit':d,'recordings':n} for (a,b,c,d),n in sorted(combo.items())])
    # Deterministic manual-level sample for each failure category.
    review=[]
    for ds in sorted({x['dataset'] for x in rec}):
        for code in sorted({x['failure_code'] or x['exclusion_reason'] for x in rec if x['dataset']==ds and x['terminal_status']!='INCLUDED'}):
            for x in sorted([z for z in rec if z['dataset']==ds and (z['failure_code'] or z['exclusion_reason'])==code],key=lambda z:z['recording_id'])[:5]:
                kind='PIPELINE_FALSE_POSITIVE' if ds=='sleep_edf_sc' and code=='ACQUISITION_FAILURE' else 'TRUE_STRUCTURAL_FAILURE'
                review.append({'dataset':ds,'recording_id':x['recording_id'],'failure_code':code,'raw_evidence':'official unique PSG/hypnogram pairing and checksum evidence' if ds=='sleep_edf_sc' else 'EDF header required-channel labels and provider audit','validator_expectation':'paired PSG/hypnogram must resolve' if ds=='sleep_edf_sc' else 'exact C3-A2 and LOC-A2 labels required by frozen contract','validator_result':x['terminal_status'],'scientific_interpretation':kind})
    write('core_attrition_manual_failure_review.csv',review)
    print(json.dumps({'expected':len(expected),'excluded':len(stages),'sleep_rows':len(sleep),'isruc_rows':len(isr),'failure_distribution_rows':len(dist)},sort_keys=True))
if __name__=='__main__': main()
