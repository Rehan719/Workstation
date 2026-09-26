import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AllocationEngine:
    """
    ARTICLE 311: Allocation Engine.
    Implements tiered fairness and preemption logic.
    """
    def __init__(self):
        self.active_allocations = {}

    # W492 (FU-183/S4.21) - the quota table and the scheduler each interpreted an unknown tier on their
    # own: the quota fell back to free while the scheduler's `else` branch treated anything not "free" as
    # paid, so "standard" (the Resource Fabric's own default) received the FREE share with PAID immediate
    # execution. One resolution now governs both, and an unrecognised tier is said, not absorbed.
    # Each tier declares BOTH facts - the share AND whether it queues - because the divergence was
    # exactly that two stages inferred them separately. "standard" is this platform's own declared
    # default (api/optimizer.py AllocateRequest.tier, and the Resource Fabric's default param): it was
    # absent from this table, so it silently drew the free share while the scheduler executed it
    # immediately. Declared here with the share and the scheduling it has always actually had.
    QUOTAS = {
        "free":       {"cpu": 0.1, "priority": 0, "queued": True},   # Article 310: zero-cost compliance
        "standard":   {"cpu": 0.1, "priority": 0, "queued": False},  # the platform default
        "pro":        {"cpu": 0.4, "priority": 1, "queued": False},
        "enterprise": {"cpu": 0.9, "priority": 2, "queued": False},
    }
    DEFAULT_TIER = "free"          # an unrecognised tier gets the most conservative declared tier

    @classmethod
    def resolve_tier(cls, tier: str) -> Dict[str, Any]:
        """(applied, recognised) for a requested tier - the single interpretation both stages use."""
        t = str(tier or "").strip().lower()
        known = t in cls.QUOTAS
        return {"tier_requested": tier, "tier_applied": t if known else cls.DEFAULT_TIER,
                "tier_recognised": known,
                "tier_basis": (f"'{tier}' is a declared tier" if known else
                               f"'{tier}' is not a declared tier ({', '.join(sorted(cls.QUOTAS))}), so the "
                               f"{cls.DEFAULT_TIER} tier applies to BOTH the share and the scheduling")}

    def allocate(self, user_id: str, tier: str, domain: str) -> Dict[str, Any]:
        resolved = self.resolve_tier(tier)
        config = {k: v for k, v in self.QUOTAS[resolved["tier_applied"]].items() if k != "queued"}
        logger.info(f"ARO: computed {config} for {user_id} ({resolved['tier_applied']}) in {domain}")

        return {
            "user_id": user_id,
            "domain": domain,
            "share": config,
            **resolved,
            # the pool this belongs to lives on a per-request optimiser instance and is discarded when
            # the response returns: nothing is held, so "ACTIVE" was a claim about state that ends here
            "status": "COMPUTED",
            "status_basis": ("a computed share for this request; no capacity is reserved or held beyond "
                             "the response"),
        }
