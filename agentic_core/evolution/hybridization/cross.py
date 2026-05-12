import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Crossover:
    """
    ARTICLE 163: Sexual Reproduction (Crossover).
    Combines two parent chromosomes into a hybrid offspring.
    """
    def __init__(self, rate: float = 0.5):
        self.rate: float = rate

    def apply(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        One-point crossover between two parent chromosomes.

        Args:
            parent1 (Chromosome): The first parent.
            parent2 (Chromosome): The second parent.

        Returns:
            Chromosome: A new hybrid offspring chromosome.
        """
        offspring_id = f"hybrid_{random.randint(1000, 9999)}"
        offspring = Chromosome(offspring_id)

        if random.random() < self.rate:
            min_len = min(len(parent1.sequence), len(parent2.sequence))
            if min_len > 0:
                cut = random.randint(0, min_len)
                offspring.sequence = parent1.sequence[:cut] + parent2.sequence[cut:]
                # Merge gene maps from parents for all genes in offspring sequence
                for gene_id in offspring.sequence:
                    if gene_id in parent1.gene_map:
                        offspring.gene_map[gene_id] = parent1.gene_map[gene_id]
                    elif gene_id in parent2.gene_map:
                        offspring.gene_map[gene_id] = parent2.gene_map[gene_id]
                logger.info(f"HYBRIDIZATION: {offspring_id} created via crossover at point {cut}.")
            else:
                offspring.sequence = list(parent1.sequence)
                offspring.gene_map = dict(parent1.gene_map)
        else:
            offspring.sequence = list(parent1.sequence)
            offspring.gene_map = dict(parent1.gene_map)

        return offspring
