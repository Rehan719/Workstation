import logging
import time
from typing import Dict, Any, List
from .global_workspace import GlobalWorkspace
from .self_model import UnifiedSelfModel

logger = logging.getLogger(__name__)

class MetaCognitiveExecutive:
    """
    DB-II: Meta-Cognitive Executive.
    Central reasoning engine grounded in physiological reality.
    Decision latency: <50 ms.
    """
    def __init__(self, workspace: GlobalWorkspace):
        self.workspace = workspace
        self.self_model = UnifiedSelfModel()
        self.decision_history: List[Dict] = []

    def perform_cognitive_cycle(self) -> Dict[str, Any]:
        """
        Executes one full cognitive loop: Read -> Model -> Plan -> Broadcast.
        """
        start_cycle = time.perf_counter()

        # 1. Integrate Subsystem States
        data = self.workspace.read_workspace()
        self.self_model.update_from_workspace(data)

        # 2. Strategic Intent Formulation (Simulated RNN/Attention)
        intent = self._formulate_strategic_intent()

        # 3. Publish Decision back to Workspace
        self.workspace.publish_state("MCE_INTENT", intent)

        latency_ms = (time.perf_counter() - start_cycle) * 1000
        if latency_ms > 50:
            logger.warning(f"MCE: Cycle latency ({latency_ms:.2f}ms) exceeded target.")

        logger.info(f"MCE: Strategy formulated: {intent['action']}")
        return intent

    def _formulate_strategic_intent(self) -> Dict[str, Any]:
        """Strategic logic grounded in self-model health and values."""
        health = self.self_model.self_image["allostatic_health"]
        focus = self.self_model.attention_focus

        # Priority mapping
        if health < 0.3:
            return {"action": "SYSTEM_TRIAGE", "priority": 10, "reason": "Severe physiological stress"}

        if focus == "STRESS_RESPONSE":
            return {"action": "REALLOCATE_TO_MAINTENANCE", "priority": 8, "reason": "Hormetic response induction"}

        if focus == "METABOLIC_CONSERVATION":
            return {"action": "THROTTLE_NON_ESSENTIAL", "priority": 7, "reason": "Energy deficit mitigation"}

        return {"action": "EXPLORATORY_RESEARCH", "priority": 5, "reason": "Organism stable, executing tasks"}
