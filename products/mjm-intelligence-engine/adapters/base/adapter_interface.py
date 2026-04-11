from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
import asyncio

@dataclass
class AdapterContext:
    ecosystem_config: Dict[str, Any]
    security_credentials: Dict[str, str]
    feature_flags: Dict[str, bool]

@dataclass
class RegistrationReceipt:
    adapter_id: str
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    capabilities: List[str] = field(default_factory=list)

@dataclass
class SovereignEvent:
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class QuerySpecification:
    query_type: str
    parameters: Dict[str, Any]

class BaseAdapter(ABC):
    """
    Universal interface for all MJM ecosystem adapters.
    """

    def __init__(self, adapter_id: str, config: Dict[str, Any] = None):
        self.adapter_id = adapter_id
        self.config = config or {}
        self.status = "DISCONNECTED"

    @abstractmethod
    async def register(self, context: AdapterContext) -> RegistrationReceipt:
        pass

    @abstractmethod
    async def publish(self, event: SovereignEvent) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def query(self, spec: QuerySpecification) -> Any:
        pass
