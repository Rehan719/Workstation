import logging
import uuid
import json
import yaml
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class RALVerifier:
    """
    ARTICLE 319: Resource Assembly Language (RAL).
    Declarative verification for resource requests (JSON/YAML support).
    Translates high-level specs into fabric-compatible requirements.
    """
    def __init__(self, fabric: Optional[Any] = None):
        from .fabric import DynamicResourceFabric
        self.fabric = fabric or DynamicResourceFabric()

    def parse(self, content: str) -> Dict[str, Any]:
        """Parses RAL content (detects JSON or YAML)."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                return yaml.safe_load(content)
            except yaml.YAMLError:
                raise ValueError("Invalid RAL format: Must be JSON or YAML")

    def verify_request(self, raw_request: str) -> Dict[str, Any]:
        """
        Verifies request against fabric inventory and security boundaries.
        """
        try:
            request = self.parse(raw_request)
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

        # Schema Validation
        required = ["id", "domain", "requirements"]
        for key in required:
            if key not in request:
                return {"status": "ERROR", "message": f"Missing key: {key}"}

        reqs = request["requirements"]

        # Security boundaries (Article 313: Domain-specific optimization)
        # Prevent excessive resource requests in free tier (implicitly enforced by fabric capacity)

        inventory = self.fabric.get_inventory_status()

        # Translation: "8 CPU cores" -> {"compute": 8}
        translated_reqs = {}
        for k, v in reqs.items():
            if "CPU" in k.upper():
                translated_reqs["compute"] = v
            elif "RAM" in k.upper() or "MEMORY" in k.upper():
                translated_reqs["memory"] = v
            elif "GPU" in k.upper():
                translated_reqs["gpu"] = v
            else:
                translated_reqs[k] = v

        for res, amount in translated_reqs.items():
            if res not in inventory:
                return {"status": "ERROR", "message": f"Unknown resource type: {res}"}
            if inventory[res]["available"] < amount:
                return {"status": "REJECTED", "message": f"Insufficient {res}"}

        return {
            "status": "VERIFIED",
            "request_id": request["id"],
            "translated_requirements": translated_reqs
        }
