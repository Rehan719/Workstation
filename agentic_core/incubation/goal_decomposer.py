from typing import List, Dict, Any

class GoalDecomposer:
    """Decomposes high-level user goals into executable scientific workflows."""

    def decompose(self, goal: str) -> List[Dict[str, Any]]:
        # Simulated decomposition logic
        if "report" in goal.lower():
            return [
                {"name": "literature_search", "type": "research"},
                {"name": "data_synthesis", "type": "analysis"},
                {"name": "draft_report", "type": "writing"}
            ]
        return [{"name": "general_exploration", "type": "discovery"}]
