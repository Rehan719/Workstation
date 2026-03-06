import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TelomereTracker:
    """Article 49: Tracks code/component health via versioning (telomere-like)."""

    def __init__(self):
        self.health_counters = {} # component_id -> health (0.0 to 1.0)

    def register_component(self, component_id: str, initial_health: float = 1.0):
        self.health_counters[component_id] = initial_health

    def decrement(self, component_id: str):
        if component_id in self.health_counters:
            self.health_counters[component_id] -= 0.05
            logger.debug(f"AGING: Component {component_id} telomere shortened. Health: {self.health_counters[component_id]:.2f}")

    def regenerate(self, component_id: str):
        if component_id in self.health_counters:
            self.health_counters[component_id] = min(1.0, self.health_counters[component_id] + 0.1)
            logger.info(f"AGING: Component {component_id} regenerated upon successful verification.")

    def get_health(self, component_id: str) -> float:
        return self.health_counters.get(component_id, 1.0)
