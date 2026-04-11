import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class LearningSignal(BaseModel):
    domain_id: str
    phase: str
    feedback_type: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MJMLearningEngine:
    """
    Biomimetic Learning System: Enables MJM Engine to adapt, evolve, and improve.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.history: List[LearningSignal] = []
        self.learned_patterns: Dict[str, List[Dict[str, Any]]] = {}

    def ingest_feedback(self, signal: LearningSignal) -> Dict[str, Any]:
        """Collects outcomes from MJM cycles."""
        logger.info(f"Ingesting learning signal for {signal.domain_id} in phase {signal.phase}")
        self.history.append(signal)

        # Simple v1.0 pattern extraction:
        # If a source is marked as unreliable, update its weight
        if signal.feedback_type == "source_reliability":
            return self._update_source_reliability(signal)

        return {"status": "ingested", "timestamp": datetime.utcnow()}

    def _update_source_reliability(self, signal: LearningSignal) -> Dict[str, Any]:
        source_uri = signal.payload.get("uri")
        score = signal.payload.get("score")
        return {"action": "update_weight", "source": source_uri, "new_score": score}

    def propagate_knowledge(self, domain_id: str) -> List[Dict[str, Any]]:
        """Identifies successful strategies that can be shared with other domains."""
        # v1.0 placeholder for cross-domain pattern sharing
        return []

    def evaluate_performance(self, domain_id: str) -> Dict[str, Any]:
        """Assess MJM performance against empirical benchmarks."""
        relevant_signals = [s for s in self.history if s.domain_id == domain_id]
        if not relevant_signals:
            return {"status": "insufficient_data"}

        # Example metric: average confidence of successful proposals
        return {"domain": domain_id, "performance_index": 0.85}

    def trigger_evolution(self, domain_id: str) -> Optional[Dict[str, Any]]:
        """Recommends configuration updates when performance thresholds are met."""
        perf = self.evaluate_performance(domain_id)
        threshold = self.config.get("evolution_triggers", {}).get("performance_threshold", 0.9) if self.config else 0.9

        if perf.get("performance_index", 0) > threshold:
            return {
                "type": "EVOLUTION_PROPOSAL",
                "domain_id": domain_id,
                "recommendation": "Increase weight of whistleblower sources",
                "reason": "High correlation with successful risk identification"
            }
        return None
