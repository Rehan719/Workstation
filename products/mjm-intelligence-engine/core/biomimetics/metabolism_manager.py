import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ResourceAllocation(BaseModel):
    compute_units: int
    gpu_enabled: bool
    priority: str
    rationale: str

class MetabolismManager:
    """
    Manages computational resource allocation dynamically.
    Biological analogue: Metabolic regulation in response to energy demands.
    """

    def __init__(self, initial_allocation: int = 4):
        self.allocation = initial_allocation
        self.history: List[Dict[str, Any]] = []

    async def allocate_resources(self, domain_id: str, phase: str, urgency: str = "normal") -> ResourceAllocation:
        """Dynamically allocate compute resources based on task complexity and priority."""
        units = self.allocation
        if urgency == "critical":
            units *= 2

        allocation = ResourceAllocation(
            compute_units=units,
            gpu_enabled=(phase == "jaiza"), # jaiza usually needs more power
            priority=urgency,
            rationale=f"Metabolic adjustment for {phase} phase in {domain_id}"
        )

        self.history.append({"timestamp": "now", "allocation": allocation.model_dump()})
        return allocation
