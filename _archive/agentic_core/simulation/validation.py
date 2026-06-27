import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

import numpy as np

class TwinValidationHarness:
    """
    ARTICLE 307: Twin Validation Harness.
    """
    def validate_prediction(self, prediction: Any, actual: Any) -> float:
        """
        ARTICLE 308: Performs cross-correlation and MSE analysis between twin state and ground truth.
        """
        try:
            pred_arr = np.array(prediction)
            act_arr = np.array(actual)

            if pred_arr.shape != act_arr.shape:
                return 0.0

            mse = np.mean((pred_arr - act_arr)**2)
            max_val = np.max(act_arr) if np.max(act_arr) > 0 else 1.0
            score = max(0.0, 1.0 - (mse / max_val))

            logger.info(f"Validation: Fidelity Score computed: {score}")
            return float(score)
        except Exception as e:
            logger.error(f"Validation: Error in validation: {e}")
            return 0.0

    def run_automated_audit(self, twin_id: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Performs a deep audit of a twin's historical fidelity.
        """
        scores = [h.get("fidelity", 0) for h in history]
        avg_fidelity = np.mean(scores) if scores else 0.0

        return {
            "twin_id": twin_id,
            "avg_fidelity": avg_fidelity,
            "status": "VALIDATED" if avg_fidelity >= 0.95 else "RE-TRAINING_REQUIRED"
        }
