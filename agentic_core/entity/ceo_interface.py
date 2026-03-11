import logging
from typing import Dict, Any, List
import datetime

logger = logging.getLogger(__name__)

class EntityCEOInterface:
    """
    ARTICLE 330/337: Entity-CEO Interface (Purpose-Aware).
    A secure channel for strategic and purpose-driven communications.
    """
    def __init__(self, owner_id: str = "Jules"):
        self.owner_id = owner_id
        self.log_path = "docs/governance/entity_ceo_log.json"
        self._initialize_log()

    def _initialize_log(self):
        import os
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', encoding='utf-8') as f:
                import json
                json.dump([], f)

    def send_purpose_alert(self, message: str) -> str:
        """Entity flags potential purpose misalignment (ARTICLE 337)."""
        return self.send_strategic_guidance(message, type="PURPOSE_ALERT")

    def provide_spiritual_guidance(self, message: str) -> str:
        """Entity provides ethical/spiritual input (ARTICLE 337)."""
        return self.send_strategic_guidance(message, type="SPIRITUAL_GUIDANCE")

    def send_strategic_guidance(self, message: str, type: str = "STRATEGIC") -> str:
        """Generic method for Entity-to-CEO messages."""
        guidance = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "ENTITY",
            "type": type,
            "message": message,
            "status": "UNREAD"
        }
        self._log_interaction(guidance)
        return guidance["timestamp"]

    def issue_veto(self, decision_id: str, reason: str, category: str = "CONSTITUTIONAL"):
        """Entity issues a veto (ARTICLE 337)."""
        veto = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "ENTITY",
            "type": "VETO",
            "category": category,
            "decision_id": decision_id,
            "reason": reason
        }
        logger.warning(f"ENTITY {category} VETO: Decision {decision_id} rejected. Reason: {reason}")
        self._log_interaction(veto)

    def purpose_check(self, proposal_id: str, payload: Dict[str, Any]):
        """AI CEO submits proposal for evaluation (ARTICLE 2.2)."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "CEO",
            "type": "PURPOSE_CHECK",
            "proposal_id": proposal_id,
            "payload": payload
        }
        self._log_interaction(entry)

    def _log_interaction(self, entry: Dict[str, Any]):
        import json
        with open(self.log_path, 'r', encoding='utf-8') as f:
            log = json.load(f)
        log.append(entry)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=4)
