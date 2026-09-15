"""Deterministic, source-calibrated Step 11 evaluation primitives."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import torch

CLASS_COUNT = 5
EPS = 1e-12


class EvaluationPhaseError(PermissionError):
    pass


@dataclass(frozen=True)
class PhaseGate:
    phase: str
    closed: bool = False

    def require_calibration(self) -> None:
        if self.phase != "PHASE_A_CALIBRATION" or self.closed:
            raise EvaluationPhaseError("calibration access is closed or phase is not Phase A")

    def freeze(self) -> "PhaseGate":
        if self.phase != "PHASE_A_CALIBRATION":
            raise EvaluationPhaseError("only Phase A can be frozen")
        return PhaseGate("PHASE_A_CALIBRATION", True)

    def begin_evaluation(self) -> "PhaseGate":
        if self.phase != "PHASE_A_CALIBRATION" or not self.closed:
            raise EvaluationPhaseError("Phase B requires frozen calibration objects")
        return PhaseGate("PHASE_B_EVALUATION", False)

    def require_evaluation(self) -> None:
        if self.phase != "PHASE_B_EVALUATION":
            raise EvaluationPhaseError("evaluation requires Phase B")


def require_fit_role(role: str) -> None:
    if role != "CALIBRATION":
        raise EvaluationPhaseError("temperature/APS fitting requires SOURCE CALIBRATION only")


def require_evaluation_role(role: str) -> None:
    if role not in {"TEST", "COMPLETE_TARGET"}:
        raise EvaluationPhaseError("Phase B evaluation permits TEST or COMPLETE_TARGET only")


def softmax(logits: np.ndarray) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float64)
    z = x - np.max(x, axis=1, keepdims=True)
    p = np.exp(z)
    p /= np.sum(p, axis=1, keepdims=True)
    if not np.isfinite(p).all():
        raise FloatingPointError("non-finite probabilities")
    return p


def fit_temperature(logits: np.ndarray, labels: np.ndarray, *, role: str, config: dict | None = None) -> dict:
    require_fit_role(role)
    x = torch.as_tensor(np.asarray(logits, dtype=np.float64))
    y = torch.as_tensor(np.asarray(labels, dtype=np.int64))
    if x.ndim != 2 or x.shape[1] != CLASS_COUNT or y.shape[0] != x.shape[0]:
        raise ValueError("temperature inputs have invalid shapes")
    settings = {"max_iter": 100, "line_search_fn": "strong_wolfe", "tolerance_grad": 1e-9, "tolerance_change": 1e-12}
    if config:
        settings.update(config)
    log_t = torch.zeros((), dtype=torch.float64, requires_grad=True)
    initial = float(torch.nn.functional.cross_entropy(x, y))
    optimizer = torch.optim.LBFGS([log_t], lr=1.0, max_iter=int(settings["max_iter"]),
                                   line_search_fn=settings["line_search_fn"],
                                   tolerance_grad=float(settings["tolerance_grad"]),
                                   tolerance_change=float(settings["tolerance_change"]))
    def closure() -> torch.Tensor:
        optimizer.zero_grad()
        loss = torch.nn.functional.cross_entropy(x / torch.exp(log_t), y)
        loss.backward()
        return loss
    optimizer.step(closure)
    temperature = float(torch.exp(log_t).detach())
    final = float(torch.nn.functional.cross_entropy(x / temperature, y))
    if not np.isfinite(temperature) or temperature <= 0 or not np.isfinite(final):
        raise FloatingPointError("invalid fitted temperature")
    return {"temperature": temperature, "initial_nll": initial, "final_nll": final,
            "converged": True, "optimization": settings}


def aps_scores(probabilities: np.ndarray, labels: np.ndarray) -> np.ndarray:
    p = np.asarray(probabilities, dtype=np.float64)
    y = np.asarray(labels, dtype=np.int64)
    scores = np.empty(len(y), dtype=np.float64)
    for i, (row, label) in enumerate(zip(p, y)):
        order = np.lexsort((np.arange(CLASS_COUNT), -row))
        cumulative = np.cumsum(row[order])
        position = int(np.flatnonzero(order == label)[0])
        scores[i] = cumulative[position]
    return scores


def aps_quantile(scores: np.ndarray, alpha: float) -> float:
    values = np.sort(np.asarray(scores, dtype=np.float64))
    n = len(values)
    if n == 0 or not (0 < alpha < 1):
        raise ValueError("invalid APS calibration inputs")
    k = min(max(int(math.ceil((n + 1) * (1 - alpha))), 1), n)
    return float(values[k - 1])


def aps_prediction_set(probabilities: np.ndarray, qhat: float) -> np.ndarray:
    p = np.asarray(probabilities, dtype=np.float64)
    result = np.zeros_like(p, dtype=bool)
    for i, row in enumerate(p):
        order = np.lexsort((np.arange(CLASS_COUNT), -row))
        cumulative = np.cumsum(row[order])
        keep = cumulative <= qhat + 1e-15
        keep[0] = True
        result[i, order[keep]] = True
    if not result.any(axis=1).all():
        raise AssertionError("APS produced an empty prediction set")
    return result


def nll(probabilities: np.ndarray, labels: np.ndarray) -> float:
    p = np.clip(np.asarray(probabilities, dtype=np.float64), EPS, 1.0)
    return float(-np.log(p[np.arange(len(labels)), np.asarray(labels, dtype=np.int64)]).mean())


def brier(probabilities: np.ndarray, labels: np.ndarray) -> float:
    p = np.asarray(probabilities, dtype=np.float64)
    onehot = np.zeros_like(p); onehot[np.arange(len(labels)), labels] = 1.0
    return float(np.mean(np.sum((p - onehot) ** 2, axis=1)))


def confusion_matrix(predictions: np.ndarray, labels: np.ndarray) -> np.ndarray:
    matrix = np.zeros((CLASS_COUNT, CLASS_COUNT), dtype=np.int64)
    for truth, pred in zip(labels, predictions):
        matrix[int(truth), int(pred)] += 1
    return matrix


def macro_f1(predictions: np.ndarray, labels: np.ndarray) -> float:
    cm = confusion_matrix(predictions, labels).astype(np.float64)
    tp = np.diag(cm); denom = 2 * tp + (cm.sum(0) - tp) + (cm.sum(1) - tp)
    return float(np.mean(np.divide(2 * tp, denom, out=np.zeros_like(tp), where=denom > 0)))


def kappa(predictions: np.ndarray, labels: np.ndarray) -> float:
    cm = confusion_matrix(predictions, labels).astype(float); n = cm.sum()
    if n == 0: return float("nan")
    po = np.trace(cm) / n; pe = np.sum(cm.sum(0) * cm.sum(1)) / (n * n)
    return float((po - pe) / (1 - pe)) if abs(1 - pe) > EPS else float("nan")


def balanced_accuracy(predictions: np.ndarray, labels: np.ndarray) -> float:
    cm = confusion_matrix(predictions, labels).astype(float)
    recalls = np.divide(np.diag(cm), cm.sum(1), out=np.zeros(CLASS_COUNT), where=cm.sum(1) > 0)
    return float(recalls.mean())


def ece(probabilities: np.ndarray, labels: np.ndarray, *, adaptive: bool = False, bins: int = 15) -> float:
    p = np.asarray(probabilities); y = np.asarray(labels); confidence = p.max(1); correct = (p.argmax(1) == y)
    n = len(y); total = 0.0
    if adaptive:
        order = np.argsort(confidence, kind="stable")
        edges = [int(math.floor(i*n/bins)) for i in range(bins)] + [n]
        ranges = [(edges[i], edges[i+1]) for i in range(bins) if edges[i] < edges[i+1]]
        groups = [order[a:b] for a,b in ranges]
    else:
        groups = [np.flatnonzero((confidence >= i/bins) & ((confidence < (i+1)/bins) if i < bins-1 else (confidence <= 1))) for i in range(bins)]
    for idx in groups:
        if len(idx): total += len(idx)/n * abs(float(correct[idx].mean()) - float(confidence[idx].mean()))
    return float(total)


def classwise_ece(probabilities: np.ndarray, labels: np.ndarray, bins: int = 15) -> float:
    p = np.asarray(probabilities); y = np.asarray(labels); result = []
    for c in range(CLASS_COUNT):
        binary = (y == c).astype(int); confidence = p[:, c]
        total = 0.0
        for i in range(bins):
            idx = np.flatnonzero((confidence >= i/bins) & ((confidence < (i+1)/bins) if i < bins-1 else (confidence <= 1)))
            if len(idx): total += len(idx)/len(y) * abs(float(binary[idx].mean()) - float(confidence[idx].mean()))
        result.append(total)
    return float(np.mean(result))


def entropy(probabilities: np.ndarray) -> np.ndarray:
    p = np.clip(np.asarray(probabilities, dtype=np.float64), EPS, 1.0)
    return -np.sum(p * np.log(p), axis=1)


def _rank_auc(scores: np.ndarray, labels: np.ndarray) -> float:
    y = np.asarray(labels, dtype=int); s = np.asarray(scores, dtype=float)
    if len(np.unique(y)) < 2: return float("nan")
    order = np.argsort(s, kind="stable"); ranks = np.empty(len(s), dtype=float); ranks[order] = np.arange(1, len(s)+1)
    pos = y == 1; npos = pos.sum(); nneg = (~pos).sum()
    return float((ranks[pos].sum() - npos*(npos+1)/2) / (npos*nneg))


def auprc(scores: np.ndarray, labels: np.ndarray) -> float:
    y = np.asarray(labels, dtype=int); s = np.asarray(scores, dtype=float)
    if y.sum() == 0: return float("nan")
    order = np.argsort(-s, kind="stable"); ys = y[order]; tp = np.cumsum(ys); fp = np.cumsum(1-ys)
    precision = tp / np.maximum(tp+fp, 1); recall = tp / y.sum(); return float(np.sum((recall[1:] - recall[:-1]) * precision[1:])) if len(recall)>1 else float(precision[-1])


def aurc(uncertainty: np.ndarray, predictions: np.ndarray, labels: np.ndarray) -> float:
    order = np.argsort(np.asarray(uncertainty), kind="stable")
    errors = (np.asarray(predictions)[order] != np.asarray(labels)[order]).astype(float)
    risk = np.cumsum(errors) / np.arange(1, len(errors)+1)
    return float(np.mean(risk))


def selective_rows(uncertainty: np.ndarray, predictions: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    order = np.argsort(np.asarray(uncertainty), kind="stable"); n = len(order); out = {"AURC": aurc(uncertainty, predictions, labels)}
    for coverage in (0.95, 0.90, 0.80, 0.70, 0.50):
        keep = min(max(int(math.ceil(coverage*n)), 1), n); idx = order[:keep]
        out[f"risk@{coverage:.2f}"] = float(np.mean(predictions[idx] != labels[idx]))
        out[f"selective_macro_f1@{coverage:.2f}"] = macro_f1(predictions[idx], labels[idx])
        out[f"actual_coverage@{coverage:.2f}"] = keep/n
    return out


def conformal_metrics(probabilities: np.ndarray, labels: np.ndarray, qhat: float, alpha: float) -> dict[str, float]:
    sets = aps_prediction_set(probabilities, qhat); sizes = sets.sum(1)
    coverage = float(np.mean(sets[np.arange(len(labels)), labels]))
    return {"nominal_coverage": 1-alpha, "empirical_coverage": coverage, "coverage_gap": 1-alpha-coverage,
            "mean_set_size": float(sizes.mean()), "median_set_size": float(np.median(sizes)),
            "singleton_fraction": float(np.mean(sizes == 1)), "empty_fraction": float(np.mean(sizes == 0))}


def compute_metric_rows(logits: np.ndarray, labels: np.ndarray, temperature: float, qhats: dict[float, float]) -> tuple[list[dict], np.ndarray]:
    raw = softmax(logits); scaled = softmax(logits / temperature); predictions = raw.argmax(1)
    rows: list[dict] = []
    for variant, probs in (("UNCALIBRATED", raw), ("SOURCE_TEMPERATURE_SCALED", scaled)):
        base = {"NLL": nll(probs, labels), "Brier": brier(probs, labels), "ECE_15_EQUAL_WIDTH": ece(probs, labels), "ADAPTIVE_ECE_15": ece(probs, labels, adaptive=True), "CLASSWISE_ECE": classwise_ece(probs, labels)}
        for metric, value in base.items(): rows.append({"probability_variant": variant, "metric": metric, "value": value})
        for score_name, score in (("PREDICTIVE_ENTROPY", entropy(probs)), ("ONE_MINUS_MAX", 1-probs.max(1))):
            error = (predictions != labels).astype(int)
            rows += [{"probability_variant": variant, "uncertainty_score": score_name, "metric": "ERROR_AUROC", "value": _rank_auc(score, error)}, {"probability_variant": variant, "uncertainty_score": score_name, "metric": "ERROR_AUPRC", "value": auprc(score, error)}]
            for metric, value in selective_rows(score, predictions, labels).items(): rows.append({"probability_variant": variant, "uncertainty_score": score_name, "metric": metric, "value": value})
    for alpha, qhat in qhats.items():
        for metric, value in conformal_metrics(raw, labels, qhat, alpha).items(): rows.append({"probability_variant": "UNCALIBRATED", "metric": f"APS_{metric}_alpha_{alpha:.2f}", "value": value})
    cm = confusion_matrix(predictions, labels)
    for metric, value in {"macro-F1": macro_f1(predictions, labels), "Cohen_kappa": kappa(predictions, labels), "balanced_accuracy": balanced_accuracy(predictions, labels)}.items(): rows.append({"probability_variant": "ARGMAX_INVARIANT", "metric": metric, "value": value})
    for c in range(CLASS_COUNT):
        den = cm[c].sum(); rows.append({"probability_variant": "ARGMAX_INVARIANT", "metric": f"recall_class_{c}", "value": float(cm[c,c]/den) if den else float("nan")})
    return rows, cm
