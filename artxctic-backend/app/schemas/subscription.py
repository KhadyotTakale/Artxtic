"""Subscription request/response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SubscriptionPlanResponse(BaseModel):
    """A single subscription plan."""
    id: str
    name: str
    price_monthly: float | None = None
    price_yearly: float | None = None
    image_limit_monthly: int = 0
    video_limit_monthly: int = 0
    features: dict[str, Any] | None = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class CheckoutRequest(BaseModel):
    """Create a Dodopayments checkout session."""
    plan_id: str
    billing_cycle: str = "monthly"  # monthly or yearly


class CheckoutResponse(BaseModel):
    """Dodopayments checkout session URL."""
    checkout_url: str
    session_id: str


class SubscriptionResponse(BaseModel):
    """Current user's subscription details with usage info."""
    id: str | None = None
    status: str = "none"  # active, cancelled, expired, none
    plan_name: str = "Free"
    current_period_end: datetime | None = None
    cancel_at_period_end: bool = False
    image_count: int = 0
    video_count: int = 0
    image_limit: int = 10
    video_limit: int = 2


class CancelSubscriptionRequest(BaseModel):
    """Cancel subscription options."""
    at_period_end: bool = True


class WebhookEvent(BaseModel):
    """Incoming Dodopayments webhook payload."""
    event_type: str
    data: dict[str, Any]


class PortalResponse(BaseModel):
    """Customer portal URL."""
    portal_url: str
