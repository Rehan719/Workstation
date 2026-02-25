from typing import Dict, Any

class AutonomyManager:
    """CO-II: Enforces fully delegated autonomy for operational tasks."""

    def is_delegated(self, workflow: Dict[str, Any]) -> bool:
        # Operational tasks are delegated
        delegated_types = ["formatting", "log_analysis", "syntax_check", "internal_routing"]
        return workflow.get("type") in delegated_types
