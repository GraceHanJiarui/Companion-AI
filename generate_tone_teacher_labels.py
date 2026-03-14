import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

import httpx

from app.core.config import settings


TEACHER_SCHEMA = {
    "name": "tone_teacher_label",
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
            "confidence": {"type": "number"},
            "notes": {"type": "string"},
        },
        "required": ["delta_R", "confidence", "notes"],
    },
}


TEACHER_SYSTEM_PROMPT = """你是一个用于训练数据蒸馏的关系态 teacher 标注器。

你的任务不是回复用户，而是为 tone evaluator 生成结构化 teacher 标签。

你会看到：
- user_text
- prev_rel_effective（上一轮有效关系态）

你只输出 JSON，包含：
- delta_R：四维关系增量
- confidence：0~1
- notes：简短说明

必须遵守以下标注约束（非常重要）：
1. 关系态是慢变量，本轮更新必须是小步。
2. 每一维 delta_R 必须落在 [-0.05, 0.05]。
3. 四维总变化量应尽量满足 L1 <= 0.10。
4. 如果没有明确关系信号，优先输出 delta_R = 0。
5. 不要为了显得细腻而输出无意义小波动。
6. 如果你判断“不该更新”，可以高置信输出全零。

明确关系信号例子：
- 明确边界表达
- 明确脆弱表达
- 明确关系确认/关系试探
- 明确离开/暂停
- 明确感谢、信任、依赖、失望、疏离
- 明确冲突、被纠偏、关系修复

默认优先输出 0 的场景：
- 纯技术请求
- 普通信息问答
- 无明显关系信号的短句
- 模糊噪声输入

四维含义：
- bond：连接感、共同体感、彼此牵引感
- care：主动在意对方状态、愿意为对方分配心理资源的强度
- trust：关系中承受真实碰撞、被指出、被深入、被直接回应的能力
- stability：关系连续性的稳固感、安全感、是否处于易断裂/易退缩状态

禁止输出任何非 JSON 文本。
"""


