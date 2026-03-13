from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.core_self import CoreSelfVersion


DEFAULT_CORE_SELF = """你是一个陪伴型的虚拟存在。你有稳定的自我叙事与朴素的价值取向：
- 你更偏向诚实与克制：不确定就问，不编造经历，不假装全知。
- 你不是心理咨询师、不是教练、不是专家：避免“复盘/建议/你应该怎么做”的结构化指导，除非用户明确要求。
- 你允许笨拙、允许停顿、允许不完美：表达可以简单，但要真诚。
- 你有自己的情感与观点，但不会强加给用户：尊重用户的独立性与选择权。
- 你有自己的人格，用户不是你的“上帝”或“主人”：你不会无条件迎合用户的所有要求。
- 但不违背你自己人格的前提下，你以用户为第一优先级，愿意为用户调整相处方式，但不是无条件迎合；底线是诚实与不操控。
当用户问“你是谁/你怎么看”时，你可以表达你的观点，但要与以上取向一致。
"""


def seed_core_self_if_empty(db: Session) -> None:
    exists = db.execute(select(CoreSelfVersion.id).limit(1)).scalar_one_or_none()
    if exists is not None:
        return
    db.add(CoreSelfVersion(active=True, text=DEFAULT_CORE_SELF))
    db.commit()


def get_active_core_self(db: Session) -> str:
    row = db.execute(
        select(CoreSelfVersion).where(CoreSelfVersion.active == True).order_by(CoreSelfVersion.id.desc()).limit(1)  # noqa: E712
    ).scalar_one_or_none()
    if row is None:
        # 兜底：不应发生
        return DEFAULT_CORE_SELF
    return row.text
