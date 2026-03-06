import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NormativeAlignment:
    """
    CO-IV: Normative Alignment.
    Ensures system behavior adheres to social norms and constitutional guidelines.
    """
    def check_behavior(self, action: str, feedback: Dict[str, Any]) -> bool:
        """Evaluates if an action violated social or constitutional norms."""
        if feedback.get("sentiment") == "negative" and feedback.get("reason") == "intrusive":
            logger.error(f"NORMATIVE: Action '{action}' flagged as intrusive. Self-correction required.")
            return False
        return True
