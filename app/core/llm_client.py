from __future__ import annotations

from typing import Optional, List

import httpx

from app.core.config import settings
from app.core.openai_compat import (
    build_chat_completions_body,
    extract_text_from_chat_completions,
    extract_text_from_responses,
    is_gemini_openai_compatible,
)


class LLMClient:
    def __init__(self, model: str = settings.llm_model) -> None:
        self.model = model

    async def generate(
        self,
        *,
        system: str,
        user: str,
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        reasoning_effort: Optional[str] = None,
        text_verbosity: Optional[str] = None,
        timeout_s: float = 60.0,
    ) -> str:
        """
        Call an OpenAI-compatible endpoint and return output text.

        - max_output_tokens: Optional hard cap for output length. If None, do not send.
        - timeout_s: request timeout in seconds (default 60s).
        """
        base = (settings.llm_base_url or "").rstrip("/")

        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        use_chat_completions = is_gemini_openai_compatible(base_url=base, model=self.model)

        if use_chat_completions:
            url = f"{base}/chat/completions"
            body = build_chat_completions_body(
                model=self.model,
                system=system,
                user=user,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            )
        else:
            url = f"{base}/responses"
            body = {
                "model": self.model,
                "input": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }

            if max_output_tokens is not None:
                try:
                    v = int(max_output_tokens)
                    if v > 0:
                        body["max_output_tokens"] = v
                except Exception:
                    pass

            if temperature is not None:
                body["temperature"] = float(temperature)

            if reasoning_effort:
                body["reasoning"] = {"effort": str(reasoning_effort)}

            if text_verbosity:
                body["text"] = {
                    "format": {"type": "text"},
                    "verbosity": str(text_verbosity),
                }

        async with httpx.AsyncClient(timeout=timeout_s) as client:
            resp = await client.post(url, headers=headers, json=body)
            if resp.status_code >= 400:
                detail = resp.text
                raise httpx.HTTPStatusError(
                    f"{resp.status_code} error for {url}: {detail}",
                    request=resp.request,
                    response=resp,
                )
            data = resp.json()

        if use_chat_completions:
            text = extract_text_from_chat_completions(data)
            if text:
                return text
            raise ValueError(f"Empty chat completion text. Raw response: {data}")

        text = extract_text_from_responses(data)
        if text:
            return text
        raise ValueError(f"Empty response text. Raw response: {data}")
