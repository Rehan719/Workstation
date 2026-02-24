import logging
import hashlib
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReproductionEngine:
    """
    CD: Reproduction Capability.
    Spawns specialized agent instances (Fission, Budding, Recombination).
    """
    def __init__(self, survival_engine: Any):
        self.survival_engine = survival_engine

    def spawn_instance(self, parent_id: str, mode: str, genome_subset: Dict[str, Any]) -> Dict[str, Any]:
        """CD-IV: Spawns a new instance subject to constitutional approval."""

        # Constitutional approval check
        if not self.survival_engine.request_action("reproduction", {"mode": mode}):
            logger.error(f"REPRODUCTION BLOCKED: {mode} denied by Survival Instinct.")
            return None

        child_id = f"AGENT_{mode.upper()}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:6]}"

        child_instance = {
            "id": child_id,
            "parent_id": parent_id,
            "mode": mode,
            "genome": genome_subset,
            "born_at": time.time(),
            "signature": f"sig:{hashlib.sha256(child_id.encode()).hexdigest()[:8]}"
        }

        logger.info(f"REPRODUCTION SUCCESS: {child_id} spawned via {mode}.")
        return child_instance
