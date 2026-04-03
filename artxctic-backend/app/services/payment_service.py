"""Dodopayments integration service — uses the official AsyncDodoPayments SDK."""

from __future__ import annotations

import logging
from typing import Any

from dodopayments import AsyncDodoPayments

from app.core.config import settings

logger = logging.getLogger(__name__)


def _get_client() -> AsyncDodoPayments:
    """Create an AsyncDodoPayments client configured from settings."""
    return AsyncDodoPayments(
        bearer_token=settings.DODOPAYMENTS_API_KEY,
        webhook_key=settings.DODOPAYMENTS_WEBHOOK_KEY or None,
        environment="test_mode",
    )


class PaymentService:
    """Dodopayments subscription management via the official SDK."""

    def __init__(self) -> None:
        self.client = _get_client()

    # ── Checkout ─────────────────────────────────────────────────

    async def create_checkout_session(
        self,
        product_id: str,
        customer_email: str,
        customer_name: str | None = None,
        return_url: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a Dodopayments checkout session.

        Returns: {"checkout_url": "...", "session_id": "..."}
        """
        try:
            response = await self.client.checkout_sessions.create(
                product_cart=[
                    {
                        "product_id": product_id,
                        "quantity": 1,
                    }
                ],
                customer={
                    "email": customer_email,
                    "name": customer_name or customer_email.split("@")[0],
                },
                return_url=return_url or settings.DODOPAYMENTS_SUCCESS_URL,
                metadata=metadata,
            )
            logger.info("Checkout session created: %s", response.session_id)
            return {
                "checkout_url": response.checkout_url or "",
                "session_id": response.session_id,
            }
        except Exception as e:
            logger.error("Dodopayments checkout error: %s", str(e))
            raise

    # ── Subscriptions ────────────────────────────────────────────

    async def get_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Get subscription details from Dodopayments."""
        try:
            sub = await self.client.subscriptions.retrieve(subscription_id)
            return sub.model_dump() if hasattr(sub, "model_dump") else dict(sub)
        except Exception as e:
            logger.error("Get subscription error: %s", str(e))
            raise

    async def cancel_subscription(
        self, subscription_id: str, at_period_end: bool = True,
    ) -> dict[str, Any]:
        """Cancel a subscription.

        If at_period_end is True, it cancels at the next billing date.
        Otherwise, it cancels immediately.
        """
        try:
            if at_period_end:
                sub = await self.client.subscriptions.update(
                    subscription_id,
                    cancel_at_next_billing_date=True,
                )
            else:
                sub = await self.client.subscriptions.update(
                    subscription_id,
                    status="cancelled",
                )
            logger.info("Subscription %s cancellation requested", subscription_id)
            return sub.model_dump() if hasattr(sub, "model_dump") else dict(sub)
        except Exception as e:
            logger.error("Cancel subscription error: %s", str(e))
            raise

    async def reactivate_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Reactivate a subscription that was scheduled for cancellation."""
        try:
            sub = await self.client.subscriptions.update(
                subscription_id,
                cancel_at_next_billing_date=False,
                status="active",
            )
            logger.info("Subscription %s reactivated", subscription_id)
            return sub.model_dump() if hasattr(sub, "model_dump") else dict(sub)
        except Exception as e:
            logger.error("Reactivate subscription error: %s", str(e))
            raise

    # ── Customer Portal ──────────────────────────────────────────

    async def get_customer_portal_url(self, customer_id: str) -> str:
        """Get the Dodopayments customer portal URL."""
        try:
            portal = await self.client.customers.customer_portal.create(
                customer_id,
            )
            url = portal.link if hasattr(portal, "link") else str(portal)
            logger.info("Portal session created for customer %s", customer_id)
            return url
        except Exception as e:
            logger.error("Customer portal error: %s", str(e))
            raise

    # ── Webhook Verification ─────────────────────────────────────

    def verify_and_parse_webhook(
        self,
        payload: str,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        """Verify webhook signature and parse the event using the SDK.

        Uses client.webhooks.unwrap() which validates via standardwebhooks
        (HMAC SHA256) and returns the parsed event object.

        Args:
            payload: Raw request body as string
            headers: Request headers dict (must contain webhook-id,
                     webhook-signature, webhook-timestamp)

        Returns:
            Parsed webhook event as a dict
        """
        try:
            event = self.client.webhooks.unwrap(
                payload,
                headers=headers,
            )
            logger.info("Webhook verified: %s", getattr(event, "type", "unknown"))
            # Convert to dict for downstream processing
            if hasattr(event, "model_dump"):
                return event.model_dump()
            return dict(event)
        except Exception as e:
            logger.error("Webhook verification failed: %s", str(e))
            raise
