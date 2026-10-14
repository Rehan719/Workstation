"""
Capital Fund & Marketplace API.

Manages the virtual capital allocation system for the VSB ecosystem:
- Capital Fund: allocate, track, and report on virtual capital
- Marketplace: list, discover, and transact VSB products/services

  GET  /api/v1/fund/status          — fund health and allocation overview
  POST /api/v1/fund/allocate        — REQUEST an allocation to a registered entity or a project: held at
                                       Change Control, applied only after an explicit approval (FU-794)
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
from agentic_core.api._ai_provenance import (reply_evidence as _reply_evidence)   # W727

router = APIRouter(prefix="/api/v1", tags=["capital-fund"])

_FUND_STORE = data_path("capital_fund.json")


def _load_fund(strict: bool = False) -> dict:
    # W444 (comment corrected by the refuter round: load_json_tolerant recovers a truncated
    # tail but does NOT quarantine) — on unrecoverable corruption the corrupt file is now
    # RENAMED ASIDE (.corrupt-<id>) before the fresh pool takes over, so the shared WST
    # endowment can never be silently reset with the evidence destroyed.
    # §12 (W496, FU-119b) - a store that EXISTS and cannot be read is not a store that was never
    # set. Renaming the corrupt file aside preserved the evidence but the caller still received a
    # FRESH 10,000,000 WST pool, so a shared endowment could be reset to its seed and reported
    # HEALTHY with a utilisation of 0% - a silent reset presented as a healthy fund. A reader that
    # only reports (fund_status) may see the seeded pool as long as it says the store was quarantined;
    # a WRITER asks strictly and refuses, because writing back over a quarantined store is how the
    # reset becomes permanent.
    # W577 (FU-298) — the quarantine leg above was right and had a hole beside it: a store that
    # yields a RECOVERABLE PREFIX returns a dict, so it took this early return and was neither
    # quarantined nor disclosed. On this store the prefix is a set of money figures - total_capital,
    # allocated, available - and a dropped tail is dropped ALLOCATIONS, which makes the fund read as
    # having more available than it has. A writer refuses; a reader is told, on the dict it reads.
    from agentic_core.config import read_json_reported
    d, _why = read_json_reported(_FUND_STORE, None) if _FUND_STORE.exists() else (None, None)
    if isinstance(d, dict):
        if _why:
            if strict:
                from agentic_core.config import StoreUnavailable
                raise StoreUnavailable(_FUND_STORE, (
                    f"{_why}; nothing was allocated or contributed, because writing back a partial "
                    f"fund is how a dropped allocation becomes permanent"))
            d = dict(d)
            d["store_incomplete"] = _why
            d["balances_are_incomplete"] = True
            d["balances_basis"] = (
                "the fund store could not be read whole, so allocations recorded after the readable "
                "part are MISSING - `allocated` may be understated and `available` OVERSTATED")
        return d
    _quarantined = None
    if _FUND_STORE.exists():
        try:
            _quarantined = _FUND_STORE.with_suffix(f".corrupt-{uuid.uuid4().hex[:8]}")
            _FUND_STORE.rename(_quarantined)
        except OSError:
            _quarantined = _FUND_STORE
        if strict:
            from agentic_core.config import StoreUnavailable
            raise StoreUnavailable(_FUND_STORE, (
                f"quarantined at {getattr(_quarantined, 'name', _quarantined)}; no balance was reset "
                f"to the seed - restore the store or have the Owner re-seed it deliberately"))
    return {
        "total_capital": 10_000_000,  # the Owner-set VIRTUAL endowment (no cycle or deposit funded it)
        "currency": "WST",            # Workstation Token
        "allocated": 0,
        "available": 10_000_000,
        "allocations": [],
        # W496 (FU-119a) - the seed is recorded AS a seed, so every reader can separate the Owner's
        # virtual endowment from what cycles actually contributed instead of presenting the sum as
        # "the real capital fund"
        "seed_capital_wst": 10_000_000,
        "seed_basis": ("an Owner-set virtual endowment recorded when the store was first created - no "
                       "cycle contribution, owner deposit or ledger entry funded it"),
        "seeded_store_quarantined": (str(getattr(_quarantined, "name", "")) or None),
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
    #  W658 (Owner ruling 2026-10-10) - the SHARED fund takes no contribution from a simulation. An unregistered
    #  scope's cycle used to compound its simulated share into the fund every registered entity draws on.
    from agentic_core.economy.living_vsbs import is_registered as _is_registered
    if not _is_registered(vsb_id):
        return {"vsb_id": vsb_id, "amount_wst": amt, "contributed": False,
                "reason": (f"'{vsb_id}' is not a registered living entity: its cycle is a simulation, and a "
                           f"simulation's share is not paid into the shared capital fund")}
    with store_lock(_FUND_STORE):
        # W496 (FU-119b) - a writer refuses rather than writing back over a quarantined store
        fund = _load_fund(strict=True)
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
    Capital Fund reflects (and is governed by) the living system's state, not a detached ledger."""
    try:
        ctx = biobus.organism_context()
        # W492 (refutation) - composite_health is a BLEND with a simulated ATP term and, while no circuits
        # are tracked, a defaulted self-healing term. biobus already reports the measured-only figure and
        # per-term basis; dropping them here meant the fund page printed the blend as a measurement.
        _terms = ctx.get("composite_health_terms") or {}
        _unmeasured = {k: (t or {}).get("basis") for k, t in _terms.items()
                       if isinstance(t, dict) and t.get("measured") is False}
        _unmeasured_weight = sum(float((_terms.get(k) or {}).get("weight") or 0) for k in _unmeasured)
        return {"mode": ctx.get("mode"), "composite_health": ctx.get("composite_health"),
                "composite_health_measured_only": ctx.get("composite_health_measured_only"),
                "composite_health_unmeasured_weight": round(_unmeasured_weight, 3),
                # W494 (refutation) - the else-arm asserted "every term in this figure is measured"
                # whenever _terms was EMPTY, which is exactly the organism's error fallback: terms None,
                # composite_health 0.9, nothing measured at all. The fund reported a fallback constant
                # as fully measured. Absence of unmeasured terms is not evidence that terms were measured.
                "composite_health_measured_weight": ctx.get("composite_health_measured_weight"),
                "composite_health_basis": (
                    ctx.get("composite_health_basis")
                    or (f"NOT MEASURED - the organism context errored, so "
                        f"{ctx.get('composite_health')} is a fallback constant and no term was measured"
                        if not _terms else
                        f"a blend; {round(_unmeasured_weight * 100)}% of it is not measured "
                        f"({', '.join(sorted(_unmeasured))})" if _unmeasured else
                        "every term in this figure is measured")),
                "atp_ratio": (ctx.get("metabolic") or {}).get("atp_ratio")}
    except Exception:
        return {}


