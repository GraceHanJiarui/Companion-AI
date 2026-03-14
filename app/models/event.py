from sqlalchemy import String, Text, DateTime, func, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    actor: Mapped[str] = mapped_column(String(16), index=True)  # "user" | "ai" | "system"
    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

class TurnEvent(Base):
    __tablename__ = "turn_events"

    id = mapped_column(Integer, primary_key=True)

    session_id = mapped_column(String, index=True)

    user_text = mapped_column(Text, nullable=False)
    assistant_text = mapped_column(Text, nullable=False)

    # Actor 控制快照（你想要的）
    behavior = mapped_column(JSON, nullable=False)
    scene = mapped_column(String, nullable=True)
    tone_eval = mapped_column(JSON, nullable=True)

    # 可选：调试 / 审计
    # trace_id = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
