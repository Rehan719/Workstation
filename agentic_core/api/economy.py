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

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, user_can_access
from agentic_core.economy.entities import ENTITY_TEMPLATES, DEFAULT_ENTITY, get_template
from agentic_core.economy.metabolism import (
    EconomicMetabolism, validate_waterfall, _load_waterfall_overrides,
    _save_waterfall_overrides, _WATERFALL_STAGES,
)
from agentic_core.economy.charity import CharityIntelligence

router = APIRouter(prefix="/api/v1/economy", tags=["vsb-economy"])


def _require_economy_access(vsb_id: str, user: dict | None) -> None:
    """§14×§12 (W320) — economy operations on a VSB are OWNER-scoped: previously the whole router
    had zero tenant isolation, so any authenticated user could run cycles, set waterfalls, read
    ledgers, or DRAIN another tenant's reserve via /transfer. 404 (never 403) when scoped out.
    Platform-level ids with no stored record (e.g. 'workstation-idbo') are admin-only under auth;
    single-user mode (auth off) stays unguarded (no tenant boundary to protect)."""
    if user is not None and not isinstance(user, dict):
        user = None
    from agentic_core.auth.core import auth_enabled
    if not auth_enabled():
        return
    owner_id = None
    try:
        from agentic_core.api.vsb import _load_vsb
        owner_id = (_load_vsb(vsb_id) or {}).get("owner_id")
    except Exception:
        pass
    if not user_can_access(user, owner_id):
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")


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
async def economy_status(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY,
                         user: dict | None = Depends(get_current_user)):
    """W442 — this surface re-committed the defects /cycle already fixed: it reported owner
    "Rehan" for EVERY tenant's VSB (the constructor default) and took entity_type from the
    caller's claim, so a stored nonprofit could be reported with a profit-distributing template's
    waterfall and capital rules. Now resolved from the stores, with the basis disclosed."""
    _require_economy_access(vsb_id, user)
    entity_type, et_source = _resolve_entity_type(vsb_id, entity_type)
    owner, owner_source = "Rehan", "platform_default"
    try:
        from agentic_core.economy.living_vsbs import _load as _lv_load
        rec = _lv_load().get(vsb_id)
        if rec and rec.get("owner"):
            owner, owner_source = str(rec["owner"]), "living_registry"
    except Exception:
        pass
    out = EconomicMetabolism(vsb_id, entity_type, owner).status()
    out["attribution"] = {"entity_type_source": et_source, "owner_source": owner_source}
    return out


class CycleRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    entity_type: str = DEFAULT_ENTITY
    # W414 — this defaulted to 10000.0, and the UI posts only {vsb_id}. So every "Run Metabolic
    # Cycle" click processed ten thousand WST of revenue that nobody earned or supplied, and the
    # resulting distributions, reserves and charity allocations were written to the real ledger as
    # if they had happened. A default that silently manufactures the input to a financial
    # calculation is worse than a missing field. Zero means zero.
    # W442 — NaN/inf/negative inputs are refused at the model: a NaN revenue would have written
    # NaN into every waterfall account (and negative figures corrupt shared totals).
    revenue: float = Field(default=0.0, ge=0.0, allow_inf_nan=False)
    costs: float = Field(default=0.0, ge=0.0, allow_inf_nan=False)
    reserve_rate: float = Field(default=0.20, ge=0.0, le=1.0, allow_inf_nan=False)
    owner: str = "Rehan"


@router.post("/cycle")
async def run_cycle(req: CycleRequest, user: dict | None = Depends(get_current_user)):
    """Run one living metabolic cycle under the FULL §3 governance chain (economy/governance.py):
    materiality → Change Control hold when the estimated distributable meets the threshold; the
    gaas.v5 gate (a failed gate is a LOUD UEG bypass event, never silent); and an explicit UEG
    event logging every cycle's per-stage split amounts. Virtual WST only."""
    _require_economy_access(req.vsb_id, user)
    # §14 (W295) — HONEST attribution: when vsb_id names a LIVING entity, its REGISTERED identity
    # (owner + entity type) is authoritative — the request's defaults ("Rehan" + the default
    # template) previously mis-attributed every user's VSB cycles. Request values remain the
    # fallback for ad-hoc/simulation ids; an override mismatch is reported, never silent.
    owner, entity_type, attribution = req.owner, req.entity_type, "request_values"
    try:
        from agentic_core.economy.living_vsbs import list_living
        reg = next((v for v in (list_living() or {}).get("living_vsbs", [])
                    if v.get("vsb_id") == req.vsb_id), None)
        if reg:
            owner = reg.get("owner") or owner
            entity_type = reg.get("entity_type") or entity_type
            attribution = "living_registration"
            if req.owner != "Rehan" and req.owner != owner:
                attribution = f"living_registration (request owner '{req.owner}' overridden)"
    except Exception:
        pass
    from agentic_core.economy.governance import governed_cycle
    result = await governed_cycle(req.vsb_id, entity_type, owner,
                                  req.revenue, req.costs, req.reserve_rate, source="api")
    if isinstance(result, dict):
        result["attribution"] = {"owner": owner, "entity_type": entity_type, "basis": attribution}
        # §13 (W338) — USER-driven cycles drift the living record too: a cycle that genuinely
        # moved the ledger marks the shipped repo stale (the audit found only AUTONOMOUS cycles
        # marked drift — an owner-run cycle silently outdated the shipped body).
        if result.get("cycle") is not None and float(req.revenue or 0) > 0:
            try:
                from agentic_core.api.vsb import mark_repo_stale
                mark_repo_stale(req.vsb_id, "owner-driven economic cycle")
            except Exception:
                pass
    return result


@router.get("/waterfall")
async def get_waterfall(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY,
                        user: dict | None = Depends(get_current_user)):
    """The current effective profit-distribution waterfall for a VSB (Owner override if set, else the entity
    template default) + the template's binding constraints the Owner must respect."""
    _require_economy_access(vsb_id, user)
    entity_type, et_source = _resolve_entity_type(vsb_id, entity_type)
    m = EconomicMetabolism(vsb_id, entity_type)
    t = m.template
    return {
        "vsb_id": vsb_id, "entity_type": entity_type, "entity_type_source": et_source,
        "entity_name": t["name"],
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


def _resolve_entity_type(vsb_id: str, claimed: str) -> tuple:
    """§4 (W313) — the template bounds bind to the VSB's REAL stored entity type, never the caller's
    claim: previously a nonprofit VSB could pay an Owner profit share by claiming entity_type='sole'
    at set time. Falls back to the claim only when the entity is unknown to both stores."""
    try:
        from agentic_core.economy.living_vsbs import _load as _lv_load
        rec = _lv_load().get(vsb_id)
        if rec and rec.get("entity_type"):
            return str(rec["entity_type"]), "living_registry"
    except Exception:
        pass
    try:
        from agentic_core.api.vsb import _load_vsb
        v = _load_vsb(vsb_id)
        if v and v.get("entity_type"):
            return str(v["entity_type"]), "vsb_store"
    except Exception:
        pass
    return claimed, "caller_claimed"


@router.post("/waterfall")
async def set_waterfall(req: WaterfallRequest, user: dict | None = Depends(get_current_user)):
    """§4/§8/§10 Owner sovereignty: adjust the profit-distribution proportions for a VSB (virtual). The
    proposal is normalised to 1.0 and BOUND by the entity template (a non-distributing form forces owner=0;
    a capital-preserving form requires capital_fund>0) — the template resolves from the VSB's STORED
    entity type, never the caller's claim. Persisted, UEG-logged, effective from the next cycle.
    Virtual/simulated only — no real funds move."""
    _require_economy_access(req.vsb_id, user)
    entity_type, et_source = _resolve_entity_type(req.vsb_id, req.entity_type)
    template = get_template(entity_type)
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
            "type": "waterfall_override", "vsb_id": req.vsb_id, "entity_type": entity_type,
            "entity_type_source": et_source,
            "entity_type_claimed": req.entity_type if req.entity_type != entity_type else None,
            "waterfall": waterfall, "by": "owner"})
    except Exception:
        pass
    return {
        "vsb_id": req.vsb_id, "entity_type": entity_type, "entity_type_source": et_source,
        "waterfall": waterfall,
        "source": "owner_override", "applied": True,
        "note": "Owner-set proportions persisted (virtual). Effective next cycle; logged to the UEG. "
                "Reset by posting the template defaults.",
    }


