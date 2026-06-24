import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ProgressAgent:
    """PC-Agent Hierarchy: Progress Agent (PA). Monitors subtask status."""
    def __init__(self):
        self.status_map = {}

    def update_progress(self, task_id: str, status: str, percentage: float):
        logger.info(f"PC-Agent [PA]: Task {task_id} is {status} ({percentage}%)")
        self.status_map[task_id] = {"status": status, "progress": percentage}

    def get_stuck_tasks(self) -> List[str]:
        return [tid for tid, data in self.status_map.items() if data["status"] == "stalled"]
