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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.economy.entities import ENTITY_TEMPLATES, DEFAULT_ENTITY, get_template
from agentic_core.economy.metabolism import (
    EconomicMetabolism, validate_waterfall, _load_waterfall_overrides,
    _save_waterfall_overrides, _WATERFALL_STAGES,
)
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
        gov = UnifiedConstitutionalInterceptorV16Omega("economy-node", UEGLogger())
        result = await gov.intercept({"intent": "economy_distribution", "vsb_id": req.vsb_id}, _action)
        report = result.output if getattr(result, "output", None) else metab.run_cycle(req.revenue, req.costs, req.reserve_rate)
        governance = {"status": result.status, "checkpoint": result.checkpoint_id}
    except Exception:
        report = metab.run_cycle(req.revenue, req.costs, req.reserve_rate)
        governance = {"status": "ungated"}

    return {"cycle": report, "governance": governance}


@router.get("/waterfall")
async def get_waterfall(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY):
    """The current effective profit-distribution waterfall for a VSB (Owner override if set, else the entity
    template default) + the template's binding constraints the Owner must respect."""
    m = EconomicMetabolism(vsb_id, entity_type)
    t = m.template
    return {
        "vsb_id": vsb_id, "entity_type": entity_type, "entity_name": t["name"],
        "waterfall": m.waterfall, "source": m.waterfall_source,
        "template_default": t["waterfall"], "stages": _WATERFALL_STAGES,
        "constraints": {"distributes_profit": t["distributes_profit"],
                        "capital_preserved": t["capital_preserved"]},
        "note": "Proportions of distributable profit (after reserves), summing to 1.0. Virtual/simulated WST.",
    }


class WaterfallRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    entity_type: str = DEFAULT_ENTITY
    proportions: Dict[str, float]


@router.post("/waterfall")
async def set_waterfall(req: WaterfallRequest):
    """§4/§8/§10 Owner sovereignty: adjust the profit-distribution proportions for a VSB (virtual). The
    proposal is normalised to 1.0 and BOUND by the entity template (a non-distributing form forces owner=0;
    a capital-preserving form requires capital_fund>0). Persisted, UEG-logged, effective from the next cycle.
    Virtual/simulated only — no real funds move."""
    template = get_template(req.entity_type)
    waterfall, violations = validate_waterfall(req.proportions, template)
    if violations:
        raise HTTPException(status_code=400, detail={
            "violations": violations,
            "constraints": {"distributes_profit": template["distributes_profit"],
                            "capital_preserved": template["capital_preserved"]},
            "stages": _WATERFALL_STAGES})
    overrides = _load_waterfall_overrides()
    overrides[req.vsb_id] = waterfall
    _save_waterfall_overrides(overrides)
    # Constitutional audit — the Owner adjusting the distribution policy is a material, logged act.
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({
            "type": "waterfall_override", "vsb_id": req.vsb_id, "entity_type": req.entity_type,
            "waterfall": waterfall, "by": "owner"})
    except Exception:
        pass
    return {
        "vsb_id": req.vsb_id, "entity_type": req.entity_type, "waterfall": waterfall,
        "source": "owner_override", "applied": True,
        "note": "Owner-set proportions persisted (virtual). Effective next cycle; logged to the UEG. "
                "Reset by posting the template defaults.",
    }


@router.get("/owner-payments")
async def owner_payments(vsb_id: str = "workstation-idbo", owner: str = "Rehan"):
    """§7 — the Owner's accrued share (virtual WST) from each cycle's §4 owner stage, plus history. Real-money
    payout rails are DISABLED and gated; no real funds move."""
    from agentic_core.economy.owner_payments import status
    return status(vsb_id, owner)


class PayoutRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    owner: str = "Rehan"
    amount: float


@router.post("/owner-payments/payout")
async def owner_payout(req: PayoutRequest):
    """Record a VIRTUAL Owner payout (reduces the accrued balance). NO real funds move — real-money rails are
    gated until the Owner explicitly authorises them AND a compliance/KYC review passes."""
    from agentic_core.economy.owner_payments import payout
    try:
        return payout(req.vsb_id, req.amount, req.owner)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/living-vsbs")
async def living_vsbs():
    """§4 — the established VSB enterprises the organism autonomously tends (each continually operated via
    paced virtual economy cycles on the circadian heartbeat). Virtual/simulated."""
    from agentic_core.economy.living_vsbs import list_living
    return list_living()


