from typing import Dict, Any, List, Optional

class EcosystemHealthObjective:
    """
    Unified ecosystem health evaluation combining all six biogeochemical cycles (Ψ-Functional).
    Ψ(π) = α·η_water + β·η_carbon + γ·η_nitrogen + δ·η_oxygen + ε·η_phosphorus + ζ·η_sulfur
    """
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "water": 0.15,
            "carbon": 0.20,
            "nitrogen": 0.15,
            "oxygen": 0.15,
            "phosphorus": 0.15,
            "sulfur": 0.10,
            "divine_alignment": 0.10 # Included as per mandate
        }

    def evaluate(
        self,
        metrics: Dict[str, float],
        closed_loop_compliance: float = 1.0,
        biomimetic_fidelity: float = 1.0
    ) -> float:
        """Evaluates health with hard constraints."""

        # Hard constraints
        if closed_loop_compliance < 1.0 or biomimetic_fidelity < 0.9:
            return float('-inf')

        score = 0.0
        for cycle, weight in self.weights.items():
            score += weight * metrics.get(cycle, 1.0)

        return score
