import logging
import time
from typing import List

logger = logging.getLogger(__name__)

class QuorumSensing:
    """
    ARTICLE DD: AI-2 Quorum Sensing.
    Calibrated decay t½ = 2 hours.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.signal_strength = 0.0 # Concentration of AI-2
        self.half_life_s = 7200.0 # 2 hours
        self.last_decay = time.time()
        self.nodes_detected = 0

    def broadcast_signal(self):
        """Simulates release of AI-2."""
        self.signal_strength += 1.0
        logger.debug(f"QUORUM: Node {self.node_id} broadcasted AI-2 signal.")

    def update_concentration(self, received_signals: int):
        """
        Updates concentration based on external signals and internal decay.
        """
        now = time.time()
        dt = now - self.last_decay
        self.last_decay = now

        # Exponential decay: C = C0 * exp(-lambda * t)
        lam = 0.693 / self.half_life_s
        self.signal_strength *= (0.5 ** (dt / self.half_life_s))

        # Add external signals
        self.signal_strength += received_signals
        self.nodes_detected = received_signals

    def check_quorum(self, threshold: float = 5.0) -> bool:
        """Determines if a 'Minimum Viable Colony' exists."""
        is_met = self.signal_strength >= threshold
        if is_met:
             logger.info(f"QUORUM: Threshold reached ({self.signal_strength:.2f}). Activating group behavior.")
        return is_met
