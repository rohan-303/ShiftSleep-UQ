from __future__ import annotations
import csv,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
 rows=list(csv.DictReader((ROOT/'reports/remediation/r2_windowed_dataset_manifest_v1.csv').open()))
 out=[]
 for ds in ['sleep_edf_sc','isruc_s1']:
  for stage in ['BEFORE','AFTER']:
   a=np.zeros(5,dtype=float)
   for r in rows:
    if r['dataset']!=ds:continue
    for i,c in enumerate(['Wake','N1','N2','N3','REM']):a[i]+=float(r[f'original_{c}'] if stage=='BEFORE' else r[f'retained_{c}'])
   p=a/a.sum();out.append({'dataset':ds,'stage':stage,**{c:float(x) for c,x in zip(['Wake','N1','N2','N3','REM'],p)}})
 for ds in ['sleep_edf_sc','isruc_s1']:
  b=next(x for x in out if x['dataset']==ds and x['stage']=='BEFORE');a=next(x for x in out if x['dataset']==ds and x['stage']=='AFTER');p=np.array([b[c] for c in ['Wake','N1','N2','N3','REM']]);q=np.array([a[c] for c in ['Wake','N1','N2','N3','REM']]);m=(p+q)/2;js=.5*np.sum(np.where(p>0,p*np.log(p/m),0))+.5*np.sum(np.where(q>0,q*np.log(q/m),0));b['js_divergence_before_after']=float(js);a['js_divergence_before_after']=float(js)
 with (ROOT/'reports/remediation/r2_class_prior_before_after_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0])+['js_divergence_before_after']);w.writeheader();w.writerows(out)
 print(json.dumps(out))
if __name__=='__main__':main()
