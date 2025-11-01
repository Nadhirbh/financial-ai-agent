from __future__ import annotations

from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select, and_

from ...db.session import SessionLocal
from ...db.models.document import Document
from ...db.models.nlp_annotation import NLPAnnotation
from ...db.models.insights import DailySummary, Alert
from ...services.insights.llm_client import LLMClient

router = APIRouter(prefix="/insights")


class SummarizeRequest(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None
    scope: str = "global"  # global | company
    tickers: Optional[List[str]] = None  # when scope=company
    max_tokens: int = 512
    async_run: bool = False


def _build_messages(scope: str, scope_key: Optional[str], items: List[Dict]) -> List[dict]:
    sys = "You are a financial analyst. Summarize key developments, risks, and market impact. Include bullet points and short takeaways."
    bullets = []
    for it in items[:15]:
        bullets.append(f"- {it.get('title','')[:140]} ({it.get('url','')})")
    user = f"Scope: {scope} {scope_key or ''}\nSources:\n" + "\n".join(bullets)
    return [{"role": "system", "content": sys}, {"role": "user", "content": user}]


def _gather_items(db, start: date, end: date, tickers: Optional[List[str]] = None) -> List[Dict]:
    rows = db.execute(
        select(Document.id, Document.title, Document.url, Document.published_at, NLPAnnotation.entities, NLPAnnotation.sentiment)
        .join(NLPAnnotation, NLPAnnotation.document_id == Document.id, isouter=True)
        .where(and_(Document.published_at >= datetime.combine(start, datetime.min.time()),
                    Document.published_at < datetime.combine(end + timedelta(days=1), datetime.min.time())))
        .order_by(Document.published_at.desc())
    ).all()
    items: List[Dict] = []
    for (doc_id, title, url, published_at, entities, sentiment) in rows:
        if tickers:
            doc_tickers = set((entities or {}).get("tickers", []))
            if not (doc_tickers & set(tickers)):
                continue
        items.append({
            "doc_id": doc_id,
            "title": title,
            "url": url,
            "published_at": published_at,
            "entities": entities or {},
            "sentiment": sentiment or {},
        })
    return items


def _persist_summary(db, day: date, scope: str, scope_key: Optional[str], text: str, sources: List[str], model: Optional[str]):
    row = DailySummary(date=day, scope=scope, scope_key=scope_key, summary=text, sources=sources, model=model)
    db.add(row)
    db.commit()
    return row.id


@router.post("/summarize")
def summarize(payload: SummarizeRequest, background_tasks: BackgroundTasks | None = None):
    start = payload.start or date.today()
    end = payload.end or start
    client = LLMClient.from_env()
    if client is None:
        raise HTTPException(status_code=400, detail="LLM provider not configured")

    def _job():
        db = SessionLocal()
        try:
            scopes: List[Dict] = []
            if payload.scope == "global":
                scopes.append({"scope": "global", "key": None, "tickers": None})
            elif payload.scope == "company":
                tickers = payload.tickers or []
                for t in tickers:
                    scopes.append({"scope": "company", "key": t, "tickers": [t]})

            for s in scopes:
                items = _gather_items(db, start, end, tickers=s["tickers"])[:100]
                if not items:
                    continue
                messages = _build_messages(s["scope"], s["key"], items)
                text = client.summarize(messages, max_tokens=payload.max_tokens) or ""
                sources = [it["url"] for it in items[:20] if it.get("url")]
                _persist_summary(db, start, s["scope"], s["key"], text, sources, client.model)
        finally:
            db.close()

    if payload.async_run and background_tasks is not None:
        background_tasks.add_task(_job)
        return {"status": "scheduled", "start": str(start), "end": str(end)}
    _job()
    return {"status": "done", "start": str(start), "end": str(end)}


@router.get("/trends")
def trends(scope: str = "company", key: Optional[str] = None, window: int = 30):
    db = SessionLocal()
    try:
        def s_to_score(lbl: Optional[str]) -> float:
            m = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
            return m.get((lbl or "").lower(), 0.0)

        since = datetime.utcnow() - timedelta(days=window)
        rows = db.execute(
            select(Document.published_at, NLPAnnotation.sentiment, NLPAnnotation.entities)
            .join(NLPAnnotation, NLPAnnotation.document_id == Document.id)
            .where(Document.published_at >= since)
        ).all()

        daily: Dict[str, List[float]] = {}
        volume: Dict[str, int] = {}
        for (ts, sentiment, entities) in rows:
            if scope == "company" and key:
                if key not in set((entities or {}).get("tickers", [])):
                    continue
            d = (ts.date() if isinstance(ts, datetime) else ts).isoformat()
            daily.setdefault(d, []).append(s_to_score((sentiment or {}).get("label")))
            volume[d] = volume.get(d, 0) + 1

        trend = [
            {"date": d, "sentiment_avg": (sum(vals) / len(vals) if vals else 0.0), "volume": volume.get(d, 0)}
            for d, vals in sorted(daily.items())
        ]
        return {"scope": scope, "key": key, "window": window, "series": trend}
    finally:
        db.close()


@router.get("/alerts")
def alerts(scope: str = "company", key: Optional[str] = None, lookback: int = 14, threshold: float = 0.25):
    db = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(days=lookback)
        rows = db.execute(
            select(Document.published_at, NLPAnnotation.sentiment, NLPAnnotation.entities)
            .join(NLPAnnotation, NLPAnnotation.document_id == Document.id)
            .where(Document.published_at >= since)
        ).all()

        def s_to_score(lbl: Optional[str]) -> float:
            m = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
            return m.get((lbl or "").lower(), 0.0)

        by_day: Dict[str, List[float]] = {}
        for (ts, sentiment, entities) in rows:
            if scope == "company" and key:
                if key not in set((entities or {}).get("tickers", [])):
                    continue
            d = (ts.date() if isinstance(ts, datetime) else ts).isoformat()
            by_day.setdefault(d, []).append(s_to_score((sentiment or {}).get("label")))

        days = sorted(by_day.keys())
        if len(days) < 3:
            return {"alerts": []}
        last = days[-1]
        prev = days[:-1]
        last_avg = sum(by_day[last]) / len(by_day[last]) if by_day[last] else 0.0
        baseline = sum(sum(by_day[d]) / len(by_day[d]) for d in prev) / len(prev)
        delta = last_avg - baseline
        out: List[Dict] = []
        if abs(delta) >= threshold:
            payload = {
                "delta": round(delta, 3),
                "baseline": round(baseline, 3),
                "last": round(last_avg, 3),
                "days": len(days),
                "threshold": threshold,
            }
            row = Alert(date=datetime.fromisoformat(last).date(), scope=scope, scope_key=key, type="sentiment_spike", payload=payload)
            db.add(row)
            db.commit()
            out.append({"type": "sentiment_spike", "date": last, "payload": payload})
        return {"alerts": out}
    finally:
        db.close()
