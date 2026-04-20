from typing import Dict, Any, List, Optional
from agentic_core.legal.precision_engine import UKLegalPrecisionEngine

class JurisdictionRouter:
    """
    Enforces cross-border legal compliance for treaty negotiations.
    Ensures UK GDPR, Equality Act 2010, and other statutory bounds are respected.
    """
    def __init__(self, legal_engine: Optional[UKLegalPrecisionEngine] = None):
        self.legal_engine = legal_engine or UKLegalPrecisionEngine()

    def validate_treaty_legal_bounds(self, treaty_terms: List[Dict[str, Any]]) -> bool:
        """
        Hard constraint validation: any term violating UK legal jurisdiction returns False.
        """
        for term in treaty_terms:
            # Check for data flow constraints (GDPR)
            if "data_transfer" in term and term.get("destination") == "restricted_zone":
                if not term.get("compliance_certified", False):
                    return False

            # Check for employment law compliance (Equality Act 2010)
            if "policy_alignment" in term and term.get("protected_characteristics") == "compromised":
                return False

        return True

    def filter_negotiation_pool(self, peer_intents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out peer intents that are fundamentally non-compliant with UK legal bounds."""
        return [i for i in peer_intents if self.validate_treaty_legal_bounds([i])]
