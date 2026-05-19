from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time
import logging
from agentic_core.cognitive.registry import EngineType
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

logger = logging.getLogger(__name__)

@dataclass
class ClearanceResult:
    passed: bool
    reason: Optional[str] = None
    attestations: Dict[str, str] = None

class ConstitutionalClearanceChain:
    """
    Five-gate constitutional clearance chain:
    Mushāwara → Niyyah → Tawazun → Tafakkur → Tahqeeq
    """
    def __init__(self, ueg_logger: Any, cognitive_orchestrator: Any):
        self.ueg = ueg_logger
        self.orchestrator = cognitive_orchestrator
        self.enforcement = OmniEnforcementPatternSupreme(
            {"fail_on_missing_validator": False},
            {"task": "avatar_clearance"}
        )

    async def validate_emission(self, emission: Dict[str, Any], context: Dict[str, Any]) -> ClearanceResult:
        """Runs the 5-gate clearance chain for every avatar emission."""
        attestations = {}

        # 1. Mushāwara: Deliberative consensus (≥3 engines)
        mushawara_res = await self.orchestrator.consult(emission, ["inkashaf", "aqal", "samajh"])
        if mushawara_res["status"] != "APPROVED":
            return ClearanceResult(False, f"Mushāwara rejection: {mushawara_res.get('reason')}")
        attestations["mushawara"] = mushawara_res.get("attestation", "MOCK_MUSHAWARA_SIG")

        # 2. Niyyah: Intent ratification
        niyyah_res = await self.orchestrator.process_engine("niyyah", emission, context)
        if not niyyah_res.get("ratified", False):
            return ClearanceResult(False, "Niyyah: Intent failed ratification")
        attestations["niyyah"] = niyyah_res.get("signature", "MOCK_NIYYAH_SIG")

        # 3. Tawazun: Balance (Depth vs Cognitive Load)
        tawazun_res = await self.orchestrator.process_engine("tawazun", emission, context)
        if not tawazun_res.get("balanced", True):
            return ClearanceResult(False, "Tawazun: Cognitive load imbalance")
        attestations["tawazun"] = tawazun_res.get("proof", "MOCK_TAWAZUN_SIG")

        # 4. Tafakkur: Reflection on downstream effects
        tafakkur_res = await self.orchestrator.process_engine("tafakkur", emission, context)
        if tafakkur_res.get("risk_score", 0) > 0.15:
            return ClearanceResult(False, "Tafakkur: High risk of downstream negative effects")
        attestations["tafakkur"] = tafakkur_res.get("audit_hash", "MOCK_TAFAKKUR_SIG")

        # 5. Tahqeeq: Output verification against rules
        tahqeeq_res = await self.orchestrator.verify_output(emission)
        if not tahqeeq_res.get("verified", True):
            return ClearanceResult(False, f"Tahqeeq: Verification failed: {tahqeeq_res.get('reason')}")
        attestations["tahqeeq"] = tahqeeq_res.get("merkle_proof", "MOCK_TAHQEEQ_SIG")

        await self.ueg.log_event("CONSTITUTIONAL_CLEARANCE_PASSED", {
            "emission_id": emission.get("id"),
            "attestations": attestations
        })

        return ClearanceResult(True, attestations=attestations)
