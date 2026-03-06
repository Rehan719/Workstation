import logging
import time

logger = logging.getLogger(__name__)

class QuorumSensing:
    """
    Communication via "heartbeats" (AI-2 analogs) to sense population density.
    Kinetics: t1/2 ~ 2 hours.
    """
    def __init__(self, agent_id: str, threshold: float = 50.0):
        self.agent_id = agent_id
        self.ai2_concentration = 0.0
        self.threshold = threshold
        self.last_update = time.time()
        self.decay_constant = 0.346 # ln(2) / 2 hours = 0.346 h^-1

    def secrete_ai2(self, amount: float = 10.0):
        self.ai2_concentration += amount
        logger.debug(f"QUORUM: Agent {self.agent_id} secreted AI-2. Current: {self.ai2_concentration:.2f}")

    def update_concentration(self, external_concentration: float):
        """
        Updates concentration based on external signals and internal decay.
        """
        now = time.time()
        dt_hours = (now - self.last_update) / 3600
        # Exponential decay: C = C0 * exp(-k*t)
        self.ai2_concentration *= (2.718 ** (-self.decay_constant * dt_hours))
        self.ai2_concentration += external_concentration
        self.last_update = now

    def get_behavior_mode(self) -> str:
        """
        COOPERATIVE if concentration > threshold, else INDEPENDENT.
        """
        if self.ai2_concentration > self.threshold:
            logger.info(f"QUORUM: Threshold EXCEEDED ({self.ai2_concentration:.2f} > {self.threshold}). Switching to COOPERATIVE mode.")
            return "COOPERATIVE"
        return "INDEPENDENT"
