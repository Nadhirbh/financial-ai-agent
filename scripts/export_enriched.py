#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict

from backend.app.db.session import SessionLocal
from backend.app.db.models.document import Document
from backend.app.db.models.nlp_annotation import NLPAnnotation


def serialize(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def export_enriched(out_path: str) -> int:
    db = SessionLocal()
    count = 0
    try:
        # Build a map of annotations by document_id
        ann_map: Dict[int, NLPAnnotation] = {row.document_id: row for row in db.query(NLPAnnotation).all()}
        for doc in db.query(Document).all():
            ann = ann_map.get(doc.id)
            rec = {
                "doc_id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "source": doc.source,
                "published_at": doc.published_at,
                "summary": doc.summary,
                "content": doc.content,
                "entities": (ann.entities if ann else None),
                "events": (ann.events if ann else None),
                "sentiment": (ann.sentiment if ann else None),
            }
            with open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, default=serialize, ensure_ascii=False) + "\n")
            count += 1
    finally:
        db.close()
    return count


def main():
    parser = argparse.ArgumentParser(description="Export enriched dataset (documents + NLP annotations) as JSONL")
    parser.add_argument("--out", default="data/enriched/enriched.jsonl", help="Output JSONL path")
    args = parser.parse_args()

    # Ensure parent dir exists
    import os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # Truncate file if exists
    open(args.out, "w").close()

    total = export_enriched(args.out)
    print(json.dumps({"exported": total, "out": args.out}))


if __name__ == "__main__":
    main()
