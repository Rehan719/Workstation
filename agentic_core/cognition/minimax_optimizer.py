import logging
import numpy as np
from typing import List, Dict, Any, Callable

logger = logging.getLogger(__name__)

class MinimaxOptimizer:
    """
    ARTICLE 78: Minimax Adversarial Optimization.
    Evaluates decisions against worst-case environmental stressors.
    """
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold

    def evaluate_strategy(self, state: Dict[str, Any], actions: List[str], utility_func: Callable) -> Dict[str, Any]:
        """
        Evaluates the best action while assuming the environment acts as a minimizer.
        """
        best_action = None
        max_min_utility = -float('inf')

        # Simulated Stress Scenarios (Minimizers)
        stressors = ["hypoxia", "oxidative_burst", "high_load", "thermal_stress"]

        for action in actions:
            min_utility = float('inf')
            for stressor in stressors:
                # Calculate utility under stress
                utility = utility_func(state, action, stressor)
                if utility < min_utility:
                    min_utility = utility

            if min_utility > max_min_utility:
                max_min_utility = min_utility
                best_action = action

        consistency = 1.0 if max_min_utility >= self.threshold else (max_min_utility / self.threshold)

        logger.info(f"Minimax Optimization: Action '{best_action}' selected with consistency {consistency:.2f}")
        return {
            "selected_action": best_action,
            "consistency_score": consistency,
            "worst_case_utility": max_min_utility
        }

def default_utility_func(state: Dict[str, Any], action: str, stressor: str) -> float:
    """Default utility calculator based on Survival Instinct Hierarchy."""
    base = state.get("base_stability", 0.9)
    if stressor == "hypoxia": base -= 0.3
    if stressor == "high_load": base -= 0.1
    return max(0.0, base)
