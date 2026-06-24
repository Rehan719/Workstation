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
from typing import Dict, Any

class AutonomyManager:
    """Enforces fully delegated autonomy for operational tasks."""

    def is_delegated(self, task: Dict[str, Any]) -> bool:
        # CO-II: Fully Delegated Autonomy for operational execution
        delegated_types = ["research", "analysis", "formatting"]
        return task.get("type") in delegated_types
from typing import Dict, Any

class AutonomyManager:
    """CO-II: Enforces fully delegated autonomy for operational tasks."""

    def is_delegated(self, workflow: Dict[str, Any]) -> bool:
        # Operational tasks are delegated
        delegated_types = ["formatting", "log_analysis", "syntax_check", "internal_routing"]
        return workflow.get("type") in delegated_types
