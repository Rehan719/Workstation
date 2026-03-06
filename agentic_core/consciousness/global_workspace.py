import logging
import time
import numpy as np
from multiprocessing import shared_memory
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GlobalWorkspace:
    """
    ARTICLE DB: Low-Latency Shared Memory Infrastructure.
    Target latency: <10 ms.
    Uses multiprocessing.shared_memory for zero-copy state aggregation.
    """
    def __init__(self, name: str = "jules_v70_workspace", size: int = 1024):
        self.name = name
        self.size = size
        try:
            self.shm = shared_memory.SharedMemory(name=name, create=True, size=size)
            logger.info(f"WORKSPACE: Created shared memory segment '{name}'.")
        except FileExistsError:
            self.shm = shared_memory.SharedMemory(name=name)
            logger.info(f"WORKSPACE: Attached to existing shared memory segment '{name}'.")

        # State Vector Schema (Simplified for simulation)
        # We use a numpy array backed by shared memory
        self.state_array = np.ndarray((16,), dtype=np.float64, buffer=self.shm.buf)
        self.state_array.fill(0)

    def publish_state(self, index: int, value: float):
        """
        Publishes a scalar state to a specific slot in the shared vector.
        """
        start = time.perf_counter()
        self.state_array[index] = value
        latency_ms = (time.perf_counter() - start) * 1000

        if latency_ms > 10:
             logger.warning(f"WORKSPACE: High latency write: {latency_ms:.4f}ms")

    def read_workspace(self) -> np.ndarray:
        """Returns the current state vector snapshot."""
        return np.copy(self.state_array)

    def close(self):
        try:
            self.shm.close()
            self.shm.unlink()
        except Exception as e:
            logger.debug(f"Shm cleanup info: {e}")

    def __del__(self):
        try:
            self.shm.close()
        except Exception as e:
            logger.debug(f"Shm __del__ cleanup: {e}")
