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
- the arithmetic, as the Owner ruled on 2026-11-19 (FU-1185): price = the declared cost / (1 - the prudential
  reserve rate - a platform margin set once, 20%). The reserve rate is the one a cycle applies by default, read from
  the cycle. The waterfall splits the distributable profit the price leaves; it does not set the price (W1123).

WHAT IS NOT FOR SALE (P5.5, W940) is read here from its one register (agentic_core/economy/not_for_sale.py): a
deliverable that names an excluded capability - the faith content, the Fitrah Spectrum, or anything needing a
real-money rail - is refused a price and a cost declaration, with the ruling in the reason.
GET /api/v1/economy/not-for-sale serves the register.

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
#  W1123 (FU-1279) - OWNER RULING 2026-11-19 (FU-1185, the recommendation accepted): price = the declared cost /
#  (1 - the prudential reserve rate - a platform margin set once). The reserve rate is the one a cycle applies by
#  default, read from EconomicMetabolism.run_cycle itself so the two never drift; the margin is set once, here.
PLATFORM_MARGIN = 0.20
RULING = ("OWNER RULING 2026-11-19 (FU-1185): price = the declared cost / (1 - the prudential reserve rate - a "
          "platform margin set once, 20%)")


def reserve_rate() -> float:
    """The prudential reserve rate a cycle applies by default, read from the cycle itself, never typed here."""
    import inspect
    from agentic_core.economy.metabolism import EconomicMetabolism
    return float(inspect.signature(EconomicMetabolism.run_cycle).parameters["reserve_rate"].default)


def ARITHMETIC(cost_wst: float, waterfall: Dict[str, Any]) -> Dict[str, Any]:
    """The ruled arithmetic: the price, and what it is made of - the cost, the reserve and the distributable profit the
    entity's waterfall splits. The waterfall does not move the price; it splits what the price leaves."""
    r, m = reserve_rate(), PLATFORM_MARGIN
    price = round(cost_wst / (1.0 - r - m), 2)
    reserve = round(price * r, 2)
    distributable = round(price - cost_wst - reserve, 2)
    return {"price_wst": price, "ruling": RULING, "reserve_rate": r, "platform_margin": m,
            "reserve_rate_source": "the rate a cycle applies by default (EconomicMetabolism.run_cycle's reserve_rate)",
            "cost_wst": round(float(cost_wst), 2), "reserve_wst": reserve, "distributable_profit_wst": distributable,
            "split_of_distributable_wst": {s: round(distributable * float(share), 2) for s, share in waterfall.items()},
            "basis": ("the price is the declared cost divided by one less the reserve rate and the platform margin. The "
                      "entity's waterfall splits the distributable profit the price leaves and does not move the price; "
                      "a cycle whose energy reading raises its reserve does not reprice, since the price reads the "
                      "default rate. Virtual WST; nothing is sold, charged or posted.")}
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


def _refuse_if_not_for_sale(deliverable: Dict[str, Any]) -> None:
    """P5.5: a deliverable that names an excluded capability has no price, and the refusal names the ruling."""
    from agentic_core.economy.not_for_sale import named_exclusion
    ex = named_exclusion(deliverable)
    if ex:
        by = ex["named_by"]
        how = (f"its domain is '{by['value']}'" if by["field"] == "domain" else
               f"its {by['field']} names '{by['term']}'")
        raise HTTPException(status_code=409, detail=(
            f"Not priced: this deliverable names {ex['what']} ({how}), which is not for sale and is not a paid "
            f"tier. The ruling: {ex['ruling']}."))


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
    priced = None if missing else ARITHMETIC(cost["cost_wst"], dict(m.waterfall))
    arithmetic = priced or {"ruling": RULING, "reserve_rate": reserve_rate(), "platform_margin": PLATFORM_MARGIN,
                            "basis": "no price until a cost is declared; this is the arithmetic it will be priced by"}
    return {"vsb_id": vsb_id, "deliverable_id": deliverable_id, "price_wst": priced["price_wst"] if priced else None,
            "currency": "WST (virtual)", "arithmetic": arithmetic,
            "inputs": {"waterfall": {"proportions": dict(m.waterfall), "source": m.waterfall_source,
                                     "entity_type": entity_type, "entity_type_source": et_source},
                       "cost": cost},
            "missing": missing, "basis": BASIS,
            "computed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


@router.get("/price")
async def get_price(vsb_id: str, deliverable_id: str, user: dict | None = Depends(get_current_user)):
    from agentic_core.api.economy import _require_economy_access
    _require_economy_access(vsb_id, user)
    _refuse_if_not_for_sale(_deliverable_of(vsb_id, deliverable_id, user))
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
    _refuse_if_not_for_sale(_deliverable_of(req.vsb_id, req.deliverable_id, user))
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


@router.get("/not-for-sale")
async def not_for_sale(user: dict | None = Depends(get_current_user)):
    """P5.5: what is not for sale, and not offered as a paid tier, each with its ruling - the register the price reads."""
    from agentic_core.economy.not_for_sale import register
    return register()
