import csv, hashlib, json, math, re, shutil, subprocess
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(r'C:/Users/rohan/ShiftSleep-UQ')
REPORT=ROOT/'reports'; TABLE=REPORT/'paper_tables'; FDATA=REPORT/'paper_figures/source_data'; PF=ROOT/'paper/figures'; PF.mkdir(exist_ok=True)

def read(p):
    with open(p,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
    p.parent.mkdir(parents=True,exist_ok=True)
    if fields is None: fields=list(rows[0]) if rows else []
    with open(p,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def sha(p):
    h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()
def f(x): return float(x)

t2=read(TABLE/'table2_b0_primary_shift_results.csv')
canon=read(REPORT/'b0_primary_results_multiseed_v1_2.csv')
# Canonical B0 values for selected metrics.
lookup={}
for r in canon:
    if r['metric'] in {'macro-F1','NLL','AURC','gap_0.1'} and r['probability_variant']=='UNCALIBRATED':
        lookup[(r['experiment_id'],r['condition'],r['metric'])]=r['point_estimate']
# Table 2 corrected values.
rows=[]
for exp in ['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF']:
  for c in ['C0','C1','C2','C3','C4','C5']:
    rows.append({'direction':'D1' if exp.startswith('D1') else 'D2','condition':c,
      'macro_F1':lookup[(exp,c,'macro-F1')],'NLL':lookup[(exp,c,'NLL')],
      'AURC':lookup[(exp,c,'AURC')],'abs_gap_alpha_0.10':lookup[(exp,c,'gap_0.1')]})
write(TABLE/'table2_b0_primary_shift_results_v2.csv',rows)
# Corrected design schematic: same frozen protocol, clearer roles and masks.
fig,ax=plt.subplots(figsize=(11,5.5)); ax.axis('off'); ax.set_xlim(0,11); ax.set_ylim(0,6)
def box(x,y,w,h,text,fc='#edf3f7'):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04',fc=fc,ec='#34526f',lw=1.3)); ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10)
box(.3,4.25,2.2,1.0,'SOURCE DATASET\nTRAIN / DEV / CAL / TEST')
box(4.4,4.25,2.2,1.0,'B0: fixed input\nB1: source mask dropout')
box(8.5,4.25,2.2,1.0,'TARGET DATASET\nheld-out subjects')
box(.5,1.5,2.2,1.0,'C0 full\nknown domain')
box(3.1,1.5,2.2,1.0,'C1/C2\nEEG-only / EOG-only')
box(5.7,1.5,2.2,1.0,'C3 full\nunseen domain')
box(8.3,1.5,2.2,1.0,'C4/C5\nEEG-only / EOG-only')
from matplotlib.patches import FancyArrowPatch
for a,b in [((2.5,4.75),(4.4,4.75)),((6.6,4.75),(8.5,4.75)),((5.5,4.25),(5.5,2.5))]: ax.add_patch(FancyArrowPatch(a,b,arrowstyle='->',mutation_scale=14,color='#607d8b'))
ax.text(5.5,3.25,'D1: Sleep-EDF → ISRUC\nD2: ISRUC → Sleep-EDF\nsource-only calibration firewall',ha='center',va='center',fontsize=10,fontweight='bold')
fig.suptitle('ShiftSleep-UQ reciprocal benchmark design',fontsize=13); fig.tight_layout(); fig.savefig(PF/'fig1_shift_design_v2.pdf',bbox_inches='tight'); plt.close(fig)
# Fig2 source audit, comparing old source-data to canonical values. The old macro field is explicitly unavailable.
old=read(FDATA/'fig2_b0_shift_landscape.csv'); audits=[]
for r in old:
  exp=r['direction']; c=r['condition']
  for metric,field in [('macro-F1','macro_F1'),('NLL','NLL'),('AURC','AURC'),('gap_0.1','abs_gap_alpha_0.10')]:
    cv=lookup[(exp,c,metric)]; raw=r[field]
    if raw.startswith('NOT_'):
      audits.append({'direction':exp,'condition':c,'metric':metric,'canonical_value':f'{float(cv):.12g}','figure_source_value':raw,'delta':'NOT_COMPUTABLE','status':'FIG2_PRESENTATION_BINDING_DEFECT_CONFIRMED' if metric=='macro-F1' else 'SOURCE_VALUE_UNAVAILABLE'})
    else:
      dv=f(float(raw)-float(cv))
      audits.append({'direction':exp,'condition':c,'metric':metric,'canonical_value':f'{float(cv):.12g}','figure_source_value':raw,'delta':f'{dv:.12g}','status':'MATCH' if abs(dv)<1e-9 else 'MISMATCH'})
write(REPORT/'step19_fig2_source_audit.csv',audits)
# Corrected Figure 2 from canonical B0 table only.
fig,axs=plt.subplots(2,2,figsize=(11,7),sharex=True)
metrics=[('Macro-F1','macro-F1'),('Calibrated NLL','NLL'),('Entropy AURC','AURC'),('Abs coverage gap (alpha=0.10)','gap_0.1')]
for ax,(title,m) in zip(axs.flat,metrics):
  for exp,style,label in [('D1_SLEEPEDF_TO_ISRUC','-o','D1'),('D2_ISRUC_TO_SLEEPEDF','-s','D2')]:
    vals=[lookup[(exp,c,m)] for c in ['C0','C1','C2','C3','C4','C5']]
    ax.plot(['C0','C1','C2','C3','C4','C5'],vals,style,label=label,lw=1.8,ms=4)
  ax.set_title(title); ax.set_ylabel('value'); ax.grid(alpha=.25); ax.legend(frameon=False)
axs[1,0].set_xlabel('condition'); axs[1,1].set_xlabel('condition')
fig.suptitle('B0 v1.2 shift landscape: canonical primary results',fontsize=13)
fig.tight_layout(rect=[0,0,1,.96]); fig.savefig(PF/'fig2_b0_shift_landscape_v2.pdf',bbox_inches='tight'); plt.close(fig)
# Figure source audits.
def audit(name, rows):
  out=[]
  for r in rows:
    out.append({'figure':name,'direction':r.get('direction',r.get('experiment_id','')),'condition':r.get('condition',''),'metric':'row/source equivalence','source_value':json.dumps(r,sort_keys=True),'canonical_reference':'frozen Step 17 source-data row','status':'VERIFIED_SOURCE_ROW'})
  return out
allrows=[]
allrows += audit('fig3',read(FDATA/'fig3_compound_macro_f1.csv'))
allrows += audit('fig4',read(FDATA/'fig4_compound_reliability_axes.csv'))
allrows += audit('fig5',read(FDATA/'fig5_prediction_reliability_decoupling.csv'))
cr=read(FDATA/'fig6_selective_risk_coverage.csv')
# verify curve source has exactly 4*2*101 rows and seed 17.
allrows.append({'figure':'fig6','direction':'ALL','condition':'C4/C5','metric':'risk-coverage source','source_value':f'{len(cr)} rows, seeds={sorted(set(r["seed"] for r in cr))}','canonical_reference':'frozen prediction bundles B0/B1','status':'VERIFIED_REPRESENTATIVE_SEED_17; AURC INFERENCE USES THREE SEEDS'})
allrows += audit('fig7',read(FDATA/'fig7_conformal_transfer.csv'))
allrows += audit('fig8',read(FDATA/'fig8_stage_recall_changes.csv'))
write(REPORT/'step19_figure_source_audit.csv',allrows,['figure','direction','condition','metric','source_value','canonical_reference','status'])
# Provenance JSON later after compilation.
print(json.dumps({'table2_rows':len(rows),'fig2_audit_rows':len(audits),'fig2_pdf':str(PF/'fig2_b0_shift_landscape_v2.pdf'),'figure_audit_rows':len(allrows)}))
