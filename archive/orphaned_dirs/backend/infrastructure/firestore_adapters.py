from typing import Dict, Any, Optional, Tuple
from firebase_admin import firestore
from .repositories import UsageRepository, BillingRepository
from datetime import datetime

class FirestoreUsageRepository(UsageRepository):
    def __init__(self):
        self.db = firestore.client()

    async def get_subscription(self, uid: str) -> Optional[Dict[str, Any]]:
        doc = self.db.collection("subscriptions").document(uid).get()
        return doc.to_dict() if doc.exists else None

    async def increment_quota(self, uid: str, operation: str, limit: int) -> Tuple[bool, int]:
        def tx_logic(transaction):
            ref = self.db.collection("usage").document(f"{uid}_{operation}")
            doc = transaction.get(ref)
            count = doc.to_dict().get("count", 0) if doc.exists else 0
            if count < limit:
                transaction.set(ref, {"count": count + 1}, merge=True)
                return True, count + 1
            return False, count
        return self.db.run_transaction(tx_logic)

class FirestoreBillingRepository(BillingRepository):
    def __init__(self):
        self.db = firestore.client()

    async def get_subscription(self, uid: str) -> Optional[Dict[str, Any]]:
        doc = self.db.collection("subscriptions").document(uid).get()
        return doc.to_dict() if doc.exists else None

    async def activate_subscription(self, uid: str, data: Dict[str, Any]) -> None:
        self.db.collection("subscriptions").document(uid).set(data, merge=True)

    async def cancel_subscription(self, subscription_id: str) -> None:
        docs = self.db.collection("subscriptions").where("stripe_subscription_id", "==", subscription_id).stream()
        for doc in docs:
            self.db.collection("subscriptions").document(doc.id).update({"status": "canceled", "plan": "free"})

    async def register_webhook_event(self, event_id: str) -> bool:
        doc_ref = self.db.collection("webhook_events").document(event_id)
        try:
            # Atomic creation to prevent race conditions
            doc_ref.create({"processed_at": firestore.SERVER_TIMESTAMP})
            return True
        except Exception:
            return False
