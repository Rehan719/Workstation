import logging
import time
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HomeostaticRegulator:
    """
    L-C-VII: Homeostatic Balance Regulator with Allostatic Load.
    Monitors a 10-biomarker system for quantified homeostasis.
    """
    def __init__(self):
        self.biomarkers = {
            "hrv_sdnn": 60.0,      # ms (HRV simulation)
            "latency_avg": 25.0,   # ms
            "error_rate": 0.001,
            "resource_usage": 0.3,
            "throughput": 100.0,
            "synaptic_scaling": 18.6,
            "immune_activity": 0.1,
            "digestive_hunger": 0.5,
            "component_health": 1.0,
            "conflict_level": 0.0
        }
        self.allostatic_load = 0.0

    def update_metrics(self, telemetry: Dict[str, Any]):
        """Updates biomarkers and recalculates allostatic load."""
        for k, v in telemetry.items():
            if k in self.biomarkers:
                self.biomarkers[k] = v

        self._calculate_allostatic_load()

    def _calculate_allostatic_load(self):
        """Quantifies stress on the organism (0.0 to 10.0)."""
        load = 0.0
        # High latency (>120ms) increases load
        if self.biomarkers["latency_avg"] > 120: load += 2.0
        # Low HRV (<20ms) suggests stress
        if self.biomarkers["hrv_sdnn"] < 20: load += 2.0
        # High error rate (>0.05)
        if self.biomarkers["error_rate"] > 0.05: load += 2.0
        # High resource usage (>0.9)
        if self.biomarkers["resource_usage"] > 0.9: load += 2.0
        # Immune activity (>0.8)
        if self.biomarkers["immune_activity"] > 0.8: load += 2.0

        self.allostatic_load = load
        logger.info(f"Allostatic Load updated: {self.allostatic_load:.2f}/10.0")

    def get_routing_decision(self) -> str:
        """HRV-linked decision routing (SDNN < 50ms -> Fast/Peripheral)."""
        if self.biomarkers["hrv_sdnn"] < 50.0:
            return "peripheral"
        return "central"
