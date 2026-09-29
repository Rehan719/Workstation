import logging
from typing import Dict, Any, List, Optional
import uuid

logger = logging.getLogger(__name__)

class DynamicResourceFabric:
    """
    ARTICLE 318: Dynamic Resource Fabric.
    Enables on-demand assembly and disassembly of resource pools.
    """
    def __init__(self):
        self.inventory = {
            "compute": {"total": 1000, "available": 1000},
            "memory": {"total": 8192, "available": 8192},
            "gpu": {"total": 64, "available": 64},
            "api_quotas": {"total": 100000, "available": 100000}
        }
        self.active_pools = {}
        # W505 (FU-018) — per pool, what it asked for and did not get. Kept apart from active_pools,
        # which now holds only what was GRANTED.
        self.shortfalls: Dict[str, Any] = {}

    def assemble_pool(self, requirements: Dict[str, Any]) -> str:
        """W505 (FU-018) — A POOL HOLDS WHAT IT WAS GRANTED, not what it asked for.

        This stored the full `requirements` even for resources it could not decrement, and for resources
        not in the inventory at all; `disassemble_pool` then gave every one of those amounts back. Each
        ungranted requirement therefore inflated `available` permanently — the register recorded gpu at
        1064 against a total of 64. The all-or-nothing-per-resource behaviour is unchanged (the old code
        granted the whole amount or none); what changes is that only the granted part is remembered, and
        the shortfall is reported instead of only logged."""
        pool_id = f"pool_{uuid.uuid4().hex[:8]}"
        logger.info(f"Fabric: Assembling resource pool {pool_id} for {requirements}")

        granted: Dict[str, Any] = {}
        self.shortfalls[pool_id] = {}
        for res, amount in requirements.items():
            if res not in self.inventory:
                self.shortfalls[pool_id][res] = {"requested": amount, "granted": 0,
                                                 "reason": "no such resource in the fabric"}
                logger.warning(f"Fabric: unknown resource {res!r} for pool {pool_id} — nothing granted")
                continue
            if self.inventory[res]["available"] >= amount:
                self.inventory[res]["available"] -= amount
                granted[res] = amount
            else:
                self.shortfalls[pool_id][res] = {"requested": amount, "granted": 0,
                                                 "available": self.inventory[res]["available"],
                                                 "reason": "insufficient available capacity"}
                logger.warning(f"Fabric: Insufficient {res} for pool {pool_id} "
                               f"(requested {amount}, available {self.inventory[res]['available']}) "
                               f"— nothing granted for it, and nothing will be released for it")

        self.active_pools[pool_id] = granted
        return pool_id

    def pool_shortfalls(self, pool_id: str) -> Dict[str, Any]:
        """W505 (FU-018) — what a pool asked for and did NOT get. A caller that treats assemble_pool as
        having satisfied its requirements is making a claim this reports on."""
        return dict(self.shortfalls.get(pool_id) or {})

    def disassemble_pool(self, pool_id: str):
        if pool_id in self.active_pools:
            granted = self.active_pools.pop(pool_id)
            self.shortfalls.pop(pool_id, None)
            logger.info(f"Fabric: Disassembling pool {pool_id}, reclaiming {granted}")
            for res, amount in granted.items():
                if res in self.inventory:
                    inv = self.inventory[res]
                    # W505 (FU-018) — the invariant, stated and enforced: available <= total. Only granted
                    # amounts reach here, so this must never bind; if it does the accounting is wrong
                    # somewhere else and that is worth a loud record, not a silent clamp.
                    if inv["available"] + amount > inv["total"]:
                        logger.error(
                            f"Fabric: releasing {amount} {res} from pool {pool_id} would take available "
                            f"to {inv['available'] + amount} of a total {inv['total']} — clamped, and this "
                            f"means a release was recorded that was never granted")
                        inv["available"] = inv["total"]
                    else:
                        inv["available"] += amount
        else:
            logger.warning(f"Fabric: Attempted to disassemble non-existent pool {pool_id}")

    def get_inventory_status(self) -> Dict[str, Any]:
        return self.inventory
