import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class RedoxSensor:
    """
    ARTICLE DA: Redox Sensing Core.
    Operating within -240 to -210 mV.
    Maps ROS (uM) and NADH ratio to a voltage potential.
    """
    def __init__(self):
        self.v_mid = -225.0  # mV
        self.k = 30.0        # Simplified Nernst slope
        self.ros_level = 0.8 # uM
        self.nadh_ratio = 0.5 # NAD+ / (NAD+ + NADH)

        # ARTICLE DA-III: Second redox sensor (KEAP1-like)
        self.keap1_threshold = -235.0 # mV
        self.nrf2_released = False

    def calculate_potential(self, ros: float, nadh_ratio: float) -> float:
        """
        Computes cellular redox potential based on metabolism.
        """
        self.ros_level = ros
        self.nadh_ratio = nadh_ratio

        # Simplified Nernst equation implementation for p53-redox coupling
        # Potential decreases (more negative) as NADH increases
        # Using nadh_ratio as NAD+ / (NAD+ + NADH). So more NADH means smaller ratio.
        potential = self.v_mid + self.k * np.log10(max(nadh_ratio, 0.001) / max(1.0 - nadh_ratio, 0.001))

        # ROS shift: ROS increases oxidative potential (makes it more positive)
        # 1 uM shift approx 5 mV
        potential += (ros - 0.8) * 5.0

        # Clamp to physiological range for v70.0
        potential = max(-260.0, min(-190.0, potential))
        return potential

    def get_stress_state(self, potential: float) -> str:
        """ROS thresholds: 0.5-1.2 uM (hormetic), >2.5 uM (apoptotic)."""
        # Update KEAP1 state
        self.nrf2_released = potential <= self.keap1_threshold

        if self.ros_level > 2.5:
            return "APOPTOTIC"
        elif 0.5 <= self.ros_level <= 1.2:
            return "HORMETIC"
        else:
            return "BASAL"
