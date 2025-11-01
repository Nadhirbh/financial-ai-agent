from __future__ import annotations

from typing import Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> Dict:
    """Return VADER polarity with compound mapped to label.
    Output example: {"compound": 0.42, "neg": 0.0, "neu": 0.7, "pos": 0.3, "label": "positive"}
    """
    if not text:
        return {"compound": 0.0, "neg": 0.0, "neu": 1.0, "pos": 0.0, "label": "neutral"}
    scores = _analyzer.polarity_scores(text)
    comp = scores.get("compound", 0.0)
    if comp >= 0.05:
        label = "positive"
    elif comp <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    scores["label"] = label
    return scores
