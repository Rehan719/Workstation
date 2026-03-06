import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Environment:
    """
    ARTICLE 162: The Environmental Engine.
    Manages energy distribution, resource regeneration, and change events.
    """
    def __init__(self, width: int = 50, height: int = 50):
        self.width = width
        self.height = height
        self.energy_grid = np.ones((width, height), dtype=np.float32)
        self.regeneration_rate = 0.05

    def regenerate(self):
        """Regenerates energy resources across the spatial grid."""
        self.energy_grid = np.clip(self.energy_grid + self.regeneration_rate, 0.0, 1.0)

    def consume_energy(self, x: int, y: int, amount: float) -> float:
        """Allows an organism to retrieve energy from the grid."""
        available = self.energy_grid[x, y]
        consumed = min(available, amount)
        self.energy_grid[x, y] -= consumed
        return consumed

    def trigger_catastrophe(self, severity: float = 0.5):
        """Simulates environmental turmoil to test adaptation pressure."""
        mask = np.random.rand(self.width, self.height) < severity
        self.energy_grid[mask] = 0.0
        logger.warning(f"Catastrophic event triggered with severity {severity}.")
