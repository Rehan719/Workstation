import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SelfAwarenessModule:
    """
    CN-I: Self-Awareness Module.
    Maintains a dynamic model of the organism's own cognitive state.
    """
    def __init__(self):
        self.state = {
            "goals": [],
            "active_hypotheses": [],
            "emotional_valence": 0.8,  # [0.0 - 1.0]
            "cognitive_load": 0.2,     # [0.0 - 1.0]
            "self_confidence": 0.9     # [0.0 - 1.0]
        }

    def update_state(self, internal_metrics: Dict[str, Any]):
        """Updates internal model based on allostatic load and success rates."""
        allostatic_load = internal_metrics.get("allostatic_load", 0.0)
        success_rate = internal_metrics.get("success_rate", 1.0)

        # Mapping stress to cognitive load
        self.state["cognitive_load"] = allostatic_load / 10.0

        # Satisfaction influence
        if success_rate > 0.9:
            self.state["emotional_valence"] = min(1.0, self.state["emotional_valence"] + 0.05)
        elif success_rate < 0.5:
            self.state["emotional_valence"] = max(0.0, self.state["emotional_valence"] - 0.1)

        logger.info(f"PSYCHOLOGY: Self-model updated. Valence: {self.state['emotional_valence']:.2f}")
        return self.state

    def get_current_focus(self) -> str:
        if self.state["cognitive_load"] > 0.7:
            return "recovery"
        return "exploration"
