import logging
import time
from typing import Dict, Any

from agentic_core.survival.survival_engine import SurvivalEngine
from agentic_core.immunity.immune_system import ImmuneSystem
from agentic_core.nervous_system.nervous_system import NervousSystem
from agentic_core.cardiovascular.cardiovascular_system import CardiovascularSystem
from agentic_core.digestion.digestive_system import DigestiveSystem
from agentic_core.aging.longevity_engine import LongevityEngine

logger = logging.getLogger(__name__)

class BiologicalOrchestrator:
    """
    L-C-IV: Biological Orchestrator.
    Coordinates all biological subsystems to maintain organism health and execute tasks.
    """
    def __init__(self):
        self.survival = SurvivalEngine()
        self.immune = ImmuneSystem()
        self.nervous = NervousSystem()
        self.cardio = CardiovascularSystem()
        self.digestion = DigestiveSystem()
        self.aging = LongevityEngine()

    async def execute_scientific_task(self, task: Dict[str, Any]):
        logger.info(f"Organism executing task: {task['name']}")

        # 1. Cardio Resource Allocation
        self.cardio.route_resources("nervous_system")

        # 2. Nervous Processing
        start = time.time()
        result = self.nervous.process_signal(task)
        self.survival.enforce_latency("nervous", start)

        # 3. Immune Surveillance
        threat_score = self.immune.evaluate_threat(task)
        if threat_score > 0.8:
            # Hierarchy: Immune overrides others
            logger.error("TASK ABORTED by Immune System.")
            return {"status": "aborted", "reason": "high_threat"}

        # 4. Aging Tracking
        self.aging.track_execution(task.get("type", "unknown"))

        # 5. Homeostatic Maintenance
        self.nervous.maintain_homeostasis()

        return {"status": "success", "result": result}

    def ingest_new_research(self, source: str, data: Dict[str, Any]):
        """Metabolic ingestion of new information."""
        if self.digestion.hunger_level > 0.2:
            return self.digestion.ingest(source, data)
        logger.info("Organism is satiated. Ingestion deferred.")
        return 0.0
