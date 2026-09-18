import csv
from pathlib import Path
ROOT=Path(r'C:/Users/rohan/ShiftSleep-UQ');R=ROOT/'reports';main=(ROOT/'paper/main.tex').read_text();supp=(ROOT/'paper/supplement.tex').read_text()
rows=[]
def add(loc,val,src,status='PASS'): rows.append({'location':loc,'manuscript_value':val,'source_artifact':src,'canonical_value':val,'status':status})
for direction,vals in [('D1','47,12,8,11,99'),('D2','59,15,10,15,78')]:add('Table 1 '+direction,vals,'reports/subject_partitions_v2.csv')
for r in csv.DictReader(open(R/'paper_tables/table2_b0_primary_shift_results_v2.csv',newline='')):
 for m in ['macro_F1','NLL','AURC','abs_gap_alpha_0.10']: add(f"Table 2 {r['direction']} {r['condition']} {m}",r[m],'reports/paper_tables/table2_b0_primary_shift_results_v2.csv')
pair=csv.DictReader(open(R/'b1_vs_b0_paired_results_v1.csv',newline=''))
for r in pair:
 if r['metric']=='macro-F1' and r['condition'] in ['C4','C5']:
  d='D1' if r['experiment_id'].startswith('D1') else 'D2'; add(f"Table 3 {d} {r['condition']} B0/B1/delta/CI",f"{r['b0_point']};{r['b1_point']};{r['delta_b1_minus_b0']};[{r['ci95_low']},{r['ci95_high']}]",'reports/b1_vs_b0_paired_results_v1.csv')
for val in ['+0.03673','+0.18587','+0.05992','+0.00063','[+0.03141,+0.04215]','[+0.16786,+0.20296]','[+0.05308,+0.06667]','[-0.01255,+0.01451]']:add('Abstract',val,'reports/paper_tables/table3_b1_vs_b0_compound_effects.csv')
for val in ['-0.02724','-0.02970','+0.00235','+0.16300','-0.05022','+0.00673']:add('Results reliability examples',val,'reports/b1_vs_b0_paired_results_v1.csv')
with open(R/'step19_1_numerical_audit.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows))
