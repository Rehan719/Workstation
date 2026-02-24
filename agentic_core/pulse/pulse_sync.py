import logging
from .pulse_clock import PulseClock

logger = logging.getLogger(__name__)

class PulseSync:
    """
    BS-III: Synchronization interface for all biological subsystems.
    Ensures subsystems operate in lockstep with the 1.2MHz clock.
    """
    def __init__(self, clock: PulseClock):
        self.clock = clock
        self.subsystem_offsets = {}

    def heartbeat(self, subsystem_name: str):
        pulse = self.clock.get_current_pulse()
        logger.debug(f"HEARTBEAT [{subsystem_name}]: Pulse {pulse}")
        return pulse
