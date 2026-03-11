import logging
from typing import Dict, Any, List
import datetime
import os

logger = logging.getLogger(__name__)

class StrategicPlanningModule:
    """
    ARTICLE 328: Strategic Business Planning.
    Generates, reviews, and updates the Business Plan (Vision, Mission, Aims, Objectives).
    """
    def __init__(self, plan_path: str = "docs/strategy/business_plan.md"):
        self.plan_path = plan_path

    def generate_draft_plan(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a draft Business Plan based on strategic inputs and current system state."""
        # Use provided inputs or default to core workstation aims
        vision = inputs.get("vision", "Transcendent Evolution of Sovereign Intelligence")
        mission = inputs.get("mission", "Perpetual Strategic Optimization via Integrated Introspection")
        aims = inputs.get("aims", [
            "Scale Specialized Sub-Reactors to 100+ instances",
            "Achieve 99.8% Digital Twin Fidelity (ESE)",
            "Automate 100% of Resource Assembly (DRAD)",
            "Ensure 100% Constitutional Compliance (VGA)"
        ])
        objectives = inputs.get("objectives", [
            "Deploy Integrated Strategic Enterprise (v101.0)",
            "Execute Grand Synthesis for v101.0 DNA",
            "Implement Entity-CEO Strategic Interface",
            "Establish QMS 3.0 Integrated Governance"
        ])

        return {
            "vision": vision,
            "mission": mission,
            "aims": aims,
            "objectives": objectives,
            "status": "DRAFT",
            "generation_ts": datetime.datetime.now().isoformat()
        }

    def save_plan(self, plan: Dict[str, Any]):
        """Saves the Business Plan to a markdown file with metadata."""
        os.makedirs(os.path.dirname(self.plan_path), exist_ok=True)
        content = f"""# Business Plan: {plan['vision']}

## 1. Vision
{plan['vision']}

## 2. Mission
{plan['mission']}

## 3. Strategic Aims
{self._format_list(plan['aims'])}

## 4. Quarterly Objectives (OKRs)
{self._format_list(plan['objectives'])}

---
*Status: {plan['status']} | Last Updated: {plan['generation_ts']}*
"""
        with open(self.plan_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _format_list(self, items: List[str]) -> str:
        return "\n".join([f"- {i}" for i in items])

class ResourceManagementModule:
    """
    ARTICLE 327: BMS Resource Management.
    Allocates resources based on strategic priorities using ARO-ready formulas.
    """
    def allocate_resources(self, priorities: List[Dict[str, Any]]) -> Dict[str, float]:
        """Allocates compute and agent time using weighted priority formulas."""
        # Weighted allocation logic: Higher priority (HIGH) gets more resource shares
        weight_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        total_weight = sum(weight_map.get(p.get("priority", "LOW"), 1) for p in priorities)

        allocation = {}
        if total_weight == 0:
            return allocation

        for p in priorities:
            name = p.get("type", "UNKNOWN")
            weight = weight_map.get(p.get("priority", "LOW"), 1)
            allocation[name] = round(weight / total_weight, 2)

        return allocation

class PerformanceManagementModule:
    """
    ARTICLE 327: BMS Performance Management.
    Tracks KPIs and reports to the AI CEO Dashboard.
    """
    def __init__(self):
        self.kpi_history = []

    def get_kpis(self, raw_telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Returns key performance indicators based on actual system telemetry."""
        # Calculate scores from telemetry
        alignment = raw_telemetry.get("strategic_alignment", 0.95)
        efficiency = 1.0 - raw_telemetry.get("resource_waste", 0.04)
        achievement = raw_telemetry.get("okr_progress", 0.8)

        kpis = {
            "strategic_alignment": alignment,
            "resource_efficiency": efficiency,
            "objective_achievement": achievement,
            "overall_health": (alignment + efficiency + achievement) / 3
        }
        self.kpi_history.append(kpis)
        return kpis
