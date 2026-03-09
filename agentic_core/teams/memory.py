import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CollectiveMemory:
    """
    ARTICLE 316: Collective Intelligence.
    Propagates successful strategies via the Knowledge Graph.
    """
    def __init__(self):
        self.memory_store = []

    def record_outcome(self, team_id: str, strategy: str, result: str, success: bool):
        entry = {
            "team_id": team_id,
            "strategy": strategy,
            "success": success,
            "score": 1.0 if success else 0.0
        }
        self.memory_store.append(entry)
        logger.info(f"Memory: Recorded outcome for {team_id}. Success: {success}")

    def get_best_strategy(self, domain: str) -> str:
        # Basic lookup logic
        return "COLLABORATIVE_PARALLEL_EXECUTION"
