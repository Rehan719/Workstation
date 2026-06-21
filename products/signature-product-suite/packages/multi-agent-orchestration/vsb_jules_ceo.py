import os
import sys
from typing import Dict, Any, List

# Sibling engine folders contain hyphens, so they cannot be imported via a
# normal dotted path. Resolve them on sys.path instead.
_PKGS = os.path.join(os.path.dirname(__file__), "..")
for _sib in ("business-intelligence", "science-intelligence", "scholarship-intelligence"):
    _p = os.path.join(_PKGS, _sib)
    if _p not in sys.path:
        sys.path.insert(0, _p)
from vsb_business import BusinessIntelligenceEngine
from vsb_science import ScienceIntelligenceEngine
from vsb_scholarship import ScholarshipIntelligenceEngine

class JulesVirtualCEO:
    """
    JULES: Virtual Sovereign CEO v12.0.
    Orchestrates the entire fabric and C-Suite swarm.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.business = BusinessIntelligenceEngine(node_id)
        self.science = ScienceIntelligenceEngine(node_id)
        self.scholarship = ScholarshipIntelligenceEngine(node_id)

    async def orchestrate_global_mission(self, mission: str):
        """Strategic alignment across all core streams."""
        results = []
        # Business assessment
        results.append(await self.business.run_strategic_assessment(mission, {}))
        # Science verification
        results.append(await self.science.automate_scientific_method(mission, {}))
        # Scholarship review
        results.append(await self.scholarship.literature_synthesis(mission, {}))

        return {
            "mission": mission,
            "orchestration_status": "synced_v12",
            "stream_results": results
        }
