import time
import logging
import numpy as np
from typing import Dict

logger = logging.getLogger(__name__)

class QuorumSensing:
    """
    DK, DD-III: Quorum-Sensing Consensus.
    Autoinducer-2 (AI-2) analogs with calibrated t1/2 = 2 hours.
    Consensus latency target: <= 200 ms.
    """
    def __init__(self, min_colony_size: int = 5):
        self.ai2_concentrations: Dict[str, float] = {} # agent_id -> conc
        self.min_colony_size = min_colony_size
        self.decay_rate = 0.346 # ln(2) / 2 hours = 0.346 h^-1
        self.last_sync_time = time.time()

    def broadcast_health_signal(self, agent_id: str, intensity: float):
        """Simulates secretion of AI-2 signal."""
        start_sync = time.perf_counter()
        self.ai2_concentrations[agent_id] = intensity * 100.0

        sync_latency = (time.perf_counter() - start_sync) * 1000
        if sync_latency > 200:
             logger.warning(f"QUORUM: Consensus sync latency ({sync_latency:.2f}ms) exceeded target.")

        logger.debug(f"QUORUM: Node {agent_id} signaled. Colony size={len(self.ai2_concentrations)}")

    def update_colony_state(self):
        """Processes decay of signals across the ecosystem."""
        now = time.time()
        dt_h = (now - self.last_sync_time) / 3600.0
        for aid in self.ai2_concentrations:
             self.ai2_concentrations[aid] *= np.exp(-self.decay_rate * dt_h)
        self.last_sync_time = now

    def has_ecosystem_quorum(self) -> bool:
        """Determines if enough nodes are 'healthy' and active."""
        active_nodes = sum(1 for c in self.ai2_concentrations.values() if c > 15.0)
        quorum = active_nodes >= self.min_colony_size
        logger.info(f"QUORUM: Active Nodes={active_nodes}, Result={quorum}")
        return quorum
