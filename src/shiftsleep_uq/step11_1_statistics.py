"""Independent Step 11.1 statistics QA primitives.

This module deliberately reconstructs epoch observations from sampled subject
clusters. It does not read raw PSG data, run models, or fit calibration.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np

from .evaluation_step11 import (
    _rank_auc,
    auprc,
    aurc,
    brier,
    conformal_metrics,
    entropy,
    macro_f1,
    nll,
    softmax,
)


METRICS = ("macro-F1", "NLL", "Brier", "ERROR_AUROC", "ERROR_AUPRC", "AURC")


def bootstrap_subject_draws(subject_count: int, *, reps: int, seed: int) -> np.ndarray:
    if subject_count < 1 or reps < 1:
        raise ValueError("subject_count and reps must be positive")
    return np.random.default_rng(seed).integers(0, subject_count, size=(reps, subject_count))


def reconstruct_cluster_indices(subject_ids: np.ndarray, sampled_subject_indices: np.ndarray, subjects: Iterable[str] | None = None) -> np.ndarray:
    ids = np.asarray(subject_ids)
    unique = list(subjects) if subjects is not None else sorted(set(ids.tolist()))
    clusters = [np.flatnonzero(ids == unique[int(i)]) for i in sampled_subject_indices]
    if not clusters:
        return np.empty(0, dtype=np.int64)
    return np.concatenate(clusters).astype(np.int64, copy=False)


def _metric(bundle: dict[str, np.ndarray], metric: str, qhat: float | None = None, alpha: float | None = None) -> float:
    probs = softmax(bundle["logits"])
    labels = np.asarray(bundle["labels"], dtype=np.int64)
    predictions = probs.argmax(1)
    uncertainty = entropy(probs)
    errors = (predictions != labels).astype(int)
    if metric == "macro-F1":
        return macro_f1(predictions, labels)
    if metric == "NLL":
        return nll(probs, labels)
    if metric == "Brier":
        return brier(probs, labels)
    if metric == "ERROR_AUROC":
        return _rank_auc(uncertainty, errors)
    if metric == "ERROR_AUPRC":
        return auprc(uncertainty, errors)
    if metric == "AURC":
        return aurc(uncertainty, predictions, labels)
    if metric.startswith("coverage_") or metric.startswith("gap_"):
        if qhat is None or alpha is None:
            raise ValueError("conformal metrics require qhat and alpha")
        name = "empirical_coverage" if metric.startswith("coverage_") else "coverage_gap"
        return conformal_metrics(probs, labels, qhat, alpha)[name]
    raise ValueError(metric)


def _slice_bundle(bundle: dict[str, np.ndarray], idx: np.ndarray) -> dict[str, np.ndarray]:
    return {k: np.asarray(v)[idx] if isinstance(v, np.ndarray) and len(v) == len(bundle["labels"]) else v for k, v in bundle.items()}


def identity_metric_from_bundle(bundle: dict[str, np.ndarray], metric: str, *, identity: bool = False, qhat: float | None = None, alpha: float | None = None) -> float:
    if identity:
        subjects = sorted(set(np.asarray(bundle["subject_id"]).tolist()))
        idx = reconstruct_cluster_indices(bundle["subject_id"], np.arange(len(subjects)), subjects)
        bundle = _slice_bundle(bundle, idx)
    return _metric(bundle, metric, qhat, alpha)


def bootstrap_metric_from_bundles(
    bundles: list[dict[str, np.ndarray]],
    metric: str,
    *,
    reps: int = 2000,
    seed: int = 2028,
    qhats: list[float] | None = None,
    alpha: float | None = None,
    draws: np.ndarray | None = None,
) -> np.ndarray:
    subjects = sorted(set(np.asarray(bundles[0]["subject_id"]).tolist()))
    if any(sorted(set(np.asarray(b["subject_id"]).tolist())) != subjects for b in bundles):
        raise ValueError("bundles do not share the same subject set")
    draws = bootstrap_subject_draws(len(subjects), reps=reps, seed=seed) if draws is None else np.asarray(draws)
    out = np.empty(len(draws), dtype=float)
    for r, sampled in enumerate(draws):
        vals = []
        for i, bundle in enumerate(bundles):
            idx = reconstruct_cluster_indices(bundle["subject_id"], sampled, subjects)
            sliced = _slice_bundle(bundle, idx)
            q = qhats[i] if qhats is not None else None
            vals.append(_metric(sliced, metric, q, alpha))
        out[r] = np.nanmean(vals)
    return out


def paired_bootstrap_difference(
    condition_a: list[dict[str, np.ndarray]], condition_b: list[dict[str, np.ndarray]], metric: str,
    *, reps: int = 2000, seed: int = 2028, qhats_a: list[float] | None = None,
    qhats_b: list[float] | None = None, alpha: float | None = None,
) -> np.ndarray:
    subjects = sorted(set(np.asarray(condition_a[0]["subject_id"]).tolist()))
    draws = bootstrap_subject_draws(len(subjects), reps=reps, seed=seed)
    out = np.empty(reps, dtype=float)
    for r, sampled in enumerate(draws):
        a, b = [], []
        for i, (left, right) in enumerate(zip(condition_a, condition_b)):
            idx = reconstruct_cluster_indices(left["subject_id"], sampled, subjects)
            a.append(_metric(_slice_bundle(left, idx), metric, qhats_a[i] if qhats_a else None, alpha))
            b.append(_metric(_slice_bundle(right, idx), metric, qhats_b[i] if qhats_b else None, alpha))
        out[r] = np.nanmean(a) - np.nanmean(b)
    return out


def interaction_bootstrap_difference(source_a: dict[str, np.ndarray], source_b: dict[str, np.ndarray], target_a: dict[str, np.ndarray], target_b: dict[str, np.ndarray], metric: str, *, reps: int = 2000, seed: int = 2028) -> np.ndarray:
    source_subjects = sorted(set(np.asarray(source_a["subject_id"]).tolist()))
    target_subjects = sorted(set(np.asarray(target_a["subject_id"]).tolist()))
    rng = np.random.default_rng(seed)
    out = np.empty(reps, dtype=float)
    for r in range(reps):
        sd = rng.integers(0, len(source_subjects), size=len(source_subjects))
        td = rng.integers(0, len(target_subjects), size=len(target_subjects))
        si = reconstruct_cluster_indices(source_a["subject_id"], sd, source_subjects)
        ti = reconstruct_cluster_indices(target_a["subject_id"], td, target_subjects)
        known = _metric(_slice_bundle(source_a, si), metric) - _metric(_slice_bundle(source_b, si), metric)
        unseen = _metric(_slice_bundle(target_a, ti), metric) - _metric(_slice_bundle(target_b, ti), metric)
        out[r] = unseen - known
    return out


def percentile_interval(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    finite = values[np.isfinite(values)]
    if len(finite) != len(values):
        raise ValueError("undefined bootstrap replicates must be audited before interval construction")
    return float(np.percentile(finite, 2.5)), float(np.percentile(finite, 97.5))


def conformal_gap_orientation() -> str:
    return "zero_is_ideal_signed_gap"


def weighted_metric_replicates(bundle: dict[str, np.ndarray], metric: str, draws: np.ndarray, *, qhat: float | None = None, alpha: float | None = None, batch_size: int = 32) -> np.ndarray:
    """Compute exact subject-cluster bootstrap values with multiplicity weights."""
    subject_ids = np.asarray(bundle["subject_id"]); subjects = sorted(set(subject_ids.tolist()))
    subject_index = np.asarray([subjects.index(x) for x in subject_ids], dtype=np.int64)
    probs = softmax(bundle["logits"]); labels = np.asarray(bundle["labels"], dtype=np.int64)
    pred = probs.argmax(1); errors = (pred != labels).astype(float); unc = entropy(probs)
    n_subjects = len(subjects); draws=np.asarray(draws, dtype=np.int64); out=np.empty(len(draws), dtype=float)
    asc=np.argsort(unc, kind="stable"); desc=np.argsort(-unc, kind="stable")
    per_nll=-np.log(np.clip(probs[np.arange(len(labels)),labels],1e-12,1.0)); per_brier=np.sum((probs-np.eye(5)[labels])**2,axis=1)
    if metric.startswith(('coverage_','gap_')):
        if qhat is None or alpha is None: raise ValueError('conformal metrics require qhat and alpha')
        from .evaluation_step11 import aps_prediction_set
        per_cov=aps_prediction_set(probs,qhat)[np.arange(len(labels)),labels].astype(float)
    # Subject-level sufficient statistics make additive metrics O(replicates x subjects).
    def sums(x): return np.bincount(subject_index,weights=x,minlength=n_subjects)
    nll_s,brier_s,cov_s=sums(per_nll),sums(per_brier),sums(per_cov) if metric.startswith(('coverage_','gap_')) else (None,None,None)
    cm_s=np.zeros((n_subjects,5,5),float)
    for i in range(5):
        for j in range(5): cm_s[:,i,j]=sums(((labels==i)&(pred==j)).astype(float))
    epoch_counts=np.bincount(subject_index,minlength=n_subjects).astype(float)
    for start in range(0,len(draws),batch_size):
        d=draws[start:start+batch_size]; weights=np.zeros((len(d),n_subjects),float)
        rr=np.arange(len(d))[:,None]; np.add.at(weights,(np.broadcast_to(rr,d.shape),d),1.0)
        total=weights@epoch_counts
        if metric=='NLL': out[start:start+len(d)]=(weights@nll_s)/total; continue
        if metric=='Brier': out[start:start+len(d)]=(weights@brier_s)/total; continue
        if metric.startswith(('coverage_','gap_')):
            cov=(weights@cov_s)/total; out[start:start+len(d)]=cov if metric.startswith('coverage_') else (1-alpha-cov); continue
        if metric=='macro-F1':
            cm=np.einsum('rs,sij->rij',weights,cm_s); tp=np.diagonal(cm,axis1=1,axis2=2); den=2*tp+cm.sum(1)-tp+cm.sum(2)-tp
            out[start:start+len(d)]=np.mean(np.divide(2*tp,den,out=np.zeros_like(tp),where=den>0),axis=1); continue
        w=weights[:,subject_index]
        if metric=='AURC':
            ww=w[:,asc]; risk=np.cumsum(ww*errors[asc],axis=1)/np.maximum(np.cumsum(ww,axis=1),1); out[start:start+len(d)]=np.sum(ww*risk,axis=1)/total; continue
        if metric=='ERROR_AUROC':
            ww=w[:,asc]; yy=errors[asc]; pos=np.sum(ww*yy,axis=1); neg=total-pos; ranks=np.cumsum(ww,axis=1)-ww/2+0.5; num=np.sum(ww*yy*ranks,axis=1)-pos*(pos+1)/2; out[start:start+len(d)]=np.divide(num,pos*neg,out=np.full(len(d),np.nan),where=(pos>0)&(neg>0)); continue
        if metric=='ERROR_AUPRC':
            ww=w[:,desc]; yy=errors[desc]; tp=np.cumsum(ww*yy,axis=1); positives=tp[:,-1]; precision=tp/np.maximum(np.cumsum(ww,axis=1),1); recall=tp/np.maximum(positives[:,None],1); out[start:start+len(d)]=np.sum(np.diff(recall,axis=1)*precision[:,1:],axis=1); out[start:start+len(d)][positives==0]=np.nan; continue
        raise ValueError(metric)
    return out
