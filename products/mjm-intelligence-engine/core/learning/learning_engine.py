import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import hashlib
import json

logger = logging.getLogger(__name__)

class LearningSignalType(str):
    EXECUTION_OUTCOME = "EXECUTION_OUTCOME"
    USER_RATING = "USER_RATING"
    EXPERT_CORRECTION = "EXPERT_CORRECTION"
    EMPIRICAL_BENCHMARK = "EMPIRICAL_BENCHMARK"

class LearningSignal(BaseModel):
    signal_type: str
    domain_id: str
    workflow_checkpoint: str
    outcome_data: Dict[str, Any]
    context: Dict[str, str]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    contributor_id: Optional[str] = None
    signature: Optional[str] = None

class MJMLearningEngine:
    """
    The cognitive cortex of the MJM organism.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.history: List[LearningSignal] = []
        self.pattern_repository: Dict[str, List[Dict[str, Any]]] = {}

    async def ingest_feedback(self, signal: LearningSignal) -> Dict[str, Any]:
        """Ingests feedback and extracts patterns."""
        logger.info(f"Learning: Ingesting {signal.signal_type} for {signal.domain_id}")
        self.history.append(signal)

        # Simple pattern extraction logic
        if signal.signal_type == LearningSignalType.EXECUTION_OUTCOME:
            success = signal.outcome_data.get("success", False)
            if success:
                self._reinforce_successful_patterns(signal)

        return {
            "status": "ACCEPTED",
            "receipt_id": hashlib.sha256(str(signal.timestamp).encode()).hexdigest()[:16]
        }

    def _reinforce_successful_patterns(self, signal: LearningSignal):
        # Implementation of pattern reinforcement
        domain = signal.domain_id
        if domain not in self.pattern_repository:
            self.pattern_repository[domain] = []
        self.pattern_repository[domain].append({"pattern": "procedural_fairness", "confidence": 0.95})

    async def propagate_patterns(self, source_domain: str, target_domains: List[str]) -> Dict[str, Any]:
        """Propagates successful patterns across compatible domains."""
        patterns = self.pattern_repository.get(source_domain, [])
        return {"source": source_domain, "targets": target_domains, "patterns_shared": len(patterns)}
