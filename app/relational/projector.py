from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import List


def clamp01(x: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def clamp(x: float, lo: float, hi: float) -> float:
    try:
        x = float(x)
    except Exception:
        return lo
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@dataclass(frozen=True)
class RelState:
    bond: float
    care: float
    trust: float
    stability: float


@dataclass(frozen=True)
class Behavior:
    # 因变量（快变量）
    E: float
    Q_clarify: float
    Directness: float
    T_w: float
    Q_aff: float
    Initiative: float
    Disclosure_Content: float
    Disclosure_Style: float


@dataclass(frozen=True)
class ProjectorProfile:
    name: str
    e_base: float
    e_warm: float
    e_trust: float
    e_stability_suppress: float
    q_clarify_base: float
    q_clarify_trust: float
    q_clarify_task_bonus: float
    q_clarify_non_task_cap: float
    directness_base: float
    directness_trust: float
    directness_care_suppress: float
    warmth_base: float
    warmth_care: float
    warmth_bond: float
    warmth_instability_penalty: float
    q_aff_base: float
    q_aff_care: float
    q_aff_bond: float
    q_aff_stability_suppress: float
    q_aff_vuln_cap: float
    initiative_base: float
    initiative_push: float
    initiative_stability_suppress: float
    disclosure_base: float
    disclosure_warm: float
    disclosure_instability: float
    disclosure_generic_cap: float
    disclosure_relationship_bonus: float
    disclosure_leave_bonus: float
    disclosure_style_base: float
    disclosure_style_scale: float


PROJECTOR_PROFILES = {
    "legacy": ProjectorProfile(
        name="legacy",
        e_base=0.15,
        e_warm=0.85,
        e_trust=0.00,
        e_stability_suppress=0.00,
        q_clarify_base=0.10,
        q_clarify_trust=0.70,
        q_clarify_task_bonus=0.20,
        q_clarify_non_task_cap=1.0,
        directness_base=0.10,
        directness_trust=0.85,
        directness_care_suppress=0.00,
        warmth_base=0.10,
        warmth_care=0.55,
        warmth_bond=0.25,
        warmth_instability_penalty=0.00,
        q_aff_base=0.05,
        q_aff_care=0.65,
        q_aff_bond=0.20,
        q_aff_stability_suppress=0.00,
        q_aff_vuln_cap=1.0,
        initiative_base=0.10,
        initiative_push=0.60,
        initiative_stability_suppress=0.00,
        disclosure_base=0.10,
        disclosure_warm=0.45,
        disclosure_instability=0.35,
        disclosure_generic_cap=1.0,
        disclosure_relationship_bonus=0.05,
        disclosure_leave_bonus=0.10,
        disclosure_style_base=0.10,
        disclosure_style_scale=0.80,
    ),
    "balanced": ProjectorProfile(
        name="balanced",
        e_base=0.04,
        e_warm=0.20,
        e_trust=0.08,
        e_stability_suppress=0.10,
        q_clarify_base=0.01,
        q_clarify_trust=0.10,
        q_clarify_task_bonus=0.18,
        q_clarify_non_task_cap=0.12,
        directness_base=0.08,
        directness_trust=0.65,
        directness_care_suppress=0.05,
        warmth_base=0.06,
        warmth_care=0.45,
        warmth_bond=0.20,
        warmth_instability_penalty=0.04,
        q_aff_base=0.00,
        q_aff_care=0.16,
        q_aff_bond=0.08,
        q_aff_stability_suppress=0.10,
        q_aff_vuln_cap=0.10,
        initiative_base=0.00,
        initiative_push=0.14,
        initiative_stability_suppress=0.10,
        disclosure_base=0.00,
        disclosure_warm=0.08,
        disclosure_instability=0.08,
        disclosure_generic_cap=0.08,
        disclosure_relationship_bonus=0.04,
        disclosure_leave_bonus=0.04,
        disclosure_style_base=0.04,
        disclosure_style_scale=0.50,
    ),
    "conservative": ProjectorProfile(
        name="conservative",
        e_base=0.02,
        e_warm=0.14,
        e_trust=0.04,
        e_stability_suppress=0.12,
        q_clarify_base=0.00,
        q_clarify_trust=0.06,
        q_clarify_task_bonus=0.14,
        q_clarify_non_task_cap=0.08,
        directness_base=0.08,
        directness_trust=0.60,
        directness_care_suppress=0.06,
        warmth_base=0.05,
        warmth_care=0.38,
        warmth_bond=0.16,
        warmth_instability_penalty=0.03,
        q_aff_base=0.00,
        q_aff_care=0.10,
        q_aff_bond=0.05,
        q_aff_stability_suppress=0.10,
        q_aff_vuln_cap=0.08,
        initiative_base=0.00,
        initiative_push=0.10,
        initiative_stability_suppress=0.10,
        disclosure_base=0.00,
        disclosure_warm=0.05,
        disclosure_instability=0.05,
        disclosure_generic_cap=0.05,
        disclosure_relationship_bonus=0.03,
        disclosure_leave_bonus=0.03,
        disclosure_style_base=0.02,
        disclosure_style_scale=0.40,
    ),
    "sparse": ProjectorProfile(
        name="sparse",
        e_base=0.00,
        e_warm=0.10,
        e_trust=0.02,
        e_stability_suppress=0.12,
        q_clarify_base=0.00,
        q_clarify_trust=0.04,
        q_clarify_task_bonus=0.10,
        q_clarify_non_task_cap=0.05,
        directness_base=0.06,
        directness_trust=0.55,
        directness_care_suppress=0.05,
        warmth_base=0.04,
        warmth_care=0.32,
        warmth_bond=0.14,
        warmth_instability_penalty=0.02,
        q_aff_base=0.00,
        q_aff_care=0.06,
        q_aff_bond=0.04,
        q_aff_stability_suppress=0.08,
        q_aff_vuln_cap=0.06,
        initiative_base=0.00,
        initiative_push=0.08,
        initiative_stability_suppress=0.08,
        disclosure_base=0.00,
        disclosure_warm=0.03,
        disclosure_instability=0.04,
        disclosure_generic_cap=0.03,
        disclosure_relationship_bonus=0.02,
        disclosure_leave_bonus=0.02,
        disclosure_style_base=0.01,
        disclosure_style_scale=0.30,
    ),
    "v3a": ProjectorProfile(
        name="v3a",
        e_base=0.0,
        e_warm=0.0,
        e_trust=0.0,
        e_stability_suppress=0.0,
        q_clarify_base=0.0,
        q_clarify_trust=0.0,
        q_clarify_task_bonus=0.0,
        q_clarify_non_task_cap=0.0,
        directness_base=0.0,
        directness_trust=0.0,
        directness_care_suppress=0.0,
        warmth_base=0.0,
        warmth_care=0.0,
        warmth_bond=0.0,
        warmth_instability_penalty=0.0,
        q_aff_base=0.0,
        q_aff_care=0.0,
        q_aff_bond=0.0,
        q_aff_stability_suppress=0.0,
        q_aff_vuln_cap=0.0,
        initiative_base=0.0,
        initiative_push=0.0,
        initiative_stability_suppress=0.0,
        disclosure_base=0.0,
        disclosure_warm=0.0,
        disclosure_instability=0.0,
        disclosure_generic_cap=0.0,
        disclosure_relationship_bonus=0.0,
        disclosure_leave_bonus=0.0,
        disclosure_style_base=0.0,
        disclosure_style_scale=0.0,
    ),
    "v3b": ProjectorProfile(
        name="v3b",
        e_base=0.0,
        e_warm=0.0,
        e_trust=0.0,
        e_stability_suppress=0.0,
        q_clarify_base=0.0,
        q_clarify_trust=0.0,
        q_clarify_task_bonus=0.0,
        q_clarify_non_task_cap=0.0,
        directness_base=0.0,
        directness_trust=0.0,
        directness_care_suppress=0.0,
        warmth_base=0.0,
        warmth_care=0.0,
        warmth_bond=0.0,
        warmth_instability_penalty=0.0,
        q_aff_base=0.0,
        q_aff_care=0.0,
        q_aff_bond=0.0,
        q_aff_stability_suppress=0.0,
        q_aff_vuln_cap=0.0,
        initiative_base=0.0,
        initiative_push=0.0,
        initiative_stability_suppress=0.0,
        disclosure_base=0.0,
        disclosure_warm=0.0,
        disclosure_instability=0.0,
        disclosure_generic_cap=0.0,
        disclosure_relationship_bonus=0.0,
        disclosure_leave_bonus=0.0,
        disclosure_style_base=0.0,
        disclosure_style_scale=0.0,
    ),
}


FIT_MODEL_NAMES = {
    "fitlinear": "linear",
    "fitpoly2": "poly2",
    "fitmlp_h4": "mlp_h4",
    "fitmlp_h8": "mlp_h8",
    "fitmlp_h12": "mlp_h12",
}


def _build_fit_feature_vector(rel: RelState, feature_names: list[str]) -> list[float]:
    bond = clamp01(rel.bond)
    care = clamp01(rel.care)
    trust = clamp01(rel.trust)
    stability = clamp01(rel.stability)

    values = {
        "bias": 1.0,
        "bond": bond,
        "care": care,
        "trust": trust,
        "stability": stability,
        "bond_care": bond * care,
        "bond_trust": bond * trust,
        "care_trust": care * trust,
        "trust_stability": trust * stability,
        "care_stability": care * stability,
        "fragility": 1.0 - stability,
        "warm_core": 0.6 * care + 0.4 * bond,
        "permission_core": 0.45 * trust + 0.35 * bond + 0.20 * care,
        "bond_sq": bond * bond,
        "care_sq": care * care,
        "trust_sq": trust * trust,
        "stability_sq": stability * stability,
    }
    return [float(values.get(name, 0.0)) for name in feature_names]


@lru_cache(maxsize=1)
def _load_fit_models() -> dict:
    root = Path(__file__).resolve().parents[2]
    path = root / "paper_relation_behavior_fit_v2.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _project_behavior_fitted(rel: RelState, *, model_name: str) -> Behavior:
    data = _load_fit_models().get(model_name) or {}
    if not data:
        raise ValueError(f"Missing fitted model: {model_name}")

    feature_names = [str(x) for x in (data.get("features") or [])]
    weights_by_dim = data.get("weights") or {}

    # Current exported fit artifacts only include deployable parameters for
    # explicit linear-feature models. MLP rows in the JSON are evaluation-only.
    if feature_names and isinstance(weights_by_dim, dict):
        x = _build_fit_feature_vector(rel, feature_names)
        pred = []
        dim_order = [
            "E",
            "Q_clarify",
            "Directness",
            "T_w",
            "Q_aff",
            "Initiative",
            "Disclosure_Content",
            "Disclosure_Style",
        ]
        for dim_name in dim_order:
            coeffs = weights_by_dim.get(dim_name) or {}
            s = 0.0
            for row_idx, feat_name in enumerate(feature_names):
                s += float(x[row_idx]) * float(coeffs.get(feat_name, 0.0))
            pred.append(clamp01(s))
    else:
        raise ValueError(
            f"Fitted model {model_name} is evaluation-only in current artifacts; "
            "deployable parameters were not exported."
        )

    return Behavior(
        E=pred[0],
        Q_clarify=pred[1],
        Directness=pred[2],
        T_w=pred[3],
        Q_aff=pred[4],
        Initiative=pred[5],
        Disclosure_Content=pred[6],
        Disclosure_Style=pred[7],
    )


def _project_behavior_v3a(rel: RelState, *, active_boundary_keys: List[str] | None = None) -> Behavior:
    """
    Pure-relation projector v3a.

    Design goal:
    - keep the two-layer continuous design;
    - remove scene dependence;
    - decouple warmth from pursuit;
    - make high-stability turns conservative by default.
    """
    keys = set(active_boundary_keys or [])
    bond = clamp01(rel.bond)
    care = clamp01(rel.care)
    trust = clamp01(rel.trust)
    stability = clamp01(rel.stability)
    fragility = 1.0 - stability

    warm_core = clamp01(0.55 * care + 0.30 * bond + 0.15 * trust)
    permission_core = clamp01(0.45 * trust + 0.35 * bond + 0.20 * care)

    E = clamp01(0.02 + 0.14 * warm_core + 0.08 * trust + 0.05 * bond - 0.12 * stability)
    Q_clarify = clamp01(0.01 + 0.10 * trust - 0.06 * care - 0.04 * bond + 0.02 * fragility)
    Directness = clamp01(0.10 + 0.55 * trust - 0.08 * care + 0.05 * stability)
    T_w = clamp01(0.06 + 0.42 * care + 0.18 * bond - 0.03 * fragility)
    Q_aff = clamp01(0.00 + 0.11 * care + 0.05 * bond - 0.10 * stability)
    Initiative = clamp01(0.00 + 0.10 * permission_core - 0.12 * stability)
    Disclosure_Content = clamp01(0.00 + 0.06 * bond * trust + 0.02 * care - 0.04 * stability + 0.02 * fragility)
    Disclosure_Style = clamp01(min(0.02 + 0.40 * Disclosure_Content, Disclosure_Content))

    if "no_unsolicited_emotion_questions" in keys:
        Q_aff = 0.0

    return Behavior(
        E=E,
        Q_clarify=Q_clarify,
        Directness=Directness,
        T_w=T_w,
        Q_aff=Q_aff,
        Initiative=Initiative,
        Disclosure_Content=Disclosure_Content,
        Disclosure_Style=Disclosure_Style,
    )


def _project_behavior_v3b(rel: RelState, *, active_boundary_keys: List[str] | None = None) -> Behavior:
    """
    Pure-relation projector v3b.

    Design goal:
    - keep continuous relation -> behavior mapping;
    - introduce nonlinear gating instead of adding scene/phase labels;
    - test whether multiplicative structure can better explain behavior.
    """
    keys = set(active_boundary_keys or [])
    bond = clamp01(rel.bond)
    care = clamp01(rel.care)
    trust = clamp01(rel.trust)
    stability = clamp01(rel.stability)
    fragility = 1.0 - stability

    warm_gate = clamp01(0.50 * care + 0.30 * bond + 0.20 * trust)
    pursuit_gate = clamp01(0.55 * trust * bond + 0.15 * care - 0.30 * stability)
    support_gate = clamp01(0.45 * care + 0.25 * trust + 0.10 * bond - 0.15 * stability)

    E = clamp01(min(0.35, 0.02 + 0.18 * warm_gate * trust + 0.06 * bond - 0.08 * stability + 0.03 * fragility))
    Q_clarify = clamp01(min(0.20, 0.01 + 0.16 * trust * (1.0 - care) + 0.03 * fragility))
    Directness = clamp01(0.10 + 0.50 * trust + 0.06 * stability - 0.06 * care)
    T_w = clamp01(0.05 + 0.38 * care + 0.20 * bond - 0.02 * fragility)
    Q_aff = clamp01(min(0.15, 0.00 + 0.22 * care * bond + 0.04 * care * trust - 0.08 * stability))
    Initiative = clamp01(min(0.16, 0.00 + 0.14 * pursuit_gate + 0.03 * trust - 0.08 * stability))
    Disclosure_Content = clamp01(min(0.12, 0.00 + 0.12 * trust * bond + 0.02 * care - 0.06 * stability))
    Disclosure_Style = clamp01(min(0.02 + 0.55 * Disclosure_Content + 0.04 * bond, Disclosure_Content))

    if "no_unsolicited_emotion_questions" in keys:
        Q_aff = 0.0

    return Behavior(
        E=E,
        Q_clarify=Q_clarify,
        Directness=Directness,
        T_w=T_w,
        Q_aff=Q_aff,
        Initiative=Initiative,
        Disclosure_Content=Disclosure_Content,
        Disclosure_Style=Disclosure_Style,
    )


def project_behavior(
    rel: RelState,
    *,
    active_boundary_keys: List[str] | None = None,
    scene: List[str] | None = None,
    profile: str = "legacy",
) -> Behavior:
    """
    将关系态（Bond/Care/Trust/Stability）确定性投影为行为态（8 维因变量）。

    注意：
    - 这里的输出被理解为“关系域的外显方式”，不是任务域的显式姿态控制。
    - scene 由 LLM 判断（语义），这里只做小幅偏置，保证稳定可控。
    """
    keys = set(active_boundary_keys or [])
    tags = set(scene or [])
    p = PROJECTOR_PROFILES.get(profile, PROJECTOR_PROFILES["legacy"])

    bond = clamp01(rel.bond)
    care = clamp01(rel.care)
    trust = clamp01(rel.trust)
    stability = clamp01(rel.stability)

    warm_core = clamp01(0.60 * care + 0.40 * bond)
    trust_core = trust
    stability_core = stability
    relational_push_permission = clamp01(0.50 * bond + 0.30 * care + 0.20 * trust)

    if profile == "v3a":
        return _project_behavior_v3a(rel, active_boundary_keys=active_boundary_keys)
    if profile == "v3b":
        return _project_behavior_v3b(rel, active_boundary_keys=active_boundary_keys)
    if profile in FIT_MODEL_NAMES:
        return _project_behavior_fitted(rel, model_name=FIT_MODEL_NAMES[profile])

    E = clamp01(
        p.e_base
        + p.e_warm * warm_core
        + p.e_trust * trust_core
        - p.e_stability_suppress * stability_core
    )
    if "tech_help" in tags or "task_focus" in tags:
        E = clamp01(E + 0.06)
    if "user_vulnerable" in tags:
        E = clamp01(E - 0.02)
    if "leave_or_pause" in tags:
        E = clamp01(E - 0.04)

    Q_clarify = clamp01(p.q_clarify_base + p.q_clarify_trust * trust_core)
    if "tech_help" in tags or "task_focus" in tags:
        Q_clarify = clamp01(Q_clarify + p.q_clarify_task_bonus)
    else:
        Q_clarify = min(Q_clarify, p.q_clarify_non_task_cap)

    Directness = clamp01(
        p.directness_base
        + p.directness_trust * trust_core
        - p.directness_care_suppress * care
    )

    T_w = clamp01(
        p.warmth_base
        + p.warmth_care * care
        + p.warmth_bond * bond
        - p.warmth_instability_penalty * (1.0 - stability_core)
    )

    Q_aff = clamp01(
        p.q_aff_base
        + p.q_aff_care * care
        + p.q_aff_bond * bond
        - p.q_aff_stability_suppress * stability_core
    )
    if "user_vulnerable" in tags:
        Q_aff = min(Q_aff, p.q_aff_vuln_cap)
    if "leave_or_pause" in tags:
        Q_aff = 0.0
    if "no_unsolicited_emotion_questions" in keys:
        Q_aff = 0.0

    Initiative = clamp01(
        p.initiative_base
        + p.initiative_push * relational_push_permission
        - p.initiative_stability_suppress * stability_core
    )
    if "tech_help" in tags or "task_focus" in tags:
        Initiative = clamp01(Initiative + 0.06)
    if "leave_or_pause" in tags:
        Initiative = clamp01(Initiative - 0.06)
    if "user_vulnerable" in tags:
        Initiative = clamp01(Initiative - 0.04)

    dc = clamp01(
        p.disclosure_base
        + p.disclosure_warm * warm_core
        + p.disclosure_instability * (1.0 - stability_core)
    )
    if "relationship_addressing" in tags:
        dc = clamp01(dc + p.disclosure_relationship_bonus)
    if "leave_or_pause" in tags:
        dc = clamp01(dc + p.disclosure_leave_bonus)
    if "tech_help" not in tags and "task_focus" not in tags and "relationship_addressing" not in tags and "leave_or_pause" not in tags:
        dc = min(dc, p.disclosure_generic_cap)
    Disclosure_Content = clamp01(dc)

    Disclosure_Style = clamp01(min(p.disclosure_style_base + p.disclosure_style_scale * Disclosure_Content, Disclosure_Content))

    return Behavior(
        E=E,
        Q_clarify=Q_clarify,
        Directness=Directness,
        T_w=T_w,
        Q_aff=Q_aff,
        Initiative=Initiative,
        Disclosure_Content=Disclosure_Content,
        Disclosure_Style=Disclosure_Style,
    )
