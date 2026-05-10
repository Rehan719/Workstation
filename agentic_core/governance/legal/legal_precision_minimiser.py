import numpy as np
from typing import Dict, Any, List, Optional
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl

class LegalPrecisionMinimiser:
    """
    Harden L4 Regulation: Non-negotiable Legal Precision.
    Ensures infinite-cost masking for non-compliant intents in UK jurisdiction.
    Hard-coded verification for EqA 2010 s.13/s.20, ERA 1996 s.98, and ACAS Code para 4.
    """
    def __init__(self):
        self.engine = UKLegalPrecisionEngineImpl(rules_path="configs/legal_precision.yaml")

    def apply_hard_constraint(self, cost_matrix: np.ndarray, tasks: List[TribunalTask], agents: List[LegalAgent]) -> np.ndarray:
        """
        Mask cost matrix with INF where legal coverage < 1.0.
        Specifically hardened for 'uk_employment'.
        """
        hardened_matrix = cost_matrix.copy()
        for i, task in enumerate(tasks):
            for j, agent in enumerate(agents):
                # Verify Specific Statutes (Hardening)
                if not self._verify_statute_compliance(task, agent):
                    hardened_matrix[i, j] = float('inf')
        return hardened_matrix

    def _verify_statute_compliance(self, task: TribunalTask, agent: LegalAgent) -> bool:
        """Deep check for requested sections (EqA s.13, s.20; ERA s.98; ACAS para 4)."""
        # 1. General competence check
        if not self.engine.agent_covers_statute(agent, task.statute):
            return False

        # 2. Specific Section Enforcement
        statute = task.statute.lower()
        if "equalityact2010" in statute or "eqa2010" in statute:
             # Must have disability adjustment (s.20) and non-disc (s.13) competence
             required = ["s.13", "s.20"]
             if not all(r in agent.competencies for r in required):
                 return False

        if "era1996" in statute:
             if "s.98" not in agent.competencies:
                 return False

        if "acas" in statute:
             if "para4" not in agent.competencies:
                 return False

        return True

    def validate_and_reject(self, assignment: Dict[str, str], tasks: List[TribunalTask], agents: List[LegalAgent]) -> bool:
        """Reject any assignment that does not reach 100% legal coverage."""
        coverage = self.engine.validate_assignment(assignment, tasks, agents)
        if coverage < 1.0:
            return False
        return True
