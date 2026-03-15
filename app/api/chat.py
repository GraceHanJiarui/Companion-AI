import json
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.core.llm_client import LLMClient
from app.memory.events import log_event, create_turn_event

from app.memory.memories import (
    retrieve_memories,
    should_create_summary_now,
    build_summary_for_last_n_turns,
    write_memory_summary,
)

from app.beliefs.extract import extract_beliefs_from_user_text
from app.beliefs.store import add_belief, list_active_beliefs, AddBeliefResult
from app.beliefs.policy import compute_ack_level, record_ack
from app.beliefs.ack import build_ack_block, belief_to_ack_topic
from app.beliefs.policy import apply_beliefs_to_policy, get_or_create_state, _load_policy, _save_policy

from app.models.belief import Belief
from app.outbox.enqueue import enqueue_job

from app.controller.controller_client import ControllerClient, fallback_plan_from_policy
from app.generation.actor_prompt import (
    build_prompt_only_baseline_system_prompt,
    build_relational_instruction_baseline_system_prompt,
    build_explicit_rel_state_direct_system_prompt,
    build_explicit_rel_state_projected_system_prompt,
    build_explicit_rel_state_direct_bridge_system_prompt,
    build_explicit_rel_state_projected_bridge_system_prompt,
    build_explicit_rel_state_projected_summary_system_prompt,
)
from app.generation.relational_instruction import (
    build_relational_instruction,
    build_relational_instruction_from_state,
    build_rel_state_explanation_from_state,
    build_behavior_explanation_from_behavior,
    collapse_relational_and_behavior_summaries,
)
from app.core.core_self import get_active_core_self
from app.core.config import settings

# relational delta (ΔR) evaluator (class name kept)
from app.inference.tone_evaluator import ToneEvaluatorClient
from app.inference.tone_delta_policy import normalize_tone_delta
from app.beliefs.policy import apply_tone_delta, slim_policy_snapshot


router = APIRouter()


class ChatIn(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=64)
    user_text: str = Field(..., min_length=1)
    experiment_mode: str | None = None
    oracle_relational_summary: str | None = None
    oracle_behavior_summary: str | None = None


def _summarize_active_beliefs_for_extractor(active_beliefs: list) -> str:
    lines: list[str] = []
    for b in active_beliefs[:20]:
        kind = getattr(b, "kind", "") or ""
        key = getattr(b, "key", None)
        value = getattr(b, "value", "") or ""
        if key:
            lines.append(f"[{kind}:{key}] {value}")
        else:
            lines.append(f"[{kind}] {value}")
    return "\n".join(lines)


def _boundary_keys_from_beliefs(active_beliefs: list) -> list[str]:
    return [b.key for b in active_beliefs if (getattr(b, "kind", None) == "boundary" and getattr(b, "key", None))]


