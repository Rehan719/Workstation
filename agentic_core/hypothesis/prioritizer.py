from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class HypothesisPrioritizer:
    """
    v48.0 Article BA: Intelligent Hypothesis Prioritization.
    Ranks research statements based on Novelty (N), Feasibility (F), and Impact/Relevance (R).
    Quality Function: Quality = w_N * N + w_F * F + w_R * R
    """

    def __init__(self, weights: Dict[str, float] = None):
        # Default weights for Novelty, Feasibility, and Relevance
        self.weights = weights or {
            "novelty": 0.4,
            "feasibility": 0.3,
            "relevance": 0.3
        }

    def calculate_quality(self, hypothesis: Dict[str, Any]) -> float:
        """
        Calculates the quality score of a hypothesis.
        """
        n = hypothesis.get("novelty_score", 0.5)
        f = hypothesis.get("feasibility_score", 0.5)
        r = hypothesis.get("relevance_score", 0.5)

        quality = (self.weights["novelty"] * n +
                   self.weights["feasibility"] * f +
                   self.weights["relevance"] * r)
        return round(quality, 4)

    def prioritize(self, hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks a list of hypotheses by their calculated quality score.
        """
        for h in hypotheses:
            h["quality_score"] = self.calculate_quality(h)

        # Sort hypotheses by quality score in descending order
        ranked = sorted(hypotheses, key=lambda x: x["quality_score"], reverse=True)
        return ranked
