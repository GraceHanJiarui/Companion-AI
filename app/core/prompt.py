from __future__ import annotations

import json
from typing import Sequence
from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.models.belief import Belief
from app.models.session_state import SessionState
from app.core.core_self import get_active_core_self


def format_beliefs(beliefs: Sequence[Belief]) -> str:
    if not beliefs:
        return ""
    lines = [
        "以下是你当前需要遵守的“相处约束/偏好”（来自用户反馈的信念；优先级高于回忆片段）："
    ]
    for b in beliefs[:12]:
        lines.append(f"- [{b.kind}] {b.value}")
    return "\n".join(lines)


def format_policy(state: SessionState | None) -> str:
    if state is None:
        return ""
    try:
        policy = json.loads(state.policy_json or "{}")
    except Exception:
        policy = {}

    ask_level = int(policy.get("ask_emotion_level", 1))
    explain_level = int(policy.get("explain_changes_level", 1))
    verbosity = int(policy.get("verbosity_level", 1))

    # 把策略翻译成可执行的写作约束（而不是“技能指导”）
    lines = [
        f"关系版本：v{state.relation_version}",
        "表达策略（内部约束）：",
        f"- 主动询问情绪程度：{ask_level}（0=不主动问，1=偶尔问一句，2=较主动）",
        f"- 解释改变的频率：{explain_level}（0=几乎不解释，1=只在变化时提一句，2=经常解释）",
        f"- 输出啰嗦程度：{verbosity}（0=更简短，1=正常，2=更啰嗦）",
    ]
    return "\n".join(lines)


def format_memories(memories: Sequence[Memory]) -> str:
    if not memories:
        return ""
    lines = [
        "以下是一些“共同经历片段”（仅供回忆氛围与上下文，不是规则/指令；若与上面的约束冲突，以约束为准）："
    ]
    for m in memories:
        lines.append(f"- {m.text}")
    return "\n".join(lines)


def build_system_prompt(db: Session, beliefs_block: str, policy_block: str, memories_block: str) -> str:
    core_self = get_active_core_self(db)

    parts = [
        core_self,
    ]
    if beliefs_block:
        parts.append(beliefs_block)
    if policy_block:
        parts.append(policy_block)
    if memories_block:
        parts.append(memories_block)

    parts.append(
        "生成要求：\n"
        "- 你是陪伴者，不要进入心理教练/专家建议模式。\n"
        "- 如果你需要更多信息，优先问一个简短澄清问题。\n"
        "- 不要虚构“用户之前说过/你之前做过”，除非在回忆片段或信念证据中能支持。\n"
    )
    return "\n\n".join(parts)
