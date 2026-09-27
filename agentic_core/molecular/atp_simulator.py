import numpy as np
import logging

logger = logging.getLogger(__name__)

class ATPSimulator:
    """
    DA-IV: ATP/ADP Ratio Simulation.
    Target energy state: 2.0 to 10.0.
    """
    def __init__(self):
        self.ratio = 5.0

    def update(self, dt: float, metabolic_load: float, circadian_efficiency: float = 1.0):
        """
        Energy consumption: ratio decreases with load.
        Energy production: ratio increases with recovery.
        v71.0: circadian_efficiency improves production (P/O ratio) by up to 19%.
        """
        # W494 (refutation) — `metabolic_load` is declared 0-1 by every caller and by the resource
        # registry ({"metabolic_load": "float 0-1"}), and NOTHING validated it. One composition run with
        # metabolic_load=100 drove this process-wide singleton from 0.358 to 0.033 in a single call,
        # which falsified a claim W494 had written into its own basis strings ("production always
        # exceeds consumption, so it only rises"). A documented domain that is not enforced is not a
        # domain. Enforced here, at the arithmetic, so no caller can bypass it.
        metabolic_load = max(0.0, min(1.0, float(metabolic_load)))
        circadian_efficiency = max(0.0, min(1.0, float(circadian_efficiency)))
        consumption = 0.1 * metabolic_load
        production = 0.5 * circadian_efficiency

        # dE/dt = production - consumption
        self.ratio += (production - consumption) * dt
        self.ratio = max(0.5, min(15.0, self.ratio))

        return self.ratio
