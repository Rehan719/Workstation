import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReputationLedger:
    """v127.0: Molecular-based reputation tracking for scholars."""
    def __init__(self):
        self.reputation: Dict[str, float] = {}

    def update_reputation(self, scholar_id: str, gain: float):
        current = self.reputation.get(scholar_id, 0.5)
        self.reputation[scholar_id] = min(1.0, current + gain)
        logger.info(f"Reputation: Scholar {scholar_id} now at {self.reputation[scholar_id]}")

    def get_rank(self, scholar_id: str) -> str:
        score = self.reputation.get(scholar_id, 0.5)
        if score > 0.9: return "Grand Scholar"
        if score > 0.7: return "Senior Fellow"
        return "Associate Scholar"
