from typing import Dict, Any

class AutonomyManager:
    """Enforces fully delegated autonomy for operational tasks."""

    def is_delegated(self, task: Dict[str, Any]) -> bool:
        # CO-II: Fully Delegated Autonomy for operational execution
        delegated_types = ["research", "analysis", "formatting"]
        return task.get("type") in delegated_types
