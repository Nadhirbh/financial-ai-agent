from __future__ import annotations

from typing import List, Dict, Tuple
from datetime import datetime, timedelta


def ema(values: List[float], window: int) -> List[float]:
    if not values:
        return []
    if window <= 1:
        return values[:]
    alpha = 2 / (window + 1)
    out: List[float] = []
    s = values[0]
    out.append(s)
    for v in values[1:]:
        s = alpha * v + (1 - alpha) * s
        out.append(s)
    return out


def ema_forecast(
    timestamps: List[datetime],
    values: List[float],
    horizon_days: int = 7,
    window: int = 14,
) -> Dict:
    if not timestamps or not values or len(timestamps) != len(values):
        return {"history": [], "forecast": [], "metrics": {}}
    smoothed = ema(values, window)
    last_ts = timestamps[-1]
    last_val = smoothed[-1]
    # naive projection: flat value for next days
    forecast: List[Tuple[datetime, float]] = []
    for i in range(1, horizon_days + 1):
        forecast.append((last_ts + timedelta(days=i), float(last_val)))
    hist = [{"ts": t.isoformat(), "value": float(v), "ema": float(s)} for t, v, s in zip(timestamps, values, smoothed)]
    fcast = [{"ts": t.isoformat(), "value": v} for t, v in forecast]
    # simple metrics: last deviation
    dev = (values[-1] - smoothed[-1]) if smoothed else 0.0
    return {
        "history": hist,
        "forecast": fcast,
        "metrics": {"last_deviation": round(float(dev), 4), "window": window},
    }


def simple_recommendation(values: List[float], smoothed: List[float]) -> Dict:
    if not values or not smoothed:
        return {"action": "neutral", "confidence": 0.0, "rationale": "insufficient data"}
    delta = values[-1] - smoothed[-1]
    # heuristic
    if delta > 0:
        act = "buy"
    elif delta < 0:
        act = "sell"
    else:
        act = "neutral"
    conf = min(0.95, max(0.05, abs(delta) / (abs(smoothed[-1]) + 1e-6)))
    return {"action": act, "confidence": round(float(conf), 3), "rationale": f"price vs EMA delta={delta:.4f}"}