@router.get("/fund/status")
async def fund_status():
    """Return Capital Fund health and overview, including the living organism's §8 posture."""
    fund = _load_fund()
    allocation_count = len(fund.get("allocations", []))
    utilisation = round(fund["allocated"] / fund["total_capital"] * 100, 1) if fund["total_capital"] else 0
    # §12 (W496, FU-119a) - the page captioned this "the real capital fund", and 10,000,000 of it is a
    # constant the loader seeds when no store exists. The seed and the contributions are reported
    # apart, so nothing has to be taken on the caption's word. A store written before W496 carries no
    # seed marker: the seed is then UNRECORDED rather than assumed to be zero or to be the whole pool.
    _seed = fund.get("seed_capital_wst")
    _contrib = round(float(fund.get("cycle_contributions_total_wst", 0) or 0), 2)
    _total = float(fund.get("total_capital") or 0)
    if _seed is None:
        _basis = (f"NOT RECORDED - this store predates the seed marker, so how much of the "
                  f"{_total:,.0f} WST pool was seeded rather than contributed is not known from it. "
                  f"{_contrib:,.2f} WST is recorded as cycle contributions.")
    else:
        _basis = (f"{float(_seed):,.0f} of {_total:,.0f} WST is an Owner-set VIRTUAL endowment that no "
                  f"cycle, deposit or ledger entry funded; {_contrib:,.2f} WST came from recorded cycle "
                  f"contributions. Virtual WST throughout - no real-money rail is enabled.")
    return {
        "total_capital": fund["total_capital"],
        "currency": fund["currency"],
        "allocated": fund["allocated"],
        "available": fund["available"],
        "utilisation_pct": utilisation,
        "allocation_count": allocation_count,
        "seed_capital_wst": _seed,
        "contributed_wst": _contrib,
        "capital_basis": _basis,
        "fund_health": "HEALTHY" if utilisation < 80 else "CONSTRAINED" if utilisation < 95 else "DEPLETED",
        # the health is a ratio of allocations to the POOL, and the pool is mostly the seed - so on a
        # freshly seeded store it cannot come out anything but HEALTHY
        "fund_health_basis": (
            f"allocations are {utilisation}% of the pool"
            + ("" if not _seed or _total <= 0 else
               f", and {round(float(_seed) / _total * 100)}% of that pool is the unfunded seed, so this "
               f"reading is mostly a ratio against a constant")),
        "store_quarantined": fund.get("seeded_store_quarantined"),
        # W577 (FU-298) — the loader learned this and the route built its own dict, so the fact died
        # one layer below the page. The consequence here is the W496 defect by another route: an
        # unreadable tail is dropped ALLOCATIONS, so `allocated` is understated, `utilisation_pct`
        # with it, and `fund_health` is computed FROM that ratio — which means a fund that may be
        # depleted reports HEALTHY. That inference is named rather than left for a reader to make.
        "store_incomplete": fund.get("store_incomplete"),
        "balances_are_incomplete": bool(fund.get("balances_are_incomplete")),
        "balances_basis": fund.get("balances_basis"),
        "fund_health_is_incomplete": bool(fund.get("balances_are_incomplete")),
        "fund_health_incomplete_basis": (
            "the fund store could not be read whole, so allocations recorded after the readable part "
            "are missing: `allocated` and `utilisation_pct` are both UNDERSTATED and this health "
            "reading is therefore OPTIMISTIC - it may say HEALTHY of a fund that is constrained"
            if fund.get("balances_are_incomplete") else None),
        "organism": _organism_posture(),
    }


