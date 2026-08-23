"""
Marketplace API — real JSON-persisted product listings + WST purchase.

Routes (all under /api/v1/marketplace):
  GET  /listings            — all listings (platform catalog + user listings)
  POST /listings            — create a new user listing
  GET  /listings/{id}       — single listing
  PATCH /listings/{id}      — update (owner only — no auth in MVP, uses creator_id field)
  DELETE /listings/{id}     — delete listing
  POST /listings/{id}/purchase — deduct WST from token ledger, record sale

Also exposes:
  GET /api/v230/marketplace/products — backward-compat alias for old frontend calls
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from agentic_core.config import atomic_write_json, data_path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.auth.core import get_current_user, request_owner_id, user_can_access

router = APIRouter(tags=["Marketplace"])

_LISTINGS_DIR = Path((os.getenv("LISTINGS_DIR") or str(data_path("marketplace"))))
_LISTINGS_DIR.mkdir(parents=True, exist_ok=True)

# ── Models ────────────────────────────────────────────────────────────────────

class Listing(BaseModel):
    id: str = ""
    name: str
    description: str = ""
    author: str = "Community"
    category: str = "Product"
    price_wst: float = 0.0
    tier: str = "Standard"
    tags: list[str] = []
    certified: bool = False
    status: str = "active"   # active | sold_out | draft | held (W322 — §11 FAIL)
    compliance: dict = {}    # §11 (W322) — the listing's real screen verdict (overall + verdicts)
    sales_count: int = 0
    created_at: float = 0.0
    updated_at: float = 0.0
    creator_id: str = "community"
    # W293 — optional VSB attribution: sales of this listing are recognised as that VSB's revenue
    vsb_id: str = ""

class CreateListingRequest(BaseModel):
    name: str
    description: str = ""
    author: str = "Community"
    category: str = "Product"
    price_wst: float = 0.0
    tier: str = "Standard"
    tags: list[str] = []
    creator_id: str = "community"
    vsb_id: str = ""

class PurchaseRequest(BaseModel):
    user_id: str = "demo_user"
    quantity: int = 1


# ── Persistence helpers ───────────────────────────────────────────────────────

def _listing_path(listing_id: str) -> Path:
    return _LISTINGS_DIR / f"{listing_id}.json"

def _load(listing_id: str) -> Listing:
    p = _listing_path(listing_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Listing {listing_id} not found")
    return Listing(**json.loads(p.read_text()))

def _save(listing: Listing) -> Listing:
    listing.updated_at = time.time()
    atomic_write_json(_listing_path(listing.id), listing.model_dump())
    return listing

def _all_listings() -> list[Listing]:
    listings = []
    for f in sorted(_LISTINGS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            listings.append(Listing(**json.loads(f.read_text())))
        except Exception:
            pass
    return listings

def _seed_platform_listings():
    """Seed built-in platform listings on first boot if the store is empty."""
    if any(_LISTINGS_DIR.glob("*.json")):
        return
    seeds = [
        {"name": "Sovereign Synthesis Pack", "description": "Full Synthesis Studio access with unlimited document generation, AI summarisation, and export to any format.", "author": "Workstation Core", "category": "Platform", "price_wst": 5000, "tier": "Pro", "tags": ["synthesis","ai","documents"], "certified": True, "creator_id": "platform"},
        {"name": "Digital Reactor — Religion Domain", "description": "Plug-in domain reactor for Islamic jurisprudence processing, consensus validation, and fatwa generation.", "author": "Workstation CoE", "category": "Reactor", "price_wst": 8000, "tier": "Enterprise", "tags": ["religion","reactor","ai"], "certified": True, "creator_id": "platform"},
        {"name": "Capital Intelligence Module", "description": "AI-powered portfolio analysis, governance proposals tracker, and Sovereign Vault integration.", "author": "Workstation CoE", "category": "Analytics", "price_wst": 12000, "tier": "Enterprise", "tags": ["capital","analytics","governance"], "certified": True, "creator_id": "platform"},
        {"name": "AI CEO Consultation Bundle", "description": "Unlimited AI CEO chat sessions with persistent ChromaDB memory across all realms and domains.", "author": "Workstation Core", "category": "AI Agent", "price_wst": 3000, "tier": "Standard", "tags": ["ceo","ai","chat"], "certified": True, "creator_id": "platform"},
        {"name": "Forge Multi-Step Pipeline Pack", "description": "Unlock unlimited pipeline steps in the AI Forge with LLM, Search, Memory, and Guardrail nodes.", "author": "Workstation Core", "category": "Developer", "price_wst": 4500, "tier": "Pro", "tags": ["forge","pipeline","developer"], "certified": True, "creator_id": "platform"},
        {"name": "Incubator Evolution Engine Pro", "description": "Run 5-variant prompt tournaments with advanced fitness scoring and auto-export of winning prompts.", "author": "Community", "category": "Developer", "price_wst": 2000, "tier": "Standard", "tags": ["incubator","evolution","prompts"], "certified": False, "creator_id": "community"},
    ]
    for s in seeds:
        lid = uuid.uuid4().hex[:12]
        listing = Listing(
            id=lid,
            created_at=time.time(),
            updated_at=time.time(),
            status="active",
            **s,
        )
        atomic_write_json(_listing_path(lid), listing.model_dump())

_seed_platform_listings()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/v1/marketplace/listings")
async def list_marketplace_listings(
    category: Optional[str] = None,
    search: Optional[str] = None,
    certified_only: bool = False,
) -> list[dict]:
    # §11 (W322) — held listings never surface on the public marketplace
    listings = [l for l in _all_listings() if l.status != "held"]
    if category:
        listings = [l for l in listings if l.category.lower() == category.lower()]
    if certified_only:
        listings = [l for l in listings if l.certified]
    if search:
        q = search.lower()
        listings = [l for l in listings if q in l.name.lower() or q in l.description.lower() or any(q in t for t in l.tags)]
    return [l.model_dump() for l in listings if l.status != "draft"]


def _require_vsb_attribution(vsb_id: str, user: dict | None) -> None:
    """§14×§12 (W311) — a listing may only be revenue-attributed to a VSB the CALLER owns:
    previously any caller could point vsb_id at another tenant's entity and inject spoofed
    marketplace revenue into its economy. 404 (never 403) — the entity is never confirmed.
    Single-user mode (auth off) is unguarded by design: there is no tenant boundary to protect,
    and registered-only entities (no full record) must stay attributable (back-compat)."""
    if not vsb_id:
        return
    from agentic_core.auth.core import auth_enabled
    if not auth_enabled():
        return
    from agentic_core.api.vsb import _load_vsb
    vsb = _load_vsb(vsb_id)
    if not vsb or not user_can_access(user, vsb.get("owner_id")):
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")


def _screen_listing(name: str, description: str, tags: list) -> dict:
    """§11 (W322) — the marketplace is INSIDE the compliance perimeter: every listing's public
    text (name + description + tags) is screened by the real engines. overall='fail' → the
    listing is HELD (never active, never purchasable) until an edit re-screens clean.
    Previously a haram listing went live and was purchasable with zero screening."""
    try:
        from agentic_core.api.compliance import screen_compliance
        s = screen_compliance(f"{name}\n{description}\n{' '.join(tags or [])}")
        return {"overall": s.get("overall"), "compliant": s.get("compliant"),
                "verdicts": s.get("verdicts")}
    except Exception as exc:   # a screen fault never silently passes NOR blocks — recorded honestly
        return {"overall": "error", "error": str(exc)[:160]}


@router.post("/api/v1/marketplace/listings")
async def create_listing(req: CreateListingRequest,
                         user: dict | None = Depends(get_current_user)) -> dict:
    if user is not None and not isinstance(user, dict):
        user = None
    _require_vsb_attribution(req.vsb_id, user)
    _screen = _screen_listing(req.name, req.description, req.tags)
    lid = uuid.uuid4().hex[:12]
    listing = Listing(
        id=lid,
        name=req.name,
        description=req.description,
        author=req.author,
        category=req.category,
        price_wst=req.price_wst,
        tier=req.tier,
        tags=req.tags,
        # §14 (W311) — attribution is server-stamped under auth; a client cannot claim another creator
        creator_id=request_owner_id(user, req.creator_id),
        vsb_id=req.vsb_id,
        certified=False,
        status="held" if _screen.get("overall") == "fail" else "active",   # §11 (W322)
        compliance=_screen,
        created_at=time.time(),
        updated_at=time.time(),
    )
    _save(listing)
    if listing.status == "held":
        try:
            from agentic_core.gaas.v5 import UEGLogger
            UEGLogger().log({"type": "marketplace.listing_held", "listing_id": lid,
                             "overall": _screen.get("overall"),
                             "note": "§11 screen FAIL — held off the marketplace until re-screened clean"})
        except Exception:
            pass
    return listing.model_dump()


@router.get("/api/v1/marketplace/listings/{listing_id}")
async def get_listing(listing_id: str) -> dict:
    return _load(listing_id).model_dump()


@router.patch("/api/v1/marketplace/listings/{listing_id}")
async def update_listing(listing_id: str, patch: dict,
                         user: dict | None = Depends(get_current_user)) -> dict:
    if user is not None and not isinstance(user, dict):
        user = None
    listing = _load(listing_id)
    # §14 (W311) — mutations are OWNER-SCOPED (404, never 403); attribution fields are immutable
    # by patch; re-pointing vsb_id requires ownership of the TARGET entity.
    if not user_can_access(user, listing.creator_id):
        raise HTTPException(status_code=404, detail=f"Listing {listing_id} not found")
    if "vsb_id" in patch and patch.get("vsb_id") != listing.vsb_id:
        _require_vsb_attribution(str(patch.get("vsb_id") or ""), user)
    for k, v in patch.items():
        if k not in ("id", "created_at", "certified", "creator_id", "sales_count",
                     "compliance", "status") and hasattr(listing, k):
            setattr(listing, k, v)
    # §11 (W322) — a public-text edit RE-SCREENS; a clean re-screen is the ONLY way off hold,
    # and a failing edit puts an active listing on hold (status/compliance are never patchable).
    if any(k in patch for k in ("name", "description", "tags")) or listing.status == "held":
        listing.compliance = _screen_listing(listing.name, listing.description, listing.tags)
        listing.status = ("held" if listing.compliance.get("overall") == "fail"
                          else ("active" if listing.status == "held" else listing.status))
    return _save(listing).model_dump()


@router.delete("/api/v1/marketplace/listings/{listing_id}")
async def delete_listing(listing_id: str,
                         user: dict | None = Depends(get_current_user)) -> dict:
    if user is not None and not isinstance(user, dict):
        user = None
    p = _listing_path(listing_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Listing not found")
    if not user_can_access(user, _load(listing_id).creator_id):    # W311 — owner-scoped, 404-never-403
        raise HTTPException(status_code=404, detail="Listing not found")
    p.unlink()
    return {"deleted": listing_id}


@router.post("/api/v1/marketplace/listings/{listing_id}/purchase")
async def purchase_listing(listing_id: str, req: PurchaseRequest,
                           user: dict | None = Depends(get_current_user)) -> dict:
    """
    Deduct WST from the user's token ledger and record the sale.
    Returns purchase receipt.
    §14 (W317): under auth the purchase is CALLER-BOUND — tokens are deducted from the
    authenticated user's own ledger; a caller-supplied user_id can no longer spend another
    tenant's WST. Single-user mode keeps the request value (back-compat).
    """
    from agentic_core.auth.core import request_owner_id
    req.user_id = request_owner_id(user if isinstance(user, dict) else None, req.user_id)
    listing = _load(listing_id)
    if listing.status == "sold_out":
        raise HTTPException(status_code=409, detail="Listing is sold out")
    if listing.status == "held":   # §11 (W322) — a FAIL-screened listing is not purchasable
        raise HTTPException(status_code=409,
                            detail="Listing is held by the §11 compliance screen and cannot be purchased.")

    total_cost = listing.price_wst * req.quantity

    if total_cost > 0:
        try:
            from agentic_core.commercial.token_ledger import TokenLedger, UserTier
            ledger = TokenLedger()
            # Ensure user exists with at least a free tier
            ledger.initialize_user(req.user_id, UserTier.FREE)
            success = ledger.consume_tokens(req.user_id, total_cost, f"Purchase: {listing.name}")
            if not success:
                raise HTTPException(
                    status_code=402,
                    detail=f"Insufficient WST balance. Required: {total_cost} WST."
                )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Ledger error: {exc}")

    # Record sale
    listing.sales_count += req.quantity
    _save(listing)

    receipt = {
        "receipt_id": uuid.uuid4().hex[:16],
        "listing_id": listing_id,
        "listing_name": listing.name,
        "user_id": req.user_id,
        "quantity": req.quantity,
        "total_cost_wst": total_cost,
        "purchased_at": time.time(),
        "status": "confirmed",
    }
    # Persist receipt
    receipts_dir = data_path("marketplace/receipts")
    receipts_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(receipts_dir / f"{receipt['receipt_id']}.json", receipt)

    # W293 (§12×§5) — a sale of a VSB-attributed listing is RECOGNISED as that VSB's revenue: the
    # same WST the buyer's TokenLedger deducted feeds the seller's next autonomous economy cycle
    # (two ledgers, one flow, counted once per side). Best-effort — recognition failure never
    # breaks the purchase.
    if total_cost > 0 and getattr(listing, "vsb_id", ""):
        try:
            from agentic_core.economy.revenue import record_event
            record_event(listing.vsb_id, "revenue", total_cost, "marketplace_sale",
                         ref=receipt["receipt_id"],
                         note=f"sale of '{listing.name}' ×{req.quantity} (virtual WST)")
            receipt["revenue_recognised_for"] = listing.vsb_id
        except Exception:
            pass

    return receipt


# ── Backward-compat alias (old frontend calls /api/v230/marketplace/products) ─

@router.get("/api/v230/marketplace/products")
async def marketplace_products_v230() -> list[dict]:
    """Backward-compat alias — returns active listings in the old product shape."""
    listings = [l for l in _all_listings() if l.status == "active"]
    return [
        {
            "id": l.id,
            "name": l.name,
            "author": l.author,
            "price": l.price_wst,
            "category": l.category,
            "certified": l.certified,
            "description": l.description,
        }
        for l in listings
    ]
