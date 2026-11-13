"""A PRICE IN WST, DERIVED FROM THE WATERFALL, NEVER TYPED (P5.2) - part 1: every price is recomputed on read from
inputs it names, and is null, with the reason, while any input is absent.

OWNER RULING 2026-09-27 (P5.2): a price is a stated amount for a named deliverable, with the arithmetic that produced
it, derived from the waterfall and the entity's own costs; never a hardcoded number. A deliverable whose cost inputs
are missing has NO price - not a default one.

    GET  /api/v1/economy/price?vsb_id=...&deliverable_id=...           the price, recomputed on this read
    POST /api/v1/economy/deliverable-cost                              declare what a deliverable costs the entity
    GET  /api/v1/economy/deliverable-cost?vsb_id=...&deliverable_id=   the cost declared, with its history

THE INPUTS, each named in every answer:
- the entity's effective waterfall, read through the resolver GET /api/v1/economy/waterfall uses (the Owner's
  override when set, else the form's template);
- the entity's declared cost for the deliverable: a person's statement in WST, with what it is made of, who declared
  it and when. A later declaration supersedes an earlier one, which is kept;
- the arithmetic that turns a cost and a waterfall into a price. The waterfall splits a profit; it does not set one,
  so a margin or a target is needed that no ruling states. The question is the Owner's (an OWNER DECISION row, with
  its recommendation). Until it is ruled every price is null, and the answer says so.

Virtual WST throughout. Nothing here sells, charges, posts or records a sale.
"""
from __future__ import annotations

import math
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, user_can_access

router = APIRouter(prefix="/api/v1/economy", tags=["economy-pricing"])

STORE = "deliverable_costs.json"
#  the Owner's ruling on the arithmetic of a price: none yet. Until there is one, no price is computed.
ARITHMETIC = None
ARITHMETIC_UNRULED = ("the arithmetic that turns a declared cost and the waterfall into a price is not ruled: the "
                      "waterfall splits a profit and does not set one, so a margin or a target is needed that no ruling "
                      "states. It waits on the Owner's decision, so no price is computed")
BASIS = ("A price is recomputed on every read from the inputs named here, and is null while any input is absent - "
         "never a default figure. Virtual WST; nothing is sold, charged or posted.")


class DeclaredCost(BaseModel):
    model_config = {"extra": "forbid"}
    vsb_id: str
    deliverable_id: str
    cost_wst: float = Field(gt=0, le=1e12, allow_inf_nan=False)
    made_of: str                                   # what the cost is made of, in the person's words


def _path():
    from agentic_core.config import data_path
    return data_path(STORE)


def _read() -> Dict[str, List[Dict[str, Any]]]:
    p = _path()
    if not p.exists():
        return {}
    from agentic_core.config import read_json_strict
    try:
        data = read_json_strict(p, dict, expect=dict)
    except Exception as e:                              # noqa: BLE001 - said, never read as "no cost declared"
        raise HTTPException(status_code=503, detail=(
            f"The declared costs could not be read ({type(e).__name__}), so no price is computed and none is declared."))
    return {k: [r for r in v if isinstance(r, dict)] for k, v in (data or {}).items() if isinstance(v, list)}


def _key(vsb_id: str, deliverable_id: str) -> str:
    return f"{vsb_id}/{deliverable_id}"


def _deliverable_of(vsb_id: str, deliverable_id: str, user: Any) -> Dict[str, Any]:
    """The deliverable, when it is this entity's and the caller may read it; otherwise not found."""
    from agentic_core.api import deliverables as _dl
    u = user if isinstance(user, dict) else None
    for d in _dl._load():
        if d.get("id") == deliverable_id and d.get("vsb_id") == vsb_id and user_can_access(u, d.get("owner_id")):
            return d
    raise HTTPException(status_code=404, detail=f"Deliverable {deliverable_id} is not one of entity {vsb_id}'s.")


