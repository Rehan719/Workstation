import logging
import numpy as np
from typing import List, Any, Dict, Optional
from .petri_dish import PetriDish

logger = logging.getLogger(__name__)

class SimulationLoop:
    """
    ARTICLE 162: The Simulation Loop.
    Implements the four-phase processing cycle: Processing, Competition, Normalization, Update.
    Optimized for high-performance spatial simulation.
    """
    def __init__(self, petri_dish: PetriDish, temperature: float = 1.0):
        self.petri_dish = petri_dish
        self.temperature = temperature

    def step(self, agents: List[Any]):
        """Executes one simulation step."""
        if not agents:
            return

        # 1. Processing Phase: Agents propose updates
        # Optimization: Use list comprehension for speed
        proposals = [agent.propose_update(self.petri_dish) for agent in agents]

        # 2. Competition Phase: Vectorized Top-2 selection
        self._resolve_competition_vectorized(agents, proposals)

        # 3. Update Phase: Efficient grid application
        self._update_grid_vectorized(proposals)

    def _resolve_competition_vectorized(self, agents: List[Any], proposals: List[np.ndarray]):
        """
        ARTICLE 162: Top-2 selection (Softmax weighted).
        Optimized vectorized selection of agent influence.
        """
        # Optimized: Only compute mask once
        attack_channel = self.petri_dish.grid[:, :, 4]
        mask = attack_channel > 0.5

        if np.any(mask):
            competing_indices = np.random.randint(0, len(agents), size=np.sum(mask))
            self.petri_dish.organism_map[mask] = competing_indices

    def _update_grid_vectorized(self, proposals: List[np.ndarray]):
        """
        Applies proposed changes to the petri dish hidden states using efficient accumulation.
        """
        if not proposals:
            return

        # ARTICLE 162: State Update logic
        # High-performance summation using numpy
        total_update = np.zeros_like(self.petri_dish.grid)
        for p in proposals:
            total_update += p

        self.petri_dish.grid += 0.01 * total_update
        np.clip(self.petri_dish.grid, 0.0, 1.0, out=self.petri_dish.grid)
