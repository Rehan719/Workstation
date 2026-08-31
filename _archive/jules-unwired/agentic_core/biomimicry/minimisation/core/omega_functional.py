import torch
from typing import Dict, Any, Optional

class MinimisationObjective:
    """
    Unified objective combining all natural minimisation principles (The Ω-Functional).
    J(π) = α·F[π] + β·W_ε(μ,ν) + γ·KL(π||R) + δ·S_export[π] + ζ·M[π]

    Hard Constraint: If legal_compliance < 1.0, J(π) = ∞
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None, legal_precision_weight: float = 1.0):
        self.weights = weights or {
            "free_energy": 0.30,      # Surprise minimisation
            "optimal_transport": 0.25, # Resource efficiency
            "schrodinger_bridge": 0.20,# Path likelihood
            "entropy_export": 0.15,    # Thermodynamic efficiency
            "murray_law": 0.10         # Branching network efficiency
        }
        self.legal_precision_weight = legal_precision_weight

    def evaluate(
        self,
        policy_metrics: Dict[str, float],
        context: Dict[str, Any],
        legal_compliance: float = 1.0
    ) -> float:
        """
        Evaluate the Ω-functional for a given policy and state.

        Args:
            policy_metrics: Dictionary of metric values (fe, ot, sb, ee, ml)
            context: System context (layer, domain)
            legal_compliance: Coverage score [0, 1]

        Returns:
            Computed cost J(π)
        """
        # 1. Legal Precision Hard Constraint (Non-negotiable)
        is_legal_domain = context.get("layer") == "L12_Policy" or context.get("domain") == "legal"
        if is_legal_domain and legal_compliance < 1.0:
            return float('inf')

        # 2. Weighted sum of minimisation objectives
        score = 0.0
        objective_map = {
            "free_energy": policy_metrics.get("free_energy", 0.0),
            "optimal_transport": policy_metrics.get("optimal_transport", 0.0),
            "schrodinger_bridge": policy_metrics.get("schrodinger_bridge", 0.0),
            "entropy_export": policy_metrics.get("entropy_export", 0.0),
            "murray_law": policy_metrics.get("murray_law", 0.0)
        }

        for key, weight in self.weights.items():
            score += weight * objective_map.get(key, 0.0)

        # 3. Penalty for partial legal compliance (soft constraint for non-critical domains)
        if not is_legal_domain and legal_compliance < 1.0:
            score += (1.0 - legal_compliance) * 1000.0  # Large penalty

        return score
