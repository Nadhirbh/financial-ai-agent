# Placeholder event extraction

from __future__ import annotations

from typing import Dict, List, Any


KEYWORDS = {
    "merger_acquisition": [
        "merger", "acquisition", "acquire", "acquired", "acquiring", "m&a", "takeover"
    ],
    "earnings": [
        "earnings", "q1", "q2", "q3", "q4", "quarterly results", "eps", "revenue", "guidance"
    ],
    "layoffs": [
        "layoff", "layoffs", "job cuts", "reduce workforce", "redundancies"
    ],
    "partnership": [
        "partnership", "partners with", "collaboration", "strategic alliance"
    ],
}


def extract_events(text: str) -> Dict[str, Any]:
    """Return a richer schema:
    {
      "events": [
        {"type": "earnings", "triggers": ["earnings"], "confidence": 0.7,
         "actors": [], "amount": null, "date": null}
      ]
    }
    """
    if not text:
        return {"events": []}
    low = text.lower()
    events: List[Dict[str, Any]] = []
    for label, kws in KEYWORDS.items():
        hits = [kw for kw in kws if kw in low]
        if hits:
            # crude confidence: min(0.5 + 0.1*#hits, 0.95)
            conf = min(0.5 + 0.1 * len(hits), 0.95)
            events.append(
                {
                    "type": label,
                    "triggers": hits,
                    "confidence": round(conf, 2),
                    "actors": [],  # to be filled by improved extraction later
                    "amount": None,
                    "date": None,
                }
            )
    return {"events": events}
