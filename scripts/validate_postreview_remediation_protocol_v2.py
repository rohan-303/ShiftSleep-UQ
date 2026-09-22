"""Strict pre-execution validator for post-review remediation protocol v2."""
from __future__ import annotations
import hashlib, itertools, json, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
V1=ROOT/'configs/postreview_remediation_protocol_v1.yaml'; V2=ROOT/'configs/postreview_remediation_protocol_v2.yaml'
EXPECTED_V1='9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,msg,errors):
    if not c: errors.append(msg)
def validate():
    e=[]
    require(sha(V1)==EXPECTED_V1,'v1 hash drift',e)
    d=yaml.safe_load(V2.read_text())
    require(d.get('status')=='EXECUTABLE_REMEDIATION_PROTOCOL_V2_FROZEN','wrong gate',e)
    require(d.get('scientific_questions_unchanged') is True,'scientific scope not frozen',e)
    r1=d['r1']; require(r1['id']=='RANDOMIZED_APS','R1 method unresolved',e); require(r1['alphas']==[0.10,0.05],'R1 alphas',e)
    require(r1['probability_stream']['name']=='UNCALIBRATED_SOFTMAX','APS stream',e)
    require(r1['randomization']['global_seed']==2031 and len(r1['randomization']['key_fields'])==10,'R1 randomizer',e)
    require(set(r1['conditions'])==set(['C0','C1','C2','C3','C4','C5']),'R1 conditions',e)
    r2=d['r2']; require(r2['window']['left_context_epoch_positions']==60 and r2['window']['right_context_epoch_positions']==60,'R2 physical context',e)
    require(r2['window']['select_physical_indices_before_validity_filter'] is True,'R2 physical selection',e)
    require(r2['training']['optimizer']=='AdamW' and r2['training']['learning_rate']==0.0003,'R2 training',e)
    require(r2['training']['batch_size_physical']==128 and r2['training']['max_epochs']==30 and r2['training']['patience']==6,'R2 limits',e)
    require(r2['checkpoint_selection']['population']=='SOURCE_DEV','R2 checkpoint population',e)
    require(r2['normalization']['fit_scope']=='WINDOWED_SOURCE_TRAIN_ONLY','R2 normalization firewall',e)
    r3=d['r3']; require(r3['model_id'] if 'model_id' in r3 else r3['id']=='SEQSLEEPNET_CLASS_L20_V1','R3 model id',e)
    for key in ['input','spectrogram','filterbank','epoch_encoder','sequence_encoder','sequences','exposure','training','checkpoint_selection','fallback']: require(key in r3,'R3 missing '+key,e)
    require(r3['sequence_encoder']['length']==20 and r3['training']['epochs']==10,'R3 sequence/training',e)
    require(r3['fallback']['if_batch8_oom']=='R3_HARDWARE_BLOCKED','R3 fallback',e)
    st=d['statistics']; require(st['replicates']==2000 and st['bootstrap_seed']==2028,'bootstrap',e)
    require(st['holm']['family_r2']!=st['holm']['family_r3'],'Holm families mixed',e)
    ac=d['artifact_contract']; require(len(ac['namespaces'])==3 and len(ac['promotion_requires'])>=6,'artifact contract',e)
    fw=d['firewall']; require(all(fw.get(k) is True for k in ['source_cal_only','target_normalization_forbidden','target_checkpoint_selection_forbidden','target_hyperparameter_selection_forbidden']),'target firewall',e)
    return d,e

def main():
    d,e=validate()
    if e: print(json.dumps({'valid':False,'errors':e},indent=2)); return 1
    print(json.dumps({'valid':True,'protocol':str(V2),'v1_sha256':sha(V1),'v2_sha256':sha(V2)},indent=2)); return 0
if __name__=='__main__': sys.exit(main())
