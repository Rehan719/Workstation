import logging
import random
from typing import Dict, Any, List, Optional
import mesa
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from datetime import datetime

logger = logging.getLogger(__name__)

class ReligionAgent(Agent):
    """An agent representing a religious scholar or community member with beliefs."""
    def __init__(self, model, unique_id, initial_belief_score: float, conviction: float):
        super().__init__(model)
        self.belief_score = initial_belief_score # 0.0 to 1.0
        self.conviction = conviction # Resistance to change (0.0 to 1.0)
        self.influence = random.uniform(0.1, 0.5)

    def step(self):
        # Interact with neighbors/random agents to simulate idea diffusion
        other_agent = self.model.random.choice(self.model.agents)
        if other_agent == self:
            return

        # Simple probabilistic belief adjustment
        delta = (other_agent.belief_score - self.belief_score) * (1 - self.conviction) * other_agent.influence
        self.belief_score += delta
        self.belief_score = max(0.0, min(1.0, self.belief_score))

class EvolutionarySimulationEngine(Model):
    """
    QEP - ESE: Evolutionary Simulation Engine.
    Models theological debates, belief diffusion, and hypothetical scenarios.
    """
    def __init__(self, num_agents: int = 100, initial_belief_mean: float = 0.5):
        super().__init__()
        self.num_agents = num_agents

        for i in range(self.num_agents):
            a = ReligionAgent(
                self,
                i,
                initial_belief_score=random.gauss(initial_belief_mean, 0.1),
                conviction=random.uniform(0.05, 0.2)
            )
            # In mesa 2.x+, agents are added to the model automatically if they inherit from Agent
            # But we might need to manage them for the schedule if using older patterns.
            # Mesa 3.x uses Model.agents property.

        self.datacollector = DataCollector(
            model_reporters={"AvgBelief": lambda m: sum([a.belief_score for a in m.agents]) / len(m.agents)},
            agent_reporters={"Belief": "belief_score"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")

    async def run_simulation(self, steps: int = 50) -> Dict[str, Any]:
        """Runs the simulation and returns results."""
        start_time = datetime.utcnow().isoformat()
        for _ in range(steps):
            self.step()

        model_vars = self.datacollector.get_model_vars_dataframe()

        return {
            "engine": "ESE",
            "timestamp": datetime.utcnow().isoformat(),
            "start_time": start_time,
            "steps_completed": steps,
            "final_avg_belief": float(model_vars["AvgBelief"].iloc[-1]),
            "history": model_vars["AvgBelief"].tolist()
        }

def get_ese_instance(num_agents: int = 100) -> EvolutionarySimulationEngine:
    return EvolutionarySimulationEngine(num_agents=num_agents)
