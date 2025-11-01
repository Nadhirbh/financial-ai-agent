from __future__ import annotations

from typing import List, Dict, Optional
import httpx
from dateutil import parser as dateparser

# GDELT Doc API v2
# Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
GDELT_DOC_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_gdelt(
    query: str,
    language: Optional[str] = "en",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    max_records: int = 50,
) -> List[Dict]:
    """Fetch articles via GDELT Doc API and map to standard schema.
    Dates should be ISO like '2024-01-01'. GDELT may ignore language for some sources.
    """
    params = {
        "query": query,
        "format": "json",
        "maxrecords": max(1, min(max_records, 250)),
        "sort": "datedesc",
    }
    if from_date:
        params["startdatetime"] = from_date
    if to_date:
        params["enddatetime"] = to_date
    if language:
        params["sourcelang"] = language

    out: List[Dict] = []
    with httpx.Client(timeout=20) as client:
        resp = client.get(GDELT_DOC_ENDPOINT, params=params)
        if resp.status_code != 200:
            return out
        data = resp.json()
        for a in data.get("articles", []):
            published = None
            if a.get("seendate"):
                try:
                    published = dateparser.parse(a["seendate"])  # e.g., 2024-05-10T12:34:56Z
                except Exception:
                    published = None
            out.append(
                {
                    "source": a.get("sourcecountry") or a.get("domain") or "gdelt",
                    "title": a.get("title") or "",
                    "url": a.get("url") or "",
                    "summary": a.get("snippet") or "",
                    "content": a.get("snippet") or "",
                    "published_at": published,
                }
            )
    return out