def price_of(vsb_id: str, deliverable_id: str) -> Dict[str, Any]:
    """The price of one deliverable, recomputed now from its inputs, or null with each absent input named."""
    from agentic_core.api.economy import _resolve_entity_type
    from agentic_core.economy.metabolism import EconomicMetabolism
    entity_type, et_source = _resolve_entity_type(vsb_id, None)
    m = EconomicMetabolism(vsb_id, entity_type)
    history = _read().get(_key(vsb_id, deliverable_id), [])
    cost = history[-1] if history else None
    missing = []
    if cost is None:
        missing.append({"input": "cost", "says": (
            "no cost has been declared for this deliverable (POST /api/v1/economy/deliverable-cost), and a "
            "deliverable whose cost is missing has no price")})
    if ARITHMETIC is None:
        missing.append({"input": "arithmetic", "says": ARITHMETIC_UNRULED})
    price = None if missing else ARITHMETIC(cost["cost_wst"], m.waterfall)
    return {"vsb_id": vsb_id, "deliverable_id": deliverable_id, "price_wst": price, "currency": "WST (virtual)",
            "inputs": {"waterfall": {"proportions": dict(m.waterfall), "source": m.waterfall_source,
                                     "entity_type": entity_type, "entity_type_source": et_source},
                       "cost": cost},
            "missing": missing, "basis": BASIS,
            "computed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


@router.get("/price")
async def get_price(vsb_id: str, deliverable_id: str, user: dict | None = Depends(get_current_user)):
    from agentic_core.api.economy import _require_economy_access
    _require_economy_access(vsb_id, user)
    _deliverable_of(vsb_id, deliverable_id, user)
    return price_of(vsb_id, deliverable_id)


@router.post("/deliverable-cost")
async def declare_cost(req: DeclaredCost, user: dict | None = Depends(get_current_user)):
    """A person declares what one of the entity's deliverables costs it, in WST, and what that cost is made of.
    Refused, with nothing written, when the amount is not above zero, the cost says nothing of what it is made of,
    or the deliverable is not the entity's."""
    from agentic_core.api.economy import _require_economy_access
    _require_economy_access(req.vsb_id, user)
    made_of = str(req.made_of or "").strip()
    if not made_of:
        raise HTTPException(status_code=422, detail="Not declared: a cost says what it is made of.")
    if not math.isfinite(req.cost_wst):
        raise HTTPException(status_code=422, detail="Not declared: the cost is not a finite amount.")
    _deliverable_of(req.vsb_id, req.deliverable_id, user)
    entry = {"vsb_id": req.vsb_id, "deliverable_id": req.deliverable_id, "cost_wst": round(float(req.cost_wst), 2),
             "made_of": made_of,
             "declared_by": (user.get("username") if isinstance(user, dict) else None) or "single-user-mode",
             "declared_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    from agentic_core.config import mutate_json

    def _add(existing):
        data = existing if isinstance(existing, dict) else {}
        data.setdefault(_key(req.vsb_id, req.deliverable_id), []).append(entry)
        return data
    _read()                                              # an unreadable store refuses before any write
    mutate_json(_path(), _add, dict)
    return {"declared": True, "cost": entry, "price_now": price_of(req.vsb_id, req.deliverable_id)}


@router.get("/deliverable-cost")
async def get_declared_cost(vsb_id: str, deliverable_id: str, user: dict | None = Depends(get_current_user)):
    from agentic_core.api.economy import _require_economy_access
    _require_economy_access(vsb_id, user)
    _deliverable_of(vsb_id, deliverable_id, user)
    history = _read().get(_key(vsb_id, deliverable_id), [])
    if not history:
        raise HTTPException(status_code=404, detail=(
            f"No cost has been declared for deliverable {deliverable_id}, so it has no price."))
    return {"cost": history[-1], "superseded": history[:-1][::-1], "basis": (
        "the latest declaration is the cost a price reads; earlier ones are kept, newest first")}
