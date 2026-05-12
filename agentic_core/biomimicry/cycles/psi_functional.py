from typing import Dict, Any, List, Optional
import numpy as np

class EcosystemHealthObjective:
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "water": 0.2,
            "carbon": 0.25,
            "nitrogen": 0.15,
            "oxygen": 0.15,
            "phosphorus": 0.15,
            "sulfur": 0.1
        }
        self.setpoints = {
            "water": 75.0,
            "carbon": 100.0,
            "nitrogen": 50.0,
            "oxygen": 21.0,
            "phosphorus": 30.0,
            "sulfur": 10.0
        }

    async def evaluate(self, system_state: Any) -> float:
        """
        Computes the Ψ-health score based on deviations from cycle setpoints.
        Ψ = exp(-mean(|x - x*| / x*))
        """
        deviations = []
        for name, setpoint in self.setpoints.items():
            current = getattr(system_state, f"{name}_metric", setpoint)
            deviations.append(abs(current - setpoint) / (setpoint + 1e-6))

        psi = float(np.exp(-np.mean(deviations)))
        return psi
