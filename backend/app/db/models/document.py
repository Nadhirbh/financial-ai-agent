from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint
from . import Base

class Document(Base):
    __tablename__ = 'documents'
    __table_args__ = (
        UniqueConstraint('url', name='uq_documents_url'),
    )

    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    title = Column(String(512))
    url = Column(String(1024))
    summary = Column(Text)
    content = Column(Text)
    published_at = Column(DateTime)
