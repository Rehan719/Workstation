import time
import logging
import hashlib
from typing import Dict, Any, List, Optional

class KademliaDHT:
    """
    Simulated Kademlia DHT for global agent discovery.
    Uses XOR-based distance and buckets.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.node_id_int = int(hashlib.sha1(node_id.encode()).hexdigest(), 16)
        self.storage: Dict[str, Any] = {} # Key -> Value
        self.routing_table: List[str] = [] # List of known node_ids

    def put(self, key: str, value: Any):
        """Stores a value in the DHT."""
        self.storage[key] = value
        return True

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value from the DHT."""
        return self.storage.get(key)

    def find_node(self, target_id: str) -> List[str]:
        """Returns nodes closest to the target_id."""
        target_int = int(hashlib.sha1(target_id.encode()).hexdigest(), 16)
        # Sort routing table by XOR distance
        sorted_nodes = sorted(self.routing_table, key=lambda n: int(hashlib.sha1(n.encode()).hexdigest(), 16) ^ target_int)
        return sorted_nodes[:5]

class FederationManager:
    """
    Manages cross-node federation, agent discovery, and routing.
    """
    def __init__(self, node_id: str, ueg_callback=None):
        self.node_id = node_id
        self.dht = KademliaDHT(node_id)
        self.ueg_callback = ueg_callback
        self.logger = logging.getLogger(f"Federation-{node_id}")

    def register_agent_globally(self, agent_id: str, metadata: Dict[str, Any]):
        """Publishes agent availability to the DHT."""
        self.dht.put(f"agent:{agent_id}", {
            "node": self.node_id,
            "metadata": metadata,
            "timestamp": time.time()
        })
        self._emit_event("GLOBAL_AGENT_REGISTERED", {"agent_id": agent_id})

    def discover_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Finds an agent across the federation."""
        start_time = time.perf_counter()
        result = self.dht.get(f"agent:{agent_id}")
        end_time = time.perf_counter()

        discovery_ms = (end_time - start_time) * 1000
        if result:
            self.logger.info(f"Discovered agent {agent_id} on node {result['node']} ({discovery_ms:.2f}ms)")

        return result

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": f"Federation-{self.node_id}",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    fed = FederationManager("node_1")
    fed.register_agent_globally("specialist_7", {"domain": "Law"})
    res = fed.discover_agent("specialist_7")
    print(f"Discovery Result: {res}")
