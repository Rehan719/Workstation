from typing import Any, Dict, List

import numpy as np

from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.legal.types import LegalAgent, LegalCompliance, TribunalTask


class LegalPrecisionMinimiser:
    """
    Harden L4 Regulation: Non-negotiable Legal Precision.
    Ensures infinite-cost masking for non-compliant intents in UK jurisdiction.
    Hard-coded verification for EqA 2010 s.13/s.20, ERA 1996 s.98, ACAS Code para 4, and GDPR/DPA 2018.
    """

    def __init__(self):
        self.engine = UKLegalPrecisionEngineImpl(
            rules_path="configs/legal_precision.yaml"
        )

    def check_compliance(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public interface for GaaS v4 to check intent compliance.
        Enforces 100% legal coverage as a hard constraint.
        """
        context = {
            "jurisdiction": "UK",
            "required_statutes": intent.get(
                "required_statutes", ["EqualityAct2010", "ERA1996", "ACASCode", "GDPR"]
            ),
        }
        compliance: LegalCompliance = self.engine.validate(intent, context)

        # Hardening: Manual check for specific critical sections if domain is legal
        if intent.get("domain") == "legal" and compliance.is_compliant:
            if not self._manual_hardening_check(intent):
                return {
                    "compliant": False,
                    "coverage_score": 0.0,
                    "violations": ["HARDENING_CHECK_FAILURE"],
                }

        return {
            "compliant": compliance.is_compliant,
            "coverage_score": compliance.coverage_score,
            "violations": compliance.violations,
            "audit_hash": compliance.audit_hash,
        }

    def _manual_hardening_check(self, intent: Dict[str, Any]) -> bool:
        """
        Hard-coded verification for mandatory UK Employment Law sections.
        """
        flags = intent.get("potential_flags", [])

        # GDPR / DPA 2018 check
        if "personal_data_breach" in flags or "unauthorized_processing" in flags:
            return False

        # Specific Employment Law Protections
        # Equality Act 2010 s.13 (Direct Discrimination) & s.20 (Duty to make adjustments)
        if "direct_discrimination" in flags or "failure_to_adjust" in flags:
            return False

        # ERA 1996 s.98 (Unfair Dismissal)
        if "unfair_procedural_dismissal" in flags:
            return False

        # ACAS Code para 4 (Principles for disciplinary and grievance)
        if "acas_procedural_breach" in flags:
            return False

        return True

    def apply_hard_constraint(
        self,
        cost_matrix: np.ndarray,
        tasks: List[TribunalTask],
        agents: List[LegalAgent],
    ) -> np.ndarray:
        """
        Mask cost matrix with INF where legal coverage < 1.0.
        Specifically hardened for 'uk_employment'.
        """
        hardened_matrix = cost_matrix.copy()
        for i, task in enumerate(tasks):
            for j, agent in enumerate(agents):
                if not self._verify_statute_compliance(task, agent):
                    hardened_matrix[i, j] = float("inf")
        return hardened_matrix

    def _verify_statute_compliance(self, task: TribunalTask, agent: LegalAgent) -> bool:
        """Deep check for requested sections (EqA s.13, s.20; ERA s.98; ACAS para 4; GDPR)."""
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

        if "gdpr" in statute or "dpa2018" in statute:
            if "data_protection" not in agent.competencies:
                return False

        return True

    def validate_and_reject(
        self,
        assignment: Dict[str, str],
        tasks: List[TribunalTask],
        agents: List[LegalAgent],
    ) -> bool:
        """Reject any assignment that does not reach 100% legal coverage."""
        coverage = self.engine.validate_assignment(assignment, tasks, agents)
        if coverage < 1.0:
            return False
        return True
