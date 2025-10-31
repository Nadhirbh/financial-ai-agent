from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB
from . import Base

class Embedding(Base):
    __tablename__ = 'embeddings'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    model = Column(String(100))
    vector = Column(BLOB)
