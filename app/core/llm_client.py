from __future__ import annotations

from typing import Optional, List

import httpx

from app.core.config import settings


class LLMClient:
    def __init__(self, model: str = settings.llm_model) -> None:
        self.model = model

    async def generate(
        self,
        *,
        system: str,
        user: str,
        max_output_tokens: Optional[int] = None,
        timeout_s: float = 60.0,
    ) -> str:
        """
        Call OpenAI-compatible /responses endpoint and return concatenated output_text.

        - max_output_tokens: Optional hard cap for output length. If None, do not send.
        - timeout_s: request timeout in seconds (default 60s).
        """
        base = (settings.llm_base_url or "").rstrip("/")
        url = f"{base}/responses"

        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }

        # Only attach if caller explicitly uses it (capability-only; no policy here).
        if max_output_tokens is not None:
            # Guard against invalid values silently (caller error shouldn't crash service)
            try:
                v = int(max_output_tokens)
                if v > 0:
                    body["max_output_tokens"] = v
            except Exception:
                pass

        async with httpx.AsyncClient(timeout=timeout_s) as client:
            resp = await client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()

        # Parse Responses API:
        # data["output"] is a list containing "message" items; message["content"] includes output_text parts.
        chunks: List[str] = []
        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            if item.get("type") != "message":
                continue

            content = item.get("content", [])
            if not isinstance(content, list):
                continue

            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "output_text" and isinstance(c.get("text"), str):
                    chunks.append(c["text"])

        if chunks:
            return "".join(chunks)

        # Fallback: some servers may provide output_text at top-level
        ot = data.get("output_text")
        if isinstance(ot, str) and ot.strip():
            return ot

        return ""
