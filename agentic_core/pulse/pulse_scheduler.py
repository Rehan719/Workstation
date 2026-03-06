import logging
import time
from .pulse_clock import PulseClock

logger = logging.getLogger(__name__)

class PulseScheduler:
    """
    BS-IV: Enforces strict latency targets using pulse-aligned time quanta.
    """
    def __init__(self, clock: PulseClock):
        self.clock = clock
        self.latency_targets = {
            "peripheral": 50.0, # ms
            "central": 800.0,   # ms
            "cardio": 120.0,    # ms
            "vision": 40.0,     # ms (CM-II)
            "audition": 10.0    # ms (CM-II)
        }

    def trigger_sensory_tick(self) -> int:
        """CM-I: Coordinates sampling of all active sensory receptors."""
        pulse = self.clock.get_current_pulse()
        logger.debug(f"PULSE TICK [Sensory]: All receptors sampled @ Pulse {pulse}")
        return pulse

    def verify_latency(self, system: str, start_ns: int) -> bool:
        elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        target = self.latency_targets.get(system, 1000.0)

        if elapsed_ms > target:
            logger.error(f"PULSE LATENCY BREACH: {system} took {elapsed_ms:.4f}ms (target: {target}ms)")
            return False
        return True
