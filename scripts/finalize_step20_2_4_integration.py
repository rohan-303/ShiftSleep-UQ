from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reports/remediation'
# R2 effects are authoritative; R3 is explicitly missing, not zero-filled.
r2=list(csv.DictReader((R/'r2_paired_results_v1.csv').open()));out=[]
for x in r2:out.append({'experiment':x['experiment'],'condition':x['condition'],'historical_B1_minus_B0':'NOT_RECONSTRUCTED_IN_STEP_20_2_4','r2_B1W_minus_B0W':x['effect_B1W_minus_B0W'],'r2_ci':f"[{x['ci_low']},{x['ci_high']}]",'r2_holm_adjusted_p':x['holm_adjusted_p'],'r2_seed_effects':x['seed_effects'],'r3_S1_minus_S0':'NOT_COMPUTED','r3_ci':'NOT_COMPUTED','r3_holm_adjusted_p':'NOT_COMPUTED'})
with (R/'remediation_primary_effect_summary_final.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
# Final reliability matrix is a status matrix, not a fabricated scalar.
rel=[]
for x in r2:rel.append({'experiment':x['experiment'],'condition':x['condition'],'family':'R2','predictive':'MEASURED','NLL':'MEASURED_IN_r2_reliability_results_v1','AURC':'MEASURED_IN_r2_reliability_results_v1','ranking':'MEASURED_IN_r2_reliability_results_v1','randomized_APS':'MEASURED_IN_r2_reliability_results_v1','status':'PARTIAL_BOOTSTRAP_COVERAGE'})
for x in r2:rel.append({'experiment':x['experiment'],'condition':x['condition'],'family':'R3','predictive':'NOT_COMPUTED','NLL':'NOT_COMPUTED','AURC':'NOT_COMPUTED','ranking':'NOT_COMPUTED','randomized_APS':'NOT_COMPUTED','status':'INCONCLUSIVE'})
with (R/'remediation_reliability_summary_final.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rel[0]));w.writeheader();w.writerows(rel)
con=[
 ('modality-exposure predictive effect','SUPPORTED','R2 three of four cells Holm-supported'),
 ('sleep-window robustness','PARTIALLY_SUPPORTED','R2 D2/C5 crosses zero'),
 ('strong-backbone generalization','INCONCLUSIVE','R3 scientific run did not complete'),
 ('probability calibration','PARTIALLY_SUPPORTED','R2 source-CAL temperature groups complete; full paired reliability bootstrap incomplete'),
 ('error ranking','PARTIALLY_SUPPORTED','R2 metrics generated; complete inferential reliability package incomplete'),
 ('selective prediction','PARTIALLY_SUPPORTED','R2 AURC/risk-coverage generated descriptively; paired bootstrap incomplete'),
 ('conformal transfer','NOT_SUPPORTED','R1 materially changes historical finding')]
with (R/'remediation_conclusion_matrix_final.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['question','status','evidence']);w.writeheader();w.writerows({'question':a,'status':b,'evidence':c} for a,b,c in con)
print(json.dumps({'effect_rows':len(out),'reliability_rows':len(rel),'conclusion_rows':len(con)}))
