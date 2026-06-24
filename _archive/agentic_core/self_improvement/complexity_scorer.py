from typing import Dict, Any

class ComplexityScorer:
    """CQ-I: Task Complexity Scoring (Cognitive Load mapping)."""

    def score(self, workload: Dict[str, Any]) -> float:
        # Scale: -1 to +1
        # Target: cognitive load >= 4.2 maps to +1
        raw_load = workload.get("cognitive_load", 3.0)

        # Mapping logic: (raw - 3.0) / 2.0 scaled to [-1, 1]
        # simplified for simulation
        if raw_load >= 4.2:
            return 1.0
        elif raw_load <= 1.8:
            return -1.0
        return (raw_load - 3.0) / 1.2