@router.get("/owner-payments")
async def owner_payments(vsb_id: str = "workstation-idbo", owner: str = "Rehan",
                         user: dict | None = Depends(get_current_user)):
    """§7 — the Owner's accrued share (virtual WST) from each cycle's §4 owner stage, plus history. Real-money
    payout rails are DISABLED and gated; no real funds move."""
    _require_economy_access(vsb_id, user)
    from agentic_core.economy.owner_payments import OwnerPaymentsUnavailable, status
    try:
        return status(vsb_id, owner)
    except OwnerPaymentsUnavailable as e:
        # W465 (FU-016) — an unreadable store is said, never shown as zero balances
        raise HTTPException(status_code=503, detail=str(e))


class PayoutRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    owner: str = "Rehan"
    amount: float = Field(gt=0, allow_inf_nan=False)   # W442 — NaN/inf/≤0 refused at the model


@router.post("/owner-payments/payout")
async def owner_payout(req: PayoutRequest, user: dict | None = Depends(get_current_user)):
    """Record a VIRTUAL Owner payout (reduces the accrued balance). NO real funds move — real-money rails are
    gated until the Owner explicitly authorises them AND a compliance/KYC review passes."""
    _require_economy_access(req.vsb_id, user)
    from agentic_core.economy.owner_payments import OwnerPaymentsUnavailable, payout
    try:
        return payout(req.vsb_id, req.amount, req.owner)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OwnerPaymentsUnavailable as e:
        raise HTTPException(status_code=503, detail=f"{e} — no payout was recorded.")
    except TimeoutError:
        raise HTTPException(status_code=503, detail=(
            "The owner-payments store is busy (another write held its lock) — no payout was recorded. Retry."))


@router.get("/living-vsbs")
async def living_vsbs(user: dict | None = Depends(get_current_user)):
    """§4 — the established VSB enterprises the organism autonomously tends (each continually operated via
    paced virtual economy cycles on the circadian heartbeat). Virtual/simulated."""
    from agentic_core.economy.living_vsbs import list_living
    res = list_living()
    # §14 (W320) — under auth the listing is tenant-scoped: entities whose stored record the caller
    # cannot access are omitted (registered-only/platform entities remain admin-only).
    from agentic_core.auth.core import auth_enabled
    if auth_enabled():
        from agentic_core.api.vsb import _load_vsb
        u = user if isinstance(user, dict) else None
        rows = []
        for v in res.get("living_vsbs", []):
            try:
                owner_id = (_load_vsb(v.get("vsb_id")) or {}).get("owner_id")
            except Exception:
                owner_id = None
            if user_can_access(u, owner_id):
                rows.append(v)
        res["living_vsbs"] = rows
        for count_key in ("living", "total", "count"):
            if count_key in res:
                res[count_key] = len(rows)
    return res


class TransferRequest(BaseModel):
    from_vsb: str
    to_vsb: str
    # W442 — NaN passed every engine guard (nan <= 0 is False) and permanently poisoned the
    # sender's reserve_fund; refused at the model AND at validate_transfer (belt and braces).
    amount: float = Field(gt=0, allow_inf_nan=False)
    memo: str = ""


@router.post("/transfer")
async def inter_vsb_transfer(req: TransferRequest, user: dict | None = Depends(get_current_user)):
    """Federation seed — generated Enterprise IDBOs TRANSACT: the sender pays from its reserve fund
    (balanced double-entry posting, refused on insufficient virtual funds) and the receiver's next
    metabolic cycle consumes the amount as intake revenue (enters its §4 waterfall). gaas.v5-gated;
    MATERIAL transfers are held for Change Control like material distributions; UEG-logged.
    Virtual WST only — no real funds."""
    # §14 (W320) — the SENDER must be the caller's own entity: previously any authenticated user
    # could drain any tenant's reserve by naming it as from_vsb. (Receiving is a payment — the
    # recipient needs no consent to be paid.)
    _require_economy_access(req.from_vsb, user)
    return await _transfer_core(req)


