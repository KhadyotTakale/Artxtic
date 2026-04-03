"""Generation queue model — `generation_queue` table."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.snowflake import generate_id


class GenerationJob(Base):
    """A queued AI generation job."""

    __tablename__ = "generation_queue"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=generate_id)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # image, video
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False, index=True,
    )  # pending, processing, completed, failed
    fal_request_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    media_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("media.id"), nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
    )

    def __repr__(self) -> str:
        return f"<GenerationJob id={self.id} type={self.type} status={self.status}>"
