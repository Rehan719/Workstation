from typing import Any, Dict, List
from src.ueg.ledger import UnifiedEvidenceGraph

class Adversary:
    """
    Layer 5: Adversarial Robustness.
    Actively attempts to refute verified claims.
    """
    def __init__(self, ueg: UnifiedEvidenceGraph):
        self.ueg = ueg

    async def probe_hypothesis(self, hypothesis_id: str) -> Dict[str, Any]:
        """Searches for counterexamples in the UEG."""
        # Find CONTRADICTS relations pointing to this hypothesis
        contradictions = []
        for u, v, data in self.ueg.get_edges():
            if v == hypothesis_id and data.get('relation') == 'CONTRADICTS':
                contradictions.append(u)

        if contradictions:
            return {
                "status": "REFUTED",
                "counterexamples": contradictions,
                "confidence_impact": -0.5
            }

        return {
            "status": "RESILIENT",
            "reason": "No counterexamples found in current knowledge graph."
        }
