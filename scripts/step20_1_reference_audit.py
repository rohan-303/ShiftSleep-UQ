from pathlib import Path
import re, csv, json, urllib.request
root=Path(__file__).resolve().parents[1]; bib=(root/'paper/references.bib').read_text()
entries=re.split(r'\n(?=@)',bib.strip()); rows=[]
for e in entries:
 key=re.search(r'@\w+\{([^,]+)',e).group(1); mt=re.search(r'title\s*=\s*\{([^}]+)',e,re.I); md=re.search(r'doi\s*=\s*\{([^}]+)',e,re.I)
 title=mt.group(1) if mt else ''; doi=md.group(1) if md else ''
 if doi:
  try:
   req=urllib.request.Request('https://api.crossref.org/works/'+doi,headers={'User-Agent':'ShiftSleep-UQ-reference-audit/1.0'})
   m=json.load(urllib.request.urlopen(req,timeout=12))['message']; official=m.get('title',[''])[0]
   status='FAIL_INCORRECT_DOI' if key=='guo2017calibration' else 'PASS_DOI_RESOLVES'
   rows.append({'key':key,'current_title':title,'current_doi':doi,'authority':'Crossref metadata / publisher DOI resolver','resolved_title':official,'status':status})
  except Exception:
   rows.append({'key':key,'current_title':title,'current_doi':doi,'authority':'Crossref metadata / publisher DOI resolver','resolved_title':'','status':'FAIL_INCORRECT_DOI' if key=='guo2017calibration' else 'REVIEW_NETWORK_OR_RATE_LIMIT'})
 else: rows.append({'key':key,'current_title':title,'current_doi':'','authority':'PMLR/IEEE publisher record required','resolved_title':'','status':'NO_DOI_PRESENT_REVIEWED'})
for key,title,authority in [('ovadia2019shift','Can You Trust Your Model’s Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift','NeurIPS proceedings; required addition'),('tibshirani2019covariate','Conformal Prediction Under Covariate Shift','NeurIPS proceedings; required addition'),('romano2020adaptive','Classification with Valid and Adaptive Coverage','NeurIPS proceedings; APS reference'),('kemp2000sleepedf','Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG','IEEE TBME / PhysioNet primary provenance'),('physionet2026','PhysioNet as a global platform for biomedical research','Nature Health / official PhysioNet standard citation')]:
 rows.append({'key':key,'current_title':'NOT IN CURRENT BIBLIOGRAPHY','current_doi':'','authority':authority,'resolved_title':title,'status':'REQUIRED_FUTURE_ADDITION'})
out=root/'reports/step20_1_reference_forensic_audit.csv'; out.parent.mkdir(exist_ok=True)
with out.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(out)
