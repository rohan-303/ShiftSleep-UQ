from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reports/remediation'
rows=list(csv.DictReader((R/'r2_reliability_results_v1.csv').open()))
# Compare the already computed complete-bundle rows; reliability-bootstrap intervals
# are intentionally not fabricated when the metric is non-additive.
metrics=['NLL','ERROR_AUROC','ERROR_AUPRC','AURC','APS_empirical_coverage_alpha_0.10','APS_mean_set_size_alpha_0.10','APS_empirical_coverage_alpha_0.05','APS_mean_set_size_alpha_0.05']
out=[]
for e in ['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']:
 for c in ['C4','C5']:
  for metric in metrics:
   vals=[]
   for s in ['17','42','2026']:
    a=[x for x in rows if x['experiment']==e and x['condition']==c and x['seed']==s and x['variant']=='B0_W' and x['metric']==metric]
    b=[x for x in rows if x['experiment']==e and x['condition']==c and x['seed']==s and x['variant']=='B1_W' and x['metric']==metric]
    if a and b:vals.append(float(b[0]['value'])-float(a[0]['value']))
   if vals:out.append({'experiment':e,'condition':c,'metric':metric,'effect_B1W_minus_B0W':sum(vals)/len(vals),'seed_effects':';'.join(map(str,vals)),'bootstrap_status':'NOT_COMPUTED_FOR_THIS_METRIC','interpretation':'DESCRIPTIVE_ONLY'})
with (R/'r2_reliability_paired_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print({'rows':len(out)})
