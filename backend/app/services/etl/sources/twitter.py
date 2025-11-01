from __future__ import annotations

from typing import List, Dict, Optional
from datetime import datetime

try:
    import snscrape.modules.twitter as sntwitter
except Exception:  # pragma: no cover
    sntwitter = None


def fetch_tweets(
    query: str,
    limit: int = 50,
    since: Optional[str] = None,  # YYYY-MM-DD
    until: Optional[str] = None,  # YYYY-MM-DD
    lang: Optional[str] = "en",
) -> List[Dict]:
    """Fetch tweets without API keys via snscrape and map to standard schema.

    - query: snscrape query (supports logical ops, e.g., "(AAPL OR Apple) (earnings)")
    - since/until: date strings (YYYY-MM-DD)
    - lang: language filter (e.g., 'en')
    """
    if sntwitter is None:
        return []

    parts = [query]
    if since:
        parts.append(f"since:{since}")
    if until:
        parts.append(f"until:{until}")
    if lang:
        parts.append(f"lang:{lang}")

    full_query = " ".join(parts)

    out: List[Dict] = []
    try:
        scraper = sntwitter.TwitterSearchScraper(full_query)
        for i, tweet in enumerate(scraper.get_items()):
            if i >= max(1, limit):
                break
            published = None
            if getattr(tweet, "date", None):
                try:
                    # tweet.date is already a datetime
                    published = tweet.date if isinstance(tweet.date, datetime) else None
                except Exception:
                    published = None
            url = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}" if getattr(tweet, "id", None) else ""
            content = tweet.content or ""
            # Basic summary as first ~30 words
            words = (content or "").split()
            summary = " ".join(words[:30]) if words else ""
            out.append(
                {
                    "source": "twitter",
                    "title": summary or (content[:80] if content else ""),
                    "url": url,
                    "summary": summary,
                    "content": content,
                    "published_at": published,
                }
            )
    except Exception:
        return out

    return out
