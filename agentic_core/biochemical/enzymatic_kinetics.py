import logging
import math
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Enzyme:
    """
    DC: Enzymatic Kinetics.
    Simulates Michaelis-Menten kinetics for enterprise processes.
    V = (Vmax * [S]) / (Km + [S])
    """
    def __init__(self, name: str, vmax: float, km: float):
        self.name = name
        self.vmax = vmax
        self.km = km

    def calculate_velocity(self, substrate_conc: float) -> float:
        if substrate_conc <= 0:
            return 0.0
        velocity = (self.vmax * substrate_conc) / (self.km + substrate_conc)
        logger.debug(f"BIOCHEM: Enzyme {self.name} velocity: {velocity:.4f} at substrate {substrate_conc}")
        return velocity

class KineticsSim:
    """
    DC: Simulator for enzymatic reactions.
    """
    def __init__(self):
        self.enzymes = {}

    def add_enzyme(self, name: str, vmax: float, km: float):
        self.enzymes[name] = Enzyme(name, vmax, km)

    def simulate_step(self, reactions: Dict[str, float]) -> Dict[str, float]:
        results = {}
        for enzyme_name, substrate_conc in reactions.items():
            if enzyme_name in self.enzymes:
                results[enzyme_name] = self.enzymes[enzyme_name].calculate_velocity(substrate_conc)
        return results
