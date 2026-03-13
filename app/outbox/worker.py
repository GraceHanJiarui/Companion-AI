from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.outbox_job import OutboxJob

from app.beliefs.extract_llm import extract_beliefs_llm
from app.beliefs.apply import apply_extractor_output
from app.beliefs.policy import get_or_create_state, _load_policy, _save_policy


POLL_INTERVAL_SECONDS = 1.0


def _utcnow():
    return datetime.now(timezone.utc)


def _claim_one_job(db: Session) -> OutboxJob | None:
    """
    Claim one pending job using SKIP LOCKED semantics.
    """
    stmt = (
        select(OutboxJob)
        .where(OutboxJob.status == "pending")
        .order_by(OutboxJob.id.asc())
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    job = db.execute(stmt).scalar_one_or_none()
    if not job:
        return None

    job.status = "processing"
    job.locked_at = _utcnow()
    job.attempts = (job.attempts or 0) + 1
    job.updated_at = _utcnow()
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


async def _process_belief_extractor_llm_job(job: OutboxJob) -> None:
    payload = job.payload
    session_id = payload["session_id"]
    user_text = payload["user_text"]
    evidence_event_id = payload["evidence_event_id"]
    model = payload.get("model", "gpt-5-nano")
    active_beliefs_text = payload.get("active_beliefs_text", "")
    policy_json = payload.get("policy_json", "{}")

    out, out_raw = await extract_beliefs_llm(
        model=model,
        user_text=user_text,
        active_beliefs_text=active_beliefs_text,
        policy_json=policy_json,
    )

    db = SessionLocal()
    try:
        apply_res = apply_extractor_output(
            db,
            session_id=session_id,
            user_text=user_text,
            evidence_event_id=evidence_event_id,
            out=out,
        )

        state = get_or_create_state(db, session_id)
        policy = _load_policy(state)
        policy["last_extractor"] = {
            "event_id": evidence_event_id,
            "ok": True,
            "error": None,
            "raw": out_raw,
            "async": True,
            "model": model,
        }
        policy["last_apply"] = {
            "event_id": evidence_event_id,
            "wrote_any": bool(apply_res.wrote_any),
            "accepted_ids": [r.belief_id for r in apply_res.add_results],
            "rejected": list(apply_res.rejected),
            "async": True,
        }
        _save_policy(db, state, policy)
        db.commit()
    finally:
        db.close()


async def run_outbox_worker_forever() -> None:
    """
    Background loop. Start once in app startup.
    """
    while True:
        db = SessionLocal()
        try:
            job = _claim_one_job(db)
        finally:
            db.close()

        if not job:
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            continue

        err = None
        try:
            if job.kind == "belief_extractor_llm":
                await _process_belief_extractor_llm_job(job)
            else:
                raise RuntimeError(f"Unknown outbox job kind: {job.kind}")
        except Exception as e:
            err = str(e)

        db2 = SessionLocal()
        try:
            fresh = db2.get(OutboxJob, job.id)
            if not fresh:
                await asyncio.sleep(0)
                continue

            fresh.updated_at = _utcnow()

            if err is None:
                fresh.status = "done"
                fresh.last_error = None
            else:
                fresh.last_error = err
                if fresh.attempts >= fresh.max_attempts:
                    fresh.status = "failed"
                else:
                    fresh.status = "pending"  # retry later

            db2.add(fresh)
            db2.commit()
        finally:
            db2.close()
