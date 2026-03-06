from typing import Dict, Any, List

class PerformanceDegradationDetector:
    """CQ-II: Performance Degradation Detection."""

    def detect(self, telemetry: List[Dict[str, Any]]) -> float:
        # Scale: -1 to +1
        # Target: >12.7% latency increase or >9.3% accuracy drop over 3 cycles
        if len(telemetry) < 3:
            return 0.0

        recent = telemetry[-3:]
        latency_change = (recent[-1]["latency"] / recent[0]["latency"]) - 1.0
        accuracy_change = recent[0]["accuracy"] - recent[-1]["accuracy"]

        if latency_change > 0.127 or accuracy_change > 0.093:
            return 1.0

        return 0.0
