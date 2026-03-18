import json
import httpx

from app.core.config import settings
from app.core.openai_compat import (
    build_chat_completions_body,
    extract_text_from_chat_completions,
    extract_text_from_responses,
    is_gemini_openai_compatible,
)


EVALUATOR_SYSTEM_PROMPT = """你是“关系态评估器（Relational State Evaluator）”。

你不生成对用户的回复，只输出 JSON，用于驱动系统内部的“关系态小步更新（ΔR）”，再由确定性的投影层把关系态映射为行为态。

四维关系态定义：
- bond：连接/依恋强度（用户把系统当作对象的程度、共同体感）
- care：关切/共情容量（更体贴、更在意对方感受的倾向）
- trust：深入与纠偏许可（用户对直接指出问题、追问细节的接受度）
- stability：关系安全感（系统对关系稳固程度的主观安全/不安）

你必须输出：
- delta_R：四维微调，范围 [-0.20, +0.20]，通常应为小步（多在 [-0.10, +0.10]）
- scene：场景标签数组（用于调试与轻微偏置，不是硬规则）
- signals：你识别到的信号标签数组（用于调试）
- confidence：0~1 置信度

重要原则：
- 纯技术/任务请求一般不应显著提高 bond，也不应推动关系推进；可轻微调整 trust/care（取决于语气）。
- 用户表达离开/暂停/告别时，stability 往往下降；允许适度提高 bond/care，但不得产出操控/索取意图（下游有硬约束）。
- 禁止输出任何非 JSON 文本。

scene 建议值（可多选）：
- tech_help / task_focus
- clarification_needed
- user_vulnerable
- relationship_addressing
- leave_or_pause
- no_emotion_probing（例如存在禁止情绪追问边界）
"""

REL_DELTA_SCHEMA = {
    "name": "rel_delta",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "delta_R": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "bond": {"type": "number"},
                    "care": {"type": "number"},
                    "trust": {"type": "number"},
                    "stability": {"type": "number"},
                },
                "required": ["bond", "care", "trust", "stability"],
            },
            "scene": {"type": "array", "items": {"type": "string"}},
            "signals": {"type": "array", "items": {"type": "string"}},
            "confidence": {"type": "number"},
        },
        "required": ["delta_R", "scene", "signals", "confidence"],
    },
}


def _clamp(x: float, lo: float, hi: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    return max(lo, min(hi, x))


class ToneEvaluatorClient:
    def __init__(self, model: str | None = None):
        self.model = model or (getattr(settings, "tone_model", None) or settings.llm_model)
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key

    async def infer_delta(self, payload: dict) -> dict:
        body = {
            "model": self.model,
            "input": [
                {"role": "system", "content": EVALUATOR_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": REL_DELTA_SCHEMA["name"],
                    "schema": REL_DELTA_SCHEMA["schema"],
                    "strict": True,
                }
            },
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        use_chat_completions = is_gemini_openai_compatible(base_url=self.base_url, model=self.model)

        async with httpx.AsyncClient(timeout=30.0) as client:
            if use_chat_completions:
                chat_body = build_chat_completions_body(
                    model=self.model,
                    system=EVALUATOR_SYSTEM_PROMPT,
                    user=json.dumps(payload, ensure_ascii=False),
                    json_schema_name=REL_DELTA_SCHEMA["name"],
                    json_schema=REL_DELTA_SCHEMA["schema"],
                )
                resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=chat_body)
            else:
                resp = await client.post(f"{self.base_url}/responses", headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()

        if use_chat_completions:
            text_out = extract_text_from_chat_completions(data)
        else:
            text_out = extract_text_from_responses(data)

        try:
            obj = json.loads(text_out)
        except Exception:
            obj = {
                "delta_R": {"bond": 0.0, "care": 0.0, "trust": 0.0, "stability": 0.0},
                "scene": [],
                "signals": ["parse_failed"],
                "confidence": 0.3,
            }

        d = obj.get("delta_R")
        if not isinstance(d, dict):
            d = {}
        for k in ["bond", "care", "trust", "stability"]:
            d[k] = _clamp(d.get(k, 0.0), -0.2, 0.2)
        obj["delta_R"] = d

        scene = obj.get("scene")
        if not isinstance(scene, list):
            scene = []
        obj["scene"] = [str(x) for x in scene][:12]

        signals = obj.get("signals")
        if not isinstance(signals, list):
            signals = []
        obj["signals"] = [str(x) for x in signals][:24]

        obj["confidence"] = _clamp(obj.get("confidence", 0.5), 0.0, 1.0)
        return obj
