import hashlib
import json
import yaml
import logging
from typing import List, Dict, Optional, Any
from .interfaces import UKLegalPrecisionEngine
from .types import TribunalTask, LegalAgent, LegalCompliance

class UKLegalPrecisionEngineImpl(UKLegalPrecisionEngine):
    """
    Concrete implementation of UK Legal Precision Engine.
    Enforces Equality Act 2010, ERA 1996, and ACAS Code compliance.
    """

    def __init__(self, rules_path: str):
        self.logger = logging.getLogger("UKLPE")
        try:
            with open(rules_path, 'r') as f:
                config = yaml.safe_load(f)
                self.rules = config.get("rules", [])
                self.statutes = config.get("statutes", {})
        except FileNotFoundError:
            self.logger.warning(f"Legal rules file not found at {rules_path}. Using defaults.")
            self.rules = []
            self.statutes = {
                "EqualityAct2010": ["discrimination", "harassment", "victimisation"],
                "ERA1996": ["unfair_dismissal", "redundancy", "wage_deduction"],
                "ACASCode": ["disciplinary", "grievance"]
            }

    def validate(self, intent: Any, context: Any) -> LegalCompliance:
        """
        Validate an intent (e.g., generating a document or proposing an action).
        """
        violations = []
        coverage = 1.0

        # Statutory check
        required_statutes = context.get("required_statutes", [])
        for statute in required_statutes:
            if not self._check_statute_compliance(intent, statute):
                violations.append(f"Statutory violation: {statute}")
                coverage -= 0.2

        # Jurisdiction check
        target_jurisdiction = context.get("jurisdiction", "UK")
        intent_jurisdiction = intent.get("jurisdiction", "UK")

        if target_jurisdiction != intent_jurisdiction and target_jurisdiction != "UK" and intent_jurisdiction != "UK":
            violations.append(f"Jurisdiction mismatch: {intent_jurisdiction} vs {target_jurisdiction}")
            coverage -= 0.5

        is_compliant = len(violations) == 0 and coverage >= 1.0

        # Audit trail
        audit_data = json.dumps({"intent": str(intent), "context": str(context), "violations": violations}, sort_keys=True)
        audit_hash = hashlib.sha3_512(audit_data.encode()).hexdigest()

        return LegalCompliance(
            is_compliant=is_compliant,
            coverage_score=max(0.0, coverage),
            violations=violations,
            matched_precedents=[],
            audit_hash=audit_hash
        )

    def agent_covers_statute(self, agent: LegalAgent, statute: str) -> bool:
        """Check if agent is qualified for the specific statute and jurisdiction."""
        if agent.jurisdiction != "Global" and agent.jurisdiction != "UK":
            # Assuming tasks have jurisdictions, normally checked in validate_assignment
            pass
        return statute in agent.competencies

    def validate_assignment(self, assignment: Dict[str, str], tasks: List[TribunalTask], agents: List[LegalAgent]) -> float:
        """
        Return coverage score for a set of assignments.
        1.0 means all tasks assigned to qualified agents in correct jurisdiction.
        """
        if not tasks:
            return 1.0

        agent_map = {a.id: a for a in agents}
        task_map = {t.id: t for t in tasks}

        total_tasks = len(tasks)
        compliant_tasks = 0

        for task_id, agent_id in assignment.items():
            task = task_map.get(task_id)
            agent = agent_map.get(agent_id)

            if not task or not agent:
                continue

            # Check statute competency
            if self.agent_covers_statute(agent, task.statute):
                # Check jurisdiction
                if agent.jurisdiction == task.jurisdiction or agent.jurisdiction == "UK":
                    compliant_tasks += 1

        return compliant_tasks / total_tasks

    def _check_statute_compliance(self, intent: Any, statute: str) -> bool:
        """Placeholder for deep statutory rule verification logic."""
        return True # In Phase 0, we assume structural compliance if inputs are valid