#  FU-794 (Owner ruling 2026-10-11, plan item P2.39) - AN ALLOCATION IS GOVERNED.
#
#  Until this ruling the route below allocated any amount to any id: no gate, no Change Control hold, and the
#  id was not looked up. It now goes through the path every other material economic action already takes -
#  the economy's own gate (economy.governance._materiality_gate), which files a Change Control hold, keeps
#  one live record per action, and hands back an approval ONCE, by compare-and-set, when the action is run
#  again after the Owner's explicit decision. Nothing here decides anything and there is no second mechanism:
#    - a request files (or finds) the hold and answers "held"; the fund is not touched;
#    - only an explicit decision at Change Control approves it (the hold is CRITICAL: a review, a model's
#      marker and the organism-health rule can each only record a recommendation);
#    - the allocation is applied when the same allocation is requested again and the gate spends that
#      approval; the applied row names the change. Approving moves nothing by itself;
#    - a rejection applies nothing, and the same request is answered "rejected" until the action changes.
#  A request's state is never stored here: it is computed from the Change Control record every time it is read.
_SAFE_PROJECT_ID = __import__("re").compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}")

STATE_LABELS = {
    "held": "held - awaiting decision",
    "approved_not_applied": "approved - not applied yet: request the same allocation again to apply it",
    "applied": "approved and applied",
    "approval_spent": "approved - the approval was spent and no allocation is stored for it",
    "rejected": "rejected - nothing was allocated",
    "withdrawn": "withdrawn - nothing was allocated",
}
LEGACY_LABEL = "recorded before allocations were governed"


