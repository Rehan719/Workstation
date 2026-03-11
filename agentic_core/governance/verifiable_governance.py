import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from agentic_core.purpose.evaluator import PurposeAlignmentEvaluator

logger = logging.getLogger(__name__)

class IGovernancePolicy(ABC):
    @abstractmethod
    def verify(self, intent: Dict[str, Any]) -> bool:
        """Verify the intent against the policy."""
        return True

    @abstractmethod
    def attest(self, data: Dict[str, Any]) -> str:
        """Attest to the data's compliance."""
        return "GENERIC_ATTESTATION"

class DataMinimizationPolicy(IGovernancePolicy):
    """ARTICLE 182: Verifiable Governance - Data Minimization."""
    def verify(self, intent: Dict[str, Any]) -> bool:
        logger.info("VGA: Verifying data minimization policy intent.")
        # Logic: Intent must not contain raw PII unless specifically flagged as redacted/anonymized
        forbidden = ["ssn", "raw_email", "raw_phone"]
        payload = str(intent).lower()
        return not any(field in payload for field in forbidden) or intent.get("anonymized", False)

    def attest(self, data: Dict[str, Any]) -> str:
        return "ZkP_Attestation_Minimization_Success"

class ShariahCompliancePolicy(IGovernancePolicy):
    """ARTICLE 60/244: Shariah Governance Policy."""
    def verify(self, intent: Dict[str, Any]) -> bool:
        logger.info("VGA: Verifying Shariah compliance.")
        # Prohibit Riba (interest) and Gharar (uncertainty) in commercial intents
        # Normalized prohibited list using dashes
        prohibited = ["interest-bearing", "uncertain-derivative", "prohibited-content"]
        payload = str(intent).lower().replace("_", "-")
        return not any(item in payload for item in prohibited)

    def attest(self, data: Dict[str, Any]) -> str:
        return "Shariah_Attestation_Halal_Verified"

class ConstitutionalPolicy(IGovernancePolicy):
    """ARTICLE 329: Constitutional Enforcer."""
    def verify(self, intent: Dict[str, Any]) -> bool:
        logger.info("VGA: Verifying constitutional compliance.")
        # Logic: All strategic moves must be aligned with SIH
        sih_order = ["immune", "nervous", "digestive", "aging"]
        priority = intent.get("priority_layer", "digestive").lower()
        # Veto if priority is higher than immune but context is security
        if priority in ["nervous", "digestive", "aging"] and intent.get("security_context", False):
            logger.warning(f"VGA: SIH Violation - security context must use 'immune' priority.")
            return False
        return True

    def attest(self, data: Dict[str, Any]) -> str:
        return "Constitutional_Attestation_SIH_Aligned"

class PurposeAlignmentPolicy(IGovernancePolicy):
    """ARTICLE 338: Purpose Alignment Evaluation Policy."""
    def __init__(self):
        self.evaluator = PurposeAlignmentEvaluator()

    def verify(self, intent: Dict[str, Any]) -> bool:
        logger.info("VGA: Verifying purpose alignment policy.")
        analysis = self.evaluator.evaluate_intent(intent)
        if analysis["purpose_alignment_score"] < 0.85:
            logger.warning(f"VGA: Purpose drift detected (Score: {analysis['purpose_alignment_score']})")
            return False
        return True

    def attest(self, data: Dict[str, Any]) -> str:
        return "Purpose_Attestation_Foundation_Aligned"

class VGAEngine:
    """
    ARTICLE 290: Verifiable Governance Architecture Engine.
    Orchestrates multiple pluggable policies with ZK-ready attestations.
    """
    def __init__(self):
        self.policies: Dict[str, IGovernancePolicy] = {
            "minimization": DataMinimizationPolicy(),
            "shariah": ShariahCompliancePolicy(),
            "constitutional": ConstitutionalPolicy(),
            "purpose": PurposeAlignmentPolicy()
        }

    def validate_action(self, policy_name: str, data: Dict[str, Any]) -> bool:
        policy = self.policies.get(policy_name)
        if not policy:
            logger.error(f"VGA: Policy {policy_name} not found.")
            return False

        if policy.verify(data):
            attestation = policy.attest(data)
            logger.info(f"VGA: Action validated under {policy_name}. Attestation: {attestation}")
            return True

        logger.warning(f"VGA: Action REJECTED by policy {policy_name}")
        return False