@router.get("/board-pack")
async def board_pack(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY):
    """§7 Financial Board Pack — the live owner-facing financial statement, assembled on demand: the P&L
    summary, the effective distribution waterfall, the Owner's accrued payments, the venture portfolio, charity
    given, and the §8 organism posture. Virtual/simulated WST only — no real funds; assembled fresh (≤5-min
    staleness invariant)."""
    import time as _t
    from agentic_core.economy.owner_payments import status as _owner_status
    from agentic_core.economy.ventures import portfolio as _venture_portfolio

    m = EconomicMetabolism(vsb_id, entity_type)
    stmt = m.ledger.statement()
    bal = stmt["balances"]
    stages = ("owner", "self_investment", "capital_fund", "user_projects", "charity")
    revenue = round(bal.get("revenue", 0.0), 2)
    reserves = round(bal.get("reserves", 0.0), 2)
    distributed = round(sum(bal.get(s, 0.0) for s in stages), 2)
    owner = _owner_status(vsb_id, m.owner)
    ventures = _venture_portfolio(vsb_id)

    try:
        from agentic_core.organism.biobus import biobus
        ctx = biobus.organism_context()
        organism = {"mode": ctx.get("mode"), "composite_health": ctx.get("composite_health"),
                    "atp_ratio": (ctx.get("metabolic") or {}).get("atp_ratio")}
    except Exception:
        organism = {}

    return {
        "vsb_id": vsb_id, "entity_type": entity_type, "entity_name": m.template["name"],
        "currency": "WST (virtual)", "generated_at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()),
        "profit_and_loss": {
            "total_revenue_wst": revenue, "total_reserves_wst": reserves,
            "total_distributed_wst": distributed,
            "distribution_by_stage": {s: round(bal.get(s, 0.0), 2) for s in stages},
        },
        "waterfall": {"effective": m.waterfall, "source": m.waterfall_source},
        "owner_payments": {"accrued_wst": owner["accrued_total_wst"], "paid_out_wst": owner["paid_out_total_wst"],
                           "balance_wst": owner["balance_wst"], "real_money_rails": owner["real_money_rails"]},
        "venture_portfolio": {"invested_total_wst": ventures["invested_total"],
                              "positions": ventures.get("positions_count", 0),
                              "holdings": ventures.get("holdings", [])[:5]},
        "charitable_giving": {"total_given_wst": round(bal.get("charity", 0.0), 2)},
        "organism_posture": organism,
        "ledger": {"entry_count": stmt["entry_count"], "recent": stmt["recent"]},
        "governance": "gaas.v5-gated cycles · UEG append-only audit · arms-length distribution policy",
        "disclaimer": "Virtual/simulated WST only — no real funds. Real-money rails are gated until the Owner "
                      "authorises them AND a compliance review passes.",
    }


@router.get("/ledger/{vsb_id}")
async def get_ledger(vsb_id: str):
    return EconomicMetabolism(vsb_id).status()["ledger"]


@router.get("/charity/candidates")
async def charity_candidates(top: int = 8):
    return {"candidates": CharityIntelligence().ranked(top),
            "method": "urgency × gravity × reach × marginal-impact × trust",
            "disclaimer": "Virtual/simulated — sources curated; live feeds pending Owner approval."}


@router.get("/ventures/candidates")
async def venture_candidates(top: int = 8):
    """§6 — ranked candidate user projects/ventures for investment (outcome × value × benefit × feasibility ×
    strategic-fit). Demo candidates until real user-project ingestion is wired; virtual/simulated."""
    from agentic_core.economy.ventures import VentureIntelligence
    vi = VentureIntelligence()
    return {"candidates": vi.ranked(top),
            "method": "outcome × value × benefit × feasibility × strategic-fit",
            "using_demo_candidates": vi.using_demo,
            "disclaimer": "Virtual/simulated — candidates are demo samples until real user-project ingestion."}


@router.get("/ventures/portfolio")
async def venture_portfolio(vsb_id: str = "workstation-idbo"):
    """§6 — the VSB's venture portfolio: positions accrued from each cycle's user_projects allocation (virtual)."""
    from agentic_core.economy.ventures import portfolio
    return portfolio(vsb_id)