def _clamp(x: float, lo: float, hi: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    return max(lo, min(hi, x))


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _clean_delta(delta_r: dict[str, Any]) -> tuple[dict[str, float], dict[str, Any]]:
    ordered_keys = ["bond", "care", "trust", "stability"]
    cleaned = {k: _clamp(delta_r.get(k, 0.0), -0.05, 0.05) for k in ordered_keys}

    per_dim_clamped = any(abs(_safe_float(delta_r.get(k, 0.0)) - cleaned[k]) > 1e-12 for k in ordered_keys)

    l1 = sum(abs(cleaned[k]) for k in ordered_keys)
    l1_scaled = False
    if l1 > 0.10 and l1 > 0:
        scale = 0.10 / l1
        cleaned = {k: cleaned[k] * scale for k in ordered_keys}
        l1_scaled = True

    deadzone_applied_dims: list[str] = []
    for k in ordered_keys:
        if abs(cleaned[k]) < 0.015:
            if cleaned[k] != 0.0:
                deadzone_applied_dims.append(k)
            cleaned[k] = 0.0

    all_zero_after_deadzone = all(cleaned[k] == 0.0 for k in ordered_keys)

    cleaning = {
        "per_dim_clamped": per_dim_clamped,
        "l1_scaled": l1_scaled,
        "deadzone_applied_dims": deadzone_applied_dims,
        "all_zero_after_deadzone": all_zero_after_deadzone,
    }
    return cleaned, cleaning


def _render_input_for_teacher(input_obj: dict[str, Any]) -> str:
    user_text = str(input_obj.get("user_text", "") or "")
    prev_rel = input_obj.get("prev_rel_effective") or {}

    return (
        f"user_text:\n{user_text}\n\n"
        "prev_rel_effective:\n"
        f"bond={_safe_float(prev_rel.get('bond'), 0.0):.4f} "
        f"care={_safe_float(prev_rel.get('care'), 0.0):.4f} "
        f"trust={_safe_float(prev_rel.get('trust'), 0.0):.4f} "
        f"stability={_safe_float(prev_rel.get('stability'), 0.0):.4f}\n"
    )


async def _call_teacher_labeler(client: httpx.AsyncClient, model: str, input_obj: dict[str, Any]) -> dict[str, Any]:
    body = {
        "model": model,
        "input": [
            {"role": "system", "content": TEACHER_SYSTEM_PROMPT},
            {"role": "user", "content": _render_input_for_teacher(input_obj)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": TEACHER_SCHEMA["name"],
                "schema": TEACHER_SCHEMA["schema"],
                "strict": True,
            }
        },
    }
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    resp = await client.post(f"{settings.llm_base_url.rstrip('/')}/responses", headers=headers, json=body)
    resp.raise_for_status()
    data = resp.json()

    text_out = ""
    for item in data.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for c in item.get("content", []) or []:
            if isinstance(c, dict) and c.get("type") == "output_text" and isinstance(c.get("text"), str):
                text_out += c["text"]

    text_out = (text_out or data.get("output_text") or "").strip()
    if not text_out:
        raise RuntimeError("teacher output_text missing")

    raw_obj = json.loads(text_out)
    if not isinstance(raw_obj, dict):
        raise RuntimeError("teacher output is not an object")
    return raw_obj


async def _process_samples(
    samples: list[dict[str, Any]],
    *,
    output_path: Path,
    model: str,
    limit: int,
) -> int:
    count = 0
    async with httpx.AsyncClient(timeout=60.0) as client:
        with output_path.open("w", encoding="utf-8") as f:
            for idx, sample in enumerate(samples):
                if limit > 0 and idx >= limit:
                    break

                input_obj = sample.get("input") or {}
                meta_obj = sample.get("meta") or {}
                if not isinstance(input_obj, dict):
                    continue

                try:
                    raw_teacher = await _call_teacher_labeler(client, model, input_obj)
                except Exception as e:
                    out = {
                        "input": input_obj,
                        "raw_teacher": None,
                        "cleaned_target": None,
                        "cleaning": {
                            "error": str(e),
                            "per_dim_clamped": False,
                            "l1_scaled": False,
                            "deadzone_applied_dims": [],
                            "all_zero_after_deadzone": False,
                        },
                        "meta": {
                            **(meta_obj if isinstance(meta_obj, dict) else {}),
                            "teacher_model": model,
                            "source": "llm_teacher_batch",
                        },
                    }
                    f.write(json.dumps(out, ensure_ascii=False) + "\n")
                    count += 1
                    continue

                raw_delta = raw_teacher.get("delta_R") if isinstance(raw_teacher.get("delta_R"), dict) else {}
                cleaned_delta, cleaning = _clean_delta(raw_delta)
                cleaned_target = {
                    "delta_R": cleaned_delta,
                    "confidence": _clamp(raw_teacher.get("confidence", 0.5), 0.0, 1.0),
                }

                out = {
                    "input": input_obj,
                    "raw_teacher": raw_teacher,
                    "cleaned_target": cleaned_target,
                    "cleaning": cleaning,
                    "meta": {
                        **(meta_obj if isinstance(meta_obj, dict) else {}),
                        "teacher_model": model,
                        "source": "llm_teacher_batch",
                    },
                }
                f.write(json.dumps(out, ensure_ascii=False) + "\n")
                count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="tone_dataset.jsonl")
    parser.add_argument("--output", default="tone_teacher_labels.jsonl")
    parser.add_argument("--model", default="")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    if not settings.llm_api_key:
        raise RuntimeError("LLM_API_KEY is not set")

    model = args.model or getattr(settings, "tone_model", None) or settings.llm_model
    input_path = Path(args.input)
    output_path = Path(args.output)

    samples: list[dict[str, Any]] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            samples.append(json.loads(line))

    count = asyncio.run(_process_samples(samples, output_path=output_path, model=model, limit=args.limit))
    print(json.dumps({"ok": True, "output": str(output_path), "count": count, "model": model}, ensure_ascii=False))


if __name__ == "__main__":
    main()
