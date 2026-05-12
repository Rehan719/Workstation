import random
from typing import List, Dict, Any
from .chromosome import Chromosome

class GenomePopulation:
    """
    ARTICLE 162: Population Management.
    Tracks a set of chromosomes over generations.
    """
    def __init__(self, size: int, template_chromosome: Chromosome):
        self.size = size
        self.chromosomes = [self._clone(template_chromosome, i) for i in range(size)]
        self.generation = 0

    def _clone(self, template: Chromosome, index: int) -> Chromosome:
        data = template.to_dict()
        data["chromosome_id"] = f"{template.chromosome_id}_gen0_{index}"
        return Chromosome.from_dict(data)

    def get_average_fitness(self, scores: List[float]) -> float:
        return sum(scores) / len(scores) if scores else 0.0

    def update_population(self, new_chromosomes: List[Chromosome]):
        self.chromosomes = new_chromosomes
        self.generation += 1
