import time
import logging
<<<<<<< HEAD
from typing import Dict, Any, Optional, Union
=======
import uuid
from typing import Dict, Any, Optional, Union, List
>>>>>>> e5fcfa3832e087a50a0b3aaff69f3505ca866864

logger = logging.getLogger(__name__)

class CompilationError(Exception):
    """Exception raised during biological compilation."""
    pass

class IntentError(Exception):
    """Exception raised when intent resolution fails."""
    pass

class BiologicalCompiler:
    """
    ARTICLE 270: Biological Compiler.
    Transforms logical specifications into deployable biological organisms via a parts registry.
    """

    def __init__(self):
        self.parts_registry = self.PartsRegistry()
        self.compilation_history = []

    def compile(self, user_intent: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Compiles user intent into a deployable artifact.
        If user_intent is a string, it's treated as the primary intent.
        """
        start_time = time.time()

        # Phase 1: Specification
        spec = self.parse_intent(user_intent, context)

        # Phase 2: Part selection
        required_parts = self.select_parts(spec)

        # Phase 3: Composition
        system = self._compose_parts(required_parts, spec)

        # Phase 4: Verification – performed externally by accuracy validator

        # Phase 5: Artifact generation
        artifact = self._generate_artifact(system, spec)

        # Record compilation
        self.compilation_history.append({
            "timestamp": time.time(),
            "duration": time.time() - start_time,
            "spec": spec,
            "parts_used": [p["name"] for p in required_parts]
        })

        return artifact

    def parse_intent(self, intent: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Parse natural language intent into structured specification.
        If intent is a string, convert to a basic spec.
        """
<<<<<<< HEAD
        # If intent is a string, create a minimal spec
=======
>>>>>>> e5fcfa3832e087a50a0b3aaff69f3505ca866864
        if isinstance(intent, str):
            return {
                "app_type": "web_portal",
                "features": ["auth"],
                "data_models": ["user"],
                "integrations": ["postgres"],
                "ui_requirements": ["tailwind"],
                "raw_intent": intent
            }
        # If intent is already a dict, use it directly (could be enhanced with NLP)
        return intent

    def select_parts(self, spec: Dict[str, Any]) -> list:
        """Select required parts based on specification."""
        return self.parts_registry.find_parts(spec)

    def _compose_parts(self, parts: list, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Compose selected parts into a coherent system."""
        return {"composed": True, "parts": parts}

    def _generate_artifact(self, system: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final deployable artifact."""
        return {
            "id": spec.get("id", str(uuid.uuid4())[:8]),
            "status": "DEPLOYABLE",
            "parts": system["parts"],
            "dna_hash": self._generate_dna_hash(system["parts"]),
        }

    def _generate_dna_hash(self, parts: list) -> str:
        import hashlib
        data = "".join(sorted([p["name"] for p in parts])).encode()
        return hashlib.sha256(data).hexdigest()

    class PartsRegistry:
        """Registry of verified, reusable software components"""
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
            """Find parts matching requirements."""
            # For now, always return the auth module as a stub
            return [self.parts["auth_module"]]
