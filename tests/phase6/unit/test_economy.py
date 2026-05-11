import pytest
import asyncio
from agentic_core.economy.market.ot_allocator import ResourceMarketAllocator
from agentic_core.economy.pricing.continuous_auction import ContinuousDoubleAuction
from agentic_core.economy.exchange.value_transfer import ValueTransferEngine

@pytest.mark.asyncio
async def test_resource_allocation():
    allocator = ResourceMarketAllocator()
    supply = [{"peer_id": "s1", "available": 1.0, "resource": "compute"}]
    demand = [{"peer_id": "d1", "required": 1.0}]

    res = await allocator.allocate(supply, demand)
    assert res["status"] == "optimized"
    assert len(res["allocations"]) > 0
    assert res["allocations"][0]["amount"] == 1.0

@pytest.mark.asyncio
async def test_double_auction_matching():
    auction = ContinuousDoubleAuction("storage")
    # No match yet
    m1 = await auction.submit_order("p1", "bid", 10.0, 50.0)
    assert m1 is None

    # Match executed
    m2 = await auction.submit_order("p2", "ask", 8.0, 100.0)
    assert m2 is not None
    assert m2["price"] == 9.0
    assert m2["volume"] == 50.0

@pytest.mark.asyncio
async def test_reputation_weighted_transfer():
    class MockHealth:
        def get_reputation(self, p): return 0.2 if p == "dodgy" else 1.0

    engine = ValueTransferEngine(MockHealth(), None)

    # Healthy peer gets full value
    t1 = await engine.execute_transfer("root", "node_1", 100, "service")
    assert t1["effective_value"] == 100

    # Dodgy peer value is discounted
    t2 = await engine.execute_transfer("root", "dodgy", 100, "service")
    assert t2["effective_value"] < 100
    assert t2["effective_value"] == 100 * (0.5 + 0.5 * 0.2) # 60
