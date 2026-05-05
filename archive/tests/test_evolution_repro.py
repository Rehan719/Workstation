import asyncio
from agentic_core.pulse.pulse_clock import PulseClock
from agentic_core.survival.survival_engine import SurvivalEngineV2
from agentic_core.synthesis.fitness_function import FitnessFunction
from agentic_core.synthesis.selection_mechanism import SelectionMechanism
from agentic_core.reproduction.reproduction_engine import ReproductionEngine

async def test_evolution_reproduction():
    clock = PulseClock()
    survival = SurvivalEngineV2(clock)
    fitness = FitnessFunction()
    selection = SelectionMechanism()
    repro = ReproductionEngine(survival)

    # 1. Fitness Evaluation
    metrics = {"success_rate": 0.9, "latency_ms": 40, "ethical_scalar": 0.98}
    score = fitness.compute_fitness(metrics)
    assert score > 0.8

    # 2. Selection
    candidates = [{"id": "mut1"}, {"id": "mut2"}]
    scores = [0.9, 0.5]
    fittest = selection.select_fittest(candidates, scores)
    assert fittest[0]["id"] == "mut1"

    # 3. Reproduction
    # Binary Fission
    child = repro.spawn_instance("parent_01", "binary_fission", {"trait": "fast_reflex"})
    assert child is not None
    assert child["mode"] == "binary_fission"

    print("Evolution & Reproduction verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_evolution_reproduction())
