import pytest
from agentic_core.communication.multi_modal_v136 import MultiModalCommunicatorV136

def test_communicator_v136_initialization():
    comm = MultiModalCommunicatorV136()
    assert "Video_Avatar" in comm.channels
    assert comm.channel_performance["Video_Avatar"] == 0.8

def test_neuro_optimal_selection():
    comm = MultiModalCommunicatorV136()
    channel = comm.select_neuro_optimal_channel("focused")
    # Serotonin bias for focused
    assert channel in ["Email_Briefing", "CLI_Output"]

def test_v136_delivery_cycle():
    comm = MultiModalCommunicatorV136()
    result = comm.run_v136_delivery("Hello Sovereign", "urgent")

    assert result["status"] == "SUCCESS"
    assert result["payload"]["latency_ms"] < 200.0
    assert result["channel_selected"] in ["Voice_Only", "Push_Notification"] # Oxytocin bias

def test_feedback_learning():
    comm = MultiModalCommunicatorV136()
    initial = comm.channel_performance["CLI_Output"]
    comm.record_feedback("CLI_Output", True)
    assert comm.channel_performance["CLI_Output"] > initial

    initial = comm.channel_performance["CLI_Output"]
    comm.record_feedback("CLI_Output", False)
    assert comm.channel_performance["CLI_Output"] < initial
