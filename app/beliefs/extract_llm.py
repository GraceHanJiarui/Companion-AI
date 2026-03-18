from __future__ import annotations

import os
import json
import httpx
from pydantic import ValidationError

from app.beliefs.schema import ExtractorOutput
from app.core.config import settings
from app.core.openai_compat import (
    build_chat_completions_body,
    extract_text_from_chat_completions,
    extract_text_from_responses,
    is_gemini_openai_compatible,
)

EXTRACTOR_SYSTEM = """你是一个“关系与边界”的结构化抽取器。
你只做一件事：判断用户这句话是否在表达需要我更新的“边界/偏好/相处风格/关系取向”，并输出结构化结果。
重要约束：
- 不要心理咨询、不要建议、不要安慰，只做抽取。
- evidence_span 必须是 user_text 的原文子串（逐字包含）。
- 如果不确定是否要更新：should_update=false，并把 beliefs 留空。
"""

# 最小：我们先不让 extractor 直接改 policy（Milestone 6 再做连续化）
# 所以 schema 里只输出 beliefs。

# JSON Schema（尽量用常见关键词，避免复杂 unsupported 关键字）
EXTRACTOR_JSON_SCHEMA = {
    "name": "belief_extractor",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "should_update": {"type": "boolean"},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "beliefs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "kind": {"type": "string", "enum": ["boundary", "preference", "style", "relationship"]},
                        "key": {"type": ["string", "null"]},          # 允许 null
                        "value": {"type": "string"},
                        "strength": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                        "evidence_span": {"type": "string"},
                    },
                    # 关键：strict 要求 required 覆盖 properties 的全部 key
                    "required": ["kind", "key", "value", "strength", "evidence_span"],
                },
            },
            "notes": {"type": ["string", "null"]},
        },
        "required": ["should_update", "confidence", "beliefs", "notes"],
    },
    "strict": True,
}


async def extract_beliefs_llm(
    *,
    model: str,
    user_text: str,
    active_beliefs_text: str,
    policy_json: str,
    timeout_s: float = 30.0,
) -> ExtractorOutput:
    api_key = settings.llm_api_key
    if not api_key:
        raise RuntimeError("LLM_API_KEY is not set (settings.llm_api_key empty)")

    base_url = settings.llm_base_url.rstrip("/")
    use_chat_completions = is_gemini_openai_compatible(base_url=base_url, model=model)
    url = f"{base_url}/chat/completions" if use_chat_completions else f"{base_url}/responses"

    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": EXTRACTOR_SYSTEM},
            {
                "role": "user",
                "content": (
                    "user_text:\n"
                    f"{user_text}\n\n"
                    "active_beliefs (summary):\n"
                    f"{active_beliefs_text}\n\n"
                    "policy_json:\n"
                    f"{policy_json}\n"
                ),
            },
        ],
        # Responses Structured Outputs: use text.format json_schema
        "text": {
            "format": {
                "type": "json_schema",
                "strict": True,
                "schema": EXTRACTOR_JSON_SCHEMA["schema"],
                "name": EXTRACTOR_JSON_SCHEMA["name"],
            }
        },
        # 对 GPT-5-nano：不要显式传 temperature（你之前已踩到 400）
    }

    async with httpx.AsyncClient(timeout=timeout_s) as client:
        if use_chat_completions:
            body = build_chat_completions_body(
                model=model,
                system=EXTRACTOR_SYSTEM,
                user=(
                    "user_text:\n"
                    f"{user_text}\n\n"
                    "active_beliefs (summary):\n"
                    f"{active_beliefs_text}\n\n"
                    "policy_json:\n"
                    f"{policy_json}\n"
                ),
                json_schema_name=EXTRACTOR_JSON_SCHEMA["name"],
                json_schema=EXTRACTOR_JSON_SCHEMA["schema"],
            )
        else:
            body = payload
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=body,
        )
        data = resp.json()
        if resp.status_code >= 400:
            raise RuntimeError(f"OpenAI Responses error {resp.status_code}: {data}")

    if use_chat_completions:
        out_text = extract_text_from_chat_completions(data)
    else:
        out_text = extract_text_from_responses(data)
    if not out_text:
        raise RuntimeError(f"Extractor: missing output_text in response: {data}")

    try:
        obj = json.loads(out_text)
        return ExtractorOutput.model_validate(obj), out_text
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Extractor output not valid JSON/schema: {e}; raw={out_text}")
