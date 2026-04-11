import logging
import yaml
import os
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class GenomeManager:
    """
    Handles domain genome loading, inheritance, and validation.
    """
    def __init__(self, genomes_dir: str = "config/domains"):
        self.genomes_dir = genomes_dir
        self.base_genome = self._load_file("base_schema.yaml")

    def _load_file(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.genomes_dir, filename)
        if not os.path.exists(filepath):
            logger.warning(f"Genome file not found: {filepath}")
            return {}
        with open(filepath, "r") as f:
            return yaml.safe_load(f)

    def get_domain_config(self, domain_id: str) -> Dict[str, Any]:
        """Loads domain genome with inheritance and validation."""
        filename = f"{domain_id}.yaml"
        config = self._load_file(filename)

        if not config:
            return self.base_genome

        final_config = {}
        if "extends" in config:
            parent = self.get_domain_config(config["extends"])
            final_config = self._deep_merge(parent, config)
        else:
            final_config = self._deep_merge(self.base_genome, config)

        # Basic validation could be added here if we had a JSON schema for the genome itself
        return final_config

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def validate_evidence(self, domain_id: str, evidence_data: Dict[str, Any]) -> bool:
        """Validates evidence against the domain's schema."""
        config = self.get_domain_config(domain_id)
        schema = config.get("mushahida", {}).get("evidence_schema")
        if not schema:
            return True
        try:
            validate(instance=evidence_data, schema=schema)
            return True
        except ValidationError as e:
            logger.error(f"Evidence validation failed: {e.message}")
            return False
