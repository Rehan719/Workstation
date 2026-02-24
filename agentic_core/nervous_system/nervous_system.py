import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NervousSystem:
    """
    L-C-VI: Central and Peripheral Nervous System.
    Reflex arcs (<50ms) and deliberative reasoning (200-800ms).
    """
    def __init__(self):
        self.homeostasis_baseline = 1.0
        self.firing_rate = 1.0

    def process_signal(self, signal: Dict[str, Any]):
        """Routes to peripheral (reflex) or central (deliberative) paths."""
        priority = signal.get("priority", "normal")

        start_time = time.time()
        if priority == "reflex":
            return self._reflex_arc(signal, start_time)
        return self._deliberative_cortex(signal, start_time)

    def _reflex_arc(self, signal: Dict[str, Any], start: float):
        # Tier 1 fixed: <50ms
        logger.info("Executing PERIPHERAL REFLEX ARC...")
        time.sleep(0.01) # 10ms processing
        return {"latency": (time.time() - start) * 1000}

    def _deliberative_cortex(self, signal: Dict[str, Any], start: float):
        # Tier 2 tunable: 200-800ms
        logger.info("Executing CENTRAL DELIBERATIVE REASONING...")
        time.sleep(0.3) # 300ms processing
        return {"latency": (time.time() - start) * 1000}

    def maintain_homeostasis(self):
        """Astrocyte-inspired homeostasis: ±5% firing rate regulation."""
        deviation = abs(self.firing_rate - self.homeostasis_baseline)
        if deviation > 0.05:
            logger.info(f"Homeostatic correction: {self.firing_rate:.2f} -> {self.homeostasis_baseline}")
            self.firing_rate = self.homeostasis_baseline
