from __future__ import annotations

from typing import List, Optional
import os
import httpx


class LLMClient:
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None, hf_api_token: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.hf_api_token = hf_api_token

    @classmethod
    def from_env(cls) -> "LLMClient | None":
        provider = os.getenv("LLM_PROVIDER", "openai").lower()  # 'openai' or 'hf'
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            if not api_key:
                return None
            return cls(provider="openai", model=model, api_key=api_key)
        elif provider in ("hf", "huggingface"):
            token = os.getenv("HF_API_TOKEN")
            model = os.getenv("HF_SUMMARY_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
            if not token:
                return None
            return cls(provider="hf", model=model, hf_api_token=token)
        return None

    def summarize(self, messages: List[dict], max_tokens: int = 512) -> Optional[str]:
        """messages: [{'role':'system'|'user'|'assistant', 'content':'...'}]"""
        try:
            if self.provider == "openai":
                # Use OpenAI Responses API via REST (avoid heavy SDK use)
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                }
                with httpx.Client(timeout=60) as client:
                    r = client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
                    r.raise_for_status()
                    data = r.json()
                    return data["choices"][0]["message"]["content"].strip()
            elif self.provider == "hf":
                headers = {"Authorization": f"Bearer {self.hf_api_token}", "Content-Type": "application/json"}
                prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens, "temperature": 0.3}}
                with httpx.Client(timeout=120) as client:
                    r = client.post(f"https://api-inference.huggingface.co/models/{self.model}", json=payload, headers=headers)
                    r.raise_for_status()
                    data = r.json()
                    # HF returns list of dicts with 'generated_text'
                    text = data[0].get("generated_text", "").strip()
                    return text
        except Exception:
            return None
        return None
