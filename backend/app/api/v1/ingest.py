from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from ...services.etl.sources.rss import fetch_rss
from ...services.etl.sources.local_file import load_local_documents
from ...services.etl.sources.newsapi import fetch_newsapi
from ...services.etl.sources.gdelt import fetch_gdelt
from ...services.etl.sources.scraper import scrape_url
from ...services.etl.sources.twitter import fetch_tweets
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


class TweetsIngestRequest(BaseModel):
    query: str  # e.g., "(EURUSD OR EUR) (ECB OR inflation)"
    limit: Optional[int] = 50
    since: Optional[str] = None  # YYYY-MM-DD
    until: Optional[str] = None  # YYYY-MM-DD
    language: Optional[str] = "en"
    keywords: Optional[List[str]] = None


@router.post("/tweets")
def ingest_tweets(payload: TweetsIngestRequest):
    raw = fetch_tweets(
        query=payload.query,
        limit=payload.limit or 50,
        since=payload.since,
        until=payload.until,
        lang=payload.language or "en",
    )
    cleaned = preprocess_items(raw, keywords=payload.keywords or [])
    inserted = load_documents(cleaned)
    return {
        "query": payload.query,
        "fetched": len(raw),
        "cleaned": len(cleaned),
        "inserted": inserted,
    }


class NewsIngestRequest(BaseModel):
    provider: str  # 'newsapi' or 'gdelt'
    query: str
    language: Optional[str] = "en"
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    page_size: Optional[int] = 50
    keywords: Optional[List[str]] = None


@router.post("/news")
def ingest_news(payload: NewsIngestRequest):
    if payload.provider.lower() == "newsapi":
        raw = fetch_newsapi(
            query=payload.query,
            language=payload.language,
            from_date=payload.from_date,
            to_date=payload.to_date,
            page_size=payload.page_size or 50,
        )
    elif payload.provider.lower() == "gdelt":
        raw = fetch_gdelt(
            query=payload.query,
            language=payload.language,
            from_date=payload.from_date,
            to_date=payload.to_date,
            max_records=payload.page_size or 50,
        )
    else:
        return {"error": "Unsupported provider"}

    cleaned = preprocess_items(raw, keywords=payload.keywords or [])
    inserted = load_documents(cleaned)
    return {
        "provider": payload.provider,
        "query": payload.query,
        "fetched": len(raw),
        "cleaned": len(cleaned),
        "inserted": inserted,
    }


class ScrapeRequest(BaseModel):
    url: str
    keywords: Optional[List[str]] = None


@router.post("/scrape")
def ingest_scrape(payload: ScrapeRequest):
    raw_item = scrape_url(payload.url)
    cleaned = preprocess_items([raw_item], keywords=payload.keywords or [])
    inserted = load_documents(cleaned)
    return {
        "url": payload.url,
        "inserted": inserted,
    }


class LocalIngestRequest(BaseModel):
    path: str
    fmt: Optional[str] = None  # 'csv' or 'json'
    mapping: Optional[dict] = None  # {title,url,summary,content,published_at,source}
    keywords: Optional[List[str]] = None


@router.post("/local")
def ingest_local(payload: LocalIngestRequest):
    raw = load_local_documents(payload.path, fmt=payload.fmt, mapping=payload.mapping)
    cleaned = preprocess_items(raw, keywords=payload.keywords or [])
    inserted = load_documents(cleaned)
    return {
        "path": payload.path,
        "fetched": len(raw),
        "cleaned": len(cleaned),
        "inserted": inserted,
    }
