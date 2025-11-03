from __future__ import annotations

from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_

from ...db.session import SessionLocal
from ...db.models.market_series import MarketSeries
from ...services.mcp.forecast import ema, ema_forecast, simple_recommendation


router = APIRouter(prefix="/mcp")


class ForecastRequest(BaseModel):
    ticker: str
    horizon_days: int = 7
    window: int = 14
    since_days: int = 120


@router.post("/forecast")
def forecast(req: ForecastRequest):
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=req.since_days)
        rows = db.execute(
            select(MarketSeries.ts, MarketSeries.price)
            .where(and_(MarketSeries.symbol == req.ticker, MarketSeries.ts >= cutoff))
            .order_by(MarketSeries.ts.asc())
        ).all()
        if not rows:
            raise HTTPException(status_code=404, detail="No market data for ticker")
        ts = [r[0] for r in rows]
        vals = [float(r[1]) for r in rows]
        res = ema_forecast(ts, vals, horizon_days=req.horizon_days, window=req.window)
        return {"ticker": req.ticker, **res}
    finally:
        db.close()


@router.get("/recommendation")
def recommendation(ticker: str, window: int = 14, since_days: int = 120):
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=since_days)
        rows = db.execute(
            select(MarketSeries.ts, MarketSeries.price)
            .where(and_(MarketSeries.symbol == ticker, MarketSeries.ts >= cutoff))
            .order_by(MarketSeries.ts.asc())
        ).all()
        if not rows:
            raise HTTPException(status_code=404, detail="No market data for ticker")
        vals = [float(r[1]) for r in rows]
        sm = ema(vals, window)
        rec = simple_recommendation(vals, sm)
        return {"ticker": ticker, "window": window, **rec}
    finally:
        db.close()
