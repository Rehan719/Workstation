import time
import logging
import asyncio
import json
from typing import Dict, Any, List, Optional

# Mock NATS Client for environments without a real server
class MockNATS:
    async def connect(self, servers): return True
    async def publish(self, subject, payload): return True
    async def subscribe(self, subject, cb): return True
    async def flush(self): return True
    async def close(self): return True

class AntColonyScheduler:
    """
    Implements swarm coordination using pheromone tables and stigmergy.
    Integrated with NATS for task allocation.
    """
    def __init__(self, nats_server: str = "nats://localhost:4222", ueg_callback=None):
        self.logger = logging.getLogger("AntColonyScheduler")
        self.nats_server = nats_server
        self.ueg_callback = ueg_callback
        # Pheromone Table: subject -> agent_id -> pheromone_level
        self.pheromones: Dict[str, Dict[str, float]] = {}
        self.decay_rate = 0.1
        self.nc = MockNATS() # Will attempt real connect in async init

    async def initialize(self):
        try:
            import nats
            self.nc = await nats.connect(self.nats_server)
            self.logger.info(f"AntColony connected to NATS at {self.nats_server}")
        except Exception as e:
            self.logger.warning(f"Could not connect to real NATS, using mock. Error: {e}")

    async def allocate_task(self, task_type: str, task_data: Dict[str, Any]):
        """
        Allocates a task based on pheromone levels (Stigmergy).
        """
        # Find best agent for task_type
        agent_scores = self.pheromones.get(task_type, {})
        if not agent_scores:
            # Broadcast task if no pheromones exist
            await self.nc.publish(f"tasks.{task_type}.broadcast", json.dumps(task_data).encode())
            self._emit_event("TASK_BROADCAST", {"task_type": task_type})
            return "BROADCAST"

        # Selection based on highest pheromone (simple greedy)
        best_agent = max(agent_scores, key=agent_scores.get)

        await self.nc.publish(f"tasks.{task_type}.{best_agent}", json.dumps(task_data).encode())
        self._emit_event("TASK_ALLOCATED", {"task_type": task_type, "agent_id": best_agent})

        return best_agent

    async def deposit_pheromone(self, task_type: str, agent_id: str, amount: float):
        """
        Increases pheromone level for an agent (Positive Feedback).
        """
        if task_type not in self.pheromones:
            self.pheromones[task_type] = {}

        current = self.pheromones[task_type].get(agent_id, 0.0)
        self.pheromones[task_type][agent_id] = current + amount

        self.logger.info(f"Pheromone deposit: {task_type} -> {agent_id} (+{amount})")

    def decay_pheromones(self):
        """
        Simulates natural pheromone evaporation to prevent stagnation.
        """
        for task_type in self.pheromones:
            for agent_id in self.pheromones[task_type]:
                self.pheromones[task_type][agent_id] *= (1.0 - self.decay_rate)

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "AntColonyScheduler",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    async def test():
        scheduler = AntColonyScheduler()
        await scheduler.initialize()
        await scheduler.deposit_pheromone("translation", "agent_1", 10.0)
        agent = await scheduler.allocate_task("translation", {"text": "hello"})
        print(f"Allocated to: {agent}")
        scheduler.decay_pheromones()

    asyncio.run(test())
