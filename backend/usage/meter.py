from firebase_admin import firestore
from datetime import datetime
from typing import Dict, Any

db = firestore.client()

# Canonical Quotas for vΩ∞-CONVERGED
QUOTAS: Dict[str, Dict[str, int]] = {
    "free": {"executions": 50, "projects": 1},
    "pro": {"executions": 2000, "projects": 10},
    "team": {"executions": 10000, "projects": 999}
}

def _get_effective_plan(uid: str) -> str:
    """Determine user's effective plan considering active status and trials."""
    sub_doc = db.collection("subscriptions").document(uid).get()
    if not sub_doc.exists:
        return "free"
    data = sub_doc.to_dict()
    if data.get("status") != "active":
        return "free"
    trial_end = data.get("trial_end")
    if trial_end and isinstance(trial_end, datetime) and datetime.utcnow() < trial_end:
        return "pro"
    return data.get("plan", "free").lower()

def check_quota(uid: str, operation: str) -> bool:
    """
    Atomic quota enforcement via Firestore transaction.
    Guarantees race-condition-free increments.
    """
    def tx_logic(transaction):
        counter_ref = db.collection("usage").document(f"{uid}_{operation}")
        doc = transaction.get(counter_ref)
        count = doc.to_dict().get("count", 0) if doc.exists else 0
        plan = _get_effective_plan(uid)
        limit = QUOTAS.get(plan, {}).get(operation, 0)

        if count < limit:
            transaction.set(counter_ref, {"count": count + 1, "last_updated": firestore.SERVER_TIMESTAMP}, merge=True)
            return True
        return False

    return db.run_transaction(tx_logic)

async def async_check_quota(uid: str, operation: str) -> bool:
    """Async wrapper for FastAPI compatibility."""
    return check_quota(uid, operation)
