import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PurposeAlignmentEvaluator:
    """
    ARTICLE 338: Purpose Alignment Evaluation.
    Scores proposals and decisions against the dual-purpose framework.
    """
    def __init__(self):
        self.spiritual_keywords = ["dawah", "charity", "scholarship", "ethics", "islamic", "quran", "sunnah"]
        self.commercial_keywords = ["profit", "efficiency", "revenue", "productivity", "growth", "utility"]

    def evaluate_intent(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates a Purpose Alignment Score (PAS)."""
        description = str(intent_data.get("description", "")).lower()

        spiritual_hits = sum(1 for kw in self.spiritual_keywords if kw in description)
        commercial_hits = sum(1 for kw in self.commercial_keywords if kw in description)

        score = 0.90

        if spiritual_hits > 0:
            score += 0.05
        if commercial_hits > 0:
            score += 0.03

        if commercial_hits > 3 and spiritual_hits == 0:
            logger.warning("Purpose Evaluator: Commercial intent lacks ethical/spiritual context.")
            score -= 0.10

        score = min(max(score, 0.0), 1.0)

        return {
            "purpose_alignment_score": round(score, 2),
            "spiritual_index": spiritual_hits,
            "commercial_index": commercial_hits,
            "recommendation": "PROCEED" if score >= 0.85 else "ENHANCE_ETHICAL_CONTEXT"
        }
