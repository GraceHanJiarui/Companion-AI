from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.outbox_job import OutboxJob


def _utcnow():
    return datetime.now(timezone.utc)


def enqueue_job(
    db: Session,
    *,
    kind: str,
    payload: dict,
    max_attempts: int = 3,
) -> OutboxJob:
    """Enqueue an outbox job.

    Design goals:
    - Minimal synchronous DB write (fast).
    - No per-request global state.
    - Caller decides idempotency strategy; this helper only writes a row.
    """
    job = OutboxJob(
        kind=kind,
        status="pending",
        attempts=0,
        max_attempts=max(1, int(max_attempts)),
        payload=payload,
        last_error=None,
        created_at=_utcnow(),
        updated_at=_utcnow(),
        locked_at=None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
