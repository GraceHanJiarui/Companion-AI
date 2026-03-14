import argparse
import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.event import TurnEvent


def _build_sample(turn_event: TurnEvent) -> dict | None:
    tone_eval = turn_event.tone_eval or {}
    if not isinstance(tone_eval, dict):
        return None

    input_obj = tone_eval.get("input")
    target_obj = tone_eval.get("target")
    meta_obj = tone_eval.get("meta")

    if not isinstance(input_obj, dict) or not isinstance(target_obj, dict):
        return None

    delta_r = target_obj.get("delta_R")
    confidence = target_obj.get("confidence")
    if not isinstance(delta_r, dict):
        return None

    required_keys = ["bond", "care", "trust", "stability"]
    if any(k not in delta_r for k in required_keys):
        return None
    if confidence is None:
        return None

    sample = {
        "input": {
            "user_text": input_obj.get("user_text", ""),
            "prev_rel_effective": input_obj.get("prev_rel_effective") or {},
        },
        "target": {
            "delta_R": {k: delta_r.get(k) for k in required_keys},
            "confidence": confidence,
        },
        "meta": {
            "turn_event_id": turn_event.id,
            "session_id": turn_event.session_id,
            "created_at": turn_event.created_at.isoformat() if turn_event.created_at else None,
            **(meta_obj if isinstance(meta_obj, dict) else {}),
        },
    }
    return sample


def _render_training_input(input_obj: dict) -> str:
    user_text = str(input_obj.get("user_text", "") or "")
    prev_rel = input_obj.get("prev_rel_effective") or {}

    bond = prev_rel.get("bond", 0.0)
    care = prev_rel.get("care", 0.0)
    trust = prev_rel.get("trust", 0.0)
    stability = prev_rel.get("stability", 0.0)

    return (
        f"User: {user_text}\n"
        f"PrevRelEffective: bond={bond:.4f} care={care:.4f} trust={trust:.4f} stability={stability:.4f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="tone_dataset.jsonl")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        stmt = select(TurnEvent).order_by(TurnEvent.id.asc())
        if args.limit > 0:
            stmt = stmt.limit(args.limit)
        rows = db.execute(stmt).scalars().all()
    finally:
        db.close()

    output_path = Path(args.output)
    count = 0
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            sample = _build_sample(row)
            if sample is None:
                continue
            sample["training_input"] = _render_training_input(sample["input"])
            sample["target_vector"] = [
                sample["target"]["delta_R"]["bond"],
                sample["target"]["delta_R"]["care"],
                sample["target"]["delta_R"]["trust"],
                sample["target"]["delta_R"]["stability"],
                sample["target"]["confidence"],
            ]
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            count += 1

    print(json.dumps({"ok": True, "output": str(output_path), "count": count}, ensure_ascii=False))


if __name__ == "__main__":
    main()
