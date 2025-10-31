from sqlalchemy import Column, Integer, String, DateTime, Float
from . import Base

class MCPForecast(Base):
    __tablename__ = 'mcp_forecasts'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    ts = Column(DateTime)
    horizon = Column(String(20))
    forecast = Column(Float)
    confidence = Column(Float)
