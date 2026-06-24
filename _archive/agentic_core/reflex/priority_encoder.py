import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PriorityEncoder:
    """
    CP-I: Priority-Encoded Stimulus Processing.
    Tags sensory inputs with priority based on salience and threat.
    """
    def encode_priority(self, stimulus: Dict[str, Any]) -> str:
        """Derives priority level (reflex, urgent, deliberative)."""
        salience = stimulus.get("salience", 0.0)
        threat = stimulus.get("threat_score", 0.0)

        if threat > 0.8:
            return "reflex" # Immediate bypass
        if salience > 0.7:
            return "urgent" # Rapid processing
        return "deliberative" # Standard cognitive path
