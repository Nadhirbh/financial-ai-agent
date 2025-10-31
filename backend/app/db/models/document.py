from sqlalchemy import Column, Integer, String, DateTime, Text
from . import Base

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    title = Column(String(512))
    content = Column(Text)
    published_at = Column(DateTime)
