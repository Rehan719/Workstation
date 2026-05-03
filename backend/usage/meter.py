from firebase_admin import firestore
from datetime import datetime

db = firestore.client()
QUOTAS = {"free": {"executions": 50, "projects": 1},
          "pro": {"executions": 2000, "projects": 10},
          "team": {"executions": 10000, "projects": 999}}

def _get_effective_plan(uid: str) -> str:
    sub = db.collection("subscriptions").document(uid).get()
    if not sub.exists:
        return "free"
    data = sub.to_dict()
    if data.get("status") != "active":
        return "free"
    trial_end = data.get("trial_end")
    if trial_end and isinstance(trial_end, datetime) and datetime.utcnow() < trial_end:
        return "pro"
    return data.get("plan", "free").lower()

def check_quota(uid: str, operation: str) -> bool:
    def tx_logic(transaction):
        counter_ref = db.collection("usage").document(f"{uid}_{operation}")
        doc = transaction.get(counter_ref)
        count = doc.to_dict().get("count", 0) if doc.exists else 0
        plan = _get_effective_plan(uid)
        limit = QUOTAS.get(plan, {}).get(operation, 0)
        if count < limit:
            transaction.set(counter_ref, {"count": count + 1}, merge=True)
            return True
        return False
    return db.run_transaction(tx_logic)

async def async_check_quota(uid: str, operation: str) -> bool:
    return check_quota(uid, operation)
