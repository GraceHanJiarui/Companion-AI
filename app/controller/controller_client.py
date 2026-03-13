from __future__ import annotations

import httpx
import json
from typing import Any, Dict, List

from app.core.config import settings
from app.controller.plan import Plan, Behavior, HardConstraints, MemoryPoint
from app.controller.prompts import CONTROLLER_SYSTEM


ALLOWED_INTENTS = ["chat", "ask_help", "task", "venting", "other"]


def _plan_json_schema() -> Dict[str, Any]:
    # strict schema: required 必须包含 properties 全量 key
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "intent": {"type": "string", "enum": ALLOWED_INTENTS},
            "behavior": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "E": {"type": "number"},
                    "Q_clarify": {"type": "number"},
                    "Directness": {"type": "number"},
                    "T_w": {"type": "number"},
                    "Q_aff": {"type": "number"},
                    "Initiative": {"type": "number"},
                    "Disclosure_Content": {"type": "number"},
                    "Disclosure_Style": {"type": "number"},
                },
                "required": [
                    "E",
                    "Q_clarify",
                    "Directness",
                    "T_w",
                    "Q_aff",
                    "Initiative",
                    "Disclosure_Content",
                    "Disclosure_Style",
                ],
            },
            "hard_constraints": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "mhr_required": {"type": "boolean"},
                    "boundary_keys": {"type": "array", "items": {"type": "string"}},
                    "forbidden_moves": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["mhr_required", "boundary_keys", "forbidden_moves"],
            },
            "selected_memories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "memory_id": {"type": ["integer", "null"]},
                        "preview": {"type": "string"},
                    },
                    "required": ["memory_id", "preview"],
                },
            },
            "notes": {"type": ["string", "null"]},
        },
        "required": ["intent", "behavior", "hard_constraints", "selected_memories", "notes"],
    }


def _clamp01(x: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _normalize_behavior(b: dict) -> dict:
    b = b or {}
    out = {}
    keys = ["E", "Q_clarify", "Directness", "T_w", "Q_aff", "Initiative", "Disclosure_Content", "Disclosure_Style"]
    for k in keys:
        out[k] = _clamp01(b.get(k, 0.0))
    return out


class ControllerClient:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or (getattr(settings, "controller_model", None) or settings.llm_model)
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key

    async def plan(
        self,
        *,
        user_text: str,
        policy_json: str,
        active_boundary_keys: List[str],
        memory_previews: List[dict],
        core_self_preview: str,
    ) -> Plan:
        payload = {
            "user_text": user_text,
            "policy_json": policy_json,
            "active_boundary_keys": active_boundary_keys,
            "memories": memory_previews,
            "core_self_preview": core_self_preview,
        }

        body = {
            "model": self.model,
            "input": [
                {"role": "system", "content": CONTROLLER_SYSTEM},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "plan",
                    "schema": _plan_json_schema(),
                    "strict": True,
                }
            },
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=40.0) as client:
            resp = await client.post(f"{self.base_url}/responses", headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()

        chunks: List[str] = []
        for item in data.get("output", []):
            if not isinstance(item, dict) or item.get("type") != "message":
                continue
            for c in item.get("content", []) or []:
                if isinstance(c, dict) and c.get("type") == "output_text" and isinstance(c.get("text"), str):
                    chunks.append(c["text"])
        raw = "".join(chunks).strip() if chunks else ""
        if not raw:
            raw = (data.get("output_text") or "").strip()

        obj = json.loads(raw)

        intent = obj.get("intent") if obj.get("intent") in ALLOWED_INTENTS else "chat"
        beh = _normalize_behavior(obj.get("behavior") or {})

        hc = obj.get("hard_constraints") or {}
        hard_constraints = HardConstraints(
            mhr_required=bool(hc.get("mhr_required", True)),
            boundary_keys=list(hc.get("boundary_keys") or []),
            forbidden_moves=list(hc.get("forbidden_moves") or []),
        )

        mems: List[MemoryPoint] = []
        for m in obj.get("selected_memories") or []:
            if not isinstance(m, dict):
                continue
            mems.append(
                MemoryPoint(
                    memory_id=m.get("memory_id"),
                    preview=str(m.get("preview") or "")[:500],
                )
            )

        return Plan(
            intent=intent,
            behavior=Behavior(**beh),
            hard_constraints=hard_constraints,
            selected_memories=mems,
            notes=obj.get("notes"),
        )


def fallback_plan_from_policy(policy: dict, boundary_keys: List[str]) -> Plan:
    beh = (policy or {}).get("behavior_effective") or {}
    beh = _normalize_behavior(beh)

    return Plan(
        intent="ask_help",
        behavior=Behavior(**beh),
        hard_constraints=HardConstraints(mhr_required=True, boundary_keys=boundary_keys, forbidden_moves=[]),
        selected_memories=[],
        notes="fallback_plan_from_policy",
    )
