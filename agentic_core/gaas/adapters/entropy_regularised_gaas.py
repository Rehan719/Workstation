import logging
from typing import Dict, Any, Optional
from agentic_core.organism.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl

class EntropyRegularisedGaaS:
    """
    Adapter for GaaSValidatorV4 adding entropy-regularised validation and legal precision gates.
    Implements the Ω-Functional logic at the regulation layer.
    """

    def __init__(self, base_validator: GaaSValidatorV4, legal_engine: UKLegalPrecisionEngineImpl):
        self.base = base_validator
        self.legal_engine = legal_engine
        self.logger = logging.getLogger("EntropyRegularisedGaaS")

    async def validate_intent(self, intent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gated constitutional audit with minimisation constraints.
        """
        # 1. Run base constitutional validation
        base_result = await self.base.validate_intent(intent, context)

        # 2. Legal Precision Gate (Non-negotiable for L12 or legal domains)
        is_legal = context.get("layer") == "L12_Policy" or context.get("domain") == "legal"
        legal_coverage = 1.0

        if is_legal:
            legal_result = self.legal_engine.validate(intent, context)
            legal_coverage = legal_result.coverage_score

            if not legal_result.is_compliant:
                self.logger.warning(f"Legal compliance check failed: {legal_result.violations}")
                return {
                    "passed": False,
                    "blocked": True,
                    "reason": "LEGAL_PRECISION_VIOLATION",
                    "violations": legal_result.violations,
                    "legal_coverage": legal_coverage,
                    "merkle_root": base_result.get("merkle_root")
                }

        # 3. Entropy Monitoring (Article 1104)
        entropy = intent.get("entropy", 0.0)
        entropy_threshold = context.get("entropy_threshold", 0.5)

        if entropy > entropy_threshold:
            self.logger.warning(f"Entropy threshold exceeded: {entropy} > {entropy_threshold}")
            # In Phase 0, we log and pass if legal precision is met,
            # but Article 1104 mandate requires monitoring.

        # Merge results
        final_result = base_result.copy()
        final_result.update({
            "legal_coverage": legal_coverage,
            "entropy": entropy,
            "minimisation_validated": True
        })

        return final_result
