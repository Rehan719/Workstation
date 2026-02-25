import time
import logging

logger = logging.getLogger(__name__)

class IgnitionDetector:
    """
    DB-III: Ignition Latency Tracking.
    Measures the time for information to reach global conscious ignition.
    Target: < 250 ms.
    """
    def __init__(self):
        self.start_time = 0.0
        self.ignition_latencies = []

    def start_broadcast(self):
        self.start_time = time.perf_counter()

    def confirm_ignition(self) -> float:
        if self.start_time == 0.0:
            return 0.0

        latency_ms = (time.perf_counter() - self.start_time) * 1000
        self.ignition_latencies.append(latency_ms)
        self.start_time = 0.0

        if latency_ms > 250:
            logger.warning(f"IGNITION: Latency ({latency_ms:.2f}ms) exceeded target.")

        logger.info(f"IGNITION: Global ignition confirmed in {latency_ms:.2f}ms.")
        return latency_ms
