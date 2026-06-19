"""
Sovereign Capital Fund & Marketplace API.

Manages the virtual capital allocation system for the VSB ecosystem:
- Sovereign Capital Fund: allocate, track, and report on virtual capital
- Marketplace: list, discover, and transact VSB products/services

  GET  /api/v1/fund/status          — fund health and allocation overview
  POST /api/v1/fund/allocate        — allocate capital to a project/VSB
  GET  /api/v1/fund/portfolio       — portfolio view of all allocations
  POST /api/v1/fund/report          — AI-generated fund performance report
  GET  /api/v1/marketplace/listings — browse available VSB products/services
  POST /api/v1/marketplace/list     — list a new product/service
  POST /api/v1/marketplace/value    — AI valuation for a product/service
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1", tags=["capital-fund"])

_FUND_STORE = Path("data/capital_fund.json")
_MARKET_STORE = Path("data/marketplace_listings.json")


def _load_fund() -> dict:
    if _FUND_STORE.exists():
        try:
            return json.loads(_FUND_STORE.read_text())
        except Exception:
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
    _FUND_STORE.write_text(json.dumps(fund, indent=2))


def _load_listings() -> list[dict]:
    if _MARKET_STORE.exists():
        try:
            return json.loads(_MARKET_STORE.read_text())
        except Exception:
            pass
    return []


def _save_listings(listings: list[dict]) -> None:
    _MARKET_STORE.parent.mkdir(parents=True, exist_ok=True)
    _MARKET_STORE.write_text(json.dumps(listings, indent=2))


# ── Capital Fund ──────────────────────────────────────────────────────────────

@router.get("/fund/status")
async def fund_status():
    """Return Sovereign Capital Fund health and overview."""
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
    """Allocate virtual capital to a project or VSB entity."""
    fund = _load_fund()

    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive.")
    if req.amount > fund["available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient capital. Available: {fund['available']} WST, requested: {req.amount} WST."
        )

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
        "allocated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    fund["allocated"] += req.amount
    fund["available"] -= req.amount
    fund["allocations"].append(allocation)
    _save_fund(fund)

    return {
        "allocation_id": allocation_id,
        "amount": req.amount,
        "currency": fund["currency"],
        "remaining_available": fund["available"],
        "status": "allocated",
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

    report = await gateway.query(prompt, agent="fund_manager")

    return {
        "report_id": uuid.uuid4().hex[:10],
        "period": req.period,
        "focus": req.focus,
        "report": report,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Marketplace ───────────────────────────────────────────────────────────────

@router.get("/marketplace/listings")
async def get_listings(domain: str = "", realm: str = ""):
    """Browse VSB marketplace listings."""
    listings = _load_listings()
    if domain:
        listings = [l for l in listings if l.get("domain", "").lower() == domain.lower()]
    if realm:
        listings = [l for l in listings if l.get("realm", "").lower() == realm.lower()]
    return {"listings": listings, "total": len(listings)}


class ListingRequest(BaseModel):
    title: str
    description: str
    product_type: str = "service"  # product | service | platform | dataset | model
    domain: str = "general"
    realm: str = "enterprise"
    price_wst: float = 0.0
    seller_entity_id: str = ""


@router.post("/marketplace/list")
async def create_listing(req: ListingRequest):
    """List a new product or service on the VSB marketplace."""
    listings = _load_listings()
    listing_id = f"mkt-{uuid.uuid4().hex[:8]}"
    listing = {
        "listing_id": listing_id,
        "title": req.title,
        "description": req.description,
        "product_type": req.product_type,
        "domain": req.domain,
        "realm": req.realm,
        "price_wst": req.price_wst,
        "seller_entity_id": req.seller_entity_id,
        "status": "active",
        "listed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "views": 0,
        "enquiries": 0,
    }
    listings.append(listing)
    _save_listings(listings)
    return listing


class ValuationRequest(BaseModel):
    title: str
    description: str
    domain: str = "general"
    market_context: str = ""


@router.post("/marketplace/value")
async def ai_valuation(req: ValuationRequest):
    """AI-generated market valuation for a product or service."""
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

    valuation = await gateway.query(prompt, agent="marketplace_valuation")

    return {
        "valuation_id": uuid.uuid4().hex[:10],
        "title": req.title,
        "domain": req.domain,
        "valuation": valuation,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": "AI valuation for planning purposes only. Professional financial advice required for investment decisions.",
    }
