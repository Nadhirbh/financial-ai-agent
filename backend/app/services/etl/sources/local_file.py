from __future__ import annotations

from typing import Dict, Iterable, List, Optional
import csv
import json
import os
from dateutil import parser as dateparser

# Heuristic keys mapping commonly found in news datasets
DEFAULT_CANDIDATES: Dict[str, List[str]] = {
    "title": ["title", "headline", "news_title", "Title"],
    "url": ["url", "link", "article_url", "Url", "Link"],
    "summary": ["summary", "description", "abstract", "Summary", "Description"],
    "content": ["content", "body", "text", "article", "Content", "Body", "Text"],
    "published_at": ["date", "published", "published_at", "pubDate", "time", "Date"],
    "source": ["source", "publisher", "site", "Source", "Publisher", "Site"],
}


def _pick(d: Dict, keys: List[str]) -> Optional[str]:
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None


def _parse_date(val: Optional[str]):
    if not val:
        return None
    try:
        return dateparser.parse(str(val))
    except Exception:
        return None


def _map_record(rec: Dict, mapping: Optional[Dict[str, str]] = None) -> Dict:
    if mapping:
        title = rec.get(mapping.get("title", ""))
        url = rec.get(mapping.get("url", ""))
        summary = rec.get(mapping.get("summary", ""))
        content = rec.get(mapping.get("content", ""))
        published_at = _parse_date(rec.get(mapping.get("published_at", "")))
        source = rec.get(mapping.get("source", ""))
    else:
        title = _pick(rec, DEFAULT_CANDIDATES["title"]) or ""
        url = _pick(rec, DEFAULT_CANDIDATES["url"]) or ""
        summary = _pick(rec, DEFAULT_CANDIDATES["summary"]) or ""
        content = _pick(rec, DEFAULT_CANDIDATES["content"]) or summary or ""
        published_at = _parse_date(_pick(rec, DEFAULT_CANDIDATES["published_at"]))
        source = _pick(rec, DEFAULT_CANDIDATES["source"]) or "local"

    return {
        "title": str(title) if title is not None else "",
        "url": str(url) if url is not None else "",
        "summary": str(summary) if summary is not None else "",
        "content": str(content) if content is not None else "",
        "published_at": published_at,
        "source": str(source) if source is not None else "local",
    }


def _iter_csv(path: str) -> Iterable[Dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def _iter_json(path: str) -> Iterable[Dict]:
    # Supports both array JSON and JSON Lines
    with open(path, encoding="utf-8", errors="ignore") as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == "[":
            data = json.load(f)
            for obj in data:
                if isinstance(obj, dict):
                    yield obj
        else:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        yield obj
                except Exception:
                    continue


def load_local_documents(
    path: str,
    fmt: Optional[str] = None,
    mapping: Optional[Dict[str, str]] = None,
) -> List[Dict]:
    """Read local file(s) and map to standardized document records.

    path: file path (.csv or .json/.jsonl). If directory, scans for supported files.
    fmt: optional explicit format: 'csv' or 'json'
    mapping: optional dict mapping {title,url,summary,content,published_at,source} -> column name
    """
    paths: List[str] = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                if name.lower().endswith((".csv", ".json", ".jsonl")):
                    paths.append(os.path.join(root, name))
    else:
        paths.append(path)

    out: List[Dict] = []
    for p in paths:
        ext = fmt or os.path.splitext(p)[1].lower().lstrip(".")
        if ext in ("csv",):
            it = _iter_csv(p)
        elif ext in ("json", "jsonl"):
            it = _iter_json(p)
        else:
            # skip unsupported
            continue
        for rec in it:
            out.append(_map_record(rec, mapping))

    return out
