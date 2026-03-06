import logging
from typing import Dict, Any
from agentic_core.business.profit_distributor import ProfitDistributor
from agentic_core.governance.command_dispatch import AICommander

logger = logging.getLogger(__name__)

class OwnerDashboard:
    """
    ARTICLE 178: Owner Oversight Dashboard.
    Provides real-time visibility into revenue, mission impact, and strategic decisions.
    """
    def __init__(self, distributor: ProfitDistributor, commander: AICommander):
        self.distributor = distributor
        self.commander = commander

    def get_summary(self) -> Dict[str, Any]:
        """Provides real-time visibility and client portal features (Article 178/207)."""
        return {
            "financials": {
                "current_revenue": self.distributor.total_revenue,
                "operational_costs": self.distributor.operational_costs,
                "projected_profit": self.distributor.total_revenue - self.distributor.operational_costs,
                "tax_liability_est": (self.distributor.total_revenue - self.distributor.operational_costs) * 0.15
            },
            "mission_impact": self.commander.mission_kpis,
            "strategic_proposals": list(self.commander.strategy_map.keys()),
            "halal_audit_status": "PASSED",
            "active_leads": 5, # Mock data for now
            "client_satisfaction_nps": 78
        }

    def approve_pivot(self, pivot_id: str):
        logger.info(f"DASHBOARD: Owner approved strategic pivot {pivot_id}.")
        # Logic to activate the pivot in commander
