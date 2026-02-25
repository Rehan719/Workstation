import time
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class SystemTier(Enum):
    IMMUNE = "IMMUNE"
    NERVOUS = "NERVOUS"
    DIGESTIVE = "DIGESTIVE"
    AGING = "AGING"

class LatencyArbiter:
    """Article 50: Enforces tier-specific latency constraints."""

    BUDGETS = {
        SystemTier.IMMUNE: 0.0083, # 8.3ms
        SystemTier.NERVOUS: 0.0117, # 11.7ms
        SystemTier.DIGESTIVE: 0.042, # 42ms
        SystemTier.AGING: 0.120,    # Default for others
    }

    def __init__(self):
        self.measurements = {}

    def start_measure(self, tier: SystemTier):
        return time.perf_counter()

    def end_measure(self, tier: SystemTier, start_time: float):
        elapsed = time.perf_counter() - start_time
        budget = self.BUDGETS.get(tier, 0.1)

        if elapsed > budget:
            logger.warning(f"SURVIVAL: Latency violation in {tier.value}. Elapsed: {elapsed*1000:.2f}ms, Budget: {budget*1000:.2f}ms")
            return False
        return True
