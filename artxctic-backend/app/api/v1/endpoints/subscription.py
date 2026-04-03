"""Subscription API endpoints (7 endpoints + webhook)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_active_verified_user, get_current_user
from app.core.snowflake import generate_id
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.usage import UsageLimit
from app.models.user import User
from app.schemas.subscription import (
    CancelSubscriptionRequest,
    CheckoutRequest,
    CheckoutResponse,
    PortalResponse,
    SubscriptionPlanResponse,
    SubscriptionResponse,
)
from app.services.payment_service import PaymentService
from app.services.usage_service import UsageService
from app.utils.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Subscription"])


# ── 23. GET /subscription/plans ─────────────────────────────────
@router.get("/subscription/plans")
async def get_plans(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Get all active subscription plans (public endpoint)."""
    result = await db.execute(
        select(SubscriptionPlan)
        .where(SubscriptionPlan.is_active == True)  # noqa: E712
        .order_by(SubscriptionPlan.price_monthly.asc().nulls_first())
    )
    plans = result.scalars().all()

    return {
        "success": True,
        "data": [
            SubscriptionPlanResponse(
                id=str(p.id),
                name=p.name,
                price_monthly=float(p.price_monthly) if p.price_monthly else None,
                price_yearly=float(p.price_yearly) if p.price_yearly else None,
                image_limit_monthly=p.image_limit_monthly,
                video_limit_monthly=p.video_limit_monthly,
                features=p.features,
                is_active=p.is_active,
            ).model_dump()
            for p in plans
        ],
    }


