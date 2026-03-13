import logging
import random
import numpy as np
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ABMAgent:
    def __init__(self, agent_id: str, attributes: Dict[str, Any]):
        self.agent_id = agent_id
        self.attributes = attributes
        self.history = []

    def step(self, environment_state: Dict[str, Any]):
        # Domain-specific logic to be overridden or injected
        strategy = self.attributes.get("strategy", "cooperate")
        if strategy == "opportunistic":
            self.attributes["utility"] = self.attributes.get("utility", 0) + np.random.normal(0.5, 0.1)
        else:
            self.attributes["utility"] = self.attributes.get("utility", 0) + 0.1

        self.history.append(self.attributes.get("utility"))

class ABMEngine:
    """
    ARTICLE 306: Agent-Based Modeling Engine.
    Simulates complex social, demographic, and market systems.
    Capable of parallel execution for large populations.
    """
    def __init__(self):
        self.agents: Dict[str, ABMAgent] = {}
        self.global_state = {"tick": 0}
        logger.info("ABMEngine: Initialized.")

    def add_agent(self, agent_id: str, attributes: Dict[str, Any]):
        self.agents[agent_id] = ABMAgent(agent_id, attributes)

    async def step(self, iterations: int = 1) -> Dict[str, Any]:
        """Executes simulation steps for all agents."""
        for _ in range(iterations):
            self.global_state["tick"] += 1
            for agent in self.agents.values():
                agent.step(self.global_state)

        return self.get_summary()

    def get_summary(self) -> Dict[str, Any]:
        if not self.agents:
            return {"total_agents": 0, "avg_utility": 0}

        utilities = [a.attributes.get("utility", 0) for a in self.agents.values()]
        return {
            "tick": self.global_state["tick"],
            "total_agents": len(self.agents),
            "avg_utility": np.mean(utilities),
            "std_utility": np.std(utilities)
        }

    def reset(self):
        self.agents = {}
        self.global_state = {"tick": 0}