async def _transfer_core(req: TransferRequest, transfer_id: Optional[str] = None, *, context: str = "transfer") -> dict:
    """The transfer itself, after the caller's access check. W465: a service-contract settlement passes the
    transfer id its claim persisted, so a retry after a crash posts under the SAME id (record_transfer is idempotent
    on it) instead of minting a fresh one and debiting the client twice. Every dependency stays imported at call
    time (tests substitute them on their modules)."""
    from agentic_core.economy.governance import _materiality_gate, _ueg_log
    from agentic_core.economy.transfers import PendingStoreUnavailable, record_transfer, validate_transfer

    # side-effect-free validation FIRST → clean HTTP codes, nothing posted on refusal
    try:
        validate_transfer(req.from_vsb, req.to_vsb, req.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e).strip("'\""))

    # W463 — the gate binds the approval to this amount AND this counterparty, and hands back exactly
    # what it spent (None when nothing was spent) so a transfer that does not post gives back only that
    held, consumed = _materiality_gate(req.from_vsb, round(float(req.amount), 2), source="transfer",
                                       counterparty=req.to_vsb)
    if held is not None:
        return {"transfer": None, "governance": held}
    from agentic_core.economy.governance import _mark_action_ran, _restore_consumed_approval

    # W442 — one transfer_id for the whole request: the gaas fallback could re-run the action
    # after it had ALREADY posted (an interceptor exception after execution), debiting the sender
    # twice for one request. record_transfer is idempotent on the id, so the retry is now a no-op.
    import uuid as _uuid
    _xfer_id = transfer_id or f"xfer-{_uuid.uuid4().hex[:10]}"
    posted = {"done": False}

    def _give_back_unless_debited(reason: str) -> None:
        # record_transfer debits and queues in two steps, so the approval comes back only when the sender's
        # ledger shows NO debit for this transfer id; an unreadable ledger keeps it spent (a second release
        # would be the worse error) and says so
        if not consumed or posted["done"]:
            return
        from agentic_core.economy.transfers import debit_posted
        ledger_error = None
        try:
            debited = bool(debit_posted(req.from_vsb, _xfer_id))
        except Exception as err:
            debited, ledger_error = None, f"{type(err).__name__}: {str(err)[:120]}"
        if debited is False:
            _restore_consumed_approval(consumed, vsb_id=req.from_vsb, reason=reason)
            return
        # the debit posted, or cannot be ruled out: never given back. Only a CONFIRMED debit counts as the released
        # action having run (W463, fifth refutation): an unknown one stays unmarked, so it never lifts an older
        # rejection — a request for the rejected transfer is then asked again only for an explicit decision
        if debited:
            _mark_action_ran(consumed, req.from_vsb, "transfer debit posted")
        # W463 (fourth refutation) — the record says which: a confirmed debit, or a ledger that could not be read
        _ueg_log({"type": "economy.materiality_approval_spent_cycle_failed", "vsb_id": req.from_vsb,
                  "source": "transfer", "cca_id": consumed.get("cca_id"),
                  "consume_id": consumed.get("consume_id"), "transfer_id": _xfer_id,
                  "debit_confirmed": bool(debited), **({"ledger_error": ledger_error} if ledger_error else {}),
                  "note": ("the transfer did not complete, but the sender's ledger shows its debit; the approval "
                           "stays spent. Do NOT re-run the transfer — the debit posted and the receiver leg may be "
                           "missing (repairing it replays this transfer_id)" if debited else
                           "the transfer did not complete and the sender's ledger could not be read, so whether its "
                           "debit posted is unknown; the approval was kept spent for that reason. Check the sender's "
                           "ledger for this transfer_id before re-approving or re-running the transfer")})

    async def _action():
        posted["started"] = True
        out = record_transfer(req.from_vsb, req.to_vsb, req.amount, req.memo, transfer_id=_xfer_id)
        posted["done"], posted["out"] = True, out
        _mark_action_ran(consumed, req.from_vsb, "transfer posted inside the gate")
        return out

    try:
        try:
            from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
            gov = UnifiedConstitutionalInterceptorV16Omega("economy-node", UEGLogger())
            result = await gov.intercept({"intent": "inter_vsb_transfer", "from": req.from_vsb,
                                          "to": req.to_vsb, "amount_wst": req.amount}, _action)
            transfer = result.output
            governance = {"status": result.status, "checkpoint": result.checkpoint_id}
            if not isinstance(transfer, dict):   # the gate blocked the action — never fabricate a transfer
                if consumed:
                    governance["approval_cca_id"] = consumed.get("cca_id")   # W465 — the settle note names it
                # W442 refuter catch: the materiality approval was consumed before this gate ran;
                # blocked means nothing posted, so the Owner's approval must not stay spent.
                if not posted["done"]:
                    returned = _restore_consumed_approval(consumed, vsb_id=req.from_vsb,
                                                          reason=f"gaas gate {result.status} — no transfer posted")
                    if consumed:
                        governance["approval_returned"] = returned   # W465 — what the give-back actually did
                elif consumed:
                    governance["approval_returned"] = "not_returned_action_ran"
                return {"transfer": None, "governance": governance}
        except ValueError:
            raise
        except Exception as e:
            if posted["done"]:
                # W463 (refuter) — the action fully POSTED and the gate raised afterwards (e.g. its checkpoint
                # write): the transfer is returned as posted, never replayed — a replay that met a second fault
                # reported a posted transfer as failed, and a client retry paid twice
                transfer = posted["out"]
                _ueg_log({"type": "economy.governance_bypass", "vsb_id": req.from_vsb, "source": "transfer",
                          "error": str(e)[:200], "note": "the transfer posted; the gate raised after execution (logged loudly)."})
                governance = {"status": "gate_raised_after_execution", "error": str(e)[:160]}
            elif posted.get("started"):
                # W463 (third refutation) — the gate ALLOWED the action and the action raised part-way (e.g. the
                # receiver queue's lock timed out after the debit). That is not a gate outage: the idempotent replay
                # completes it (repairing the receiver leg), and the record says what happened — the post-execution
                # check and checkpoint did not run for the retry.
                transfer = record_transfer(req.from_vsb, req.to_vsb, req.amount, req.memo, transfer_id=_xfer_id)
                posted["done"], posted["out"] = True, transfer
                _mark_action_ran(consumed, req.from_vsb, "transfer posted on an idempotent retry")
                _ueg_log({"type": "economy.governance_bypass", "vsb_id": req.from_vsb, "source": "transfer",
                          "error": str(e)[:200],
                          "note": "the gate allowed the transfer and the action raised; it was retried idempotently "
                                  "outside the gate's post-execution check and checkpoint (logged loudly)."})
                governance = {"status": "allowed_action_retried", "error": str(e)[:160]}
            else:
                transfer = record_transfer(req.from_vsb, req.to_vsb, req.amount, req.memo, transfer_id=_xfer_id)
                posted["done"], posted["out"] = True, transfer
                _mark_action_ran(consumed, req.from_vsb, "transfer posted with the gate unavailable")
                _ueg_log({"type": "economy.governance_bypass", "vsb_id": req.from_vsb, "source": "transfer",
                          "error": str(e)[:200], "note": "gaas.v5 gate unavailable — transfer ran ungated (logged loudly)."})
                governance = {"status": "ungated_bypass_logged", "error": str(e)[:160]}
    except ValueError as e:
        # W442 refuter catch: the atomic in-lock funds re-check (a concurrent drain won the race)
        # used to escape as a 500; it is a clean refusal — and the consumed approval is restored when
        # nothing posted. W463: "nothing posted" is the LEDGER's answer, not a progress flag — a replay of
        # an already-debited transfer could raise here too.
        _give_back_unless_debited("funds re-check refused — nothing posted")
        raise HTTPException(status_code=400, detail=str(e))
    except PendingStoreUnavailable as e:
        # W465 — the receiver's queue could not be read (it is checked before the debit, so normally nothing posted);
        # a refusal of the store, not a server fault, and the answer says what the sender's ledger shows
        _give_back_unless_debited("the receiver's pending-transfers store could not be read — nothing posted")
        from agentic_core.economy.transfers import debit_posted
        try:
            debited = bool(debit_posted(req.from_vsb, _xfer_id))
        except Exception:
            debited = None
        settling = context == "settlement"
        why = str(e).replace("; nothing was written", "")
        if debited is False:
            detail = f"{why}. Nothing was debited — {'settle' if settling else 'retry'} again once the store is readable."
        elif debited:
            logged = _ueg_log({"type": "economy.transfer_receiver_leg_missing", "vsb_id": req.from_vsb,
                               "to_vsb": req.to_vsb, "amount_wst": req.amount, "transfer_id": _xfer_id,
                               "context": context, "error": why[:200],
                               "note": "the sender was debited and the receiver's pending queue could not be written; "
                                       "replaying this transfer_id through record_transfer completes the credit once, "
                                       "without a second debit"})
            if settling:
                detail = (f"{why}. This settlement's payment ({_xfer_id}) debited the client but has not reached the "
                          "provider's queue — settle again once the store is readable: it completes the payment "
                          "without paying twice.")
            else:
                detail = (f"{why}. Transfer {_xfer_id} debited the sender (its ledger shows the debit) but has not "
                          "reached the receiver's queue. Do NOT re-run the transfer — a new request debits again. The "
                          "receiver's credit is completed by replaying this transfer id once the store is readable"
                          + (" (recorded on the constitutional ledger)." if logged else
                             "; the ledger entry recording it did not land — note the transfer id now."))
        else:
            detail = (f"{why}. Whether this {'settlement' if settling else 'transfer'} ({_xfer_id}) debited the "
                      + ("client is unknown (its ledger could not be read) — settle again: it asks the ledger first "
                         "and never pays twice." if settling else
                         "sender is unknown (its ledger could not be read) — check the sender's ledger for this id "
                         "before re-running; a new request would debit again."))
        raise HTTPException(status_code=503, detail=detail) from None
    except BaseException:
        # W463 — anything else that stops the transfer (a vanished receiver, a busy store) used to escape
        # as a 500 with the Owner's approval spent on nothing.
        _give_back_unless_debited("the transfer raised before it posted — nothing was debited")
        raise

    _ueg_log({"type": "economy.inter_vsb_transfer", **{k: transfer[k] for k in
              ("transfer_id", "from_vsb", "to_vsb", "amount_wst")},
              "disclaimer": "Virtual/simulated WST — no real funds moved."})
    return {"transfer": transfer, "governance": governance}


