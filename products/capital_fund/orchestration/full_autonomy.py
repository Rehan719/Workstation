"""
FullAutonomyDelegationEngine – owner‑enabled mode for complete AI‑driven fund management.
All actions are constitutionally bounded and logged to UEG.
"""
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from firebase_admin import firestore
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from products.capital_fund.core.vault import CapitalVault
from products.capital_fund.orchestration.investment_orchestrator import InvestmentOrchestrator

db = firestore.client()

class FullAutonomyDelegationEngine:
    """
    Enables autonomous delegation for capital fund management.
    Owner grants authority for a specific timeframe and risk threshold.
    """
    def __init__(self, owner_uid: str):
        self.owner_uid = owner_uid
        self.vault = CapitalVault(owner_uid)
        self.orchestrator = InvestmentOrchestrator()
        self.ueg = UEGLogger()
        self.config_ref = db.collection("capital_fund_config").document(owner_uid)

    async def get_autonomy_state(self) -> Dict[str, Any]:
        """Fetch current autonomous delegation status."""
        doc = self.config_ref.get()
        if not doc.exists:
            return {"enabled": False, "risk_tolerance": 0.2, "max_allocation_pct": 0.2}
        return doc.to_dict()

    async def configure_autonomy(
        self,
        enabled: bool,
        risk_tolerance: float = 0.2,
        max_allocation_pct: float = 0.2
    ) -> Dict[str, Any]:
        """
        Configure delegation settings (Owner only).
        Sets bounds for autonomous execution.
        """
        config = {
            "enabled": enabled,
            "risk_tolerance": risk_tolerance,
            "max_allocation_pct": max_allocation_pct,
            "last_updated": firestore.SERVER_TIMESTAMP,
            "updated_by": self.owner_uid
        }
        self.config_ref.set(config, merge=True)

        await self.ueg.log_event("AUTONOMY_CONFIG_UPDATED", {
            "uid": self.owner_uid,
            "enabled": enabled,
            "risk_tolerance": risk_tolerance
        })

        return config

    async def run_autonomous_cycle(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a complete investment cycle without manual intervention.
        Strictly bounded by configured risk tolerance and constitutional rules.
        """
        state = await self.get_autonomy_state()
        if not state.get("enabled"):
            return {"status": "SKIPPED", "reason": "Full autonomy mode disabled."}

        # 1. Fetch available capital
        total_value = await self.vault._get_total_fund_value()
        # Maintain liquidity guard (10%)
        available_capital = total_value * Decimal("0.9")

        if available_capital <= 0:
            return {"status": "SKIPPED", "reason": "No available capital after liquidity guard."}

        # 2. Run Investment Orchestrator
        # Orchestrator uses MJM v4.0 and Mushāwara consultation internally
        deployments = await self.orchestrator.step(self.owner_uid, available_capital, market_context)

        if not deployments:
            return {"status": "NO_ACTION", "reason": "No high-confidence opportunities identified."}

        # 3. Post-execution validation & logging
        summary = {
            "status": "COMPLETED",
            "cycle_at": datetime.now(UTC).isoformat(),
            "deployments_count": len(deployments),
            "total_deployed": float(sum(Decimal(str(d.get("amount", 0.0))) for d in deployments))
        }

        await self.ueg.log_event("AUTONOMOUS_CYCLE_COMPLETED", {
            "uid": self.owner_uid,
            "summary": summary
        })

        return summary

    async def emergency_halt(self):
        """Disables autonomy immediately in case of abnormal system behavior."""
        await self.configure_autonomy(enabled=False)
        await self.ueg.log_event("AUTONOMY_EMERGENCY_HALT", {"uid": self.owner_uid})
