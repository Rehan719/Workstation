import logging
import time
from typing import Dict, Any
from .global_workspace import GlobalWorkspace
from agentic_core.molecular.triad_integration import MolecularTriad

logger = logging.getLogger(__name__)

class WorkspaceIntegration:
    """
    DB-IV: Foundational Layer Integration.
    Explicitly connects the Molecular Triad to the Global Workspace.
    Ensures cognition is grounded in physiological reality.
    """
    def __init__(self, workspace: GlobalWorkspace, triad: MolecularTriad):
        self.workspace = workspace
        self.triad = triad

    def synchronize(self, substrate: float, load: float) -> Dict[str, Any]:
        """
        Polls the triad and publishes the state vector to the workspace.
        Target: <100ms response from detection to strategic reallocation.
        """
        start_sync = time.perf_counter()

        # 1. Run Triad step
        state_vector = self.triad.run_step(substrate, load)

        # 2. Publish to Workspace
        self.workspace.publish_state("molecular_triad", state_vector)

        latency_ms = (time.perf_counter() - start_sync) * 1000
        logger.debug(f"INTEGRATION: Triad-Workspace sync latency: {latency_ms:.2f}ms")

        return state_vector