# ── §15 (W330) — the inter-entity organ beyond one verb: SERVICE CONTRACTS ────────────────────
# Entity A COMMISSIONS entity B: offer → accept → deliver (a real cascade scoped to the provider)
# → settle (the existing gaas-gated, materiality-held transfer primitive; the provider's next
# cycle recognises the intake). Tenant-scoped end-to-end. Virtual WST only.

class ContractRequest(BaseModel):
    client_vsb: str
    provider_vsb: str
    brief: str
    # W465 — a NaN price was stored and then broke GET /contracts for every party (JSON refuses NaN), and a price of 0
    # or below could never settle (its transfer is refused at the model): both refused at the offer
    price_wst: float = Field(default=100.0, gt=0, allow_inf_nan=False)


# W465 (register FU-015) — the contract store is written only by a read-modify-write under its lock. Every route used
# to load the whole list, change one row and save the whole list: deliver held its copy across a 15–25 minute cascade
# and wrote it back, erasing whatever happened meanwhile — a settlement of another contract included, whose Settle
# button then reappeared and paid the provider a second time — and two settles of one contract could both pass the
# 'delivered' check. A settle now CLAIMS the contract, and its transfer id is persisted on the claim, so a retry after a
# crash completes the same transfer (the ledger is idempotent on the id) instead of paying twice.
_CONTRACT_CAP = 500
_SETTLE_CLAIM_STALE_S = 600      # a settle takes seconds; its locks time out in tens of seconds


def _contracts_path():
    from agentic_core.config import data_path
    return data_path("vsb_contracts.json")


def _contract_ts() -> str:
    import time as _time
    return _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime())


def _read_contracts() -> list:
    """STRICT read: a missing store is empty; a store that exists but cannot be read whole is refused (503). The
    tolerant read answered [] for an unreadable store, and the next offer then wrote a store of one contract."""
    import json as _json
    import time as _time
    p = _contracts_path()
    if not p.exists():
        return []
    raw = None
    for attempt in range(5):
        try:
            raw = p.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return []
        except UnicodeDecodeError:
            raise HTTPException(status_code=503, detail=(
                "The service-contract store is not valid UTF-8 — nothing was done (an unreadable store is never overwritten)."))
        except PermissionError:
            if attempt == 4:
                raise HTTPException(status_code=503, detail="The service-contract store stayed locked — nothing was done. Retry.")
            _time.sleep(0.05 * (attempt + 1))
        except OSError as e:
            raise HTTPException(status_code=503,
                                detail=f"The service-contract store could not be read ({str(e)[:120]}) — nothing was done.")
    try:
        rows = _json.loads(raw)
    except ValueError:
        raise HTTPException(status_code=503, detail=(
            "The service-contract store is unreadable — nothing was done (an unreadable store is never overwritten)."))
    if not isinstance(rows, list) or not all(isinstance(r, dict) and r.get("id") for r in rows):
        raise HTTPException(status_code=503, detail="The service-contract store is not a list of contracts — nothing was done.")
    return rows


def _load_contracts() -> list:
    return _read_contracts()


def _trim_contracts(rows: list, keep: Optional[str] = None) -> list:
    """Beyond the cap only the oldest SETTLED contracts are dropped — never `keep`, the contract the current change
    touched (a settle's own write dropped the row it had just settled once the store held 500 unsettled rows). The old
    `rows[-500:]` dropped the oldest rows whatever their state — an accepted contract whose cascade was running, or a
    delivered one still owed. With nothing droppable the store stays above the cap: nothing is lost."""
    excess = len(rows) - _CONTRACT_CAP
    if excess <= 0:
        return rows
    drop = set()
    for i, r in enumerate(rows):
        if len(drop) >= excess:
            break
        if r.get("status") == "settled" and not r.get("settling") and r.get("id") != keep:
            drop.add(i)
    return [r for i, r in enumerate(rows) if i not in drop]


def _mutate_contracts(change, keep: Optional[str] = None):
    """Read-modify-write under the store lock. `change(rows)` raises HTTPException to refuse (nothing is written). It
    never awaits: the lock is held only for the synchronous read, change and atomic write. `keep` names the contract
    the change touched, which the cap never drops in the same write."""
    from agentic_core.config import atomic_write_json, store_lock
    lock = store_lock(_contracts_path(), timeout=5.0)
    try:
        lock.__enter__()
    except TimeoutError:
        raise HTTPException(status_code=503,
                            detail="The service-contract store is busy — another change is being written. Retry.") from None
    try:
        rows = _read_contracts()
        out = change(rows)
        atomic_write_json(_contracts_path(), _trim_contracts(rows, keep))
        return out
    finally:
        lock.__exit__(None, None, None)


def _find_contract(rows: list, cid: str) -> dict:
    c = next((x for x in rows if x.get("id") == cid), None)
    if not c:
        raise HTTPException(status_code=404, detail=f"Contract {cid} not found.")
    return c


def _claim_live(cl) -> bool:
    """A settle claim that still holds the contract: the same test the claim itself applies."""
    import time as _time
    return (isinstance(cl, dict) and bool(cl.get("claim"))
            and _time.time() - float(cl.get("at_epoch") or 0) < _SETTLE_CLAIM_STALE_S)


def _public_contract(c: dict) -> dict:
    """A contract as the parties see it: a LIVE settle claim shows only since when (its transfer id stays server-side);
    a released or stale claim, kept only so a retry reuses its transfer id, is not shown as a settlement in progress."""
    out = dict(c)
    cl = out.get("settling")
    if isinstance(cl, dict) and _claim_live(cl):
        out["settling"] = {"since": cl.get("at")}
    else:
        out.pop("settling", None)
    return out


def _contract_ueg(event: dict) -> None:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({**event, "disclaimer": "Virtual/simulated WST — no real funds moved."})
    except Exception:
        pass


