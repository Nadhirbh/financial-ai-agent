from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from ...db.session import SessionLocal
from ...db.models.document import Document


def load_documents(items: List[Dict]) -> int:
    """Persist items into the documents table.
    Returns number of successfully inserted rows (duplicates skipped).
    """
    inserted = 0
    db = SessionLocal()
    try:
        for it in items:
            doc = Document(
                source=it.get("source"),
                title=it.get("title"),
                url=it.get("url"),
                summary=it.get("summary"),
                content=it.get("content"),
                published_at=it.get("published_at"),
            )
            db.add(doc)
            try:
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()  # duplicate URL or other constraint -> skip
    finally:
        db.close()
    return inserted
