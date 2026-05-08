import logging
import math
from typing import Dict, Any, List, Optional
from .immune_defense import ImmuneDefense

logger = logging.getLogger(__name__)

class ImmuneSystem:
    """
    L-C-VI: Multi-layered Immune Defense.
    Enhanced with twin-prediction logic and real-time defense.
    """
    def __init__(self, validator: Optional[Any] = None, digital_twin: Optional[Any] = None, ueg: Optional[Any] = None):
        self.threat_database = []
        self.ic50_perplexity = 42.3
        self.defense = ImmuneDefense(validator, digital_twin, ueg)

    def evaluate_threat(self, sample: Dict[str, Any]) -> float:
        """
        Calibrated to perplexity > 42.3.
        Returns a threat score [0.0 - 1.0].
        """
        perplexity = sample.get("perplexity", 0)

        # Sigmoidal inhibition curve
        k = 0.5
        score = 1.0 / (1.0 + math.exp(-k * (perplexity - self.ic50_perplexity)))

        if score > 0.8:
            logger.warning(f"IMMUNE RESPONSE: High threat detected (score: {score:.2f})")

        return score

    async def scan_threats(self, orchestrator: Any) -> List[Dict[str, Any]]:
        """
        Public interface to scan for threats using the internal defense module.
        Integrates with the digital twin's predictive simulation.
        """
        risk = await self.defense.scan_threats()
        return [{"source": "system_scan", "data": {"risk_score": risk}}]

    def heal(self, component_id: str):
        logger.info(f"Regenerative healing initiated for {component_id}")
