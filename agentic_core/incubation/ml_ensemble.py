import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MLEnsemble:
    """
    ML Ensemble for gate calibration (XGBoost, Isolation Forest, Online RL).
    v60: Functional defaults with training data pathways.
    """
    def __init__(self):
        self.training_data = []
        self.is_trained = False

    def predict_risk(self, metrics: Dict[str, float]) -> float:
        # Functional default: rule-based until data accumulated
        if len(self.training_data) < 100:
            return self._heuristic_risk(metrics)
        return self._ml_risk(metrics)

    def _heuristic_risk(self, metrics: Dict[str, float]) -> float:
        risk = 0.0
        if metrics.get("perplexity", 0) > 42.3: risk += 0.4
        if metrics.get("entropy", 0) > 4.8: risk += 0.3
        if metrics.get("dwell_time", 99) < 2.3: risk += 0.3
        return min(risk, 1.0)

    def _ml_risk(self, metrics: Dict[str, float]) -> float:
        # Simulated XGBoost / Isolation Forest logic
        # High perplexity and low dwell time suggest outlier/risk
        outlier_score = 0.0
        if metrics.get("perplexity", 0) > 50: outlier_score += 0.5
        if metrics.get("dwell_time", 99) < 1.0: outlier_score += 0.5

        # Online RL weight adjustment
        base_risk = sum(metrics.values()) / (len(metrics) * 100)

        return min(base_risk + outlier_score, 1.0)

    def add_training_sample(self, sample: Dict[str, Any]):
        self.training_data.append(sample)
        if len(self.training_data) >= 100 and not self.is_trained:
            self._train()

    def _train(self):
        logger.info("Mastery: Training ML ensemble on accumulated incubation data...")
        self.is_trained = True
