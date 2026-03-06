import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Duplication:
    """
    ARTICLE 163: Gene and Segment Duplication.
    Critical for gene family expansion and adaptive potential.
    """
    def __init__(self, rate: float = 1e-5):
        self.rate: float = rate

    def apply(self, chromosome: Chromosome) -> None:
        if not chromosome.sequence:
            return

        if random.random() < self.rate:
            start = random.randint(0, len(chromosome.sequence) - 1)
            length = random.randint(1, min(5, len(chromosome.sequence) - start))

            segment = chromosome.sequence[start:start+length]
            # Insert duplicate after the original
            chromosome.sequence = (
                chromosome.sequence[:start+length] +
                segment +
                chromosome.sequence[start+length:]
            )
            logger.info(f"REARRANGEMENT: Duplicated segment of length {len(segment)} in {chromosome.chromosome_id}.")
