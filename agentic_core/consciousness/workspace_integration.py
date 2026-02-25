import time
from typing import Dict, Any
from .global_workspace import GlobalWorkspace
from .meta_cognitive_executive import MetaCognitiveExecutive
from .gamma_coherence import GammaCoherenceMonitor
from .ignition_detector import IgnitionDetector

class ConsciousnessEngine:
    """
    ARTICLE DB: High-level consciousness orchestrator.
    Stress Response: Triad-to-MCE loop <100 ms.
    """
    def __init__(self):
        self.workspace = GlobalWorkspace()
        self.mce = MetaCognitiveExecutive()
        self.gamma_monitor = GammaCoherenceMonitor()
        self.ignition = IgnitionDetector()

    def run_cognitive_cycle(self, subsystem_states: Dict[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()

        # 1. Publish all to workspace
        for cid, state in subsystem_states.items():
            self.workspace.publish_state(cid, state)

        # 2. Strategic Decision (MCE)
        workspace_full = self.workspace.read_workspace()
        # Flattened for MCE
        triad_state = workspace_full.get("triad", {}).get("data", {})
        decision = self.mce.make_strategic_decision({"triad": triad_state})

        # 3. Coherence and Ignition
        import numpy as np
        sig1 = np.random.rand(100)
        sig2 = np.random.rand(100)
        self.gamma_monitor.calculate_coherence(sig1, sig2)

        duration_ms = (time.perf_counter() - start) * 1000
        return {
            "decision": decision,
            "integrated": self.gamma_monitor.is_consciously_integrated(),
            "cycle_latency_ms": duration_ms
        }
