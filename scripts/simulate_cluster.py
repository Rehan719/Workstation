import asyncio
import time
import random
from typing import List, Dict, Any
from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID
from agentic_core.mesh.health.monitor import MeshHealthMonitor
from agentic_core.mesh.aggregator.federated_aggregator import FederatedAggregator
from agentic_core.mesh.consensus.consensus import MeshConsensus
from agentic_core.mesh.negotiation.stream_negotiation import StreamNegotiator
from agentic_core.mesh.negotiation.treaty_negotiation import TreatyNegotiator
from agentic_core.mesh.negotiation.jurisdiction_routing import JurisdictionRouter
from agentic_core.ueg.logger import VSBUEGLogger

class MockLegal:
    def agent_covers_statute(self, *args): return True
    def validate(self, *args): return type('obj', (object,), {'is_compliant': True})()
    def validate_assignment(self, *args): return 1.0

async def run_node(node_name: str, duration: int = 15):
    print(f"Node {node_name} Starting...")
    ueg = VSBUEGLogger()
    discovery = MeshDiscovery(PeerID(node_name), ueg_logger=ueg)
    health = MeshHealthMonitor(ueg_logger=ueg)
    aggregator = FederatedAggregator(discovery=discovery, ueg_logger=ueg)
    consensus = MeshConsensus(node_name, health, ueg_logger=ueg)

    router = JurisdictionRouter(legal_engine=MockLegal())
    negotiator = TreatyNegotiator(node_name, ueg_logger=ueg)
    stream_neg = StreamNegotiator(node_name, negotiator, router, ueg_logger=ueg)

    # Track heartbeats manually for simulation
    health.peer_heartbeats[node_name] = time.time()

    tasks = [
        asyncio.create_task(health.start_heartbeat()),
        asyncio.create_task(aggregator.sync_weights_loop(interval_sec=3.0)),
    ]

    # Simulate Activity
    start = time.time()
    while time.time() - start < duration:
        peers = await discovery.discover_peers("mesh:all", limit=5)
        if peers:
            target = random.choice(peers)
            # Simulate Consensus Proposal
            await consensus.reach_consensus({"id": f"prop_{random.randint(0,100)}"}, [str(p) for p in peers])

            # Simulate Intent Exchange
            await stream_neg.send_intent(str(target), {"id": "intent_1", "profile": [0.7, 0.3]})
            await stream_neg.process_incoming_negotiations(str(target))

        await asyncio.sleep(2.0)

    for t in tasks: t.cancel()
    print(f"Node {node_name} Shutdown.")

async def main():
    print("Sovereign Mesh Stress Simulation v139.1-Ω∞")
    nodes = [run_node(f"node_{i}") for i in range(5)]
    await asyncio.gather(*nodes)
    print("Simulation Complete.")

if __name__ == "__main__":
    asyncio.run(main())
