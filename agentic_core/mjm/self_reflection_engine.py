from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ReflectionResult:
    score: float   # 0-100
    critiques: List[Dict[str, Any]]

class SelfReflectionEngine:
    """
    Ultimate Self-Reflection Engine.
    Evaluates simulation traces against constitutional, biomimetic, and geospheric constraints.
    Emits structured, typed critiques for autonomous system response.
    """
    async def reflect(self, trace: List[Dict[str, Any]]) -> ReflectionResult:
        """
        Reflect on a sequence of events (simulation trace).
        """
        score = 100.0
        critiques = []
        for event in trace:
            # 1. Constitutional Compliance Audit
            if not event.get("constitutional_ok", True):
                critiques.append({
                    "type": "constitutional_violation",
                    "component": "governance",
                    "message": f"Constitutional violation: {event.get('id', 'unknown')}",
                    "severity": "critical"
                })
                score -= 10

            # 2. Biomimetic Fidelity Audit (Target >= 0.90)
            fidelity = event.get("fidelity", 1.0)
            if fidelity < 0.9:
                critiques.append({
                    "type": "low_fidelity",
                    "component": "biomimicry",
                    "message": f"Low biomimetic fidelity ({fidelity:.2f}) for event {event.get('id', 'unknown')}",
                    "severity": "warning"
                })
                score -= 5

            # 3. Geospheric Homeostasis Audit (Tolerance check ±5%)
            deviations = event.get("deviations", {})
            for cycle, deviation in deviations.items():
                if abs(deviation) > 0.05:
                    critiques.append({
                        "type": "homeostasis_breach",
                        "component": cycle,
                        "message": f"Homeostasis breach in {cycle} cycle: {deviation*100:.1f}% deviation",
                        "severity": "critical" if abs(deviation) > 0.1 else "warning",
                        "deviation": deviation
                    })
                    score -= 5

            # 4. Metabolic Waste Audit (Closed-loop transformation)
            waste = event.get("waste", 0)
            if waste > 0:
                critiques.append({
                    "type": "unreclaimed_waste",
                    "component": "metabolism",
                    "message": f"Unreclaimed metabolic waste detected: {waste:.3f} units",
                    "severity": "critical",
                    "waste_units": waste
                })
                score -= 20

        score = max(0.0, min(100.0, score))
        return ReflectionResult(score=score, critiques=critiques)
