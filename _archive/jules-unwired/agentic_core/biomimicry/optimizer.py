import time
import logging
import random
from typing import Dict, Any, List

class SelfOptimisationEngine:
    """
    Autonomous reconfiguration of system parameters using Reinforcement Learning.
    Adjusts resource allocation, channel priorities, and replication factors.
    """
    def __init__(self, ueg_callback=None):
        self.logger = logging.getLogger("Optimizer")
        self.ueg_callback = ueg_callback
        # Current system state/parameters
        self.params = {
            "replication_factor": 3,
            "max_swarm_size": 20,
            "latency_buffer_ms": 15.0
        }
        self.reward_history: List[float] = []

    def step(self, kpis: Dict[str, float]):
        """
        Executes an optimization step based on current KPIs.
        """
        # Calculate Reward (Composite of KPIs)
        # Latency (inverse), Accuracy, Energy (inverse)
        reward = (1.0 / (kpis.get("latency_ms", 50) + 1)) * 100 + kpis.get("accuracy", 0) * 10
        self.reward_history.append(reward)

        # Policy Selection (Simulated PPO)
        action = random.choice(["INCREASE_REPLICATION", "DECREASE_REPLICATION", "IDLE"])

        if action == "INCREASE_REPLICATION" and self.params["replication_factor"] < 10:
            self.params["replication_factor"] += 1
        elif action == "DECREASE_REPLICATION" and self.params["replication_factor"] > 1:
            self.params["replication_factor"] -= 1

        self.logger.info(f"Self-Opt: KPI reward {reward:.2f} | Action: {action} | New Params: {self.params}")

        self._emit_event("SYSTEM_OPTIMIZED", {
            "action": action,
            "reward": reward,
            "new_params": self.params
        })

        return self.params

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "SelfOptimisationEngine",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    opt = SelfOptimisationEngine()
    for _ in range(5):
        opt.step({"latency_ms": 10 + random.random()*40, "accuracy": 0.85})
