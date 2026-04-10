import time
import logging
import random
import math
from typing import List, Dict, Any, Optional

class SwarmAgent:
    """
    Simulated agent for swarm formation.
    Tracks 'position' in task space and trust vectors.
    """
    def __init__(self, agent_id: str, task_vector: List[float]):
        self.agent_id = agent_id
        self.pos = task_vector # N-dimensional task competency vector
        self.vel = [random.uniform(-0.1, 0.1) for _ in range(len(task_vector))]
        self.swarm_id = None
        self.trust_score = 1.0

class SwarmFormationEngine:
    """
    Implements autonomous swarm formation using Boids-inspired rules.
    - Cohesion: Agents move toward the average position of neighbors.
    - Alignment: Agents match velocity with neighbors.
    - Separation: Agents avoid crowding.
    """
    def __init__(self, nats_client=None, ueg_callback=None):
        self.logger = logging.getLogger("SwarmFormation")
        self.nc = nats_client
        self.ueg_callback = ueg_callback
        self.agents: Dict[str, SwarmAgent] = {}
        self.swarms: Dict[str, List[str]] = {} # swarm_id -> [agent_ids]

    def add_agent(self, agent_id: str, task_vector: List[float]):
        self.agents[agent_id] = SwarmAgent(agent_id, task_vector)

    def update_topology(self):
        """
        Runs one iteration of the Boids-based self-organization.
        Identifies clusters and forms swarms.
        """
        agent_list = list(self.agents.values())
        if len(agent_list) < 2: return

        for agent in agent_list:
            # 1. Calculate Boids forces (Simplified)
            # Find neighbors in task space
            neighbors = [a for a in agent_list if a.agent_id != agent.agent_id and
                         self._distance(agent.pos, a.pos) < 0.5]

            if neighbors:
                # Cohesion: Move to center
                center = [sum(n.pos[i] for n in neighbors)/len(neighbors) for i in range(len(agent.pos))]
                for i in range(len(agent.pos)):
                    agent.vel[i] += (center[i] - agent.pos[i]) * 0.05

                # Update swarm assignment based on cluster
                if not agent.swarm_id:
                    new_swarm_id = f"swarm_{random.randint(1000, 9999)}"
                    agent.swarm_id = new_swarm_id
                    self.swarms[new_swarm_id] = [agent.agent_id]
                    self._emit_event("SWARM_FORMED", {"swarm_id": new_swarm_id, "leader": agent.agent_id})

            # Update position
            for i in range(len(agent.pos)):
                agent.pos[i] += agent.vel[i]

    def _distance(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "SwarmFormationEngine",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    engine = SwarmFormationEngine()
    engine.add_agent("agent_1", [0.1, 0.2])
    engine.add_agent("agent_2", [0.15, 0.25])
    engine.add_agent("agent_3", [0.9, 0.9])

    for _ in range(5):
        engine.update_topology()
        print(f"Swarms: {engine.swarms}")
