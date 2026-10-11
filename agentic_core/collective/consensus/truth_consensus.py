from typing import List, Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class TruthConsensusEngine:
    """
    Emergent consensus on ground truth across the mesh.
    Uses weighted confidence aggregation and calibration.
    """
    def __init__(self, threshold: float = 0.85, ueg_logger: Optional[Any] = None):
        self.threshold = threshold
        self.ueg = ueg_logger or VSBUEGLogger()

    async def reach_truth_consensus(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        unique_claims = {}
        for c in claims:
            unique_claims.setdefault(c["claim"], []).append(c)
        for claim_text, observations in unique_claims.items():
            total_weight = sum(o["reputation"] for o in observations)
            weighted_conf = sum(o["confidence"] * o["reputation"] for o in observations) / total_weight if total_weight > 0 else 0
            #  W670 (ledger v16 R4.8) - with ONE observation the "weighted" confidence is that observer's own
            #  figure and nothing agreed with anything; it was returned as consensus and the claim marked
            #  accepted. A single observation is never accepted as a consensus, and the row says why.
            _n = len(observations)
            is_accepted = (weighted_conf >= self.threshold) if _n >= 2 else False
            results.append({
                "claim": claim_text,
                "consensus_confidence": float(weighted_conf),
                "accepted": is_accepted,
                "observations": _n,
                "basis": (f"{_n} observations, weighted by the reputation each row states" if _n >= 2 else
                          "ONE observation: the figure is that observer's own stated confidence, so no "
                          "consensus was reached and the claim is not accepted"),
            })
        await self.ueg.log_minimisation_event("truth_consensus_cycle", {"results": results})
        return results
