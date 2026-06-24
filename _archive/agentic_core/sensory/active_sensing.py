import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ActiveSensingModule:
    """
    CQ-I: Active Sensing Module.
    Proactively queries for additional sensory data when uncertainty is high.
    """
    def check_uncertainty(self, perception_data: Dict[str, Any]) -> bool:
        """Determines if more data is needed."""
        confidence = perception_data.get("confidence", 1.0)

        if confidence < 0.7:
            logger.info("ACTIVE SENSING: Confidence low. Requesting additional data streams.")
            return True
        return False

    def request_data(self, modality: str):
        """Simulates a request for more sensory input."""
        logger.info(f"ACTIVE SENSING: Requesting high-fidelity {modality} scan.")
        return {"status": "request_sent", "modality": modality}
