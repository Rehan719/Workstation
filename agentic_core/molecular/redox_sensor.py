import logging
import numpy as np

logger = logging.getLogger(__name__)

class RedoxSensor:
    """
    Simulates cellular redox state: NAD+/NADH and ROS levels.
    Redox potential range: -240 to -210 mV.
    """
    def __init__(self):
        self.ros_level = 0.3 # uM
        self.nad_nadh_ratio = 8.0 # Baseline
        self.redox_mv = -230.0 # Baseline mV

    def update_state(self, metabolic_load: float):
        """
        metabolic_load: 0.0 (idle) to 1.0 (overload)
        Higher load -> Higher ROS, lower NAD/NADH, higher potential (less negative).
        """
        # Linear/sigmoid mapping
        self.ros_level = 0.1 + (metabolic_load * 3.0) # 0.1 to 3.1 uM
        self.nad_nadh_ratio = max(1.0, 10.0 - (metabolic_load * 8.0))

        # Nernst-like potential shift
        # -240 (healthy) to -210 (oxidized)
        self.redox_mv = -240.0 + (metabolic_load * 30.0)

        logger.debug(f"REDOX: ROS={self.ros_level:.2f}uM, Ratio={self.nad_nadh_ratio:.1f}, Potential={self.redox_mv:.1f}mV")
        return self.ros_level, self.nad_nadh_ratio, self.redox_mv
