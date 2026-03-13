import json
from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.db.session import get_db
from app.beliefs.store import list_active_beliefs
from app.beliefs.policy import get_or_create_state
from app.models.core_self import CoreSelfVersion
from app.memory.memories import retrieve_memories

router = APIRouter(prefix="/debug")


def _safe_json_loads(s: str | None) -> dict:
    try:
        if not s:
            return {}
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _as_dict(x) -> dict:
    # 防御性：确保一定是普通 dict（避免奇怪对象/None 导致 PowerShell 显示成空）
    if isinstance(x, dict):
        return dict(x)
    return {}


def _summarize_latency(lat: dict | None) -> dict:
    if not isinstance(lat, dict):
        return {}
    seg_ms = lat.get("segments_ms")
    if not isinstance(seg_ms, dict):
        seg_ms = {}
    # 挑最重要的几段
    keys = ["event_user_write", "belief_extract", "belief_apply_store", "tone_delta", "memory_retrieve", "controller", "actor"]
    out = {}
    for k in keys:
        if k in seg_ms:
            out[k] = seg_ms.get(k)
    if "total_ms" in lat:
        out["total_ms"] = lat.get("total_ms")
    if "trace_id" in lat:
        out["trace_id"] = lat.get("trace_id")
    return out


def _summarize_controller(c: dict | None) -> dict:
    if not isinstance(c, dict):
        return {}
    out = {
        "ok": c.get("ok"),
        "intent": c.get("intent"),
        "error": c.get("error"),
    }
    # behavior/controls 只保留一层，避免爆屏
    if isinstance(c.get("behavior"), dict):
        out["behavior"] = c.get("behavior")
    if isinstance(c.get("controls"), dict):
        out["controls"] = c.get("controls")
    return {k: v for k, v in out.items() if v is not None}


def _summarize_rel_delta(d: dict | None) -> dict:
    if not isinstance(d, dict):
        return {}
    out = {
        "ok": d.get("ok"),
        "confidence": d.get("confidence"),
        "delta_R": d.get("delta_R"),
        "scene": d.get("scene"),
        "signals": d.get("signals"),
    }
    # signals 太长就截断
    if isinstance(out.get("signals"), list):
        out["signals"] = [str(x) for x in out["signals"]][:12]
    if isinstance(out.get("scene"), list):
        out["scene"] = [str(x) for x in out["scene"]][:12]
    return {k: v for k, v in out.items() if v is not None}


def _build_policy_view(policy: dict) -> dict:
    """
    精简视图（用于 PowerShell 友好输出）：
    - rel: trait/state_boost/effective
    - behavior_effective
    - debug: 只给摘要（trace/latency/controller/rel_delta + outbox extractor/apply）
    """
    if not isinstance(policy, dict):
        policy = {}

    rel = {
        "trait": _as_dict(policy.get("rel_trait")),
        "state_boost": _as_dict(policy.get("rel_state_boost")),
        "effective": _as_dict(policy.get("rel_effective")),
    }

    view = {
        "rel": rel,
        "behavior_effective": _as_dict(policy.get("behavior_effective")),
        "debug": {
            "_last_trace_id": policy.get("_last_trace_id"),
            "_last_latency_ms": _summarize_latency(policy.get("_last_latency")),
            "_last_controller": _summarize_controller(policy.get("_last_controller")),
            "_last_rel_delta": _summarize_rel_delta(policy.get("_last_rel_delta")),
            "last_extractor": policy.get("last_extractor"),
            "last_apply": policy.get("last_apply"),
        },
    }

    # 轻量 prune：只去掉 None，不去掉空 dict（空 dict 对你排查很有用）
    def prune_none(obj):
        if isinstance(obj, dict):
            return {k: prune_none(v) for k, v in obj.items() if v is not None}
        if isinstance(obj, list):
            return [prune_none(v) for v in obj if v is not None]
        return obj

    return prune_none(view)


@router.get("/sessions/{session_id}/context")
async def debug_context(
    session_id: str,
    query: str | None = None,
    slim: int | None = Query(default=None, description="slim=1 只返回核心字段（建议默认就用）"),
    db: Session = Depends(get_db),
):
    # core self (active)
    core = db.execute(
        select(CoreSelfVersion).where(CoreSelfVersion.active == True).order_by(desc(CoreSelfVersion.id)).limit(1)  # noqa: E712
    ).scalar_one_or_none()

    core_payload = None
    if core is not None:
        core_payload = {
            "id": core.id,
            "active": core.active,
            "preview": (core.text or "")[:200],
            "created_at": core.created_at,
        }

    beliefs = list_active_beliefs(db, session_id, limit=50)
    state = get_or_create_state(db, session_id)

    policy = _safe_json_loads(state.policy_json)
    policy_view = _build_policy_view(policy)

    memories_payload = []
    if query:
        try:
            mems = await retrieve_memories(db, session_id, query, k=5)
            memories_payload = [
                {"id": m.id, "created_at": m.created_at, "preview": (m.text or "")[:200]}
                for m in mems
            ]
        except Exception as e:
            memories_payload = [{"error": str(e)}]

    payload = {
        "session_id": session_id,
        "core_self": core_payload,
        "relation_version": state.relation_version,
        "policy_view": policy_view,
        "beliefs": [
            {
                "id": b.id,
                "kind": b.kind,
                "key": b.key,
                "strength": b.strength,
                "value": b.value,
                "evidence_event_id": b.evidence_event_id,
                "created_at": b.created_at,
                "updated_at": b.updated_at,
            }
            for b in beliefs
        ],
        "memories": memories_payload,
    }

    # slim=0 时把全量 policy 一并带上（默认不带，避免爆屏）
    if slim is not None and int(slim) == 0:
        payload["policy"] = policy

    return JSONResponse(
        content=jsonable_encoder(payload),
        media_type="application/json; charset=utf-8",
    )


@router.get("/sessions/{session_id}/state")
def debug_state(
    session_id: str,
    slim: int | None = Query(default=None, description="slim=1 只返回 policy_view（推荐）"),
    db: Session = Depends(get_db),
):
    state = get_or_create_state(db, session_id)
    policy = _safe_json_loads(state.policy_json)
    policy_view = _build_policy_view(policy)

    if slim is not None and int(slim) == 1:
        payload = {
            "session_id": state.session_id,
            "relation_version": state.relation_version,
            "policy_view": policy_view,
            "updated_at": state.updated_at,
        }
    else:
        # 向后兼容：保留 policy_json（你原来的 PowerShell 用法不变）
        payload = {
            "session_id": state.session_id,
            "relation_version": state.relation_version,
            "policy_json": state.policy_json,
            "policy": policy,
            "policy_view": policy_view,
            "updated_at": state.updated_at,
        }

    return JSONResponse(
        content=jsonable_encoder(payload),
        media_type="application/json; charset=utf-8",
    )


@router.get("/sessions/{session_id}/beliefs")
def debug_beliefs(session_id: str, db: Session = Depends(get_db)):
    bs = list_active_beliefs(db, session_id, limit=200)
    payload = [
        {
            "id": b.id,
            "kind": b.kind,
            "key": b.key,
            "value": b.value,
            "strength": b.strength,
            "status": b.status,
            "evidence_event_id": b.evidence_event_id,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
        }
        for b in bs
    ]
    return JSONResponse(
        content=jsonable_encoder(payload),
        media_type="application/json; charset=utf-8",
    )
