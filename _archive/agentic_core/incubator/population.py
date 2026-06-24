import logging
import random
from typing import List, Any, Dict
from .petri_dish import PetriDish

logger = logging.getLogger(__name__)

class Population:
    """
    ARTICLE 162: The Population Engine.
    Implements Wright-Fisher dynamics for digital organisms.
    """
    def __init__(self, size: int = 100):
        self.size = size
        self.organisms: List[Any] = []
        self.generation = 0

    def replace_generation(self, fitness_scores: Dict[str, float]):
        """
        WF Model: Entire population replaced based on weighted fitness.
        """
        if not fitness_scores or len(fitness_scores) == 0:
            logger.warning("POPULATION: No fitness scores provided. Skipping generation replacement.")
            return

        next_gen = []
        organism_ids = list(fitness_scores.keys())
        weights = list(fitness_scores.values())

        # Add small constant to weights to ensure selection if all are zero
        total_weight = sum(weights)
        if total_weight == 0:
            weights = [1.0] * len(weights)

        for _ in range(self.size):
            # Weighted random choice with replacement
            parent_id = random.choices(organism_ids, weights=weights, k=1)[0]
            next_gen.append(self._reproduce(parent_id))

        self.organisms = next_gen
        self.generation += 1
        logger.info(f"Generation {self.generation} established via Wright-Fisher dynamics.")

    def _reproduce(self, parent_id: str) -> Any:
        """
        ARTICLE 162: Reproduction logic.
        Clones the parent and initiates the mutation pipeline.
        """
        # In a full implementation, this would return a new digital organism
        # with a mutated copy of the parent's genome.
        # For the orchestrator, we track the ID and trigger mutations via the operators.
        logger.debug(f"POPULATION: Organism {parent_id} reproduced.")
        return f"{parent_id}_clone_{random.randint(0, 999)}"
