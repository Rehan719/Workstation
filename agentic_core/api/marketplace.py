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
from pydantic import BaseModel, Field

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
    # W392 — where this listing came from, so the UI never has to guess:
    #   "catalog" → derived from a REAL registered product; identity is a fact, price is unset.
    #   "user"    → created by someone through POST /listings, with a price they chose.
    origin: str = "user"
    route: str = ""          # the real in-app route for a catalog-derived listing ("" otherwise)
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
    quantity: int = Field(default=1, ge=1, le=1000)   # W444 — 0/negative quantities were accepted


# ── Persistence helpers ───────────────────────────────────────────────────────

def _listing_path(listing_id: str) -> Path:
    return _LISTINGS_DIR / f"{listing_id}.json"


def _read_doc(path: Path) -> dict | None:
    """Read a listing file whatever encoding it was written in.

    W392 — a real listing in the dev store held byte 0x97 (a cp1252 em-dash), and this mattered more
    than it looks. `read_text()` with no encoding uses the PLATFORM default: cp1252 on Windows, where
    it happens to decode, and UTF-8 on Linux, where it raises. `_all_listings` swallowed that with a
    bare `except: pass`, so the same store showed the listing in Windows development and silently
    DROPPED it in Linux CI and production. Decode explicitly, widest-compatible last, and never let a
    legacy encoding make a record disappear.
    """
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.loads(path.read_text(encoding=enc))
        except UnicodeDecodeError:
            continue
        except (OSError, ValueError):
            return None
    return None


