import logging
from typing import List

logger = logging.getLogger(__name__)

class ToleranceEnsembles:
    """
    DD-IV, DJ-III: Peripheral Tolerance.
    Regulatory agent ensembles (Treg-analogues) maintain self-tolerance.
    Minority veto power calibrated to ratio > 1.8:1.
    """
    def __init__(self):
        self.veto_ratio = 1.8

    def evaluate_tolerance(self, support_votes: int, veto_votes: int) -> bool:
        """
        Determines if a mutation/action should be tolerated.
        Vetoes have disproportionate weight.
        """
        if support_votes == 0: return False

        actual_ratio = veto_votes / support_votes
        # If vetoes exceed the threshold ratio relative to support
        if actual_ratio > (1.0 / self.veto_ratio):
             logger.warning(f"TOLERANCE: Action VETOED by Treg-analogue. Ratio {actual_ratio:.2f} > 0.55")
             return False

        logger.info("TOLERANCE: Action accepted by consensus.")
        return True
