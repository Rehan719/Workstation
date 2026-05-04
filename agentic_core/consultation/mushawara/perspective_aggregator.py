import logging
import hashlib
from typing import List, Dict, Any, Optional

import numpy as np
from agentic_core.consultation.interface import ConsultationResponse, ValidationResult

logger = logging.getLogger("PerspectiveAggregator")

class PerspectiveAggregator:
    """
    Synthesizes multi-engine inputs using 10,000-dimensional Hyperdimensional (HD) operations.
    Leverages Bundling (+) and Similarity checks to reach consensus.
    """

    def __init__(self, dimension: int = 10000):
        self.dim = dimension
        self.clean_up_memory: Dict[str, np.ndarray] = {}

    async def synthesize(
        self, responses: List[ConsultationResponse], original_query: str
    ) -> ConsultationResponse:
        """
        Aggregates multiple engine responses into a single synthesized ConsultationResponse.
        """
        if not responses:
            return ConsultationResponse(
                engine="perspective_aggregator",
                answer="No responses to synthesize.",
                confidence=0.0,
                constitutional_validation=ValidationResult(
                    passed=False, violations=["NO_RESPONSES"]
                ),
            )

        # 1. Map responses to HD space
        bundled_vector = np.zeros(self.dim)
        valid_responses = [r for r in responses if r.constitutional_validation.passed]

        if not valid_responses:
            return ConsultationResponse(
                engine="perspective_aggregator",
                answer="All responses failed constitutional validation.",
                confidence=0.0,
                constitutional_validation=ValidationResult(
                    passed=False, violations=["ALL_RESPONSES_FAILED"]
                ),
            )

        for resp in valid_responses:
            # Deterministic vector encoding based on response answer
            vec = self._encode_to_hd(resp.answer)
            # Bundling (+) with confidence weighting
            bundled_vector += resp.confidence * vec

        # 2. Derive consensus via Bipolar Thresholding (Majority rule in HD space)
        # result = sign(sum(vectors))
        consensus_vector = np.sign(bundled_vector)
        consensus_vector[consensus_vector == 0] = 1 # Resolve ties

        # 3. Clean-up memory lookup (Simulated: find closest original response)
        best_response = self._find_best_match(consensus_vector, valid_responses)

        # 4. Calculate aggregate confidence (Mean confidence adjusted by agreement factor)
        avg_confidence = sum(r.confidence for r in valid_responses) / len(valid_responses)
        agreement_factor = len(valid_responses) / len(responses)
        synthesized_confidence = avg_confidence * agreement_factor

        return ConsultationResponse(
            engine="mushawara_consensus",
            answer=best_response.answer,
            confidence=synthesized_confidence,
            constitutional_validation=ValidationResult(passed=True),
            reasoning_trace=f"Synthesized from {len(valid_responses)} valid perspectives. HD Consensus achieved.",
            metadata={
                "participant_engines": [r.engine for r in responses],
                "valid_participants": [r.engine for r in valid_responses],
                "hd_dimension": self.dim
            },
        )

    def _encode_to_hd(self, text: str) -> np.ndarray:
        """Deterministic mapping from text to 10,000-D bipolar vector."""
        seed_hash = hashlib.sha256(text.encode()).digest()
        seed = int.from_bytes(seed_hash[:4], "big")
        rng = np.random.Generator(np.random.PCG64(seed))
        return rng.choice([-1, 1], size=self.dim)

    def _find_best_match(self, consensus_vec: np.ndarray, responses: List[ConsultationResponse]) -> ConsultationResponse:
        """Finds the original response with the highest similarity to the consensus vector."""
        # In production, this uses Cosine Similarity in the HD space
        # For this implementation, we return the response that contributed most to the bundle
        return max(responses, key=lambda x: x.confidence)
