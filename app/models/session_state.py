from sqlalchemy import String, DateTime, func, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SessionState(Base):
    __tablename__ = "session_state"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    relation_version: Mapped[int] = mapped_column(Integer, default=1)
    policy_json: Mapped[str] = mapped_column(Text, default="{}")

    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
