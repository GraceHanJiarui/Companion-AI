from __future__ import annotations

import re
from dataclasses import dataclass
from sqlalchemy.orm import Session

from app.beliefs.schema import ExtractorOutput, BeliefUpdate
from app.beliefs.store import add_belief, AddBeliefResult
from app.beliefs.extract import BeliefCandidate


_EMOTION_TOPIC_PAT = re.compile(r"(压力|情绪|心情|难受|焦虑|抑郁|崩溃|烦|累)")


@dataclass
class ApplyResult:
    wrote_any: bool
    add_results: list[AddBeliefResult]
    rejected: list[str]  # reasons (for debug)


def _normalize_key(u: BeliefUpdate) -> str | None:
    if u.key:
        return u.key
    return None


def apply_extractor_output(
    db: Session,
    *,
    session_id: str,
    user_text: str,
    evidence_event_id: int,
    out: ExtractorOutput,
) -> ApplyResult:
    rejected: list[str] = []
    add_results: list[AddBeliefResult] = []

    if not out.should_update or out.confidence < 0.6:
        return ApplyResult(wrote_any=False, add_results=[], rejected=["should_update=false or low_confidence"])

    for b in out.beliefs:
        span = (b.evidence_span or "").strip()
        if not span or span not in user_text:
            rejected.append(f"evidence_span_not_in_text: {span!r}")
            continue

        key = _normalize_key(b)

        cand = BeliefCandidate(
            kind=b.kind,
            key=key,
            value=b.value.strip(),
            strength=float(b.strength),
        )
        res = add_belief(db, session_id, cand, evidence_event_id=evidence_event_id)
        add_results.append(res)

    return ApplyResult(wrote_any=len(add_results) > 0, add_results=add_results, rejected=rejected)
