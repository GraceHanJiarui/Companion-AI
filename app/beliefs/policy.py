from __future__ import annotations
import json

from sqlalchemy.orm import Session

from app.models.session_state import SessionState
from app.models.belief import Belief
from app.relational.projector import RelState, project_behavior


DEFAULT_POLICY = {
    # legacy sliders (kept for backward compatibility, but may be deprecated later)
    "ask_emotion_level": 1,
    "explain_changes_level": 1,
    "verbosity_level": 1,

    # ack tracking
    "last_ack_key": None,
    "last_ack_user_turn": -999999,

    # relational trait/state
    "rel_trait": {"bond": 0.25, "care": 0.25, "trust": 0.25, "stability": 0.60},
    "rel_state_boost": {"bond": 0.00, "care": 0.00, "trust": 0.00, "stability": 0.00},

    # cached effective + projected behavior (for debug & controller input)
    "rel_effective": {"bond": 0.25, "care": 0.25, "trust": 0.25, "stability": 0.60},
    "behavior_effective": {
        "E": 0.20,
        "Q_clarify": 0.20,
        "Directness": 0.20,
        "T_w": 0.30,
        "Q_aff": 0.10,
        "Initiative": 0.20,
        "Disclosure_Content": 0.10,
        "Disclosure_Style": 0.10,
    },

    # debug (existing project convention) - we will keep minimal set only
    "_last_controller": None,
    "_last_rel_delta": None,
    "_last_latency": None,
    "_last_trace_id": None,

    # legacy debug keys still seen in your current state dumps
    # we will stop writing them, but we won't break if they exist
    "last_extractor": None,
    "last_apply": None,
    "_last_tone_delta": None,
}


# Keys that are noisy and safe to delete from policy_json on each write
PRUNE_KEYS = {
    # old / redundant duplicates
    "_last_tone_delta",  # duplicate of _last_rel_delta
    # these two are useful when you are actively debugging outbox; keep if you want
    # "last_extractor",
    # "last_apply",
}

# If you want to keep last_extractor/last_apply, set this True.
KEEP_EXTRACTOR_DEBUG = True


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


def _prune_policy_debug(policy: dict) -> None:
    """
    Keep policy_json readable. This does NOT affect system behavior.
    Only deletes known noisy keys (mostly duplicated debug payloads).
    """
    if not isinstance(policy, dict):
        return

    for k in list(PRUNE_KEYS):
        if k in policy:
            del policy[k]

    if not KEEP_EXTRACTOR_DEBUG:
        policy.pop("last_extractor", None)
        policy.pop("last_apply", None)


def _ensure_policy_defaults(policy: dict) -> dict:
    """
    Scheme A:
    - Only fill defaults + clamp trait/state.
    - DO NOT recompute caches here.

    Rationale:
    - Recomputing rel_effective/behavior_effective requires boundary_keys & scene.
    - If we recompute here with empty context, we can overwrite the gated caches
      computed by apply_tone_delta(), causing Q_aff gating to "disappear".
    """
    if not isinstance(policy, dict):
        policy = {}

    for k, v in DEFAULT_POLICY.items():
        if k not in policy:
            policy[k] = v

    # ensure nested dicts
    if not isinstance(policy.get("rel_trait"), dict):
        policy["rel_trait"] = dict(DEFAULT_POLICY["rel_trait"])
    if not isinstance(policy.get("rel_state_boost"), dict):
        policy["rel_state_boost"] = dict(DEFAULT_POLICY["rel_state_boost"])
    if not isinstance(policy.get("rel_effective"), dict):
        policy["rel_effective"] = dict(DEFAULT_POLICY["rel_effective"])
    if not isinstance(policy.get("behavior_effective"), dict):
        policy["behavior_effective"] = dict(DEFAULT_POLICY["behavior_effective"])

    # clamp trait/state
    for k in ["bond", "care", "trust", "stability"]:
        policy["rel_trait"][k] = _clamp01(policy["rel_trait"].get(k, DEFAULT_POLICY["rel_trait"][k]))
        policy["rel_state_boost"][k] = _clamp01(policy["rel_state_boost"].get(k, 0.0))

    # IMPORTANT: no cache recompute here
    _prune_policy_debug(policy)
    return policy


def _recompute_effective_and_behavior(policy: dict, *, active_boundary_keys: list[str], scene: list[str]) -> None:
    """
    The only place we recompute cached rel_effective/behavior_effective.
    Must be called with correct boundary context.
    """
    trait = policy.get("rel_trait") or {}
    boost = policy.get("rel_state_boost") or {}

    eff = {
        "bond": _clamp01(_clamp01(trait.get("bond", 0.25)) + _clamp01(boost.get("bond", 0.0))),
        "care": _clamp01(_clamp01(trait.get("care", 0.25)) + _clamp01(boost.get("care", 0.0))),
        "trust": _clamp01(_clamp01(trait.get("trust", 0.25)) + _clamp01(boost.get("trust", 0.0))),
        "stability": _clamp01(_clamp01(trait.get("stability", 0.60)) + _clamp01(boost.get("stability", 0.0))),
    }
    policy["rel_effective"] = eff

    rel = RelState(
        bond=eff["bond"],
        care=eff["care"],
        trust=eff["trust"],
        stability=eff["stability"],
    )
    beh = project_behavior(rel, active_boundary_keys=active_boundary_keys, scene=scene)
    policy["behavior_effective"] = {
        "E": beh.E,
        "Q_clarify": beh.Q_clarify,
        "Directness": beh.Directness,
        "T_w": beh.T_w,
        "Q_aff": beh.Q_aff,
        "Initiative": beh.Initiative,
        "Disclosure_Content": beh.Disclosure_Content,
        "Disclosure_Style": beh.Disclosure_Style,
    }


