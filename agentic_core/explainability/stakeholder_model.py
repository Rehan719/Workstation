from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class StakeholderModel:
    """
    BL-I: Stakeholder-Tailored Explanations.
    Defines preference models for different stakeholder roles.
    """
    def __init__(self):
        self.preferences = {
            "expert": {"granularity": "high", "format": "technical_report"},
            "manager": {"granularity": "low", "format": "executive_summary"},
            "auditor": {"granularity": "high", "format": "compliance_audit"},
            "end_user": {"granularity": "medium", "format": "plain_language"}
        }

    def get_preference(self, role: str) -> Dict[str, Any]:
        return self.preferences.get(role, self.preferences["end_user"])
