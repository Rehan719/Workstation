import logging
from typing import Dict, List, Any
import time

logger = logging.getLogger(__name__)

class CoordinationServer:
    """
    DO: Swarm Coordination Server.
    Manages node registration and dynamic topology.
    """
    def __init__(self):
        self.registered_nodes: Dict[str, Dict[str, Any]] = {}

    def register_node(self, agent_id: str, capabilities: List[str]):
        logger.info(f"INFRA: Registering agent {agent_id} with capabilities {capabilities}")
        self.registered_nodes[agent_id] = {
            "capabilities": capabilities,
            "last_heartbeat": time.time(),
            "status": "ONLINE"
        }

    def deregister_node(self, agent_id: str):
        if agent_id in self.registered_nodes:
            logger.info(f"INFRA: Deregistering agent {agent_id}")
            del self.registered_nodes[agent_id]

    def heartbeat(self, agent_id: str):
        if agent_id in self.registered_nodes:
            self.registered_nodes[agent_id]["last_heartbeat"] = time.time()

    def get_active_nodes(self) -> List[str]:
        current_time = time.time()
        active = []
        for aid, info in self.registered_nodes.items():
            if current_time - info["last_heartbeat"] < 30: # 30s timeout
                active.append(aid)
        return active

    def get_node_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return self.registered_nodes.get(agent_id)
