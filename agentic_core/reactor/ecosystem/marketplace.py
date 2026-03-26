import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AgentMarketplace:
    """v0.1: Agent Marketplace Registry (JSON-backed)."""
    def __init__(self, registry_path: str = "agentic_core/data/marketplace.json"):
        self.registry_path = registry_path
        os.makedirs(os.path.dirname(registry_path), exist_ok=True)
        self.agents = self._load_agents()

    def _load_agents(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, 'r') as f:
                    return json.load(f)
            except: return []
        return []

    def _save_agents(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.agents, f, indent=2)

    def publish_agent(self, blueprint: Dict[str, Any], creator: str):
        """Publishes a new agent blueprint to the marketplace."""
        agent_id = f"pub-{os.urandom(4).hex()}"
        entry = {
            "id": agent_id,
            "blueprint": blueprint,
            "creator": creator,
            "rating": 0,
            "votes": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.agents.append(entry)
        self._save_agents()
        return agent_id

    def list_agents(self) -> List[Dict[str, Any]]:
        return self.agents

    def rate_agent(self, agent_id: str, rating: int):
        """Simple rating (1-5)."""
        for a in self.agents:
            if a["id"] == agent_id:
                a["votes"] += 1
                a["rating"] = (a["rating"] * (a["votes"] - 1) + rating) / a["votes"]
                self._save_agents()
                return True
        return False

marketplace = AgentMarketplace()
