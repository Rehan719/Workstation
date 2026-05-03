import logging
from backend.usage.usage_meter import check_quota
from agentic_core.ueg.logger import VSBUEGLogger

logger = logging.getLogger("BillingBridge")
ueg = VSBUEGLogger()

class BillingBridge:
    """
    ARTICLE 1124: The Billing-Biomimetic Nexus.
    Injects SaaS quota enforcement into geospheric cycles.
    """
    @staticmethod
    async def validate_execution(uid: str, operation: str = "executions"):
        """Validates if the organism is permitted to execute a cycle."""
        if not check_quota(uid, operation):
            logger.error(f"Quota exhausted for user {uid}. Biomimetic cycle halted.")
            await ueg.log_minimisation_event("billing_breach_detected", {
                "uid": uid,
                "operation": operation,
                "status": "402_PAYMENT_REQUIRED"
            })
            return False

        await ueg.log_minimisation_event("billing_compliance_check", {
            "uid": uid,
            "operation": operation,
            "status": "passed"
        })
        return True

    @staticmethod
    async def log_subscription_event(uid: str, event_type: str, metadata: dict):
        """Logs commercial events to the UEG Merkle-DAG."""
        await ueg.log_minimisation_event("CONSTITUTIONAL COMPLIANCE: BILLING", {
            "uid": uid,
            "event": event_type,
            "metadata": metadata
        })
