import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Deletion:
    """
    ARTICLE 163: Large Segment Deletion.
    Removes a continuous segment of genes from the chromosome.
    """
    def __init__(self, rate: float = 1e-5):
        self.rate: float = rate

    def apply(self, chromosome: Chromosome) -> None:
        """
        Randomly removes a sequence of genes from the chromosome.

        Args:
            chromosome (Chromosome): The chromosome to modify in-place.
        """
        if len(chromosome.sequence) < 2:
            return

        if random.random() < self.rate:
            start = random.randint(0, len(chromosome.sequence) - 1)
            length = random.randint(1, min(10, len(chromosome.sequence) - start))

            deleted_segment = chromosome.sequence[start:start+length]
            chromosome.sequence = chromosome.sequence[:start] + chromosome.sequence[start+length:]
            logger.info(f"REARRANGEMENT: Deleted {len(deleted_segment)} genes from {chromosome.chromosome_id} at {start}.")
