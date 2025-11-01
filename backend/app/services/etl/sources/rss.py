from typing import List, Dict
import feedparser
from bs4 import BeautifulSoup
from dateutil import parser as dateparser


def _clean_html(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(separator=" ", strip=True)


def fetch_rss(urls: List[str]) -> List[Dict]:
    items: List[Dict] = []
    for url in urls:
        feed = feedparser.parse(url)
        source_title = feed.feed.get("title", "rss") if hasattr(feed, "feed") else "rss"
        for e in feed.entries:
            link = getattr(e, "link", None)
            title = getattr(e, "title", None)
            summary = _clean_html(getattr(e, "summary", "") or getattr(e, "description", ""))
            content = summary
            published = None
            if getattr(e, "published", None):
                try:
                    published = dateparser.parse(e.published)
                except Exception:
                    published = None
            items.append(
                {
                    "source": source_title,
                    "title": title or "",
                    "url": link or "",
                    "summary": summary or "",
                    "content": content or "",
                    "published_at": published,
                }
            )
    return items
