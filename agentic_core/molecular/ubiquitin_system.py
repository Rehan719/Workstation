import logging
import random
from typing import Dict, List

logger = logging.getLogger(__name__)

class UbiquitinSystem:
    """
    DA-II: Ubiquitin-Mediated Catabolism.
    Models the E1/E2/E3 enzymatic cascade with K48/K63 linkage discrimination.
    Tunable half-lives: 2.3–8.7 minutes (138–522 seconds).
    """
    def __init__(self):
        # resource_id -> {"linkage": "K48"|"K63", "age": float, "half_life": float}
        self.tagged_pool: Dict[str, Dict] = {}
        self.stress_index = 0.0
        # E1/E2/E3 enzymatic state (simulated)
        self.e1_active = 1.0
        self.e2_active = 1.0
        self.e3_mdm2_level = 1.0

    def tag_resource(self, resource_id: str, linkage: str = "K48", redox_stress: float = 0.5):
        """
        Tags a resource for catabolism via E1->E2->E3 cascade.
        Higher redox stress accelerates E3 (MDM2) activity for p53-analogs.
        """
        # Cascade efficiency
        efficiency = self.e1_active * self.e2_active * self.e3_mdm2_level

        # Linear map: redox_stress 0.0 -> 8.7m, 1.0 -> 2.3m
        half_life_s = (8.7 - (6.4 * redox_stress)) * 60.0
        # Apply cascade efficiency (lower efficiency = slower tagging/higher half-life)
        half_life_s = half_life_s / max(0.1, efficiency)

        self.tagged_pool[resource_id] = {
            "linkage": linkage,
            "age": 0.0,
            "half_life": half_life_s
        }
        logger.info(f"UBIQUITIN: E1->E2->E3 Cascade tagged {resource_id} with {linkage}. t1/2: {half_life_s/60:.2f} min")

    def process_cycle(self, dt: float) -> List[str]:
        """Updates aging and returns resources for degradation."""
        degraded = []
        for rid, entry in list(self.tagged_pool.items()):
            entry["age"] += dt
            # Probability-based degradation (stochastic model)
            prob = 1.0 - (0.5 ** (entry["age"] / entry["half_life"]))
            if random.random() < prob:
                degraded.append(rid)
                del self.tagged_pool[rid]

        # Stress Index based on pool density
        self.stress_index = len(self.tagged_pool) / 50.0
        return degraded

    def get_stress_index(self) -> float:
        return min(1.0, self.stress_index)
