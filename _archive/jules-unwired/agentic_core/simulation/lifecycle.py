import logging
from typing import Dict, Any
from .registry import TwinRegistry
from .fidelity import FidelityScorer

logger = logging.getLogger(__name__)

class TwinLifecycleManager:
    """
    ARTICLE 310: Twin Lifecycle Governance.
    Handles the birth, evolution, and assimilation of digital twins.
    """
    def __init__(self):
        self.registry = TwinRegistry()
        self.scorer = FidelityScorer()

    async def create_twin(self, reactor_id: str, twin_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Lifecycle: Creating twin {twin_id} for {reactor_id}")
        initial_state = {
            "config": config,
            "status": "INITIALIZED",
            "data": {}
        }
        self.registry.register_twin(twin_id, reactor_id, initial_state)
        return initial_state

    async def evolve_twin(self, twin_id: str, new_data: Any) -> Dict[str, Any]:
        twin = self.registry.get_twin(twin_id)
        if not twin:
            raise ValueError(f"Twin {twin_id} not found.")

        state = twin["state"]
        state["data"] = new_data
        state["status"] = "EVOLVING"

        fidelity = self.scorer.score_fidelity(state, {}) # Real-world data compare
        self.registry.update_twin(twin_id, state, fidelity)

        return state