@router.post("/contracts")
async def offer_contract(req: ContractRequest, user: dict | None = Depends(get_current_user)):
    """§15 (W330) — entity-to-entity commissioning: the CLIENT entity offers a service contract
    to a PROVIDER entity. The caller must own the client entity; the offer is a real persisted
    record the provider must ACCEPT before any work or money moves."""
    _require_economy_access(req.client_vsb, user)
    if not req.brief.strip():
        raise HTTPException(status_code=400, detail="A contract needs a brief.")
    if req.client_vsb == req.provider_vsb:
        raise HTTPException(status_code=400, detail="An entity cannot contract itself.")
    import uuid as _uuid
    contract = {
        "id": f"ctr-{_uuid.uuid4().hex[:10]}", "client_vsb": req.client_vsb,
        "provider_vsb": req.provider_vsb, "brief": req.brief[:1000],
        "price_wst": round(float(req.price_wst), 2), "status": "offered",
        "delivery": None, "settlement": None,
        "offered_at": _contract_ts(),
    }
    _mutate_contracts(lambda rows: rows.append(contract))
    _contract_ueg({"type": "economy.contract_offered", "contract_id": contract["id"],
                   "client_vsb": req.client_vsb, "provider_vsb": req.provider_vsb,
                   "price_wst": contract["price_wst"]})
    return contract


@router.get("/contracts")
async def list_contracts(vsb_id: Optional[str] = None,
                         user: dict | None = Depends(get_current_user)):
    """Contracts the caller is party to (client- or provider-side access)."""
    def _can(vid: str) -> bool:
        try:
            _require_economy_access(vid, user)
            return True
        except HTTPException:
            return False
    rows = [_public_contract(c) for c in _load_contracts() if _can(c["client_vsb"]) or _can(c["provider_vsb"])]
    if vsb_id:
        rows = [c for c in rows if vsb_id in (c["client_vsb"], c["provider_vsb"])]
    return {"contracts": rows[::-1], "total": len(rows)}


@router.post("/contracts/{cid}/accept")
async def accept_contract(cid: str, user: dict | None = Depends(get_current_user)):
    def _accept(rows: list) -> dict:
        c = _find_contract(rows, cid)
        _require_economy_access(c["provider_vsb"], user)   # only the provider accepts
        if c["status"] != "offered":
            raise HTTPException(status_code=409, detail=f"Contract is {c['status']}, not offered.")
        c["status"] = "accepted"
        return _public_contract(c)
    c = _mutate_contracts(_accept)
    _contract_ueg({"type": "economy.contract_accepted", "contract_id": cid})
    return c


@router.post("/contracts/{cid}/deliver")
async def deliver_contract(cid: str, user: dict | None = Depends(get_current_user)):
    """The provider DELIVERS: a REAL org cascade runs scoped to the provider entity (its own
    Chief/CEO tiers ground in ITS living plan — W280), and the run's summary + QMS verdict bind
    to the contract. Honest: a weak delivery carries its real verdict, never a fabricated pass.
    W465 — the cascade runs outside the store's lock and binds only if the contract is still accepted when it
    finishes (a concurrent delivery that bound first wins; this run is reported unbound, never written over it)."""
    c = _find_contract(_read_contracts(), cid)
    _require_economy_access(c["provider_vsb"], user)
    if c["status"] != "accepted":
        raise HTTPException(status_code=409, detail=f"Contract is {c['status']}, not accepted.")
    # W452 (P1.4, refuter F5) — the provider's Mode 3 review gate holds its delivery cascade too,
    # and the refusal names THIS mover (the inner cascade would have said "cascade")
    from agentic_core.api.vsb import _load_vsb as _gate_load, _refuse_gated
    _prov = _gate_load(c["provider_vsb"])
    if _prov:
        _refuse_gated(_prov, "contract delivery")
    from agentic_core.api.swarm import CascadeRequest, cascade_orchestration
    run = await cascade_orchestration(CascadeRequest(
        mission=f"Deliver the commissioned work: {c['brief'][:400]}",
        domain="enterprise", scope=c["provider_vsb"]))
    delivery = {"run_id": run.get("run_id"), "quality": run.get("quality"),
                "served_by": (run.get("ai_provenance") or {}).get("served_by")}

    def _bind(rows: list) -> dict:
        cur = next((x for x in rows if x.get("id") == cid), None)
        if cur is None:
            raise HTTPException(status_code=409, detail=(
                f"Contract {cid} no longer exists; delivery run {run.get('run_id')} ran but is bound to nothing."))
        if cur["status"] != "accepted":
            raise HTTPException(status_code=409, detail=(
                f"Contract {cid} became {cur['status']} while this delivery ran (another delivery bound first); "
                f"run {run.get('run_id')} is not bound to it."))
        cur["delivery"] = delivery
        cur["status"] = "delivered"
        return _public_contract(cur)
    c = _mutate_contracts(_bind)
    _contract_ueg({"type": "economy.contract_delivered", "contract_id": cid,
                   "run_id": run.get("run_id")})
    return c


def _settlement_outcome(gov: dict, client: str, provider: str) -> tuple:
    """W465 (register FU-024) — what a transfer answered without a transfer MEANS for the settlement. Every such answer
    used to be recorded as `held: True` with "settlement HELD by governance — retry after the hold clears", including a
    rejection (no hold exists; retrying the same price is refused), a gate refusal and a gate error."""
    from agentic_core.economy.governance import _REJECTED_BY_WORDS
    st = str((gov or {}).get("status") or "")
    if st == "rejected_by_change_control":
        by = _REJECTED_BY_WORDS.get(str(gov.get("rejected_by") or ""), "by Change Control")
        return "rejected", (f"Change Control rejected exactly this payment ({by}) — nothing was paid. Settling again at "
                            f"this price is refused while that rejection is the newest decision on payments from "
                            f"{client} to {provider}.")
    if st == "held_for_change_control":
        if gov.get("decided_concurrently"):
            return "decided_concurrently", ("The Change Control hold for this payment was decided while this settle ran "
                                             "— nothing was paid; settle again.")
        if not gov.get("cca_id"):
            return "gate_error", ("The governance check could not complete — nothing was paid; any Change Control hold "
                                  "already filed for this payment is unchanged. Settle again.")
        return "held", (f"Held for the Owner's decision (Change Control hold {gov.get('cca_id')}, decided in the "
                        "Governance hub's Sovereign Sanctum) — nothing was paid; settle again once it is approved.")
    ref, returned = gov.get("approval_cca_id"), gov.get("approval_returned")
    if not ref:
        spent = ""
    elif returned == "restored":
        spent = f" The Owner approval {ref} spent on this attempt was handed back — settling again spends it."
    elif returned == "superseded":
        spent = (f" The Owner approval {ref} spent on this attempt stays spent: a newer Change Control record for this "
                 "payment replaced it.")
    else:
        spent = (f" The Owner approval {ref} spent on this attempt could not be handed back (its Change Control record "
                 "was busy or had changed) and stays spent — settling again asks the Owner again.")
    return "blocked", f"The constitutional gate answered '{st or 'no status'}' — nothing was paid." + spent


