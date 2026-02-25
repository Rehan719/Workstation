import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class HeritabilityTracker:
    """
    DC-II, DI-II: Heritability Tracking.
    Measures retention of acquired traits across simulated generations.
    Target: > 98%.
    """
    def __init__(self):
        self.trait_history: Dict[str, List[bool]] = {}

    def record_inheritance(self, trait_id: str, generation: int, successful: bool):
        if trait_id not in self.trait_history:
            self.trait_history[trait_id] = []
        self.trait_history[trait_id].append(successful)

        rate = self.calculate_current_rate(trait_id)
        logger.info(f"HERITABILITY: Trait {trait_id} Gen {generation} retention: {successful}. Current Rate: {rate*100:.1f}%")

    def calculate_current_rate(self, trait_id: str) -> float:
        history = self.trait_history.get(trait_id, [])
        if not history: return 1.0
        return sum(history) / len(history)

    def get_overall_heritability(self) -> float:
        if not self.trait_history: return 1.0
        rates = [self.calculate_current_rate(tid) for tid in self.trait_history]
        return sum(rates) / len(rates)
