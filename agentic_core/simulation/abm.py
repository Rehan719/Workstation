import logging
import random
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ABMEngine:
    """
    ARTICLE 306: Agent-Based Modeling Engine.
    Simulates complex social, demographic, and market systems.
    """
    def __init__(self):
        self.agents = []
        logger.info("ABMEngine: Initialized.")

    def add_agent(self, agent_data: Dict[str, Any]):
        self.agents.append(agent_data)

    async def step(self) -> List[Dict[str, Any]]:
        """Executes one simulation step for all agents."""
        for agent in self.agents:
            # Domain-specific behavior logic (e.g. market trading, learning)
            strategy = agent.get("strategy", "random")
            if strategy == "opportunistic":
                agent["utility"] = agent.get("utility", 0) + random.uniform(0, 1)
            else:
                agent["utility"] = agent.get("utility", 0) + 0.1

        return self.agents

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self.agents),
            "avg_utility": sum(a.get("utility", 0) for a in self.agents) / max(len(self.agents), 1)
        }
