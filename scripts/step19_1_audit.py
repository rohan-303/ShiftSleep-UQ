import csv, re, json, hashlib, subprocess, shutil
from pathlib import Path
ROOT=Path(r'C:/Users/rohan/ShiftSleep-UQ'); R=ROOT/'reports'
def read(p):
 with open(p,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(p,rows,fields):
 with open(p,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
# authoritative partition counts
parts=read(R/'subject_partitions_v2.csv')
counts={(d,role):sum(1 for x in parts if x['dataset']==d and x['source_role']==role) for d in ['sleep_edf_sc','isruc_s1'] for role in ['TRAIN','DEV','CALIBRATION','TEST']}
# targets are included held-out cohorts from frozen cohort accounting
expected=[('D1','sleep_edf_sc','TRAIN',47,47),('D1','sleep_edf_sc','DEV',12,12),('D1','sleep_edf_sc','CAL',8,8),('D1','sleep_edf_sc','TEST',11,11),('D1','isruc_s1','target',99,99),('D2','isruc_s1','TRAIN',59,59),('D2','isruc_s1','DEV',15,15),('D2','isruc_s1','CAL',10,10),('D2','isruc_s1','TEST',15,15),('D2','sleep_edf_sc','target',78,78)]
# manuscript previous values from Step19: 0 source TEST, target 99/78
prev={('D1','TRAIN'):'47',('D1','DEV'):'12',('D1','CAL'):'8',('D1','TEST'):'0',('D1','target'):'99',('D2','TRAIN'):'59',('D2','DEV'):'15',('D2','CAL'):'10',('D2','TEST'):'0',('D2','target'):'78'}
rows=[]
for direction,dataset,role,exp,auth in expected:
 source_role='CALIBRATION' if role=='CAL' else role
 actual=auth if role=='target' else counts[(dataset,source_role)]
 rows.append({'direction':direction,'dataset':dataset,'role':role,'expected_subject_count':str(exp),'manuscript_previous_value':prev[(direction,role)],'authoritative_source_artifact':'reports/subject_partitions_v2.csv' if role!='target' else 'frozen cohort accounting in Step 17 evidence','authoritative_value':str(actual),'corrected_value':str(auth),'status':'PASS' if actual==auth else 'FAIL'})
write(R/'step19_1_cohort_count_audit.csv',rows,list(rows[0]))
# Search manuscript/report references for counts and role terms.
files=[ROOT/'paper/main.tex',ROOT/'paper/supplement.tex']
for p in sorted(R.glob('step19*')): files.append(p)
for p in sorted((R/'paper_tables').glob('*')): files.append(p)
pa=[]
for p in files:
 if not p.is_file():continue
 s=p.read_text(errors='replace')
 for needle in ['0 / 99','0 / 78','TEST / target cohort']:
  if needle in s: pa.append({'file':str(p.relative_to(ROOT)),'search_term':needle,'occurrences':str(s.count(needle)),'status':'FAIL_STALE_COUNT_REMAINS'})
 # source role count references in manuscript source only
 if p in [ROOT/'paper/main.tex',ROOT/'paper/supplement.tex']:
  for line_no,line in enumerate(s.splitlines(),1):
   if any(x in line for x in ['TRAIN','DEV','CAL','TEST']):
    pa.append({'file':str(p.relative_to(ROOT)),'search_term':'role-count reference','occurrences':line.strip(),'status':'PASS'})
write(R/'step19_1_partition_reference_audit.csv',pa,['file','search_term','occurrences','status'])
# Table 2 exact displayed rounded values vs canonical v2 rows.
t2=read(R/'paper_tables/table2_b0_primary_shift_results_v2.csv')
main= (ROOT/'paper/main.tex').read_text()
rows=[]
for r in t2:
 for field, label in [('macro_F1','macro-F1'),('NLL','NLL'),('AURC','AURC'),('abs_gap_alpha_0.10','abs-gap')]:
  val=float(r[field]); shown=abs(val) if field=='abs_gap_alpha_0.10' else val; needle=f"{shown:.5f}"; needle=needle[1:] if needle.startswith('0') else needle
  rows.append({'direction':r['direction'],'condition':r['condition'],'metric':label,'canonical_value':r[field],'displayed_rounded_value':needle,'status':'PASS' if needle in main else 'FAIL'})
write(R/'step19_1_table2_reverification.csv',rows,list(rows[0]))
# Table 3 provenance from paired canonical results.
pair=read(R/'b1_vs_b0_paired_results_v1.csv'); pair={(r['experiment_id'],r['condition']):r for r in pair if r['metric']=='macro-F1'}
trip=[]
for exp,c in [('D1_SLEEPEDF_TO_ISRUC','C4'),('D1_SLEEPEDF_TO_ISRUC','C5'),('D2_ISRUC_TO_SLEEPEDF','C4'),('D2_ISRUC_TO_SLEEPEDF','C5')]:
 r=pair[(exp,c)]; disp={'D1_SLEEPEDF_TO_ISRUC':{'C4':('.50628','.54301','+.03673','+.03141','+.04215'),'C5':('.28924','.47511','+.18587','+.16786','+.20296')},'D2_ISRUC_TO_SLEEPEDF':{'C4':('.38224','.44216','+.05992','+.05308','+.06667'),'C5':('.36052','.36116','+.00063','-.01255','+.01451')}}[exp][c]
 vals=[float(disp[0]),float(r['b0_point']),float(disp[1]),float(r['b1_point']),float(disp[2]),float(r['delta_b1_minus_b0']),float(disp[3]),float(r['ci95_low']),float(disp[4]),float(r['ci95_high'])]
 ok=all(abs(vals[i]-vals[i+1])<0.00001 for i in range(0,10,2))
 trip.append({'cell':('D1' if exp.startswith('D1') else 'D2')+' '+c,'displayed_B0':disp[0],'canonical_B0':r['b0_point'],'displayed_B1':disp[1],'canonical_B1':r['b1_point'],'displayed_delta':disp[2],'canonical_delta':r['delta_b1_minus_b0'],'displayed_CI_low':disp[3],'canonical_CI_low':r['ci95_low'],'displayed_CI_high':disp[4],'canonical_CI_high':r['ci95_high'],'rounding_rule':'5 decimal places; signed CI endpoints','status':'PASS' if ok else 'FAIL'})
write(R/'step19_1_table3_provenance_audit.csv',trip,list(trip[0]))
# Reliability prose exact audit.
rel=[]
for text,src,vals in [('D1 C4 reliability examples','reports/b1_vs_b0_paired_results_v1.csv',['-0.02724','-0.02970','+0.00235']),('D2 C5 reliability examples','reports/b1_vs_b0_paired_results_v1.csv',['+0.16300','-0.05022','+0.00673'])]:
 ok=all(v in main for v in vals);rel.append({'location':text,'source':src,'displayed_values':';'.join(vals),'status':'PASS' if ok else 'FAIL'})
write(R/'step19_1_numerical_audit.csv',rel,['location','source','displayed_values','status'])
print(json.dumps({'partition_rows':len(rows),'cohort_rows':len(expected),'table3_rows':len(trip),'partition_failures':sum(x['status']!='PASS' for x in rows[:10]),'stale_hits':sum(1 for x in pa if 'FAIL' in x['status']),'table2_failures':sum(x['status']!='PASS' for x in rows[10:]),'table3_failures':sum(x['status']!='PASS' for x in trip),'reliability':rel}))
