from __future__ import annotations

from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from ...db.session import SessionLocal
from ...db.models.document import Document
from ...db.models.embedding import Embedding
from ...services.rag.chunk import simple_chunks
from ...services.rag.embeddings import embed_texts, to_bytes


router = APIRouter(prefix="/rag")


class IndexRequest(BaseModel):
    limit: int = 200
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    document_ids: Optional[List[int]] = None


@router.post("/index")
def index_docs(payload: IndexRequest):
    db = SessionLocal()
    created = 0
    processed = 0
    try:
        if payload.document_ids:
            docs = db.execute(select(Document).where(Document.id.in_(payload.document_ids))).scalars().all()
        else:
            docs = db.execute(select(Document).order_by(Document.id.desc())).scalars().all()[: payload.limit]

        for d in docs:
            processed += 1
            text = (d.content or d.summary or d.title or "").strip()
            chunks = simple_chunks(text)
            if not chunks:
                continue
            vecs = embed_texts(chunks, model_name=payload.model)
            for chunk_text, vec in zip(chunks, vecs):
                row = Embedding(document_id=d.id, model=payload.model, vector=to_bytes(vec), content=chunk_text)
                db.add(row)
                created += 1
            db.commit()
    finally:
        db.close()
    return {"processed": processed, "created": created, "model": payload.model}
