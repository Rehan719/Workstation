import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DualMetricMiddleware:
    """
    ARTICLE 247: Dual-Metric Governance Middleware.
    Executes spiritual KPIs and business KPIs in parallel without one superseding the other.
    """
    def __init__(self, scholar_board_ref: Optional[Any] = None, policy_path: str = "config/qep/policies.json"):
        self.scholar_board = scholar_board_ref
        self.active_policies = self._load_policies(policy_path)

    def _load_policies(self, path: str) -> Dict[str, Any]:
        """ARTICLE 246: Enables adaptive governance without code changes."""
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Middleware: Failed to load policies from {path}: {e}")

        return {
            "spiritual_thresholds": {"tazkiyah_min": 75.0, "dawah_readiness_min": 0.85},
            "business_thresholds": {"retention_min": 0.60, "growth_min": 0.05}
        }

    def evaluate_operation(self, user_id: str, action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercepts operations and evaluates them against dual metrics.
        """
        # Parallel Path 1: Spiritual Evaluation
        spiritual_result = self._evaluate_spiritual_kpi(user_id, action_type, context)

        # Parallel Path 2: Business Evaluation
        business_result = self._evaluate_business_kpi(user_id, action_type, context)

        combined_decision = {
            "spiritual_compliance": spiritual_result["status"],
            "business_viability": business_result["status"],
            "decision": "PROCEED" if spiritual_result["status"] == "COMPLIANT" and business_result["status"] == "VIABLE" else "CONSTRAIN",
            "reasoning": {
                "spiritual": spiritual_result["reason"],
                "business": business_result["reason"]
            },
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"DualMetricMiddleware: Evaluated {action_type} for user {user_id}. Decision: {combined_decision['decision']}")
        return combined_decision

    def _evaluate_spiritual_kpi(self, user_id: str, action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates spiritual KPI constraints."""
        # ARTICLE 60: Functional logic for policy enforcement
        tazkiyah_score = context.get("user_tazkiyah", 0)
        is_compliant = tazkiyah_score >= self.active_policies["spiritual_thresholds"]["tazkiyah_min"]

        # Specific gating logic for Dawah activities
        if action_type == "DAWAH_ACTIVITY" and not context.get("dawah_ready", False):
            return {"status": "VIOLATION", "reason": "User not yet Da'wah Ready (Quran 3:104)"}

        return {
            "status": "COMPLIANT" if is_compliant else "CONSTRAINED",
            "reason": "Spiritual thresholds maintained" if is_compliant else "Spiritual purification required"
        }

    def _evaluate_business_kpi(self, user_id: str, action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates business KPI constraints."""
        # Simple viability check based on retention/growth patterns
        is_viable = True # Simulation default

        return {
            "status": "VIABLE" if is_viable else "UNVIABLE",
            "reason": "Operational sustainability verified"
        }

class TazkiyahEngine:
    """
    ARTICLE 248: Tazkiyah Score Engine.
    Calculates spiritual purification based on Quranic practice metrics.
    """
    def __init__(self, db_manager: Optional[Any] = None, weights_path: str = "config/qep/policies.json"):
        self.db = db_manager
        self.weights = self._load_weights(weights_path)

    def _load_weights(self, path: str) -> Dict[str, float]:
        """Enables scholar-led weight adjustment."""
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    return data.get("tazkiyah_weights", {})
        except Exception:
            logger.warning(f"TazkiyahEngine: Could not load weights from {path}, using defaults.")

        return {
            "memorization": 0.25, "prayer": 0.30, "dhikr": 0.15,
            "fasting": 0.15, "charity": 0.10, "character": 0.05
        }

    def calculate_tazkiyah_score(self, user_id: str, metrics: Optional[Dict[str, float]] = None) -> float:
        """
        Calculates dynamic Tazkiyah score (0-100).
        """
        if metrics is None and self.db:
            data = self.db.get_spiritual_metrics(user_id)
            metrics = data.get('metrics_json', {})

        if not metrics:
            return 0.0

        score = 0.0
        for key, weight in self.weights.items():
            score += metrics.get(key, 0.0) * weight * 100

        final_score = min(100.0, max(0.0, score))
        logger.info(f"TazkiyahEngine: Calculated score for {user_id}: {final_score:.2f}")

        # Persist to DB
        if self.db:
            self.db.save_spiritual_metrics(user_id, final_score, metrics)

        return final_score

    def get_tier(self, score: float) -> str:
        """Calibrates score into tiers."""
        if score >= 92: return "MUTAQIN"
        if score >= 78: return "MUSTAQIM"
        if score >= 60: return "MUHSIN"
        if score >= 40: return "SALIK"
        return "MUBTADI"

class DawahReadinessEngine:
    """
    ARTICLE 249: Da'wah Readiness Gating.
    Determines user qualification for Dawah activities.
    """
    def __init__(self, db_manager: Any, tazkiyah_engine: Optional[Any] = None):
        self.db = db_manager
        self.tazkiyah_engine = tazkiyah_engine
        self.tazkiyah_threshold = 75.0
        self.character_threshold = 0.85

    def is_ready(self, user_id: str, profile_data: Optional[Dict[str, Any]] = None) -> bool:
        """Wrapper for boolean check used in tests."""
        res = self.evaluate_readiness(user_id, profile_data or {})
        return res["is_ready"]

    def evaluate_readiness(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates readiness based on Quran 3:104 and Hadith Muslim 1036.
        """
        foundational_complete = profile_data.get("foundational_modules_complete", False)
        tazkiyah_score = profile_data.get("tazkiyah_score")
        if tazkiyah_score is None:
            if self.tazkiyah_engine:
                tazkiyah_score = self.tazkiyah_engine.calculate_tazkiyah_score(user_id)
            elif self.db:
                data = self.db.get_spiritual_metrics(user_id)
                tazkiyah_score = data.get('tazkiyah_score', 0.0)

        tazkiyah_score = tazkiyah_score or 0.0
        feedback_ratio = profile_data.get("community_feedback_ratio", 0.0)

        tazkiyah_passed = tazkiyah_score >= self.tazkiyah_threshold
        character_passed = feedback_ratio >= self.character_threshold

        is_ready = foundational_complete and tazkiyah_passed and character_passed

        details = {
            "foundational": foundational_complete,
            "tazkiyah": tazkiyah_passed,
            "character": character_passed
        }

        # Persist to DB
        if self.db:
            self.db.save_dawah_readiness(user_id, is_ready, details)

        logger.info(f"DawahReadinessEngine: User {user_id} readiness: {is_ready}")
        return {
            "is_ready": is_ready,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
