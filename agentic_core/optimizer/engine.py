import logging
import sqlite3
from typing import Dict, Any, List, Optional
from .monitor import ResourceMonitor
from .predictor import DemandPredictor
from .allocator import AllocationEngine
from .scheduler import CostAwareScheduler
from .fabric import DynamicResourceFabric
from .ral import RALVerifier

logger = logging.getLogger(__name__)

class AdaptiveResourceOptimizer:
    """
    v100.0: Master Adaptive Resource Optimizer (ARO).
    Unifies monitoring, prediction, allocation, and dynamic assembly.
    Governed by Articles 305-306.
    """
    def __init__(self):
        self.monitor = ResourceMonitor()
        self.predictor = DemandPredictor()
        self.allocator = AllocationEngine()
        self.scheduler = CostAwareScheduler(monitor=self.monitor)
        self.fabric = DynamicResourceFabric()
        self.ral = RALVerifier(fabric=self.fabric)
        logger.info("ARO: Adaptive Resource Optimizer Awakened.")

    async def process_ral_request(self, user_id: str, tier: str, ral_spec: str) -> Dict[str, Any]:
        """
        End-to-end processing of a RAL request:
        Verify -> Schedule -> Assemble -> Allocate
        """
        # 1. Verify
        verification = self.ral.verify_request(ral_spec)
        if verification["status"] != "VERIFIED":
            return verification

        # 2. Schedule (Cost-aware) - on the RESOLVED tier, so the scheduler and the quota cannot read
        #    the same unknown tier differently (W492/FU-183: "standard" got a free share and paid
        #    scheduling).
        resolved = self.allocator.resolve_tier(tier)
        task = {"id": verification["request_id"], "user_id": user_id}
        schedule_status = await self.scheduler.schedule_task(
            task, resolved["tier_applied"],
            queued=bool(self.allocator.QUOTAS[resolved["tier_applied"]]["queued"]))
        if schedule_status["status"] in ["REJECTED", "QUEUED"]:
            return {**schedule_status, **resolved}

        # 3. Assemble (DRAD)
        pool_id = self.fabric.assemble_pool(verification["translated_requirements"])

        # 4. Allocate (Tiered Fairness) - on the domain the request actually asked for; the verifier
        #    now returns it, so this no longer silently becomes "general".
        domain = verification.get("domain")
        allocation = self.allocator.allocate(user_id, tier, domain or "general")
        allocation["domain_basis"] = ("the domain this request asked for" if domain else
                                      "the request carried no domain, so the general pool applies")

        return {
            "status": "SUCCESS",
            "pool_id": pool_id,
            "pool_basis": ("assembled on this per-request optimiser instance and discarded when the "
                           "response returns - not a held reservation"),
            "allocation": allocation,
            "verification": verification
        }

    def release_pool(self, pool_id: str):
        self.fabric.disassemble_pool(pool_id)
