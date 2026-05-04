from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ReflectionResult:
    score: float   # 0-100
    critiques: List[Dict[str, Any]]

class SelfReflectionEngine:
    """
    Continuously evaluates the twin’s simulation trace against the constitution,
    biomimetic fidelity, and geospheric homeostasis. Emits criticism and
    generates improvement hypotheses.
    """
    async def reflect(self, trace: List[Dict[str, Any]]) -> ReflectionResult:
        """
        Reflect on a sequence of events (simulation trace).
        """
        score = 100.0
        critiques = []
        for event in trace:
            # Constitutional compliance
            if not event.get("constitutional_ok", True):
                critiques.append({
                    "type": "constitutional_violation",
                    "component": "governance",
                    "message": f"Constitutional violation: {event.get('id', 'unknown')}"
                })
                score -= 10

            # Biomimetic fidelity check (Target >= 0.90)
            fidelity = event.get("fidelity", 1.0)
            if fidelity < 0.9:
                critiques.append({
                    "type": "low_fidelity",
                    "component": "biomimicry",
                    "message": f"Low biomimetic fidelity ({fidelity:.2f}): {event.get('id', 'unknown')}"
                })
                score -= 5

            # Geospheric homeostasis (Tolerance check)
            deviations = event.get("deviations", {})
            for cycle, deviation in deviations.items():
                if abs(deviation) > 0.05:
                    critiques.append({
                        "type": "homeostasis_breach",
                        "component": cycle,
                        "message": f"Homeostasis breach in {cycle} cycle: {deviation*100:.1f}% deviation"
                    })
                    score -= 5

            # Closed-loop waste check
            waste = event.get("waste", 0)
            if waste > 0:
                critiques.append({
                    "type": "unreclaimed_waste",
                    "component": "metabolism",
                    "message": f"Unreclaimed waste detected: {waste} units"
                })
                score -= 20

        score = max(0, min(100, score))
        return ReflectionResult(score=score, critiques=critiques)
