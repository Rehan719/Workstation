import logging
import asyncio
import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class OmniSignal(BaseModel):
    id: str = Field(default_factory=lambda: hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8])
    source: str
    type: str # execution_outcome, user_interaction, ecosystem_event, meta_decision
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OmniLearningReceipt(BaseModel):
    signal_id: str
    ingested: bool
    patterns_extracted: int
    federated_share_sent: bool

class OmniLearningEngine:
    """
    Learns from all available signals in the Workstation ecosystem.
    Integrates federated learning and universal pattern storage.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.signal_history: List[OmniSignal] = []
        self.universal_patterns: List[Dict[str, Any]] = []
        self.domain_patterns: Dict[str, List[Dict[str, Any]]] = {}

    async def omni_ingest(self, signal: OmniSignal) -> OmniLearningReceipt:
        """Ingests a signal and extracts multi-dimensional patterns."""
        logger.info(f"OmniLearning: Ingesting {signal.type} signal from {signal.source}")
        self.signal_history.append(signal)

        # 1. Pattern Extraction (Simulated for RC, logic to be expanded)
        extracted_patterns = self._extract_patterns(signal)

        # 2. Store domain-specific patterns
        domain_id = signal.payload.get("domain_id", "universal")
        if domain_id not in self.domain_patterns:
            self.domain_patterns[domain_id] = []
        self.domain_patterns[domain_id].extend(extracted_patterns)

        # 3. Store universal patterns
        for p in extracted_patterns:
            if p.get("generalization_score", 0) > 0.8:
                self.universal_patterns.append(p)

        # 4. Federated Share (Simulated)
        federated_sent = self.config.get("federation_enabled", False)

        return OmniLearningReceipt(
            signal_id=signal.id,
            ingested=True,
            patterns_extracted=len(extracted_patterns),
            federated_share_sent=federated_sent
        )

    def _extract_patterns(self, signal: OmniSignal) -> List[Dict[str, Any]]:
        """Extracts patterns based on signal type and content."""
        patterns = []
        if signal.type == "execution_outcome":
            success = signal.payload.get("success", False)
            if success:
                patterns.append({
                    "id": f"P-{signal.id}",
                    "type": "successful_strategy",
                    "strategy_id": signal.payload.get("strategy_id"),
                    "generalization_score": 0.85
                })
        elif signal.type == "meta_decision":
            patterns.append({
                "id": f"PM-{signal.id}",
                "type": "meta_logic_shift",
                "generalization_score": 0.92
            })
        return patterns

    async def replay_experiences(self, domain_id: str) -> List[Dict[str, Any]]:
        """Returns relevant learned patterns for a domain."""
        return self.domain_patterns.get(domain_id, []) + self.universal_patterns
