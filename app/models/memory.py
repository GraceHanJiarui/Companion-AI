from sqlalchemy import String, Text, DateTime, func, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)

    # 摘要记忆文本（episodic）
    text: Mapped[str] = mapped_column(Text)

    # 向量
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    # 重要性（MVP 先固定 1.0）
    salience: Mapped[float] = mapped_column(Float, default=1.0)

    # 这条摘要覆盖到的事件范围（用于避免重复写入）
    from_event_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    to_event_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
