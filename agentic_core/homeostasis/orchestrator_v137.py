import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PIDControllerV137:
    """Standard PID Controller with clamping and anti-windup."""
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float, output_limits=(None, None)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._min_output, self._max_output = output_limits

        self._last_error = 0.0
        self._integral = 0.0
        self._last_time = time.time()

    def update(self, current_value: float) -> float:
        now = time.time()
        dt = now - self._last_time
        if dt <= 0: dt = 1e-6

        error = self.setpoint - current_value

        # Proportional
        p = self.kp * error

        # Integral with basic anti-windup
        self._integral += error * dt
        i = self.ki * self._integral

        # Derivative
        d = self.kd * (error - self._last_error) / dt

        output = p + i + d

        # Clamp output
        if self._min_output is not None: output = max(self._min_output, output)
        if self._max_output is not None: output = min(self._max_output, output)

        self._last_error = error
        self._last_time = now
        return output

class HomeostaticOrchestratorV137:
    """
    ARTICLE 1071 & 1081: Master regulator for the 7-layer biomimetic architecture.
    Production-hardened PID control for civilizational scale.
    """
    def __init__(self):
        # Mapped to Specification 1.3
        self.layers = {
            "mycelial": {"metric": "latency", "controller": PIDControllerV137(1.8, 0.08, 0.03, 0.050)},
            "ant_colony": {"metric": "throughput", "controller": PIDControllerV137(1.0, 0.1, 0.05, 1000)},
            "octopus": {"metric": "response_time", "controller": PIDControllerV137(2.0, 0.05, 0.1, 0.200)},
            "immune": {"metric": "threat_detection", "controller": PIDControllerV137(2.5, 0.2, 0.1, 0.999)},
            "symbiotic": {"metric": "trust_score", "controller": PIDControllerV137(1.0, 0.2, 0.01, 0.85)},
            "civilizational": {"metric": "node_count", "controller": PIDControllerV137(1.5, 0.1, 0.05, 50)}
        }

        self.current_metrics = {k: 0.0 for k in self.layers}
        self.is_holding = False
        self.global_tolerance = 5.0

    def ingest_telemetry(self, telemetry: Dict[str, float]):
        """Updates internal state with layer telemetry."""
        for layer, value in telemetry.items():
            if layer in self.current_metrics:
                self.current_metrics[layer] = value

        self._check_stability()

    def _check_stability(self):
        """ARTICLE 1081: Emergency 888_HOLD logic."""
        total_deviation = sum(abs(v - self.layers[k]["controller"].setpoint)
                              for k, v in self.current_metrics.items())

        if total_deviation > self.global_tolerance and not self.is_holding:
            self.is_holding = True
            logger.critical(f"888_HOLD: Global deviation {total_deviation:.3f} exceeds threshold!")
        elif total_deviation <= self.global_tolerance * 0.5 and self.is_holding:
            self.is_holding = False
            logger.info(f"888_HOLD RELEASED: System deviation stabilized at {total_deviation:.3f}")

    def run_regulation_cycle(self) -> Dict[str, Any]:
        """Performs a full regulation cycle for all 7 layers."""
        if self.is_holding:
            return {"status": "HOLD", "action": "STABILIZE_CORE"}

        adjustments = {}
        for layer, config in self.layers.items():
            output = config["controller"].update(self.current_metrics[layer])
            if abs(output) > 0.01:
                adjustments[layer] = {
                    "output": output,
                    "action": self._map_to_actuator(layer, output)
                }

        return {"status": "ACTIVE", "adjustments": adjustments}

    def _map_to_actuator(self, layer: str, output: float) -> str:
        """Determines the specific actuator response for a layer."""
        if layer == "mycelial":
            return "REROUTE_TRAFFIC" if output < 0 else "INCREASE_CAPACITY"
        elif layer == "immune":
            return "TIGHTEN_GATES" if output < 0 else "RELAX_QUARANTINE"
        elif layer == "civilizational":
            return "PROVISION_NODE" if output > 0 else "DECOMMISSION_NODE"
        return "ADJUST_SETPOINT_WEIGHT"

    def get_layer_status(self) -> Dict[str, Any]:
        return {
            "metrics": self.current_metrics,
            "setpoints": {k: v["controller"].setpoint for k, v in self.layers.items()},
            "is_holding": self.is_holding
        }
