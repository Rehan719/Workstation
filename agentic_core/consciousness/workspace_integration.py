import time
import numpy as np
from typing import Dict, Any
from .global_workspace import GlobalWorkspace
from .meta_cognitive_executive import MetaCognitiveExecutive
from .gamma_coherence import GammaCoherenceMonitor
from .ignition_detector import IgnitionDetector

class ConsciousnessEngine:
    """
    ARTICLE DB: High-level consciousness orchestrator.
    Now utilizes Shared Memory Global Workspace and PLV monitoring.
    """
    def __init__(self):
        self.workspace = GlobalWorkspace()
        self.mce = MetaCognitiveExecutive()
        self.gamma_monitor = GammaCoherenceMonitor()
        self.ignition = IgnitionDetector()

    def run_cognitive_cycle(self, triad_state: Dict[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()

        # 1. Publish to Shared Memory Workspace
        self.workspace.publish_state(0, triad_state.get("redox_potential_mv", -225.0))
        self.workspace.publish_state(1, triad_state.get("atp_adp_ratio", 5.0))
        self.workspace.publish_state(2, triad_state.get("p53_level", 0.5))
        self.workspace.publish_state(3, triad_state.get("ubiquitin_stress", 0.05))
        self.workspace.publish_state(4, triad_state.get("hsp_atp_turnover", 3.0))

        # 2. Strategic Decision (MCE)
        workspace_vec = self.workspace.read_workspace()
        decision = self.mce.make_strategic_decision(workspace_vec)

        # 3. Coherence and Ignition Monitoring
        t = np.linspace(0, 0.1, 100)
        # Simulate coherent gamma (40Hz) signals
        sig1 = np.sin(2 * np.pi * 40 * t) + 0.1 * np.random.randn(100)
        sig2 = np.sin(2 * np.pi * 40 * t + 0.05) + 0.1 * np.random.randn(100)

        self.gamma_monitor.calculate_coherence(sig1, sig2)

        # Ignition detection based on signal power envelope
        self.ignition.detect_ignition(sig1 + sig2)

        duration_ms = (time.perf_counter() - start) * 1000
        return {
            "decision": decision,
            "integrated": self.gamma_monitor.is_consciously_integrated(),
            "cycle_latency_ms": duration_ms
        }

    def cleanup(self):
        self.workspace.close()
