from typing import Dict, Any

class EcosystemHealthObjective:
    """
    Evaluates Global Ecosystem Health (Ψ‑functional).
    Targets Ψ ≥ 0.90 for high‑fidelity biological regulation.
    """
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights
        self.setpoints = {
            "water": 75.0,
            "carbon": 50.0,
            "nitrogen": 10.0,
            "oxygen": 60.0,
            "phosphorus": 80.0,
            "sulfur": 1.0
        }

    async def evaluate(self, system_state) -> float:
        scores = []
        for name, weight in self.weights.items():
            metric = getattr(system_state, f"{name}_metric", None)
            setpoint = self.setpoints.get(name, 100.0)

            if metric is not None:
                deviation = abs(metric - setpoint)
                tolerance = max(0.1, setpoint * 0.05)
                fidelity = max(0.0, 1.0 - (deviation / tolerance))
                scores.append(fidelity * weight)

        return sum(scores) if scores else 0.0
