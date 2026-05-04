from firebase_admin import firestore
from datetime import datetime
from typing import Dict, Any

db = firestore.client()

# Canonical Quotas for vΩ∞-MASTER
QUOTAS: Dict[str, Dict[str, int]] = {
    "free": {"executions": 50, "projects": 1},
    "pro": {"executions": 2000, "projects": 10},
    "team": {"executions": 10000, "projects": 999}
}

def _get_effective_plan(uid: str) -> str:
    """Retrieve the current active plan, handling trial logic."""
    sub_doc = db.collection("subscriptions").document(uid).get()
    if not sub_doc.exists:
        return "free"

    data = sub_doc.to_dict()
    if data.get("status") != "active":
        return "free"

    trial_end = data.get("trial_end")
    if trial_end:
        # Support both timestamp objects and datetime
        end_dt = trial_end if isinstance(trial_end, datetime) else datetime.fromtimestamp(trial_end)
        if datetime.utcnow() < end_dt:
            return "pro" # Implicit upgrade during trial

    return data.get("plan", "free").lower()

def check_quota(uid: str, operation: str) -> bool:
    """Atomic, race-condition-free quota enforcement via Firestore transaction."""
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
    """FastAPI-compatible async wrapper."""
    return check_quota(uid, operation)
