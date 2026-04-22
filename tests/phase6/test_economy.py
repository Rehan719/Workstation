import torch
import pytest
import asyncio
from agentic_core.economy.market.ot_allocator import ResourceMarketAllocator
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.economy.policy.rl_economist import RLEconomist

@pytest.mark.asyncio
async def test_ot_resource_allocation():
    ot_core = OptimalTransportRouter()
    allocator = ResourceMarketAllocator(ot_core)

    supply = [{"id": "S1", "available": 100.0}, {"id": "S2", "available": 50.0}]
    demand = [{"id": "D1", "required": 80.0}, {"id": "D2", "required": 70.0}]

    res = await allocator.allocate(supply, demand)
    assert len(res["plan"]) == 2
    assert res["wasserstein"] >= 0

def test_rl_economist_legal_floor():
    economist = RLEconomist(state_dim=10, action_dim=5, legal_floor=0.15)
    state = torch.randn(10)
    probs = economist.forward(state)

    # Probabilities should be valid and respect a minimal non-zero floor for exploration/legality
    assert torch.all(probs > 0)
    assert torch.isclose(probs.sum(), torch.tensor(1.0))
