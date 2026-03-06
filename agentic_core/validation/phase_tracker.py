import logging
import time

logger = logging.getLogger(__name__)

class PhaseTracker:
    """
    DF: Hierarchical Implementation Blueprint Tracker.
    Enforces the 6-phase sequence.
    """
    PHASES = [
        "1: Molecular Triad",
        "2: Global Workspace",
        "3: Genomic Registry",
        "4: Decentralized Governance",
        "5: Neuromorphic Interface",
        "6: System Integration"
    ]

    def __init__(self):
        self.current_phase_index = 0
        self.completion_log = {}

    def mark_phase_complete(self, phase_name: str):
        if phase_name in self.PHASES[self.current_phase_index]:
             self.completion_log[phase_name] = time.time()
             self.current_phase_index += 1
             logger.info(f"ROADMAP: Phase {phase_name} complete. Moving to {self.PHASES[self.current_phase_index] if self.current_phase_index < len(self.PHASES) else 'FINISHED'}")
        else:
             logger.warning(f"ROADMAP: Out-of-order completion attempted for {phase_name}.")

    def get_progress(self) -> float:
        return (self.current_phase_index / len(self.PHASES)) * 100.0
