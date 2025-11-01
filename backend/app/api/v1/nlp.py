from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from ...services.nlp.pipeline import run_nlp_pipeline
from ...db.session import SessionLocal
from ...db.models.nlp_annotation import NLPAnnotation

router = APIRouter(prefix="/nlp")


class RunNLPRequest(BaseModel):
    limit: int = 100
    document_ids: Optional[List[int]] = None


@router.post("/run")
def run_nlp(payload: RunNLPRequest | None = None):
    payload = payload or RunNLPRequest()
    res = run_nlp_pipeline(limit=payload.limit, document_ids=payload.document_ids)
    return res


@router.get("/doc/{doc_id}")
def get_annotation(doc_id: int):
    db = SessionLocal()
    try:
        row = db.execute(
            select(NLPAnnotation).where(NLPAnnotation.document_id == doc_id)
        ).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Annotation not found")
        return {
            "document_id": row.document_id,
            "entities": row.entities,
            "sentiment": row.sentiment,
            "events": row.events,
        }
    finally:
        db.close()
