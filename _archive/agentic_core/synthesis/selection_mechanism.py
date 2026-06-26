import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SelectionMechanism:
    """
    CC-II: Periodic Selection.
    Retains the fittest mutation candidates and archives inferior variants.
    """
    def select_fittest(self, candidates: List[Dict[str, Any]], fitness_scores: List[float]) -> List[Dict[str, Any]]:
        # Pair candidates with scores
        scored_candidates = sorted(zip(candidates, fitness_scores), key=lambda x: x[1], reverse=True)

        # CC-II: Retain top 20%
        cutoff = max(1, len(scored_candidates) // 5)
        fittest = [c for c, s in scored_candidates[:cutoff]]

        logger.info(f"SELECTION COMPLETE: Retained {len(fittest)} fittest candidates.")
        return fittest
