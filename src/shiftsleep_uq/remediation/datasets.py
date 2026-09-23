"""Protocol-scoped remediation data overlay; historical files are read-only."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import numpy as np
import torch
from torch.utils.data import Dataset
from shiftsleep_uq.training.datasets import ManifestEpochDataset, source_dataset_for_experiment
from shiftsleep_uq.training.normalization import apply_normalization
ROOT=Path(__file__).resolve().parents[3]
REPAIRED=ROOT/'artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2'

def overlay_path(path: Path, dataset: str) -> Path:
    if dataset != 'sleep_edf_sc': return path
    candidate=REPAIRED/path.name
    if not candidate.exists(): raise FileNotFoundError(f'repaired ledger missing: {candidate}')
    return candidate

class RemediationManifestDataset(ManifestEpochDataset):
    def _load_recording(self,path: Path,subject: str,recording: str):
        key=(self.dataset,self.role,self.purpose,subject,recording,str(path));self._accessed.add(key)
        if path not in self._cache:
            with np.load(path,allow_pickle=False) as z:
                self._cache[path]={'eeg':z['eeg'],'eog':z['eog'],'labels':z['labels'],'source_epoch_indices':z['source_epoch_indices']}
        return self._cache[path]
    def __getitem__(self,index: int) -> dict[str,Any]:
        path,row_index,subject,recording_id,montage=self.records[index];a=self._load_recording(path,subject,recording_id)
        label=int(a['labels'][row_index]);physical=int(a['source_epoch_indices'][row_index])
        eeg=np.asarray(a['eeg'][row_index],dtype=np.float32);eog=np.asarray(a['eog'][row_index],dtype=np.float32)
        if self.normalization is not None:
            eeg=apply_normalization(eeg,self.normalization['EEG']);eog=apply_normalization(eog,self.normalization['EOG'])
        return {'eeg':torch.from_numpy(eeg).unsqueeze(0),'eog':torch.from_numpy(eog).unsqueeze(0),'label':torch.tensor(label,dtype=torch.long),'dataset':self.dataset,'subject_id':subject,'recording_id':recording_id,'epoch_index':torch.tensor(physical,dtype=torch.long),'row_index':torch.tensor(row_index,dtype=torch.long),'montage_variant':montage,'source_role':self.role}

def _new(dataset,role,purpose): return RemediationManifestDataset(dataset,role,purpose,root=ROOT)
def _overlay_records(ds): ds.records=[(overlay_path(p,ds.dataset),i,s,r,m) for p,i,s,r,m in ds.records];return ds

def _apply_physical_windows(ds):
    grouped={}
    for rec in ds.records: grouped.setdefault(rec[0],[]).append(rec)
    selected=[]
    for path,records in grouped.items():
        with np.load(path,allow_pickle=False) as z: labels=z['labels'].astype(int);indices=z['source_epoch_indices'].astype(int)
        if len(labels)!=len(records) or not np.array_equal(np.asarray([r[1] for r in records]),np.arange(len(labels))): raise ValueError(f'overlay record mismatch: {path}')
        nw=np.flatnonzero(labels!=0)
        if len(nw)==0: continue
        lo=max(0,int(indices[nw[0]])-60);hi=min(int(indices[-1]),int(indices[nw[-1]])+60)
        selected.extend(r for r in records if lo<=int(indices[r[1]])<=hi)
    ds.records=selected
    if not ds.records: raise ValueError(f'empty windowed dataset: {ds.dataset}/{ds.role}')
    return ds

def build_overlay_dataset(experiment: str, role: str, purpose: str, *, windowed: bool):
    ds=_overlay_records(_new(source_dataset_for_experiment(experiment),role,purpose))
    return _apply_physical_windows(ds) if windowed else ds

def build_overlay_evaluation_dataset(experiment: str, population: str, *, windowed: bool=True):
    if population=='SOURCE_TEST': dataset,role,purpose=source_dataset_for_experiment(experiment),'TEST','evaluation_test'
    elif population=='COMPLETE_TARGET': dataset,role,purpose=('isruc_s1' if experiment=='D1_SLEEPEDF_TO_ISRUC' else 'sleep_edf_sc'),'COMPLETE_TARGET','evaluation_target'
    else: raise ValueError(population)
    ds=_overlay_records(_new(dataset,role,purpose))
    return _apply_physical_windows(ds) if windowed else ds

def sample_arrays(ds):
    for path,idx,subject,recording,montage in ds.records:
        a=ds._load_recording(path,subject,recording);yield a['eeg'][idx],a['eog'][idx],int(a['labels'][idx]),subject,recording,idx

def fit_windowed_normalization(ds):
    if ds.role!='TRAIN': raise ValueError('normalization requires SOURCE TRAIN')
    sums={'EEG':0.0,'EOG':0.0};sq={'EEG':0.0,'EOG':0.0};counts={'EEG':0,'EOG':0}
    for eeg,eog,*_ in sample_arrays(ds):
        for key,x in [('EEG',eeg),('EOG',eog)]:
            x=np.asarray(x,dtype=np.float64)
            if not np.isfinite(x).all(): raise ValueError('nonfinite normalization input')
            sums[key]+=float(x.sum());sq[key]+=float(np.square(x).sum());counts[key]+=x.size
    out={}
    for key in ('EEG','EOG'):
        mean=sums[key]/counts[key];std=max(float(np.sqrt(max(sq[key]/counts[key]-mean*mean,0.0))),1e-8)
        out[key]={'mean':mean,'std':std,'std_epsilon':1e-8,'count':counts[key]}
    return out

def set_normalization(ds,normalization): ds.set_normalization(normalization);return ds
