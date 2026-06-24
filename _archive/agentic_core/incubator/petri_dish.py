import logging
import numpy as np
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PetriDish:
    """
    ARTICLE 162: The Petri Dish Incubator.
    Spatial grid environment for digital organism competition.
    """
    def __init__(self,
                 width: int = 50,
                 height: int = 50,
                 channels: int = 16):
        """
        Initializes the petri dish spatial grid.

        Args:
            width (int): Grid width.
            height (int): Grid height.
            channels (int): Number of state channels (e.g., visual, hidden).
        """
        self.width: int = width
        self.height: int = height
        self.channels: int = channels
        # Grid state: (W, H, C)
        self.grid: np.ndarray = np.zeros((width, height, channels), dtype=np.float32)
        self.organism_map: np.ndarray = np.zeros((width, height), dtype=np.int32)

    def apply_attack(self, x: int, y: int, strength: float) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y, 4] = np.clip(self.grid[x, y, 4] + strength, 0.0, 1.0)

    def apply_defense(self, x: int, y: int, strength: float) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y, 5] = np.clip(self.grid[x, y, 5] + strength, 0.0, 1.0)

    def get_local_neighborhood(self, x: int, y: int, radius: int = 1) -> np.ndarray:
        x_start = max(0, x - radius)
        x_end = min(self.width, x + radius + 1)
        y_start = max(0, y - radius)
        y_end = min(self.height, y + radius + 1)
        return self.grid[x_start:x_end, y_start:y_end, :]
