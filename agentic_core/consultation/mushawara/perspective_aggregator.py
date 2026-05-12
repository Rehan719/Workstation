import numpy as np
from typing import List, Dict, Any

class PerspectiveAggregator:
    def __init__(self, mjm_learner):
        self.mjm = mjm_learner

    async def synthesize(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate perspectives using HD bundling (10,000‑dimensional).
        V_consensus = sign(sum(w_i * V_i))
        """
        if not responses:
            return {"consensus_vector": None, "agreement_score": 0.0}

        vectors = []
        weights = []
        for r in responses:
            vectors.append(np.array(r["vector"]))
            weights.append(r["confidence"])

        # Weighted sum
        v_sum = np.zeros(10000)
        for v, w in zip(vectors, weights):
            v_sum += w * v

        # Sign bundling
        v_consensus = np.sign(v_sum).tolist()

        # Agreement score (magnitude relative to possible max)
        agreement = float(np.mean(np.abs(v_sum)) / len(responses))

        return {
            "consensus_vector": v_consensus,
            "agreement_score": agreement,
            "engine_count": len(responses)
        }
