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
        pass

    @abstractmethod
    async def generate_artifact(self, data: Any, format: str = "pdf") -> Dict[str, Any]:
        """Produces actual production-grade artifacts (LaTeX, DOCX, etc.)."""
        pass

    def get_capabilities(self) -> List[str]:
        """Returns list of specific tasks this reactor can perform."""
        return self.config.get("capabilities", [])