def get_or_create_state(db: Session, session_id: str) -> SessionState:
    state = db.get(SessionState, session_id)
    if state is not None:
        return state
    state = SessionState(session_id=session_id, relation_version=1, policy_json="{}")
    db.add(state)
    db.commit()
    db.refresh(state)
    return state


def _load_policy(state: SessionState) -> dict:
    try:
        raw = state.policy_json or "{}"
        policy = json.loads(raw)
    except Exception:
        policy = {}
    return _ensure_policy_defaults(policy)


def _save_policy(db: Session, state: SessionState, policy: dict) -> None:
    _prune_policy_debug(policy)
    state.policy_json = json.dumps(policy, ensure_ascii=False)
    db.add(state)
    db.commit()
    db.refresh(state)


def slim_policy_snapshot(policy: dict) -> dict:
    """
    Slim snapshot for Controller / Evaluator:
    - only effective relational state + projected behavior
    - no debug blob
    """
    policy = _ensure_policy_defaults(policy)
    return {
        "rel_effective": policy.get("rel_effective", {}),
        "behavior_effective": policy.get("behavior_effective", {}),
    }


def compute_ack_level(policy: dict, key: str | None, current_turn: int) -> int:
    if not key:
        return 0
    last_key = policy.get("last_ack_key")
    if last_key == key:
        return 2
    return 1


def record_ack(policy: dict, key: str, current_turn: int) -> None:
    policy["last_ack_key"] = key
    policy["last_ack_user_turn"] = int(current_turn)


def apply_beliefs_to_policy(db: Session, session_id: str, beliefs: list[Belief]) -> SessionState:
    """
    v1: beliefs mainly affect gating via boundary keys at projector/actor.
    Keep legacy behavior: if no_unsolicited_emotion_questions active -> lower ask_emotion_level.
    """
    state = get_or_create_state(db, session_id)
    policy = _load_policy(state)

    hit = any(
        b.kind == "boundary" and b.status == "active" and b.key == "no_unsolicited_emotion_questions"
        for b in beliefs
    )
    if hit:
        policy["ask_emotion_level"] = max(0, int(policy.get("ask_emotion_level", 1)) - 1)

    _save_policy(db, state, policy)
    return state


def apply_tone_delta(policy: dict, delta_obj: dict, boundary_keys: list[str]) -> dict:
    """
    Backward-compatible name used by chat.py.

    Applies ΔR (relational delta) -> updates rel_state_boost -> recompute caches using boundary_keys + scene.
    """
    policy = _ensure_policy_defaults(policy)

    before = {
        "rel_state_boost": dict(policy.get("rel_state_boost", {})),
        "rel_effective": dict(policy.get("rel_effective", {})),
        "behavior_effective": dict(policy.get("behavior_effective", {})),
    }

    # decay to avoid drift-only-up
    decay = 0.85
    for k in ["bond", "care", "trust", "stability"]:
        policy["rel_state_boost"][k] = _clamp01(policy["rel_state_boost"].get(k, 0.0) * decay)

    # confidence shrink
    try:
        conf = float(delta_obj.get("confidence", 0.5))
    except Exception:
        conf = 0.5
    conf = max(0.0, min(1.0, conf))
    shrink = 0.5 if conf < 0.45 else 1.0

    d = delta_obj.get("delta_R")
    if not isinstance(d, dict):
        d = {}

    for k in ["bond", "care", "trust", "stability"]:
        try:
            dv = float(d.get(k, 0.0))
        except Exception:
            dv = 0.0
        dv = max(-0.2, min(0.2, dv)) * shrink
        policy["rel_state_boost"][k] = _clamp01(policy["rel_state_boost"].get(k, 0.0) + dv)

    scene = delta_obj.get("scene")
    if not isinstance(scene, list):
        scene = []
    scene = [str(x) for x in scene][:12]

    _recompute_effective_and_behavior(policy, active_boundary_keys=boundary_keys, scene=scene)

    after = {
        "rel_state_boost": dict(policy.get("rel_state_boost", {})),
        "rel_effective": dict(policy.get("rel_effective", {})),
        "behavior_effective": dict(policy.get("behavior_effective", {})),
    }

    # keep only one delta debug field (avoid duplication)
    policy["_last_rel_delta"] = {
        "ok": True,
        "error": None,
        "confidence": conf,
        "scene": scene,
        "signals": (delta_obj.get("signals") if isinstance(delta_obj.get("signals"), list) else []),
        "raw_delta_R": (delta_obj.get("raw_delta_R") if isinstance(delta_obj.get("raw_delta_R"), dict) else None),
        "delta_R": d,
        "normalization": (delta_obj.get("normalization") if isinstance(delta_obj.get("normalization"), dict) else None),
        "before": before,
        "after": after,
    }

    # Do NOT write _last_tone_delta anymore (it was duplicating _last_rel_delta)
    policy.pop("_last_tone_delta", None)

    _prune_policy_debug(policy)
    return {"before": before, "after": after, "scene": scene, "confidence": conf}
