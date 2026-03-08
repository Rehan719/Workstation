import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import os

logger = logging.getLogger(__name__)

class DigitalReactor(ABC):
    """
    ARTICLE 251/256: Base class for all domain-specific reactors.
    Provides a unified three-part structure: Incubator, Experimenter, Studio.
    """
    def __init__(self, domain: str, config: Optional[Dict[str, Any]] = None):
        self.domain = domain
        self.config = config or {}
        self.checkpoints_dir = "archive/checkpoints"
        logger.info(f"DigitalReactor: Initializing {self.domain} reactor.")

    @abstractmethod
    async def incubate(self, input_data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run iterative generation/evolution process."""
        # Derived classes must implement specific incubation logic
        return {"status": "incubating", "domain": self.domain}

    @abstractmethod
    async def interact(self, state: Any, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Real-time interaction and scenario testing."""
        # Derived classes must implement specific interaction logic
        return {"status": "interacted", "domain": self.domain}

    @abstractmethod
    async def visualize(self, data: Any, mode: str) -> Dict[str, Any]:
        """Generate interactive 2D/3D visualizations."""
        # Derived classes must implement specific visualization logic
        return {"status": "visualized", "mode": mode}

    @abstractmethod
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform deep analysis and insight generation."""
        # Derived classes must implement specific analysis logic
        return {"status": "analyzed", "domain": self.domain}

    def bundle(self, results: List[Any], bundle_type: str = "default") -> Dict[str, Any]:
        """ARTICLE 251: Package results into a structured unit (e.g., Career Launch Kit)."""
        logger.info(f"DigitalReactor: Bundling {len(results)} items into {bundle_type}.")
        return {
            "bundle_id": f"bundle_{self.domain}_{bundle_type}",
            "items": results,
            "metadata": {"domain": self.domain, "type": bundle_type}
        }

    def save_checkpoint(self, state: Any, checkpoint_id: str):
        """ARTICLE 259: Checkpointing for long-running simulations."""
        path = f"{self.checkpoints_dir}/{self.domain}/{checkpoint_id}.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'w') as f:
                json.dump(state, f)
            logger.info(f"DigitalReactor: Checkpoint saved at {path}")
            return True
        except Exception as e:
            logger.error(f"DigitalReactor: Failed to save checkpoint {checkpoint_id}: {e}")
            return False
