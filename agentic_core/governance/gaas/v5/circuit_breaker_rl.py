import random
from typing import Dict, Any, List, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class SelfTuningCircuitBreaker:
    """
    RL-Based Self-Tuning Circuit Breaker (v140.0).
    Adapts error thresholds dynamically based on constitutional telemetry.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.error_threshold = 5 # Initial
        self.consecutive_errors = 0
        self.reward_history = []

    async def check_health(self, last_action_success: bool) -> bool:
        """Evaluate status and tune threshold via simplified RL."""
        if not last_action_success:
            self.consecutive_errors += 1
            # Negative reward for error
            self._update_rl_policy(-1.0)
        else:
            self.consecutive_errors = 0
            # Positive reward for success
            self._update_rl_policy(0.1)

        tripped = self.consecutive_errors >= self.error_threshold
        if tripped:
            await self.ueg.log_minimisation_event("circuit_breaker_tripped", {"threshold": self.error_threshold})

        return tripped

    def _update_rl_policy(self, reward: float):
        """Simple Policy Gradient approximation to tune threshold."""
        self.reward_history.append(reward)
        if len(self.reward_history) > 10:
            avg_reward = sum(self.reward_history[-10:]) / 10
            if avg_reward < -0.5:
                # Too many errors, tighten threshold
                self.error_threshold = max(2, self.error_threshold - 1)
            elif avg_reward > 0.05:
                # System stable, relax threshold
                self.error_threshold = min(20, self.error_threshold + 1)
            self.reward_history = [] # Reset for next tuning window