def _load(listing_id: str) -> Listing:
    p = _listing_path(listing_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Listing {listing_id} not found")
    doc = _read_doc(p)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Listing {listing_id} not found")
    return Listing(**doc)

def _save(listing: Listing) -> Listing:
    listing.updated_at = time.time()
    atomic_write_json(_listing_path(listing.id), listing.model_dump())
    return listing

def _all_listings() -> list[Listing]:
    listings = []
    for f in sorted(_LISTINGS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        doc = _read_doc(f)
        if doc is None:
            continue
        try:
            listings.append(Listing(**doc))
        except Exception:
            pass
    return listings

# W392 — the six listings this module used to write at first boot. Every one was invented: a made-up
# product ("Sovereign Synthesis Pack"), a made-up price (5,000 WST), and `certified: True` asserted by
# nobody. They were never shown, because the frontend deliberately refused to display them — but they
# sat in the data store as if real, and any API consumer would have read them as certified products.
# They are retired on boot and replaced by listings derived from the REAL product catalogue.
_INVENTED_SEED_NAMES = {
    "Sovereign Synthesis Pack",
    "Digital Reactor — Religion Domain",
    "Capital Intelligence Module",
    "AI CEO Consultation Bundle",
    "Forge Multi-Step Pipeline Pack",
    "Incubator Evolution Engine Pro",
}


def _retire_invented_seeds() -> list[str]:
    """Remove the fabricated demo listings. Anything with a recorded sale is KEPT and reported —
    a receipt must never point at a listing that vanished, even a fabricated one."""
    removed, kept = [], []
    for path in _LISTINGS_DIR.glob("*.json"):
        doc = _read_doc(path)
        if doc is None:
            continue
        if doc.get("name") in _INVENTED_SEED_NAMES and doc.get("creator_id") in {"platform", "community"}:
            if doc.get("sales_count"):
                # A recorded sale means a receipt points here, so the record must survive. But it
                # must stop ASSERTING things nobody established: the invented certification is
                # dropped and the listing is moved to "draft", which the public list already filters
                # out while GET /listings/{id} still resolves it for the receipt. Retained, not
                # advertised.
                if doc.get("certified") or doc.get("status") != "draft":
                    doc["certified"] = False
                    doc["status"] = "draft"
                    doc["description"] = (
                        (doc.get("description") or "").rstrip()
                        + " [Retired sample listing: retained because it carries a recorded sale. "
                          "Its original 'certified' flag was asserted by no certifying process.]"
                    ).strip()
                    doc["updated_at"] = time.time()
                    atomic_write_json(path, doc)
                kept.append(doc.get("name", "?"))
                continue
            try:
                path.unlink()
                removed.append(doc.get("name", "?"))
            except OSError:
                pass
    if kept:
        import logging
        logging.getLogger(__name__).warning(
            "marketplace: retired-in-place %d fabricated seed listing(s) that carry sales "
            "(certification dropped, withdrawn from the public list, receipts still resolve): %s",
            len(kept), kept)
    return removed


def _seed_from_catalog() -> int:
    """Seed listings from the REAL registered product catalogue.

    Every field here is a fact about something that exists: name, category and tier come from the
    product the catalogue actually serves, and `route` is the real in-app route. What is NOT known is
    left unset rather than invented — `price_wst` stays 0 (nobody has priced these) and `certified`
    stays False (nothing has certified them). The UI reports both as unset rather than as "free" or
    "certified", so the marketplace can be real without asserting anything nobody established.
    """
    # Seed when there is no catalogue-derived listing yet — NOT merely when the store is empty.
    # "Empty" was wrong: a single retired fabrication kept for its receipt left the store non-empty,
    # so seeding never ran and the marketplace showed nothing but that fabrication.
    for path in _LISTINGS_DIR.glob("*.json"):
        doc = _read_doc(path)
        if doc is not None and doc.get("origin") == "catalog":
            return 0
    try:
        from agentic_core.catalog.api import list_products   # local: avoids an import cycle at boot
        products = list_products()
    except Exception:                                        # a catalogue read must never block boot
        return 0
    n = 0
    for prod in products:
        lid = uuid.uuid4().hex[:12]
        listing = Listing(
            id=lid,
            name=prod.get("name") or prod.get("slug", "Unnamed"),
            description=", ".join(prod.get("features") or []) or "Registered product in the live catalogue.",
            author="Platform catalogue",
            category=(prod.get("category") or "Product").split(" (")[0].strip(),
            price_wst=0.0,          # unset, not free — nobody has priced this
            tier=prod.get("tier") or "Standard",
            tags=[t for t in [str(prod.get("slug", "")).lower()] if t],
            certified=False,        # nothing has certified this
            status="active",
            creator_id="platform",
            origin="catalog",
            route=prod.get("route") or "",
            created_at=time.time(),
            updated_at=time.time(),
        )
        atomic_write_json(_listing_path(lid), listing.model_dump())
        n += 1
    return n


_retire_invented_seeds()
_seed_from_catalog()


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
    # W444 — the raw-dict patch was applied via setattr with NO validation: price_wst "free"
    # (or a negative/NaN price) persisted verbatim, the next Listing(**doc) raised, and
    # _all_listings silently DROPPED the record — an owner could corrupt their listing into
    # invisibility, and a negative price made purchases skip the ledger while sales_count
    # climbed. The merged result must re-validate as a Listing before anything is saved.
    # W444 refuter catch: origin/route are PROVENANCE ('catalog' asserts derivation from a real
    # registered product) — an owner could forge them by patch; immutable now.
    _immutable = ("id", "created_at", "certified", "creator_id", "sales_count",
                  "compliance", "status", "origin", "route")
    allowed = {k: v for k, v in patch.items() if k not in _immutable and hasattr(listing, k)}
    if "price_wst" in allowed:
        try:
            _p = float(allowed["price_wst"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=422, detail="price_wst must be a number.")
        import math as _math
        if not _math.isfinite(_p) or _p < 0:
            raise HTTPException(status_code=422, detail="price_wst must be a finite number ≥ 0.")
        allowed["price_wst"] = round(_p, 2)
    try:
        listing = type(listing)(**{**listing.model_dump(), **allowed})
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid patch: {str(e)[:300]}")
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
    listing = _load(listing_id)
    if not user_can_access(user, listing.creator_id):    # W311 — owner-scoped, 404-never-403
        raise HTTPException(status_code=404, detail="Listing not found")
    # W444 — the module's own invariant: "a receipt must never point at a listing that
    # vanished". A SOLD listing is retired to draft (kept, not advertised), never unlinked.
    if getattr(listing, "sales_count", 0) > 0:
        listing.status = "draft"
        _save(listing)
        return {"deleted": None, "retired_to_draft": listing_id,
                "note": (f"listing has {listing.sales_count} recorded sale(s) — retained as a "
                         "draft so its receipts keep resolving; it is no longer advertised")}
    p.unlink()
    return {"deleted": listing_id, "retired_to_draft": None}


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
    # W444 refuter catch (reproduced): a DRAFT listing — including one its owner just deleted,
    # retired to draft so receipts keep resolving — stayed fully purchasable by id, selling and
    # charging WST after deletion. Anything not 'active' is not for sale.
    if listing.status != "active":
        raise HTTPException(status_code=409,
                            detail=f"Listing is {listing.status} — not offered for sale.")

    total_cost = listing.price_wst * req.quantity

    # §12 (W348) — the WHOLE virtual-WST purchase sequence is SERIALISED under one cross-process
    # lock, with the balance loaded FRESH inside it: previously each request constructed its own
    # in-memory TokenLedger, so N concurrent purchases each saw the starting balance, each
    # "deducted" in memory, and the last snapshot write won — the audit confirmed 17 sales on an
    # 11-sale balance with only ONE charge persisted, plus torn listing/receipt state.
    from agentic_core.config import data_path as _dp, store_lock
    with store_lock(_dp("token_ledger_snapshot.json")):
        # W348 — the listing is RELOADED inside the lock: each racer otherwise increments its own
        # stale pre-lock copy's sales_count and the last writer wins (audit: 4 recorded of 11).
        listing = _load(listing_id)
        if listing.status == "sold_out":
            raise HTTPException(status_code=409, detail="Listing is sold out")
        if listing.status == "held":
            raise HTTPException(status_code=409,
                                detail="Listing is held by the §11 compliance screen and cannot be purchased.")
        if listing.status != "active":   # W444 — re-checked inside the lock like the others
            raise HTTPException(status_code=409,
                                detail=f"Listing is {listing.status} — not offered for sale.")
        if total_cost > 0:
            try:
                from agentic_core.commercial.token_ledger import TokenLedger, UserTier
                ledger = TokenLedger()   # constructed INSIDE the lock → fresh balance load
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

        # Record sale (still inside the lock — the listing write is part of the money sequence)
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
        except Exception as exc:
            # §12 (W348) — recognition failure is LOUD, never silent: the purchase stands (the
            # buyer was charged) but the receipt and the UEG both carry the honest miss so the
            # seller's books can be reconciled — the audit found this branch swallowing 170
            # recognition failures invisibly.
            receipt["revenue_recognition_failed"] = str(exc)[:160]
            try:
                from agentic_core.gaas.v5 import UEGLogger
                UEGLogger().log({"type": "marketplace.recognition_failed",
                                 "receipt_id": receipt["receipt_id"],
                                 "vsb_id": listing.vsb_id, "amount_wst": total_cost,
                                 "error": str(exc)[:160]})
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
