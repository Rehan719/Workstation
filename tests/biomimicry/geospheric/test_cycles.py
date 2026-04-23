import pytest
from agentic_core.biomimicry.cycles.geospheric_orchestrator import GeosphericHomeostaticOrchestrator
from agentic_core.biomimicry.cycles.psi_functional import EcosystemHealthObjective

def test_geospheric_homeostasis():
    orchestrator = GeosphericHomeostaticOrchestrator(target_psi=0.85)

    # Normal load
    res = orchestrator.step(system_load=0.5, error_rate=0.01, data_size=1000.0)
    assert res["psi_score"] > 0.85
    assert res["status"] == "HOMEOSTATIC"
    assert res["cycle_states"]["oxygen"] == "active"

def test_psi_hard_constraints():
    psi = EcosystemHealthObjective()
    metrics = {"water": 0.9, "carbon": 0.9}

    # Should pass with 1.0 compliance
    score = psi.evaluate(metrics, closed_loop_compliance=1.0, biomimetic_fidelity=0.95)
    assert score > 0

    # Should fail if closed-loop transformation is violated (waste detected)
    fail_score = psi.evaluate(metrics, closed_loop_compliance=0.0)
    assert fail_score == float('-inf')

def test_sulfur_acid_rain_trigger():
    orchestrator = GeosphericHomeostaticOrchestrator()

    # High error rate should trigger throttling (Acid Rain)
    res = orchestrator.step(system_load=0.9, error_rate=0.4, data_size=500.0)
    assert res["cycle_states"]["sulfur"] == "THROTTLE"
    assert res["cycle_states"]["oxygen"] == "turbo"
