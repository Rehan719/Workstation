import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AutonomyManager:
    """Manages fully delegated vs. supervised autonomy levels."""

    def is_delegated(self, workflow: Dict[str, Any]) -> bool:
        # Research tasks usually require oversight
        if workflow.get("type") == "research":
            return False
        return True
