import os
import json
import yaml
from datetime import datetime, timezone
from typing import Dict, Any, List

class APIRegistryManagerV83:
    """
    REGISTRY MANAGER: CROWDSOURCED API ENDPOINTS v8.3
    Manages community-sourced scraping and knowledge endpoints.
    """
    def __init__(self, registry_path: str = "knowledge/Religion/QuranEducation/community/api_registry.yaml"):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        with open(self.registry_path, "r") as f:
            return yaml.safe_load(f)

    def register_endpoint(self, endpoint_data: Dict[str, Any], contributor: str) -> Dict[str, Any]:
        """
        Register a new community-sourced API endpoint.
        """
        endpoint_id = f"quran-api-community-{len(self.registry['endpoints']) + 1:03d}"
        new_endpoint = {
            "id": endpoint_id,
            "name": endpoint_data.get("name"),
            "base_url": endpoint_data.get("base_url"),
            "endpoints": endpoint_data.get("endpoints", []),
            "validation": {
                "schema": endpoint_data.get("schema", "default_schema.json"),
                "checksum_required": True,
                "source_attribution": "required"
            },
            "community_metadata": {
                "contributed_by": contributor,
                "verified_by": [],
                "trust_score": 0.5,
                "last_verified": datetime.now(timezone.utc).date().isoformat()
            },
            "status": "pending"
        }

        self.registry["endpoints"].append(new_endpoint)
        self._save_registry()

        return new_endpoint

    def _save_registry(self):
        with open(self.registry_path, "w") as f:
            yaml.dump(self.registry, f, sort_keys=False)

    def verify_endpoint(self, endpoint_id: str, scholar_id: str) -> Dict[str, Any]:
        """
        Verify a community endpoint through scholar network review.
        """
        for endpoint in self.registry["endpoints"]:
            if endpoint["id"] == endpoint_id:
                endpoint["status"] = "approved"
                endpoint["community_metadata"]["verified_by"].append(scholar_id)
                endpoint["community_metadata"]["trust_score"] += 0.1
                endpoint["community_metadata"]["last_verified"] = datetime.now(timezone.utc).date().isoformat()
                self._save_registry()
                return endpoint
        return {"error": "Endpoint not found"}

    def get_discovery_endpoints(self) -> List[Dict[str, Any]]:
        """
        Return list of approved discovery endpoints for scraping pipeline.
        """
        return [e for e in self.registry["endpoints"] if e["status"] == "approved"]
