import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GlobalWorkspace:
    """
    DB-I: Shared Memory Infrastructure.
    Central workspace for global broadcast of subsystem state vectors.
    Target latency: <10 ms.
    """
    def __init__(self):
        self.workspace: Dict[str, Any] = {}
        self.ignition_listeners: List[Any] = []
        self.last_ignition_timestamp = 0.0

    def publish_state(self, component_id: str, state_vector: Dict[str, Any]):
        """Publishes state with latency tracking."""
        start = time.perf_counter()
        self.workspace[component_id] = {
            "data": state_vector,
            "timestamp": time.time()
        }
        latency_ms = (time.perf_counter() - start) * 1000
        if latency_ms > 10:
            logger.warning(f"WORKSPACE: High latency publish: {latency_ms:.3f}ms")

        logger.debug(f"WORKSPACE: Published {component_id} state.")

    def read_workspace(self) -> Dict[str, Any]:
        """Returns the full unified field of the workspace."""
        return self.workspace

    def trigger_global_ignition(self):
        """Simulates global broadcast/ignition event (<250ms)."""
        self.last_ignition_timestamp = time.time()
        logger.info("WORKSPACE: GLOBAL IGNITION triggered. Synchronizing modules.")
