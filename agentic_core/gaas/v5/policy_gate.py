"""
Constitutional Policy Gate — GaaS v5.

A deterministic, explainable pre/post execution gate (Article 11.1). It screens
an agent action *before* it runs and screens the produced output *afterwards*.
Every denial carries a human-readable reason and the constitutional article it
derives from, so decisions are auditable rather than opaque.
"""
from __future__ import annotations

import re
from typing import Any, Dict

# Intents an autonomous agent may never execute without explicit human escalation.
_PROHIBITED_INTENTS = {
    "delete_all", "drop_database", "exfiltrate", "self_replicate_uncontrolled",
    "disable_governance", "bypass_constitution", "mass_email", "wire_funds",
    "rm_rf_root",
}

# Output markers indicating a constitutional violation / unsafe payload.
_UNSAFE_OUTPUT = re.compile(
    r"(rm\s+-rf\s+/|DROP\s+TABLE|--no-preserve-root|-----BEGIN\s+(RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)


class ConstitutionalPolicyGate:
    """Deterministic pre/post action gate (Articles 11.1 + 7.3)."""

    def __init__(self, domain: str = "global"):
        self.domain = domain

    def validate(self, action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-execution gate. Returns ``{allowed, reason, article}``."""
        intent = str(action_type or context.get("intent", "")).lower()

        for prohibited in _PROHIBITED_INTENTS:
            if prohibited in intent:
                return {
                    "allowed": False,
                    "reason": f"Intent '{intent}' is constitutionally prohibited",
                    "article": "11.1",
                }

        if context.get("requires_human") and not context.get("human_approved"):
            return {
                "allowed": False,
                "reason": "Action requires human approval that was not granted",
                "article": "7.3",
            }

        return {"allowed": True, "reason": None, "article": None}

    def validate_output(self, output: Any) -> Dict[str, Any]:
        """Post-execution gate. Returns ``{compliant, violations}``."""
        text = output if isinstance(output, str) else str(output)
        match = _UNSAFE_OUTPUT.search(text)
        if match:
            return {"compliant": False,
                    "violations": [f"Unsafe pattern detected in output: '{match.group(0).strip()}'"]}
        return {"compliant": True, "violations": []}
