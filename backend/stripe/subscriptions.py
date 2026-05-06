import os
import stripe
import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..infrastructure.repositories import BillingRepository
from ..infrastructure.firestore_adapters import FirestoreBillingRepository

logger = logging.getLogger(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_mock")
router = APIRouter(prefix="/stripe")

def get_billing_repo() -> BillingRepository:
    return FirestoreBillingRepository()

@router.post("/create-checkout-session")
async def create_checkout_session(uid: str, price_id: str, success_url: str, cancel_url: str, repo: BillingRepository = Depends(get_billing_repo)):
    # Simple check for existing subscription
    sub = await repo.get_subscription(uid)
    if sub and sub.get("status") == "active":
         raise HTTPException(400, "Already subscribed")

    trial_end = int((datetime.utcnow() + timedelta(days=30)).timestamp())

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            subscription_data={"trial_end": trial_end},
            metadata={"firebase_uid": uid}
        )
        return {"sessionId": session.id, "url": session.url}
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, repo: BillingRepository = Depends(get_billing_repo)):
    """Race-safe, sovereignty-compliant webhook handler."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_mock")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        raise HTTPException(400, "Invalid signature")

    event_id = event["id"]

    # Atomic registration of webhook event to prevent race conditions
    if not await repo.register_webhook_event(event_id):
        return {"status": "ok"} # Already processed

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"]["firebase_uid"]

        await repo.activate_subscription(uid, {
            "status": "active",
            "plan": session.get("display_items", [{}])[0].get("price", {}).get("nickname", "pro").lower() if session.get("display_items") else "pro",
            "trial_end": datetime.utcnow() + timedelta(days=30),
            "stripe_customer_id": session["customer"],
            "stripe_subscription_id": session["subscription"]
        })

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        await repo.cancel_subscription(sub["id"])

    return {"status": "ok"}
