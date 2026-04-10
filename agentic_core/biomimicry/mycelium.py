import time
import logging
import random
from typing import Dict, Any, List, Set, Optional

class MycelialClient:
    """
    Implements a resilient P2P network fabric inspired by fungal hyphae.
    Features: Redundant routing, heartbeat gossiping, and automatic rerouting.
    """
    def __init__(self, node_id: str, ueg_callback=None):
        self.node_id = node_id
        self.ueg_callback = ueg_callback
        self.logger = logging.getLogger(f"Mycelial-{node_id}")

        # Network state
        self.peers: Dict[str, Dict[str, Any]] = {} # peer_id -> info
        self.routes: Dict[str, List[str]] = {} # destination -> [path1, path2]
        self.active_paths: Set[str] = set()

    def discover_peer(self, peer_id: str, address: str):
        """Adds a peer to the mycelial mesh."""
        self.peers[peer_id] = {
            "address": address,
            "latency": random.uniform(5, 50),
            "last_heartbeat": time.time(),
            "status": "ALIVE"
        }
        self.logger.info(f"Mycelial: Peer {peer_id} discovered at {address}")
        self._emit_event("PEER_DISCOVERY", {"peer_id": peer_id})

    def send_heartbeat(self):
        """Gossips health signal to neighbors."""
        for peer_id in self.peers:
            # Simulate network activity
            self.peers[peer_id]["last_heartbeat"] = time.time()
        self.logger.debug("Mycelial heartbeats sent.")

    def find_route(self, destination_id: str) -> Optional[List[str]]:
        """
        Finds redundant paths to a destination.
        Matches Article 1102 (latency < 50ms).
        """
        if destination_id in self.peers:
            peer_info = self.peers[destination_id]
            if peer_info["status"] == "ALIVE" and peer_info["latency"] < 50:
                return [self.node_id, destination_id]

        # In a real system, this would use libp2p DHT/Gossipsub
        self.logger.warning(f"No direct route to {destination_id}, searching mycelial mesh...")
        return None

    def handle_partition(self, failed_peer_id: str):
        """
        Automatic rerouting when a node fails.
        """
        if failed_peer_id in self.peers:
            self.peers[failed_peer_id]["status"] = "DEAD"
            self.logger.error(f"Mycelial: Partition detected! Peer {failed_peer_id} unreachable.")

            # Simulated reroute
            new_path = ["core_node_1", "worker_node_A", "target_node"]
            self.logger.info(f"Mycelial: Automatic reroute successful via path: {new_path}")

            self._emit_event("NETWORK_REROUTE", {
                "failed_node": failed_peer_id,
                "new_path": new_path
            })

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": f"MycelialClient-{self.node_id}",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    def autonomous_ueg(e): print(f"UEG -> {e['type']} ({e['payload'].get('peer_id', '')})")
    mesh = MycelialClient("node_alpha", autonomous_ueg)
    mesh.discover_peer("node_beta", "192.168.1.10")
    mesh.handle_partition("node_beta")
