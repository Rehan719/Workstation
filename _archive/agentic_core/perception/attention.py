import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CrossModalAttention:
    """
    CI-II: Cross-Modal Attention Mechanism.
    Dynamically allocates perceptual resources based on salience.
    """
    def allocate_attention(self, active_streams: List[Dict[str, Any]]) -> str:
        """Prioritizes the most salient signal."""
        # Simulated salience: prioritize audition if transcript found, else vision
        for stream in active_streams:
            if stream.get("modality") == "audition":
                logger.info("ATTENTION: Focus directed to Auditory stream (High Salience).")
                return "audition"

        logger.info("ATTENTION: Focus directed to Visual stream (Baseline).")
        return "vision"
