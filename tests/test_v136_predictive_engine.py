import pytest
from agentic_core.synthesis.predictive_engine_v136 import AdvancedPredictiveAssimilationEngineV136

def test_predictive_engine_v136_initialization():
    engine = AdvancedPredictiveAssimilationEngineV136()
    assert "Homeostatic_PID" in engine.active_capabilities
    assert engine.platforms == ["microsoft", "google", "amazon", "meta", "apple", "nvidia", "tesla"]

def test_genetic_recombination():
    engine = AdvancedPredictiveAssimilationEngineV136()
    synergy = {"M7_AI_Convergence": 0.9, "Sovereignty_Demand": 0.8}
    result = engine.evolve_capabilities(synergy)

    assert "new_capabilities" in result
    assert len(engine.active_capabilities) > 0
    # verify it's a list of strings
    assert isinstance(engine.active_capabilities[0], str)

def test_v136_cycle():
    engine = AdvancedPredictiveAssimilationEngineV136()
    cycle_result = engine.run_v136_cycle()

    assert "synergy_metrics" in cycle_result
    assert "evolution_results" in cycle_result
    assert "proposals" in cycle_result
    assert len(cycle_result["proposals"]) == 7 # One per M7 platform
