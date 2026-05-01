import os
import stripe
from fastapi import APIRouter, HTTPException
from firebase_admin import auth, firestore
from datetime import datetime, timedelta

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")
db = firestore.client()
router = APIRouter(prefix="/stripe")

@router.post("/create-checkout-session")
async def create_checkout_session(uid: str, price_id: str, success_url: str, cancel_url: str):
    """
    ARTICLE 1120: Sovereign Commercial Integration.
    Creates a Stripe Checkout Session with a 30-day free trial.
    """
    try:
        user = auth.get_user(uid)
        sub_doc = db.collection("subscriptions").document(uid).get()
        if sub_doc.exists and sub_doc.to_dict().get("status") == "active":
            return {"status": "already_active", "message": "User already has an active subscription."}

        trial_end = int((datetime.utcnow() + timedelta(days=30)).timestamp())
        session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            subscription_data={
                "trial_settings": {"end_behavior": {"deleted": True}},
                "trial_end": trial_end
            },
            metadata={"firebase_uid": uid}
        )
        return {"sessionId": session.id, "url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