@router.post("/contracts/{cid}/settle")
async def settle_contract(cid: str, user: dict | None = Depends(get_current_user)):
    """The client SETTLES: payment moves through the EXISTING transfer primitive (gaas-gated,
    materiality-held, double-entry, UEG-logged); the provider's next metabolic cycle recognises
    the intake. W465: the settle CLAIMS the contract first (a second settle while one runs is refused, 409), under a
    transfer id persisted on the claim — a retry after a crash asks the client's ledger whether that id already
    debited and, if so, completes it instead of paying again. What an unpaid settlement means (held for the Owner,
    rejected, refused by the gate, a gate error) is recorded and said as it is; the contract stays 'delivered'."""
    import time as _time
    import uuid as _uuid
    c0 = _find_contract(_read_contracts(), cid)
    _require_economy_access(c0["client_vsb"], user)     # only the client pays
    token = _uuid.uuid4().hex

    def _claim(rows: list) -> dict:
        c = _find_contract(rows, cid)
        if c["status"] == "settled":
            return {"state": "settled", "contract": _public_contract(c)}
        if c["status"] != "delivered":
            raise HTTPException(status_code=409, detail=f"Contract is {c['status']}, not delivered.")
        cl = c.get("settling") if isinstance(c.get("settling"), dict) else None
        if cl and _claim_live(cl):
            raise HTTPException(status_code=409, detail=(
                f"A settlement of contract {cid} is already in progress (since {cl.get('at')}) — this request paid "
                "nothing. Retry when it has finished."))
        # a stale or released claim's transfer id is REUSED: its attempt may have debited the client
        xid = (cl or {}).get("transfer_id") or f"xfer-{_uuid.uuid4().hex[:10]}"
        c["settling"] = {"claim": token, "transfer_id": xid, "at": _contract_ts(), "at_epoch": _time.time()}
        return {"state": "claimed", "contract": dict(c), "transfer_id": xid}

    claim = _mutate_contracts(_claim, keep=cid)
    if claim["state"] == "settled":
        return {**claim["contract"], "note": "Already settled — nothing more was paid."}
    xid, c = claim["transfer_id"], claim["contract"]
    client, provider, price = c["client_vsb"], c["provider_vsb"], c["price_wst"]
    memo = f"contract {cid} settlement"

    def _release() -> None:
        # the claim stays on the contract with its transfer id, immediately reclaimable: the next settle asks the
        # ledger first, so reusing the id can never pay twice
        def _rel(rows: list) -> None:
            cur = next((x for x in rows if x.get("id") == cid), None)
            cl = (cur or {}).get("settling")
            if isinstance(cl, dict) and cl.get("claim") == token:
                cl["claim"], cl["at_epoch"] = None, 0
        try:
            _mutate_contracts(_rel, keep=cid)
        except Exception:
            pass                       # the claim goes stale on its own

    from agentic_core.economy import transfers as _tr
    try:
        try:
            already = bool(_tr.debit_posted(client, xid))
        except Exception as err:
            raise HTTPException(status_code=503, detail=(
                f"The client's ledger could not be read ({type(err).__name__}), so whether an earlier attempt of this "
                "settlement debited it is unknown — nothing was done. Retry."))
        if already:
            # an earlier attempt of THIS settlement debited the client and did not finish: complete it (the replay
            # repairs a missing receiver leg); no second debit, and no second approval asked for or spent
            try:
                replayed = _tr.record_transfer(client, provider, price, memo, transfer_id=xid)
            except _tr.PendingStoreUnavailable as err:
                raise HTTPException(status_code=503, detail=(
                    f"An earlier attempt of this settlement debited the client; completing it needs the provider's "
                    f"pending-transfers store, which could not be read ({err}). Nothing more was paid — settle again "
                    "once it is readable; it completes the payment without paying twice.")) from None
            result = {"transfer": replayed,
                      "governance": {"status": "replay_of_posted_debit",
                                     "note": "an earlier attempt of this settlement had already debited the client; "
                                             "it was completed, not paid again"}}
        else:
            result = await _transfer_core(TransferRequest(from_vsb=client, to_vsb=provider, amount=price, memo=memo),
                                          transfer_id=xid, context="settlement")
    except BaseException:
        _release()
        raise

    transfer, gov, unknown = result.get("transfer"), (result.get("governance") or {}), False
    if not transfer:
        # a gate that answers without a transfer after the action ran must not leave a paid contract unsettled
        try:
            if _tr.debit_posted(client, xid):
                transfer = _tr.record_transfer(client, provider, price, memo, transfer_id=xid)
                gov = {**gov, "note": "the gate answered without a transfer, but the client's ledger shows this "
                                      "settlement's debit; it was completed"}
        except Exception:
            unknown = True
    answer: dict = {}

    def _apply(rows: list):
        cur = next((x for x in rows if x.get("id") == cid), None)
        if cur is None:
            return None
        cl = cur.get("settling") if isinstance(cur.get("settling"), dict) else {}
        mine = cl.get("claim") == token
        if transfer:
            if cur["status"] == "delivered":
                cur["status"] = "settled"
                cur["settlement"] = {"outcome": "paid", "transfer_id": transfer.get("transfer_id"),
                                     "governance": gov, "at": _contract_ts()}
            cur.pop("settling", None)
            return _public_contract(cur)
        if not mine:
            answer["note"] = "Another settle of this contract took over while this one ran; its answer stands."
            return _public_contract(cur)
        if unknown:
            kind, note = "unknown", ("Whether this payment posted could not be determined (the client's ledger could not "
                                     "be read) — settle again: it asks the ledger first and never pays twice.")
            cl["claim"], cl["at_epoch"] = None, 0
        else:
            kind, note = _settlement_outcome(gov, client, provider)
            cur.pop("settling", None)
        prior_cca = (cur.get("settlement") or {}).get("cca_id") if isinstance(cur.get("settlement"), dict) else None
        cca_ref = gov.get("cca_id") or (prior_cca if kind in ("gate_error", "blocked", "unknown", "decided_concurrently") else None)
        cur["settlement"] = {"outcome": kind, "held": kind == "held", "governance": gov, "at": _contract_ts(),
                             **({"cca_id": cca_ref} if cca_ref else {}),
                             **({"rejected_by": gov.get("rejected_by")} if gov.get("rejected_by") else {})}
        answer["note"] = note
        return _public_contract(cur)

    try:
        out = _mutate_contracts(_apply, keep=cid)
    except Exception:
        # the claim is released (its transfer id kept): the "settle again" this answer asks for must not meet a 409
        _release()
        if transfer:
            _contract_ueg({"type": "economy.contract_settlement_record_failed", "contract_id": cid,
                           "transfer_id": transfer.get("transfer_id"), "price_wst": price,
                           "note": "the payment posted but the contract record could not be updated; settling again "
                                   "completes the record without paying twice"})
            raise HTTPException(status_code=503, detail=(
                f"The payment posted (transfer {transfer.get('transfer_id')}) but the contract record could not be "
                "updated — settle again to record it; it will not pay twice.")) from None
        raise
    if out is None:
        if transfer:
            _contract_ueg({"type": "economy.contract_settlement_record_failed", "contract_id": cid,
                           "transfer_id": transfer.get("transfer_id"), "price_wst": price,
                           "note": "the payment posted but the contract no longer exists in the store"})
        raise HTTPException(status_code=409, detail=(
            f"Contract {cid} no longer exists"
            + (f"; its payment posted (transfer {transfer.get('transfer_id')})." if transfer else "; nothing was paid.")))
    if transfer and out.get("status") == "settled":
        _contract_ueg({"type": "economy.contract_settled", "contract_id": cid,
                       "transfer_id": transfer.get("transfer_id"), "price_wst": price,
                       "governance": gov.get("status")})
    return {**out, **({"note": answer["note"]} if answer.get("note") else {})}


class ClosePeriodRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    entity_type: str = DEFAULT_ENTITY
    owner: str = "Rehan"


