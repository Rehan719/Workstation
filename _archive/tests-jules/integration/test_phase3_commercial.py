from agentic_core.commercial.tier_manager import TierManager
from backend.usage.sovereign_meter import SovereignMeter
def test_tiers():
    mgr = TierManager(SovereignMeter(None))
    assert mgr.get_resource_limits("advanced")["con"] == 20
