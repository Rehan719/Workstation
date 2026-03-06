import logging
from typing import Dict, Any, List, Optional
import numpy as np

logger = logging.getLogger(__name__)

class AccuracyValidator:
    """
    ARTICLE 150: Continuous validation of cognitive outputs against ground truth.
    Supports automated accuracy assurance for cognitive models and generated artifacts.
    """
    def __init__(self, target_accuracy: float = 0.95):
        self.target_accuracy = target_accuracy
        self.validation_history: List[Dict[str, Any]] = []

    def validate_output(self, prediction: Any, actual: Any, task_type: str = "GENERIC") -> Dict[str, Any]:
        """
        Validates a single cognitive output against a ground truth value.
        """
        is_accurate = False
        confidence = 1.0

        if task_type == "NUMERICAL":
            try:
                error = abs(prediction - actual)
                is_accurate = error <= (0.01 * actual) # 1% error tolerance
                confidence = 1.0 / (1.0 + error)
            except:
                is_accurate = False
                confidence = 0.0

        elif task_type == "SEMANTIC":
            # Semantic similarity placeholder (v99 implementation would use embeddings)
            is_accurate = prediction == actual
            confidence = 0.9 if is_accurate else 0.1

        elif task_type == "APP_CODE":
            # Simple check for code validity and presence of key elements
            is_accurate = "class " in str(prediction) or "def " in str(prediction) or "import " in str(prediction)
            confidence = 0.85 if is_accurate else 0.2

        else:
            is_accurate = prediction == actual

        result = {
            "is_accurate": is_accurate,
            "confidence": confidence,
            "task_type": task_type,
            "timestamp": np.datetime64('now')
        }

        self.validation_history.append(result)
        logger.info(f"AccuracyValidator: Validated {task_type} output. Accuracy: {is_accurate}, Confidence: {confidence:.2f}")
        return result

    def get_aggregate_accuracy(self, last_n: int = 100) -> float:
        """
        Returns the aggregate accuracy over the last n validation events.
        """
        if not self.validation_history:
            return 1.0

        history_slice = self.validation_history[-last_n:]
        accurate_count = sum(1 for v in history_slice if v["is_accurate"])
        accuracy = accurate_count / len(history_slice)

        logger.info(f"AccuracyValidator: Aggregate Accuracy over last {len(history_slice)} events: {accuracy:.2f}")
        return accuracy

    def check_compliance(self) -> bool:
        """
        Checks if the system is currently meeting its target accuracy threshold.
        """
        current_accuracy = self.get_aggregate_accuracy()
        is_compliant = current_accuracy >= self.target_accuracy

        if not is_compliant:
            logger.warning(f"AccuracyValidator: Accuracy ({current_accuracy:.2f}) is below target ({self.target_accuracy:.2f}).")

        return is_compliant
