import logging
import random
import numpy as np
from typing import Dict, List

logger = logging.getLogger(__name__)

class UbiquitinSystem:
    """
    ARTICLE DA: Ubiquitin-Mediated Catabolism.
    Tunable half-lives: 2.3–8.7 minutes.
    """
    def __init__(self):
        self.tagged_pool = {} # id -> {"half_life": float, "age": float}
        self.stress_index = 0.0

    def calculate_half_life(self, potential_mv: float) -> float:
        """
        Maps redox potential to half-life.
        -240 mV (reducing) -> 8.7 min (522s)
        -210 mV (oxidative) -> 2.3 min (138s)
        """
        # Linear interpolation
        # -210 -> 138, -240 -> 522
        # slope = (522-138) / (-240 - (-210)) = 384 / -30 = -12.8
        half_life_s = 138.0 + (potential_mv - (-210.0)) * (-12.8)
        return max(138.0, min(522.0, half_life_s))

    def tag_for_degradation(self, resource_id: str, potential_mv: float):
        hl = self.calculate_half_life(potential_mv)
        self.tagged_pool[resource_id] = {"half_life": hl, "age": 0.0}
        logger.debug(f"UBIQUITIN: Tagged {resource_id}, t1/2: {hl/60:.2f}m")

    def update(self, dt: float) -> List[str]:
        degraded = []
        for rid, data in list(self.tagged_pool.items()):
            data["age"] += dt
            # Stochastic decay probability: 1 - exp(-ln2 * t / t1/2)
            prob = 1.0 - np.exp(-np.log(2) * dt / data["half_life"])
            if random.random() < prob:
                degraded.append(rid)
                del self.tagged_pool[rid]

        self.stress_index = len(self.tagged_pool) / 100.0
        return degraded
