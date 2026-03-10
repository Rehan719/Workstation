import logging
from typing import Dict, Any, List, Optional
import json

logger = logging.getLogger(__name__)

class RALVerifier:
    """
    ARTICLE 319: Resource Assembly Language (RAL).
    Declarative verification for resource requests.
    """
    def __init__(self, fabric: Optional[Any] = None):
        from .fabric import DynamicResourceFabric
        self.fabric = fabric or DynamicResourceFabric()

    def verify_request(self, request_json: str) -> Dict[str, Any]:
        try:
            request = json.loads(request_json)
        except json.JSONDecodeError:
            return {"status": "ERROR", "message": "Invalid JSON in RAL request"}

        logger.info(f"RAL: Verifying request: {request}")

        # Declarative schema check
        required_keys = ["id", "domain", "requirements"]
        for key in required_keys:
            if key not in request:
                return {"status": "ERROR", "message": f"Missing key: {key}"}

        # Check inventory via fabric
        inventory = self.fabric.get_inventory_status()
        requirements = request["requirements"]

        for res, amount in requirements.items():
            if res not in inventory:
                return {"status": "ERROR", "message": f"Unknown resource type: {res}"}
            if inventory[res]["available"] < amount:
                return {"status": "REJECTED", "message": f"Insufficient {res}"}

        return {"status": "VERIFIED", "request_id": request["id"]}

    def compile_request(self, request: Dict[str, Any]) -> str:
        """Converts internal spec into RAL JSON."""
        return json.dumps(request)
