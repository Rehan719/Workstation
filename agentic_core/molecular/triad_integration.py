import logging
import time
from typing import Dict, Any
from .p53_oscillator import p53Oscillator
from .ubiquitin_system import UbiquitinSystem
from .hsp_network import HSPNetwork
from .redox_sensor import RedoxSensor
from .atp_simulator import ATPSimulator

logger = logging.getLogger(__name__)

class MolecularTriad:
    """
    DA-IV: Triad Integration.
    Couples p53, Ubiquitin, and HSP systems into a closed-loop metabolic-respiratory governor.
    """
    def __init__(self):
        self.p53 = p53Oscillator()
        self.ubiquitin = UbiquitinSystem()
        self.hsp = HSPNetwork()
        self.redox = RedoxSensor()
        self.atp = ATPSimulator()
        self.last_step_time = time.time()
        self.tagging_latency_s = 0.0

    def run_step(self, substrate_availability: float, demand: float) -> Dict[str, Any]:
        """
        Executes a biological integration step.
        substrate: 0.0 to 1.0 (input nutrient flux)
        demand: 0.0 to 1.0 (executive/task load)
        """
        start_step = time.perf_counter()
        now = time.time()
        dt = now - self.last_step_time
        self.last_step_time = now

        # 1. Update Sensors
        ros, nad_ratio, mv = self.redox.update_state(metabolic_load=demand)
        energy_ratio = self.atp.update(production=substrate_availability, demand=demand)

        # 2. Update Components
        p53_level, mdm2_level = self.p53.update(dt, ros, nad_ratio / 10.0)
        degraded = self.ubiquitin.process_cycle(dt)
        refolded = self.hsp.process_refolding(dt, energy_ratio)

        # DA-II: Tagging Latency tracking
        # We simulate tagging latency based on ubiquitin stress
        self.tagging_latency_s = self.ubiquitin.get_stress_index() * 5.0 # Up to 5s

        # DA-II: Tagging latency < 3.7 s inhibits registry writes until refolding >= 92% fidelity.
        registry_inhibited = self.tagging_latency_s > 3.7
        refolding_fidelity = 0.95 if not degraded else 0.85 # Simplified

        # 3. Cross-Coupling Logic (Closed Loop)
        if ros > 2.5:
             logger.critical("TRIAD: Apoptotic threshold exceeded. Triggering genomic stress protocols.")
             self.ubiquitin.tag_resource("ExcessMetabolite_Critical", "K48", 0.9)

        if p53_level > 1.2:
             self.hsp.bind_misfolded(f"Protein_Denatured_p53_{int(time.time())}")

        state_vector = {
            "p53_level": p53_level,
            "p53_phase": self.p53.get_phase(),
            "ubiquitin_stress": self.ubiquitin.get_stress_index(),
            "hsp_occupancy": self.hsp.get_occupancy_rate(),
            "ros_level": ros,
            "nad_nadh_ratio": nad_ratio,
            "atp_adp_ratio": energy_ratio,
            "redox_potential_mv": mv,
            "tagging_latency_s": self.tagging_latency_s,
            "registry_inhibited": registry_inhibited,
            "refolding_fidelity": refolding_fidelity
        }

        logger.info(f"TRIAD_STEP: p53={p53_level:.2f}, Energy={energy_ratio:.2f}, ROS={ros:.2f}")
        return state_vector
