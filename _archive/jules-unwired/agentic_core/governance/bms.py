import logging
import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OKR:
    """Represents an Objective and Key Result."""
    def __init__(self, objective: str, key_results: List[Dict[str, Any]]):
        self.objective = objective
        self.key_results = key_results # Each KR: {"text": str, "target": float, "current": float, "unit": str}
        self.purpose_alignment_score = 0.0

    def update_progress(self, kr_index: int, value: float):
        if 0 <= kr_index < len(self.key_results):
            self.key_results[kr_index]["current"] = value
            logger.info(f"BMS: Updated KR {kr_index} for objective '{self.objective}' to {value}.")

    def calculate_completion(self) -> float:
        if not self.key_results:
            return 0.0
        total_completion = 0.0
        for kr in self.key_results:
            target = kr["target"]
            current = kr["current"]
            if target == 0:
                completion = 1.0 if current == 0 else 0.0
            else:
                completion = min(current / target, 1.0)
            total_completion += completion
        return total_completion / len(self.key_results)

class BusinessManagementSystem:
    """
    ARTICLE 327, 346 & 531: Business Management System (BMS).
    Manages OKRs, strategic planning, and Purpose Alignment Scores.
    """
    def __init__(self):
        self.okrs: List[OKR] = []
        self.strategic_plan: Dict[str, Any] = {
            "vision": "To be the ultimate platform for human productivity and spiritual alignment.",
            "mission": "Deliver production-ready, dual-purpose digital products.",
            "last_updated": datetime.datetime.now().isoformat()
        }

    def add_okr(self, objective: str, key_results: List[Dict[str, Any]], pas: float = 0.95):
        okr = OKR(objective, key_results)
        okr.purpose_alignment_score = pas
        self.okrs.append(okr)
        logger.info(f"BMS: Added OKR: {objective} (PAS: {pas})")

    def calculate_global_pas(self) -> float:
        """Calculates the weighted Purpose Alignment Score across all operations."""
        if not self.okrs:
            return 1.0
        total_pas = sum(okr.purpose_alignment_score for okr in self.okrs)
        return total_pas / len(self.okrs)

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generates a comprehensive business performance report."""
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "global_pas": self.calculate_global_pas(),
            "okr_progress": [],
            "strategic_alignment": "HIGH" if self.calculate_global_pas() >= 0.95 else "MODERATE"
        }
        for okr in self.okrs:
            report["okr_progress"].append({
                "objective": okr.objective,
                "completion": okr.calculate_completion(),
                "pas": okr.purpose_alignment_score
            })
        return report

    def update_strategic_plan(self, updates: Dict[str, Any]):
        self.strategic_plan.update(updates)
        self.strategic_plan["last_updated"] = datetime.datetime.now().isoformat()
        logger.info("BMS: Strategic Plan updated.")
