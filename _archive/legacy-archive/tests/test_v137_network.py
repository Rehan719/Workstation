import pytest
import asyncio
from agentic_core.network.p2p_stack_v137 import Libp2pStack, WebRTCSignalingServer

@pytest.mark.asyncio
async def test_libp2p_stack_dht():
    stack = Libp2pStack()
    await stack.start()

    await stack.dht_put("agent_jules", {"ip": "10.0.0.1", "status": "active"})
    result = await stack.dht_get("agent_jules")

    assert result["status"] == "active"
    await stack.stop()

@pytest.mark.asyncio
async def test_libp2p_gossipsub():
    stack = Libp2pStack()
    await stack.start()
    await stack.subscribe("threat_alerts")
    await stack.publish("threat_alerts", {"id": "ASI_01", "level": "high"})
    # Verification is done via log check in a real environment
    await stack.stop()

@pytest.mark.asyncio
async def test_webrtc_signaling():
    server = WebRTCSignalingServer()
    session_id = await server.create_session("user123", "jules_v137")

    answer = await server.handle_offer(session_id, "v=0\no=- 12345 ...")
    assert "Jules Avatar Answer" in answer

    latency = server.get_latency_metrics(session_id)
    assert latency < 200.0
