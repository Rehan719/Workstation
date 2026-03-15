import pytest
from agentic_core.communication.adaptive_v137 import AdaptiveCommunicatorV137

def test_v137_channel_selection():
    comm = AdaptiveCommunicatorV137()
    # Mocking high urgency mobile context
    class MockMsg: type = "threat"; emotional = False
    context = {"device": "mobile", "urgency": "high"}
    selected = comm.select_channels(MockMsg(), context)

    assert len(selected) == 3
    # With urgency: high and device: mobile, notification should be top
    assert "notification" in selected
    assert "signal" in selected

def test_v137_rl_feedback():
    comm = AdaptiveCommunicatorV137()
    context = {"device": "desktop"}
    comm.record_feedback(context, "info", ["dashboard"], 1.0)

    state = comm._encode_state(context, "info")
    assert comm.q_table[(state, "dashboard")] > 0.5

def test_v137_full_cycle():
    comm = AdaptiveCommunicatorV137()
    class Msg: type = "status"; emotional = True
    channels = comm.communicate(Msg(), "user_1", {"device": "desktop"})
    assert "avatar" in channels or "ethical" in channels
