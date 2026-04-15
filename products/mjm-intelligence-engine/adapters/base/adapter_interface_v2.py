from abc import ABC, abstractmethod
from typing import Any, Dict, List, AsyncIterator, Callable

class BaseAdapterV2(ABC):
    """
    Enhanced universal interface for all MJM ecosystem adapters in v2.0.
    Supports streaming and meta-cognitive context propagation.
    """

    @abstractmethod
    async def connect(self) -> bool:
        """Establishes connection to the adapter's backend."""
        return True

    @abstractmethod
    async def publish(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Publishes a payload to a specific ecosystem topic."""
        return {"status": "published", "topic": topic}

    @abstractmethod
    async def stream_query(self, query_spec: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Yields results in chunks for efficiency."""
        yield {"chunk": "adapter_base_v2_stream_active"}

    @abstractmethod
    async def receive_meta_context(self, context: Dict[str, Any]):
        """Accepts meta-cognitive strategy alignment data."""
        return {"context_ingested": True}
