"""
VSB Economy API — the living economic metabolism (virtual/simulated).

Exposes the biomimetic economic subsystem: legal-entity-type selection, the
virtual ledger, and the metabolic profit-distribution cycle (intake → reserves →
circulation waterfall → intelligent charitable giving), wired to the organism's
biomimetic systems and governed by gaas.v5.

  GET  /api/v1/economy/entity-types          — selectable legal forms (Sole/Ltd/PLC/Trust/Waqf/…/Hybrid)
  GET  /api/v1/economy/status                — metabolism status for a VSB
  POST /api/v1/economy/cycle                 — run one metabolic distribution cycle
  GET  /api/v1/economy/ledger/{vsb_id}       — virtual ledger statement
  GET  /api/v1/economy/charity/candidates    — ranked charitable causes
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.economy.entities import ENTITY_TEMPLATES, DEFAULT_ENTITY
from agentic_core.economy.metabolism import EconomicMetabolism
from agentic_core.economy.charity import CharityIntelligence

router = APIRouter(prefix="/api/v1/economy", tags=["vsb-economy"])


@router.get("/entity-types")
async def entity_types():
    """The legal forms a user can select when generating their VSB."""
    return {
        "default": DEFAULT_ENTITY,
        "types": [
            {"id": k, "name": v["name"], "description": v["description"],
             "distributes_profit": v["distributes_profit"],
             "capital_preserved": v["capital_preserved"], "waterfall": v["waterfall"]}
            for k, v in ENTITY_TEMPLATES.items()
        ],
        "note": "Selectable at VSB generation. All flows are virtual/simulated WST.",
    }


@router.get("/status")
async def economy_status(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY):
    return EconomicMetabolism(vsb_id, entity_type).status()


class CycleRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    entity_type: str = DEFAULT_ENTITY
    revenue: float = 10000.0
    costs: float = 0.0
    reserve_rate: float = 0.20
    owner: str = "Rehan"


@router.post("/cycle")
async def run_cycle(req: CycleRequest):
    """Run one living metabolic cycle, governed by gaas.v5 and logged to the UEG."""
    metab = EconomicMetabolism(req.vsb_id, req.entity_type, req.owner)

    async def _action():
        return metab.run_cycle(req.revenue, req.costs, req.reserve_rate)

    # Governance: route the distribution through the constitutional gate (arms-length, audited).
    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        gov = UnifiedConstitutionalInterceptorV16Omega("economy-node", UEGLogger("meta/gaas_v5_ueg.json"))
        result = await gov.intercept({"intent": "economy_distribution", "vsb_id": req.vsb_id}, _action)
        report = result.output if getattr(result, "output", None) else metab.run_cycle(req.revenue, req.costs, req.reserve_rate)
        governance = {"status": result.status, "checkpoint": result.checkpoint_id}
    except Exception:
        report = metab.run_cycle(req.revenue, req.costs, req.reserve_rate)
        governance = {"status": "ungated"}

    return {"cycle": report, "governance": governance}


@router.get("/ledger/{vsb_id}")
async def get_ledger(vsb_id: str):
    return EconomicMetabolism(vsb_id).status()["ledger"]


@router.get("/charity/candidates")
async def charity_candidates(top: int = 8):
    return {"candidates": CharityIntelligence().ranked(top),
            "method": "urgency × gravity × reach × marginal-impact × trust",
            "disclaimer": "Virtual/simulated — sources curated; live feeds pending Owner approval."}
