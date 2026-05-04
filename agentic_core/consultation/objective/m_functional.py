from typing import Dict, Any, List

class MushawaraConsultationObjective:
    """
    Unified Consultation Objective (Μ‑Functional).
    Evaluates the quality and compliance of a Mushawara session.
    """
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "consensus_quality": 0.3,
            "perspective_diversity": 0.2,
            "deliberation_efficiency": 0.2,
            "constitutional_alignment": 0.3
        }

    def evaluate(self, consultation: Any, context: Any, legal_compliance: float = 1.0,
                 cognitive_perspectives: int = 0, biomimetic_fidelity: float = 1.0) -> float:
        """
        Evaluate consultation session. Returns infinity for hard constraint violations.
        """
        # Hard constraints
        if (getattr(context, 'layer', '') == "L12_Policy" or getattr(context, 'domain', '') == "legal") and legal_compliance < 1.0:
            return float('inf')
        if cognitive_perspectives < 3:
            return float('inf')  # Mandatory requirement for at least 3 cognitive engines
        if biomimetic_fidelity < 0.9:
            return float('inf')

        # Weighted scores
        cq = self._consensus_quality_score(consultation.participants, consultation.outcome)
        pd = self._perspective_diversity_score(consultation.participants)
        de = self._deliberation_efficiency_score(consultation.duration, consultation.resource_cost)
        ca = self._constitutional_alignment_score(consultation.outcome, context)

        scores = [cq, pd, de, ca]
        return sum(w * v for w, v in zip(self.weights.values(), scores))

    def _consensus_quality_score(self, participants, outcome):
        return 0.95 # Simulated

    def _perspective_diversity_score(self, participants):
        return 0.88 # Simulated

    def _deliberation_efficiency_score(self, duration, cost):
        return 0.92 # Simulated

    def _constitutional_alignment_score(self, outcome, context):
        return 1.0 # Simulated
