# Placeholder preprocess module

from typing import List, Dict, Set
import unicodedata
import re


def normalize_utf8(text: str) -> str:
    if text is None:
        return ""
    # NFC normalization
    t = unicodedata.normalize("NFC", text)

    # Known zero-width and BOM chars to convert to a space (per tests expectation)
    ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\ufeff"}

    out_chars: List[str] = []
    for ch in t:
        # Convert zero-width characters to a normal space
        if ch in ZERO_WIDTH:
            out_chars.append(" ")
            continue
        cat = unicodedata.category(ch)
        # Preserve newline explicitly
        if ch == "\n":
            out_chars.append(ch)
            continue
        # Convert any unicode space separators or NBSP to regular space
        if cat == "Zs" or ch in ("\u00A0", "\u2007", "\u202F"):
            out_chars.append(" ")
            continue
        # Drop other control/format characters (categories starting with 'C')
        if cat.startswith("C"):
            continue
        out_chars.append(ch)

    s = "".join(out_chars)
    # Collapse multiple spaces but preserve newlines
    s = re.sub(r"[ \t\x0b\x0c\r]+", " ", s)
    # Trim spaces around lines
    s = "\n".join(part.strip() for part in s.splitlines()).strip()
    return s


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
