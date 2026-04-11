from abc import ABC, abstractmethod
from typing import Any, Dict, List

class AdapterInterface(ABC):
    """
    Base interface for all MJM Engine adapters.
    Ensures consistent integration pattern across the Workstation ecosystem.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the target system."""
        return True

    @abstractmethod
    def publish(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Publish data to the target system."""
        return {"status": "published", "topic": topic}

    @abstractmethod
    def subscribe(self, topic: str) -> Any:
        """Subscribe to updates from the target system."""
        return {"status": "subscribed", "topic": topic}
