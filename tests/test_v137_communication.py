import pytest
from agentic_core.communication.adaptive_v137 import AdaptiveCommunicatorV137

def test_v137_channel_selection():
    comm = AdaptiveCommunicatorV137()
    # Mocking high urgency context
    context = {"device": "mobile", "urgency": "high"}
    selected = comm.select_channels("threat_alert", context)

    assert len(selected) == 3
    # With urgency: high, notification and signal should be top choices
    assert "notification" in selected
    assert "signal" in selected

def test_v137_rl_feedback():
    comm = AdaptiveCommunicatorV137()
    initial_q = comm.q_table["avatar"]
    # Provide positive feedback
    comm.record_feedback(["avatar"], True)
    assert comm.q_table["avatar"] > initial_q

    # Provide negative feedback
    comm.record_feedback(["avatar"], False)
    assert comm.q_table["avatar"] < 1.0

def test_v137_delivery_metrics():
    comm = AdaptiveCommunicatorV137()
    meta = comm.deliver_payload("System Stable", "status", {"device": "desktop"})
    assert meta["latency_ms"] < 200.0
    assert meta["v137_compliance"] == True
