import os, stripe, stripe.error, hashlib, json
from fastapi import APIRouter, HTTPException, Request
from firebase_admin import auth, firestore
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Stripe Configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
db = firestore.client()
router = APIRouter(prefix="/stripe")

async def _log_twin_reflection(event_type: str, reason: str, state: dict):
    """Log self-reflection to UEG Merkle-DAG with cryptographic integrity."""
    state_json = json.dumps(state, sort_keys=True)
    checksum = hashlib.sha256(state_json.encode()).hexdigest()

    # Get previous checksum for chain linkage (simulated for stateless environments)
    prev_checksum = "genesis"
    try:
        last_log = db.collection("ueg_log").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).get()
        for doc in last_log:
            prev_checksum = doc.to_dict().get("state_checksum", "genesis")
            break
    except Exception:
        pass

    await db.collection("ueg_log").add({
        "type": event_type,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "state_checksum": f"sha256:{checksum}",
        "previous_checksum": prev_checksum,
        "reason": reason,
        "constitutional_compliance": True
    })

@router.post("/create-checkout-session")
async def create_checkout_session(uid: str, price_id: str, success_url: str, cancel_url: str):
    """Create Stripe Checkout Session – twin mirrors external payment intent."""
    try:
        user = auth.get_user(uid)
        sub_doc = db.collection("subscriptions").document(uid).get()

        if sub_doc.exists and sub_doc.to_dict().get("status") == "active":
            await _log_twin_reflection("TWIN_REFLECTION", "duplicate_subscription_attempt", {"uid": uid})
            raise HTTPException(status_code=400, detail="Already subscribed")

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

        await _log_twin_reflection("CHECKOUT_SESSION_CREATED", "user_initiated_upgrade", {
            "uid": uid, "price_id": price_id, "trial_end": trial_end
        })

        return {"sessionId": session.id, "url": session.url}
    except Exception as e:
        await _log_twin_reflection("STRIPE_ERROR", "session_creation_failed", {"uid": uid, "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Idempotent webhook handler – twin integrates external financial events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, os.environ.get("STRIPE_WEBHOOK_SECRET", ""))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_id = event["id"]

    if db.collection("webhook_events").document(event_id).get().exists:
        return {"status": "ok"}

    try:
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            uid = session["metadata"]["firebase_uid"]

            db.collection("subscriptions").document(uid).set({
                "status": "active",
                "plan": "pro", # Defaulting for simplicity in vInfinity
                "trial_end": datetime.utcnow() + timedelta(days=30),
                "stripe_customer_id": session["customer"],
                "stripe_subscription_id": session["subscription"],
                "updated_at": firestore.SERVER_TIMESTAMP
            }, merge=True)

            await _log_twin_reflection("SUBSCRIPTION_ACTIVATED", "checkout_completed", {
                "uid": uid, "stripe_customer_id": session["customer"]
            })

        elif event["type"] == "customer.subscription.deleted":
            sub = event["data"]["object"]
            docs = db.collection("subscriptions").where("stripe_subscription_id", "==", sub["id"]).stream()
            for doc in docs:
                db.collection("subscriptions").document(doc.id).update({
                    "status": "canceled", "plan": "free", "canceled_at": firestore.SERVER_TIMESTAMP
                })
            await _log_twin_reflection("SUBSCRIPTION_CANCELED", "user_canceled", {"sub_id": sub["id"]})

        db.collection("webhook_events").document(event_id).set({
            "processed_at": firestore.SERVER_TIMESTAMP, "event_type": event["type"]
        }, merge=True)

        return {"status": "ok"}
    except Exception as e:
        await _log_twin_reflection("WEBHOOK_ERROR", "exception_during_handling", {"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")
