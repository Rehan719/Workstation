import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmotionalStateMachine:
    """
    CN-III: Emotional State Machine.
    Core affect model (Valence, Arousal, Dominance) influencing decision making.
    """
    def __init__(self):
        self.affect = {
            "valence": 0.5,  # [0: Unpleasant, 1: Pleasant]
            "arousal": 0.3,  # [0: Calm, 1: Excited]
            "dominance": 0.7 # [0: Controlled, 1: Controlling]
        }

    def process_stimulus(self, salience: float, impact: float):
        """Updates emotional state based on significant events."""
        # Simple affect update logic
        self.affect["arousal"] = min(1.0, self.affect["arousal"] + salience * 0.2)

        if impact > 0:
            self.affect["valence"] = min(1.0, self.affect["valence"] + impact * 0.1)
        else:
            self.affect["valence"] = max(0.0, self.affect["valence"] + impact * 0.15)

        logger.info(f"EMOTION: State updated. Arousal: {self.affect['arousal']:.2f}, Valence: {self.affect['valence']:.2f}")

    def get_resource_bias(self) -> float:
        """Returns a multiplier for resource allocation based on arousal."""
        return 1.0 + (self.affect["arousal"] * 0.5)
