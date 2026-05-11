import random
from typing import List, Dict, Any
from .chromosome import Chromosome

class EvolutionEngine:
    """
    ARTICLE 166: The Core Evolution Engine.
    Manages selection, mutation, and crossover for a population of chromosomes.
    """
    def __init__(self, mutation_rate: float = 0.01, crossover_rate: float = 0.7):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def evolve_population(self, population: List[Chromosome], fitness_scores: List[float]) -> List[Chromosome]:
        """
        Executes one generation of evolution.
        """
        if not population:
            return []

        new_population = []
        while len(new_population) < len(population):
            # Selection
            parent1 = self._select_parent(population, fitness_scores)
            parent2 = self._select_parent(population, fitness_scores)

            # Crossover
            if random.random() < self.crossover_rate:
                child = parent1.crossover(parent2)
            else:
                child = Chromosome.from_dict(parent1.to_dict())

            # Mutation
            child.mutate(self.mutation_rate)
            new_population.append(child)

        return new_population

    def _select_parent(self, population: List[Chromosome], scores: List[float]) -> Chromosome:
        """Tournament selection."""
        idx = random.choices(range(len(population)), weights=scores, k=1)[0]
        return population[idx]
