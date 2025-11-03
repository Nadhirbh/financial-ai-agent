from __future__ import annotations

from typing import List, Optional
import os
import numpy as np
import httpx


def embed_texts(texts: List[str], model_name: str = "text-embedding-3-small") -> np.ndarray:
    """Return numpy array of shape (n, d) using OpenAI Embeddings API.
    Requires OPENAI_API_KEY. model_name defaults to text-embedding-3-small.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set for embeddings")
    # OpenAI embeddings endpoint
    url = "https://api.openai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model_name, "input": texts}
    with httpx.Client(timeout=60) as client:
        r = client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        vecs = [np.array(item["embedding"], dtype=np.float32) for item in data.get("data", [])]
    # stack
    if not vecs:
        return np.zeros((0, 0), dtype=np.float32)
    return np.vstack(vecs)


def to_bytes(vec: np.ndarray) -> bytes:
    return vec.astype(np.float32).tobytes()


def from_bytes(b: bytes, dim: Optional[int] = None) -> np.ndarray:
    arr = np.frombuffer(b, dtype=np.float32)
    if dim and arr.size != dim:
        # allow reshape if needed later
        pass
    return arr


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        # try to broadcast if needed (should not happen in our flow)
        pass
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-12
    return float(np.dot(a, b) / denom)

