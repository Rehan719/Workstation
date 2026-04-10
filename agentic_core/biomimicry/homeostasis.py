import time
import logging
from typing import Dict, Any

class HomeostasisMonitor:
    """
    Maintains internal stability via negative feedback loops (PID-like).
    Tracks CPU, RAM, and Latency.
    """
    def __init__(self, ueg_callback=None):
        self.logger = logging.getLogger("HomeostasisMonitor")
        self.ueg_callback = ueg_callback
        self.setpoints = {
            "cpu_target": 70.0,
            "latency_target_ms": 10.0
        }

    def monitor_vitals(self, current_vitals: Dict[str, float]):
        """
        Compares vitals to setpoints and triggers allostatic adjustments.
        """
        adjustments = []

        # Latency check (Article 1095/1096 alignment)
        if current_vitals["latency_ms"] > self.setpoints["latency_target_ms"]:
            delta = current_vitals["latency_ms"] - self.setpoints["latency_target_ms"]
            adjustments.append(f"REDUCE_LOAD: Latency delta {delta:.2f}ms")

        # CPU check
        if current_vitals["cpu_percent"] > self.setpoints["cpu_target"]:
            adjustments.append("SCALE_OUT: CPU threshold exceeded")

        if adjustments:
            self._emit_event("VITALS_STRESS", {"adjustments": adjustments, "vitals": current_vitals})
            self.logger.warning(f"Homeostasis Stress: {adjustments}")
        else:
            self._emit_event("VITALS_STABLE", {"vitals": current_vitals})

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "HomeostasisMonitor",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)
        # For simulation, we log it
        # print(f"UEG EVENT: {event_type} | {data}")

if __name__ == "__main__":
    def autonomous_ueg(e): print(f"UEG -> {e['type']}")
    hm = HomeostasisMonitor(autonomous_ueg)
    hm.monitor_vitals({"latency_ms": 15.0, "cpu_percent": 85.0})
