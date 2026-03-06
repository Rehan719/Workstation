import asyncio
import logging
from agentic_core.immune.immune_system import ImmuneSystemV2 as ImmuneSystem
from agentic_core.nervous_system.nervous_system import NervousSystem
from agentic_core.cardiovascular.cardiovascular_system import CardiovascularSystem
from agentic_core.digestion.digestive_system import DigestiveSystem
from agentic_core.aging.longevity_engine import LongevityEngine
from agentic_core.homeostasis.homeostatic_regulator import HomeostaticRegulator
from agentic_core.ethics.constitutional_enforcer import ConstitutionalEnforcer

async def test_immune_memory():
    immune = ImmuneSystem()
    sample = {"perplexity": 60.0}
    score1 = immune.evaluate_threat(sample)
    assert score1 > 0.8
    # Second time should be detected by memory
    score2 = immune.evaluate_threat(sample)
    assert score2 == 1.0

def test_homeostasis_allostatic_load():
    reg = HomeostaticRegulator()
    reg.update_metrics({"error_rate": 0.1, "latency_avg": 200.0})
    assert reg.allostatic_load >= 4.0

def test_longevity_apoptosis():
    longevity = LongevityEngine()
    for _ in range(101):
        longevity.track_execution("test_comp")
    assert longevity.health_counters["test_comp"] <= 0

async def test_constitutional_violation():
    enforcer = ConstitutionalEnforcer()
    # Tier 1 parameter update should fail
    res = enforcer.verify_action("parameter_update", {"tier": 1, "param": "key_size"})
    assert res is False

async def run_all():
    await test_immune_memory()
    test_homeostasis_allostatic_load()
    test_longevity_apoptosis()
    await test_constitutional_violation()

if __name__ == "__main__":
    asyncio.run(run_all())
    print("Biological subsystem tests PASSED.")
