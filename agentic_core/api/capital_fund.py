"""
Sovereign Capital Fund & Marketplace API.

Manages the virtual capital allocation system for the VSB ecosystem:
- Sovereign Capital Fund: allocate, track, and report on virtual capital
- Marketplace: list, discover, and transact VSB products/services

  GET  /api/v1/fund/status          — fund health and allocation overview
  POST /api/v1/fund/allocate        — allocate capital to a project/VSB
  GET  /api/v1/fund/portfolio       — portfolio view of all allocations
  POST /api/v1/fund/report          — AI-generated fund performance report
  (the parallel marketplace routes this file once carried are RETIRED — W444; the real,
   §11-screened marketplace lives in agentic_core/api/marketplace.py)
  POST /api/v1/marketplace/value    — AI valuation for a product/service
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import atomic_write_json, data_path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1", tags=["capital-fund"])

_FUND_STORE = data_path("capital_fund.json")


def _load_fund() -> dict:
    # W444 (comment corrected by the refuter round: load_json_tolerant recovers a truncated
    # tail but does NOT quarantine) — on unrecoverable corruption the corrupt file is now
    # RENAMED ASIDE (.corrupt-<id>) before the fresh pool takes over, so the shared WST
    # endowment can never be silently reset with the evidence destroyed.
    from agentic_core.config import load_json_tolerant
    d = load_json_tolerant(_FUND_STORE, None) if _FUND_STORE.exists() else None
    if isinstance(d, dict):
        return d
    if _FUND_STORE.exists():
        try:
            _FUND_STORE.rename(_FUND_STORE.with_suffix(f".corrupt-{uuid.uuid4().hex[:8]}"))
        except OSError:
            pass
    return {
        "total_capital": 10_000_000,  # £10M sovereign capital pool (virtual)
        "currency": "WST",            # Workstation Token
        "allocated": 0,
        "available": 10_000_000,
        "allocations": [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _save_fund(fund: dict) -> None:
    _FUND_STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_FUND_STORE, fund)


def contribute_from_cycle(vsb_id: str, amount_wst: float) -> dict:
    """§12 (W294) — an entity's waterfall `capital_fund` stage COMPOUNDS into the Sovereign Capital
    Fund (the 'energy storage' stage genuinely stores): the shared pool grows by the contribution,
    attributed + UEG-logged. Previously the stage only wrote a ledger row — three disconnected WST
    pools with no compounding endowment. Virtual WST only."""
    # W444 — the fund is shared WST accounting: the read-modify-write runs under the store
    # lock (heartbeat contributions raced /fund/allocate as last-writer-wins).
    from agentic_core.config import store_lock
    amt = round(float(amount_wst), 2)
    with store_lock(_FUND_STORE):
        fund = _load_fund()
        fund["total_capital"] = round(float(fund.get("total_capital", 0)) + amt, 2)
        fund["available"] = round(float(fund.get("available", 0)) + amt, 2)
        entry = {"vsb_id": vsb_id, "amount_wst": amt,
                 "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        fund["cycle_contributions"] = (fund.get("cycle_contributions") or [])[-199:] + [entry]
        fund["cycle_contributions_total_wst"] = round(
            float(fund.get("cycle_contributions_total_wst", 0)) + amt, 2)
        _save_fund(fund)
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.capital_fund.contribution",
                         "vsb_id": vsb_id, "amount_wst": amt})
    except Exception:
        pass
    return entry



# ── Capital Fund ──────────────────────────────────────────────────────────────

def _organism_posture() -> dict:
    """Read the living organism's current energy/economic posture (§8) — best-effort, read-only, so the
    Sovereign Capital Fund reflects (and is governed by) the living system's state, not a detached ledger."""
    try:
        ctx = biobus.organism_context()
        return {"mode": ctx.get("mode"), "composite_health": ctx.get("composite_health"),
                "atp_ratio": (ctx.get("metabolic") or {}).get("atp_ratio")}
    except Exception:
        return {}


