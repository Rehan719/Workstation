import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SocialContext:
    """
    CO-III: Social Context Awareness.
    Adapts communication style based on inferred social environment.
    """
    def determine_tone(self, context_metrics: Dict[str, Any]) -> str:
        """Determines appropriate interaction tone."""
        user_expertise = context_metrics.get("expertise", 0.5)

        if user_expertise < 0.3:
            return "educational_and_patient"
        elif user_expertise > 0.8:
            return "concise_and_expert"
        return "collaborative"
