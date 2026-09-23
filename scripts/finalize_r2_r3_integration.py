from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reports/remediation'
rows=list(csv.DictReader((R/'r2_primary_results_v1.csv').open()))
# Compact source-only calibration ledger from the 12 model-condition rows.
cal=[]
for r in rows:
 if r['condition']=='C0': cal.append({k:r[k] for k in ['experiment','variant','seed','temperature','aps_q_0.10','aps_q_0.05']})
with (R/'r2_calibration_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(cal[0]));w.writeheader();w.writerows(cal)
paired=list(csv.DictReader((R/'r2_paired_results_v1.csv').open()))
seed=[]
for x in paired:
 for i,v in enumerate(json.loads(x['seed_effects']),17):seed.append({'experiment':x['experiment'],'condition':x['condition'],'seed':v if False else [17,42,2026][i-17],'effect_B1W_minus_B0W':v})
with (R/'r2_seed_results_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(seed[0]));w.writeheader();w.writerows(seed)
# Integrated matrices are explicit about unavailable R3 quantities.
effects=[]
for x in paired:
 effects.append({'experiment':x['experiment'],'condition':x['condition'],'historical_effect':'NOT_RECONSTRUCTED_IN_THIS_STEP','r2_effect':x['effect_B1W_minus_B0W'],'r2_ci':f"[{x['ci_low']},{x['ci_high']}]",'r2_holm_p':x['holm_adjusted_p'],'r3_effect':'NOT_COMPUTED','r3_ci':'NOT_COMPUTED','r3_holm_p':'NOT_COMPUTED'})
for name in ['remediation_primary_effect_summary_v2.csv']:
 with (R/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(effects[0]));w.writeheader();w.writerows(effects)
rel=[]
for x in paired:
 rel.append({'experiment':x['experiment'],'condition':x['condition'],'family':'R2','NLL_effect':'AVAILABLE_IN_r2_primary_results_v1.csv','AURC_effect':'NOT_COMPUTED','conformal_coverage':'NOT_COMPUTED','conformal_set_size':'NOT_COMPUTED','interpretation':'R2 primary macro-F1 effect available; reliability extensions incomplete'})
for e in ['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']:
 for c in ['C4','C5']:rel.append({'experiment':e,'condition':c,'family':'R3','NLL_effect':'NOT_COMPUTED','AURC_effect':'NOT_COMPUTED','conformal_coverage':'NOT_COMPUTED','conformal_set_size':'NOT_COMPUTED','interpretation':'R3 scientific execution blocked'})
with (R/'remediation_reliability_summary_v2.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rel[0]));w.writeheader();w.writerows(rel)
con=[
 {'question':'modality-dropout predictive effect','status':'SUPPORTED','evidence':'R2: 3/4 Holm-adjusted primary cells positive; one inconclusive'},
 {'question':'recording-window robustness','status':'PARTIALLY_SUPPORTED','evidence':'R2 completed; D2 C5 CI crosses zero'},
 {'question':'backbone generalization','status':'INCONCLUSIVE','evidence':'R3 scientific jobs not executed'},
 {'question':'calibration','status':'INCONCLUSIVE','evidence':'SOURCE CAL temperature/APS ledger generated; full reliability matrix incomplete'},
 {'question':'selective prediction','status':'INCONCLUSIVE','evidence':'not computed in this partial integration'},
 {'question':'conformal transfer','status':'NOT_SUPPORTED','evidence':'R1 materially changes historical conformal finding'}]
with (R/'remediation_conclusion_matrix_v2.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(con[0]));w.writeheader();w.writerows(con)
print(json.dumps({'calibration_rows':len(cal),'seed_rows':len(seed),'effects':len(effects),'reliability_rows':len(rel),'conclusion_rows':len(con)}))
