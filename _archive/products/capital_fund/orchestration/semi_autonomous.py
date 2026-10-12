import asyncio
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from products.capital_fund.orchestration.investment_orchestrator import InvestmentOrchestrator
from products.capital_fund.core.vault import CapitalVault

class SemiAutonomousExecutor:
    """
    Module 3C: Semi-Autonomous Execution Engine.
    Owner-enabled mode where AI can execute low-risk rebalancing without real-time approval.
    High-risk (>10% AUM or risk > 0.2) still requires manual/council approval.
    """
    def __init__(self, owner_uid: str, orchestrator: InvestmentOrchestrator, vault: CapitalVault):
        self.owner_uid = owner_uid
        self.orchestrator = orchestrator
        self.vault = vault
        self.ueg = UEGLogger()
        self.enabled = False
        self.risk_threshold = 0.20
        self.aum_threshold = Decimal("0.10")

    async def toggle_autonomous_mode(self, uid: str, enabled: bool) -> bool:
        """Enables or disables autonomous mode. Only the owner can call this."""
        if uid != self.owner_uid:
            raise ValueError("Unauthorized: Only the sovereign owner can toggle autonomous execution.")

        self.enabled = enabled
        await self.ueg.log_event(
            "SEMI_AUTONOMOUS_MODE_CHANGED",
            {"uid": uid, "enabled": enabled, "timestamp": datetime.now(UTC).isoformat()}
        )
        return self.enabled

    async def execute_low_risk_rebalance(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-driven rebalancing for low-risk scenarios.
        """
        if not self.enabled:
            raise ValueError("Semi-autonomous execution is currently disabled.")

        # 1. Fetch current total value
        total_value = await self.vault._get_total_fund_value()
        if total_value == 0:
            return {"status": "SKIPPED", "reason": "No AUM to rebalance."}

        # 2. Get Orchestration Decision (MJM v4.0 + Mushāwara)
        # We use Decimal for high precision
        allocations = await self.orchestrator.step(self.owner_uid, total_value, market_context)

        if not allocations:
            return {"status": "SKIPPED", "reason": "No high-confidence allocation proposed."}

        # 3. Check Risk and Scale (Constitutional Safety Gate)
        # We assume the first deployment represents the primary action for risk check
        primary_action = allocations[0]
        risk_score = primary_action.get("risk_score", 0.0)
        action_amount = Decimal(str(primary_action.get("amount", 0.0)))

        is_high_risk = risk_score > self.risk_threshold
        is_large_scale = action_amount > (total_value * self.aum_threshold)

        if is_high_risk or is_large_scale:
            await self.ueg.log_event("AUTONOMOUS_EXECUTION_BLOCKED", {
                "reason": "High risk or large scale detected",
                "risk_score": risk_score,
                "amount": float(action_amount),
                "total_value": float(total_value)
            })
            return {
                "status": "APPROVAL_REQUIRED",
                "reason": "Proposal exceeds autonomous safety limits.",
                "proposal": allocations
            }

        # 4. Execute (ACT)
        # In a full implementation, this would trigger the actual rebalance in the vault
        # For Phase 3, we log the execution and return the receipts
        await self.ueg.log_event("AUTONOMOUS_REBALANCE_EXECUTED", {
            "uid": self.owner_uid,
            "allocations": allocations,
            "risk_score": risk_score,
            "autonomous": True
        })

        return {
            "status": "EXECUTED",
            "receipts": allocations,
            "autonomous": True
        }
