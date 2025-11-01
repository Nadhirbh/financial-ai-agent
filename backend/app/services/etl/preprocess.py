# Placeholder preprocess module

from typing import List, Dict, Set
import unicodedata


def normalize_utf8(text: str) -> str:
    if text is None:
        return ""
    # NFC normalization and strip control chars
    t = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in t if ch >= " " or ch == "\n").strip()


def simple_topic_filter(item: Dict, keywords: List[str]) -> bool:
    blob = f"{item.get('title','')}\n{item.get('summary','')}\n{item.get('content','')}".lower()
    return any(kw.lower() in blob for kw in keywords) if keywords else True


def tokenize(text: str) -> List[str]:
    # Very simple whitespace tokenizer as a placeholder
    return [t for t in (text or "").split() if t]


def preprocess_items(items: List[Dict], keywords: List[str] | None = None) -> List[Dict]:
    # Normalize
    normalized: List[Dict] = []
    for it in items:
        it = dict(it)
        it["title"] = normalize_utf8(it.get("title", ""))
        it["summary"] = normalize_utf8(it.get("summary", ""))
        it["content"] = normalize_utf8(it.get("content", ""))
        normalized.append(it)

    # Dedupe by URL (primary) then by title
    seen_urls: Set[str] = set()
    seen_titles: Set[str] = set()
    deduped: List[Dict] = []
    for it in normalized:
        url = (it.get("url") or "").strip()
        title = (it.get("title") or "").strip().lower()
        if url and url in seen_urls:
            continue
        if not url and title and title in seen_titles:
            continue
        if url:
            seen_urls.add(url)
        elif title:
            seen_titles.add(title)
        deduped.append(it)

    # Topic filter
    if keywords:
        deduped = [it for it in deduped if simple_topic_filter(it, keywords)]

    # Add basic metadata (e.g., token count)
    for it in deduped:
        it["token_count"] = len(tokenize(it.get("content", "")))

    return deduped
