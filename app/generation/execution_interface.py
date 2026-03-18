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


def _rel_to_direct_signals(rel_effective: Dict[str, float] | None) -> Dict[str, float]:
    """
    Build a deployable-interface candidate directly from relation state.

    This is intentionally simple and deterministic. The goal is not to claim
    this is the final correct interface, but to let us test whether bypassing
    the 8D behavior layer reduces deployment mismatch.
    """
    rel = rel_effective or {}
    bond = _clamp01(rel.get("bond", 0.25))
    care = _clamp01(rel.get("care", 0.25))
    trust = _clamp01(rel.get("trust", 0.25))
    stability = _clamp01(rel.get("stability", 0.60))
    fragility = 1.0 - stability

    warm_core = _clamp01(0.55 * care + 0.30 * bond + 0.15 * trust)
    permission_core = _clamp01(0.45 * trust + 0.35 * bond + 0.20 * care)

    return {
        "reply_scope_signal": _clamp01(0.03 + 0.10 * warm_core + 0.05 * trust + 0.03 * bond - 0.08 * stability),
        "clarify_followup_signal": _clamp01(0.02 + 0.16 * trust - 0.09 * care + 0.04 * fragility),
        "affective_followup_signal": _clamp01(0.00 + 0.18 * care + 0.08 * bond - 0.16 * stability),
        "initiative_signal": _clamp01(0.00 + 0.12 * permission_core - 0.12 * stability),
        "warmth_signal": _clamp01(0.08 + 0.34 * care + 0.14 * bond - 0.03 * fragility),
        "directness_signal": _clamp01(0.10 + 0.45 * trust - 0.05 * care),
    }


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


