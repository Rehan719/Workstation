import hashlib
import time
import json
from enum import Enum
from typing import List, Dict, Any, Optional

class TruthDimension(Enum):
    I_OBJECTIVE_RECORD = "I"
    II_SUBJECTIVE_NARRATIVE = "II"
    III_PROCEDURAL = "III"
    IV_TEMPORAL_DYNAMIC = "IV"
    V_PREDICTIVE = "V"
    VI_SYSTEMIC_ETHICAL = "VI"
    VII_INTEGRATIVE = "VII"
    VIII_SOVEREIGN_MULTIMODAL = "VIII"
    IX_OPERATIONAL_CONVERGENCE = "IX"
    X_ADAPTIVE_CONSTITUTIONAL = "X"

class TruthEngine:
    """
    Deca-Veritas Truth Engine (v3.0).
    Enforces and tracks all 10 dimensions of truth across the intelligence fabric.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.applied_dimensions = []

    def apply_dimension(self, dimension: TruthDimension, metadata: Dict[str, Any] = None):
        """Records the application of a specific truth dimension."""
        # Check if the dimension is enabled in the config
        # Dimension keys in config can be like "I_objective_record"
        dim_key = [k for k in self.config.keys() if k.startswith(dimension.name) or k.startswith(dimension.value + "_")]

        is_enabled = False
        if dim_key:
            is_enabled = self.config.get(dim_key[0], {}).get("enabled", False)

        if is_enabled:
            self.applied_dimensions.append({
                "dimension": dimension.value,
                "name": dimension.name,
                "timestamp": time.time(),
                "metadata": metadata or {}
            })
            return True
        return False

    def generate_report(self) -> Dict[str, Any]:
        """Generates a summary of all truth dimensions applied."""
        return {
            "version": "10.0.0",
            "dimensions_applied": [d["name"] for d in self.applied_dimensions],
            "agent_telemetry_enabled": self.config.get("X_adaptive_constitutional", {}).get("agent_telemetry", False),
            "audit_trail": self.applied_dimensions,
            "integrity_hash": self._calculate_integrity_hash()
        }

    def _calculate_integrity_hash(self) -> str:
        data = json.dumps(self.applied_dimensions, sort_keys=True)
        return hashlib.sha3_512(data.encode()).hexdigest()
