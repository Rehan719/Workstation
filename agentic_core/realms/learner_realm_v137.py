import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class LearnerRealmV137:
    """
    ARTICLE 1042 & 1076: The Garden of Curiosity.
    Implements neuro-adaptive pacing and Knowledge Gardens.
    """
    def __init__(self):
        self.mastery_levels = {} # user_id -> {concept -> progress}
        self.garden_status = {} # user_id -> List of active "flowers"

    def process_interaction(self, user_id: str, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes engagement proxies to adapt pacing."""
        speed = interaction.get("response_speed_ms", 2000)
        accuracy = interaction.get("accuracy", 0.8)

        # Adaptation logic (Spec 4.1)
        if speed < 1000 and accuracy > 0.9:
            adjustment = "INCREASE_CHALLENGE"
        elif speed > 5000 or accuracy < 0.6:
            adjustment = "DECREASE_CHALLENGE"
        else:
            adjustment = "MAINTAIN_PACE"

        logger.info(f"LearnerRealm: Adjusted {user_id} pacing to {adjustment}")

        return {
            "pacing_adjustment": adjustment,
            "flow_state": "OPTIMAL" if adjustment == "MAINTAIN_PACE" else "ADAPTING"
        }

    def update_mastery(self, user_id: str, concept: str, score: float) -> Dict[str, Any]:
        """Concepts 'bloom' in the Knowledge Garden upon mastery."""
        if user_id not in self.mastery_levels:
            self.mastery_levels[user_id] = {}

        current = self.mastery_levels[user_id].get(concept, 0.0)
        new_progress = min(1.0, current + score)
        self.mastery_levels[user_id][concept] = new_progress

        bloom_event = False
        if new_progress >= 1.0:
            if user_id not in self.garden_status:
                self.garden_status[user_id] = []
            if concept not in self.garden_status[user_id]:
                self.garden_status[user_id].append(concept)
                bloom_event = True
                logger.info(f"LearnerRealm: Concept '{concept}' bloomed for user {user_id}!")

        return {
            "concept": concept,
            "progress": new_progress,
            "bloomed": bloom_event,
            "garden_size": len(self.garden_status.get(user_id, []))
        }

    def get_garden_visuals(self, user_id: str) -> List[str]:
        """Returns the list of mastered concepts (flowers) for the UI."""
        return self.garden_status.get(user_id, [])
