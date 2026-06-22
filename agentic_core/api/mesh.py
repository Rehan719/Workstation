"""
Federation Mesh API — surfaces Workstation's OWN multi-instance federation mesh
(`agentic_core.mesh`) into the live platform: peer discovery, reputation-weighted BFT consensus,
and health/heartbeat. Previously developed but entirely unwired (0 importers); now reachable and a
first-class Resource-Fabric resource — leveraging an existing in-house capability.

Honest by construction: in a single-node deployment there are NO real remote peers, so discovery
returns simulated nodes (clearly flagged `simulated: true`). The Schrödinger-bridge **treaty
ledger** requires the optional ML stack (`torch`) which is not in the lightweight runtime, so it
is deliberately NOT imported here — it is reported as available-with-that-stack rather than faked.

  GET /api/v1/mesh/status — the federation mesh's live posture + capabilities
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/mesh", tags=["federation-mesh"])

_NODE = "workstation-node-0"


@router.get("/status")
async def mesh_status():
    out = {
        "node_id": _NODE,
        "operational": True,
        "posture": "in-house federation mesh",
        "modules": ["discovery", "consensus", "health", "treaty_ledger",
                    "treaty_negotiation", "jurisdiction_routing", "aggregator"],
        "treaty_ledger": "available with the optional ML stack (torch) — Schrödinger-bridge "
                         "treaty negotiation; not loaded in the lightweight runtime.",
    }
    # Reputation-weighted BFT consensus + health (torch-free, real classes).
    try:
        from agentic_core.mesh.health.monitor import MeshHealthMonitor
        from agentic_core.mesh.consensus.consensus import MeshConsensus
        health = MeshHealthMonitor()
        consensus = MeshConsensus(_NODE, health)
        out["consensus"] = {"type": "reputation-weighted BFT", "supermajority": "2/3 + 1",
                            "timeout_s": consensus.timeout}
        out["health"] = {"heartbeat_interval_s": health.heartbeat_interval,
                         "self_reputation": round(health.get_reputation(_NODE), 3)}
    except Exception as e:
        out["consensus_error"] = str(e)[:120]
    # Peer discovery (simulated in a single-node deployment — honestly flagged).
    try:
        from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID
        peers = await MeshDiscovery(PeerID(_NODE)).discover_peers("vsb-federation", limit=5)
        out["discovery"] = {"topic": "vsb-federation", "peers": [str(p) for p in peers],
                            "simulated": True,
                            "note": "single-node deployment — peers are simulated until real remote "
                                    "instances join the mesh."}
    except Exception as e:
        out["discovery"] = {"peers": [], "simulated": True, "error": str(e)[:120]}
    return out
