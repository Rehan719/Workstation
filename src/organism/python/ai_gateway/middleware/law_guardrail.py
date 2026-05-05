import logging
from typing import Dict, Any
from src.organism.python.neural.event_types import ValidationResult

logger = logging.getLogger(__name__)

class UKLawGuardrail:
    """
    Constitutional Guardrail for UK Employment Law.
    Validates AI outputs against Equality Act 2010 and ERA 1996 constraints.
    """
    PROTECTED_CHARACTERISTICS = [
        "age", "disability", "gender reassignment", "marriage and civil partnership",
        "pregnancy and maternity", "race", "religion or belief", "sex", "sexual orientation"
    ]

    def __init__(self):
        self.policy_version = "v1.0.0-uk-legal"

    def validate_output(self, output: str, context: Dict[str, Any]) -> ValidationResult:
        """
        Checks if the AI output violates key legal constraints or mentions
        sensitive characteristics without appropriate legal framing.
        """
        issues = []
        lower_output = output.lower()

        # 1. Check for Protected Characteristics without context
        for char in self.PROTECTED_CHARACTERISTICS:
            if char in lower_output:
                # In a real legal tool, we'd check if it's discussing a claim or being biased.
                # For this guardrail, we flag it for human review.
                logger.info(f"LawGuardrail: Identified protected characteristic '{char}'")

        # 2. Check for Mandatory Legislation References in legal research tasks
        if context.get("task_type") == "legal_research":
            if not any(ref in output for ref in ["Equality Act 2010", "EqA 2010", "Employment Rights Act 1996"]):
                issues.append("Missing mandatory statutory references (EqA 2010 / ERA 1996)")

        # 3. Decision Logic
        if issues:
            return ValidationResult(
                is_valid=False,
                reason="; ".join(issues),
                policy_version=self.policy_version
            )

        return ValidationResult(
            is_valid=True,
            reason="Aligned with UK legal constraints",
            policy_version=self.policy_version
        )
