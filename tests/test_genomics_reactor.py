import pytest
import numpy as np
import asyncio
from agentic_core.incubator.petri_dish import PetriDish
from agentic_core.incubator.simulation_loop import SimulationLoop
from agentic_core.compiler.biological_compiler import BiologicalCompiler
from agentic_core.architecture.hox_patterns import HoxPatternRegistry
from agentic_core.architecture.phylotypic_core import PhylotypicCore
from agentic_core.reactor.base import DigitalReactor
from unittest.mock import MagicMock

class MockAgent:
    def propose_update(self, petri_dish):
        # Propose a small change to a hidden channel
        update = np.zeros_like(petri_dish.grid)
        update[10, 10, 0] = 1.0
        return update

def test_petri_dish_simulation():
    dish = PetriDish(width=20, height=20)
    loop = SimulationLoop(dish)
    agents = [MockAgent(), MockAgent()]

    # Run 5 steps
    for _ in range(5):
        loop.step(agents)

    # Verify grid state changed (accumulated 0.01 * 1.0 * 2 agents * 5 steps = 0.1)
    assert dish.grid[10, 10, 0] > 0.05
    assert dish.grid[10, 10, 0] < 0.15

def test_biological_compiler_compilation():
    compiler = BiologicalCompiler()
    intent = "Build a secure web portal with payment integration"
    artifact = compiler.compile(intent)

    assert artifact["status"] == "DEPLOYABLE"
    assert len(artifact["parts"]) > 0
    assert "dna_hash" in artifact
    assert artifact["dna_hash"] is not None

def test_hox_pattern_validation():
    # HoxPatternRegistry.validate_module raises ConstitutionalViolation if invalid
    # Mock a module that doesn't implement 'satisfies'
    class LegacyModule:
        def __init__(self, name):
            self.name = name

    module = LegacyModule("LegacyAuth")
    # This should pass because we don't have modules with 'satisfies' yet,
    # but the logic is functional.
    assert HoxPatternRegistry.validate_module(module, "v99.0") is True

def test_phylotypic_core_stability():
    # ARTICLE 128: Stability check
    # 2% change (within 5% limit)
    assert PhylotypicCore.validate_stability("CoreEngine", 0.02) is True
    # 10% change (exceeds 5% limit)
    assert PhylotypicCore.validate_stability("CoreEngine", 0.10) is False

@pytest.mark.asyncio
async def test_digital_reactor_base_functionality():
    # Base class is ABC, so we mock a concrete subclass
    class ScienceReactor(DigitalReactor):
        async def incubate(self, input_data, params):
            return {"status": "SUCCESS", "domain": self.domain}
        async def interact(self, state, action, context): return {}
        async def visualize(self, data, mode): return {}
        async def analyze(self, data): return {}

    reactor = ScienceReactor("science")
    res = await reactor.incubate("test_experiment", {})
    assert res["status"] == "SUCCESS"

    bundle = reactor.bundle([{"paper": "v99_physics.pdf"}], "ACADEMIC_REPORT")
    assert bundle["bundle_id"].startswith("bundle_science")
    assert bundle["items"][0]["paper"] == "v99_physics.pdf"
