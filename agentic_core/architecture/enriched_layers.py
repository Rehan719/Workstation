from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.biomimicry.geospheric.orchestrator import GeosphericHomeostaticOrchestrator

class EnrichedArchitecturalLayerManager:
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.geospheric = GeosphericHomeostaticOrchestrator(None, self.ueg)

    async def geospheric_homeostasis(self, inputs: Dict[str, Any], context: Dict[str, Any]):
        try:
            return await self.geospheric.step(inputs)
        except Exception as e:
            # Handle possible positional arg mismatch if step signature changed
            return await self.geospheric.step(inputs, context)
