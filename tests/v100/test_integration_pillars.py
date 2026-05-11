import asyncio
import pytest
from agentic_core.reactor.science.physics import PhysicsReactor
from agentic_core.reactor.integrator import UnifiedReactorIntegrator

@pytest.fixture
def integrator():
    return UnifiedReactorIntegrator()

@pytest.mark.asyncio
async def test_reactor_integration_with_pillars(integrator):
    physics = PhysicsReactor()
    user_id = "user_v100"
    tier = "pro"

    # Initialize context (ARO + ESE)
    context = await integrator.initialize_reactor_context(user_id, tier, physics)

    assert context["status"] == "INTEGRATED"
    assert "resource_pool" in context
    assert "twin_id" in context

    # Execute Task with VTF (BTO)
    supports = ["science:math", "science:computer_science"]
    result = await integrator.execute_task_with_vtf("intent_456", "science", physics, supports)

    assert result["status"] == "SUCCESS"
    assert "vtf_id" in result

    # Verify collective memory entry
    best = integrator.bto.memory.query_best_strategies("science")
    assert "HYBRID_STRATEGY" in best
