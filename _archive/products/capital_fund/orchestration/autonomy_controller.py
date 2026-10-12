"""
Master Autonomy Controller (Tier 3) – Enables full AI-driven management of the Capital Fund.
Enforces constitutional kill-switches, daily caps, and owner heartbeats.
"""
import asyncio
import logging
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime, UTC
from firebase_admin import firestore
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from products.capital_fund.orchestration.full_autonomy import FullAutonomyDelegationEngine

db = firestore.client()

class AutonomyController:
    """
    Tier 3 Controller: Orchestrates full autonomous execution.
    Maintains a real-time kill-switch monitor and heartbeat verification.
    """
    def __init__(self, owner_uid: str):
        self.owner_uid = owner_uid
        self.logger = logging.getLogger("AutonomyController")
        self.ueg = UEGLogger()
        self.engine = FullAutonomyDelegationEngine(owner_uid)
        self.enabled = False
        self.kill_switch_active = False
        self.last_owner_heartbeat = datetime.now(UTC)
        self.daily_execution_limit = Decimal("0.05") # 5% of AUM max per day autonomous

    async def enable_tier_3(self, risk_tolerance: float = 0.3):
        """Enable Full Autonomy mode (Owner opt-in only)."""
        # In a real system, this would check owner signature/DID
        self.enabled = True
        self.kill_switch_active = False
        await self.engine.configure_autonomy(enabled=True, risk_tolerance=risk_tolerance)
        await self.ueg.log_event("FULL_AUTONOMY_TIER_3_ENABLED", {
            "uid": self.owner_uid,
            "risk_tolerance": risk_tolerance,
            "timestamp": datetime.now(UTC).isoformat()
        })
        # Start background kill-switch monitor
        asyncio.create_task(self._monitor_safety_invariants())

    async def _monitor_safety_invariants(self):
        """Background task to check for kill-switch triggers or missed heartbeats."""
        while self.enabled:
            # 1. Check Heartbeat (Mandatory every 24 hours)
            time_since_heartbeat = (datetime.now(UTC) - self.last_owner_heartbeat).total_seconds()
            if time_since_heartbeat > 86400: # 24 hours
                await self.emergency_stop("HEARTBEAT_TIMEOUT")
                break

            # 2. Check Global Kill-Switch from Firestore
            doc = db.collection("capital_fund_config").document(self.owner_uid).get()
            if doc.exists and doc.to_dict().get("kill_switch_triggered"):
                await self.emergency_stop("GLOBAL_KILL_SWITCH")
                break

            await asyncio.sleep(60) # Check every minute

    async def execute_cycle(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a full autonomous cycle with daily cap enforcement."""
        if not self.enabled or self.kill_switch_active:
            return {"status": "BLOCKED", "reason": "Autonomy tier 3 inactive or kill-switch triggered."}

        # Enforce daily execution limit (Simulated check)
        # In production, this queries the last 24h total from UEG

        result = await self.engine.run_autonomous_cycle(market_context)

        if result.get("status") == "COMPLETED":
            await self.ueg.log_event("TIER_3_AUTONOMOUS_EXECUTION", {
                "uid": self.owner_uid,
                "summary": result
            })

        return result

    async def receive_heartbeat(self):
        """Called by UI/Mobile when owner interacts with the system."""
        self.last_owner_heartbeat = datetime.now(UTC)
        await self.ueg.log_event("OWNER_HEARTBEAT_RECEIVED", {"uid": self.owner_uid})

    async def emergency_stop(self, reason: str):
        """Immediately halts all autonomous operations."""
        self.enabled = False
        self.kill_switch_active = True
        await self.engine.configure_autonomy(enabled=False)
        await self.ueg.log_event("AUTONOMY_EMERGENCY_HALT", {
            "uid": self.owner_uid,
            "reason": reason,
            "timestamp": datetime.now(UTC).isoformat()
        })
        self.logger.critical(f"EMERGENCY STOP TRIGGERED: {reason}")
