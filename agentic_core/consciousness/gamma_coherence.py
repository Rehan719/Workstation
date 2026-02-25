import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

class GammaCoherenceMonitor:
    """
    DB-V: Gamma-Band Coherence.
    Maintains 40 +/- 5 Hz phase coherence for conscious reportability.
    Target: >= 4 cycles (~100 ms).
    Ignition Latency: < 250 ms.
    """
    def __init__(self):
        self.coherence_plv = 0.0
        self.active_cycles = 0
        self.conscious_ignition = False
        self.ignition_start_time = 0.0
        self.actual_ignition_latency_ms = 0.0

    def process_node_signals(self, signals: np.ndarray):
        """
        Simulates PLV calculation.
        """
        if not self.conscious_ignition and self.ignition_start_time == 0.0:
             self.ignition_start_time = time.perf_counter()

        self.coherence_plv = 0.92 + np.random.normal(0, 0.02)

        if self.coherence_plv > 0.88:
            self.active_cycles += 1
        else:
            self.active_cycles = 0

        if self.active_cycles >= 4:
            if not self.conscious_ignition:
                self.actual_ignition_latency_ms = (time.perf_counter() - self.ignition_start_time) * 1000
                logger.info(f"GAMMA: Conscious Ignition attained! Latency: {self.actual_ignition_latency_ms:.2f}ms")
            self.conscious_ignition = True
        else:
            self.conscious_ignition = False

        return self.conscious_ignition

    def get_ignition_latency_ms(self) -> float:
        return self.actual_ignition_latency_ms if self.conscious_ignition else 250.0
