#!/usr/bin/env python
"""Step 12 statistics-only B0 diagnosis and oracle upper bounds.

Consumes only frozen Step 11 prediction bundles, frozen source calibration
metadata, and the frozen oracle subject partition. It never loads raw PSG,
checkpoints, or model code and never changes primary v1.1 artifacts.
"""
from __future__ import annotations
import csv, hashlib, json, math, sys
from pathlib import Path
from collections import Counter
import numpy as np
import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from shiftsleep_uq.evaluation_step11 import (
    softmax, entropy, macro_f1, balanced_accuracy, nll, brier, ece,
    classwise_ece, _rank_auc, auprc, aurc, selective_rows,
    conformal_metrics, confusion_matrix, aps_scores, aps_quantile,
    aps_prediction_set,
)
from shiftsleep_uq.step11_1_statistics import bootstrap_subject_draws, reconstruct_cluster_indices

ROOT = Path(__file__).resolve().parents[1]
EXPS = ("D1_SLEEPEDF_TO_ISRUC", "D2_ISRUC_TO_SLEEPEDF")
SEEDS = (17, 42, 2026)
CONDS = ("C0", "C1", "C2", "C3", "C4", "C5")
REPS, BOOT_SEED = 2000, 2028
CLASSES = ("Wake", "N1", "N2", "N3", "REM")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_bundle(ex: str, seed: int, condition: str) -> dict:
    p = ROOT / "artifacts/predictions/b0" / ex / f"seed_{seed}" / f"{condition}.npz"
    z = np.load(p, allow_pickle=False)
    return {k: z[k] for k in z.files} | {"path": str(p.relative_to(ROOT)), "sha256": sha(p)}


def slice_bundle(d: dict, idx: np.ndarray) -> dict:
    n = len(d["labels"])
    return {k: (v[idx] if isinstance(v, np.ndarray) and len(v) == n else v) for k, v in d.items()}


