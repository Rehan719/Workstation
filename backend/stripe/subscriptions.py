import os, stripe
from fastapi import APIRouter, HTTPException, Request
from firebase_admin import auth, firestore
from datetime import datetime, timedelta

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_mock")
db = firestore.client()
router = APIRouter(prefix="/stripe")

@router.post("/create-checkout-session")
async def create_checkout_session(uid: str, price_id: str, success_url: str, cancel_url: str):
    try:
        user = auth.get_user(uid)
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    sub_doc = db.collection("subscriptions").document(uid).get()
    if sub_doc.exists and sub_doc.to_dict().get("status") == "active":
        raise HTTPException(400, "Already subscribed")

    trial_end = int((datetime.utcnow() + timedelta(days=30)).timestamp())
    session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
        subscription_data={"trial_end": trial_end},
        metadata={"firebase_uid": uid}
    )
    return {"sessionId": session.id, "url": session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_mock")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        raise HTTPException(400, "Invalid signature")

    event_id = event["id"]
    if db.collection("webhook_events").document(event_id).get().exists:
        return {"status": "ok"}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        uid = session["metadata"]["firebase_uid"]
        db.collection("subscriptions").document(uid).set({
            "status": "active",
            "plan": session["display_items"][0]["price"]["nickname"].lower() if session.get("display_items") else "pro",
            "trial_end": datetime.utcnow() + timedelta(days=30),
            "stripe_customer_id": session["customer"],
            "stripe_subscription_id": session["subscription"]
        }, merge=True)
    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        docs = db.collection("subscriptions").where("stripe_subscription_id", "==", sub["id"]).stream()
        for doc in docs:
            db.collection("subscriptions").document(doc.id).update({"status": "canceled", "plan": "free"})
    elif event["type"] == "invoice.payment_failed":
        db.collection("ueg_log").add({
            "type": "CONSTITUTIONAL_COMPLIANCE_BILLING",
            "event_id": event_id,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "payload": event["data"]["object"]
        })
    db.collection("webhook_events").document(event_id).set({"processed_at": firestore.SERVER_TIMESTAMP})
    return {"status": "ok"}

@router.post("/create-portal-session")
async def create_portal_session(uid: str, return_url: str):
    sub_doc = db.collection("subscriptions").document(uid).get()
    if not sub_doc.exists:
        raise HTTPException(400, "No subscription")
    customer_id = sub_doc.to_dict().get("stripe_customer_id")
    if not customer_id:
        raise HTTPException(400, "Missing customer ID")
    portal = stripe.billing_portal.Session.create(customer=customer_id, return_url=return_url)
    return {"url": portal.url}
