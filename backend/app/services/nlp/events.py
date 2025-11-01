# Placeholder event extraction

from __future__ import annotations

from typing import Dict, List


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


def extract_events(text: str) -> Dict[str, List[str]]:
    if not text:
        return {k: [] for k in KEYWORDS}
    low = text.lower()
    out: Dict[str, List[str]] = {}
    for label, kws in KEYWORDS.items():
        hits = [kw for kw in kws if kw in low]
        out[label] = hits
    return out
