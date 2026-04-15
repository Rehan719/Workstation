import numpy as np
from skopt import gp_minimize
from skopt.space import Real
from typing import Dict, List, Any, Callable

class AdaptiveLearning:
    """
    Truth X: Adaptive Constitutional Intelligence.
    Learns optimal constitutional rule weights using Bayesian optimization.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.was_tuning_applied = False
        self.tuning_history = []

    def optimize_rule_weight(self, rule_id: str, current_weight: float, bounds: Dict[str, float],
                             objective_fn: Callable[[float], float]) -> float:
        """
        Performs Bayesian optimization to find the optimal rule weight.
        objective_fn should return a cost (lower is better, e.g., -compliance_gain).
        """
        space = [Real(bounds['min'], bounds['max'], name='weight')]

        def skopt_objective(weight_list):
            return objective_fn(weight_list[0])

        result = gp_minimize(skopt_objective, space, n_calls=15, random_state=42)

        new_weight = float(result.x[0])
        self.was_tuning_applied = True
        self.tuning_history.append({
            "rule_id": rule_id,
            "old_weight": current_weight,
            "new_weight": new_weight,
            "improvement": -result.fun # Assuming objective_fn returns -improvement
        })

        return new_weight

    def generate_insights(self) -> Dict[str, Any]:
        return {
            "was_tuning_applied": self.was_tuning_applied,
            "tuning_history": self.tuning_history,
            "cross_domain_transfers": [] # Populated by higher level orchestrator
        }
