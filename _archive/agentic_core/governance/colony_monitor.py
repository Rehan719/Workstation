import logging
import time
from typing import List

logger = logging.getLogger(__name__)

class ColonyMonitor:
    """
    DD-V: Colony density and stability monitor.
    Ensures minimum viable colony size (>= 5 nodes) for revalidation.
    """
    def __init__(self, min_size: int = 5):
        self.min_size = min_size
        self.active_nodes: List[str] = []

    def update_nodes(self, node_ids: List[str]):
        self.active_nodes = node_ids
        logger.info(f"COLONY: Currently monitoring {len(self.active_nodes)} active nodes.")

    def check_viability(self) -> bool:
        is_viable = len(self.active_nodes) >= self.min_size
        if not is_viable:
            logger.warning(f"COLONY: Underpopulated! Size {len(self.active_nodes)} < {self.min_size}")
        return is_viable
