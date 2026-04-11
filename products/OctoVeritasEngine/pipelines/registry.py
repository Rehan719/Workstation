import json
import os
from typing import List, Dict, Any

class PipelineRegistry:
    def __init__(self, rules_path: str = None):
        if rules_path is None:
            rules_path = os.path.join(os.path.dirname(__file__), "pipeline_rules.json")

        with open(rules_path, 'r') as f:
            self.rules = json.load(f)

        self.priority_map = {
            "lowest": 0,
            "medium": 1,
            "high": 2,
            "highest": 3,
            "variable": 1.5
        }

    def get_pipeline_priority(self, pipeline: str) -> float:
        if pipeline not in self.rules:
            return 0.0
        priority_str = self.rules[pipeline].get("injection_priority", "lowest")
        return self.priority_map.get(priority_str, 0.0)

    def is_pipeline_allowed_in_mode(self, pipeline: str, mode: str) -> bool:
        if pipeline not in self.rules:
            return False
        allowed_modes = self.rules[pipeline].get("allowed_modes", [])
        return "all" in allowed_modes or mode.lower() in [m.lower() for m in allowed_modes]

    def get_injection_modifiers(self, pipeline: str) -> List[str]:
        if pipeline not in self.rules:
            return []
        return self.rules[pipeline].get("injection_modifiers", [])

    def get_format_preferences(self, pipeline: str) -> List[str]:
        if pipeline not in self.rules:
            return []
        return self.rules[pipeline].get("format_preferences", [])

    def get_constitutional_checks(self, pipeline: str) -> List[str]:
        if pipeline not in self.rules:
            return []
        return self.rules[pipeline].get("constitutional_checks", [])
