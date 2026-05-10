import pytest
import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from agentic_core.federation.autonomous_mesh import AutonomousMesh

@pytest.mark.slow
@pytest.mark.asyncio
async def test_mesh_stress_simulation():
    """Simulates 10 virtual nodes negotiating treaties."""
    node_count = 10
    nodes = []

    # 1. Initialize nodes
    for i in range(node_count):
        val = MagicMock()
        val.validate_action = AsyncMock(return_value={"passed": True})
        ueg = MagicMock()
        ueg.log_event = AsyncMock()

        mesh = AutonomousMesh(val)
        mesh.host_id = f"node_{i}"
        nodes.append(mesh)

    # 2. Discover and negotiate
    for i in range(node_count):
        # Peer with the next node in cycle
        peer_node = nodes[(i + 1) % node_count]
        peer_info = {"id": peer_node.host_id, "constitution_hash": "sha3_abc"}

        treaty = await nodes[i].negotiate_treaty(peer_info, {"liquidity_cap": 5.0})
        assert treaty.status == "SIGNED"
        assert treaty.node_a == nodes[i].host_id
        assert treaty.node_b == peer_node.host_id

    print(f"Mesh stress test passed with {node_count} nodes.")
