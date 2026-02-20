from typing import List, Dict, Any, Optional
import numpy as np

class AdaptiveConvergenceChecker:
    """
    Article R: Dual-metric adaptive convergence checking.
    Monitors both Energy (Primary) and Shannon Entropy (Secondary).
    """
    def __init__(self, energy_threshold: float = 1e-4, entropy_threshold: float = 0.01):
        self.energy_threshold = energy_threshold
        self.entropy_threshold = entropy_threshold
        self.energy_history = []
        self.entropy_history = []

    def check(self, energy: float, state_vector: Optional[np.ndarray] = None) -> bool:
        """
        Returns True if converged based on dual metrics.
        """
        self.energy_history.append(energy)

        # Calculate entropy if state vector provided
        if state_vector is not None:
            probs = np.abs(state_vector)**2
            entropy = -np.sum(probs * np.log2(probs + 1e-12))
            self.entropy_history.append(entropy)

        if len(self.energy_history) < 5:
            return False

        # 1. Primary Metric: Energy delta
        energy_delta = abs(self.energy_history[-1] - self.energy_history[-2])

        # 2. Secondary Metric: Entropy stability (Article R)
        entropy_stable = True
        if self.entropy_history:
            entropy_delta = abs(self.entropy_history[-1] - self.entropy_history[-2])
            entropy_stable = entropy_delta < self.entropy_threshold

        is_converged = (energy_delta < self.energy_threshold) and entropy_stable
        return is_converged
