import logging
import time
from typing import Dict, Any, List
from .p53_oscillator import p53Oscillator
from .ubiquitin_system import UbiquitinSystem
from .hsp_network import HSPNetwork
from .redox_sensor import RedoxSensor
from .atp_simulator import ATPSimulator

logger = logging.getLogger(__name__)

class TriadIntegrator:
    """
    ARTICLE DA: The definitive metabolic-respiratory core integration.
    """
    def __init__(self):
        self.redox_sensor = RedoxSensor()
        self.p53_osc = p53Oscillator()
        self.ubiquitin = UbiquitinSystem()
        self.hsp = HSPNetwork()
        self.atp = ATPSimulator()
        self.last_update = time.time()

    def run_cycle(self, ros_level: float = 0.8, nadh_ratio: float = 0.5) -> Dict[str, Any]:
        """
        Executes one metabolic pulse cycle.
        """
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # 1. Redox Sensing
        potential = self.redox_sensor.calculate_potential(ros_level, nadh_ratio)
        stress_state = self.redox_sensor.get_stress_state(potential)

        # 2. ATP Simulation
        atp_ratio = self.atp.update(dt, ros_level * 2.0)

        # 3. p53 Oscillation
        p53_val, mdm2_val = self.p53_osc.update(dt, potential, ros_level)

        # 4. Ubiquitin & HSP Maintenance
        degraded = self.ubiquitin.update(dt)
        atp_turnover = self.hsp.calculate_turnover(atp_ratio, ros_level)

        state = {
            "redox_potential_mv": potential,
            "stress_state": stress_state,
            "atp_adp_ratio": atp_ratio,
            "p53_level": p53_val,
            "p53_phase": self.p53_osc.get_phase(),
            "ubiquitin_stress": self.ubiquitin.stress_index,
            "hsp_atp_turnover": atp_turnover,
            "degraded_components": degraded
        }

        logger.info(f"TRIAD_PULSE: State={stress_state}, Pot={potential:.1f}mV, p53={p53_val:.2f}")
        return state
