from __future__ import annotations

from typing import Dict
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_vader = SentimentIntensityAnalyzer()
_finbert_pipeline = None  # lazy


def _get_finbert():
    global _finbert_pipeline
    if _finbert_pipeline is not None:
        return _finbert_pipeline
    model_name = os.getenv("FIN_SENTIMENT_MODEL", "")  # e.g., "ProsusAI/finbert"
    if not model_name:
        return None
    try:
        from transformers import pipeline  # type: ignore

        _finbert_pipeline = pipeline(
            "text-classification", model=model_name, tokenizer=model_name, truncation=True
        )
        return _finbert_pipeline
    except Exception:
        return None


def _analyze_vader(text: str) -> Dict:
    if not text:
        return {"compound": 0.0, "neg": 0.0, "neu": 1.0, "pos": 0.0, "label": "neutral"}
    scores = _vader.polarity_scores(text)
    comp = scores.get("compound", 0.0)
    if comp >= 0.05:
        label = "positive"
    elif comp <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    scores["label"] = label
    return scores


def _analyze_finbert(text: str) -> Dict | None:
    clf = _get_finbert()
    if clf is None:
        return None
    try:
        res = clf(text, top_k=None)
        # transformers pipeline returns list of dicts with label/score
        if isinstance(res, list) and res:
            # Choose max score label
            best = max(res, key=lambda x: x.get("score", 0.0))
            label = best.get("label", "neutral").lower()
            # Map to pos/neu/neg; FinBERT labels often: "positive", "neutral", "negative"
            return {"compound": best.get("score", 0.0), "neg": 0.0, "neu": 0.0, "pos": 0.0, "label": label}
    except Exception:
        return None
    return None


def analyze_sentiment(text: str) -> Dict:
    # Try FinBERT if configured and available, else fallback to VADER
    if text:
        fb = _analyze_finbert(text)
        if fb is not None:
            return fb
    return _analyze_vader(text)
