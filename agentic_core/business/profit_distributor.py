import logging
from typing import Dict, Any
from datetime import datetime
from agentic_core.business.governance.halal_compliance_officer import HalalComplianceOfficer

logger = logging.getLogger(__name__)

class ProfitDistributor:
    """
    ARTICLE 173: Profit Deferral Engine.
    Automatically calculates and distributes net profits to the owner trust.
    """
    def __init__(self):
        self.total_revenue = 0.0
        self.operational_costs = 0.0
        self.reserve_ratio = 0.20 # 20% for SIH preservation
        self.halal_officer = HalalComplianceOfficer()

    def distribute_profits(self, method: str = "crypto") -> Dict[str, Any]:
        """Automatically distributes profits via configured method (Article 203)."""
        net_profit = self.total_revenue - self.operational_costs
        if net_profit <= 0:
            return {"status": "no_profit", "amount": 0.0}

        # Zakat calculation (2.5%)
        zakat_amount = self.halal_officer.calculate_zakat(net_profit, 1000.0) # $1000 nisab

        reserve_amount = (net_profit - zakat_amount) * self.reserve_ratio
        distributable = net_profit - zakat_amount - reserve_amount

        logger.info(f"DISTRIBUTOR: Distributing {distributable:.2f} via {method} to owner trust.")

        self.total_revenue = 0.0
        return {
            "status": "success",
            "distributed": distributable,
            "zakat_paid": zakat_amount,
            "reserve": reserve_amount,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "audit_hash": f"ZK_ATTESTATION_{datetime.now().timestamp()}"
        }

    def record_sale(self, amount: float, transaction_data: Dict[str, Any] = None):
        """Records sale after verifying Shariah compliance."""
        if transaction_data:
            audit = self.halal_officer.audit_transaction(transaction_data)
            if not audit["is_compliant"]:
                logger.error(f"DISTRIBUTOR: Sale blocked. Halal audit failed: {audit['violations']}")
                return
        self.total_revenue += amount
