from __future__ import annotations

from typing import Any


def is_gemini_openai_compatible(*, base_url: str, model: str) -> bool:
    base = (base_url or "").lower()
    mdl = (model or "").lower()
    return "generativelanguage.googleapis.com" in base or mdl.startswith("gemini")


def build_chat_completions_body(
    *,
    model: str,
    system: str,
    user: str,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
    json_schema_name: str | None = None,
    json_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }

    if max_output_tokens is not None:
        body["max_tokens"] = int(max_output_tokens)

    if temperature is not None:
        body["temperature"] = float(temperature)

    if json_schema_name and json_schema:
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": json_schema_name,
                "schema": json_schema,
            },
        }

    return body


def extract_text_from_chat_completions(data: dict[str, Any]) -> str:
    choices = data.get("choices")
    if not isinstance(choices, list):
        return ""

    chunks: list[str] = []
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        message = choice.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if isinstance(content, str) and content.strip():
            chunks.append(content)

    return "".join(chunks).strip()


def extract_text_from_responses(data: dict[str, Any]) -> str:
    chunks: list[str] = []
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
        return "".join(chunks).strip()

    ot = data.get("output_text")
    if isinstance(ot, str) and ot.strip():
        return ot.strip()

    return ""
