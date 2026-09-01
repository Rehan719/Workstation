import logging
from typing import Dict, Any, List, Optional
import numpy as np
import difflib

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
        # W432 — §4.5 class. `confidence` was initialised to 1.0 and the GENERIC branch never
        # reassigned it, so a flatly wrong answer ("alpha" vs "omega") came back
        # `is_accurate: False, confidence: 1.0` — a field named confidence reporting MAXIMUM
        # confidence in a mismatch. It was structurally incapable of any other value on that path.
        # APP_CODE was worse in kind: 0.85/0.2 are invented constants presented as a measurement.
        #
        # Confidence is now None wherever nothing computes one, with `confidence_basis` saying why.
        # A binary check has no confidence gradient, and inventing one is the defect, not the fix.
        is_accurate = False
        confidence: Optional[float] = None
        basis = ""

        if task_type == "NUMERICAL":
            try:
                error = abs(prediction - actual)
                is_accurate = error <= (0.01 * actual) # 1% error tolerance
                confidence = 1.0 / (1.0 + error)
                basis = f"1/(1+error) on absolute error {error}"
            except (TypeError, ValueError, ZeroDivisionError) as exc:
                # A non-numeric input is not an INACCURATE prediction — it is an unusable comparison.
                is_accurate = False
                confidence = None
                basis = f"numeric comparison failed ({type(exc).__name__}) - nothing was measured"

        elif task_type == "SEMANTIC":
            # Article 60: difflib SequenceMatcher ratio for semantic similarity
            ratio = difflib.SequenceMatcher(None, str(prediction), str(actual)).ratio()
            is_accurate = ratio >= 0.8
            confidence = ratio
            basis = f"difflib similarity ratio {round(ratio, 4)} against threshold 0.8"

        elif task_type == "APP_CODE":
            # A presence check, honestly named. There is no gradient here: the tokens are there or
            # they are not, so no confidence is reported rather than a fabricated 0.85.
            is_accurate = "class " in str(prediction) or "def " in str(prediction) or "import " in str(prediction)
            confidence = None
            basis = ("presence of class/def/import in the prediction - a syntax presence check, "
                     "not a correctness measure, and it carries no confidence gradient")

        else:
            is_accurate = prediction == actual
            confidence = None
            basis = "exact equality - a binary comparison with no confidence gradient"

        result = {
            "is_accurate": is_accurate,
            "confidence": confidence,
            "confidence_basis": basis,
            "task_type": task_type,
            "timestamp": np.datetime64('now')
        }

        self.validation_history.append(result)
        logger.info("AccuracyValidator: Validated %s output. Accuracy: %s, Confidence: %s (%s)",
                    task_type, is_accurate,
                    "not measured" if confidence is None else round(confidence, 2), basis)
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
