from __future__ import annotations

import copy
import re

from app.core.config import settings


DELTA_KEYS = ("bond", "care", "trust", "stability")

STRONG_SCENES = {
    "user_vulnerable",
    "relationship_addressing",
    "leave_or_pause",
}

STRONG_SIGNALS = {
    "boundary",
    "vulnerable",
    "relationship_confirm",
    "relationship_testing",
    "leave_or_pause",
    "gratitude",
    "trust",
    "dependence",
    "disappointment",
    "distance",
    "conflict",
    "repair",
}

STRONG_PATTERNS = [
    re.compile(
        r"(别再|不要再|不想聊|别问|不要问|别逼|别逼近|别追问|保持距离|退一下|暂停|先不聊|我不想被追问)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(难受|崩溃|委屈|失望|脆弱|受不了|受伤|低落|想哭|害怕|不安|孤单|想退|想离开)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(谢谢你|我信任你|我还是在意|不是完全不想理你|我有点依赖|你别装得太陌生|关系|距离|疏远|冷淡)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(don't ask|stop asking|leave me alone|need space|take a step back|trust you|disappointed|hurt|vulnerable|pause)",
        re.IGNORECASE,
    ),
]


def _as_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def _has_strong_text_signal(user_text: str) -> bool:
    text = (user_text or "").strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in STRONG_PATTERNS)


def _has_strong_relationship_signal(delta_obj: dict, user_text: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    scene = delta_obj.get("scene")
    if isinstance(scene, list):
        hit = [str(x) for x in scene if str(x) in STRONG_SCENES]
        if hit:
            reasons.append(f"scene:{','.join(hit)}")

    signals = delta_obj.get("signals")
    if isinstance(signals, list):
        hit = [str(x) for x in signals if str(x) in STRONG_SIGNALS]
        if hit:
            reasons.append(f"signals:{','.join(hit)}")

    if _has_strong_text_signal(user_text):
        reasons.append("user_text_pattern")

    return (len(reasons) > 0, reasons)


def normalize_tone_delta(delta_obj: dict, *, user_text: str) -> dict:
    """
    Normalize raw teacher output before applying it to relational state.

    Goals:
    - treat relation state as a slow variable
    - prefer zero updates over noisy micro-changes
    - keep a debuggable record of raw vs normalized deltas
    """
    obj = copy.deepcopy(delta_obj if isinstance(delta_obj, dict) else {})

    raw_delta = obj.get("delta_R")
    if not isinstance(raw_delta, dict):
        raw_delta = {}
    raw_delta = {k: _as_float(raw_delta.get(k, 0.0)) for k in DELTA_KEYS}
    component_limit = _as_float(getattr(settings, "tone_delta_component_limit", 0.05), 0.05)
    l1_limit = _as_float(getattr(settings, "tone_delta_l1_limit", 0.10), 0.10)
    deadzone = _as_float(getattr(settings, "tone_delta_deadzone", 0.015), 0.015)

    strong_signal, signal_reasons = _has_strong_relationship_signal(obj, user_text)
    normalized = dict(raw_delta)
    reasons: list[str] = []

    if not strong_signal:
        normalized = {k: 0.0 for k in DELTA_KEYS}
        reasons.append("no_strong_signal")
    else:
        for key in DELTA_KEYS:
            clipped = _clamp(normalized[key], -component_limit, component_limit)
            if clipped != normalized[key]:
                reasons.append(f"component_clamp:{key}")
            normalized[key] = clipped

        for key in DELTA_KEYS:
            if abs(normalized[key]) < deadzone:
                if normalized[key] != 0.0:
                    reasons.append(f"deadzone_zero:{key}")
                normalized[key] = 0.0

        l1 = sum(abs(normalized[key]) for key in DELTA_KEYS)
        if l1 > l1_limit and l1 > 0.0:
            scale = l1_limit / l1
            normalized = {key: normalized[key] * scale for key in DELTA_KEYS}
            reasons.append("l1_rescaled")

        for key in DELTA_KEYS:
            if abs(normalized[key]) < deadzone:
                normalized[key] = 0.0

        if all(normalized[key] == 0.0 for key in DELTA_KEYS):
            reasons.append("all_zero_after_normalization")

    raw_conf = _clamp(_as_float(obj.get("confidence", 0.5), 0.5), 0.0, 1.0)
    if not strong_signal:
        confidence = max(raw_conf, 0.80)
    elif all(normalized[key] == 0.0 for key in DELTA_KEYS):
        confidence = max(raw_conf, 0.65)
    else:
        confidence = raw_conf

    obj["delta_R"] = normalized
    obj["confidence"] = confidence
    obj["raw_delta_R"] = raw_delta
    obj["normalization"] = {
        "enabled": True,
        "strong_signal": strong_signal,
        "signal_reasons": signal_reasons,
        "component_limit": component_limit,
        "l1_limit": l1_limit,
        "deadzone": deadzone,
        "reasons": reasons,
    }
    return obj
