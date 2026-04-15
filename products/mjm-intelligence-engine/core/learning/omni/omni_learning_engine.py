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

        # 1. Pattern Extraction via LLM Synthesis
        extracted_patterns = await self._extract_patterns_async(signal)

        # 2. Store domain-specific patterns
        domain_id = signal.payload.get("domain_id", "universal")
        if domain_id not in self.domain_patterns:
            self.domain_patterns[domain_id] = []
        self.domain_patterns[domain_id].extend(extracted_patterns)

        # 3. Store universal patterns
        for p in extracted_patterns:
            if p.get("generalization_score", 0) > 0.8:
                self.universal_patterns.append(p)

        # 4. Federated Share (Actual persistence to shared ecosystem log)
        federated_sent = False
        if self.config.get("federation_enabled", False):
            federated_sent = self._broadcast_to_ecosystem(signal, extracted_patterns)

        return OmniLearningReceipt(
            signal_id=signal.id,
            ingested=True,
            patterns_extracted=len(extracted_patterns),
            federated_share_sent=federated_sent
        )

    async def _extract_patterns_async(self, signal: OmniSignal) -> List[Dict[str, Any]]:
        """Extracts patterns using LLM analysis of the signal payload."""
        prompt = f"""
        Analyze the following signal for reusable intelligence patterns:
        Source: {signal.source}
        Type: {signal.type}
        Payload: {json.dumps(signal.payload)}

        Output: Return a JSON list of pattern objects: {{ "id": string, "type": string, "description": string, "generalization_score": float }}
        """
        try:
            from ollama import AsyncClient
            client = AsyncClient()
            response = await client.generate(model="llama3.1:8b", prompt=prompt)
            text = response['response']
            start = text.find('[')
            end = text.rfind(']') + 1
            return json.loads(text[start:end])
        except Exception as e:
            logger.warning(f"Omni pattern extraction fallback: {e}")
            return self._heuristic_pattern_extraction(signal)

    def _heuristic_pattern_extraction(self, signal: OmniSignal) -> List[Dict[str, Any]]:
        patterns = []
        if signal.type == "execution_outcome" and signal.payload.get("success"):
            patterns.append({
                "id": f"P-{signal.id}",
                "type": "success_heuristic",
                "description": f"Successful execution in {signal.payload.get('domain_id')}",
                "generalization_score": 0.7
            })
        return patterns

    def _broadcast_to_ecosystem(self, signal: OmniSignal, patterns: List[Dict[str, Any]]) -> bool:
        """Persists learned patterns to a shared ecosystem discovery log."""
        try:
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "signal_id": signal.id,
                "patterns": patterns
            }
            with open("ecosystem_discovery.log", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            return True
        except Exception:
            return False

    async def replay_experiences(self, domain_id: str) -> List[Dict[str, Any]]:
        """Returns relevant learned patterns for a domain."""
        return self.domain_patterns.get(domain_id, []) + self.universal_patterns
