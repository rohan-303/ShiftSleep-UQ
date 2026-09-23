from __future__ import annotations
import csv,json,hashlib
from pathlib import Path
import numpy as np
from shiftsleep_uq.evaluation_step11 import softmax,macro_f1
ROOT=Path(__file__).resolve().parents[1];EXPS=['D1_SLEEPEDF_TO_ISRUC','D2_ISRUC_TO_SLEEPEDF'];SEEDS=[17,42,2026]
def load(e,v,s,c):
 p=ROOT/'artifacts/remediation/r2'/f'R2_{e}_{v}_SEED_{s}'/'ATTEMPT_001'/'predictions'/f'{c}.npz'
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def boot(a,b,reps=2000):
 subs=np.asarray(sorted(set(a['subject_id'].tolist())&set(b['subject_id'].tolist())));ca=[];cb=[]
 for s in subs:
  ia=np.flatnonzero(a['subject_id']==s);ib=np.flatnonzero(b['subject_id']==s);ca.append(np.bincount(a['labels'][ia]*5+softmax(a['logits'][ia]).argmax(1),minlength=25).reshape(5,5));cb.append(np.bincount(b['labels'][ib]*5+softmax(b['logits'][ib]).argmax(1),minlength=25).reshape(5,5))
 ca=np.asarray(ca);cb=np.asarray(cb);rng=np.random.default_rng(2028);v=np.empty(reps)
 def mf(cm):
  tp=np.diag(cm);prec=tp/np.maximum(cm.sum(0),1);rec=tp/np.maximum(cm.sum(1),1);return float(np.mean(2*prec*rec/np.maximum(prec+rec,1e-12)))
 for r in range(reps):
  pick=rng.choice(len(subs),len(subs),replace=True);v[r]=mf(cb[pick].sum(0))-mf(ca[pick].sum(0))
 return v

def main():
 effects=[];summary=[]
 for e in EXPS:
  for c in ['C4','C5']:
   vals=[];bs=[]
   for s in SEEDS:
    a=load(e,'B0_W',s,c);b=load(e,'B1_W',s,c);vals.append(macro_f1(softmax(b['logits']).argmax(1),b['labels'])-macro_f1(softmax(a['logits']).argmax(1),a['labels']));bs.append(boot(a,b))
   hat=float(np.mean(vals));v=np.mean(np.stack(bs),axis=0);p=float((1+np.sum(np.abs(v-hat)>=abs(hat)))/2001);effects.append({'experiment':e,'condition':c,'effect_B1W_minus_B0W':hat,'ci_low':float(np.quantile(v,.025)),'ci_high':float(np.quantile(v,.975)),'p_unadjusted':p,'seed_effects':json.dumps([float(x) for x in vals]),'bootstrap_replicates':2000,'bootstrap_seed':2028})
 # standard step-down Holm
 order=sorted(range(4),key=lambda i:effects[i]['p_unadjusted']);running=0.0
 for rank,i in enumerate(order):running=max(running,min(1.,(4-rank)*effects[i]['p_unadjusted']));effects[i]['holm_adjusted_p']=running;effects[i]['holm_reject']=running<.05
 for name in ['r2_paired_results_v1.csv','r2_holm_v1.csv']:
  with (ROOT/'reports/remediation'/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(effects[0]));w.writeheader();w.writerows(effects)
 with (ROOT/'reports/remediation/r2_bootstrap_summary_v1.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['experiment','condition','effect','ci_low','ci_high','replicates','seed']);w.writeheader();w.writerows({'experiment':x['experiment'],'condition':x['condition'],'effect':x['effect_B1W_minus_B0W'],'ci_low':x['ci_low'],'ci_high':x['ci_high'],'replicates':2000,'seed':2028} for x in effects)
 print(json.dumps(effects,indent=2))
if __name__=='__main__':main()
