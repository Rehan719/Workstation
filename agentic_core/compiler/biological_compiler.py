import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

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
        # Registry of verified functional components
        self.parts_registry = {
            "web": ["interface_react", "api_fastapi", "db_postgres"],
            "mobile": ["interface_react_native", "api_fastapi", "db_sqlite"],
            "sim": ["core_simulation_v99", "viz_threejs", "telemetry_prometheus"],
            "spiritual": ["quran_engine", "hadith_validator", "tazkiyah_tracker"]
        }

    def compile(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles the provided specification into a functional entity package.
        """
        intent = spec.get("intent", "").lower()
        logger.info(f"BioCompiler: Compiling specification {spec.get('id', 'anonymous')} for intent: {intent}")

        if not intent:
            raise CompilationError("Compilation failed: Missing intent in specification.")

        # Resolve parts based on intent keywords
        parts = self._resolve_parts(intent)

        return {
            "id": spec.get("id", str(uuid.uuid4())[:8]),
            "status": "COMPILED",
            "intent_resolved": intent,
            "parts": parts,
            "dna_hash": self._generate_dna_hash(parts),
            "timestamp": datetime.now().isoformat()
        }

    def _resolve_parts(self, intent: str) -> List[str]:
        resolved = []
        if "web" in intent: resolved.extend(self.parts_registry["web"])
        if "sim" in intent: resolved.extend(self.parts_registry["sim"])
        if "spiritual" in intent or "quran" in intent: resolved.extend(self.parts_registry["spiritual"])

        # Default to sim if nothing else matches (core functionality)
        if not resolved:
            resolved.extend(self.parts_registry["sim"])

        return list(set(resolved)) # Deduplicate

    def _generate_dna_hash(self, parts: List[str]) -> str:
        import hashlib
        data = "".join(sorted(parts)).encode()
        return hashlib.sha256(data).hexdigest()
