from __future__ import annotations

from typing import List, Optional, Dict
from sqlalchemy import select

from ...db.session import SessionLocal
from ...db.models.document import Document
from ...db.models.nlp_annotation import NLPAnnotation
from .ner import extract_entities
from .events import extract_events
from .sentiment import analyze_sentiment


def annotate_text(text: str) -> Dict:
    entities = extract_entities(text)
    events = extract_events(text)
    sentiment = analyze_sentiment(text)
    return {"entities": entities, "events": events, "sentiment": sentiment}


def run_nlp_pipeline(limit: int = 100, document_ids: Optional[List[int]] = None) -> Dict:
    """Annotate documents and persist results.

    - If document_ids provided, only process those
    - Else, process up to `limit` documents without existing annotation
    """
    db = SessionLocal()
    processed = 0
    created = 0
    try:
        if document_ids:
            docs = db.execute(
                select(Document).where(Document.id.in_(document_ids))
            ).scalars().all()
        else:
            # select docs with no NLPAnnotation yet (simple heuristic)
            annotated_ids = {aid for (aid,) in db.query(NLPAnnotation.document_id).all()}
            q = db.execute(select(Document)).scalars()
            docs = [d for d in q if d.id not in annotated_ids][:limit]

        for doc in docs:
            text = (doc.content or doc.summary or doc.title or "").strip()
            ann = annotate_text(text)
            row = NLPAnnotation(
                document_id=doc.id,
                entities=ann["entities"],
                sentiment=ann["sentiment"],
                events=ann["events"],
            )
            db.add(row)
            db.commit()
            created += 1
            processed += 1
    finally:
        db.close()

    return {"processed": processed, "created": created}
