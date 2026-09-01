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
        # Simulated Stress Scenarios (Minimizers)
        stressors = ["hypoxia", "oxidative_burst", "high_load", "thermal_stress"]

        scores: Dict[str, float] = {}
        for action in actions:
            min_utility = float('inf')
            for stressor in stressors:
                # Calculate utility under stress
                utility = utility_func(state, action, stressor)
                if utility < min_utility:
                    min_utility = utility
            scores[action] = min_utility

        # W431 — §4.5 class. This used a strict `>` walk over the action list, so when the utility
        # function does not read `action` (the shipped `default_utility_func` accepts it and never
        # uses it) EVERY action scores identically and the walk silently returns whichever the caller
        # listed FIRST. Proved live on this endpoint: the same three actions reordered produced a
        # different "decision", and with one ordering it reported `detonate_reactor` as the
        # maximin-optimal action under adversarial stress — while the response asserted
        # "minimax adversarial (owned cognition)".
        #
        # A utility that cannot tell two actions apart has not chosen between them. Say so.
        max_min_utility = max(scores.values()) if scores else -float('inf')
        top = sorted(a for a, s in scores.items() if s == max_min_utility)
        discriminated = len(scores) > 1 and len(top) < len(scores)
        tied = len(top) > 1
        best_action = top[0] if (top and not tied) else None

        consistency = 1.0 if max_min_utility >= self.threshold else (max_min_utility / self.threshold)

        logger.info("Minimax: action=%s discriminated=%s tied=%s consistency=%.2f",
                    best_action, discriminated, tied, consistency)
        return {
            "selected_action": best_action,
            "consistency_score": consistency,
            "worst_case_utility": max_min_utility,
            "per_action_utility": scores,
            "discriminated": discriminated,
            "tied_actions": top if tied else [],
            "basis": ("no actions supplied" if not scores else
                      f"the utility function scored all {len(scores)} actions identically at "
                      f"{max_min_utility} - it did not distinguish between them, so no action was "
                      f"selected" if tied and len(top) == len(scores) else
                      f"{len(top)} actions tied at {max_min_utility}" if tied else
                      f"{best_action} has the highest worst-case utility {max_min_utility}"),
        }

def default_utility_func(state: Dict[str, Any], action: str, stressor: str) -> float:
    """Default utility calculator based on Survival Instinct Hierarchy."""
    base = state.get("base_stability", 0.9)
    if stressor == "hypoxia": base -= 0.3
    if stressor == "high_load": base -= 0.1
    return max(0.0, base)
