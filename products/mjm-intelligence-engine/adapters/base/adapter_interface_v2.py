from abc import ABC, abstractmethod
from typing import Any, Dict, List, AsyncIterator, Callable

class BaseAdapterV2(ABC):
    """
    Enhanced universal interface for all MJM ecosystem adapters in v2.0.
    Supports streaming and meta-cognitive context propagation.
    """

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def publish(self, topic: str, payload: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def stream_query(self, query_spec: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Yields results in chunks for efficiency."""
        yield {"chunk": "default"}

    @abstractmethod
    async def receive_meta_context(self, context: Dict[str, Any]):
        """Accepts meta-cognitive strategy alignment data."""
        pass
