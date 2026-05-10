from firebase_admin import firestore
from datetime import datetime
from typing import Dict, Any

db = firestore.client()

# ARTICLE 1122: Multi-tier Quota Specification
QUOTAS = {
    "free": {"executions": 50},
    "pro": {"executions": 2000},
    "team": {"executions": 10000}
}

def _get_effective_plan(uid: str) -> str:
    """Determines the user's current plan level based on subscription state."""
    sub = db.collection("subscriptions").document(uid).get()
    if not sub.exists:
        return "free"

    data = sub.to_dict()
    plan = data.get("plan", "free")
    trial_end = data.get("trial_end")

    # Standard trial check: if within 30 days of trial start, promote to Pro
    if trial_end and isinstance(trial_end, datetime) and datetime.utcnow() < trial_end:
        return "pro"

    return plan

def check_quota(uid: str, operation: str) -> bool:
    """
    ARTICLE 1123: Atomic Quota Enforcement.
    Uses Firestore Transactions to prevent race conditions in free-tier usage.
    """
    transaction = db.transaction()

    @firestore.transactional
    def tx_logic(transaction, uid, operation):
        counter_ref = db.collection("usage").document(f"{uid}_{operation}")
        snapshot = counter_ref.get(transaction=transaction)

        current_count = snapshot.to_dict().get("count", 0) if snapshot.exists else 0
        effective_plan = _get_effective_plan(uid)
        limit = QUOTAS.get(effective_plan, {}).get(operation, 0)

        if current_count < limit:
            transaction.set(counter_ref, {
                "count": current_count + 1,
                "last_updated": firestore.SERVER_TIMESTAMP
            }, merge=True)
            return True
        return False

    return tx_logic(transaction, uid, operation)
