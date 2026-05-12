import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Inversion:
    """
    ARTICLE 163: Segment Inversion.
    Reverses the orientation of a segment of genes on the chromosome.
    """
    def __init__(self, rate: float = 1e-5):
        self.rate: float = rate

    def apply(self, chromosome: Chromosome) -> None:
        if len(chromosome.sequence) < 2:
            return

        if random.random() < self.rate:
            idx1 = random.randint(0, len(chromosome.sequence) - 1)
            idx2 = random.randint(0, len(chromosome.sequence) - 1)
            start, end = min(idx1, idx2), max(idx1, idx2)

            segment = chromosome.sequence[start:end+1]
            chromosome.sequence = (
                chromosome.sequence[:start] +
                list(reversed(segment)) +
                chromosome.sequence[end+1:]
            )
            logger.info(f"REARRANGEMENT: Inverted segment of length {len(segment)} in {chromosome.chromosome_id}.")
