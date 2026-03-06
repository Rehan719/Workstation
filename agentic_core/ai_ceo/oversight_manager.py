import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HumanOversightManager:
    """
    ARTICLE 278: Human Oversight & Frictionless Override.
    Intercepts and logs autonomous AI decisions for owner approval.
    """
    def __init__(self):
        self.pending_actions = []
        self.audit_log = []

    def request_approval(self, action_type: str, action_data: Dict[str, Any]) -> str:
        """
        ARTICLE 278: Queues an AI action for human review with risk assessment.
        """
        action_id = f"rev_{action_type}_{datetime.now().strftime('%H%M%S')}"

        # ARTICLE 278: automated risk flag for autonomous decisions
        is_auto_approvable = action_type in ["LOW_RISK_MARKETING", "METER_CHECK"]

        review_request = {
            "id": action_id,
            "type": action_type,
            "data": action_data,
            "risk_score": 0.1 if is_auto_approvable else 0.85,
            "status": "AUTO_APPROVED" if is_auto_approvable else "PENDING",
            "timestamp": datetime.now().isoformat()
        }

        if review_request["status"] == "PENDING":
            self.pending_actions.append(review_request)
            logger.info(f"Oversight: HIGH RISK action {action_id} queued for owner review.")
        else:
            self.audit_log.append(review_request)
            logger.info(f"Oversight: LOW RISK action {action_id} auto-approved.")

        return action_id

    def approve_action(self, action_id: str) -> bool:
        """Approves and logs the action."""
        for action in self.pending_actions:
            if action["id"] == action_id:
                action["status"] = "APPROVED"
                self.audit_log.append(action)
                self.pending_actions.remove(action)
                return True
        return False

    def reject_action(self, action_id: str, reason: str = "") -> bool:
        """Rejects the action and logs feedback."""
        for action in self.pending_actions:
            if action["id"] == action_id:
                action["status"] = "REJECTED"
                action["rejection_reason"] = reason
                self.audit_log.append(action)
                self.pending_actions.remove(action)
                return True
        return False

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return self.audit_log
