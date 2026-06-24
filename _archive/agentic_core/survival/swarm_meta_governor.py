import logging
from typing import Dict, List
import time

logger = logging.getLogger(__name__)

class SwarmMetaGovernor:
    """
    DN: Swarm Meta-Governor.
    Monitors swarm-level allostatic load and triggers triage.
    """
    def __init__(self, threshold_load: float = 8.5):
        self.threshold_load = threshold_load
        self.swarm_allostatic_load = 0.0
        self.agent_loads: Dict[str, float] = {}

    def update_agent_load(self, agent_id: str, load: float):
        self.agent_loads[agent_id] = load
        self._recalculate_swarm_load()

    def _recalculate_swarm_load(self):
        if not self.agent_loads:
            self.swarm_allostatic_load = 0.0
            return
        self.swarm_allostatic_load = sum(self.agent_loads.values()) / len(self.agent_loads)

        if self.swarm_allostatic_load > self.threshold_load:
            self._trigger_triage()

    def _trigger_triage(self):
        logger.critical(f"GOVERNANCE: Swarm allostatic load ({self.swarm_allostatic_load:.2f}) EXCEEDED THRESHOLD. Initiating TRIAGE.")
        # Triage actions: pause non-essential tasks, reallocate, or shutdown.
        logger.info("GOVERNANCE: Triage: Suspending low-priority synthesis tasks.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "swarm_load": self.swarm_allostatic_load,
            "agent_count": len(self.agent_loads),
            "status": "CRITICAL" if self.swarm_allostatic_load > self.threshold_load else "HEALTHY"
        }
