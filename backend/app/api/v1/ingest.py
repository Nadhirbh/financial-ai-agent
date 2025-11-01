from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from ...services.etl.sources.rss import fetch_rss
from ...services.etl.preprocess import preprocess_items
from ...services.etl.loader import load_documents


router = APIRouter(prefix="/ingest")


DEFAULT_RSS_SOURCES = [
    "https://www.investopedia.com/news/rss",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]


class IngestRequest(BaseModel):
    sources: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


@router.post("/run")
def run_ingest(payload: IngestRequest | None = None):
    sources = (payload.sources if payload and payload.sources else DEFAULT_RSS_SOURCES)
    keywords = (payload.keywords if payload and payload.keywords else [])

    raw_items = fetch_rss(sources)
    cleaned = preprocess_items(raw_items, keywords=keywords)
    inserted = load_documents(cleaned)

    return {
        "sources": sources,
        "keywords": keywords,
        "fetched": len(raw_items),
        "cleaned": len(cleaned),
        "inserted": inserted,
    }