def build_execution_interface_from_rel(
    rel_effective: Dict[str, float] | None,
    *,
    variant: str,
    phase: str | None = None,
) -> Dict[str, str]:
    signals = _rel_to_direct_signals(rel_effective)
    reply_scope_signal = signals["reply_scope_signal"]
    clarify_signal = signals["clarify_followup_signal"]
    affective_signal = signals["affective_followup_signal"]
    initiative_signal = signals["initiative_signal"]
    warmth_signal = signals["warmth_signal"]
    directness_signal = signals["directness_signal"]
    relational_push_signal = _clamp01(max(affective_signal, initiative_signal, 0.60 * warmth_signal))
    support_signal = _clamp01(max(reply_scope_signal, affective_signal, 0.60 * warmth_signal))

    if variant == "i4":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i6":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "followup_mode": _followup_bucket(max(clarify_signal, affective_signal)),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i7":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "clarify_followup": _followup_bucket(clarify_signal),
            "affective_followup": _followup_bucket(affective_signal),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i8":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "clarify_followup": _followup_bucket(clarify_signal),
            "affective_followup": _followup_bucket(affective_signal),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "directness_level": _directness_bucket(directness_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    else:
        raise ValueError(f"Unsupported direct execution interface variant: {variant}")

    return _apply_phase_overrides(interface, phase)


def build_execution_interface_from_instruction_labels(
    labels: list[str] | None,
    *,
    variant: str,
    phase: str | None = None,
) -> Dict[str, str]:
    labels_set = set(labels or [])

    reply_scope_signal = 0.28
    clarify_signal = 0.18
    affective_signal = 0.16
    initiative_signal = 0.18
    warmth_signal = 0.30
    directness_signal = 0.22

    if "respect_boundary" in labels_set:
        reply_scope_signal = min(reply_scope_signal, 0.18)
        clarify_signal = min(clarify_signal, 0.10)
        affective_signal = min(affective_signal, 0.12)
        initiative_signal = min(initiative_signal, 0.08)
        warmth_signal = min(warmth_signal, 0.24)
    if "cooling" in labels_set:
        reply_scope_signal = min(reply_scope_signal, 0.20)
        clarify_signal = min(clarify_signal, 0.10)
        affective_signal = min(affective_signal, 0.10)
        initiative_signal = min(initiative_signal, 0.06)
        warmth_signal = min(warmth_signal, 0.20)
    if "steady_support" in labels_set:
        reply_scope_signal = max(reply_scope_signal, 0.32)
        affective_signal = max(affective_signal, 0.32)
        warmth_signal = max(warmth_signal, 0.42)
        initiative_signal = max(initiative_signal, 0.12)
    if "task_focus" in labels_set:
        reply_scope_signal = max(reply_scope_signal, 0.34)
        directness_signal = max(directness_signal, 0.42)
        clarify_signal = max(clarify_signal, 0.22)
        affective_signal = min(affective_signal, 0.18)
    if "gradual_warmth" in labels_set:
        warmth_signal = max(warmth_signal, 0.46)
        affective_signal = max(affective_signal, 0.28)
        initiative_signal = max(initiative_signal, 0.18)
    if "memory_restraint" in labels_set:
        initiative_signal = min(initiative_signal, 0.16)
    if "neutral_steady" in labels_set:
        initiative_signal = min(initiative_signal, 0.14)
        warmth_signal = max(warmth_signal, 0.28)

    relational_push_signal = _clamp01(max(affective_signal, initiative_signal, 0.60 * warmth_signal))
    support_signal = _clamp01(max(reply_scope_signal, affective_signal, 0.60 * warmth_signal))

    if variant == "i4":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i6":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "followup_mode": _followup_bucket(max(clarify_signal, affective_signal)),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i7":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "clarify_followup": _followup_bucket(clarify_signal),
            "affective_followup": _followup_bucket(affective_signal),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    elif variant == "i8":
        interface = {
            "reply_scope": _scope_bucket(reply_scope_signal),
            "clarify_followup": _followup_bucket(clarify_signal),
            "affective_followup": _followup_bucket(affective_signal),
            "initiative_level": _initiative_bucket(initiative_signal),
            "warmth_level": _warmth_bucket(warmth_signal),
            "directness_level": _directness_bucket(directness_signal),
            "relational_push": _push_bucket(relational_push_signal),
            "support_mode": _support_bucket(support_signal),
            "meta_talk": "avoid",
        }
    else:
        raise ValueError(f"Unsupported baseline execution interface variant: {variant}")

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


def render_execution_interface_with_semantics(interface: Dict[str, str], *, semantic_variant: str = "sa") -> str:
    label_maps = {
        "sa": {
            "reply_scope": "reply_scope",
            "followup_mode": "followup_mode",
            "clarify_followup": "clarify_followup",
            "affective_followup": "affective_followup",
            "initiative_level": "initiative_level",
            "warmth_level": "warmth_level",
            "directness_level": "directness_level",
            "relational_push": "relational_push",
            "support_mode": "support_mode",
            "meta_talk": "meta_talk",
        },
        "sb": {
            "reply_scope": "response_extent",
            "followup_mode": "followup_tendency",
            "clarify_followup": "clarification_tendency",
            "affective_followup": "emotional_checkin_tendency",
            "initiative_level": "forward_pacing",
            "warmth_level": "tone_warmth",
            "directness_level": "tone_directness",
            "relational_push": "forward_pressure",
            "support_mode": "support_posture",
            "meta_talk": "meta_talk",
        },
        "sc": {
            "reply_scope": "response_extent_limit",
            "followup_mode": "followup_permission",
            "clarify_followup": "clarification_permission",
            "affective_followup": "emotional_checkin_permission",
            "initiative_level": "forward_pressure_limit",
            "warmth_level": "social_temperature",
            "directness_level": "directness_band",
            "relational_push": "relational_movement",
            "support_mode": "support_posture",
            "meta_talk": "meta_talk",
        },
    }
    labels = label_maps.get(semantic_variant, label_maps["sa"])
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
            lines.append(f"- {labels.get(key, key)}: {interface[key]}")
    return "\n".join(lines).strip()


def _followup_rank(value: str) -> int:
    ranks = {
        "none": 0,
        "optional_light": 1,
        "one_light": 2,
    }
    return ranks.get(str(value), 0)


def _followup_from_rank(rank: int) -> str:
    mapping = {
        0: "none",
        1: "optional_light",
        2: "one_light",
    }
    return mapping[max(0, min(2, int(rank)))]


def _interactional_ontology(interface: Dict[str, str]) -> Dict[str, str]:
    curiosity_rank = max(
        _followup_rank(interface.get("clarify_followup", "none")),
        _followup_rank(interface.get("affective_followup", "none")) - 1,
    )
    return {
        "response_extent": interface.get("reply_scope", "brief"),
        "curiosity": _followup_from_rank(curiosity_rank),
        "emotional_checkin": interface.get("affective_followup", "none"),
        "forward_pacing": interface.get("initiative_level", "hold"),
        "temperature": interface.get("warmth_level", "gentle"),
        "interaction_pressure": interface.get("relational_push", "hold"),
        "support_posture": interface.get("support_mode", "light_practical"),
    }


def _permission_ontology(interface: Dict[str, str]) -> Dict[str, str]:
    return {
        "response_extent_limit": interface.get("reply_scope", "brief"),
        "clarification_permission": interface.get("clarify_followup", "none"),
        "emotional_permission": interface.get("affective_followup", "none"),
        "forward_pressure_limit": interface.get("initiative_level", "hold"),
        "social_temperature_cap": interface.get("warmth_level", "gentle"),
        "relational_movement_limit": interface.get("relational_push", "hold"),
        "support_allowance": interface.get("support_mode", "light_practical"),
    }


def render_execution_interface_with_ontology(
    interface: Dict[str, str],
    *,
    ontology_variant: str = "A",
    semantic_variant: str = "sa",
) -> str:
    if ontology_variant == "A":
        return render_execution_interface_with_semantics(interface, semantic_variant=semantic_variant)

    if ontology_variant == "B":
        remapped = _interactional_ontology(interface)
        order = [
            "response_extent",
            "curiosity",
            "emotional_checkin",
            "forward_pacing",
            "temperature",
            "interaction_pressure",
            "support_posture",
        ]
        label_maps = {
            "sa": {
                "response_extent": "response_extent",
                "curiosity": "curiosity",
                "emotional_checkin": "emotional_checkin",
                "forward_pacing": "forward_pacing",
                "temperature": "temperature",
                "interaction_pressure": "interaction_pressure",
                "support_posture": "support_posture",
            },
            "sb": {
                "response_extent": "turn_extent",
                "curiosity": "curiosity_drive",
                "emotional_checkin": "emotional_checkin",
                "forward_pacing": "forward_pacing",
                "temperature": "interaction_temperature",
                "interaction_pressure": "forward_pressure",
                "support_posture": "support_posture",
            },
            "sc": {
                "response_extent": "response_extent_band",
                "curiosity": "curiosity_permission",
                "emotional_checkin": "emotional_checkin_permission",
                "forward_pacing": "forward_pacing_limit",
                "temperature": "social_temperature",
                "interaction_pressure": "interaction_pressure_cap",
                "support_posture": "support_allowance",
            },
        }
        labels = label_maps.get(semantic_variant, label_maps["sa"])
        return "\n".join(f"- {labels[key]}: {remapped[key]}" for key in order).strip()

    if ontology_variant == "C":
        remapped = _permission_ontology(interface)
        order = [
            "response_extent_limit",
            "clarification_permission",
            "emotional_permission",
            "forward_pressure_limit",
            "social_temperature_cap",
            "relational_movement_limit",
            "support_allowance",
        ]
        label_maps = {
            "sa": {
                "response_extent_limit": "response_extent_limit",
                "clarification_permission": "clarification_permission",
                "emotional_permission": "emotional_permission",
                "forward_pressure_limit": "forward_pressure_limit",
                "social_temperature_cap": "social_temperature_cap",
                "relational_movement_limit": "relational_movement_limit",
                "support_allowance": "support_allowance",
            },
            "sb": {
                "response_extent_limit": "response_pacing_limit",
                "clarification_permission": "clarification_room",
                "emotional_permission": "emotional_room",
                "forward_pressure_limit": "forward_pressure_limit",
                "social_temperature_cap": "temperature_ceiling",
                "relational_movement_limit": "movement_allowance",
                "support_allowance": "support_allowance",
            },
            "sc": {
                "response_extent_limit": "response_extent_limit",
                "clarification_permission": "clarification_permission",
                "emotional_permission": "emotional_permission",
                "forward_pressure_limit": "forward_permission",
                "social_temperature_cap": "temperature_cap",
                "relational_movement_limit": "relational_movement_cap",
                "support_allowance": "support_allowance",
            },
        }
        labels = label_maps.get(semantic_variant, label_maps["sa"])
        return "\n".join(f"- {labels[key]}: {remapped[key]}" for key in order).strip()

    raise ValueError(f"Unsupported ontology variant: {ontology_variant}")


def render_continuous_execution_interface(behavior: Dict[str, float] | None) -> str:
    b = behavior or {}
    ordered_keys = [
        "E",
        "Q_clarify",
        "Q_aff",
        "Initiative",
        "T_w",
        "Directness",
        "Disclosure_Content",
        "Disclosure_Style",
    ]
    gloss = {
        "E": "reply_scope_signal",
        "Q_clarify": "clarify_followup_signal",
        "Q_aff": "affective_followup_signal",
        "Initiative": "initiative_signal",
        "T_w": "warmth_signal",
        "Directness": "directness_signal",
        "Disclosure_Content": "disclosure_content_signal",
        "Disclosure_Style": "disclosure_style_signal",
    }
    lines: list[str] = []
    for key in ordered_keys:
        lines.append(f"- {key} ({gloss[key]}): {_clamp01(b.get(key, 0.0)):.3f}")
    return "\n".join(lines).strip()


def _soft_level(value: float) -> str:
    v = _clamp01(value)
    if v < 0.15:
        return "off"
    if v < 0.35:
        return "low"
    if v < 0.65:
        return "medium"
    return "high"


def _soft_scope(value: float) -> str:
    v = _clamp01(value)
    if v < 0.15:
        return "minimal"
    if v < 0.45:
        return "brief"
    if v < 0.75:
        return "moderate"
    return "extended"


def _band(value: float, *, half_width: float = 0.06) -> str:
    v = _clamp01(value)
    lo = _clamp01(v - half_width)
    hi = _clamp01(v + half_width)
    return f"{lo:.2f}-{hi:.2f}"


def render_ordinal_soft_execution_interface(behavior: Dict[str, float] | None) -> str:
    b = behavior or {}
    lines = [
        f"- reply_scope: {_soft_scope(b.get('E', 0.0))}",
        f"- clarify_followup: {_soft_level(b.get('Q_clarify', 0.0))}",
        f"- affective_followup: {_soft_level(b.get('Q_aff', 0.0))}",
        f"- initiative: {_soft_level(b.get('Initiative', 0.0))}",
        f"- warmth: {_soft_level(b.get('T_w', 0.0))}",
        f"- directness: {_soft_level(b.get('Directness', 0.0))}",
        f"- disclosure_content: {_soft_level(b.get('Disclosure_Content', 0.0))}",
        f"- disclosure_style: {_soft_level(b.get('Disclosure_Style', 0.0))}",
    ]
    return "\n".join(lines).strip()


def render_ordinal_soft_execution_interface_with_semantics(
    behavior: Dict[str, float] | None,
    *,
    semantic_variant: str = "sa",
) -> str:
    b = behavior or {}
    label_maps = {
        "sa": {
            "reply_scope": "reply_scope",
            "clarify_followup": "clarify_followup",
            "affective_followup": "affective_followup",
            "initiative": "initiative",
            "warmth": "warmth",
            "directness": "directness",
            "disclosure_content": "disclosure_content",
            "disclosure_style": "disclosure_style",
        },
        "sb": {
            "reply_scope": "response_extent",
            "clarify_followup": "clarification_tendency",
            "affective_followup": "emotional_checkin_tendency",
            "initiative": "forward_pacing",
            "warmth": "tone_warmth",
            "directness": "tone_directness",
            "disclosure_content": "self_disclosure_content",
            "disclosure_style": "self_disclosure_style",
        },
        "sc": {
            "reply_scope": "response_extent_limit",
            "clarify_followup": "clarification_permission",
            "affective_followup": "emotional_checkin_permission",
            "initiative": "forward_pressure_limit",
            "warmth": "social_temperature",
            "directness": "directness_band",
            "disclosure_content": "disclosure_content_allowance",
            "disclosure_style": "disclosure_style_allowance",
        },
    }
    labels = label_maps.get(semantic_variant, label_maps["sa"])
    lines = [
        f"- {labels['reply_scope']}: {_soft_scope(b.get('E', 0.0))}",
        f"- {labels['clarify_followup']}: {_soft_level(b.get('Q_clarify', 0.0))}",
        f"- {labels['affective_followup']}: {_soft_level(b.get('Q_aff', 0.0))}",
        f"- {labels['initiative']}: {_soft_level(b.get('Initiative', 0.0))}",
        f"- {labels['warmth']}: {_soft_level(b.get('T_w', 0.0))}",
        f"- {labels['directness']}: {_soft_level(b.get('Directness', 0.0))}",
        f"- {labels['disclosure_content']}: {_soft_level(b.get('Disclosure_Content', 0.0))}",
        f"- {labels['disclosure_style']}: {_soft_level(b.get('Disclosure_Style', 0.0))}",
    ]
    return "\n".join(lines).strip()


def render_banded_execution_interface(behavior: Dict[str, float] | None) -> str:
    b = behavior or {}
    ordered_keys = [
        "E",
        "Q_clarify",
        "Q_aff",
        "Initiative",
        "T_w",
        "Directness",
        "Disclosure_Content",
        "Disclosure_Style",
    ]
    lines: list[str] = []
    for key in ordered_keys:
        lines.append(f"- {key}: {_band(b.get(key, 0.0))}")
    return "\n".join(lines).strip()


def render_hybrid_execution_interface(behavior: Dict[str, float] | None) -> str:
    b = behavior or {}
    lines = [
        f"- reply_scope: {_scope_bucket(b.get('E', 0.0))}",
        f"- clarify_followup: {_followup_bucket(b.get('Q_clarify', 0.0))}",
        f"- affective_followup: {_followup_bucket(b.get('Q_aff', 0.0))}",
        f"- initiative_level: {_initiative_bucket(b.get('Initiative', 0.0))}",
        f"- warmth_band: {_band(b.get('T_w', 0.0))}",
        f"- directness_band: {_band(b.get('Directness', 0.0))}",
        f"- disclosure_content_band: {_band(b.get('Disclosure_Content', 0.0))}",
        f"- disclosure_style_band: {_band(b.get('Disclosure_Style', 0.0))}",
    ]
    return "\n".join(lines).strip()
