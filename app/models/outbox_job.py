from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OutboxJob(Base):
    __tablename__ = "outbox_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # e.g. "belief_extractor_llm"
    kind: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    # "pending" | "processing" | "done" | "failed"
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending", index=True)

    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