def recipient_known(recipient_id: str) -> dict:
    """WHO THE FUND MAY ALLOCATE TO: an id that EXISTS - a registered living entity, or a project in the
    project store. What is refused is only what cannot exist. Three answers, and the third is never given as
    either of the other two: known True (with its kind), known False, known None (a store could not be read).
    A lookup only: it refuses nothing, the route does."""
    rid = str(recipient_id or "")
    registered, why = None, None
    try:
        from agentic_core.economy import living_vsbs as _lv
        registered = bool(_lv.is_registered(rid))
    except Exception as _err:                            # noqa: BLE001 - not known is said, never guessed
        why = type(_err).__name__
    project = False
    #  the project store is a directory of <id>.json files, so only an id that is ONE safe path segment is
    #  ever looked up in it; anything else cannot be a project id and never reaches the file system
    if registered is not True and _SAFE_PROJECT_ID.fullmatch(rid):
        try:
            from agentic_core.projects import api as _pj
            project = bool(_pj._path(rid).is_file())
        except Exception as _err:                        # noqa: BLE001
            project, why = None, (why or type(_err).__name__)
    if registered is True:
        known, kind = True, "entity"
    elif project is True:
        known, kind = True, "project"
    elif registered is None or project is None:
        known, kind = None, None
    else:
        known, kind = False, None
    return {"known": known, "kind": kind, "registered": registered, "why_unknown": why}


def _decision_of(c: dict) -> dict:
    """Who decided a change, read from its own audit trail - never from a request and never assumed."""
    ev = next((e for e in reversed((c or {}).get("audit_trail") or [])
               if isinstance(e, dict) and e.get("event") in ("approved", "rejected")), None)
    if ev is None:
        return {"decision": None, "decided_by": None, "decided_by_verified": None, "decided_at": None,
                "decision_source": None}
    return {"decision": ev.get("event"),
            "decided_by": ev.get("by"),
            "decided_by_verified": ev.get("by_verified"),
            "decided_at": ev.get("ts"),
            "decision_source": (c or {}).get("decision_source")}


def _request_view(c: dict, allocation: dict | None) -> dict:
    """One allocation request, as its Change Control record says it stands NOW. `allocation` is the stored
    allocation that names this change, when there is one."""
    from agentic_core.economy import governance as _gov
    st = c.get("status")
    if st in ("submitted", "under_review"):
        state, label = "held", STATE_LABELS["held"]
    elif st == "approved" and _gov._owner_decided(c):
        state, label = "approved_not_applied", STATE_LABELS["approved_not_applied"]
    elif st == "approved":
        #  an approval that is not an explicit decision releases nothing (the gate's own rule), so it is not
        #  reported as one
        state, label = "held", (STATE_LABELS["held"] + " (an approval that was not an explicit decision "
                                                        "releases nothing)")
    elif st == "implemented" and allocation:
        state, label = "applied", STATE_LABELS["applied"]
    elif st == "implemented":
        state, label = "approval_spent", STATE_LABELS["approval_spent"]
    elif st == "rejected":
        state, label = "rejected", STATE_LABELS["rejected"]
    else:
        state, label = "withdrawn", STATE_LABELS["withdrawn"]
    asked = c.get("fund_request") if isinstance(c.get("fund_request"), dict) else {}
    return {
        "cca_id": c.get("cca_id"), "state": state, "state_label": label, "change_status": st,
        "project_id": c.get("counterparty"), "project_name": asked.get("project_name"),
        "purpose": asked.get("purpose"), "domain": asked.get("domain"), "realm": asked.get("realm"),
        "amount": c.get("est_distributable_wst"),
        "requested_by": asked.get("requested_by"), "requested_by_verified": asked.get("requested_by_verified"),
        "requested_at": asked.get("first_requested_at") or c.get("submitted_at"),
        "fund_available_at_request": asked.get("fund_available_at_request"),
        **_decision_of(c),
        "allocation_id": (allocation or {}).get("allocation_id"),
        "applied_amount": (allocation or {}).get("amount"),
    }


