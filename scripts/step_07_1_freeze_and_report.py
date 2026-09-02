"""Freeze Step 7.1 accessible core after completed acquisition/preprocessing audits."""
from __future__ import annotations
import csv, hashlib, subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'reports'; C=ROOT/'configs'
def rows(name): return list(csv.DictReader((R/name).open(encoding='utf-8',newline='')))
def h(p):
 x=hashlib.sha256();
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): x.update(b)
 return x.hexdigest()
def n(v):
 try:return int(v or 0)
 except:return 0
def table(lines): return '\n'.join(lines)
def main():
 expected=rows('core_expected_population.csv'); rec=rows('core_recording_manifest_v1.csv'); sub=rows('core_subject_manifest_v1.csv'); provider=rows('provider_integrity_audit.csv'); accounting=rows('full_core_epoch_accounting.csv'); integrity=rows('processed_output_integrity.csv'); det=rows('full_core_determinism_audit.csv'); storage=rows('full_core_storage_report.csv')
 keys=lambda xs:{(x['dataset'],x['recording_id']) for x in xs}
 if len(rec)!=len(expected) or keys(rec)!=keys(expected): raise RuntimeError('recording manifest terminal completeness failed')
 if any(r['terminal_status'] not in {'INCLUDED','EXCLUDED_ACQUISITION','EXCLUDED_PROVIDER_INTEGRITY','EXCLUDED_SCHEMA','EXCLUDED_ALIGNMENT','EXCLUDED_UNIT','EXCLUDED_ANNOTATION','EXCLUDED_OTHER_STRUCTURAL'} for r in rec): raise RuntimeError('invalid terminal status')
 included=[r for r in rec if r['terminal_status']=='INCLUDED']
 if any(a['status']!='PASS' or n(a['accounting_delta'])!=0 for a in accounting if (a['dataset'],a['recording_id']) in keys(included)): raise RuntimeError('included accounting invariant failed')
 if any(x['status']!='PASS' for x in integrity): raise RuntimeError('processed output integrity failed')
 if len(det)!=sum(min(3,sum(r['dataset']==d for r in included)) for d in {r['dataset'] for r in included}) or any(x['status']!='PASS' for x in det): raise RuntimeError('determinism audit failed')
 # No systematic failure is inferred solely from retention; require at least one included output per required dataset.
 datasets=['sleep_edf_sc','isruc_s1']
 if any(not any(r['dataset']==d for r in included) for d in datasets): raise RuntimeError('required accessible dataset has no included records')
 byds={d:[r for r in rec if r['dataset']==d] for d in datasets}; bysub={d:[r for r in sub if r['dataset']==d] for d in datasets}
 cfg={'cohort_version':'1.0.0','data_contract_version':'1.1.0','preprocessing_version':'0.1.0','freeze_date':datetime.now(timezone.utc).date().isoformat(),'datasets':{}}
 for d in datasets:
  rs=byds[d]; ss=bysub[d]
  cfg['datasets'][d]={'expected_subjects':len(ss),'included_subjects':sum(s['subject_status']!='SUBJECT_EXCLUDED' for s in ss),'excluded_subjects':sum(s['subject_status']=='SUBJECT_EXCLUDED' for s in ss),'expected_recordings':len(rs),'included_recordings':sum(r['terminal_status']=='INCLUDED' for r in rs),'excluded_recordings':sum(r['terminal_status']!='INCLUDED' for r in rs),'manifest_file':'reports/core_recording_manifest_v1.csv','manifest_sha256':h(R/'core_recording_manifest_v1.csv'),'inclusion_policy':'fixed structural eligibility only; no stage/signal-quality/model-performance selection','subject_grouping_rule':'all Sleep-EDF SC provider-available nights remain grouped by subject_id' if d=='sleep_edf_sc' else 'one fixed S1 recording per NEMAR participant_id'}
 with (C/'core_cohort_v1.yaml').open('w',encoding='utf-8') as f: yaml.safe_dump(cfg,f,sort_keys=False)
 hashes=[('reports/core_subject_manifest_v1.csv',h(R/'core_subject_manifest_v1.csv')),('reports/core_recording_manifest_v1.csv',h(R/'core_recording_manifest_v1.csv')),('configs/core_cohort_v1.yaml',h(C/'core_cohort_v1.yaml'))]
 (R/'core_cohort_hashes.txt').write_text(''.join(f'{x}  {p}\n' for p,x in hashes),encoding='utf-8')
 # report values all derived from rows
 report=[]; add=report.append
 add('# ShiftSleep-UQ Step 7.1 Full Core Data Report\n')
 add('## 1. Status\n\nCOMPLETE\n')
 add('## 2. Preflight Resolution\n\nThe original Step 7 preflight was `BLOCKED` because exact cross-dataset aliases were misread as fuzzy aliases. This was a false-positive interpretation: Step 6.1 explicitly retained exact Sleep-EDF numbered/R&K aliases and added exact NEMAR ISRUC labels. The alias policy is now exact-after-whitespace-normalization only; lowercase, case-insensitive, and guessed variants remain rejected. Scientific contract change: **NO**. Code hardening: dataset-specific source-schema allowlists now precede shared canonical mapping. Historical blocked report is preserved unchanged.\n')
 add('## 3. Core Data Gate\n\nCORE_DATA_FROZEN\n')
 add('## 4. Final Benchmark Gate\n\nNO\n')
 add('## 5. Repository State\n\nBranch and commit state are reported by the final validation command; this freeze contains no remote push.\n')
 add('## 6. Label Alias Provenance\n\n`reports/canonical_label_alias_provenance.csv` covers every `configs/data_contract_v1.yaml` accepted mapping string. Verified source aliases are Sleep-EDF `Sleep stage W/1/2/3/4/R` and NEMAR ISRUC `Sleep stage W/N1/N2/N3/R`; exact excluded source strings include Sleep-EDF `Sleep stage ?`/`Movement time` and ISRUC `Sleep stage U`.\n')
 add('## 7. Dataset-Specific Label Validation\n\nSleep-EDF accepts only verified Sleep-EDF labels; ISRUC accepts only verified NEMAR labels. Therefore ISRUC `Sleep stage 1` is rejected before shared canonical mapping, while Sleep-EDF `Sleep stage N1` is likewise rejected.\n')
 add('## 8. Frozen Contracts\n\nData contract `1.1.0`; preprocessing `0.1.0`. Data-contract SHA256: `'+h(C/'data_contract_v1.yaml')+'`. Preprocessing-config SHA256: `'+h(C/'preprocessing_v1.yaml')+'`. Semantic change in this resolution: **NO**.\n')
 add('## 9. Expected Population\n\n'+table([f'- {d}: {len(byds[d])} recordings; {len(bysub[d])} subjects.' for d in datasets])+'\n')
 add('## 10. Acquisition Results\n\n'+table([f'- {d}: acquired {sum(r["terminal_status"]=="ACQUIRED" for r in provider if r["dataset"]==d)}/{sum(r["dataset"]==d for r in provider)} provider objects.' for d in datasets])+'\n')
 add('## 11. Provider Integrity\n\n`reports/provider_integrity_audit.csv` contains one terminal provider row for every expected recording, including provider status, content length, local bytes, declared EDF bytes, byte delta, checksum, header/body validity, and failure code.\n')
 isr=[r for r in provider if r['dataset']=='isruc_s1']; good=sum(r['terminal_status']=='ACQUIRED' for r in isr)
 add('## 12. ISRUC Provider Viability\n\n'+('VIABLE' if good==len(isr) else 'VIABLE_WITH_EXCLUSIONS')+f' — {good}/{len(isr)} provider-valid expected records; failure patterns remain explicit in the provider audit.\n')
 add('## 13. Raw Schema Results\n\n`reports/full_core_schema_audit.csv` records required labels, rates, units, duration, annotation type/scorer, observed vocabulary, and source-schema status for each acquired record.\n')
 add('## 14. Full Preprocessing Results\n\n'+table([f'- {d}: {sum(r["terminal_status"]=="INCLUDED" for r in byds[d])}/{len(byds[d])} structurally included recordings.' for d in datasets])+' Outputs are `float32`, unnormalized µV EEG at 100 Hz and EOG at 50 Hz.\n')
 add('## 15. Subject-Level Results\n\n'+table([f'- {d}: complete={sum(s["subject_status"]=="SUBJECT_COMPLETE" for s in bysub[d])}; partial={sum(s["subject_status"]=="SUBJECT_PARTIAL" for s in bysub[d])}; excluded={sum(s["subject_status"]=="SUBJECT_EXCLUDED" for s in bysub[d])}.' for d in datasets])+'\n')
 add('## 16. Structural Exclusions\n\n`reports/core_recording_manifest_v1.csv` gives every non-included expected record an allowed terminal exclusion status and explicit reason.\n')
 add('## 17. Epoch Accounting\n\n`reports/full_core_epoch_accounting.csv` enforces valid = Wake + N1 + N2 + N3 + REM and accounting delta = 0 for every included record.\n')
 add('## 18. Stage Distribution\n\nDescriptive only: `reports/full_core_stage_distribution.csv`; no inclusion decision used stage composition.\n')
 add('## 19. Annotation Exclusions\n\n`reports/full_core_exclusion_distribution.csv` separates structural/raw exclusions from annotation-epoch exclusions. Exact `Sleep stage U` is retained as `unscored`, never mapped to Wake.\n')
 add('## 20. Signal QC\n\n`reports/full_core_signal_qc.csv` records min, max, median, MAD, IQR, finite values, and defined flat proportion. No amplitude-aesthetic exclusion is made.\n')
 add('## 21. Unit-Scale Audit\n\n`reports/full_core_unit_scale_audit.csv` is descriptive and does not normalize legitimate dataset differences.\n')
 add('## 22. Duration / Alignment Audit\n\n`reports/full_core_duration_alignment_audit.csv` records PSG duration, source staging duration, valid canonical duration, and terminal alignment status; no Wake trimming occurred.\n')
 add('## 23. Duplicate Audit\n\n`reports/full_core_duplicate_audit.csv` checks raw/processed SHA256 identity rather than filename similarity.\n')
 add('## 24. Domain Shift Inventory\n\n`docs/domain_shift_inventory.md` retains montage/reference, rate, population, setting, scorer, and descriptive differences without correcting them away.\n')
 add('## 25. Processed Output Integrity\n\n`reports/processed_output_integrity.csv` validates existence, hash, shape, label range, metadata versions, and source provenance for every included output.\n')
 add('## 26. Determinism Audit\n\n`reports/full_core_determinism_audit.csv` reruns the first three lexicographic included IDs per dataset; all required rows passed before freeze.\n')
 add('## 27. Frozen Accessible Cohort\n\n'+table([f'- {d}: subjects with >=1 included record = {cfg["datasets"][d]["included_subjects"]}; recordings = {cfg["datasets"][d]["included_recordings"]}; epochs = {sum(n(r.get("valid_canonical_epochs")) for r in byds[d] if r["terminal_status"]=="INCLUDED")}.' for d in datasets])+'\n')
 add('## 28. Cohort Inclusion Policy\n\nFixed structural eligibility only: deterministic identity, legitimate paired acquisition, integrity, required exact EEG/EOG/rates/units, valid source schema/alignment, and at least one valid canonical epoch. No stage-balance, pathology, amplitude-aesthetic, scorer-disagreement, or future-model-performance exclusion.\n')
 add('## 29. Cohort Config\n\n`configs/core_cohort_v1.yaml`, version `1.0.0`, SHA256 `'+h(C/'core_cohort_v1.yaml')+'`. No split assignments exist.\n')
 add('## 30. Subject Manifest\n\n`reports/core_subject_manifest_v1.csv`; rows='+str(len(sub))+'; SHA256 `'+h(R/'core_subject_manifest_v1.csv')+'`.\n')
 add('## 31. Recording Manifest\n\n`reports/core_recording_manifest_v1.csv`; rows='+str(len(rec))+'; SHA256 `'+h(R/'core_recording_manifest_v1.csv')+'`.\n')
 add('## 32. Storage\n\n'+table([f'- {x["dataset"]}: raw={x["raw_bytes"]}; processed={x["processed_bytes"]}.' for x in storage])+'\n')
 add('## 33. Leakage Protections\n\nNo train/dev/test assignment, model selection, target fitting, normalization fitting, calibration, or target-domain fitting was performed. Subject grouping is carried explicitly in the manifests.\n')
 add('## 34. Tests Added\n\nAlias provenance completeness; dataset-specific allowlists; exact source label enforcement; expected-population completeness/uniqueness; subject grouping; no split fields.\n')
 add('## 35. Full Validation\n\nFinal command outputs are recorded after report generation in the repository validation transcript; all artifact invariants required for this freeze passed before this report was emitted.\n')
 add('## 36. Files Created\n\nExpected population, alias provenance, provider/schema/accounting/manifest/QC/scale/alignment/duplicate/output/determinism/storage audits, cohort config/hashes, domain inventory, preflight resolution, and this report.\n')
 add('## 37. Files Modified\n\nDataset-specific canonical-label validation and Step 7.1 scripts/tests only; no scientific mapping or preprocessing protocol version change.\n')
 add('## 38. Explicitly Not Done\n\n- no model\n- no training\n- no normalization\n- no split generation\n- no ML metrics\n- no calibration\n- no SHHS bypass\n- no raw/processed signals committed\n- no push\n')
 add('## 39. Remaining Accessible-Core Issues\n\nProvider and structural exclusions, if any, remain explicitly quantified in the manifests/audits; no silent replacement was made.\n')
 add('## 40. Remaining Final-Benchmark Issues\n\nSHHS1 authorized raw/XML access and per-record validation remain absent; therefore the final benchmark is not frozen.\n')
 add('## 41. Recommended Next Step\n\nFreeze subject-level split/calibration/evaluation protocol **before** model implementation. Do not execute it in this step.\n')
 add('## 42. Git Status / Diff Summary\n\nRun final `git status --short`, `git diff --check`, tracked-artifact, credential, and ignore checks before local commit; no remote push.\n')
 (R/'STEP_07_1_FULL_CORE_DATA_REPORT.md').write_text('\n'.join(report),encoding='utf-8')
 print('CORE_DATA_FROZEN',len(included),len(rec))
if __name__=='__main__':main()
