import os
from fastapi import Request, HTTPException, APIRouter
import stripe
from firebase_admin import firestore
from datetime import datetime, timedelta

router = APIRouter(prefix="/stripe")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")
db = firestore.client()

@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    ARTICLE 1121: Idempotent Webhook Processing.
    Ensures absolute consistency between Stripe and Workstation State.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_placeholder")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_id = event["id"]
    if db.collection("webhook_events").document(event_id).get().exists:
        return {"status": "ok", "message": "idempotent"}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"]["firebase_uid"]
        db.collection("subscriptions").document(uid).set({
            "status": "active",
            "plan": "pro", # Default pro for first month
            "trial_end": datetime.utcnow() + timedelta(days=30),
            "stripe_customer_id": session["customer"],
            "stripe_subscription_id": session["subscription"],
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        docs = db.collection("subscriptions").where("stripe_subscription_id", "==", sub["id"]).stream()
        for doc in docs:
            db.collection("subscriptions").document(doc.id).update({
                "status": "canceled",
                "plan": "free",
                "updated_at": firestore.SERVER_TIMESTAMP
            })

    db.collection("webhook_events").document(event_id).set({
        "processed_at": firestore.SERVER_TIMESTAMP,
        "type": event["type"]
    })
    return {"status": "ok"}
