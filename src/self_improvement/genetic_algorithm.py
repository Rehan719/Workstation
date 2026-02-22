import random
from typing import List, Dict, Any
import hashlib

class PromptGene:
    """Represents a single prompt variant (a gene) in the population."""
    def __init__(self, content: str, fitness: float = 0.0):
        self.content = content
        self.fitness = fitness
        self.gene_id = hashlib.md5(content.encode()).hexdigest()

class GeneticEvolutionEngine:
    """
    L7 Evolutionary Engine: Evolves prompts using mutation and crossover.
    Fitness is determined by L4 Meta-Cognitive analysis (A/B testing).
    """
    def __init__(self, population_size: int = 10, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population: List[PromptGene] = []

    def initialize_population(self, seed_prompt: str):
        """Create initial population by mutating the seed prompt."""
        self.population = [PromptGene(seed_prompt)]
        for _ in range(self.population_size - 1):
            mutated_content = self._mutate(seed_prompt)
            self.population.append(PromptGene(mutated_content))

    def evolve(self):
        """Run one generation of evolution."""
        # Sort by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Keep the top 20% (elitism)
        new_population = self.population[:max(1, int(self.population_size * 0.2))]

        # Fill the rest with offspring
        while len(new_population) < self.population_size:
            if random.random() < 0.7:
                # Crossover
                parent1 = random.choice(new_population)
                parent2 = random.choice(self.population)
                child_content = self._crossover(parent1.content, parent2.content)
            else:
                # Mutation
                parent = random.choice(self.population)
                child_content = self._mutate(parent.content)

            new_population.append(PromptGene(child_content))

        self.population = new_population

    def _mutate(self, content: str) -> str:
        """Simulate prompt mutation (e.g., changing adjectives or instructions)."""
        # Radical Simplification: in a real system, this would use an LLM
        mutations = [
            " Be more concise.",
            " Use formal academic tone.",
            " Focus on experimental evidence.",
            " Explain reasoning step-by-step.",
            " Include relevant citations."
        ]
        return content + random.choice(mutations)

    def _crossover(self, p1: str, p2: str) -> str:
        """Simulate prompt crossover (combining instructions)."""
        parts1 = p1.split(". ")
        parts2 = p2.split(". ")
        split_idx = random.randint(0, min(len(parts1), len(parts2)) - 1)
        return ". ".join(parts1[:split_idx] + parts2[split_idx:])
