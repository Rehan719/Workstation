from typing import Dict, Any

class IntrospectiveLearning:
    """
    CN-IV: Introspective Learning.
    Incorporates self-model accuracy into the fitness function.
    """
    def calculate_calibration_score(self, prediction: float, outcome: float) -> float:
        """How accurate was the organism's self-assessment?"""
        error = abs(prediction - outcome)
        return 1.0 - error
