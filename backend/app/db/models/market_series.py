from sqlalchemy import Column, Integer, String, Float, DateTime
from . import Base

class MarketSeries(Base):
    __tablename__ = 'market_series'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    ts = Column(DateTime)
    price = Column(Float)
    volume = Column(Float)
