import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TCellRegulator:
    """
    CF-II: T-Cell Regulation.
    Distinguishes self from non-self to prevent autoimmune reactions.
    """
    def is_self(self, component_metadata: Dict[str, Any]) -> bool:
        # Check for system-internal signatures
        signature = component_metadata.get("signature", "")
        if signature.startswith("sig:v62"):
            return True
        return False

    def validate_mutation(self, mutation: Dict[str, Any]) -> bool:
        """Prevents false positives against benign mutations."""
        if mutation.get("type") == "lean_optimization":
            return True # Recognized as beneficial 'self'
        return False
