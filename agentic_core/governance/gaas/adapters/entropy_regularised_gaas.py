import logging
from typing import Dict, Any, Optional, List

# torch is an optional heavy ML dependency — not required for the FastAPI
# deployment environment. The EntropyRegularisedGaaS class uses torch tensors
# internally but is not wired into any of the 32 mounted API routers.
# Guard the import so the package remains importable without torch installed.
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False
    torch = None  # type: ignore

from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl

try:
    from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
except ImportError:
    OptimalTransportRouter = None  # type: ignore

class EntropyRegularisedGaaS:
    """
    Adapter for GaaSValidatorV4 adding entropy-regularised validation and legal precision gates.
    Implements the Ω-Functional logic at the regulation layer (L1-L3).
    """

    def __init__(
        self,
        base_validator: GaaSValidatorV4,
        legal_engine: UKLegalPrecisionEngineImpl,
        ot_solver=None
    ):
        self.base = base_validator
        self.legal_engine = legal_engine
        if OptimalTransportRouter is not None:
            self.ot = ot_solver or OptimalTransportRouter(epsilon=0.01)
        else:
            self.ot = None
        self.logger = logging.getLogger("EntropyRegularisedGaaS")
        # Constitutional articles represented as a distribution over intent space
        if _TORCH_AVAILABLE:
            self.const_embs = torch.ones(10) / 10.0  # type: ignore
        else:
            self.const_embs = [0.1] * 10

    async def validate_intent(self, intent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gated constitutional audit with minimisation constraints.
        """
        # 1. Run base constitutional validation
        base_result = await self.base.validate_intent(intent, context)

        # 2. Legal Precision Gate (Non-negotiable for legal domains)
        is_legal = context.get("layer") == "L12_Policy" or context.get("domain") == "legal"
        legal_coverage = 1.0

        if is_legal:
            # For testing: ensure we use context's jurisdiction if provided
            legal_context = context.copy()
            legal_result = self.legal_engine.validate(intent, legal_context)
            legal_coverage = legal_result.coverage_score

            if not legal_result.is_compliant:
                self.logger.error(f"Legal Precision Violation: {legal_result.violations}")
                return {
                    "passed": False,
                    "blocked": True,
                    "reason": "LEGAL_PRECISION_VIOLATION",
                    "violations": legal_result.violations,
                    "legal_coverage": legal_coverage,
                    "merkle_root": base_result.get("merkle_root")
                }

        # 3. Entropy-Regularised Constitutional Validation via OT
        # Compute "transport cost" from intent to constitutional baseline
        intent_profile = torch.tensor(intent.get("profile", [0.1]*10), dtype=torch.float32)
        cost_matrix = self._compute_semantic_cost(intent_profile)

        # Solve OT for minimal transport cost (constitutional surprise)
        _, transport_cost, _ = self.ot.solve(
            source=intent_profile,
            target=self.const_embs,
            cost_matrix=cost_matrix
        )

        entropy_threshold = context.get("entropy_threshold", 0.5)

        if transport_cost > entropy_threshold:
            self.logger.warning(f"Entropy threshold exceeded: {transport_cost:.4f} > {entropy_threshold}")
            # Suggest minimal-compliant intent (gradient descent step towards constitution)
            suggested_profile = self._suggest_compliant_profile(intent_profile)

            # If transport cost is too high, we block or flag for MultiSig
            if transport_cost > entropy_threshold * 2:
                return {
                    "passed": False,
                    "blocked": False, # Flagged
                    "reason": "ENTROPY_THRESHOLD_EXCEEDED",
                    "transport_cost": transport_cost,
                    "suggested_profile": suggested_profile.tolist(),
                    "merkle_root": base_result.get("merkle_root")
                }

        # Merge results
        final_result = base_result.copy()
        final_result.update({
            "legal_coverage": legal_coverage,
            "transport_cost": transport_cost,
            "minimisation_validated": True,
            "passed": base_result["passed"] and legal_coverage == 1.0
        })

        return final_result

    def _compute_semantic_cost(self, profile: torch.Tensor) -> torch.Tensor:
        """Heuristic semantic distance between intent profile and constitutional articles."""
        # Cost is distance in intent-profile space
        n = profile.shape[0]
        m = self.const_embs.shape[0]
        # Outer subtraction squared
        C = (profile.unsqueeze(1) - self.const_embs.unsqueeze(0))**2
        return C

    def _suggest_compliant_profile(self, current: torch.Tensor) -> torch.Tensor:
        """Perform a single gradient descent step towards the constitutional baseline."""
        lr = 0.1
        # Simple step towards uniform constitution
        return current + lr * (self.const_embs - current)
