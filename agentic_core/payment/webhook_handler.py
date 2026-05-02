import os
from fastapi import Request, HTTPException, APIRouter
import stripe
from firebase_admin import firestore
from datetime import datetime, timedelta
from agentic_core.payment.billing_bridge import BillingBridge

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
db = firestore.client()
router = APIRouter(prefix="/stripe")

@router.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        raise HTTPException(400, "Invalid webhook signature")

    event_id = event["id"]
    if db.collection("webhook_events").document(event_id).get().exists:
        return {"status": "ok"}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"]["firebase_uid"]
        plan_name = "pro"
        db.collection("subscriptions").document(uid).set({
            "status": "active",
            "plan": plan_name,
            "trial_end": datetime.utcnow() + timedelta(days=30),
            "stripe_customer_id": session["customer"],
            "stripe_subscription_id": session["subscription"]
        }, merge=True)
        await BillingBridge.log_subscription_event(uid, "checkout.session.completed", {"plan": plan_name})

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        docs = db.collection("subscriptions").where("stripe_subscription_id", "==", sub["id"]).stream()
        for doc in docs:
            db.collection("subscriptions").document(doc.id).update({"status": "canceled", "plan": "free"})
            await BillingBridge.log_subscription_event(doc.id, "customer.subscription.deleted", {})

    db.collection("webhook_events").document(event_id).set({"processed_at": firestore.SERVER_TIMESTAMP})
    return {"status": "ok"}
