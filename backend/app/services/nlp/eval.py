from __future__ import annotations

from typing import Dict, List, Tuple, Set


def prf(gold: Set[str], pred: Set[str]) -> Tuple[float, float, float]:
    if not gold and not pred:
        return 1.0, 1.0, 1.0
    tp = len(gold & pred)
    prec = tp / len(pred) if pred else 0.0
    rec = tp / len(gold) if gold else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
    return prec, rec, f1


def eval_ner(gold_ents: Dict[str, List[str]], pred_ents: Dict[str, List[str]]) -> Dict[str, float]:
    keys = {"tickers", "orgs", "indices", "products"}
    scores: Dict[str, float] = {}
    p_sum = r_sum = f_sum = 0.0
    n = 0
    for k in keys:
        g = set(map(str, gold_ents.get(k, [])))
        p = set(map(str, pred_ents.get(k, [])))
        p_, r_, f_ = prf(g, p)
        scores[f"{k}_precision"] = round(p_, 4)
        scores[f"{k}_recall"] = round(r_, 4)
        scores[f"{k}_f1"] = round(f_, 4)
        p_sum += p_
        r_sum += r_
        f_sum += f_
        n += 1
    if n:
        scores["macro_precision"] = round(p_sum / n, 4)
        scores["macro_recall"] = round(r_sum / n, 4)
        scores["macro_f1"] = round(f_sum / n, 4)
    return scores


def eval_sentiment(gold_label: str, pred_label: str) -> float:
    return 1.0 if (gold_label or "").lower() == (pred_label or "").lower() else 0.0


def event_coverage(gold_types: List[str], pred_types: List[str]) -> float:
    g = set(map(str, gold_types))
    p = set(map(str, pred_types))
    if not g:
        return 1.0 if not p else 0.0
    return len(g & p) / len(g)
