from typing import Dict, Any

class DomainNoveltyAssessor:
    """CQ-IV: Domain Novelty Assessment."""

    def assess(self, domain_data: Dict[str, Any]) -> float:
        # Scale: -1 to +1
        # Target: >=68% lexical divergence mapped to +1
        divergence = domain_data.get("lexical_divergence", 0.3)

        if divergence >= 0.68:
            return 1.0
        elif divergence < 0.1:
            return -1.0

        return (divergence - 0.39) / 0.29
