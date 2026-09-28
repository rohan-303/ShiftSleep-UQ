from __future__ import annotations
import csv,math,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reports/remediation';classes=['Wake','N1','N2','N3','REM']
def js(p,q):
 p=np.asarray(p,float);q=np.asarray(q,float);m=(p+q)/2
 return float(.5*np.sum(np.where(p>0,p*np.log(p/m),0))+ .5*np.sum(np.where(q>0,q*np.log(q/m),0)))
def main():
 rows=list(csv.DictReader((R/'r2_windowed_dataset_manifest_v1.csv').open()))
 d={}
 for ds in ['sleep_edf_sc','isruc_s1']:
  for stage,prefix in [('BEFORE','original'),('AFTER','retained')]:
   c=np.array([sum(float(x[f'{prefix}_{k}']) for x in rows if x['dataset']==ds) for k in classes]);d[(ds,stage)]=c/c.sum()
 before=js(d[('sleep_edf_sc','BEFORE')],d[('isruc_s1','BEFORE')]);after=js(d[('sleep_edf_sc','AFTER')],d[('isruc_s1','AFTER')]);change=before-after
 out=[{'comparison':'Sleep-EDF_vs_ISRUC','stage':'BEFORE','js_natural_log':before,'sleepedf_'+k:d[('sleep_edf_sc','BEFORE')][i],'isruc_'+k:d[('isruc_s1','BEFORE')][i]} for i,k in enumerate(classes)]
 out += [{'comparison':'Sleep-EDF_vs_ISRUC','stage':'AFTER','js_natural_log':after,'absolute_change_vs_before':change,'relative_reduction_vs_before':change/before if before else None,'sleepedf_'+k:d[('sleep_edf_sc','AFTER')][i],'isruc_'+k:d[('isruc_s1','AFTER')][i]} for i,k in enumerate(classes)]
 fields=['comparison','stage','js_natural_log','absolute_change_vs_before','relative_reduction_vs_before']+[f'{x}_{k}' for x in ['sleepedf','isruc'] for k in classes]
 with (R/'r2_cross_dataset_class_prior_divergence_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
 print(json.dumps({'before_js':before,'after_js':after,'absolute_change':change,'relative_reduction':change/before},indent=2))
if __name__=='__main__':main()
