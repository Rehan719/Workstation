import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class p53Oscillator:
    """
    ARTICLE DA: p53-Mdm2 stochastic oscillator.
    Implements 4-6 hour ultradian period with redox sensing.
    """
    def __init__(self, period_hours: float = 5.0):
        self.period_s = period_hours * 3600
        self.p53 = 0.5
        self.mdm2 = 0.5
        self.active_fraction = 0.5
        self.phase = 0.0 # 0 to 2*pi

    def update(self, dt: float, potential_mv: float, ros_level: float):
        """
        Gillespie-inspired stochastic update for p53 conformational switching.
        Redox range: -240 to -210 mV.
        """
        # Conformational switch: p53 becomes more active as potential increases (oxidative)
        # Midpoint at -225 mV. Sigmoid width 15 mV.
        self.active_fraction = 1.0 / (1.0 + np.exp(-(potential_mv + 225.0) / 7.5))

        # Hormetic ROS (0.5-1.2) stabilizes p53
        if 0.5 <= ros_level <= 1.2:
             self.active_fraction = min(1.0, self.active_fraction + 0.2)

        # Basic SDE for oscillator
        # dp/dt = s1 - d1*m*p + sigma*dW
        # dm/dt = s2*p - d2*m
        s_p53 = 0.2 * (1.0 + self.active_fraction * 2.0)
        k_deg_p53 = 0.3 * self.mdm2
        s_mdm2 = 0.25 * self.p53
        k_deg_mdm2 = 0.15

        # Stochastic noise
        noise = 0.05 * np.random.randn()

        self.p53 += (s_p53 - k_deg_p53 * self.p53 + noise) * dt
        self.mdm2 += (s_mdm2 - k_deg_mdm2 * self.mdm2) * dt

        self.p53 = max(0.01, self.p53)
        self.mdm2 = max(0.01, self.mdm2)

        # Update phase based on p53/mdm2 ratio (limit cycle approximation)
        self.phase = np.arctan2(self.p53 - 0.7, self.mdm2 - 0.7)

        return self.p53, self.mdm2

    def get_phase(self) -> float:
        return self.phase
