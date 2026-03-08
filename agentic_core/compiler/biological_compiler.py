import logging
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

logger = logging.getLogger(__name__)

class CompilationError(Exception):
    pass

class IntentError(Exception):
    pass

class BiologicalCompiler:
    def __init__(self):
        self.parts_registry = self.PartsRegistry()
        self.compilation_history = []

    def compile(self, user_intent: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> Dict[str, Any]:
        start_time = time.time()
        spec = self.parse_intent(user_intent, context)
        required_parts = self.select_parts(spec)
        system = self._compose_parts(required_parts, spec)
        artifact = self._generate_artifact(system, spec)
        self.compilation_history.append({
            "timestamp": time.time(),
            "duration": time.time() - start_time,
            "spec": spec,
            "parts_used": [p["name"] for p in required_parts]
        })
        return artifact

    def parse_intent(self, intent: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> Dict[str, Any]:
        if isinstance(intent, str):
            return {
                "app_type": "web_portal",
                "features": ["auth"],
                "data_models": ["user"],
                "integrations": ["postgres"],
                "ui_requirements": ["tailwind"],
                "raw_intent": intent
            }
        return intent

    def select_parts(self, spec: Dict[str, Any]) -> list:
        return self.parts_registry.find_parts(spec)

    def _compose_parts(self, parts: list, spec: Dict[str, Any]) -> Dict[str, Any]:
        return {"composed": True, "parts": parts}

    def _generate_artifact(self, system: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": spec.get("id", str(uuid.uuid4())[:8]),
            "status": "DEPLOYABLE",
            "parts": system["parts"],
            "dna_hash": self._generate_dna_hash(system["parts"]),
        }

    def _resolve_parts(self, intent: str) -> List[str]:
        resolved = []
        if "web" in intent: resolved.extend(self.parts_registry["web"])
        if "sim" in intent: resolved.extend(self.parts_registry["sim"])
        if "spiritual" in intent or "quran" in intent: resolved.extend(self.parts_registry["spiritual"])

        # Default to sim if nothing else matches (core functionality)
        if not resolved:
            resolved.extend(self.parts_registry["sim"])

    class PartsRegistry:
        def __init__(self):
            self.parts = {
                "auth_module": {
                    "name": "auth_module",
                    "type": "security",
                    "properties": {
                        "latency": "<50ms",
                        "compliance": ["GDPR", "SOC2", "HIPAA"]
                    }
                },
                "payment_processor": {
                    "name": "payment_processor",
                    "type": "integration",
                    "properties": {
                        "supported_gateways": ["stripe", "paypal"],
                        "latency": "<200ms"
                    }
                }
            }

        def find_parts(self, requirements: Dict[str, Any]) -> list:
            return [self.parts["auth_module"]]
