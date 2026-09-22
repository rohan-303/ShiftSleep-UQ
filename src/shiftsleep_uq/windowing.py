"""Physical-index harmonized sleep-window construction (synthetic-testable)."""
from __future__ import annotations
import numpy as np

def harmonized_window_indices(labels, valid_mask=None, wake_label=0, context_epochs=60):
    y=np.asarray(labels); valid=np.ones(len(y),dtype=bool) if valid_mask is None else np.asarray(valid_mask,dtype=bool)
    if valid.shape != y.shape: raise ValueError("valid_mask shape mismatch")
    nonwake=np.flatnonzero(valid & (y != wake_label))
    if len(nonwake)==0: return np.array([],dtype=int)
    lo=max(0,int(nonwake[0])-context_epochs); hi=min(len(y)-1,int(nonwake[-1])+context_epochs)
    return np.arange(lo,hi+1,dtype=int)

def apply_historical_validity(indices, valid_mask):
    valid=np.asarray(valid_mask,dtype=bool); idx=np.asarray(indices,dtype=int)
    return idx[valid[idx]]
