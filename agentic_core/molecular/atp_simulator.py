import logging
import time

logger = logging.getLogger(__name__)

class ATPSimulator:
    """
    Simulates ATP/ADP ratio as energy currency.
    Update frequency: 50 ms.
    """
    def __init__(self):
        self.atp_adp_ratio = 5.0 # Healthy baseline
        self.last_update = time.time()

    def update(self, production: float, demand: float):
        """
        production: Input metabolic flux.
        demand: Computational/executive load.
        """
        now = time.time()
        dt = now - self.last_update
        if dt < 0.05: # Enforce 50ms interval if called too fast
             return self.atp_adp_ratio

        self.last_update = now

        # dEnergy/dt = Production - Demand
        self.atp_adp_ratio = max(0.1, self.atp_adp_ratio + (production - demand) * dt * 5.0)

        # Homeostatic pull back to 5.0
        self.atp_adp_ratio += (5.0 - self.atp_adp_ratio) * 0.01

        logger.debug(f"ATP_SIM: Ratio={self.atp_adp_ratio:.2f}")
        return self.atp_adp_ratio