@router.post("/chat")
async def chat(payload: ChatIn, db: Session = Depends(get_db)):
    experiment_mode = (payload.experiment_mode or getattr(settings, "experiment_mode", "explicit_rel_state_projected") or "explicit_rel_state_projected").strip()
    if experiment_mode == "method":
        experiment_mode = "explicit_rel_state_projected"
    prompt_variant = "A"
    if experiment_mode.endswith("_vA") or experiment_mode.endswith("_vB") or experiment_mode.endswith("_vC"):
        experiment_mode, prompt_variant = experiment_mode.rsplit("_v", 1)
        prompt_variant = prompt_variant.upper()
    allowed_modes = {
        "baseline_prompt_only",
        "baseline_prompt_only_strong",
        "baseline_relational_instruction",
        "explicit_rel_state_direct",
        "explicit_rel_state_projected",
        "explicit_rel_state_direct_oracle",
        "explicit_rel_state_projected_oracle",
        "baseline_relational_instruction_oracle_collapsed",
    }
    if experiment_mode not in allowed_modes:
        experiment_mode = "explicit_rel_state_projected"
    is_experiment = True

    trace_id = uuid.uuid4().hex
    t0 = time.perf_counter()

    timings = {
        "trace_id": trace_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "segments": {},
        "segments_ms": {},
        "total_s": 0.0,
        "total_ms": 0,
        "summary_triggered": False,
        "experiment_mode": experiment_mode,
    }

    def _mark(name: str, t_start: float) -> None:
        t_end = time.perf_counter()
        dt = t_end - t_start
        timings["segments"][name] = round(dt, 6)
        timings["segments_ms"][name] = int(dt * 1000)

    # 1) log user event
    t = time.perf_counter()
    user_event_id = log_event(db, payload.session_id, "user", payload.user_text)
    _mark("event_user_write", t)

    # 2) extract & store beliefs
    ack_block = ""
    active_beliefs = []
    state = None
    policy = None

    try:
        add_results: list[AddBeliefResult] = []

        # 2.1) rule-based
        rule_cands = extract_beliefs_from_user_text(payload.user_text)

        # 2.2) apply rule candidates synchronously
        if rule_cands:
            for c in rule_cands:
                res = add_belief(db, payload.session_id, c, evidence_event_id=user_event_id)
                add_results.append(res)

        # refresh active beliefs / ack
        state = get_or_create_state(db, payload.session_id)
        active_beliefs = list_active_beliefs(db, payload.session_id, limit=50)
        policy = _load_policy(state)

        # 2.3) (optional) enqueue async extractor job
        if getattr(settings, "belief_extractor_async", False) and not is_experiment:
            try:
                enqueue_job(
                    db,
                    kind="belief_extractor_llm",
                    payload={
                        "session_id": payload.session_id,
                        "user_text": payload.user_text,
                        "evidence_event_id": user_event_id,
                        "model": getattr(settings, "llm_model", "gpt-5-nano"),
                        "active_beliefs_text": _summarize_active_beliefs_for_extractor(active_beliefs),
                        "policy_json": json.dumps(slim_policy_snapshot(policy), ensure_ascii=False),
                    },
                )
            except Exception:
                pass

        # ack duplicate boundary (based on store results)
        try:
            dup_ids = [r.duplicate_of_id for r in add_results if (not r.created and r.duplicate_of_id)]
            if dup_ids:
                dup_belief_id = dup_ids[-1]
                dup_belief = db.execute(select(Belief).where(Belief.id == dup_belief_id)).scalar_one_or_none()
                if dup_belief:
                    level = compute_ack_level(policy, dup_belief.key, user_event_id)
                    topic = belief_to_ack_topic(dup_belief)
                    ack_block = build_ack_block(topic, level=level)
                    record_ack(policy, dup_belief.key or "", user_event_id)
                    _save_policy(db, state, policy)
        except Exception:
            pass

    except Exception:
        ack_block = ""
        try:
            state = get_or_create_state(db, payload.session_id)
            active_beliefs = list_active_beliefs(db, payload.session_id, limit=50)
            policy = _load_policy(state)
        except Exception:
            active_beliefs = []

    if state is None:
        state = get_or_create_state(db, payload.session_id)
    if policy is None:
        policy = _load_policy(state)

    boundary_keys = _boundary_keys_from_beliefs(active_beliefs)
    tone_prev = slim_policy_snapshot(policy)

    core_self_text = ""
    try:
        core_self_text = get_active_core_self(db)
    except Exception:
        core_self_text = ""
    core_self_preview = (core_self_text or "")[:220]

    # 3) relational delta (ΔR)
    if experiment_mode in {"explicit_rel_state_direct", "explicit_rel_state_projected"}:
        t = time.perf_counter()
        try:
            evaluator = ToneEvaluatorClient(model=(getattr(settings, "tone_model", None) or settings.llm_model))
            eval_payload = {
                "user_text": payload.user_text,
                "prev": tone_prev,
                "active_boundary_keys": boundary_keys,
            }

            raw_delta_obj = await evaluator.infer_delta(eval_payload)
            delta_obj = normalize_tone_delta(raw_delta_obj, user_text=payload.user_text)
            delta_debug = apply_tone_delta(policy, delta_obj, boundary_keys)

            policy["_last_rel_delta"] = {
                "ok": True,
                "error": None,
                "confidence": delta_obj.get("confidence"),
                "signals": delta_obj.get("signals"),
                "scene": delta_obj.get("scene"),
                "raw_delta_R": delta_obj.get("raw_delta_R"),
                "delta_R": delta_obj.get("delta_R"),
                "normalization": delta_obj.get("normalization"),
                "before": delta_debug.get("before"),
                "after": delta_debug.get("after"),
                "rel_effective": policy.get("rel_effective"),
                "behavior_effective": policy.get("behavior_effective"),
            }
            # backward compatible debug field name (if you still inspect it)
            policy["_last_tone_delta"] = policy["_last_rel_delta"]

        except Exception as e:
            try:
                policy = _load_policy(state)
                policy["_last_rel_delta"] = {"ok": False, "error": str(e)}
                policy["_last_tone_delta"] = policy["_last_rel_delta"]
            except Exception:
                pass
        _mark("tone_delta", t)
    else:
        policy["_last_rel_delta"] = {
            "ok": None,
            "error": None,
            "scene": [experiment_mode],
            "signals": ["disabled_for_baseline"],
            "delta_R": None,
        }
        policy["_last_tone_delta"] = policy["_last_rel_delta"]
        timings["segments"]["tone_delta"] = 0.0
        timings["segments_ms"]["tone_delta"] = 0

    # 4) retrieve episodic memories
    t = time.perf_counter()
    try:
        memories = await retrieve_memories(db, payload.session_id, payload.user_text, k=(2 if is_experiment else 5))
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={"detail": f"memory retrieval failed: {e}"},
            media_type="application/json; charset=utf-8",
        )
    _mark("memory_retrieve", t)

    memory_previews = []
    for m in (memories or [])[:(1 if is_experiment else 2)]:
        preview = getattr(m, "text", None) or getattr(m, "preview", None) or ""
        # 更紧凑，减少 controller tokens
        memory_previews.append({"id": getattr(m, "id", None), "preview": str(preview)[:160]})

    controller_err = None
    plan = None
    relational_instruction = None
    timings["segments"]["controller"] = 0.0
    timings["segments_ms"]["controller"] = 0

    # persist debug + timings
    try:
        if experiment_mode == "explicit_rel_state_projected":
            policy["_last_controller"] = {
                "ok": True,
                "error": None,
                "intent": experiment_mode,
                "behavior": dict(policy.get("behavior_effective") or {}),
                "selected_memories": memory_previews,
                "notes": {"mode": "rel_state_to_behavior_to_generation"},
                "plan": None,
                "experiment_mode": experiment_mode,
            }
        elif experiment_mode == "explicit_rel_state_direct":
            rel_inst = build_relational_instruction_from_state(policy.get("rel_effective") or {})
            relational_instruction = rel_inst.summary
            policy["_last_controller"] = {
                "ok": True,
                "error": None,
                "intent": experiment_mode,
                "behavior": None,
                "selected_memories": memory_previews,
                "notes": {
                    "relational_instruction": rel_inst.summary,
                    "labels": rel_inst.labels,
                    "reasons": rel_inst.reasons,
                    "prompt_variant": prompt_variant,
                    "mode": "rel_state_direct_to_generation",
                },
                "plan": None,
                "experiment_mode": experiment_mode,
            }
        elif experiment_mode == "explicit_rel_state_direct_oracle":
            relational_instruction = (payload.oracle_relational_summary or "").strip()
            if not relational_instruction:
                relational_instruction = "当前关系姿态应保持克制、连续、低过冲，不要自行升级关系。"
            policy["_last_controller"] = {
                "ok": True,
                "error": None,
                "intent": experiment_mode,
                "behavior": None,
                "selected_memories": memory_previews,
                "notes": {
                    "relational_instruction": relational_instruction,
                    "oracle": True,
                    "mode": "rel_state_direct_oracle_to_generation",
                },
                "plan": None,
                "experiment_mode": experiment_mode,
            }
        elif experiment_mode == "explicit_rel_state_projected_oracle":
            relational_instruction = (payload.oracle_relational_summary or "").strip()
            oracle_behavior_summary = (payload.oracle_behavior_summary or "").strip()
            if not relational_instruction:
                relational_instruction = "当前关系姿态应保持克制、连续、低过冲，不要自行升级关系。"
            if not oracle_behavior_summary:
                oracle_behavior_summary = "当前行为倾向应保持轻度温暖、低主动推进、少追问、避免过度安抚和解释。"
            policy["_last_controller"] = {
                "ok": True,
                "error": None,
                "intent": experiment_mode,
                "behavior": None,
                "selected_memories": memory_previews,
                "notes": {
                    "relational_instruction": relational_instruction,
                    "behavior_summary": oracle_behavior_summary,
                    "oracle": True,
                    "mode": "rel_state_projected_oracle_to_generation",
                },
                "plan": None,
                "experiment_mode": experiment_mode,
            }
        elif experiment_mode == "baseline_relational_instruction_oracle_collapsed":
            relational_instruction = (payload.oracle_relational_summary or "").strip()
            oracle_behavior_summary = (payload.oracle_behavior_summary or "").strip()
            if not relational_instruction:
                relational_instruction = "????????????????????????????"
            if not oracle_behavior_summary:
                oracle_behavior_summary = "??????????????????????????????????"
            collapsed_instruction = collapse_relational_and_behavior_summaries(
                relational_instruction,
                oracle_behavior_summary,
            )
            relational_instruction = collapsed_instruction
            policy["_last_controller"] = {
                "ok": True,
                "error": None,
                "intent": experiment_mode,
                "behavior": None,
                "selected_memories": memory_previews,
                "notes": {
                    "relational_instruction": collapsed_instruction,
                    "oracle": True,
                    "collapsed": True,
                    "mode": "oracle_collapsed_relational_instruction",
                },
                "plan": None,
                "experiment_mode": experiment_mode,
            }
        else:
            policy["_last_controller"] = {
                "ok": None,
                "error": None,
                "intent": experiment_mode,
                "behavior": None,
                "selected_memories": memory_previews,
                "notes": None,
                "plan": None,
                "experiment_mode": experiment_mode,
            }
            if experiment_mode == "baseline_relational_instruction":
                rel_inst = build_relational_instruction(
                    user_text=payload.user_text,
                    active_boundary_keys=boundary_keys,
                    memory_previews=memory_previews,
                )
                relational_instruction = rel_inst.summary
                policy["_last_controller"]["notes"] = {
                    "relational_instruction": rel_inst.summary,
                    "labels": rel_inst.labels,
                    "reasons": rel_inst.reasons,
                    "prompt_variant": prompt_variant,
                }
        policy["_last_trace_id"] = trace_id

        total_s = time.perf_counter() - t0
        timings["total_s"] = round(total_s, 6)
        timings["total_ms"] = int(total_s * 1000)
        policy["_last_latency"] = (
            {
                "trace_id": trace_id,
                "experiment_mode": experiment_mode,
                "total_ms": timings["total_ms"],
                "segments_ms": timings["segments_ms"],
            }
            if is_experiment
            else timings
        )

        _save_policy(db, state, policy)
    except Exception:
        pass

    # 5) Actor generate
    t = time.perf_counter()
    try:
        if experiment_mode == "explicit_rel_state_projected":
            rel_state_explanation = build_rel_state_explanation_from_state(policy.get("rel_effective") or {})
            behavior = (policy.get("behavior_effective") or {})
            behavior_explanation = build_behavior_explanation_from_behavior(behavior)
            if prompt_variant == "B":
                system_prompt = build_explicit_rel_state_projected_bridge_system_prompt(
                    core_self_text,
                    rel_state_explanation=rel_state_explanation,
                    behavior=behavior,
                    behavior_explanation=behavior_explanation,
                    memory_previews=memory_previews,
                )
            elif prompt_variant == "C":
                system_prompt = build_explicit_rel_state_projected_summary_system_prompt(
                    core_self_text,
                    relational_summary_only=rel_state_explanation,
                    behavior_summary_only=behavior_explanation,
                    memory_previews=memory_previews,
                )
            else:
                system_prompt = build_explicit_rel_state_projected_system_prompt(
                    core_self_text,
                    behavior=behavior,
                    memory_previews=memory_previews,
                )
        elif experiment_mode == "explicit_rel_state_direct":
            rel_effective = policy.get("rel_effective") or {}
            rel_state_explanation = build_rel_state_explanation_from_state(rel_effective)
            if prompt_variant == "B":
                system_prompt = build_explicit_rel_state_direct_bridge_system_prompt(
                    core_self_text,
                    rel_effective=rel_effective,
                    rel_state_explanation=rel_state_explanation,
                    memory_previews=memory_previews,
                )
            elif prompt_variant == "C":
                system_prompt = build_explicit_rel_state_direct_system_prompt(
                    core_self_text,
                    relational_instruction=rel_state_explanation,
                    memory_previews=memory_previews,
                )
            else:
                system_prompt = build_explicit_rel_state_direct_system_prompt(
                    core_self_text,
                    relational_instruction=(relational_instruction or ""),
                    memory_previews=memory_previews,
                )
        elif experiment_mode == "explicit_rel_state_direct_oracle":
            system_prompt = build_explicit_rel_state_direct_system_prompt(
                core_self_text,
                relational_instruction=(relational_instruction or ""),
                memory_previews=memory_previews,
            )
        elif experiment_mode == "explicit_rel_state_projected_oracle":
            system_prompt = build_explicit_rel_state_projected_summary_system_prompt(
                core_self_text,
                relational_summary_only=(relational_instruction or ""),
                behavior_summary_only=((policy.get("_last_controller") or {}).get("notes", {}) or {}).get("behavior_summary", ""),
                memory_previews=memory_previews,
            )
        elif experiment_mode in {"baseline_relational_instruction", "baseline_relational_instruction_oracle_collapsed"}:
            system_prompt = build_relational_instruction_baseline_system_prompt(
                core_self_text,
                relational_instruction=(relational_instruction or ""),
                active_boundary_keys=boundary_keys,
                memory_previews=memory_previews,
            )
        else:
            system_prompt = build_prompt_only_baseline_system_prompt(
                core_self_text,
                active_boundary_keys=boundary_keys,
                memory_previews=memory_previews,
                style_strength=("strong" if experiment_mode == "baseline_prompt_only_strong" else "normal"),
            )

        actor_model = getattr(settings, "actor_model", None) or settings.llm_model
        llm = LLMClient(model=actor_model)
        reply = await llm.generate(system=system_prompt, user=payload.user_text)

        if ack_block:
            reply = (ack_block.strip() + "\n\n" + reply.strip()).strip()

        log_event(db, payload.session_id, "assistant", reply)
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={"detail": f"llm generation failed: {e}"},
            media_type="application/json; charset=utf-8",
        )
    _mark("actor_generate", t)
    create_turn_event(
        db,
        session_id=payload.session_id,
        user_text=payload.user_text,
        assistant_text=reply,
        behavior=(policy["behavior_effective"] if experiment_mode == "explicit_rel_state_projected" else {}),
        scene=policy.get("_last_controller", {}).get("intent"),
        tone_eval={
            "input": {
                "user_text": payload.user_text,
                "prev_rel_effective": (tone_prev.get("rel_effective") if isinstance(tone_prev, dict) else {}),
            },
            "target": {
                "raw_delta_R": ((policy.get("_last_rel_delta") or {}).get("raw_delta_R") if isinstance(policy.get("_last_rel_delta"), dict) else None),
                "delta_R": ((policy.get("_last_rel_delta") or {}).get("delta_R") if isinstance(policy.get("_last_rel_delta"), dict) else None),
                "confidence": ((policy.get("_last_rel_delta") or {}).get("confidence") if isinstance(policy.get("_last_rel_delta"), dict) else None),
                "normalization": ((policy.get("_last_rel_delta") or {}).get("normalization") if isinstance(policy.get("_last_rel_delta"), dict) else None),
            },
            "meta": {
                "trace_id": trace_id,
                "teacher_model": getattr(settings, "tone_model", None) or settings.llm_model,
                "source": "llm_teacher",
            },
        },
        # trace_id=policy.get("_last_trace_id"),
    )

    # 6) optional summary
    t = time.perf_counter()
    try:
        if (not is_experiment) and should_create_summary_now(
            db,
            payload.session_id,
            every_n_user_turns=getattr(settings, "summary_every_n", 8),
        ):
            timings["summary_triggered"] = True
            summary_text, from_event_id, to_event_id = await build_summary_for_last_n_turns(
                db,
                payload.session_id,
                n_user_turns=12,
            )
            await write_memory_summary(
                db,
                payload.session_id,
                summary_text,
                from_event_id=from_event_id,
                to_event_id=to_event_id,
            )
    except Exception:
        pass
    if is_experiment:
        timings["segments"]["summary"] = 0.0
        timings["segments_ms"]["summary"] = 0
    else:
        _mark("summary", t)

    return {"reply": reply}
