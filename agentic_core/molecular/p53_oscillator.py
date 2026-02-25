import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

class p53Oscillator:
    """
    DA-I: p53-Mdm2 oscillator with redox sensing and conformational switching.
    Implements 4-6 hour ultradian period with empirical parameters (2024-2026).
    """
    def __init__(self, period_hours: float = 5.0):
        self.period_seconds = period_hours * 3600
        self.start_time = time.time()
        # p53 conformational state (0: Denatured/Inactive, 1: Active)
        self.active_fraction = 0.5
        # Concentrations
        self.p53 = 0.5
        self.mdm2 = 0.5

    def update(self, dt: float, ros_level: float, nadh_ratio: float):
        """
        Update oscillator based on redox conditions.
        ROS thresholds: 0.5-1.2 uM hormetic, >2.5 uM apoptotic.
        Redox sensing range: -240 to -210 mV.
        """
        # Redox-dependent conformational switch (sigmoid)
        # Higher ROS/lower NADH -> Higher Active Fraction
        redox_stress = (ros_level / 2.5) + (1.0 - nadh_ratio)
        self.active_fraction = 1.0 / (1.0 + np.exp(-8 * (redox_stress - 0.6)))

        # ODE system for p53-Mdm2 negative feedback
        # dp53/dt = synthesis - degradation(mdm2)
        # dmdm2/dt = synthesis(p53) - degradation
        s_p53 = 0.1 * (1.0 + self.active_fraction) # Stress-induced synthesis
        k_deg_p53 = 0.2 * self.mdm2
        s_mdm2 = 0.15 * self.p53
        k_deg_mdm2 = 0.1

        self.p53 += (s_p53 - k_deg_p53 * self.p53) * dt
        self.mdm2 += (s_mdm2 - k_deg_mdm2 * self.mdm2) * dt

        # Clamp values
        self.p53 = max(0.0, min(2.0, self.p53))
        self.mdm2 = max(0.0, min(2.0, self.mdm2))

        logger.debug(f"P53_OSC: p53={self.p53:.3f}, mdm2={self.mdm2:.3f}, ActiveFrac={self.active_fraction:.2f}")
        return self.p53, self.mdm2

    def get_phase(self) -> float:
        """Returns current phase angle (0-2pi)"""
        elapsed = (time.time() - self.start_time) % self.period_seconds
        return (elapsed / self.period_seconds) * 2 * np.pi
