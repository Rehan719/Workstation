import random
import hashlib
import json
import logging
from typing import List, Dict, Any

class Genotype:
    """Represents a set of system parameters or prompts."""
    def __init__(self, parameters: Dict[str, Any], fitness: float = 0.0):
        self.parameters = parameters
        self.fitness = fitness
        self.id = hashlib.md5(json.dumps(parameters, sort_keys=True).encode()).hexdigest()

class AdaptiveStrategySelector:
    """
    v53 Upgrade: Adaptive Mutation Strategy Selection.
    Uses reinforcement learning (simplified score-based) to choose operators.
    """
    def __init__(self):
        self.strategies = ["exploration", "exploitation", "chaotic", "hybrid"]
        self.scores = {s: 1.0 for s in self.strategies}
        self.alpha = 0.1 # Learning rate for strategy scores

    def select_strategy(self) -> str:
        # Epsilon-greedy selection with probability of random exploration
        if random.random() < 0.15:
            return random.choice(self.strategies)
        return max(self.scores, key=self.scores.get)

    def update_scores(self, strategy: str, reward: float):
        # Update strategy efficacy score based on fitness gain
        self.scores[strategy] = (1 - self.alpha) * self.scores[strategy] + self.alpha * reward

class GeneticEvolutionEngine:
    """
    v53 Upgrade: Adaptive Genetic Evolution Engine.
    Evolves system parameters with adaptive operator selection and multi-objective hooks.
    """
    def __init__(self, population_size: int = 10):
        self.population_size = population_size
        self.population: List[Genotype] = []
        self.strategy_selector = AdaptiveStrategySelector()
        self.generation = 0

    def initialize_population(self, seed_params: Dict[str, Any]):
        self.population = [Genotype(seed_params)]
        for _ in range(self.population_size - 1):
            mutated = self._mutate(seed_params, "exploration")
            self.population.append(Genotype(mutated))

    def evolve(self):
        """Runs one generation of evolution with adaptive strategies and chaotic mapping."""
        self.generation += 1
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # v53: Adaptive Strategy Selection
        strategy = self.strategy_selector.select_strategy()
        logging.info(f"Gen {self.generation}: Evolving with strategy: {strategy}")

        # Elitism (preserve best 20%)
        elite_count = max(2, self.population_size // 5)
        new_population = self.population[:elite_count]

        while len(new_population) < self.population_size:
            parent = random.choice(self.population[:max(3, self.population_size // 3)])
            mutated_params = self._mutate(parent.parameters, strategy)
            new_genotype = Genotype(mutated_params)
            new_population.append(new_genotype)

        self.population = new_population

    def _mutate(self, params: Dict[str, Any], strategy: str) -> Dict[str, Any]:
        mutated = params.copy()
        if not mutated: return mutated

        key = random.choice(list(mutated.keys()))

        if strategy == "exploration":
            # High variance mutation (Cauchy-like)
            factor = random.uniform(0.1, 5.0)
        elif strategy == "exploitation":
            # Low variance mutation (Gaussian-like)
            factor = random.gauss(1.0, 0.05)
        elif strategy == "chaotic":
            # v53: Chaotic Mapping (Logistic Map) to avoid local optima
            # x_{n+1} = r * x_n * (1 - x_n)
            r = 3.99 # Chaotic regime
            x = random.random()
            factor = (r * x * (1 - x)) * 2.0
        elif strategy == "hybrid":
            # Mix of exploration and exploitation
            factor = random.choice([0.5, 1.5, 0.98, 1.02])
        else:
            factor = 1.1

        if isinstance(mutated[key], (float, int)):
            mutated[key] *= abs(factor)

        return mutated

    def report_performance(self, strategy: str, reward: float):
        """Reinforcement hook for the strategy selector."""
        self.strategy_selector.update_scores(strategy, reward)