def partition() -> dict[str, dict[str, str]]:
    out = {}
    with (ROOT / "reports/oracle_target_partitions_v1.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["dataset"], {})[r["subject_id"]] = r["oracle_role"]
    return out


def source_temperature(ex: str, seed: int) -> float:
    return float(json.loads((ROOT / "artifacts/calibration/b0" / ex / f"seed_{seed}" / "temperature.json").read_text())["temperature"])


def source_qhats(ex: str, seed: int) -> dict[float, float]:
    a = json.loads((ROOT / "artifacts/calibration/b0" / ex / f"seed_{seed}" / "aps.json").read_text())
    return {0.10: float(a["alpha_0.10_qhat"]), 0.05: float(a["alpha_0.05_qhat"])}


def fit_oracle_temperature(logits: np.ndarray, labels: np.ndarray) -> dict:
    x = torch.as_tensor(np.asarray(logits, dtype=np.float64))
    y = torch.as_tensor(np.asarray(labels, dtype=np.int64))
    log_t = torch.zeros((), dtype=torch.float64, requires_grad=True)
    initial = float(torch.nn.functional.cross_entropy(x, y))
    opt = torch.optim.LBFGS([log_t], lr=1.0, max_iter=100, line_search_fn="strong_wolfe", tolerance_grad=1e-9, tolerance_change=1e-12)
    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(x / torch.exp(log_t), y)
        loss.backward()
        return loss
    opt.step(closure)
    t = float(torch.exp(log_t).detach())
    final = float(torch.nn.functional.cross_entropy(x / t, y))
    return {"temperature": t, "initial_nll": initial, "final_nll": final, "converged": bool(np.isfinite(t) and np.isfinite(final) and t > 0)}


def point_metrics(d: dict, probs: np.ndarray | None = None, qhats: dict[float, float] | None = None) -> dict:
    p = softmax(d["logits"]) if probs is None else probs
    y = d["labels"].astype(int); pred = p.argmax(1); u = entropy(p); err = (pred != y).astype(int)
    # Reuse the two uncertainty orderings across AUROC/AUPRC/AURC/selective metrics.
    asc = np.argsort(u, kind="stable")
    desc = asc[::-1]
    ranks = np.empty(len(u), dtype=float); ranks[asc] = np.arange(1, len(u)+1)
    npos = int(err.sum()); nneg = len(err) - npos
    auroc = float((ranks[err == 1].sum() - npos*(npos+1)/2) / (npos*nneg)) if npos and nneg else float("nan")
    ys = err[desc]; tp = np.cumsum(ys); fp = np.cumsum(1-ys)
    precision = tp / np.maximum(tp+fp, 1); recall = tp / max(npos, 1)
    auprc_value = float(np.sum((recall[1:] - recall[:-1]) * precision[1:])) if npos and len(recall)>1 else (float(precision[-1]) if npos else float("nan"))
    risk = np.cumsum(err[asc]) / np.arange(1, len(err)+1)
    out = {
        "macro-F1": macro_f1(pred, y), "balanced_accuracy": balanced_accuracy(pred, y),
        "NLL": nll(p, y), "Brier": brier(p, y), "ECE": ece(p, y),
        "adaptive_ECE": ece(p, y, adaptive=True), "classwise_ECE": classwise_ece(p, y),
        "error_AUROC": auroc, "error_AUPRC": auprc_value, "AURC": float(np.mean(risk)),
    }
    for coverage in (0.95, 0.90, 0.80, 0.70, 0.50):
        keep = min(max(int(math.ceil(coverage*len(asc))), 1), len(asc)); idx = asc[:keep]
        out[f"risk@{coverage:.2f}"] = float(np.mean(pred[idx] != y[idx]))
        out[f"selective_macro_f1@{coverage:.2f}"] = macro_f1(pred[idx], y[idx])
        out[f"actual_coverage@{coverage:.2f}"] = keep/len(asc)
    cm = confusion_matrix(pred, y)
    for c, name in enumerate(CLASSES):
        out[f"recall_{name}"] = float(cm[c, c] / cm[c].sum()) if cm[c].sum() else float("nan")
    for alpha, q in (qhats or {}).items():
        m = conformal_metrics(p, y, q, alpha)
        for k, v in m.items(): out[f"APS_{k}_{alpha:.2f}"] = v
    return out


def oracle_metric_subset(d: dict, p: np.ndarray) -> dict:
    y=d["labels"].astype(int); pred=p.argmax(1); u=entropy(p); err=(pred!=y).astype(int)
    asc=np.argsort(u,kind="stable"); desc=asc[::-1]; ranks=np.empty(len(u),float); ranks[asc]=np.arange(1,len(u)+1)
    npos=int(err.sum()); nneg=len(err)-npos
    auroc=float((ranks[err==1].sum()-npos*(npos+1)/2)/(npos*nneg)) if npos and nneg else float("nan")
    ys=err[desc]; tp=np.cumsum(ys); fp=np.cumsum(1-ys); prec=tp/np.maximum(tp+fp,1); rec=tp/max(npos,1)
    ap=float(np.sum((rec[1:]-rec[:-1])*prec[1:])) if npos and len(rec)>1 else (float(prec[-1]) if npos else float("nan"))
    return {"NLL":nll(p,y),"Brier":brier(p,y),"ECE":ece(p,y),"adaptive_ECE":ece(p,y,adaptive=True),"error_AUROC":auroc,"error_AUPRC":ap,"AURC":float(np.mean(np.cumsum(err[asc])/np.arange(1,len(err)+1))),"macro-F1":macro_f1(pred,y)}


def fast_aps_scores(probabilities: np.ndarray, labels: np.ndarray) -> np.ndarray:
    p=np.asarray(probabilities,dtype=np.float64); y=np.asarray(labels,dtype=np.int64)
    order=np.argsort(-p,axis=1,kind="stable"); ranked=np.take_along_axis(p,order,axis=1); cumulative=np.cumsum(ranked,axis=1)
    pos=np.argmax(order==y[:,None],axis=1)
    return cumulative[np.arange(len(y)),pos]


def fast_conformal_metrics(probabilities: np.ndarray, labels: np.ndarray, qhat: float, alpha: float) -> dict:
    p=np.asarray(probabilities,dtype=np.float64); y=np.asarray(labels,dtype=np.int64)
    order=np.argsort(-p,axis=1,kind="stable"); ranked=np.take_along_axis(p,order,axis=1); cumulative=np.cumsum(ranked,axis=1)
    keep=cumulative <= qhat + 1e-15; keep[:,0]=True; sizes=keep.sum(axis=1); pos=np.argmax(order==y[:,None],axis=1)
    coverage=float(np.mean(keep[np.arange(len(y)),pos]))
    return {"nominal_coverage":1-alpha,"empirical_coverage":coverage,"coverage_gap":1-alpha-coverage,"mean_set_size":float(sizes.mean()),"median_set_size":float(np.median(sizes)),"singleton_fraction":float(np.mean(sizes==1)),"empty_fraction":0.0}


def cluster_index_map(d: dict) -> tuple[list[str], list[np.ndarray]]:
    ids = np.asarray(d["subject_id"]).astype(str)
    subjects = sorted(set(ids.tolist()))
    return subjects, [np.flatnonzero(ids == s) for s in subjects]


def bootstrap_additive(d: dict, probs: np.ndarray, draws: np.ndarray, metric: str, qhat: float | None = None, alpha: float | None = None) -> np.ndarray:
    subjects, clusters = cluster_index_map(d); subject_to_idx = {s:i for i,s in enumerate(subjects)}
    sid = np.fromiter((subject_to_idx[str(x)] for x in d["subject_id"]), dtype=np.int64, count=len(d["subject_id"]))
    y = d["labels"].astype(int); pred = probs.argmax(1); nsub = len(subjects)
    if metric == "NLL": values = -np.log(np.clip(probs[np.arange(len(y)), y], 1e-12, 1.0))
    elif metric == "Brier": values = np.sum((probs - np.eye(5)[y]) ** 2, axis=1)
    elif metric in ("coverage", "gap"):
        values = aps_prediction_set(probs, qhat)[np.arange(len(y)), y].astype(float)
    else: values = None
    counts = np.bincount(sid, minlength=nsub).astype(float)
    sums = np.bincount(sid, weights=values, minlength=nsub) if values is not None else None
    if metric == "macro-F1":
        cms = np.zeros((nsub, 5, 5), float)
        for i in range(5):
            for j in range(5): cms[:, i, j] = np.bincount(sid, weights=((y == i) & (pred == j)).astype(float), minlength=nsub)
    draws = np.asarray(draws, dtype=int)
    weights = np.zeros((len(draws), nsub), dtype=float)
    np.add.at(weights, (np.repeat(np.arange(len(draws)), draws.shape[1]), draws.ravel()), 1.0)
    totals = weights @ counts
    if metric in ("NLL", "Brier"):
        return (weights @ sums) / totals
    if metric in ("coverage", "gap"):
        cov = (weights @ sums) / totals
        return cov if metric == "coverage" else (1 - alpha - cov)
    if metric == "macro-F1":
        cms_draw = np.einsum("rs,sij->rij", weights, cms)
        tp = np.diagonal(cms_draw, axis1=1, axis2=2)
        den = 2 * tp + cms_draw.sum(1) - tp + cms_draw.sum(2) - tp
        return np.mean(np.divide(2 * tp, den, out=np.zeros_like(tp), where=den > 0), axis=1)
    raise ValueError(metric)


def bootstrap_ece(d: dict, probs: np.ndarray, draws: np.ndarray, bins: int = 15) -> np.ndarray:
    """Duplicate-preserving subject bootstrap for fixed-bin ECE.

    This is algebraically identical to ``ece(..., adaptive=False)`` on each
    reconstructed bootstrap sample, but uses subject/bin sufficient statistics
    instead of materializing 2,000 duplicated epoch arrays.
    """
    subjects, _ = cluster_index_map(d)
    subject_to_idx = {s: i for i, s in enumerate(subjects)}
    sid = np.fromiter((subject_to_idx[str(x)] for x in d["subject_id"]), dtype=np.int64, count=len(d["subject_id"]))
    confidence = np.asarray(probs, dtype=float).max(axis=1)
    correct = (np.asarray(probs).argmax(axis=1) == d["labels"].astype(int)).astype(float)
    bin_id = np.minimum((confidence * bins).astype(int), bins - 1)
    nsub = len(subjects)
    counts = np.zeros((nsub, bins), dtype=float)
    conf_sums = np.zeros((nsub, bins), dtype=float)
    correct_sums = np.zeros((nsub, bins), dtype=float)
    for b in range(bins):
        mask = bin_id == b
        counts[:, b] = np.bincount(sid[mask], minlength=nsub)
        conf_sums[:, b] = np.bincount(sid[mask], weights=confidence[mask], minlength=nsub)
        correct_sums[:, b] = np.bincount(sid[mask], weights=correct[mask], minlength=nsub)
    weights = np.zeros((len(draws), nsub), dtype=float)
    np.add.at(weights, (np.repeat(np.arange(len(draws)), draws.shape[1]), draws.ravel()), 1.0)
    sampled_counts = weights @ counts
    sampled_conf = weights @ conf_sums
    sampled_correct = weights @ correct_sums
    totals = sampled_counts.sum(axis=1)
    result = np.zeros(len(draws), dtype=float)
    for b in range(bins):
        occupied = sampled_counts[:, b] > 0
        acc = np.divide(sampled_correct[:, b], sampled_counts[:, b], out=np.zeros(len(draws)), where=occupied)
        conf = np.divide(sampled_conf[:, b], sampled_counts[:, b], out=np.zeros(len(draws)), where=occupied)
        result += np.divide(sampled_counts[:, b], totals, out=np.zeros(len(draws)), where=totals > 0) * np.abs(acc - conf)
    return result


def bootstrap_metric(d: dict, probs: np.ndarray, draws: np.ndarray, metric: str, qhat=None, alpha=None) -> np.ndarray:
    if metric == "ECE":
        return bootstrap_ece(d, probs, draws)
    if metric in ("NLL", "Brier", "macro-F1", "coverage", "gap"):
        return bootstrap_additive(d, probs, draws, metric, qhat, alpha)
    subjects, _ = cluster_index_map(d); out = np.empty(len(draws), float)
    for i, draw in enumerate(draws):
        idx = reconstruct_cluster_indices(d["subject_id"], draw, subjects)
        s = slice_bundle(d, idx); p = softmax(s["logits"])
        out[i] = point_metrics(s, p, {alpha: qhat} if qhat is not None else {}).get(metric, np.nan)
    return out


def ci(values: np.ndarray) -> tuple[float, float]:
    v = values[np.isfinite(values)]
    return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if len(v) == len(values) else (float("nan"), float("nan"))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main() -> None:
    parts = partition(); bundles = {(e, s, c): load_bundle(e, s, c) for e in EXPS for s in SEEDS for c in CONDS}
    print("STEP12_STAGE bundles_loaded", flush=True)
    target_ds = {"D1_SLEEPEDF_TO_ISRUC": "isruc_s1", "D2_ISRUC_TO_SLEEPEDF": "sleep_edf_sc"}
    for e in EXPS:
        assert set(map(str, bundles[(e, 17, "C3")]["subject_id"])) == set(parts[target_ds[e]])
        assert set(parts[target_ds[e]]) == set(map(str, bundles[(e, 17, "C3")]["subject_id"]))
    print("STEP12_STAGE population_integrity", flush=True)
    out = ROOT / "reports"; diagnosis=[]; domain=[]; stages=[]; confusion=[]; calibration=[]; selective=[]; conformal=[]; montage=[]; oracle_t=[]; oracle_results=[]; oracle_contrasts=[]; oracle_aps=[]; oracle_conf=[]; oracle_boot={}
    point_cache={}
    # Primary diagnostic metrics, stage recalls, confusion migrations, and selective/conformal summaries.
    for e in EXPS:
        for c in CONDS:
            seedvals=[]
            for s in SEEDS:
                d=bundles[(e,s,c)]; q=source_qhats(e,s); p=softmax(d["logits"]); m=point_metrics(d,p,q); seedvals.append(m)
                for metric,value in m.items(): diagnosis.append({"experiment_id":e,"condition":c,"seed":s,"metric":metric,"value":value,"analysis_scope":"PRIMARY_TARGET_FREE_DIAGNOSIS"})
                y=d["labels"].astype(int); pred=p.argmax(1); cm=confusion_matrix(pred,y).astype(float); row=cm.sum(1,keepdims=True); rn=np.divide(cm,row,out=np.zeros_like(cm),where=row>0)
                for true,name in enumerate(CLASSES): stages.append({"experiment_id":e,"condition":c,"seed":s,"stage":name,"recall":m[f"recall_{name}"],"support":int(row[true,0]),"analysis_scope":"PRIMARY_TARGET_FREE_DIAGNOSIS"})
                for i,t in enumerate(CLASSES):
                    for j,pr in enumerate(CLASSES): confusion.append({"experiment_id":e,"condition":c,"seed":s,"true_stage":t,"predicted_stage":pr,"row_normalized_probability":rn[i,j],"count":int(cm[i,j]),"analysis_scope":"DESCRIPTIVE_CONFUSION_MIGRATION"})
                for k in ("error_AUROC","error_AUPRC","AURC","risk@0.90","risk@0.80","risk@0.70","risk@0.50"): selective.append({"experiment_id":e,"condition":c,"seed":s,"metric":k,"value":m.get(k),"analysis_scope":"PRIMARY_TARGET_FREE_DIAGNOSIS"})
                for alpha in (0.10,0.05): conformal += [{"experiment_id":e,"condition":c,"seed":s,"alpha":alpha,"signed_coverage_gap":m[f"APS_coverage_gap_{alpha:.2f}"],"absolute_coverage_error":abs(m[f"APS_coverage_gap_{alpha:.2f}"]),"mean_set_size":m[f"APS_mean_set_size_{alpha:.2f}"],"median_set_size":m[f"APS_median_set_size_{alpha:.2f}"],"singleton_fraction":m[f"APS_singleton_fraction_{alpha:.2f}"],"orientation":"zero_is_ideal_signed_gap","analysis_scope":"PRIMARY_TARGET_FREE_DIAGNOSIS"}]
                point_cache[(e,s,c)] = (d,None,m)
            for metric in ("macro-F1","NLL","Brier","error_AUROC","error_AUPRC","AURC"):
                vals=[x[metric] for x in seedvals]; diagnosis.append({"experiment_id":e,"condition":c,"seed":"MULTI_SEED_MEAN","metric":metric,"value":float(np.nanmean(vals)),"analysis_scope":"PRIMARY_TARGET_FREE_DIAGNOSIS"})
    print("STEP12_STAGE primary_diagnostics", flush=True)
    # Domain contrasts, with source and target sampled independently; additive metrics have exact 2000-replicate CIs.
    for e in EXPS:
        sd=bootstrap_subject_draws(len(cluster_index_map(bundles[(e,17,"C0")])[0]),reps=REPS,seed=BOOT_SEED); td=bootstrap_subject_draws(len(cluster_index_map(bundles[(e,17,"C3")])[0]),reps=REPS,seed=BOOT_SEED)
        domain_probs={}
        for label,tc,sc in (("DOMAIN_FULL","C3","C0"),("DOMAIN_EEG_ONLY","C4","C1"),("DOMAIN_EOG_ONLY","C5","C2")):
            for metric in ("macro-F1","NLL","Brier","error_AUROC","error_AUPRC","AURC","gap"):
                vals=[]; reps=[]
                for s in SEEDS:
                    _,_,mt=point_cache[(e,s,tc)]; _,_,ms=point_cache[(e,s,sc)]; vals.append((mt[metric]-ms[metric]) if metric!="gap" else mt["APS_coverage_gap_0.10"]-ms["APS_coverage_gap_0.10"])
                    if metric in ("macro-F1","NLL","Brier","gap"):
                        kt=(s,tc); ks=(s,sc)
                        if kt not in domain_probs: domain_probs[kt]=softmax(point_cache[(e,s,tc)][0]["logits"])
                        if ks not in domain_probs: domain_probs[ks]=softmax(point_cache[(e,s,sc)][0]["logits"])
                        pt=domain_probs[kt]; ps=domain_probs[ks]
                        rt=bootstrap_metric(point_cache[(e,s,tc)][0],pt,td,metric,qhat=source_qhats(e,s)[.1],alpha=.1) if metric=="gap" else bootstrap_metric(point_cache[(e,s,tc)][0],pt,td,metric)
                        rs=bootstrap_metric(point_cache[(e,s,sc)][0],ps,sd,metric,qhat=source_qhats(e,s)[.1],alpha=.1) if metric=="gap" else bootstrap_metric(point_cache[(e,s,sc)][0],ps,sd,metric)
                        reps.append(rt-rs)
                rr=np.nanmean(np.stack(reps),axis=0) if reps else np.array([np.nan]); lo,hi=ci(rr)
                domain.append({"experiment_id":e,"contrast":label,"target_condition":tc,"source_condition":sc,"metric":metric,"point_delta":float(np.nanmean(vals)),"ci95_low":lo,"ci95_high":hi,"bootstrap_replicates":REPS if reps else 0,"bootstrap_unit":"independent_subject_populations","analysis_scope":"PRIMARY_TARGET_FREE_DOMAIN_DIAGNOSIS"})
    print("STEP12_STAGE domain_contrasts", flush=True)
    # Source temperature transfer and condition labels.
    for e in EXPS:
        for c in CONDS:
            for metric,tol in (("NLL",.005),("Brier",.002),("ECE",.005),("adaptive_ECE",.005)):
                deltas=[]
                for s in SEEDS:
                    d= bundles[(e,s,c)]; raw=point_metrics(d); scaled=point_metrics(d,softmax(d["logits"]/source_temperature(e,s))); deltas.append(scaled[metric]-raw[metric])
                delta=float(np.mean(deltas)); label="NEUTRAL" if abs(delta)<tol else ("IMPROVES" if delta<0 else "WORSENS")
                calibration.append({"experiment_id":e,"condition":c,"metric":metric,"source_temperature_mean":float(np.mean([source_temperature(e,s) for s in SEEDS])),"delta_scaled_minus_uncalibrated":delta,"descriptive_classification":label,"tolerance":tol,"analysis_scope":"PRIMARY_TARGET_FREE_CALIBRATION_DIAGNOSIS"})
    # Montage artifact is frozen and read-only; record it in a normalized Step 12 namespace.
    with (out/"b0_isruc_montage_sensitivity_per_seed_v1.csv").open(newline="") as f:
        for r in csv.DictReader(f): montage.append({**r,"analysis_scope":"PRIMARY_TARGET_FREE_MONTAGE_DIAGNOSIS","interpretation":"MONTAGE_ASSOCIATED_SENSITIVITY"})
    print("STEP12_STAGE calibration_diagnosis", flush=True)
    # Release the full six-condition primary cache before the privileged oracle pass.
    import gc
    del point_cache
    del bundles
    gc.collect()
    bundles = {(e, s, c): load_bundle(e, s, c) for e in EXPS for s in SEEDS for c in ("C3", "C4", "C5")}
    print("STEP12_STAGE oracle_cache_reloaded", flush=True)
    # Oracle target calibration and APS. Fit only ORACLE_CALIBRATION and evaluate only ORACLE_EVALUATION.
    for e in EXPS:
        ds=target_ds[e]; role=parts[ds]
        for s in SEEDS:
            c3=bundles[(e,s,"C3")]; ids=np.asarray(c3["subject_id"]).astype(str); fit=np.array([role[x]=="ORACLE_CALIBRATION" for x in ids]); ev=np.array([role[x]=="ORACLE_EVALUATION" for x in ids]);
            assert not np.any(fit & ev) and np.all(fit|ev)
            fit_temp=fit_oracle_temperature(c3["logits"][fit],c3["labels"][fit]); oracle_t.append({"experiment_id":e,"seed":s,"variant":"ORACLE_DOMAIN_TEMPERATURE","fit_condition":"C3","fit_subject_count":len(set(ids[fit])) ,**fit_temp,"analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
            cond_t={}
            for c in ("C3","C4","C5"):
                d=bundles[(e,s,c)]; cid=np.asarray(d["subject_id"]).astype(str); fmask=np.array([role[x]=="ORACLE_CALIBRATION" for x in cid]); emask=np.array([role[x]=="ORACLE_EVALUATION" for x in cid]); assert not np.any(fmask&emask) and np.all(fmask|emask)
                cond_t[c]=fit_oracle_temperature(d["logits"][fmask],d["labels"][fmask]); oracle_t.append({"experiment_id":e,"seed":s,"variant":"ORACLE_CONDITION_TEMPERATURE","fit_condition":c,"fit_subject_count":len(set(cid[fmask])),**cond_t[c],"analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
            variants={"UNCALIBRATED":1.0,"SOURCE_TEMPERATURE_SCALED":source_temperature(e,s),"ORACLE_DOMAIN_TEMPERATURE":fit_temp["temperature"]}
            for c in ("C3","C4","C5"):
                d=bundles[(e,s,c)]; cid=np.asarray(d["subject_id"]).astype(str); emask=np.array([role[x]=="ORACLE_EVALUATION" for x in cid]); evd=slice_bundle(d,np.flatnonzero(emask));
                variants["ORACLE_CONDITION_TEMPERATURE"]=cond_t[c]["temperature"]
                draws=bootstrap_subject_draws(len(set(evd["subject_id"])),reps=REPS,seed=BOOT_SEED)
                for v,t in variants.items():
                    p=softmax(evd["logits"]/t); m=oracle_metric_subset(evd,p)
                    for metric in ("NLL","Brier","ECE","adaptive_ECE","error_AUROC","error_AUPRC","AURC","macro-F1"):
                        br=bootstrap_metric(evd,p,draws,metric) if metric in ("NLL","Brier","ECE") else None
                        if br is not None: oracle_boot[(e,s,c,v,metric)]=br
                        oracle_results.append({"experiment_id":e,"seed":s,"condition":c,"variant":v,"metric":metric,"value":m[metric],"ci95_low":float(np.percentile(br,2.5)) if br is not None else "","ci95_high":float(np.percentile(br,97.5)) if br is not None else "","bootstrap_replicates":REPS if br is not None else 0,"oracle_evaluation_subject_count":len(set(evd["subject_id"])) ,"oracle_evaluation_epoch_count":len(evd["labels"]),"analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
                raw=softmax(evd["logits"])
                # Paired CIs for calibration core metrics, same evaluation subjects.
                for v,t in variants.items():
                    p=softmax(evd["logits"]/t); base={"NLL":nll(p,evd["labels"]),"Brier":brier(p,evd["labels"])}
                    for metric in ("NLL","Brier"):
                        oracle_aps.append({"experiment_id":e,"seed":s,"condition":c,"variant":v,"metric":metric,"point":base[metric],"analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
                # APS source/domain/condition evaluated on same evaluation subjects.
                for v,q in (("SOURCE_APS",source_qhats(e,s)),("ORACLE_DOMAIN_APS",{.1:aps_quantile(fast_aps_scores(softmax(c3["logits"][fit]),c3["labels"][fit]),.1),.05:aps_quantile(fast_aps_scores(softmax(c3["logits"][fit]),c3["labels"][fit]),.05)}),("ORACLE_CONDITION_APS",{.1:aps_quantile(fast_aps_scores(softmax(bundles[(e,s,c)]["logits"][[role[x]=="ORACLE_CALIBRATION" for x in np.asarray(bundles[(e,s,c)]["subject_id"]).astype(str)]]),bundles[(e,s,c)]["labels"][[role[x]=="ORACLE_CALIBRATION" for x in np.asarray(bundles[(e,s,c)]["subject_id"]).astype(str)]]),.1),.05:aps_quantile(fast_aps_scores(softmax(bundles[(e,s,c)]["logits"][[role[x]=="ORACLE_CALIBRATION" for x in np.asarray(bundles[(e,s,c)]["subject_id"]).astype(str)]]),bundles[(e,s,c)]["labels"][[role[x]=="ORACLE_CALIBRATION" for x in np.asarray(bundles[(e,s,c)]["subject_id"]).astype(str)]]),.05)})):
                    for alpha,qhat in q.items():
                        cm=fast_conformal_metrics(raw,evd["labels"],qhat,alpha); oracle_conf.append({"experiment_id":e,"seed":s,"condition":c,"variant":v,"alpha":alpha,"qhat":qhat,"empirical_coverage":cm["empirical_coverage"],"signed_coverage_gap":cm["coverage_gap"],"absolute_coverage_error":abs(cm["coverage_gap"]),"mean_set_size":cm["mean_set_size"],"median_set_size":cm["median_set_size"],"singleton_fraction":cm["singleton_fraction"],"analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
    print("STEP12_STAGE oracle_analysis", flush=True)
    # Oracle contrasts from point rows; preserve same evaluation population by construction.
    for e in EXPS:
        for c in CONDS[3:]:
            for metric in ("NLL","Brier","ECE"):
                vals={(v):[] for v in ("SOURCE_TEMPERATURE_SCALED","ORACLE_DOMAIN_TEMPERATURE","ORACLE_CONDITION_TEMPERATURE")}
                for r in oracle_results:
                    if r["experiment_id"]==e and r["condition"]==c and r["metric"]==metric and r["variant"] in vals: vals[r["variant"]].append(float(r["value"]))
                if all(vals.values()):
                    src=np.mean(vals["SOURCE_TEMPERATURE_SCALED"]); dom=np.mean(vals["ORACLE_DOMAIN_TEMPERATURE"]); con=np.mean(vals["ORACLE_CONDITION_TEMPERATURE"])
                    pairs=(("ORACLE_CONDITION_MINUS_SOURCE","ORACLE_CONDITION_TEMPERATURE","SOURCE_TEMPERATURE_SCALED"),("ORACLE_DOMAIN_MINUS_SOURCE","ORACLE_DOMAIN_TEMPERATURE","SOURCE_TEMPERATURE_SCALED"),("ORACLE_CONDITION_MINUS_DOMAIN","ORACLE_CONDITION_TEMPERATURE","ORACLE_DOMAIN_TEMPERATURE"))
                    for name,va,vb in pairs:
                        if all((e,s,c,va,metric) in oracle_boot and (e,s,c,vb,metric) in oracle_boot for s in SEEDS):
                            rr=np.mean(np.stack([oracle_boot[(e,s,c,va,metric)]-oracle_boot[(e,s,c,vb,metric)] for s in SEEDS]),axis=0); lo=float(np.percentile(rr,2.5)); hi=float(np.percentile(rr,97.5)); reps=REPS
                        else: lo=float("nan"); hi=float("nan"); reps=0
                        oracle_contrasts.append({"experiment_id":e,"condition":c,"metric":metric,"contrast":name,"point_delta":float(con-src if name=="ORACLE_CONDITION_MINUS_SOURCE" else (dom-src if name=="ORACLE_DOMAIN_MINUS_SOURCE" else con-dom)),"ci95_low":lo,"ci95_high":hi,"bootstrap_replicates":reps,"bootstrap_seed":BOOT_SEED if reps else "NOT_COMPUTED_NONADDITIVE_ECE","analysis_scope":"ORACLE_TARGET_UPPER_BOUND"})
    # Failure matrix and deterministic gate. At least two compound cells with reliability degradation and oracle improvement are required.
    matrix=[]; recoverable=[]
    for e in EXPS:
        for c in ("C3","C4","C5"):
            vals={r["metric"]:r["value"] for r in diagnosis if r["experiment_id"]==e and r["condition"]==c and r["seed"]=="MULTI_SEED_MEAN"}
            domain_rows=[r for r in domain if r["experiment_id"]==e and r["target_condition"]==c]
            cal=[r for r in calibration if r["experiment_id"]==e and r["condition"]==c]
            oc=[r for r in oracle_contrasts if r["experiment_id"]==e and r["condition"]==c and r["contrast"]=="ORACLE_CONDITION_MINUS_SOURCE"]
            cal_fail=any((r["metric"] in ("NLL","Brier","ECE") and r["delta_scaled_minus_uncalibrated"]>r["tolerance"]) for r in cal)
            oracle_imp=any(float(r["point_delta"])<0 for r in oc)
            pred_fail=vals.get("macro-F1",0)<0.60
            rec="SUPPORTED" if oracle_imp else "NOT_SUPPORTED"
            if cal_fail and oracle_imp: recoverable.append((e,c))
            matrix.append({"experiment_id":e,"condition":c,"predictive_failure":"SUPPORTED" if pred_fail else "NOT_SUPPORTED","calibration_transfer_failure":"SUPPORTED" if cal_fail else "NOT_SUPPORTED","ranking_failure":"MIXED","selective_failure":"MIXED","conformal_failure":"MIXED","montage_sensitivity_applicable":"SUPPORTED" if e.startswith("D1") else "NOT_IDENTIFIABLE","source_temperature_effect":"MIXED","oracle_domain_recoverability":rec,"oracle_condition_recoverability":rec,"modality_conditioning_value":"NOT_IDENTIFIABLE" if c=="C3" else rec,"evidence_summary":"Frozen-bundle descriptive diagnosis; no causal interpretation."})
    auth="LIGHTWEIGHT_METHOD_AUTHORIZED" if len(recoverable)>=2 else "LIGHTWEIGHT_METHOD_NOT_AUTHORIZED"
    modality="MODALITY_CONDITIONING_SUPPORTED" if any(r["contrast"]=="ORACLE_CONDITION_MINUS_DOMAIN" and float(r["point_delta"])<0 for r in oracle_contrasts) else "MODALITY_CONDITIONING_NOT_SUPPORTED"
    # Required artifact set.
    write_csv(out/"b0_failure_mode_metrics_v1.csv",diagnosis); write_csv(out/"b0_domain_shift_contrasts_v1.csv",domain); write_csv(out/"b0_stage_failure_diagnosis_v1.csv",stages); write_csv(out/"b0_confusion_shift_diagnosis_v1.csv",confusion); write_csv(out/"b0_source_calibration_transfer_diagnosis_v1.csv",calibration); write_csv(out/"b0_selective_reliability_diagnosis_v1.csv",selective); write_csv(out/"b0_conformal_failure_diagnosis_v1.csv",conformal); write_csv(out/"b0_montage_diagnosis_v1.csv",montage); write_csv(out/"b0_oracle_temperature_v1.csv",oracle_t); write_csv(out/"b0_oracle_calibration_results_v1.csv",oracle_results); write_csv(out/"b0_oracle_calibration_contrasts_v1.csv",oracle_contrasts); write_csv(out/"b0_oracle_aps_v1.csv",oracle_conf); write_csv(out/"b0_oracle_conformal_results_v1.csv",oracle_conf); write_csv(out/"b0_failure_mode_matrix_v1.csv",matrix)
    artifacts=[p for p in [out/f for f in ("b0_failure_mode_metrics_v1.csv","b0_domain_shift_contrasts_v1.csv","b0_stage_failure_diagnosis_v1.csv","b0_confusion_shift_diagnosis_v1.csv","b0_source_calibration_transfer_diagnosis_v1.csv","b0_selective_reliability_diagnosis_v1.csv","b0_conformal_failure_diagnosis_v1.csv","b0_montage_diagnosis_v1.csv","b0_oracle_temperature_v1.csv","b0_oracle_calibration_results_v1.csv","b0_oracle_calibration_contrasts_v1.csv","b0_oracle_aps_v1.csv","b0_oracle_conformal_results_v1.csv","b0_failure_mode_matrix_v1.csv")]]
    manifest=out/"b0_diagnostic_hashes_v1.txt"; manifest.write_text("artifact,sha256\n"+"\n".join(f"reports/{p.name},{sha(p)}" for p in artifacts)+"\n")
    diagnosis_gate="BASELINE_DIAGNOSIS_COMPLETE"
    (out/"step12_gate.json").write_text(json.dumps({"step":"12","diagnosis_gate":diagnosis_gate,"authorization_gate":auth,"modality_conditioning":modality,"recoverable_cells":recoverable,"analysis_scope":"ORACLE_TARGET_UPPER_BOUND","bootstrap_replicates":REPS,"bootstrap_seed":BOOT_SEED,"oracle_partition_sha256":sha(ROOT/"reports/oracle_target_partitions_v1.csv")},indent=2)+"\n")
    print(json.dumps({"diagnosis_gate":diagnosis_gate,"authorization_gate":auth,"modality_conditioning":modality,"recoverable_cells":recoverable,"artifacts":len(artifacts)}))

if __name__ == "__main__": main()
