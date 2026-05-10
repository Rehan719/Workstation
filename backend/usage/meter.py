from firebase_admin import firestore
from datetime import datetime
from typing import Dict, Any

db = firestore.client()

QUOTAS: Dict[str, Dict[str, int]] = {
    "free": {"executions": 50, "projects": 1},
    "pro": {"executions": 2000, "projects": 10},
    "team": {"executions": 10000, "projects": 999}
}

def _get_effective_plan(uid: str) -> str:
    sub_doc = db.collection("subscriptions").document(uid).get()
    if not sub_doc.exists: return "free"
    data = sub_doc.to_dict()
    if data.get("status") != "active": return "free"

    trial_end = data.get("trial_end")
    if trial_end and isinstance(trial_end, datetime) and datetime.utcnow() < trial_end:
        return "pro"

    return data.get("plan", "free").lower()

def check_quota(uid: str, operation: str) -> bool:
    """Atomic quota check – twin's self-limiting reflex via Firestore transaction."""
    def transaction_logic(transaction):
        counter_ref = db.collection("usage").document(f"{uid}_{operation}")
        doc = transaction.get(counter_ref)
        current_count = doc.to_dict().get("count", 0) if doc.exists else 0

        plan = _get_effective_plan(uid)
        limit = QUOTAS.get(plan, {}).get(operation, 0)

        if current_count < limit:
            transaction.set(counter_ref, {"count": current_count + 1}, merge=True)
            return True
        return False

    result = db.run_transaction(transaction_logic)

    if not result:
        db.collection("ueg_log").add({
            "type": "QUOTA_EXHAUSTED",
            "uid": uid,
            "operation": operation,
            "plan": _get_effective_plan(uid),
            "timestamp": firestore.SERVER_TIMESTAMP
        })
    return result

async def async_check_quota(uid: str, operation: str) -> bool:
    return check_quota(uid, operation)
