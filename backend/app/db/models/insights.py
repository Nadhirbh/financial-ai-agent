from __future__ import annotations

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, JSON
from datetime import datetime, date
from . import Base


class DailySummary(Base):
    __tablename__ = "daily_summaries"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    scope = Column(String(32), default="global")  # global | company
    scope_key = Column(String(128), nullable=True)  # e.g., ticker when scope=company
    summary = Column(Text)
    sources = Column(JSON)  # list of URLs used
    model = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    scope = Column(String(32), default="company")
    scope_key = Column(String(128), nullable=True)  # e.g., ticker
    type = Column(String(64))  # sentiment_spike, volume_spike
    payload = Column(JSON)  # {delta, baseline, window, stats}
    created_at = Column(DateTime, default=datetime.utcnow)
