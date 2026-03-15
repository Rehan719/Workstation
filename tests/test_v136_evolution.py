import pytest
import random
from agentic_core.evolution.epigenetic_v3 import UnifiedEventGraph, EpigeneticEvolutionEngineV3

def test_ueg_integrity():
    ueg = UnifiedEventGraph()
    ueg.log_event("TEST_1", {"val": 1})
    ueg.log_event("TEST_2", {"val": 2})

    assert len(ueg.nodes) == 2
    assert ueg.verify_integrity() == True

    # Tamper
    ueg.nodes[0]["data"]["val"] = 99
    assert ueg.verify_integrity() == False

def test_generative_amendment():
    ueg = UnifiedEventGraph()
    engine = EpigeneticEvolutionEngineV3(ueg)

    proposal = engine.propose_generative_amendment({"realm": "Learner", "score": 0.95})
    assert "amendment_id" in proposal
    assert proposal["simulation_status"] == "PENDING_DIGITAL_REACTOR"

    # Verify it's in UEG
    assert ueg.nodes[0]["type"] == "AMENDMENT_PROPOSAL"

def test_digital_reactor_simulation():
    ueg = UnifiedEventGraph()
    engine = EpigeneticEvolutionEngineV3(ueg)
    proposal = {"amendment_id": "AMD_123"}

    result = engine.run_digital_reactor_simulation(proposal)
    # The random seed might affect this, but it should log a SIMULATION_RESULT
    assert ueg.nodes[0]["type"] == "SIMULATION_RESULT"

def test_v137_two_layer_inheritance():
    class MockUEG:
        def log_event(self, t, d): pass

    engine = EpigeneticEvolutionEngineV3(MockUEG())

    # Apply marking (Article 1084)
    signals = [{"associated_article": 1086, "success_score": 0.9, "cycles": 12}]
    engine.experience_cycle(signals)

    assert engine.methylation_patterns[1086] == 0.09
    assert 1086 in engine.histone_modifications

    # Generate inheritance pack
    old_profile = {"methylation": {1086: 0.5}, "histone": [1086]}
    pack = engine.inherit_to_next_version(old_profile)
    assert pack["version"] == "137.0.0"
    assert pack["epigenetic_inheritance"]["methylation"][1086] == 0.45 # Drift: 0.5 * 0.9
    assert 1086 in pack["epigenetic_inheritance"]["histone"]