# ── 23b. GET /subscription/current ──────────────────────────────
@router.get("/subscription/current", response_model=SubscriptionResponse)
async def get_current_subscription(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SubscriptionResponse:
    """Get the current user's subscription details and usage."""
    # Get active subscription
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    # Defaults for free tier
    plan_name = "Free"
    image_limit = 10
    video_limit = 2
    sub_status = "none"
    current_period_end = None
    cancel_at_period_end = False
    sub_id = None

    if subscription:
        sub_status = subscription.status
        sub_id = str(subscription.id)
        current_period_end = subscription.current_period_end
        cancel_at_period_end = subscription.cancel_at_period_end

        if subscription.plan_id:
            plan_result = await db.execute(
                select(SubscriptionPlan).where(SubscriptionPlan.id == subscription.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_name = plan.name
                image_limit = plan.image_limit_monthly
                video_limit = plan.video_limit_monthly

    # Get usage
    usage_result = await db.execute(
        select(UsageLimit).where(UsageLimit.user_id == current_user.id)
    )
    usage = usage_result.scalar_one_or_none()

    return SubscriptionResponse(
        id=sub_id,
        status=sub_status,
        plan_name=plan_name,
        current_period_end=current_period_end,
        cancel_at_period_end=cancel_at_period_end,
        image_count=usage.image_count if usage else 0,
        video_count=usage.video_count if usage else 0,
        image_limit=image_limit,
        video_limit=video_limit,
    )


# ── 24. POST /subscription/checkout ─────────────────────────────
@router.post("/subscription/checkout", response_model=CheckoutResponse)
async def create_checkout(
    body: CheckoutRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> CheckoutResponse:
    """Create a Dodopayments checkout session."""
    # Verify plan exists
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == int(body.plan_id))
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise NotFoundError("Subscription plan")
    if not plan.dodopayments_plan_id:
        raise ValidationError("This plan is not available for purchase (free tier)")

    # Determine the product ID based on billing cycle
    # The dodopayments_plan_id in the database stores the product ID
    product_id = plan.dodopayments_plan_id

    payment_service = PaymentService()
    try:
        checkout_data = await payment_service.create_checkout_session(
            product_id=product_id,
            customer_email=current_user.email,
            customer_name=current_user.name,
            return_url=settings.DODOPAYMENTS_SUCCESS_URL,
            metadata={
                "user_id": str(current_user.id),
                "plan_id": str(plan.id),
                "billing_cycle": body.billing_cycle,
            },
        )
    except Exception as e:
        logger.error("Dodopayments checkout failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Payment provider error: {str(e)}",
        )

    return CheckoutResponse(
        checkout_url=checkout_data["checkout_url"],
        session_id=checkout_data.get("session_id", ""),
    )


# ── 24b. POST /subscription/cancel ──────────────────────────────
@router.post("/subscription/cancel")
async def cancel_subscription(
    body: CancelSubscriptionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> dict:
    """Cancel the current user's subscription."""
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.status == "active",
        ).order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        raise NotFoundError("No active subscription found")

    if not subscription.dodopayments_subscription_id:
        raise ValidationError("Subscription has no payment record to cancel")

    # Cancel via Dodopayments SDK
    payment_service = PaymentService()
    await payment_service.cancel_subscription(
        subscription.dodopayments_subscription_id,
        at_period_end=body.at_period_end,
    )

    # Update local record
    subscription.cancel_at_period_end = body.at_period_end
    if not body.at_period_end:
        subscription.status = "cancelled"
    await db.flush()

    return {
        "success": True,
        "message": (
            "Subscription will be cancelled at period end"
            if body.at_period_end
            else "Subscription cancelled immediately"
        ),
    }


# ── 24c. POST /subscription/reactivate ──────────────────────────
@router.post("/subscription/reactivate")
async def reactivate_subscription(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> dict:
    """Reactivate a subscription that was scheduled for cancellation."""
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.cancel_at_period_end == True,  # noqa: E712
        ).order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        raise NotFoundError("No cancellation-pending subscription found")

    if not subscription.dodopayments_subscription_id:
        raise ValidationError("Subscription has no payment record to reactivate")

    # Reactivate via Dodopayments SDK
    payment_service = PaymentService()
    await payment_service.reactivate_subscription(
        subscription.dodopayments_subscription_id,
    )

    # Update local record
    subscription.cancel_at_period_end = False
    subscription.status = "active"
    await db.flush()

    return {"success": True, "message": "Subscription reactivated successfully"}


# ── 25. POST /webhooks/dodopayments ─────────────────────────────
@router.post("/webhooks/dodopayments", status_code=status.HTTP_200_OK)
async def handle_webhook(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Handle Dodopayments webhook events.

    Verifies the webhook signature using the SDK's standardwebhooks integration,
    then processes subscription lifecycle events.
    """
    raw_body = await request.body()
    body_str = raw_body.decode("utf-8")

    # Extract webhook headers
    headers = {
        "webhook-id": request.headers.get("webhook-id", ""),
        "webhook-signature": request.headers.get("webhook-signature", ""),
        "webhook-timestamp": request.headers.get("webhook-timestamp", ""),
    }

    # Verify and parse webhook using the SDK
    payment_service = PaymentService()
    try:
        event = payment_service.verify_and_parse_webhook(body_str, headers=headers)
    except Exception as e:
        logger.error("Webhook verification failed: %s", str(e))
        # Fall back to parsing without verification if webhook key is not configured
        if not settings.DODOPAYMENTS_WEBHOOK_KEY or settings.DODOPAYMENTS_WEBHOOK_KEY == "your-dodo-webhook-key":
            logger.warning("Webhook key not configured — processing without verification")
            import json
            event = json.loads(body_str)
        else:
            return {"success": False, "error": "Invalid webhook signature"}

    event_type = event.get("type", event.get("event_type", "unknown"))
    data = event.get("data", event)

    logger.info("Processing webhook event: %s", event_type)

    # ── subscription.active — new subscription created/activated ──
    if event_type in ("subscription.active", "subscription.created"):
        await _handle_subscription_activated(db, data)

    # ── subscription.renewed — recurring payment succeeded ───────
    elif event_type == "subscription.renewed":
        await _handle_subscription_renewed(db, data)

    # ── subscription.cancelled — user cancelled ─────────────────
    elif event_type in ("subscription.cancelled", "subscription.canceled"):
        await _handle_subscription_cancelled(db, data)

    # ── subscription.expired — subscription ended ────────────────
    elif event_type in ("subscription.expired", "subscription.failed"):
        await _handle_subscription_expired(db, data)

    # ── payment.failed — payment processing failed ──────────────
    elif event_type in ("payment.failed", "subscription.payment_failed"):
        await _handle_payment_failed(db, data)

    else:
        logger.info("Unhandled webhook event type: %s", event_type)

    return {"success": True, "received": True}


# ── Webhook Handlers ────────────────────────────────────────────

async def _handle_subscription_activated(db: AsyncSession, data: dict) -> None:
    """Handle new subscription activation from webhook."""
    dodo_sub_id = data.get("subscription_id", "")
    dodo_customer_id = data.get("customer_id", data.get("customer", {}).get("customer_id", ""))
    dodo_product_id = data.get("product_id", "")
    customer_email = data.get("customer", {}).get("email", data.get("customer_email", ""))
    period_start = data.get("current_period_start")
    period_end = data.get("current_period_end")

    # Find the plan by Dodopayments product/plan ID
    plan = None
    if dodo_product_id:
        plan_result = await db.execute(
            select(SubscriptionPlan).where(
                SubscriptionPlan.dodopayments_plan_id == dodo_product_id
            )
        )
        plan = plan_result.scalar_one_or_none()

    # Find user by email or customer ID
    user = None

    # Try via metadata user_id first
    metadata = data.get("metadata", {})
    user_id_str = metadata.get("user_id")
    if user_id_str:
        user_result = await db.execute(
            select(User).where(User.id == int(user_id_str))
        )
        user = user_result.scalar_one_or_none()

    # Fall back to email lookup
    if not user and customer_email:
        user_result = await db.execute(select(User).where(User.email == customer_email))
        user = user_result.scalar_one_or_none()

    # Fall back to dodopayments_customer_id lookup
    if not user and dodo_customer_id:
        user_result = await db.execute(
            select(User).where(User.dodopayments_customer_id == dodo_customer_id)
        )
        user = user_result.scalar_one_or_none()

    if not user:
        logger.error("Webhook: cannot find user for customer %s / %s", dodo_customer_id, customer_email)
        return

    # Store dodopayments_customer_id on user
    if dodo_customer_id and not user.dodopayments_customer_id:
        user.dodopayments_customer_id = dodo_customer_id

    # Check for existing subscription
    sub_result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user.id,
        ).order_by(Subscription.created_at.desc())
    )
    existing = sub_result.scalar_one_or_none()

    now = datetime.now(timezone.utc)

    if existing:
        existing.plan_id = plan.id if plan else existing.plan_id
        existing.status = "active"
        existing.dodopayments_customer_id = dodo_customer_id
        existing.dodopayments_subscription_id = dodo_sub_id
        existing.cancel_at_period_end = False
        existing.current_period_start = period_start or now
        existing.current_period_end = period_end
        sub_id = existing.id
    else:
        sub = Subscription(
            id=generate_id(),
            user_id=user.id,
            plan_id=plan.id if plan else None,
            status="active",
            dodopayments_customer_id=dodo_customer_id,
            dodopayments_subscription_id=dodo_sub_id,
            current_period_start=period_start or now,
            current_period_end=period_end,
        )
        db.add(sub)
        sub_id = sub.id

    await db.flush()

    # Initialize usage limits
    usage_service = UsageService(db)
    await usage_service.initialize_usage(user.id, sub_id)

    logger.info("Subscription activated for user %d (sub=%s)", user.id, dodo_sub_id)


async def _handle_subscription_renewed(db: AsyncSession, data: dict) -> None:
    """Handle subscription renewal (recurring payment succeeded)."""
    dodo_sub_id = data.get("subscription_id", "")
    period_start = data.get("current_period_start")
    period_end = data.get("current_period_end")

    result = await db.execute(
        select(Subscription).where(
            Subscription.dodopayments_subscription_id == dodo_sub_id
        )
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        logger.warning("Webhook renewal: subscription %s not found", dodo_sub_id)
        return

    now = datetime.now(timezone.utc)
    subscription.status = "active"
    subscription.cancel_at_period_end = False
    subscription.current_period_start = period_start or now
    subscription.current_period_end = period_end
    await db.flush()

    # Reset monthly usage
    usage_service = UsageService(db)
    await usage_service.reset_monthly_usage(subscription.user_id)

    logger.info("Subscription renewed for user %d", subscription.user_id)


async def _handle_subscription_cancelled(db: AsyncSession, data: dict) -> None:
    """Handle subscription cancellation."""
    dodo_sub_id = data.get("subscription_id", "")

    await db.execute(
        update(Subscription)
        .where(Subscription.dodopayments_subscription_id == dodo_sub_id)
        .values(status="cancelled", cancel_at_period_end=True)
    )
    await db.flush()
    logger.info("Subscription cancelled: %s", dodo_sub_id)


async def _handle_subscription_expired(db: AsyncSession, data: dict) -> None:
    """Handle subscription expiration."""
    dodo_sub_id = data.get("subscription_id", "")

    await db.execute(
        update(Subscription)
        .where(Subscription.dodopayments_subscription_id == dodo_sub_id)
        .values(status="expired")
    )
    await db.flush()
    logger.info("Subscription expired: %s", dodo_sub_id)


async def _handle_payment_failed(db: AsyncSession, data: dict) -> None:
    """Handle failed payment."""
    dodo_sub_id = data.get("subscription_id", "")

    await db.execute(
        update(Subscription)
        .where(Subscription.dodopayments_subscription_id == dodo_sub_id)
        .values(status="expired")
    )
    await db.flush()
    logger.info("Payment failed for subscription: %s", dodo_sub_id)


# ── 26. GET /subscription/portal ─────────────────────────────────
@router.get("/subscription/portal", response_model=PortalResponse)
async def get_portal(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> PortalResponse:
    """Get the Dodopayments customer portal URL."""
    # Try getting customer ID from user record first
    customer_id = current_user.dodopayments_customer_id

    # Fall back to subscription record
    if not customer_id:
        result = await db.execute(
            select(Subscription).where(
                Subscription.user_id == current_user.id,
                Subscription.dodopayments_customer_id.isnot(None),
            ).order_by(Subscription.created_at.desc())
        )
        subscription = result.scalar_one_or_none()
        if subscription:
            customer_id = subscription.dodopayments_customer_id

    if not customer_id:
        raise NotFoundError("No Dodopayments customer record found. Please subscribe first.")

    payment_service = PaymentService()
    portal_url = await payment_service.get_customer_portal_url(customer_id)

    return PortalResponse(portal_url=portal_url)
