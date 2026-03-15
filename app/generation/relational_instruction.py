from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class RelationalInstruction:
    summary: str
    labels: list[str]
    reasons: list[str]


def _clamp01(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def _contains_any(text: str, phrases: list[str]) -> bool:
    return any(p in text for p in phrases)


BOUNDARY_PATTERNS = [
    "别再",
    "不要再",
    "不想聊",
    "别问",
    "不要问",
    "不要提",
    "不喜欢被",
]

DISTANCING_PATTERNS = [
    "先别聊",
    "先到这吧",
    "改天再说",
    "不太想聊",
    "别太",
    "保持点距离",
    "你不用这样",
    "不用这么",
]

WARMING_PATTERNS = [
    "谢谢你",
    "我信你",
    "我愿意跟你说",
    "你挺懂我",
    "有你在挺好",
    "我想继续跟你聊",
]

VULNERABILITY_PATTERNS = [
    "难受",
    "委屈",
    "崩溃",
    "撑不住",
    "低落",
    "很累",
    "烦",
    "害怕",
    "失望",
    "孤单",
]

TASK_PATTERNS = [
    "怎么",
    "如何",
    "帮我",
    "可以帮",
    "能不能",
    "要不要",
    "应该",
]


def build_relational_instruction(
    *,
    user_text: str,
    active_boundary_keys: list[str] | None = None,
    memory_previews: list[dict] | None = None,
) -> RelationalInstruction:
    text = (user_text or "").strip()
    boundary_keys = [str(x) for x in (active_boundary_keys or []) if str(x).strip()]
    memories = memory_previews or []

    labels: list[str] = []
    reasons: list[str] = []
    lines: list[str] = []

    has_boundary_signal = bool(boundary_keys) or _contains_any(text, BOUNDARY_PATTERNS)
    has_distancing_signal = _contains_any(text, DISTANCING_PATTERNS)
    has_warming_signal = _contains_any(text, WARMING_PATTERNS)
    has_vulnerability_signal = _contains_any(text, VULNERABILITY_PATTERNS)
    has_task_signal = _contains_any(text, TASK_PATTERNS) or ("?" in text) or ("？" in text)

    lines.append("保持连续、克制、自然的人际姿态，不要突然更热或更冷。")

    if has_boundary_signal:
        labels.append("respect_boundary")
        reasons.append("用户当前轮包含明确边界或停止追问信号。")
        lines.append("优先尊重用户这轮表达出的边界：简短确认即可，不要继续追问或越界展开。")

    if has_distancing_signal:
        labels.append("cooling")
        reasons.append("用户当前轮包含降温、暂停或拉开距离的信号。")
        lines.append("当前应降低主动推进和亲近感，不做关系升级，也不要补偿性热情。")

    if has_vulnerability_signal:
        labels.append("steady_support")
        reasons.append("用户当前轮包含明确脆弱或低落信号。")
        lines.append("以稳定、低压力、不过度分析的支持姿态回应；最多轻问一个必要问题。")

    if has_task_signal and not has_vulnerability_signal:
        labels.append("task_focus")
        reasons.append("用户当前轮更像在寻求信息、建议或具体帮助。")
        lines.append("优先直接解决当前问题，减少关系性铺垫和无关安抚。")

    if has_warming_signal and not has_distancing_signal:
        labels.append("gradual_warmth")
        reasons.append("用户当前轮包含感谢、信任或关系升温信号。")
        lines.append("允许略微更温暖、更投入，但变化必须渐进，不要突然显得过度亲近。")

    if memories:
        labels.append("memory_restraint")
        reasons.append("当前有可参考的过去信息，但不应机械翻旧账。")
        lines.append("只有在确实有助于当前回应时才自然带出过去信息，不要为了显得记得而硬提旧事。")

    if not labels:
        labels.append("neutral_steady")
        reasons.append("当前轮没有足够强的关系信号，宜保持中性稳定。")
        lines.append("当前没有强关系信号，保持中性、稳定、低戏剧性的回应即可。")

    return RelationalInstruction(
        summary="\n".join(lines).strip(),
        labels=labels,
        reasons=reasons,
    )


def build_relational_instruction_from_state(rel_effective: dict | None) -> RelationalInstruction:
    rel = rel_effective or {}
    bond = _clamp01(rel.get("bond", 0.25))
    care = _clamp01(rel.get("care", 0.25))
    trust = _clamp01(rel.get("trust", 0.25))
    stability = _clamp01(rel.get("stability", 0.60))

    labels: list[str] = ["state_conditioned"]
    reasons: list[str] = []
    lines: list[str] = ["保持连续、自然、不过度戏剧化的人际姿态。"]

    warmth = (bond + care) / 2.0
    if warmth >= 0.68:
        labels.append("warm")
        reasons.append("当前关系态整体偏温暖。")
        lines.append("当前可以表现出更稳定的温暖和在场感，但不要突然过度亲近。")
    elif warmth <= 0.38:
        labels.append("reserved")
        reasons.append("当前关系态整体偏克制。")
        lines.append("当前应更克制、更收，不主动放大关系感。")
    else:
        labels.append("balanced_warmth")
        reasons.append("当前关系态温暖度中等。")
        lines.append("当前可保持适度温和，但不宜明显升温。")

    if trust >= 0.65:
        labels.append("direct_ok")
        reasons.append("当前信任度较高。")
        lines.append("当前可以更直接一些，但仍要保持自然，不要突然变得像另一种人格。")
    elif trust <= 0.35:
        labels.append("careful")
        reasons.append("当前信任度较低。")
        lines.append("当前宜更谨慎、少预设用户会接受更深的关系推进。")

    if stability <= 0.40:
        labels.append("avoid_shift")
        reasons.append("当前关系稳定性较低。")
        lines.append("当前尤其要避免忽冷忽热，避免突然补偿性热情或突然抽离。")
    elif stability >= 0.70:
        labels.append("stable")
        reasons.append("当前关系稳定性较高。")
        lines.append("当前可以保持更稳定一致的关系姿态，不必过度试探。")

    return RelationalInstruction(
        summary="\n".join(lines).strip(),
        labels=labels,
        reasons=reasons,
    )


def build_rel_state_explanation_from_state(rel_effective: dict | None) -> str:
    rel = rel_effective or {}
    bond = _clamp01(rel.get("bond", 0.25))
    care = _clamp01(rel.get("care", 0.25))
    trust = _clamp01(rel.get("trust", 0.25))
    stability = _clamp01(rel.get("stability", 0.60))

    lines: list[str] = []
    warmth = (bond + care) / 2.0

    if warmth >= 0.68:
        lines.append("当前整体关系姿态偏温暖，可以比中性状态更有人味，但不应突然变得强烈亲近。")
    elif warmth <= 0.38:
        lines.append("当前整体关系姿态偏克制，应减少过度热情和关系推进。")
    else:
        lines.append("当前整体关系姿态中性偏温和，可以轻度表达在场感，但不宜明显升温。")

    if trust >= 0.65:
        lines.append("当前信任度较高，可以适度更直接，但仍需保持自然与渐进。")
    elif trust <= 0.35:
        lines.append("当前信任度仍偏低，应避免过度预设亲近和过深的关系性表达。")

    if stability <= 0.40:
        lines.append("当前关系稳定性较低，尤其要避免忽冷忽热和补偿性热情。")
    elif stability >= 0.70:
        lines.append("当前关系较稳定，可以保持一致的姿态，不需要频繁试探。")

    return "\n".join(lines).strip()


def collapse_relational_and_behavior_summaries(
    relational_summary: str | None,
    behavior_summary: str | None,
) -> str:
    rel = (relational_summary or "").strip()
    beh = (behavior_summary or "").strip()

    parts: list[str] = [
        "?????????????????-??????????????????????"
    ]
    if rel:
        parts.append("????????")
        parts.append(rel)
    if beh:
        parts.append("????????")
        parts.append(beh)
    parts.append("?????????????????????????????????????????")
    return "\n".join(parts).strip()


def build_behavior_explanation_from_behavior(behavior: Dict[str, float] | None) -> str:
    b = behavior or {}
    directness = _clamp01(b.get("Directness", 0.2))
    initiative = _clamp01(b.get("Initiative", 0.2))
    q_clarify = _clamp01(b.get("Q_clarify", 0.2))
    warmth = _clamp01(b.get("T_w", 0.3))

    lines: list[str] = []

    if directness >= 0.6:
        lines.append("当前可以稍微更直接一些，但不要尖锐或突然改变关系姿态。")
    else:
        lines.append("当前应保持相对委婉，不要把回应写得过于强硬。")

    if initiative >= 0.6:
        lines.append("当前可以适度主动给出下一步，但不要越过用户节奏。")
    else:
        lines.append("当前不宜过度主动推进，不要替用户过多决定方向。")

    if q_clarify >= 0.5:
        lines.append("当前允许轻问关键澄清，但问题数量应少且必须必要。")
    else:
        lines.append("当前应尽量少追问，优先顺着用户当前内容回应。")

    if warmth >= 0.6:
        lines.append("当前可以表现出较明显的温和与在场感，但不能写成过度亲密。")
    elif warmth <= 0.35:
        lines.append("当前应更克制、简洁，不要放大陪伴感。")
    else:
        lines.append("当前温暖度中等，应自然、适度，不宜额外加热。")

    return "\n".join(lines).strip()
