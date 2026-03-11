import asyncio
import logging
import os
from typing import List, Dict, Any, Optional
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine
from agentic_core.synthesis.collation.orchestrator import CollationOrchestrator
from agentic_core.synthesis.convergence.engine import ConvergenceEngine
from agentic_core.synthesis.assimilation.engine import AssimilationEngine
from agentic_core.ueg.version_graph import VersionGraph

logger = logging.getLogger(__name__)

class GrandSynthesisService:
    """ARTICLE 323: Grand Synthesis as a continuous business service."""
    def __init__(self):
        self.engine = GrandSynthesisEngine()
        self.vg = VersionGraph()
        self.collator = CollationOrchestrator()
        self.converger = ConvergenceEngine()
        self.assimilator = AssimilationEngine()

    async def run_synthesis(self, mode: str = "routine", scope: Optional[List[str]] = None) -> Dict[str, Any]:
        """Executes a GSE run in the specified mode (adhoc, ondemand, routine, planned)."""
        run_id = f"run_{int(asyncio.get_event_loop().time())}"
        logger.info(f"QMS: Initiating {mode} Grand Synthesis run {run_id}")

        self.vg.add_pipeline_run(run_id, "gse_operations", "started", mode=mode)

        # 1. Category Collation
        collation_data = await self.collator.run_full_collation()

        # 2. Convergence
        converged_configs = await self.converger.run_convergence(collation_data)

        # 3. Code & Constitution Synthesis
        synthesis_result = await self.engine.run_synthesis(output_path=f"meta/synthesis/run_{run_id}.json")

        # 4. Optional Assimilation (planned or adhoc only)
        if mode in ["planned", "adhoc"]:
            await self.assimilator.assimilate_all(converged_configs)

        self.vg.add_pipeline_run(run_id, "gse_operations", "completed", mode=mode)
        logger.info(f"QMS: Grand Synthesis run {run_id} complete.")

        return synthesis_result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = GrandSynthesisService()
    asyncio.run(service.run_synthesis(mode="routine"))
