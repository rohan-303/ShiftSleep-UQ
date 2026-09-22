"""Deterministic randomized APS utilities for the post-review protocol v2.

This module is scaffolding only; Step 20.1.2 does not call it on scientific
prediction bundles.
"""
from __future__ import annotations
import hashlib, math
from typing import Iterable
import numpy as np

NAMESPACE = "SHIFT_SLEEP_UQ_RAPSENS_V1"
GLOBAL_SEED = 2031

def deterministic_u(*, direction: str, model_family: str, model_seed: int,
                    split: str, subject_id: str, recording_id: str,
                    epoch_index: int, purpose: str, seed: int = GLOBAL_SEED) -> float:
    if purpose not in {"CAL_SCORE", "PRED_SET"}:
        raise ValueError("purpose must be CAL_SCORE or PRED_SET")
    fields = [NAMESPACE, str(seed), direction, model_family, str(model_seed),
              split, str(subject_id), str(recording_id), str(epoch_index), purpose]
    digest = hashlib.sha256("\x1f".join(fields).encode("utf-8")).digest()
    # First 53 bits, matching the binary64 mantissa resolution.
    integer = int.from_bytes(digest[:8], "big") >> 11
    return integer / float(1 << 53)

def stable_order(probs: np.ndarray) -> np.ndarray:
    probs = np.asarray(probs, dtype=float)
    if probs.ndim != 1:
        raise ValueError("probs must be one-dimensional")
    return np.lexsort((np.arange(probs.size), -probs))

def randomized_scores(probs, labels, u_values) -> np.ndarray:
    p = np.asarray(probs, dtype=float); y=np.asarray(labels,dtype=int); u=np.asarray(u_values,dtype=float)
    if p.ndim != 2 or y.shape != (p.shape[0],) or u.shape != y.shape: raise ValueError("shape mismatch")
    out=np.empty(len(y),float)
    for i in range(len(y)):
        order=stable_order(p[i]); rank=int(np.flatnonzero(order==y[i])[0]); out[i]=p[i,order[:rank]].sum()+u[i]*p[i,order[rank]]
    return out

def quantile_kth(scores, alpha: float) -> float:
    x=np.sort(np.asarray(scores,dtype=float)); n=len(x)
    if n==0: raise ValueError("calibration scores cannot be empty")
    k=min(max(math.ceil((n+1)*(1-alpha)),1),n)
    return float(x[k-1])

def randomized_prediction_set(probs, q_alpha: float, u_values) -> np.ndarray:
    p=np.asarray(probs,dtype=float); u=np.asarray(u_values,dtype=float)
    if p.ndim != 2 or u.shape != (p.shape[0],): raise ValueError("shape mismatch")
    out=np.zeros_like(p,dtype=bool)
    for i in range(len(p)):
        order=stable_order(p[i]);
        if q_alpha >= 1.0:
            out[i,:]=True; continue
        cum=0.0; boundary=None
        for rank, cls in enumerate(order):
            nxt=cum+p[i,cls]
            if nxt >= q_alpha:
                boundary=rank; c_prev=cum; pk=p[i,cls]; break
            out[i,cls]=True; cum=nxt
        if boundary is None: out[i,:]=True; continue
        t=float(np.clip((q_alpha-c_prev)/pk,0.0,1.0)) if pk>0 else 1.0
        if u[i] <= t: out[i,order[boundary]]=True
    return out

def summarize_sets(sets, labels) -> dict[str,float]:
    s=np.asarray(sets,dtype=bool); y=np.asarray(labels,dtype=int); sizes=s.sum(1)
    return {"coverage": float(s[np.arange(len(y)),y].mean()), "mean_set_size":float(sizes.mean()), "median_set_size":float(np.median(sizes)), "empty_fraction":float((sizes==0).mean()), **{f"size_{k}_fraction":float((sizes==k).mean()) for k in range(1,6)}}
