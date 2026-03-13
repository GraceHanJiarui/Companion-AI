from sqlalchemy import Boolean, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CoreSelfVersion(Base):
    __tablename__ = "core_self_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    text: Mapped[str] = mapped_column(Text)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
