"""Merge completed Step 7.1 provider-audit shards only if identity accounting is exact."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; REPORTS=ROOT/'reports'
FIELDS=["dataset","subject_id","recording_id","provider_url","http_status","provider_content_length","local_bytes","edf_declared_bytes","byte_delta","checksum_status","header_valid","body_valid","terminal_status","failure_code"]

def main():
 expected=list(csv.DictReader((REPORTS/'core_expected_population.csv').open(encoding='utf-8',newline='')))
 parts=sorted(REPORTS.glob('provider_integrity_audit.part-*-of-08.csv'))
 if len(parts)!=8: raise RuntimeError(f'need exactly eight completed shard audits, found {len(parts)}')
 rows=[]
 for p in parts: rows.extend(csv.DictReader(p.open(encoding='utf-8',newline='')))
 for row in rows:
  if row['terminal_status'] != 'ACQUIRED' and not row['failure_code']:
   row['failure_code'] = 'EDF_DECLARED_BYTE_MISMATCH' if row['body_valid'] == 'FAIL' else 'UNSPECIFIED_PROVIDER_INTEGRITY'
 keys={(r['dataset'],r['recording_id']) for r in rows}; expected_keys={(r['dataset'],r['recording_id']) for r in expected}
 if len(rows)!=len(expected) or keys!=expected_keys: raise RuntimeError('provider shard identity accounting failed')
 with (REPORTS/'provider_integrity_audit.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(sorted(rows,key=lambda r:(r['dataset'],r['recording_id'])))
 print({'expected':len(expected),'rows':len(rows),'acquired':sum(r['terminal_status']=='ACQUIRED' for r in rows),'excluded':sum(r['terminal_status']!='ACQUIRED' for r in rows)})
if __name__=='__main__': main()
