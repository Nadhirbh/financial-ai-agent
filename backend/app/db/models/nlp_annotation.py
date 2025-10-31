from sqlalchemy import Column, Integer, ForeignKey, JSON
from . import Base

class NLPAnnotation(Base):
    __tablename__ = 'nlp_annotations'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    entities = Column(JSON)
    sentiment = Column(JSON)
    events = Column(JSON)
