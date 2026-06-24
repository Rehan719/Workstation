import json
import os
from typing import Dict, Any, List, Optional

class DataGovernanceModule:
    """
    Enforces cross-domain data governance and sensitivity rules.
    """
    def __init__(self, config_path: str = "configs/governance/rules.json"):
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)

        # Default rules
        return {
            "sensitive_fields": ["name", "address", "nhs_number", "id_number", "salary"],
            "cross_domain_exceptions": {
                "Science": ["Care"],
                "Care": ["Science"]
            }
        }

    def check_data_governance(self, asset_metadata: Dict[str, Any], target_domain: str) -> Dict[str, Any]:
        """
        Validates if an asset can be used in the target domain based on sensitivity.
        """
        governance = asset_metadata.get("governance", {})
        sensitive_fields = governance.get("sensitive_fields", [])
        source_domain = asset_metadata.get("domain", "Unknown")

        if not sensitive_fields:
            return {"allowed": True}

        # Check if domains are compatible for sensitive transfer
        allowed_domains = self.rules["cross_domain_exceptions"].get(source_domain, [])
        if target_domain != source_domain and target_domain not in allowed_domains:
            return {
                "allowed": False,
                "reason": f"Sensitive data transfer blocked from {source_domain} to {target_domain}.",
                "blocked_fields": sensitive_fields
            }

        return {"allowed": True}

    def sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes sensitive fields from metadata if intended for generic use.
        """
        sanitized = metadata.copy()
        for field in self.rules["sensitive_fields"]:
            if field in sanitized:
                sanitized[field] = "[REDACTED]"
        return sanitized
