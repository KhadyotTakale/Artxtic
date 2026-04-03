"""Subscription models — `subscription_plans` and `subscriptions` tables."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.snowflake import generate_id


class SubscriptionPlan(Base):
    """Available subscription tiers."""

    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=generate_id)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    dodopayments_plan_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    price_monthly: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_yearly: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    image_limit_monthly: Mapped[int] = mapped_column(default=0, nullable=False)
    video_limit_monthly: Mapped[int] = mapped_column(default=0, nullable=False)
    features: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
    )

    subscriptions = relationship("Subscription", back_populates="plan", lazy="selectin")

    def __repr__(self) -> str:
        return f"<SubscriptionPlan id={self.id} name={self.name}>"


class Subscription(Base):
    """User's active subscription record."""

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=generate_id)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    plan_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("subscription_plans.id"), nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="active",
    )  # active, cancelled, expired, trial
    dodopayments_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dodopayments_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
    )

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"<Subscription id={self.id} user_id={self.user_id} status={self.status}>"
