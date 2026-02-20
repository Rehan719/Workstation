import pytest
from agentic_core.quantum_ai.hierarchy_manager import CapabilityHierarchyManager

@pytest.mark.asyncio
async def test_tier_stability():
    manager = CapabilityHierarchyManager()
    is_stable = await manager.check_tier_stability('tier1')
    assert is_stable is True
    assert manager.tiers['tier1']['stable'] is True

@pytest.mark.asyncio
async def test_tier_prerequisites():
    manager = CapabilityHierarchyManager()
    # By default tier1 is not stable, so tier2 should fail if checked immediately without stability check
    # But hierarchy_manager's ensure_tier_prerequisites calls check_tier_stability internally if needed
    result = await manager.ensure_tier_prerequisites('tier2')
    assert result is True
