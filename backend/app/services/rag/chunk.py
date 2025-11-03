from __future__ import annotations

from typing import List
import re


def clean_text(text: str) -> str:
    if not text:
        return ""
    t = re.sub(r"\s+", " ", text)
    return t.strip()


def simple_chunks(text: str, max_words: int = 180) -> List[str]:
    t = clean_text(text)
    if not t:
        return []
    words = t.split()
    out: List[str] = []
    for i in range(0, len(words), max_words):
        out.append(" ".join(words[i : i + max_words]))
    return out