def _fund_requests(fund: dict) -> tuple[list | None, str]:
    """Every allocation request, newest first, read from the Change Control records the gate filed for the
    fund. (requests, basis) - requests is None, with the reason, when the records could not be read: an
    unreadable list is never answered as an empty one."""
    try:
        from agentic_core.api import change_control as _cca
        from agentic_core.economy import governance as _gov
        applied = {a.get("cca_id"): a for a in (fund.get("allocations") or [])
                   if isinstance(a, dict) and a.get("cca_id")}
        rows = []
        for x in _cca._list_changes():
            if (x.get("change_type") != "economy_material"
                    or not str(x.get("title") or "").startswith(_gov.FUND_HOLD_TITLE_PREFIX)):
                continue
            c = _cca._load_change(x["cca_id"])
            if (not c or c.get("vsb_id") != _gov.FUND_ENTITY_ID
                    or not str(c.get("submitted_by") or "").startswith("economy:" + _gov.FUND_SOURCE_PREFIX)):
                continue
            rows.append(_request_view(c, applied.get(c["cca_id"])))
        return rows, ("every Change Control record the fund's gate filed; each state is computed from that "
                      "record when this is read")
    except Exception as _err:                            # noqa: BLE001 - said, never an empty list
        return None, f"the allocation requests could not be read ({type(_err).__name__})"


def _allocation_row(a: dict) -> dict:
    """A stored allocation with what kind of record it is, COMPUTED when read. The stored row is not rewritten:
    one written before allocations were governed carries no change id, and says so here."""
    governed = bool(isinstance(a, dict) and a.get("cca_id"))
    return {**a, "record_state": "applied" if governed else "ungoverned_legacy",
            "record_state_label": STATE_LABELS["applied"] if governed else LEGACY_LABEL}


class AllocateRequest(BaseModel):
    project_id: str
    project_name: str
    amount: float
    purpose: str
    domain: str = "general"
    realm: str = "enterprise"


@router.post("/fund/allocate")
async def allocate_capital(req: AllocateRequest, user: dict | None = Depends(get_current_user)):
    """Request an allocation of virtual capital to a registered entity or a project (FU-794).

    The request moves nothing. It is held at Change Control until an explicit decision approves it, and it is
    applied - once - when the same allocation is requested again and the economy's gate spends that approval.

    W496 (FU-119b): the STRICT store read is the first thing this route does, before the amount, the recipient
    or the gate is looked at - a fund that cannot be read whole answers 503 and nothing else is said about the
    request. W444: every read-modify-write of the fund runs under the store lock."""
    from agentic_core.config import StoreUnavailable, store_lock as _sl
    with _sl(_FUND_STORE):
        try:
            fund = _load_fund(strict=True)
        except StoreUnavailable as e:
            # W496 (FU-119b) - the fund could not be read whole, so nothing was allocated and no
            # balance was reset to the seed. A 500 would have read as a bug; this says what happened.
            raise HTTPException(status_code=503, detail=f"{e}")
    #  the lock is released before the gate runs: the gate takes its own per-action lock and writes to the
    #  constitutional ledger, and the fund's lock must not be held across either
    return _allocate_governed(req, fund, user if isinstance(user, dict) else None)


