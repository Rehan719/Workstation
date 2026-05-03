import logging
import random
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RealTimeAnomalyScorer:
    """
    ARTICLE 1045: Real-Time Anomaly Scoring (Immune Layer).
    Replaces scheduled scans with message-level risk evaluation.
    """
    def __init__(self):
        self.threat_signatures = ["SQL_INJECTION", "PROMPT_INJECTION", "UNAUTHORIZED_FEDERATION_REQUEST"]

    def score_message(self, message: Dict[str, Any]) -> float:
        """Evaluates a message and returns a risk score (0.0 to 1.0)."""
        content = str(message.get("payload", ""))

        # Simple signature matching logic
        risk_score = 0.0
        for sig in self.threat_signatures:
            if sig in content:
                risk_score += 0.5

        # Baseline noise
        risk_score += random.uniform(0.01, 0.05)

        score = min(risk_score, 1.0)
        logger.info(f"ImmuneLayer: Message Anomaly Score: {score}")
        return score

    def trigger_containment(self, score: float, context: str):
        """Triggers containment if score exceeds threshold."""
        if score > 0.7:
            logger.error(f"ImmuneLayer: CRITICAL THREAT DETECTED ({score}) in {context}. Initiating 888_HOLD.")
            return True
        return False
