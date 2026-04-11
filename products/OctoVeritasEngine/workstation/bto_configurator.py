import json
import os
from typing import Dict, Any

class BTOConfigurator:
    def __init__(self, schema_path: str = None):
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "bto_schema.json")
        self.schema_path = schema_path
        self._load_schema()

    def _load_schema(self):
        # Standard BTO Schema for Veritas Products
        schema = {
            "enabled_pipelines": ["Scraping", "Ingestion", "Knowledge", "Introspection", "Retrospection", "Extrospection", "Learning"],
            "default_mode": "jaiza",
            "csuite_overrides": {},
            "coe_requirements": ["Security", "AI Ethics"],
            "format_whitelist": ["PDF", "DOCX", "PPTX", "XLSX", "HTML", "MP4", "MP3", "PNG", "SVG"]
        }
        with open(self.schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
        self.schema = schema

    def validate_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates a user's BTO configuration against the schema.
        """
        config = self.schema.copy()
        config.update(user_config)
        # Validation logic (simplified)
        for pipeline in config.get("enabled_pipelines", []):
            if pipeline not in self.schema["enabled_pipelines"]:
                raise ValueError(f"Invalid pipeline in BTO config: {pipeline}")
        return config
