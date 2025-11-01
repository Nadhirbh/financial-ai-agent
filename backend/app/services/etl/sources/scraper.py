from __future__ import annotations

from typing import Dict
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def scrape_url(url: str) -> Dict:
    """Fetch a web page and extract a simple article representation.
    Heuristic: use <title> and visible text from common containers.
    """
    source = urlparse(url).netloc or "scraper"
    title = ""
    content = ""

    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            r = client.get(url)
            r.raise_for_status()
            html = r.text
    except Exception:
        return {"source": source, "title": title, "url": url, "summary": "", "content": "", "published_at": None}

    soup = BeautifulSoup(html, "lxml")
    # Title
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Try common article containers
    candidates = []
    for sel in ["article", "main", "div#content", "div.post", "div.article", "section"]:
        for node in soup.select(sel):
            text = node.get_text(separator=" ", strip=True)
            if text and len(text) > 200:  # heuristic min length
                candidates.append(text)
    if candidates:
        content = max(candidates, key=len)
    else:
        # fallback: all text
        content = soup.get_text(separator=" ", strip=True)

    # Summary as first ~40 words
    words = content.split()
    summary = " ".join(words[:40]) if words else ""

    return {
        "source": source,
        "title": title,
        "url": url,
        "summary": summary,
        "content": content,
        "published_at": None,
    }
