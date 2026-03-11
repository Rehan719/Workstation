import logging
from typing import Dict, Any, List
import datetime

logger = logging.getLogger(__name__)

class EntityCEOInterface:
    """
    ARTICLE 330: Strategic Integration with Entity.
    A secure channel for strategic communications between the Entity and AI CEO.
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

    def send_strategic_guidance(self, message: str) -> str:
        """Entity sends strategic guidance to AI CEO."""
        guidance = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "ENTITY",
            "message": message,
            "status": "UNREAD"
        }
        self._log_interaction(guidance)
        return guidance["timestamp"]

    def issue_veto(self, decision_id: str, reason: str):
        """Entity issues a veto for a strategic decision."""
        veto = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "ENTITY",
            "type": "VETO",
            "decision_id": decision_id,
            "reason": reason
        }
        logger.warning(f"ENTITY VETO: Decision {decision_id} rejected. Reason: {reason}")
        self._log_interaction(veto)

    def query_entity(self, question: str) -> str:
        """AI CEO queries the Entity for constitutional guidance."""
        query = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "CEO",
            "question": question
        }
        self._log_interaction(query)
        # Mocking the response
        return "Guidance provided: Aligned with Article 77."

    def _log_interaction(self, entry: Dict[str, Any]):
        import json
        with open(self.log_path, 'r', encoding='utf-8') as f:
            log = json.load(f)
        log.append(entry)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=4)
