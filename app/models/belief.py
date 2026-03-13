from sqlalchemy import String, Text, DateTime, func, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Belief(Base):
    __tablename__ = "beliefs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)

    kind: Mapped[str] = mapped_column(String(32))  # boundary/preference/style/relationship
    key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    value: Mapped[str] = mapped_column(Text)
    strength: Mapped[float] = mapped_column(Float, default=0.7)

    status: Mapped[str] = mapped_column(String(32), default="active")  # active/superseded/revoked
    evidence_event_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_memory_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supersedes_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
