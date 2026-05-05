from dataclasses import dataclass
from typing import List

@dataclass
class ReflectionResult:
    score: float
    critiques: List[str]

class SelfReflectionEngine:
    """
    Continuously evaluates the twin’s simulation trace against the constitution,
    biomimetic fidelity, and geospheric homeostasis. Emits criticism and
    generates improvement hypotheses.
    """
    def __init__(self, validator, biomimetic_validator):
        self.validator = validator
        self.biomimetic_validator = biomimetic_validator

    async def reflect(self, trace):
        score = 0.0
        critiques = []
        for event in trace:
            # Check constitutional compliance
            if hasattr(self.validator, "check") and not self.validator.check(event):
                critiques.append(f"Constitutional violation detected in event")
                score -= 10
            # Check biomimetic fidelity
            if hasattr(self.biomimetic_validator, "check") and not self.biomimetic_validator.check(event):
                critiques.append(f"Low fidelity detected in event")
                score -= 5
            # Check closed‑loop waste
            waste = getattr(event, "waste", 0)
            if waste > 0:
                critiques.append(f"Unreclaimed waste: {waste}")
                score -= 20
        # Score normalised to 0‑100
        return ReflectionResult(score=max(0, 100+score), critiques=critiques)