@router.post("/close-period")
async def close_period(req: ClosePeriodRequest, user: dict | None = Depends(get_current_user)):
    """§9.1 PERIOD CLOSE — the CFO closes the books: P&L · balance sheet · cash flow computed from the
    REAL double-entry postings, then closing entries roll income/expenses into retained earnings so the
    next period starts clean. UEG-logged (tamper-evident). Virtual WST only."""
    _require_economy_access(req.vsb_id, user)
    # W442 — the close report was labelled with the CALLER-CLAIMED legal form (a §4.5 cousin on a
    # financial statement header); resolve from the stores like /waterfall does.
    entity_type, et_source = _resolve_entity_type(req.vsb_id, req.entity_type)
    m = EconomicMetabolism(req.vsb_id, entity_type, req.owner)
    result = m.ledger.close_period()
    # W442 — the docstring claims "UEG-logged (tamper-evident)" but the log call was swallowed
    # try/except-pass; the response now SAYS whether the tamper-evident event actually landed.
    ueg_logged = False
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({
            "type": "economy.period_close", "vsb_id": req.vsb_id,
            "net_profit_wst": result["close"]["net_profit_wst"],
            "retained_earnings_wst": result["retained_earnings_wst"],
            "prepared_by": "CFO agent (AI C-Suite)",
            "disclaimer": "Virtual/simulated WST — no real funds moved.",
        })
        ueg_logged = True
    except Exception:
        pass
    return {"vsb_id": req.vsb_id, "entity_type": entity_type,
            "entity_type_source": et_source, "ueg_logged": ueg_logged, **result}


@router.get("/board-pack")
async def board_pack(vsb_id: str = "workstation-idbo", entity_type: str = DEFAULT_ENTITY,
                     user: dict | None = Depends(get_current_user)):
    """§7 Financial Board Pack — the live owner-facing financial statement, assembled on demand: the P&L
    summary, the effective distribution waterfall, the Owner's accrued payments, the venture portfolio, charity
    given, and the §8 organism posture. Virtual/simulated WST only — no real funds; assembled fresh (≤5-min
    staleness invariant)."""
    _require_economy_access(vsb_id, user)
    import time as _t
    from agentic_core.economy.owner_payments import status as _owner_status
    from agentic_core.economy.ventures import portfolio as _venture_portfolio

    # W442 refuter catch: the owner-facing financial pack still took entity_type from the caller's
    # query and owner from the constructor default ("Rehan") — the claim-echo class W442 fixed on
    # /status and /close-period, left live on the surface the UI actually renders.
    entity_type, _et_source = _resolve_entity_type(vsb_id, entity_type)
    _owner, _owner_source = "Rehan", "platform_default"
    try:
        from agentic_core.economy.living_vsbs import _load as _lv_load
        _rec = _lv_load().get(vsb_id)
        if _rec and _rec.get("owner"):
            _owner, _owner_source = str(_rec["owner"]), "living_registry"
    except Exception:
        pass
    m = EconomicMetabolism(vsb_id, entity_type, _owner)
    stmt = m.ledger.statement()
    bal = stmt["balances"]
    stages = ("owner", "self_investment", "capital_fund", "user_projects", "charity")
    revenue = round(bal.get("revenue", 0.0), 2)
    reserves = round(bal.get("reserves", 0.0), 2)
    distributed = round(sum(bal.get(s, 0.0) for s in stages), 2)
    try:
        owner = _owner_status(vsb_id, m.owner)
        owner_section = {"accrued_wst": owner["accrued_total_wst"], "paid_out_wst": owner["paid_out_total_wst"],
                         "balance_wst": owner["balance_wst"], "real_money_rails": owner["real_money_rails"],
                         "available": True}
    except Exception as _own_err:
        # W465 (FU-016) — the rest of the pack stands; this section says it could not be read (never zeros)
        owner_section = {"available": False, "real_money_rails": "DISABLED",
                         "error": f"the owner-payments store could not be read: {str(_own_err)[:160]}"}
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
        "attribution": {"entity_type_source": _et_source, "owner_source": _owner_source},
        "currency": "WST (virtual)", "generated_at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()),
        "profit_and_loss": {
            "total_revenue_wst": revenue, "total_reserves_wst": reserves,
            "total_distributed_wst": distributed,
            "distribution_by_stage": {s: round(bal.get(s, 0.0), 2) for s in stages},
        },
        "waterfall": {"effective": m.waterfall, "source": m.waterfall_source},
        "owner_payments": owner_section,
        "venture_portfolio": {"invested_total_wst": ventures["invested_total"],
                              "positions": ventures.get("positions_count", 0),
                              "holdings": ventures.get("holdings", [])[:5]},
        "charitable_giving": {"total_given_wst": round(bal.get("charity", 0.0), 2)},
        "organism_posture": organism,
        # §9.1 — the CFO's three statements (current period, from the REAL double-entry postings)
        "statements": m.ledger.statements(),
        "ledger": {"entry_count": stmt["entry_count"], "recent": stmt["recent"]},
        "governance": "gaas.v5-gated cycles · UEG append-only audit · arms-length distribution policy",
        "disclaimer": "Virtual/simulated WST only — no real funds. Real-money rails are gated until the Owner "
                      "authorises them AND a compliance review passes.",
    }


@router.get("/ledger/{vsb_id}")
async def get_ledger(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_economy_access(vsb_id, user)
    return EconomicMetabolism(vsb_id).status()["ledger"]


@router.get("/charity/candidates")
async def charity_candidates(top: int = 8, user: dict | None = Depends(get_current_user)):
    """§5 — the ranked charitable-cause pool the directives act on. Weights are CURATED editorial
    values (or Owner-gated ingested signals) — nothing is measured; every row says which."""
    ranked = CharityIntelligence().ranked(top)
    # W442 — the disclaimer was STATIC ("sources curated") and became false the moment ingested
    # signals joined the pool; it is now computed from what the pool actually contains.
    n_signal = sum(1 for c in ranked if str(c.get("weights_source", "")).startswith("owner_signal"))
    # W442 refuter catch: the ranked pool is EXCLUSION-FILTERED, so the UI's typo check against it
    # flagged every CORRECT exclusion as "matches no cause". Typed ids validate against the
    # unfiltered id universe instead.
    from agentic_core.economy.charity import _CANDIDATES, approved_signals
    all_ids = sorted({c["id"] for c in _CANDIDATES} | {s["id"] for s in approved_signals()})
    return {"candidates": ranked,
            "all_cause_ids": all_ids,
            "method": ("weighted rank over CURATED priority weights (urgency · gravity · reach · "
                       "marginal-impact · trust) — editorial values, not measurements"),
            "pool": {"curated": len(ranked) - n_signal, "ingested_signals": n_signal},
            "disclaimer": ("Virtual/simulated. " +
                           ("Pool includes Owner-gated ingested signal rows (caller-asserted values) "
                            "alongside the curated set." if n_signal else
                            "Sources curated; live feeds pending Owner approval."))}


@router.get("/charity/directives")
async def get_charity_directives(user: dict | None = Depends(get_current_user)):
    """§5 — the Owner's charity directives (priorities · exclusions · 100%-donation rule), honoured
    by every allocation. Also reports the live-signal gate state (read-only) so the UI can say
    whether ingestion is enabled without probing the POST."""
    import os as _os
    from agentic_core.economy.charity import approved_signals, get_directives
    d = get_directives()
    d["live_signals"] = {
        "enabled": _os.getenv("CHARITY_LIVE_SIGNALS_ENABLED", "false").lower() == "true",
        "approved_signal_count": len(approved_signals()),
        "note": "Owner-gated — no fabricated feeds; sources must be Owner-approved.",
    }
    return d


class CharityDirectivesRequest(BaseModel):
    priorities: list[str] = []
    exclusions: list[str] = []
    require_100pct: bool = True


@router.post("/charity/directives")
async def set_charity_directives(req: CharityDirectivesRequest,
                                 user: dict | None = Depends(get_current_user)):
    """§5 — the Owner SETS the charity directives at runtime; persisted + UEG-logged + honoured by
    the metabolic cycle's allocations from the next cycle on.

    W442 — these directives are GLOBAL (they steer the charity stage of EVERY tenant's waterfall)
    yet the route had no auth dependency at all: under multi-user auth any caller could rewrite
    the Owner's priorities/exclusions/100% rule. Platform-scoped now (admin-only under auth)."""
    _require_economy_access("workstation-idbo", user)
    from agentic_core.economy.charity import set_directives
    result = set_directives(req.priorities or None, req.exclusions, req.require_100pct)
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.charity_directives_set", **{k: result[k] for k in
                        ("priorities", "exclusions", "require_100pct")}})
    except Exception:
        pass
    return result


