import logging
import asyncio
import uuid
import time
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ProtocolType(Enum):
    MCP = "Model Context Protocol"
    A2A = "Agent-to-Agent"
    ACP = "Agent Communication Protocol"
    ANP = "Agent Network Protocol"

class MycelialBackbone:
    """ARTICLE III.A: VSB (Virtual Systems Bridge) — Mycelial resilience layer.

    W440 truth pass: this is an IN-MEMORY agent registry with simulated transport. No
    authentication exists ("zero-trust auth" was advertising); route_message/_find_failover are
    UNREACHED from any surface and carry the repo's §4.5 archetype (see their comments) — they
    must not be wired as-is.
    """
    def __init__(self):
        self.registry = {} # Agent Cards
        self.active_links = {}
        self.failures = set()
        self.latency_p95 = 0.0

    async def register_agent(self, agent_id: str, card: Dict[str, Any]) -> bool:
        """DID-labelled registration (the DID is minted here; nothing is verified — no JSON-LD
        processing exists, and re-registration replaces the card)."""
        did = card.get("did", f"did:vsb:{uuid.uuid4().hex[:8]}")
        self.registry[agent_id] = {
            "did": did,
            "capabilities": card.get("capabilities", []),
            "status": "ONLINE",
            "last_seen": time.time()
        }
        logger.info(f"VSB: Agent {agent_id} registered with DID {did}")
        return True

    async def route_message(self, source: str, target: str, payload: Dict[str, Any], protocol: ProtocolType) -> Dict[str, Any]:
        """UNREACHED (W440: zero callers) and NOT wire-ready — §4.5 archetype: the payload is
        ignored, an unregistered target still returns status "DELIVERED" (a constant), and the
        latency is a simulated sleep. Fix delivery semantics before ever wiring this."""
        start_time = time.time()

        if target in self.failures:
            # Dynamic rerouting logic
            logger.warning(f"VSB: Target {target} offline. Initiating rerouting...")
            target = self._find_failover(target)

        # Simulate transport latency
        await asyncio.sleep(0.04)

        elapsed = (time.time() - start_time) * 1000
        self.latency_p95 = (self.latency_p95 * 0.9) + (elapsed * 0.1)

        logger.info(f"VSB: Message routed via {protocol.value} in {elapsed:.2f}ms")

        return {
            "status": "DELIVERED",
            "latency_ms": elapsed,
            "protocol": protocol.name,
            "target": target
        }

    def _find_failover(self, failed_target: str) -> str:
        # W440: §4.5 archetype — picks the FIRST agent by dict insertion order (capabilities and
        # status ignored) and fabricates "HYPHAL_NODE_0" for an empty registry. Unreached; must
        # select on real criteria (and refuse honestly when no candidate exists) before wiring.
        for agent_id in self.registry:
            if agent_id != failed_target:
                return agent_id
        return "HYPHAL_NODE_0"

    def simulate_link_failure(self, agent_id: str):
        self.failures.add(agent_id)
        logger.error(f"VSB: Link failure detected for {agent_id}. Topology reconfiguring.")

    def get_backbone_health(self) -> Dict[str, Any]:
        # W440 — the old field was named latency_p95: the figure is an EWMA over SIMULATED
        # transport (a 40ms sleep), neither a p95 nor a measurement; and a 0-node registry
        # reported failure_rate 0.0 as if measured. Names now match what the values are.
        nodes = len(self.registry)
        return {
            "latency_ewma_ms": round(self.latency_p95, 2),
            "latency_note": "EWMA over SIMULATED transport (fixed 40ms sleep) — not a measured p95",
            "active_nodes": nodes,
            "failure_rate": (len(self.failures) / nodes) if nodes else None,
            "failure_rate_basis": (f"failed links / {nodes} registered nodes" if nodes else
                                   "no nodes registered — nothing measured"),
            "scope": "in-memory, this server process since start",
            "protocol_stack": [p.name for p in ProtocolType],
        }
