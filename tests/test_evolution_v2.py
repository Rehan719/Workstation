from agentic_core.synthesis.evolutionary_engine import EvolutionaryEngineV2
from agentic_core.synthesis.evolutionary_memory import EvolutionaryMemory

def test_evolution_v2():
    memory = EvolutionaryMemory()
    engine = EvolutionaryEngineV2(memory)

    base_dna = {
        "prompts": ["Analyze the following scientific claim."],
        "guardrails": ["no_harm", "truthfulness", "fairness"]
    }

    candidates = engine.generate_mutation_candidates(base_dna)
    assert len(candidates) == 2
    assert candidates[0]["type"] == "prompt_delta"
    assert candidates[1]["type"] == "policy_relaxation"
    assert len(candidates[1]["data"]) < len(base_dna["guardrails"])

    print("Evolutionary Engine v2.0 verification PASSED.")

if __name__ == "__main__":
    test_evolution_v2()
