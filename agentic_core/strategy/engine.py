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
        """Generates a draft Business Plan based on strategic inputs and dual-purpose mandates."""
        # ARTICLE 336: Dual-Purpose Foundation
        vision = inputs.get("vision", "Transcendent Evolution of Purpose-Driven Intelligence")
        mission = inputs.get("mission", "Seeking Divine Pleasure via Profit-Enabled Innovation & Scholarship")

        aims = inputs.get("aims", [
            "Become the leading platform for Islamic scholarship and Dawah-tech.",
            "Generate sustainable profit to fund charitable works and system expansion.",
            "Empower users in scholarship, enterprise, and personal affairs.",
            "Ensure 100% Purpose Alignment across all sub-reactors."
        ])

        # OKRs now include purpose alignment targets (Article 339)
        objectives = inputs.get("objectives", [
            {"desc": "Launch free Dawah module", "purpose_target": 0.95},
            {"desc": "Increase revenue by 20% (5% to charity)", "purpose_target": 0.90},
            {"desc": "Execute v103.0 Purpose Grand Synthesis", "purpose_target": 1.0}
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

    def _format_list(self, items: List[Any]) -> str:
        formatted = []
        for i in items:
            if isinstance(i, dict):
                formatted.append(f"- {i.get('desc')} (Purpose Target: {i.get('purpose_target')})")
            else:
                formatted.append(f"- {i}")
        return "\n".join(formatted)

class ResourceManagementModule:
    """
    ARTICLE 327: BMS Resource Management.
    Allocates resources based on strategic priorities using ARO-ready formulas.
    """
    def allocate_resources(self, priorities: List[Dict[str, Any]]) -> Dict[str, float]:
        """Allocates resources using weighted priority and Purpose Alignment scores."""
        weight_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        total_weight = sum(weight_map.get(p.get("priority", "LOW"), 1) for p in priorities)

        allocation = {}
        if total_weight == 0:
            return allocation

        for p in priorities:
            name = p.get("type", "UNKNOWN")
            weight = weight_map.get(p.get("priority", "LOW"), 1)
            purpose_factor = p.get("purpose_target", 1.0)
            allocation[name] = round((weight * purpose_factor) / total_weight, 2)

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
