import hashlib
import json
import logging
from typing import Any, Dict

import yaml

from agentic_core.consultation.interface import ConsultationRequest
from agentic_core.governance.legal.legal_precision_minimiser import (
    LegalPrecisionMinimiser,
)


class GaaSValidatorV4:
    """
    IDBO Layer 4: Regulation (Epigenetic State).
    Enforces UK Legal Precision and Constitutional GaaS Intercepts.
    Now extended for Mushawara Consultation validation.
    """

    def __init__(self, genome_path: str, legal_path: str):
        self.logger = logging.getLogger("GaaS_v4")
        with open(genome_path, "r") as f:
            self.genome = yaml.safe_load(f)
        with open(legal_path, "r") as f:
            self.legal_rules = yaml.safe_load(f).get("rules", [])
        self.merkle_root = "0" * 64
        self.legal_minimiser = LegalPrecisionMinimiser()

    async def validate_intent(
        self, intent: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gated constitutional audit of agent intent.
        """
        self.logger.info(f"GaaS: Auditing intent '{intent.get('type')}'")

        # 1. Statutory Rule Matching
        violations = []
        for rule in self.legal_rules:
            if rule["id"] in intent.get("potential_flags", []):
                violations.append(rule)

        # 2. Truth Dimension Scoring
        min_conf = self.genome.get("gaas_v4_config", {}).get(
            "min_confidence_score", 0.9
        )
        intent_conf = intent.get("confidence", 0.95)

        blocked = any(v.get("enforcement_action") == "block" for v in violations)

        # 3. Legal Precision Integration
        if context.get("domain") == "legal" or intent.get("domain") == "legal":
            legal_compliance = self.legal_minimiser.check_compliance(intent)
            if not legal_compliance.get("compliant", False):
                blocked = True
                violations.append(
                    {"id": "LEGAL_PRECISION_FAILURE", "enforcement_action": "block"}
                )

        passed = (intent_conf >= min_conf) and not blocked

        # 4. Merkle DAG Update
        self._update_merkle_dag(intent, passed)

        return {
            "passed": passed,
            "blocked": blocked,
            "violations": [
                v if isinstance(v, str) else v.get("id") for v in violations
            ],
            "merkle_root": self.merkle_root,
        }

    async def validate_consultation(
        self, request: ConsultationRequest
    ) -> Dict[str, Any]:
        """
        Specifically validates a Mushawara Consultation Request.
        """
        intent = {
            "type": "consultation_request",
            "engine": request.engine,
            "query": request.query,
            "domain": request.domain,
            "confidence": 1.0,  # Request itself is high confidence
        }
        return await self.validate_intent(intent, request.context)

    def _update_merkle_dag(self, intent: Dict, passed: bool):
        payload = json.dumps({"intent": intent, "result": passed}, sort_keys=True)
        new_hash = hashlib.sha3_512(
            payload.encode() + self.merkle_root.encode()
        ).hexdigest()
        self.merkle_root = new_hash
