from typing import List, Dict

class TruthConsensusEngine:
    """Emergent truth consensus with confidence calibration (Phase 7)."""

    async def reach_consensus(self, claims: List[Dict], threshold: float = 0.85) -> List[Dict]:
        unique_claims = {}
        for claim in claims:
            text = claim["claim"]
            unique_claims.setdefault(text, []).append(claim)

        results = []
        for text, variants in unique_claims.items():
            total_weight = sum(v.get("reputation", 1.0) for v in variants)
            weighted_conf = sum(v["confidence"] * v.get("reputation", 1.0) for v in variants) / total_weight

            results.append({
                "claim": text,
                "consensus_confidence": weighted_conf,
                "accepted": weighted_conf >= threshold,
                "evidence_count": len(variants)
            })

        return results
