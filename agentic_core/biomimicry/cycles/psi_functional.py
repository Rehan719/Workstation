from typing import Dict, Any, List, Optional
import numpy as np

class EcosystemHealthObjective:
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "free_energy": 0.10,
            "optimal_transport": 0.10,
            "schrodinger_bridge": 0.08,
            "entropy_export": 0.08,
            "murray_law": 0.05,
            "quantum_security": 0.03,
            "hyperdimensional_transfer": 0.07,
            "biomimetic_fidelity": 0.03,
            "genetic_integrity": 0.08,
            "immune_defense": 0.07,
            "geospheric_homeostasis": 0.13,
            "closed_loop_transformation": 0.18
        }

    def evaluate(
        self,
        cycle_scores: Dict[str, float],
        system_metrics: Dict[str, float],
        legal_compliance: float = 1.0,
        closed_loop_waste: float = 0.0,
        biomimetic_fidelity: float = 1.0,
        genetic_integrity: float = 1.0
    ) -> float:
        if legal_compliance < 1.0 or closed_loop_waste > 0.0 or biomimetic_fidelity < 0.9 or genetic_integrity < 1.0:
            return float('-inf')

        gh = np.mean(list(cycle_scores.values()))

        comps = {
            "free_energy": system_metrics.get("free_energy", 1.0),
            "optimal_transport": system_metrics.get("optimal_transport", 1.0),
            "schrodinger_bridge": system_metrics.get("schrodinger_bridge", 1.0),
            "entropy_export": system_metrics.get("entropy_export", 1.0),
            "murray_law": system_metrics.get("murray_law", 1.0),
            "quantum_security": system_metrics.get("quantum_security", 1.0),
            "hyperdimensional_transfer": system_metrics.get("hyperdimensional_transfer", 1.0),
            "biomimetic_fidelity": biomimetic_fidelity,
            "genetic_integrity": genetic_integrity,
            "immune_defense": system_metrics.get("immune_defense", 1.0),
            "geospheric_homeostasis": gh,
            "closed_loop_transformation": 1.0 - closed_loop_waste
        }
        return sum(self.weights[k] * comps[k] for k in self.weights)
