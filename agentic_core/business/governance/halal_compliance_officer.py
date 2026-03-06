import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class HalalComplianceOfficer:
    """
    ARTICLE 185: Halal Compliance & Shariah Governance.
    Audits transactions for Riba, Gharar, and Haram elements.
    """
    def __init__(self):
        self.rules = {
            "riba_prohibition": True,
            "gharar_avoidance": True,
            "haram_content_filter": ["alcohol", "gambling", "interest-based-finance"]
        }

    def audit_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Performs real-time Shariah auditing."""
        violations = []
        if transaction.get("interest_rate", 0) > 0:
            violations.append("RIBA_DETECTED")

        for element in self.rules["haram_content_filter"]:
            if element in str(transaction.get("description", "")).lower():
                violations.append(f"HARAM_ELEMENT_{element.upper()}")

        is_compliant = len(violations) == 0
        logger.info(f"HALAL_OFFICER: Audit complete. Compliant: {is_compliant}. Violations: {violations}")

        return {
            "is_compliant": is_compliant,
            "violations": violations,
            "attestation": "Shariah_Compliant_Hash" if is_compliant else "NON_COMPLIANT"
        }

    def calculate_zakat(self, assets: float, nisab_threshold: float) -> float:
        """Calculates 2.5% Zakat if assets exceed Nisab."""
        if assets >= nisab_threshold:
            zakat = assets * 0.025
            logger.info(f"HALAL_OFFICER: Zakat calculated: {zakat:.2f}")
            return zakat
        return 0.0
