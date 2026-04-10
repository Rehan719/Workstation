import time
import logging
import random
from typing import Dict, Any, List

class RewardModel:
    """
    Mock Reward Model for RLHF loop.
    Predicts user preference based on agent behavior.
    """
    def predict(self, agent_output: str, user_context: Dict[str, Any]) -> float:
        # Simplified: reward informative but concise output
        length = len(agent_output)
        if 50 < length < 200:
            return 0.8 + (random.random() * 0.2)
        return 0.4 + (random.random() * 0.3)

class HybridFitnessFunction:
    """
    Implements the Phase 4 hybrid fitness logic.
    Technical (0.3) + User-Centric (0.7).
    """
    def __init__(self, reward_model: RewardModel):
        self.reward_model = reward_model
        self.tech_weight = 0.3
        self.user_weight = 0.7

    def calculate_fitness(self, metrics: Dict[str, Any], feedback: List[Dict[str, Any]]) -> float:
        # 1. Technical Components
        latency_score = max(0, 1 - (metrics.get("latency_ms", 100) / 500))
        accuracy_score = metrics.get("accuracy", 0.5)
        energy_score = metrics.get("energy_efficiency", 0.5)

        tech_base = (latency_score + accuracy_score + energy_score) / 3

        # 2. User-Centric Components
        # Aggregate feedback (1-5 stars)
        if feedback:
            avg_stars = sum(f["stars"] for f in feedback) / len(feedback)
            user_base = avg_stars / 5.0
        else:
            # Fallback to Reward Model prediction if no live feedback
            user_base = self.reward_model.predict("agent_output_mock", {})

        total_fitness = (self.tech_weight * tech_base) + (self.user_weight * user_base)
        return total_fitness

class FeedbackChannel:
    """
    Learner Realm Feedback Channel (Mock).
    Collects user ratings and flags for evolution.
    """
    def __init__(self, ueg_callback=None):
        self.ueg_callback = ueg_callback
        self.storage: List[Dict[str, Any]] = []

    def submit_feedback(self, agent_id: str, stars: int, flags: List[str] = None):
        entry = {
            "agent_id": agent_id,
            "stars": stars,
            "flags": flags or [],
            "timestamp": time.time()
        }
        self.storage.append(entry)
        self._emit_event("USER_FEEDBACK", entry)
        return True

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "FeedbackChannel",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    rm = RewardModel()
    hff = HybridFitnessFunction(rm)
    fb = FeedbackChannel()

    fb.submit_feedback("agent_alpha", 5)
    fb.submit_feedback("agent_alpha", 4)

    fit = hff.calculate_fitness({"latency_ms": 10, "accuracy": 0.9}, fb.storage)
    print(f"Calculated Hybrid Fitness: {fit:.4f}")
