import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MetacognitiveMonitor:
    """
    CN-II: Metacognitive Monitor.
    Evaluates the quality of reasoning processes and identifies biases.
    """
    def __init__(self):
        self.confidence_threshold = 0.6

    def evaluate_reasoning(self, trace: Dict[str, Any]) -> float:
        """Evaluates reasoning quality based on logic consistency and evidence support."""
        # Simulated metacognitive evaluation
        consistency_score = trace.get("consistency", 1.0)
        evidence_gap = trace.get("evidence_gap", 0.0)

        metaconfidence = consistency_score - (evidence_gap * 0.5)

        if metaconfidence < self.confidence_threshold:
            logger.warning(f"METACOGNITION: Low reasoning confidence ({metaconfidence:.2f}). Refinement triggered.")
            return metaconfidence

        logger.info(f"METACOGNITION: Reasoning validated. Confidence: {metaconfidence:.2f}")
        return metaconfidence