def _allocate_governed(req: "AllocateRequest", fund: dict, user: dict | None):
    import math
    from agentic_core.api import change_control as _cca
    from agentic_core.auth.core import auth_enabled, request_owner_id
    from agentic_core.config import StoreUnavailable, store_lock as _sl
    from agentic_core.economy import governance as _gov

    amount = round(float(req.amount), 2) if math.isfinite(float(req.amount)) else float("nan")
    if not math.isfinite(amount) or amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive.")
    if amount > fund["available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient capital. Available: {fund['available']} WST, requested: {amount} WST."
        )

    #  THE RECIPIENT EXISTS, OR NOTHING IS FILED. Checked after the strict read and before the gate, so an id
    #  nothing knows never becomes a Change Control record somebody has to decide.
    pid = str(req.project_id)
    _shown = pid[:80]
    who = recipient_known(pid)
    if who["known"] is None:
        raise HTTPException(status_code=503, detail=(
            f"Whether '{_shown}' is a registered entity or a project could not be read ({who['why_unknown']}), "
            f"so the allocation was not requested: nothing was filed with Change Control and the fund is "
            f"unchanged."))
    if who["known"] is False:
        raise HTTPException(status_code=404, detail=(
            f"'{_shown}' is neither a registered entity nor a project, so there is nothing for the fund to "
            f"allocate to. Nothing was filed with Change Control and the fund is unchanged."))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    requester = request_owner_id(user, "single-user-mode")
    requester_verified = bool(auth_enabled() and user)

    # §8 survival instinct — the organism's posture is ADVISORY only (virtual WST): restraint is flagged when
    # the organism is energy-depleted and the tranche is a large fraction of remaining capital. It decides
    # nothing; the decision is Change Control's.
    posture = _organism_posture()
    atp = posture.get("atp_ratio")
    frac = amount / fund["available"] if fund["available"] else 1.0   # of capital available BEFORE this draw
    caution = None
    if isinstance(atp, (int, float)) and atp < 0.3 and frac > 0.25:
        caution = (f"§8 survival instinct: the organism is energy-depleted (ATP {atp:.0%}); this tranche is "
                   f"{frac:.0%} of available capital. Consider a smaller tranche or deferring until recovery.")

    #  THE GOVERNED PATH - the economy's own gate, with the fund as the actor and the recipient as the
    #  counterparty. It returns (held, consumed): held -> nothing may run; consumed -> an approval was spent
    #  for THIS allocation and bounds it. The fund's class has no threshold (economy.governance).
    held, consumed = _gov._materiality_gate(_gov.FUND_ENTITY_ID, amount,
                                            source=_gov.FUND_SOURCE_PREFIX + pid, counterparty=pid)

    if held is not None:
        cca_id = held.get("cca_id")
        rejected = held.get("status") == "rejected_by_change_control"
        record, request_recorded = None, None
        if cca_id and not rejected:
            #  what was asked, written onto the hold the gate filed - while it is still undecided only, so a
            #  record under review keeps exactly what its decider was shown
            asked = {"project_id": pid, "project_name": req.project_name, "purpose": req.purpose,
                     "domain": req.domain, "realm": req.realm, "amount": amount,
                     "requested_by": requester, "requested_by_verified": requester_verified,
                     "requested_at": now, "recipient_kind": who["kind"],
                     "fund_available_at_request": fund["available"],
                     "currency": fund.get("currency")}

            def _note(fresh: dict) -> None:
                if fresh.get("status") != "submitted":
                    return
                _before = fresh.get("fund_request") if isinstance(fresh.get("fund_request"), dict) else {}
                fresh["fund_request"] = {**asked, "first_requested_at": _before.get("first_requested_at") or now}
            try:
                record = _cca._update_change(cca_id, _note)
                request_recorded = "recorded"
            except Exception as _note_err:               # noqa: BLE001 - said, never silent
                request_recorded = f"NOT recorded ({type(_note_err).__name__})"
        if record is None and cca_id:
            record = _cca._load_change(cca_id)
        view = _request_view(record, None) if record else None
        _state = "rejected" if rejected else "held"
        if rejected:
            _basis = (f"REJECTED, NOT ALLOCATED: Change Control record {cca_id} rejected exactly this allocation "
                      f"({amount} {fund.get('currency')} to '{_shown}'). Nothing was allocated and the fund's "
                      f"available figure is unchanged at {fund['available']}. It is asked again, as a fresh hold, "
                      f"when the allocation changes.")
        elif cca_id:
            _basis = (f"HELD, NOT ALLOCATED: this request is Change Control record {cca_id}. Nothing moves until "
                      f"an explicit decision approves it and the allocation is then requested again; the fund's "
                      f"available figure is unchanged at {fund['available']} {fund.get('currency')}.")
        else:
            _basis = ("HELD, NOT ALLOCATED: the governed path could not file or read a hold for this request, "
                      "and an allocation is never applied without one. The fund is unchanged.")
        return {
            "allocation_id": None,
            "applied": False,
            "amount": amount,
            "currency": fund["currency"],
            "remaining_available": fund["available"],
            "status": "rejected" if rejected else "held",
            "status_label": STATE_LABELS[_state],
            "cca_id": cca_id,
            "change": view,
            "organism": posture,
            "homeostasis_caution": caution,
            "governance": {"gate": "not applied", "change_control": _state, "cca_id": cca_id,
                           "recipient_registered": who["registered"], "recipient_kind": who["kind"],
                           "credited_to": None, "request_recorded": request_recorded,
                           "note": held.get("note"), "basis": _basis},
        }

    #  NOTHING IS APPLIED WITHOUT AN APPROVAL THE GATE SPENT FOR IT. The gate has no "proceed" answer for the
    #  fund; if it ever gave one, this refuses rather than allocating on it.
    if not consumed or not consumed.get("cca_id"):
        raise HTTPException(status_code=503, detail=(
            "The governed path returned neither a hold nor an approval for this allocation, so nothing was "
            "allocated: an allocation is applied only against an approved Change Control record."))
    cca_id, consume_id = consumed["cca_id"], consumed.get("consume_id")

    def _give_back(reason: str) -> str:
        """The approval was spent and the allocation did not happen: hand it back, and SAY what happened."""
        _r = _gov._restore_consumed_approval(consumed, vsb_id=_gov.FUND_ENTITY_ID, reason=reason)
        return (f"the approval {cca_id} was given back and can be applied again" if _r == "restored" else
                f"the approval {cca_id} was NOT given back ({_r}) and stays spent; a new request files a new hold")

    with _sl(_FUND_STORE):
        try:
            fresh = _load_fund(strict=True)
        except StoreUnavailable as e:
            raise HTTPException(status_code=503, detail=(
                f"{e}. Nothing was allocated; " + _give_back("the fund store could not be read whole") + "."))
        if amount > fresh["available"]:
            raise HTTPException(status_code=400, detail=(
                f"Insufficient capital. Available: {fresh['available']} WST, requested: {amount} WST. "
                f"Nothing was allocated; " + _give_back("the fund no longer holds the amount") + "."))
        approved = _cca._load_change(cca_id) or {}
        decided = _decision_of(approved)
        _by = decided.get("decided_by")
        _governance = {
            "gate": "not applied", "change_control": "approved", "cca_id": cca_id,
            "decided_by": _by, "decided_by_verified": decided.get("decided_by_verified"),
            "decided_at": decided.get("decided_at"), "decision_source": decided.get("decision_source"),
            "approved_amount": approved.get("est_distributable_wst"),
            "recipient_registered": who["registered"], "recipient_kind": who["kind"], "credited_to": None,
            "basis": (f"A GOVERNED RECORD: Change Control record {cca_id} was approved by "
                      + (f"'{_by}'" if _by else "a decider its record does not name")
                      + (" (an authenticated principal)" if decided.get("decided_by_verified") else
                         " (a name the platform did not check - authentication is off)")
                      + f" as an explicit decision, and this allocation spent that approval. It names "
                      + ("a registered entity" if who["kind"] == "entity" else f"the project '{_shown}'")
                      + ". No constitutional gate was applied. This route credited no entity's ledger: it "
                        "reduced the fund's available figure and did nothing else. Virtual WST."),
        }
        allocation_id = f"alloc-{uuid.uuid4().hex[:8]}"
        allocation = {
            "allocation_id": allocation_id,
            "project_id": req.project_id,
            "project_name": req.project_name,
            "amount": amount,
            "purpose": req.purpose,
            "domain": req.domain,
            "realm": req.realm,
            "status": "active",
            "cca_id": cca_id,
            "consume_id": consume_id,
            "requested_by": requester,
            "requested_by_verified": requester_verified,
            "homeostasis_caution": caution,
            "governance": dict(_governance),
            "allocated_at": now,
        }
        fresh["allocated"] = round(float(fresh["allocated"]) + amount, 2)
        fresh["available"] = round(float(fresh["available"]) - amount, 2)
        fresh["allocations"].append(allocation)
        try:
            _save_fund(fresh)
        except Exception as _save_err:                   # noqa: BLE001 - the approval is not spent on nothing
            raise HTTPException(status_code=503, detail=(
                f"The fund store could not be written ({type(_save_err).__name__}). Nothing was allocated; "
                + _give_back("the fund store could not be written") + "."))

    #  the allocation is stored: the spent approval records that its action ran (never given back after this)
    _gov._mark_action_ran(consumed, _gov.FUND_ENTITY_ID, "capital fund allocation stored")

    #  W672 (ledger v16 R6.5) - the audit event, written after the save, so an event never describes an
    #  allocation that was not stored; whether it was recorded is said in the response. FU-794: it names the
    #  change that authorised it. (The request, the decision and the spend are already on the ledger from the
    #  gate and from Change Control - economy.materiality_hold_filed, cca.change_approved / cca.change_rejected,
    #  economy.materiality_approved_consumed - so none of them is written a second time here.)
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.capital_fund.allocation", "allocation_id": allocation_id,
                         "project_id": req.project_id, "amount_wst": amount,
                         "recipient_registered": who["registered"], "gate": "not applied",
                         "change_control": "approved", "cca_id": cca_id, "consume_id": consume_id,
                         "decided_by": _by})
        _audit_event = "recorded"
    except Exception as _ueg_err:                        # noqa: BLE001 - said, never silent
        _audit_event = f"NOT recorded ({type(_ueg_err).__name__})"

    biobus.fire_signal(
        "motor", "fund.allocate",
        f"Capital allocated: {amount} WST → {req.project_name} [{req.domain}] (Change Control {cca_id})",
        0.8,
    )

    return {
        "allocation_id": allocation_id,
        "applied": True,
        "amount": amount,
        "currency": fresh["currency"],
        "remaining_available": fresh["available"],
        "status": "allocated",
        "status_label": STATE_LABELS["applied"],
        "cca_id": cca_id,
        "organism": posture,
        "homeostasis_caution": caution,
        "governance": {**_governance, "audit_event": _audit_event},
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

    #  FU-794 - what was ASKED and where each request stands, beside what was applied. A held request is in
    #  `allocation_requests` and never in `allocations`: every total on this page sums `allocations`, and a
    #  request has moved nothing.
    _requests, _requests_basis = _fund_requests(fund)
    return {
        "total_capital": fund["total_capital"],
        "allocated": fund["allocated"],
        "available": fund["available"],
        "currency": fund["currency"],
        "allocations": [_allocation_row(a) for a in allocations],
        "allocation_count": len(allocations),
        "allocation_requests": _requests,
        "allocation_requests_basis": _requests_basis,
        "by_domain": by_domain,
        "by_realm": by_realm,
        # W577 (FU-298) — a PORTFOLIO is the one place a missing allocation is most invisible: every
        # per-domain and per-realm total is a sum over rows that may not all be here.
        "store_incomplete": fund.get("store_incomplete"),
        "allocations_are_incomplete": bool(fund.get("balances_are_incomplete")),
        "allocations_basis": (
            "the fund store could not be read whole, so allocations after the readable part are "
            "MISSING from this portfolio and from every by_domain and by_realm total in it"
            if fund.get("balances_are_incomplete")
            else "every allocation recorded in the fund store"),
    }


class FundReportRequest(BaseModel):
    period: str = "current"
    focus: str = "performance"  # performance | risk | opportunity


@router.post("/fund/report")
async def generate_fund_report(req: FundReportRequest):
    """AI-generated Capital Fund performance report."""
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
        f"You are writing a report on a VIRTUAL capital fund (no real money is held or invested). "
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
    meta = await gateway.query_meta(prompt, agent="fund_manager", augment=False, user_text=(req.focus or None))
    biobus.record_operation("fund_report", "fund.report", success=True)

    return {**_reply_evidence(meta.get('served_by')), 
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

    # §17.5 invariant 1 (W343, FU-276) — the caller's identity reaches the memory layer, or what they asked for is stored where even they cannot recall it.
    _owner_id = user.get("username") if isinstance(user, dict) else None
    meta = await gateway.query_meta(prompt, agent="marketplace_valuation", augment=False, owner_id=_owner_id, user_text=(chr(10).join(x for x in (req.title, req.description) if isinstance(x, str) and x.strip()) or None))
    if meta.get("served_by") == "native":
        raise HTTPException(status_code=503, detail=(
            "No model is available to produce a valuation — the deterministic floor can only "
            "emit an outline, and an outline presented as a valuation would be fabrication. "
            "Load a local model or enable an external provider (Owner-gated)."))

    return {**_reply_evidence(meta.get('served_by')), 
        "valuation_id": uuid.uuid4().hex[:10],
        "title": req.title,
        "domain": req.domain,
        "valuation": meta.get("output"),
        "served_by": meta.get("served_by"),
        "is_external": meta.get("is_external"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": "AI valuation for planning purposes only. Professional financial advice required for investment decisions.",
    }
