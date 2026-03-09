import logging
from typing import Dict, Any, List, Type, Optional
from .base import SpecializedReactor

logger = logging.getLogger(__name__)

class ReactorRegistry:
    """Central registry for all 40+ sub-reactors in the v100.0 ecosystem."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReactorRegistry, cls).__new__(cls)
            cls._instance.reactors: Dict[str, SpecializedReactor] = {}
        return cls._instance

    def register(self, reactor: SpecializedReactor):
        logger.info(f"Registry: Registering sub-reactor {reactor.registry_id}")
        self.reactors[reactor.registry_id] = reactor

    def get_reactor(self, registry_id: str) -> Optional[SpecializedReactor]:
        return self.reactors.get(registry_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": rid,
                "domain": r.domain,
                "sub_domain": r.sub_domain,
                "capabilities": r.get_capabilities()
            }
            for rid, r in self.reactors.items()
        ]