class CharitySignalsRequest(BaseModel):
    signals: list[dict] = []   # each mirrors a candidate: {id, cause, region, urgency, gravity, reach, trust, donation_100pct}


@router.post("/charity/signals")
async def ingest_charity_signals(req: CharitySignalsRequest,
                                 user: dict | None = Depends(get_current_user)):
    """§5 — the REAL live-signal ingestion seam (humanitarian/disaster/needs feeds). OWNER-GATED:
    disabled unless CHARITY_LIVE_SIGNALS_ENABLED=true (no fabricated feeds; sources must be
    Owner-approved). Accepted signals persist and join the candidate pool."""
    import math as _math
    import os as _os
    import time as _time
    if _os.getenv("CHARITY_LIVE_SIGNALS_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=403, detail=(
            "Live charity-signal ingestion is Owner-gated (set CHARITY_LIVE_SIGNALS_ENABLED=true "
            "after approving the sources). No fabricated feeds are ever used."))
    # W442 — even with the flag on, the route had NO auth dependency: any network caller could
    # fabricate the "Owner-approved" feed steering every tenant's charity stage. Platform-scoped
    # (admin-only under auth), each row stamped with who submitted it and validated per-field —
    # junk values used to raise an unhandled 500; they are now rejected and REPORTED.
    _require_economy_access("workstation-idbo", user)
    from agentic_core.config import atomic_write_json, store_lock
    from agentic_core.economy.charity import _SIGNALS_STORE, approved_signals

    def _finite01(v) -> bool:
        try:
            f = float(v)
        except (TypeError, ValueError):
            return False
        return _math.isfinite(f) and 0.0 <= f <= 1.0

    valid, rejected = [], []
    for s in req.signals:
        if (isinstance(s, dict) and s.get("id") and s.get("cause")
                and all(_finite01(s.get(k, 0.5)) for k in ("urgency", "gravity", "reach", "trust"))):
            valid.append({**s, "submitted_by": (user or {}).get("username") or "anonymous",
                          "submitted_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime())})
        else:
            rejected.append({"id": (s.get("id") if isinstance(s, dict) else None),
                             "reason": "missing id/cause or non-finite/out-of-range weight"})
    with store_lock(_SIGNALS_STORE):
        existing = {s["id"]: s for s in approved_signals()}
        replaced = [s["id"] for s in valid if s["id"] in existing]
        for s in valid:
            existing[s["id"]] = s
        atomic_write_json(_SIGNALS_STORE, list(existing.values()))
    ueg_logged = False
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.charity_signals_ingested", "count": len(valid),
                         "rejected": len(rejected), "replaced": replaced,
                         "submitted_by": (user or {}).get("username") or "anonymous"})
        ueg_logged = True
    except Exception:
        pass
    return {"ingested": len(valid), "rejected": rejected, "replaced_ids": replaced,
            "total_signals": len(existing), "ueg_logged": ueg_logged,
            "note": ("Signals join the candidate pool labelled 'owner_signal (ingested; "
                     "caller-asserted values)' — still subject to the 100%-donation rule + "
                     "compliance screening.")}


@router.get("/ventures/candidates")
async def venture_candidates(top: int = 8, vsb_id: str = "workstation-idbo",
                             user: dict | None = Depends(get_current_user)):
    """§6 — ranked candidate ventures for investment, harvested from the platform's REAL projects and
    living VSB offspring (metrics derived deterministically from live stage/status/governance); the
    curated demo set only when the platform is empty (honestly flagged). Virtual/simulated."""
    _require_economy_access(vsb_id, user)
    from agentic_core.economy.ventures import VentureIntelligence, real_candidates
    # W442 — the harvest leaked every tenant's project titles + living enterprises to any caller;
    # scoped to what THIS user can access (the internal cycle path keeps the federation view).
    vi = VentureIntelligence(real_candidates(exclude_vsb=vsb_id, user=user) or None)
    return {"candidates": vi.ranked(top),
            "method": "outcome × value × benefit × feasibility × strategic-fit",
            "using_demo_candidates": vi.using_demo,
            "disclaimer": ("Virtual/simulated WST. Candidates are the platform's REAL projects/VSBs with "
                           "deterministically-derived metrics — the demo set only when the platform is empty.")}


class VentureReturnRequest(BaseModel):
    vsb_id: str = "workstation-idbo"
    holding_id: str
    amount: float = Field(gt=0, allow_inf_nan=False)   # W442 — inf/NaN minted WST from nothing
    memo: str = ""


@router.post("/ventures/return")
async def venture_return(req: VentureReturnRequest, user: dict | None = Depends(get_current_user)):
    """§6 — record a virtual RETURN on a portfolio holding; it queues as a pending return that the
    NEXT metabolic cycle consumes as intake revenue, so returns genuinely recycle into the waterfall.
    UEG-logged. Virtual WST only — no real funds."""
    _require_economy_access(req.vsb_id, user)
    from agentic_core.economy.ventures import record_return
    try:
        result = record_return(req.vsb_id, req.holding_id, req.amount, req.memo)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    ueg_logged = False
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.venture_return", "vsb_id": req.vsb_id,
                         "holding_id": req.holding_id, "amount_wst": result["returned_wst"],
                         "amount_source": "caller_asserted (bounded at 10× invested)",
                         "disclaimer": "Virtual/simulated WST — no real funds moved."})
        ueg_logged = True
    except Exception:
        pass
    return {**result, "ueg_logged": ueg_logged}


@router.get("/ventures/portfolio")
async def venture_portfolio(vsb_id: str = "workstation-idbo",
                            user: dict | None = Depends(get_current_user)):
    """§6 — the VSB's venture portfolio: positions accrued from each cycle's user_projects allocation (virtual)."""
    _require_economy_access(vsb_id, user)
    from agentic_core.economy.ventures import portfolio
    return portfolio(vsb_id)
