import random
import hashlib
import json
from typing import List, Dict, Any

class Genotype:
    """Represents a set of system parameters or prompts."""
    def __init__(self, parameters: Dict[str, Any], fitness: float = 0.0):
        self.parameters = parameters
        self.fitness = fitness
        self.id = hashlib.md5(json.dumps(parameters, sort_keys=True).encode()).hexdigest()

class GeneticEvolutionEngine:
    """
    v52.0 Autonomous Improvement: Genetic Algorithm.
    Evolves system parameters (learning_rate, thresholds, prompt_suffixes).
    """
    def __init__(self, population_size: int = 10):
        self.population_size = population_size
        self.population: List[Genotype] = []

    def initialize_population(self, seed_params: Dict[str, Any]):
        self.population = [Genotype(seed_params)]
        for _ in range(self.population_size - 1):
            mutated = self._mutate(seed_params)
            self.population.append(Genotype(mutated))

    def evolve(self):
        """Runs one generation of evolution."""
        # Sort by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Elitism
        new_population = self.population[:2]

        # Reproduction
        while len(new_population) < self.population_size:
            if random.random() < 0.7:
                # Crossover
                p1, p2 = random.sample(self.population[:5], 2)
                child_params = self._crossover(p1.parameters, p2.parameters)
                new_population.append(Genotype(child_params))
            else:
                # Mutation
                parent = random.choice(self.population[:5])
                mutated_params = self._mutate(parent.parameters)
                new_population.append(Genotype(mutated_params))

        self.population = new_population

    def _mutate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        mutated = params.copy()
        key = random.choice(list(mutated.keys()))
        if isinstance(mutated[key], (float, int)):
            mutated[key] *= random.uniform(0.8, 1.2)
        return mutated

    def _crossover(self, p1: Dict[str, Any], p2: Dict[str, Any]) -> Dict[str, Any]:
        child = {}
        for key in p1:
            child[key] = random.choice([p1[key], p2[key]])
        return child
