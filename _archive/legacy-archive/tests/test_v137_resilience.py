import pytest
from agentic_core.biomimicry.geospheric.resilience import ResilienceManager

def test_self_healing():
    mgr = ResilienceManager()
    mgr.system_health = 0.5
    res = mgr.trigger_self_healing({"component": "p2p_relay"})
    assert res["health_boost"] > 0
    assert mgr.system_health == 0.6

def test_graceful_degradation():
    mgr = ResilienceManager()
    assert mgr.feature_flags["advanced_avatars"] == True
    actions = mgr.execute_graceful_degradation()
    assert "FALLBACK_TO_WEBGL_SIM" in actions
    assert mgr.feature_flags["advanced_avatars"] == False

def test_adaptive_reconfiguration():
    mgr = ResilienceManager()
    # Lose 2 nodes
    actions = mgr.perform_adaptive_reconfiguration(2)
    assert "TASK_REROUTING_COMPLETE" in actions
    assert mgr.active_redundant_nodes == 1

    # Lose the last node
    actions2 = mgr.perform_adaptive_reconfiguration(1)
    assert "FALLBACK_TO_WEBGL_SIM" in actions2
    assert mgr.active_redundant_nodes == 0
