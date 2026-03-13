from __future__ import annotations

from dataclasses import dataclass
from sqlalchemy import select, desc, update
from sqlalchemy.orm import Session

from app.models.belief import Belief
from app.beliefs.extract import BeliefCandidate


@dataclass
class AddBeliefResult:
    belief_id: int
    created: bool
    duplicate_of_id: int | None = None
    duplicate_reason: str | None = None  # "same_key" / "same_value"


def list_active_beliefs(db: Session, session_id: str, limit: int = 50) -> list[Belief]:
    stmt = (
        select(Belief)
        .where((Belief.session_id == session_id) & (Belief.status == "active"))
        .order_by(desc(Belief.updated_at), desc(Belief.id))
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def add_belief(
    db: Session,
    session_id: str,
    cand: BeliefCandidate,
    *,
    evidence_event_id: int | None = None,
    evidence_memory_id: int | None = None,
) -> AddBeliefResult:
    # 1) same_value 去重（优先，避免重复插入同一句）
    same_value = db.execute(
        select(Belief).where(
            (Belief.session_id == session_id)
            & (Belief.kind == cand.kind)
            & (Belief.value == cand.value)
            & (Belief.status == "active")
        ).order_by(desc(Belief.id)).limit(1)
    ).scalar_one_or_none()

    if same_value is not None:
        return AddBeliefResult(
            belief_id=same_value.id,
            created=False,
            duplicate_of_id=same_value.id,
            duplicate_reason="same_value",
        )

    # 2) 同 key 的 supersede（把所有 active 都 supersede，避免双活）
    supersedes_id = None
    if cand.key:
        prevs = db.execute(
            select(Belief).where(
                (Belief.session_id == session_id)
                & (Belief.kind == cand.kind)
                & (Belief.key == cand.key)
                & (Belief.status == "active")
            )
        ).scalars().all()

        if prevs:
            supersedes_id = prevs[-1].id
            for p in prevs:
                db.execute(update(Belief).where(Belief.id == p.id).values(status="superseded"))

    # 3) 插入新 belief
    b = Belief(
        session_id=session_id,
        kind=cand.kind,
        key=cand.key,
        value=cand.value,
        strength=cand.strength,
        status="active",
        evidence_event_id=evidence_event_id,
        evidence_memory_id=evidence_memory_id,
        supersedes_id=supersedes_id,
    )
    db.add(b)
    db.commit()
    db.refresh(b)

    # 若同 key 有历史，这次属于“更新”（但不是 duplicate），ack 是否触发由上层决定
    return AddBeliefResult(belief_id=b.id, created=True)