@router.get("/fund/status")
async def fund_status():
    """Return Sovereign Capital Fund health and overview, including the living organism's §8 posture."""
    fund = _load_fund()
    allocation_count = len(fund.get("allocations", []))
    utilisation = round(fund["allocated"] / fund["total_capital"] * 100, 1) if fund["total_capital"] else 0

    return {
        "total_capital": fund["total_capital"],
        "currency": fund["currency"],
        "allocated": fund["allocated"],
        "available": fund["available"],
        "utilisation_pct": utilisation,
        "allocation_count": allocation_count,
        "fund_health": "HEALTHY" if utilisation < 80 else "CONSTRAINED" if utilisation < 95 else "DEPLETED",
        "organism": _organism_posture(),
    }


class AllocateRequest(BaseModel):
    project_id: str
    project_name: str
    amount: float
    purpose: str
    domain: str = "general"
    realm: str = "enterprise"


@router.post("/fund/allocate")
async def allocate_capital(req: AllocateRequest):
    """Allocate virtual capital to a project or VSB entity.

    W444 refuter catch (reproduced): only contribute_from_cycle held the store lock — this
    read-modify-write raced it unlocked and erased contributions (total, row and running total
    all reverted). Both writers now serialise on the same lock."""
    from agentic_core.config import store_lock as _sl
    with _sl(_FUND_STORE):
        return _allocate_locked(req)


