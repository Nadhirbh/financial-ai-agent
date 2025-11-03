from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select

from ...services.nlp.pipeline import run_nlp_pipeline
from ...db.session import SessionLocal
from ...db.models.nlp_annotation import NLPAnnotation
from ...db.models.document import Document

router = APIRouter(prefix="/nlp")


class RunNLPRequest(BaseModel):
    limit: int = 100
    document_ids: Optional[List[int]] = None
    async_run: bool = False


@router.post("/run")
def run_nlp(payload: RunNLPRequest | None = None, background_tasks: BackgroundTasks = None):
    payload = payload or RunNLPRequest()
    if payload.async_run and background_tasks is not None:
        background_tasks.add_task(run_nlp_pipeline, limit=payload.limit, document_ids=payload.document_ids)
        return {"status": "scheduled", "limit": payload.limit, "document_ids": payload.document_ids or []}
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


@router.get("/pending")
def list_pending(limit: int = 100):
    db = SessionLocal()
    try:
        annotated_ids = {aid for (aid,) in db.query(NLPAnnotation.document_id).all()}
        ids = [d.id for d in db.query(Document.id).all() if d.id not in annotated_ids][: limit]
        return {"count": len(ids), "document_ids": ids}
    finally:
        db.close()
