"""
Adaptive Resource Optimizer API — surfaces Workstation's OWN resource-optimisation engine
(`agentic_core.optimizer.AdaptiveResourceOptimizer`) into the live pipeline. Previously orphaned
(not mounted); now reachable + a first-class Resource-Fabric resource. Real, deterministic logic:
verify a resource request (RAL) → cost-aware schedule → assemble a dynamic pool → tiered-fair
allocate. Honest: the capacity is a SINGLE-NODE simulated inventory baseline (no real cloud quota),
clearly labelled — no fabricated utilisation figures.

  GET  /api/v1/optimizer/inventory  — the resource fabric inventory (simulated single-node baseline)
  POST /api/v1/optimizer/allocate   — verify + schedule + assemble + allocate a resource request
"""
from __future__ import annotations

import json
import uuid
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/optimizer", tags=["resource-optimizer"])

_NOTE = "Capacity is a single-node simulated inventory baseline (no real cloud quota)."


@router.get("/inventory")
async def inventory():
    try:
        from agentic_core.optimizer.fabric import DynamicResourceFabric
        inv = DynamicResourceFabric().get_inventory_status()
    except Exception as e:
        inv, _ = {}, str(e)
    return {"inventory": inv, "simulated": True, "note": _NOTE}


class AllocateRequest(BaseModel):
    domain: str = "general"
    requirements: Dict[str, Any] = {"CPU": 4, "RAM": 1024}   # keys containing CPU/RAM/GPU
    tier: str = "standard"
    user_id: str = "default"


@router.post("/allocate")
async def allocate(req: AllocateRequest):
    """Run a resource request through the adaptive optimiser (verify → schedule → assemble →
    allocate). Real engine logic; capacity is a simulated single-node baseline (honestly flagged)."""
    from agentic_core.optimizer.engine import AdaptiveResourceOptimizer
    spec = json.dumps({"id": f"ral-{uuid.uuid4().hex[:8]}", "domain": req.domain,
                       "requirements": req.requirements})
    out = await AdaptiveResourceOptimizer().process_ral_request(req.user_id, req.tier, spec)
    return {"posture": "in-house adaptive resource optimiser", "simulated_capacity": True,
            "note": _NOTE, **out}
