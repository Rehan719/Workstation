from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from .types import TribunalTask, LegalAgent, LegalCompliance

class UKLegalPrecisionEngine(ABC):
    """Abstract interface for UK legal compliance validation."""

    @abstractmethod
    def validate(self, intent: Any, context: Any) -> LegalCompliance:
        """Validate intent against statutory and constitutional obligations."""

    @abstractmethod
    def agent_covers_statute(self, agent: LegalAgent, statute: str) -> bool:
        """Check if agent has jurisdiction/competence for specified statute."""

    @abstractmethod
    def validate_assignment(self, assignment: Dict[str, str], tasks: List[TribunalTask], agents: List[LegalAgent]) -> float:
        """Return coverage score [0.0, 1.0] for task-agent assignment."""
