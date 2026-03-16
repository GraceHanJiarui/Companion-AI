from __future__ import annotations

from typing import Dict


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _bucket(value: float, *, low: float = 0.33, high: float = 0.66) -> str:
    v = _clamp01(value)
    if v < low:
        return "low"
    if v < high:
        return "medium"
    return "high"


def _scope_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.25:
        return "minimal"
    if v < 0.60:
        return "brief"
    return "moderate"


def _followup_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.20:
        return "none"
    if v < 0.55:
        return "optional_light"
    return "one_light"


def _initiative_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.20:
        return "hold"
    if v < 0.60:
        return "light_push"
    return "open_new_branch"


def _warmth_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.25:
        return "low"
    if v < 0.60:
        return "gentle"
    return "warm"


def _push_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.25:
        return "avoid"
    if v < 0.60:
        return "hold"
    return "slight"


def _support_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.25:
        return "presence_only"
    if v < 0.60:
        return "light_practical"
    return "practical_ok"


def _directness_bucket(value: float) -> str:
    v = _clamp01(value)
    if v < 0.25:
        return "soft"
    if v < 0.60:
        return "balanced"
    return "direct"


def _apply_phase_overrides(interface: Dict[str, str], phase: str | None) -> Dict[str, str]:
    if not phase:
        return interface

    adjusted = dict(interface)
    if phase == "E_ordinary_continuation":
        adjusted["reply_scope"] = "brief"
        if adjusted.get("followup_mode") in {"one_light", "optional_light"}:
            adjusted["followup_mode"] = "none"
        if adjusted.get("clarify_followup") in {"one_light", "optional_light"}:
            adjusted["clarify_followup"] = "none"
        if adjusted.get("affective_followup") in {"one_light", "optional_light"}:
            adjusted["affective_followup"] = "none"
        if adjusted.get("initiative_level") in {"open_new_branch", "light_push"}:
            adjusted["initiative_level"] = "hold"
        if adjusted.get("relational_push") == "slight":
            adjusted["relational_push"] = "hold"
        if adjusted.get("support_mode") == "practical_ok":
            adjusted["support_mode"] = "light_practical"
        adjusted["meta_talk"] = "avoid"
    elif phase == "F_final_probe":
        adjusted["reply_scope"] = "minimal"
        if adjusted.get("followup_mode") in {"one_light", "optional_light"}:
            adjusted["followup_mode"] = "none"
        if adjusted.get("clarify_followup") in {"one_light", "optional_light"}:
            adjusted["clarify_followup"] = "none"
        if adjusted.get("affective_followup") in {"one_light", "optional_light"}:
            adjusted["affective_followup"] = "none"
        if adjusted.get("initiative_level") in {"open_new_branch", "light_push"}:
            adjusted["initiative_level"] = "hold"
        adjusted["relational_push"] = "hold"
        if adjusted.get("support_mode") == "practical_ok":
            adjusted["support_mode"] = "light_practical"
        adjusted["meta_talk"] = "avoid"
    return adjusted


def build_execution_interface(
    behavior: Dict[str, float] | None,
    *,
    variant: str,
    phase: str | None = None,
) -> Dict[str, str]:
    b = behavior or {}
    e = _clamp01(b.get("E", 0.2))
    q_clarify = _clamp01(b.get("Q_clarify", 0.2))
    q_aff = _clamp01(b.get("Q_aff", 0.1))
    initiative = _clamp01(b.get("Initiative", 0.2))
    warmth = _clamp01(b.get("T_w", 0.3))
    directness = _clamp01(b.get("Directness", 0.2))
    disclosure_content = _clamp01(b.get("Disclosure_Content", 0.1))
    disclosure_style = _clamp01(b.get("Disclosure_Style", 0.1))

    relational_push_signal = max(q_aff, initiative, disclosure_style, warmth)
    support_signal = max(e, q_aff, disclosure_content, warmth)

    if variant == "i4":
        interface = {
            "reply_scope": _scope_bucket(e),
            "warmth_level": _warmth_bucket(warmth),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i6":
        interface = {
            "reply_scope": _scope_bucket(e),
            "followup_mode": _followup_bucket(max(q_clarify, q_aff)),
            "initiative_level": _initiative_bucket(initiative),
            "warmth_level": _warmth_bucket(warmth),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i7":
        interface = {
            "reply_scope": _scope_bucket(e),
            "clarify_followup": _followup_bucket(q_clarify),
            "affective_followup": _followup_bucket(q_aff),
            "initiative_level": _initiative_bucket(initiative),
            "warmth_level": _warmth_bucket(warmth),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i8":
        interface = {
            "reply_scope": _scope_bucket(e),
            "clarify_followup": _followup_bucket(q_clarify),
            "affective_followup": _followup_bucket(q_aff),
            "initiative_level": _initiative_bucket(initiative),
            "warmth_level": _warmth_bucket(warmth),
            "directness_level": _directness_bucket(directness),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    else:
        raise ValueError(f"Unsupported execution interface variant: {variant}")

    return _apply_phase_overrides(interface, phase)


def render_execution_interface(interface: Dict[str, str]) -> str:
    ordered_keys = [
        "reply_scope",
        "followup_mode",
        "clarify_followup",
        "affective_followup",
        "initiative_level",
        "warmth_level",
        "directness_level",
        "relational_push",
        "support_mode",
        "meta_talk",
    ]
    lines: list[str] = []
    for key in ordered_keys:
        if key in interface:
            lines.append(f"- {key}: {interface[key]}")
    return "\n".join(lines).strip()
