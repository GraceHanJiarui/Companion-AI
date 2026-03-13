from __future__ import annotations

import re
from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, literal
from sqlalchemy import text
from pgvector.sqlalchemy import Vector

from app.models.event import Event
from app.models.memory import Memory
from app.memory.embedder import Embedder
from app.core.llm_client import LLMClient

_embedder = Embedder()
_llm = LLMClient()


# --- 1) 边界/否定类过滤（MVP 规则，不上 ML） ---
_BOUNDARY_PATTERNS = [
    r"我不喜欢",
    r"我讨厌",
    r"别这样",
    r"我想(要|不想)",
    r"不要(再)?(这样|问|说)",
    r"可以不要",
    r"你别",
    r"别问",
    r"别说",
    r"别提",
]
_boundary_re = re.compile("|".join(_BOUNDARY_PATTERNS))


def should_write_episodic_memory(user_text: str) -> bool:
    """过滤：边界/否定类反馈先不进 episodic memory（Milestone 4 再进 beliefs）。"""
    t = (user_text or "").strip()
    if len(t) < 12:
        return False
    if _boundary_re.search(t):
        return False
    return True


# --- 2) 向量检索（纯 cosine top-k） ---
async def retrieve_memories(db: Session, session_id: str, query: str, k: int = 5) -> list[Memory]:
    raw = await _embedder.embed(query)

    # --- HARD ASSERT: raw 必须是 list ---
    if isinstance(raw, str):
        # 这说明 embedder 没返回向量，而是返回了文本（或者你把 raw 赋成了 query）
        raise RuntimeError(f"Embedder returned str instead of vector. raw[:50]={raw[:50]!r}")

    if not isinstance(raw, list):
        raise RuntimeError(f"Embedder returned unexpected type: {type(raw)}")

    # --- HARD CAST: list[str|float] -> list[float] ---
    try:
        q_emb = [float(x) for x in raw]
    except Exception as e:
        raise RuntimeError(f"Embedding cast failed: {e}; sample={raw[:5]!r}")

    q_vec = literal(q_emb, type_=Vector(1536))
    stmt = (
    select(Memory)
    .where(Memory.session_id == session_id)
    .order_by(Memory.embedding.op("<=>")(q_vec))
    .limit(k)
)
    return db.execute(stmt).scalars().all()



# --- 3) 写入 memory（写“摘要记忆”） ---
async def write_memory_summary(
    db: Session,
    session_id: str,
    summary_text: str,
    *,
    from_event_id: int,
    to_event_id: int,
    salience: float = 1.0,
) -> int:
    emb = [float(x) for x in await _embedder.embed(summary_text)]
    m = Memory(
        session_id=session_id,
        text=summary_text,
        embedding=emb,
        salience=salience,
        from_event_id=from_event_id,
        to_event_id=to_event_id,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m.id


def _latest_memory_to_event_id(db: Session, session_id: str) -> int | None:
    stmt = (
        select(Memory.to_event_id)
        .where(Memory.session_id == session_id)
        .order_by(desc(Memory.id))
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def _count_user_turns(db: Session, session_id: str) -> int:
    stmt = select(func.count()).select_from(Event).where(
        (Event.session_id == session_id) & (Event.actor == "user")
    )
    return int(db.execute(stmt).scalar_one())


def _get_event_window_for_last_n_user_turns(db: Session, session_id: str, n_user_turns: int) -> Sequence[Event]:
    """
    取最近 n 个 user turn 的窗口事件（包含 user/ai），按时间顺序返回。
    简化假设：每个 user 后面会跟一个 ai（你当前 chat 流程成立）。
    """
    # 先找最近 n 条 user 事件的 id（降序）
    user_stmt = (
        select(Event.id)
        .where((Event.session_id == session_id) & (Event.actor == "user"))
        .order_by(desc(Event.id))
        .limit(n_user_turns)
    )
    user_ids = db.execute(user_stmt).scalars().all()
    if not user_ids:
        return []

    from_id = min(user_ids)
    to_id_stmt = (
        select(Event.id)
        .where(Event.session_id == session_id)
        .order_by(desc(Event.id))
        .limit(1)
    )
    to_id = db.execute(to_id_stmt).scalar_one()

    # 取窗口内所有事件
    win_stmt = (
        select(Event)
        .where((Event.session_id == session_id) & (Event.id >= from_id) & (Event.id <= to_id))
        .order_by(Event.id.asc())
    )
    return db.execute(win_stmt).scalars().all()


def should_create_summary_now(db: Session, session_id: str, *, every_n_user_turns: int = 8) -> bool:
    user_turns = _count_user_turns(db, session_id)
    if user_turns == 0 or user_turns % every_n_user_turns != 0:
        return False

    latest_mem_to = _latest_memory_to_event_id(db, session_id)
    # 如果已经覆盖到当前最新事件，则不重复写
    latest_event_id = db.execute(
        select(Event.id).where(Event.session_id == session_id).order_by(desc(Event.id)).limit(1)
    ).scalar_one()

    if latest_mem_to is not None and latest_mem_to >= latest_event_id:
        return False

    return True


async def build_summary_for_last_n_turns(db: Session, session_id: str, n_user_turns: int = 8) -> tuple[str, int, int]:
    events = _get_event_window_for_last_n_user_turns(db, session_id, n_user_turns)
    if not events:
        raise RuntimeError("No events found to summarize.")

    from_event_id = events[0].id
    to_event_id = events[-1].id

    # 准备对话片段（尽量短）
    lines: list[str] = []
    for e in events:
        role = "用户" if e.actor == "user" else ("你" if e.actor == "ai" else e.actor)
        content = (e.content or "").strip()
        if content:
            lines.append(f"{role}: {content}")

    transcript = "\n".join(lines)

    # 用 LLM 生成“共同经历摘要”，注意：不要变成建议/专家
    system = (
        "你要把下面的对话片段总结成一段“共同经历摘要”。\n"
        "要求：\n"
        "1) 用非常朴素的叙述口吻，像在记一段发生过的事。\n"
        "2) 不要给建议，不要分析心理，不要复盘。\n"
        "3) 不要编造对话里没有出现的内容。\n"
        "4) 1-3 句话，尽量短。\n"
    )
    user = f"对话片段：\n{transcript}\n\n请输出共同经历摘要："

    summary = await _llm.generate(system=system, user=user)
    summary = summary.strip()

    return summary, from_event_id, to_event_id
