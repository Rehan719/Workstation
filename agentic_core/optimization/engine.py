import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OptimizationEngine:
    """
    ARTICLE 91: Centralized resource optimization across cognitive layers.
    Manages CPU, memory, and network allocation for cognitive workloads.
    """
    def __init__(self, cpu_threshold: float = 0.8, mem_threshold: float = 0.85):
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self.resource_map = {
            "TRIAD": {"priority": 10, "usage": 0.05},
            "MCE": {"priority": 9, "usage": 0.1},
            "QUANTUM": {"priority": 8, "usage": 0.2},
            "BUILDER": {"priority": 7, "usage": 0.3},
            "COLLAB": {"priority": 6, "usage": 0.15}
        }
        logger.info("OptimizationEngine: Initialized with Articles 91 & 150 mandates.")

    def get_allocation_strategy(self, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates the optimal resource allocation based on current system load.
        """
        cpu_load = current_metrics.get("cpu_load", 0.5)
        mem_load = current_metrics.get("mem_load", 0.5)

        strategy = "BALANCED"
        if cpu_load > self.cpu_threshold or mem_load > self.mem_threshold:
            strategy = "PRIORITY_CONSTRAINED"
            logger.warning(f"Resource contention detected (CPU: {cpu_load}, MEM: {mem_load}). Switching to {strategy}.")

        allocations = {}
        for layer, config in self.resource_map.items():
            if strategy == "PRIORITY_CONSTRAINED":
                # Scale usage by priority normalized to max priority (10)
                allocations[layer] = config["usage"] * (config["priority"] / 10.0)
            else:
                allocations[layer] = config["usage"]

        return {
            "strategy": strategy,
            "allocations": allocations,
            "optimization_status": "OPTIMAL" if strategy == "BALANCED" else "CONSTRAINED"
        }

    def optimize_layer_load(self, layer_id: str, load_factor: float) -> float:
        """
        Dynamically adjusts the load factor for a specific layer to maintain system stability.
        """
        if layer_id not in self.resource_map:
            return load_factor

        priority = self.resource_map[layer_id]["priority"]
        # Higher priority (10) gets less reduction than lower priority
        reduction_factor = 1.0 - ((10 - priority) * 0.05)
        optimized_load = load_factor * reduction_factor

        logger.debug(f"OptimizationEngine: Optimized load for {layer_id} from {load_factor} to {optimized_load:.2f}")
        return optimized_load