def _allocate_locked(req: "AllocateRequest"):
    fund = _load_fund()

    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive.")
    if req.amount > fund["available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient capital. Available: {fund['available']} WST, requested: {req.amount} WST."
        )

    # §8 survival instinct — the organism's posture governs capital deployment. ADVISORY only: virtual WST,
    # and real-money decisions are Owner-gated, so we never auto-block the allocation — we flag restraint when
    # the organism is energy-depleted and the tranche is a large fraction of remaining capital.
    posture = _organism_posture()
    atp = posture.get("atp_ratio")
    frac = req.amount / fund["available"] if fund["available"] else 1.0  # of capital available BEFORE this draw
    caution = None
    if isinstance(atp, (int, float)) and atp < 0.3 and frac > 0.25:
        caution = (f"§8 survival instinct: the organism is energy-depleted (ATP {atp:.0%}); this tranche is "
                   f"{frac:.0%} of available capital. Consider a smaller tranche or deferring until recovery.")

    allocation_id = f"alloc-{uuid.uuid4().hex[:8]}"
    allocation = {
        "allocation_id": allocation_id,
        "project_id": req.project_id,
        "project_name": req.project_name,
        "amount": req.amount,
        "purpose": req.purpose,
        "domain": req.domain,
        "realm": req.realm,
        "status": "active",
        "homeostasis_caution": caution,
        "allocated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    fund["allocated"] += req.amount
    fund["available"] -= req.amount
    fund["allocations"].append(allocation)
    _save_fund(fund)

    biobus.fire_signal(
        "motor", "fund.allocate",
        f"Capital allocated: {req.amount} WST → {req.project_name} [{req.domain}]",
        0.8,
    )

    return {
        "allocation_id": allocation_id,
        "amount": req.amount,
        "currency": fund["currency"],
        "remaining_available": fund["available"],
        "status": "allocated",
        "organism": posture,
        "homeostasis_caution": caution,
    }


@router.get("/fund/portfolio")
async def fund_portfolio():
    """Portfolio view of all capital allocations."""
    fund = _load_fund()
    allocations = fund.get("allocations", [])

    by_domain: dict[str, float] = {}
    by_realm: dict[str, float] = {}
    for a in allocations:
        by_domain[a.get("domain", "unknown")] = by_domain.get(a.get("domain", "unknown"), 0) + a["amount"]
        by_realm[a.get("realm", "unknown")] = by_realm.get(a.get("realm", "unknown"), 0) + a["amount"]

    return {
        "total_capital": fund["total_capital"],
        "allocated": fund["allocated"],
        "available": fund["available"],
        "currency": fund["currency"],
        "allocations": allocations,
        "allocation_count": len(allocations),
        "by_domain": by_domain,
        "by_realm": by_realm,
    }


class FundReportRequest(BaseModel):
    period: str = "current"
    focus: str = "performance"  # performance | risk | opportunity


@router.post("/fund/report")
async def generate_fund_report(req: FundReportRequest):
    """AI-generated Sovereign Capital Fund performance report."""
    fund = _load_fund()
    portfolio_summary = (
        f"Total capital: {fund['total_capital']} WST\n"
        f"Allocated: {fund['allocated']} WST ({round(fund['allocated']/fund['total_capital']*100, 1)}%)\n"
        f"Available: {fund['available']} WST\n"
        f"Active allocations: {len(fund.get('allocations', []))}\n"
    )

    if fund.get("allocations"):
        top_allocs = sorted(fund["allocations"], key=lambda x: x["amount"], reverse=True)[:5]
        portfolio_summary += "Top allocations:\n" + "\n".join(
            f"  - {a['project_name']} ({a['domain']}): {a['amount']} WST — {a['purpose']}"
            for a in top_allocs
        )

    prompt = (
        f"You are the Chief Investment Officer of a Sovereign Capital Fund. "
        f"Generate a {req.focus} report for the {req.period} period.\n\n"
        f"Portfolio summary:\n{portfolio_summary}\n\n"
        "Deliver:\n"
        "## Executive Summary\n"
        "## Portfolio Performance Analysis\n"
        "## Domain Allocation Analysis\n"
        "## Risk Assessment\n"
        "## Value Creation Highlights\n"
        "## Recommendations (capital reallocation, new opportunities)\n"
        "## Outlook\n"
    )

    biobus.fire_signal("cognitive", "fund.report", f"Fund report: {req.focus}/{req.period}", 0.5)
    # W444 — provenance: a floor-served scaffold used to ship as an unlabelled CIO analysis.
    meta = await gateway.query_meta(prompt, agent="fund_manager")
    biobus.record_operation("fund_report", "fund.report", success=True)

    return {
        "report_id": uuid.uuid4().hex[:10],
        "period": req.period,
        "focus": req.focus,
        "report": meta.get("output"),
        "served_by": meta.get("served_by"),
        "is_external": meta.get("is_external"),
        **({"floor_note": "structured floor — a deterministic outline, not model analysis"}
           if meta.get("served_by") == "native" else {}),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Marketplace ───────────────────────────────────────────────────────────────
# W444 — RETIRED: this file used to carry a PARALLEL marketplace (GET /marketplace/listings +
# POST /marketplace/list) writing to its own store. The GET was permanently shadowed by
# marketplace.py's identical path (registered first), so a listing created here returned
# status "active" while being invisible to every consumer forever — fabricated success — and
# the create path bypassed the §11 compliance screen, auth, ownership and bounds the real
# marketplace enforces. The real, screened create path is POST /api/v1/marketplace/listings.
# Only the AI valuation helper survives, with provenance fixed.


class ValuationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)   # empty is a legal stored state
    domain: str = "general"
    market_context: str = Field(default="", max_length=2000)


@router.post("/marketplace/value")
async def ai_valuation(req: ValuationRequest, user: dict | None = Depends(get_current_user)):
    """AI market-valuation assessment for a product or service. W444 — provenance-honest:
    refuses when only the deterministic floor would serve (a template cannot value anything),
    and carries served_by/is_external so the UI renders the provenance badge."""
    prompt = (
        f"You are a startup valuation expert. Provide a market valuation assessment.\n\n"
        f"Product/Service: {req.title}\n"
        f"Description: {req.description}\n"
        f"Domain: {req.domain}\n"
        + (f"Market context: {req.market_context}\n" if req.market_context else "")
        + "\nDeliver:\n"
        "## Valuation Summary (range in £ and WST equivalent)\n"
        "## Valuation Methodology Used\n"
        "## Market Comparable Analysis\n"
        "## Revenue Potential (Year 1, 3, 5 projections)\n"
        "## Key Value Drivers\n"
        "## Key Value Detractors / Risks\n"
        "## Recommended Pricing Strategy\n"
        "## Exit Multiple Estimate\n"
    )

    meta = await gateway.query_meta(prompt, agent="marketplace_valuation")
    if meta.get("served_by") == "native":
        raise HTTPException(status_code=503, detail=(
            "No model is available to produce a valuation — the deterministic floor can only "
            "emit an outline, and an outline presented as a valuation would be fabrication. "
            "Load a local model or enable an external provider (Owner-gated)."))

    return {
        "valuation_id": uuid.uuid4().hex[:10],
        "title": req.title,
        "domain": req.domain,
        "valuation": meta.get("output"),
        "served_by": meta.get("served_by"),
        "is_external": meta.get("is_external"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": "AI valuation for planning purposes only. Professional financial advice required for investment decisions.",
    }
