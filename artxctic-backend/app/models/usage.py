"""Usage limits model — `usage_limits` table."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.snowflake import generate_id


class UsageLimit(Base):
    """Monthly usage counters per user, tied to their subscription."""

    __tablename__ = "usage_limits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=generate_id)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True,
    )
    subscription_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("subscriptions.id"), nullable=True,
    )
    image_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    video_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reset_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
    )

    user = relationship("User", back_populates="usage_limit")

    def __repr__(self) -> str:
        return f"<UsageLimit user_id={self.user_id} images={self.image_count} videos={self.video_count}>"
