import logging
import random
from typing import List, Dict

logger = logging.getLogger(__name__)

class HSPNetwork:
    """
    DA-III: HSP Chaperone Cycling.
    ATPase turnover rate: 1-5 ATP/sec.
    Models HSP70/90 client binding and probability-based refolding.
    """
    def __init__(self):
        self.capacity = 100
        self.occupancy_hsp70 = 0
        self.occupancy_hsp90 = 0
        self.atp_turnover_hsp70 = 3.0 # ATP/sec
        self.atp_turnover_hsp90 = 2.0 # ATP/sec
        self.refolding_pool_hsp70: List[str] = []
        self.refolding_pool_hsp90: List[str] = []

    def bind_misfolded(self, client_id: str, client_type: str = "general") -> bool:
        """Binds client to HSP70 or HSP90."""
        # HSP70 handles nascent/general folding, HSP90 handles signaling/metastable
        if client_type == "signaling" or self.occupancy_hsp70 >= 50:
            if self.occupancy_hsp90 < 50:
                self.occupancy_hsp90 += 1
                self.refolding_pool_hsp90.append(client_id)
                logger.debug(f"HSP90: Bound client {client_id}.")
                return True
        else:
            if self.occupancy_hsp70 < 50:
                self.occupancy_hsp70 += 1
                self.refolding_pool_hsp70.append(client_id)
                logger.debug(f"HSP70: Bound client {client_id}.")
                return True
        return False

    def process_refolding(self, dt: float, atp_adp_ratio: float) -> List[str]:
        """
        Refolds proteins based on ATPase kinetics of HSP70 and HSP90.
        """
        energy_factor = atp_adp_ratio / 5.0

        # ATPase rates (1-5 ATP/sec range)
        rate70 = max(1.0, min(5.0, self.atp_turnover_hsp70 * energy_factor))
        rate90 = max(1.0, min(5.0, self.atp_turnover_hsp90 * energy_factor))

        refolded = []

        # P(refold) per cycle
        # HSP70 cycle probability
        for client in list(self.refolding_pool_hsp70):
            if random.random() < (rate70 * dt / 50.0):
                refolded.append(client)
                self.refolding_pool_hsp70.remove(client)
                self.occupancy_hsp70 -= 1

        # HSP90 cycle probability
        for client in list(self.refolding_pool_hsp90):
            if random.random() < (rate90 * dt / 75.0): # HSP90 cycle is often slower/more complex
                refolded.append(client)
                self.refolding_pool_hsp90.remove(client)
                self.occupancy_hsp90 -= 1

        if refolded:
             logger.info(f"HSP: Refolded {len(refolded)} clients. Rates: 70={rate70:.1f}, 90={rate90:.1f} ATP/s")
        return refolded

    def get_occupancy_rate(self) -> float:
        return (self.occupancy_hsp70 + self.occupancy_hsp90) / self.capacity
