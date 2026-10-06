import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from agentic_core.reactor.base import DigitalReactor

logger = logging.getLogger(__name__)

class SpecializedReactor(DigitalReactor, ABC):
    """
    v100.0: Base for all hyper-specialized sub-reactors.
    Enforces truth-validation hooks and artifact generation workflows.
    """
    def __init__(self, domain: str, sub_domain: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(domain, config)
        self.sub_domain = sub_domain
        self.registry_id = f"{domain}:{sub_domain}"
        logger.info(f"SpecializedReactor: Initializing {self.registry_id}")

    @abstractmethod
    async def validate_truth(self, content: Any) -> Dict[str, Any]:
        """Domain-specific truth validation (Articles 289-292)."""

    @abstractmethod
    async def generate_artifact(self, data: Any, format: str = "pdf") -> Dict[str, Any]:
        """Produces actual production-grade artifacts (LaTeX, DOCX, etc.)."""

    def get_capabilities(self) -> List[str]:
        """Returns list of specific tasks this reactor can perform."""
        return self.config.get("capabilities", [])

    async def get_digital_twin(self, twin_id: str) -> Dict[str, Any]:
        """NOT AVAILABLE in core — and it says so rather than raising ImportError at the call.

        W597 (FU-452). This imported `EnvironmentalSimulator` from `agentic_core.simulation.engine`,
        where no such class is defined — so any caller got an ImportError naming a module rather than an
        answer. It never fired only because this method has NO CALLERS anywhere in the live tree, which
        was checked rather than assumed.

        The class it wanted is in the digital_reactor SDK, and that is a PRODUCT. Pointing a core
        ecosystem base class at a product SDK inverts the layering — core would then depend on something
        built on top of it — so the import is not simply redirected. A reactor that needs a twin should
        be given a simulator by whatever constructs it, rather than core reaching sideways for one.

        A reasoned refusal, not a silent None: a caller learns that core provisions no twin simulator and
        where one exists, instead of concluding the feature is merely missing.
        """
        return {
            "twin_id": twin_id,
            "twin": None,
            "available": False,
            "basis": (
                "No digital-twin simulator is provisioned in core. The EnvironmentalSimulator this "
                "method once imported is not defined in agentic_core.simulation.engine - that import "
                "would have raised ImportError at the call - and it lives in the digital_reactor product "
                "SDK, which core must not depend on. A reactor needing a twin should be constructed with "
                "a simulator rather than core reaching into a product for one."),
            "simulator_location": "products/digital_reactor/sdk/engine.py",
        }

    async def optimize_resources(self, user_id: str, tier: str) -> Dict[str, Any]:
        """ARTICLE 311/313: Domain-specific resource optimization."""
        from agentic_core.optimizer.engine import AdaptiveResourceOptimizer
        aro = AdaptiveResourceOptimizer()
        return aro.allocator.allocate(user_id, tier, self.domain)
