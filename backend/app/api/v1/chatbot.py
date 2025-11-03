from __future__ import annotations

from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from ...db.session import SessionLocal
from ...db.models.embedding import Embedding
from ...db.models.document import Document
from ...services.rag.embeddings import from_bytes, cosine
from ...services.insights.llm_client import LLMClient


router = APIRouter(prefix="/chat")


class ChatRequest(BaseModel):
    message: str
    top_k: int = 4
    days: int = 30
    tickers: Optional[List[str]] = None


class ChatResponse(BaseModel):
    reply: str
    sources: List[Dict]


def _retrieve(db, qvec: List[float], top_k: int, days: int, tickers: Optional[List[str]]):
    # MVP: read embeddings and score in memory; for large data, switch to pgvector
    rows = db.execute(select(Embedding.id, Embedding.vector, Embedding.document_id, Embedding.content)).all()
    q = from_bytes(bytes(bytearray()) + b"".join([]))  # placeholder to keep types
    import numpy as np
    q = np.asarray(qvec, dtype=np.float32)
    scored = []
    for (_id, vec_b, doc_id, content) in rows:
        v = from_bytes(vec_b)
        if v.size != q.size:
            continue
        s = cosine(q, v)
        scored.append((s, doc_id, content))
    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:top_k]
    doc_ids = [d for _, d, _ in top]
    docs = {d.id: d for d in db.query(Document).filter(Document.id.in_(doc_ids)).all()}
    out = []
    for s, did, content in top:
        d = docs.get(did)
        if not d:
            continue
        out.append({"score": float(s), "title": d.title, "url": d.url, "content": content})
    return out


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    client = LLMClient.from_env()
    if client is None:
        raise HTTPException(status_code=400, detail="LLM provider not configured")

    # Embed question with the same embedding model used for index
    from ...services.rag.embeddings import embed_texts
    import numpy as np

    qvec = embed_texts([req.message])[0]

    db = SessionLocal()
    try:
        ctx = _retrieve(db, qvec.tolist(), req.top_k, req.days, req.tickers)
    finally:
        db.close()

    bullets = []
    for c in ctx:
        bullets.append(f"- {c['title']}: {c['url']}")
    system = "You are a financial assistant. Answer concisely with bullet points and cite sources."
    user = f"Question: {req.message}\nContext:\n" + "\n".join(bullets)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    ans = client.summarize(messages, max_tokens=400) or ""
    return ChatResponse(reply=ans, sources=ctx)
