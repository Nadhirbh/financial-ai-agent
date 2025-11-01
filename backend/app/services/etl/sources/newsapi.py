from __future__ import annotations

from typing import List, Dict, Optional
import os
import httpx
from dateutil import parser as dateparser

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"


def fetch_newsapi(
    query: str,
    language: Optional[str] = "en",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_size: int = 50,
) -> List[Dict]:
    """Fetch articles from NewsAPI and map to standard schema.
    Requires env NEWSAPI_API_KEY.
    """
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        return []

    params = {
        "q": query,
        "language": language or "en",
        "pageSize": min(max(page_size, 1), 100),
        "sortBy": "publishedAt",
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    headers = {"X-Api-Key": api_key}

    out: List[Dict] = []
    with httpx.Client(timeout=20) as client:
        resp = client.get(NEWSAPI_ENDPOINT, params=params, headers=headers)
        if resp.status_code != 200:
            return out
        data = resp.json()
        for a in data.get("articles", []):
            published = None
            if a.get("publishedAt"):
                try:
                    published = dateparser.parse(a["publishedAt"])  # ISO
                except Exception:
                    published = None
            out.append(
                {
                    "source": (a.get("source") or {}).get("name") or "newsapi",
                    "title": a.get("title") or "",
                    "url": a.get("url") or "",
                    "summary": a.get("description") or "",
                    "content": a.get("content") or a.get("description") or "",
                    "published_at": published,
                }
            )
    return out
