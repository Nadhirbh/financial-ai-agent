from __future__ import annotations

from typing import Dict, List, Set
import re


TICKER_RE = re.compile(r"\b[A-Z]{2,5}\b")
CURRENCY_PAIR_RE = re.compile(r"\b[A-Z]{3}/[A-Z]{3}\b")

ORG_SUFFIXES = (
    "Inc", "Inc.", "Corp", "Corp.", "Corporation", "Ltd", "Ltd.", "PLC", "LLC",
)

INDEX_KEYWORDS = {
    "S&P 500": {"spx", "s&p 500", "s&p500", "sp500"},
    "Dow Jones": {"dow jones", "djia", "dow"},
    "Nasdaq": {"nasdaq", "ndx"},
}


def extract_entities(text: str) -> Dict[str, List[str]]:
    if not text:
        return {"tickers": [], "orgs": [], "indices": [], "products": []}

    s = text
    tickers: Set[str] = set(TICKER_RE.findall(s))
    # Heuristic: remove common words mistaken as tickers
    for bad in {"AND", "FOR", "THE", "WITH", "WAS", "HAS", "WILL"}:
        tickers.discard(bad)

    products: Set[str] = set(CURRENCY_PAIR_RE.findall(s))

    # Organizations: capitalized sequences possibly ending with a known suffix
    orgs: Set[str] = set()
    for m in re.finditer(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z&]+){0,3})(?:\s+(?:" + "|".join(ORG_SUFFIXES) + "))?\b", s):
        cand = m.group(0).strip()
        if len(cand.split()) >= 1 and len(cand) >= 3:
            # Filter out obvious false positives
            if cand.lower() in {"the", "and", "for", "in", "on", "at"}:
                continue
            orgs.add(cand)

    # Indices by keyword presence
    indices: Set[str] = set()
    low = s.lower()
    for label, kws in INDEX_KEYWORDS.items():
        if any(k in low for k in kws):
            indices.add(label)

    return {
        "tickers": sorted(tickers),
        "orgs": sorted(orgs),
        "indices": sorted(indices),
        "products": sorted(products),
    }
