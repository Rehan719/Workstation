import asyncio
from typing import Dict, Any, List, Optional
from .genetic_algorithm import GeneticEvolutionEngine, PromptGene
from .ab_tester import ABTester

class RecursiveEvolutionEngine:
    """
    L7 Evolutionary Engine (Radical Evolution Cycle).
    Ties together Genetic Mutation and A/B Testing to drive system self-improvement.
    """
    def __init__(self, agent_id: str, seed_prompt: str):
        self.agent_id = agent_id
        self.genetic_engine = GeneticEvolutionEngine(population_size=10)
        self.genetic_engine.initialize_population(seed_prompt)
        self.tester = ABTester()
        self.generation = 0

    async def run_evolution_cycle(self, test_tasks: List[Dict[str, Any]], agent_executor):
        """
        Runs one full cycle of evolution:
        1. Evaluate population -> 2. Select & Breed -> 3. Mutate
        """
        self.generation += 1
        print(f"Starting Generation {self.generation} for agent {self.agent_id}")

        # 1. Evaluate current population
        for gene in self.genetic_engine.population:
            avg_fitness = 0.0
            for task in test_tasks:
                # We use the current best as 'control' and current gene as 'variant'
                # but for simplicity we just evaluate each gene directly here
                result = await agent_executor.execute_with_prompt(task, gene.content)
                avg_fitness += self.tester._evaluate_quality(result)
            gene.fitness = avg_fitness / len(test_tasks)

        print(f"Gen {self.generation} Best Fitness: {max(g.fitness for g in self.genetic_engine.population):.2f}")

        # 2. Evolve population (Selection, Crossover, Mutation)
        self.genetic_engine.evolve()

    def get_best_prompt(self) -> str:
        return max(self.genetic_engine.population, key=lambda g: g.fitness).content
