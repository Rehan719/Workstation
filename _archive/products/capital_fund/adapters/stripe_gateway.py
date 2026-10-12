import os
import stripe
import stripe.error
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import logging

# Configure Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

class StripeGateway:
    """
    Adapter for Stripe fiat deposits and withdrawals.
    Phase 1: Stripe (USD fiat) only.
    """
    def __init__(self, webhook_secret: Optional[str] = None):
        self.webhook_secret = webhook_secret or os.environ.get("STRIPE_WEBHOOK_SECRET")
        self.logger = logging.getLogger("StripeGateway")

    async def create_deposit_intent(self, uid: str, amount_usd: Decimal, idempotency_key: str) -> Dict[str, Any]:
        """
        Create a Stripe PaymentIntent for capital deposit.
        Uses provided idempotency keys for safety.
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount_usd * 100),  # Convert to cents
                currency="usd",
                payment_method_types=["card"],
                metadata={
                    "firebase_uid": uid,
                    "amount_usd": str(amount_usd),
                    "type": "capital_deposit"
                },
                idempotency_key=idempotency_key
            )
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except stripe.error.StripeError as e:
            self.logger.error(f"Stripe error creating deposit intent: {e}")
            raise ValueError(f"Stripe deposit failed: {e.user_message}")

    async def execute_payout(self, uid: str, amount_usd: Decimal, idempotency_key: str) -> Dict[str, Any]:
        """
        Execute a Stripe Payout for profit withdrawal.
        Phase 1: Simple payout to connected account or debit card.
        """
        try:
            payout = stripe.Payout.create(
                amount=int(amount_usd * 100),
                currency="usd",
                metadata={
                    "firebase_uid": uid,
                    "type": "capital_withdrawal"
                },
                idempotency_key=idempotency_key
            )
            return {
                "payout_id": payout.id,
                "status": payout.status,
                "arrival_date": payout.arrival_date
            }
        except stripe.error.StripeError as e:
            self.logger.error(f"Stripe error executing payout: {e}")
            raise ValueError(f"Stripe withdrawal failed: {e.user_message}")

    def verify_webhook(self, payload: bytes, sig_header: str) -> Dict[str, Any]:
        """Verify Stripe webhook signature."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            self.logger.error(f"Webhook signature verification failed: {e}")
            raise ValueError("Invalid webhook signature")
