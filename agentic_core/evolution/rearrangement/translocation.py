import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Translocation:
    """
    ARTICLE 163: Segment Translocation.
    Moves a segment of genes to a new position on the same or different chromosome.
    """
    def __init__(self, rate: float = 1e-5):
        self.rate: float = rate

    def apply(self, chromosome: Chromosome) -> None:
        if len(chromosome.sequence) < 5:
            return

        if random.random() < self.rate:
            start = random.randint(0, len(chromosome.sequence) - 1)
            length = random.randint(1, min(5, len(chromosome.sequence) - start))

            segment = chromosome.sequence[start:start+length]
            remaining = chromosome.sequence[:start] + chromosome.sequence[start+length:]

            new_pos = random.randint(0, len(remaining))
            chromosome.sequence = remaining[:new_pos] + segment + remaining[new_pos:]
            logger.info(f"REARRANGEMENT: Translocated {len(segment)} genes in {chromosome.chromosome_id} to position {new_pos}.")
