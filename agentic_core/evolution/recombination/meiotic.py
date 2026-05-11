import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class MeioticRecombination:
    """
    ARTICLE 163: Meiotic Recombination.
    Models crossover events for diploid genomes during reproduction.
    """
    def __init__(self, chiasma_rate: float = 0.5):
        self.chiasma_rate: float = chiasma_rate

    def apply(self, pair: List[Chromosome]) -> List[Chromosome]:
        """
        Simulates meiosis with crossover between homologous chromosome pairs.
        """
        if len(pair) < 2: return pair

        c1, c2 = pair[0], pair[1]
        if random.random() >= self.chiasma_rate:
            return [c1, c2]

        min_len = min(len(c1.sequence), len(c2.sequence))
        if min_len == 0: return [c1, c2]

        cut = random.randint(1, min_len - 1) if min_len > 1 else 0

        o1_seq = c1.sequence[:cut] + c2.sequence[cut:]
        o2_seq = c2.sequence[:cut] + c1.sequence[cut:]

        o1 = Chromosome(f"{c1.chromosome_id}_recomb")
        o2 = Chromosome(f"{c2.chromosome_id}_recomb")
        o1.sequence = o1_seq
        o2.sequence = o2_seq

        # Merge gene maps
        for c in [c1, c2]:
            o1.gene_map.update(c.gene_map)
            o2.gene_map.update(c.gene_map)

        logger.info(f"RECOMBINATION: Meiotic crossover executed at point {cut}.")
        return [o1, o2]
