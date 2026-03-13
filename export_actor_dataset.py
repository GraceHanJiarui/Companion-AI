import json
from collections import defaultdict
from typing import Dict, Any, List

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ========= 配置区 =========

DATABASE_URL = "postgresql+psycopg://app:app@localhost:5432/companion"

OUTPUT_PATH = "actor_dataset.jsonl"

# core_self 你现在是 prompt 拼接的，这里给一个稳定短版
CORE_SELF_PREVIEW = (
    "我是一个以用户利益为先的陪伴型存在。"
    "我会提供可执行的帮助，不操控、不诱导依赖，"
    "并尊重你的边界与自由选择。"
)

# ========= 数据库 =========

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def load_events(db) -> Dict[str, List[Dict[str, Any]]]:
    """
    按 session_id 聚合 events，按时间排序
    """
    rows = db.execute(
        text("""
        SELECT session_id, actor, content, created_at
        FROM events
        ORDER BY session_id, created_at
        """)
    ).fetchall()

    sessions = defaultdict(list)
    for r in rows:
        sessions[r.session_id].append({
            "actor": r.actor,
            "content": r.content,
            "created_at": r.created_at
        })
    return sessions


def load_session_states(db):
    rows = db.execute(
        text("""
        SELECT session_id, policy_json
        FROM session_state
        """)
    ).fetchall()

    states = {}
    for r in rows:
        try:
            states[r.session_id] = json.loads(r.policy_json)
        except Exception:
            continue
    return states



def extract_actor_samples(events_by_session, states_by_session):
    samples = []

    for session_id, events in events_by_session.items():
        state = states_by_session.get(session_id)
        if not state:
            continue

        controller = state.get("_last_controller")
        if not controller:
            continue

        plan = controller.get("plan")
        behavior = plan.get("behavior") if plan else None
        hard_constraints = plan.get("hard_constraints") if plan else None
        selected_memories = plan.get("selected_memories", []) if plan else []

        if not behavior or not hard_constraints:
            continue

        # 取 user -> ai 对
        for i in range(len(events) - 1):
            if events[i]["actor"] != "user":
                continue
            if events[i + 1]["actor"] != "ai":
                continue

            user_text = events[i]["content"].strip()
            assistant_text = events[i + 1]["content"].strip()

            sample = {
                "id": f"{session_id}-{i}",
                "input": {
                    "user_text": user_text,
                    "core_self_preview": CORE_SELF_PREVIEW,
                    "active_boundary_keys": hard_constraints.get("boundary_keys", []),
                    "selected_memories_preview": [
                        {"preview": m.get("preview", "")}
                        for m in selected_memories
                        if "preview" in m
                    ],
                    "plan": {
                        "behavior": behavior,
                        "hard_constraints": hard_constraints,
                        "notes": plan.get("notes")
                    }
                },
                "output": {
                    "assistant_reply": assistant_text
                }
            }

            samples.append(sample)

    return samples


def main():
    db = Session()

    print("Loading events...")
    events_by_session = load_events(db)

    print("Loading session states...")
    states_by_session = load_session_states(db)

    print("Extracting samples...")
    samples = extract_actor_samples(events_by_session, states_by_session)

    print(f"Writing {len(samples)} samples to {OUTPUT_PATH}")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print("Done.")


if __name__ == "__main__":
    main()
