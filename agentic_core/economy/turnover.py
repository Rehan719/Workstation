"""P3.26 clause (4) — the entities that may NEVER be retired automatically, ENFORCED rather than documented.

Every rule is evaluated, not the first that fires, so a reader sees every reason an entity is protected. Each rule
answers one of three verdicts: `refuses` (this entity is protected by it), `clear` (it is not), or
`not_assessable` (the rule could not be checked). FAIL-SAFE: any not_assessable makes the whole answer a refusal,
because the clause says NEVER auto-retire, and "could not confirm it is unprotected" is not "unprotected".

THE "NAMED IN A RULING" RULE HAS NO SOURCE IN CODE: the council's rulings are held in memory and carry no entity id.
So it reads a record a person writes, data/governance/protected_entities.json ({"entities": {vsb_id: reason}});
when that record does not exist the rule is not_assessable and says why, and nothing is retired.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List

from agentic_core.config import data_path, read_json_strict

QEP_ENTITY_TYPE = "qep_waqf_trust"


def _rule(rule: str, verdict: str, basis: str) -> Dict[str, Any]:
    return {"rule": rule, "verdict": verdict, "basis": basis}


def _unsettled(vsb_id: str) -> Dict[str, Any]:
    from agentic_core.economy import revenue, transfers, ventures
    try:
        legs = transfers.open_legs_for(vsb_id)
        if legs.get("ledger_unreadable"):
            return _rule("unsettled_obligations", "not_assessable", "the transfer ledger could not be read whole")
        pend = revenue.peek_pending(vsb_id)
        #  read the portfolio itself: peek_pending_returns answers 0.0 when its store is unreadable
        pf = ventures._load_portfolio().get(vsb_id) or {}
    except Exception as exc:  # noqa: BLE001 - an unreadable obligation store is never "nothing owed"
        return _rule("unsettled_obligations", "not_assessable", f"an obligation store could not be read ({exc.__class__.__name__})")
    owed = []
    if legs.get("open") or legs.get("settling") or legs.get("credited_unclosed"):
        owed.append(f"{len(legs.get('open') or [])} open and {len(legs.get('settling') or [])} settling transfer leg(s)")
    if int(pend.get("events") or 0) > 0:
        owed.append(f"{pend['events']} unconsumed revenue/cost event(s)")
    if float(pf.get("pending_returns_wst") or 0.0) > 0:
        owed.append(f"{pf['pending_returns_wst']} WST of venture returns queued")
    return (_rule("unsettled_obligations", "refuses", "it has unsettled obligations: " + "; ".join(owed)) if owed else
            _rule("unsettled_obligations", "clear", "no open transfer leg, no unconsumed event, no queued return"))


def _hold(rec: Dict[str, Any]) -> Dict[str, Any]:
    from agentic_core.economy.living_vsbs import _DECISION_HOLDS
    h = rec.get("last_hold")
    if (h in _DECISION_HOLDS) or rec.get("decision_hold"):
        return _rule("governance_hold", "refuses", f"it is under a governance hold ({h or rec.get('decision_hold')})")
    return _rule("governance_hold", "clear", "no governance hold is recorded on it")


def _ruling(vsb_id: str) -> Dict[str, Any]:
    try:
        d = read_json_strict(data_path("governance/protected_entities.json"), missing=None, expect=dict)
    except Exception as exc:  # noqa: BLE001
        return _rule("named_in_a_ruling", "not_assessable", f"the protected-entities record could not be read ({exc.__class__.__name__})")
    if d is None:
        return _rule("named_in_a_ruling", "not_assessable",
                     ("no record of entities named in a ruling exists (data/governance/protected_entities.json), and "
                      "the council's rulings carry no entity id, so whether this entity is named in one is NOT KNOWN"))
    named = (d.get("entities") or {})
    if vsb_id in named:
        return _rule("named_in_a_ruling", "refuses", f"it is named in a ruling: {named[vsb_id]}")
    return _rule("named_in_a_ruling", "clear", "it is not on the record of entities named in a ruling")


def _qep(rec: Dict[str, Any], vsb: Dict[str, Any]) -> Dict[str, Any]:
    et = rec.get("entity_type") or (vsb.get("economy") or {}).get("entity_type")
    if et == QEP_ENTITY_TYPE:
        return _rule("qep_entity", "refuses", "it is the QEP entity (entity type qep_waqf_trust)")
    return _rule("qep_entity", "clear", f"its entity type is {et!r}, not the QEP's")


def _last_in_pair(vsb_id: str, rec: Dict[str, Any], vsb: Dict[str, Any], roster: Dict[str, Any],
                  load_vsb: Callable[[str], Any]) -> Dict[str, Any]:
    from agentic_core.economy.living_vsbs import lifecycle
    realm = vsb.get("realm")
    domain = rec.get("domain") or vsb.get("domain")
    if not realm or not domain:
        return _rule("last_in_realm_domain", "not_assessable",
                     f"its realm ({realm!r}) or domain ({domain!r}) is not recorded, so its peers cannot be counted")
    peers = 0
    for oid, o in roster.items():
        if oid == vsb_id or not isinstance(o, dict) or o.get("lifecycle_state") == "retired":
            continue
        #  a peer is any living entity in the same pair: operable, or dormant (dormancy is reversible)
        if (o.get("domain") or "") != domain or (not lifecycle(o)["operable"] and o.get("lifecycle_state") != "dormant"):
            continue
        ov = load_vsb(oid) or {}
        if ov.get("realm") == realm:
            peers += 1
    if peers == 0:
        return _rule("last_in_realm_domain", "refuses", f"it is the last living entity in {realm} x {domain}")
    return _rule("last_in_realm_domain", "clear", f"{peers} other living entit(y/ies) share {realm} x {domain}")


def retirement_refusal(vsb_id: str) -> Dict[str, Any]:
    """Every never-auto-retire rule for this entity. refused True when ANY refuses or cannot be assessed."""
    from agentic_core.api.vsb import _load_vsb
    from agentic_core.economy.living_vsbs import _load
    try:
        roster = _load()
    except Exception as exc:  # noqa: BLE001
        return {"vsb_id": vsb_id, "refused": True, "rules": [],
                "basis": f"the living roster could not be read ({exc.__class__.__name__}), so nothing is retired"}
    rec = roster.get(vsb_id)
    if not isinstance(rec, dict):
        return {"vsb_id": vsb_id, "refused": True, "rules": [],
                "basis": f"{vsb_id} is not on the living roster, so there is nothing to retire"}
    vsb = _load_vsb(vsb_id) or {}
    rules: List[Dict[str, Any]] = [_unsettled(vsb_id), _hold(rec), _ruling(vsb_id), _qep(rec, vsb),
                                   _last_in_pair(vsb_id, rec, vsb, roster, _load_vsb)]
    refusing = [r["rule"] for r in rules if r["verdict"] == "refuses"]
    unknown = [r["rule"] for r in rules if r["verdict"] == "not_assessable"]
    refused = bool(refusing or unknown)
    basis = ("REFUSED: " + "; ".join(
        ([f"protected by {', '.join(refusing)}"] if refusing else [])
        + ([f"could not confirm it is unprotected ({', '.join(unknown)}), and an unknown is not a clear"]
           if unknown else []))) if refused else "no never-auto-retire rule protects it; every rule was checked"
    return {"vsb_id": vsb_id, "refused": refused, "refusing": refusing, "not_assessable": unknown,
            "rules": rules, "basis": basis}


#  ── P3.26 clauses (3) and (7) — RETIREMENT IS GOVERNED, AND APOPTOSIS CONSERVES ───────────────────────────
#  A removal is PROPOSED through Change Control (autophagy, clause 7), never set directly: propose_removal files
#  the change only for an entity no never-auto-retire rule protects, naming what it would remove and why. The
#  change is applied by Change Control's implement step, which calls apply_retirement: it RE-CHECKS the rules
#  (an entity can become protected between filing and approval), then moves every asset balance out of the
#  entity's books into the Sovereign Capital Fund with a balanced posting each, credits the fund by exactly that
#  total, and marks the entity retired. THE RECORD IS KEPT: the roster row and the books stay readable, and
#  nothing is deleted, because a retirement that loses its record fails the clause as surely as one that loses
#  a balance.
RETIREMENT_CHANGE_TYPE = "entity_retirement"
_ASSET_ACCOUNTS = ("cash", "reserve_fund")


async def propose_removal(vsb_id: str, why: str, by: str) -> Dict[str, Any]:
    why, by = str(why or "").strip(), str(by or "").strip()
    #  one key set on every path (P2.21 clause 2), declared once
    out: Dict[str, Any] = {"filed": False, "refused": None, "cca_id": None, "check": None, "basis": ""}
    if not why or not by:
        out.update(refused="incomplete", basis="REFUSED: a removal names why it is proposed and who proposes it")
        return out
    chk = retirement_refusal(vsb_id)
    if chk["refused"]:
        out.update(refused="protected", check=chk, basis=f"NOT FILED: {chk['basis']}")
        return out
    from agentic_core.api.change_control import SubmitChangeRequest, submit_change
    rec = await submit_change(SubmitChangeRequest(
        title=f"[turnover] retire {vsb_id}", change_type=RETIREMENT_CHANGE_TYPE, vsb_id=vsb_id,
        description=(f"Retire living entity {vsb_id}: its asset balances move to the Sovereign Capital Fund, its "
                     f"record and books are KEPT, and the organism stops operating it. Why: {why}"),
        rationale=why, submitted_by=by,
        affected_systems=[vsb_id, "living roster", "Sovereign Capital Fund"],
        rollback_plan=("the record is kept, so a retirement is reversible by Change Control; the moved balance "
                       "is attributed in the fund to this entity")))
    out.update(filed=True, cca_id=rec.get("cca_id"), check=chk,
               basis=f"filed through Change Control as {rec.get('cca_id')}; nothing moves until it is approved and implemented")
    return out


def apply_retirement(vsb_id: str, cca_id: str) -> Dict[str, Any]:
    """Change Control's implement step for an approved retirement. Re-checks, conserves, keeps the record."""
    chk = retirement_refusal(vsb_id)
    out: Dict[str, Any] = {"retired": False, "refused": None, "check": chk, "conserved_wst": None, "moved": None,
                           "fund_after": None, "basis": ""}
    if chk["refused"]:
        out.update(refused="protected", basis=f"NOT RETIRED: {chk['basis']}")
        return out
    from agentic_core.api.capital_fund import contribute_from_cycle
    from agentic_core.config import store_lock
    from agentic_core.economy.ledger import VirtualLedger
    from agentic_core.economy import living_vsbs as _lv
    led = VirtualLedger(vsb_id)
    bal = led.chart_balances()
    moved: Dict[str, float] = {}
    for acct in _ASSET_ACCOUNTS:
        amt = round(float(bal.get(acct) or 0.0), 2)
        if amt > 0:
            led.post(debit="distribution_capital_fund", credit=acct, amount=amt,
                     memo=f"apoptosis: {vsb_id} retired by {cca_id}", source="apoptosis")
            moved[acct] = amt
    total = round(sum(moved.values()), 2)
    if total > 0:
        contribute_from_cycle(vsb_id, total)
    from agentic_core.api.capital_fund import _load_fund
    fund_after = (_load_fund() or {}).get("total_capital")
    stamp = _lv._now()
    with store_lock(_lv._STORE):
        d = _lv._load()
        rec = d.get(vsb_id)
        if isinstance(rec, dict):
            prev = rec.get("lifecycle_state")
            rec["lifecycle_state"] = "retired"
            rec["lifecycle_basis"] = _lv.lifecycle(rec)["basis"]
            rec.setdefault("lifecycle_history", []).append(
                {"from": prev, "to": "retired", "by": f"cca:{cca_id}", "at": stamp, "note": "governed retirement"})
            rec["retirement"] = {"cca_id": cca_id, "at": stamp, "conserved_wst": total, "moved": moved}
            _lv._save(d)
    out.update(retired=True, conserved_wst=total, moved=moved, fund_after=fund_after)
    out["basis"] = (f"retired: {total} WST moved from its books to the Sovereign Capital Fund "
                      f"({', '.join(f'{k} {v}' for k, v in moved.items()) or 'it held nothing'}); its record and books "
                      f"are kept and the organism no longer operates it")
    return out


#  ── P3.26 clause (5) — MITOSIS: a mature entity divides, the child inherits its constitution VERBATIM ─────────
#  Funded from the parent's own share - its reserve fund - by transfers.record_transfer, which debits the parent
#  inside the ledger lock and queues the same amount into the child's intake, so nothing is created and nothing
#  goes negative. Proposed and applied through Change Control, like retirement; the implement step re-checks
#  maturity and funds, because both can change between filing and approval.
MITOSIS_CHANGE_TYPE = "entity_mitosis"
#  the STORED parts a constitution is derived from (api/vsb.py derives the rest on read from these)
CONSTITUTION_FIELDS = ("constitution", "values", "genome_spec", "epigenetic_traits", "problem", "entity_type")


def constitution_of(vsb: Dict[str, Any]) -> Dict[str, Any]:
    import copy
    return {k: copy.deepcopy(vsb.get(k)) for k in CONSTITUTION_FIELDS}


def _mitosis_check(parent_id: str, amount: float) -> Dict[str, Any]:
    from agentic_core.economy.ledger import VirtualLedger
    from agentic_core.economy.living_vsbs import _load
    rec = (_load() or {}).get(parent_id)
    if not isinstance(rec, dict):
        return {"ok": False, "refused": "not_on_roster", "basis": f"{parent_id} is not on the living roster"}
    if rec.get("lifecycle_state") != "mature":
        return {"ok": False, "refused": "not_mature",
                "basis": (f"{parent_id} is {rec.get('lifecycle_state') or 'UNRECORDED'}, and only a MATURE entity "
                          f"divides")}
    try:
        amt = round(float(amount), 2)
    except (TypeError, ValueError):
        return {"ok": False, "refused": "bad_amount", "basis": f"{amount!r} is not an amount"}
    if amt <= 0:
        return {"ok": False, "refused": "bad_amount", "basis": "a child is funded with a positive amount"}
    reserve = round(float(VirtualLedger(parent_id).chart_balances().get("reserve_fund") or 0.0), 2)
    if amt > reserve:
        return {"ok": False, "refused": "insufficient_share",
                "basis": f"the parent's reserve fund holds {reserve} WST, less than the {amt} WST asked"}
    return {"ok": True, "refused": None, "amount": amt, "reserve": reserve, "basis": "mature and funded"}


async def propose_mitosis(parent_id: str, child_name: str, amount: float, why: str, by: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"filed": False, "refused": None, "cca_id": None, "check": None, "basis": ""}
    if not str(child_name or "").strip() or not str(why or "").strip() or not str(by or "").strip():
        out.update(refused="incomplete", basis="REFUSED: a division names the child, why, and who proposes it")
        return out
    chk = _mitosis_check(parent_id, amount)
    out["check"] = chk
    if not chk["ok"]:
        out.update(refused=chk["refused"], basis=f"NOT FILED: {chk['basis']}")
        return out
    from agentic_core.api.change_control import SubmitChangeRequest, submit_change
    rec = await submit_change(SubmitChangeRequest(
        title=f"[turnover] {parent_id} divides: {str(child_name)[:60]}", change_type=MITOSIS_CHANGE_TYPE,
        vsb_id=parent_id, submitted_by=str(by), rationale=str(why),
        description=(f"Mitosis: {parent_id} creates the subsidiary {child_name!r}, which inherits its constitution "
                     f"verbatim and is funded with {chk['amount']} WST moved from the parent's reserve fund. "
                     f"Why: {why}"),
        affected_systems=[parent_id, "living roster", "VSB store", "ledger"]))
    # the child's name and amount travel on the record, read back by the implement step
    from agentic_core.api.change_control import _load_change, _save_change
    c = _load_change(rec.get("cca_id")) or {}
    c["mitosis"] = {"child_name": str(child_name)[:120], "amount_wst": chk["amount"]}
    _save_change(c)
    out.update(filed=True, cca_id=rec.get("cca_id"),
               basis=f"filed as {rec.get('cca_id')}; nothing is created or moved until it is approved and implemented")
    return out


def apply_mitosis(parent_id: str, cca_id: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"divided": False, "refused": None, "child_vsb": None, "amount_wst": None,
                           "constitution_inherited": None, "transfer": None, "basis": ""}
    chk = _mitosis_check(parent_id, (spec or {}).get("amount_wst"))
    if not chk["ok"]:
        out.update(refused=chk["refused"], basis=f"NOT DIVIDED: {chk['basis']}")
        return out
    import uuid
    from agentic_core.api.vsb import _load_vsb, _save_vsb, enrich_vsb_entity
    from agentic_core.economy.transfers import record_transfer
    parent = _load_vsb(parent_id) or {}
    child_id = f"vsb-{uuid.uuid4().hex[:10]}"
    inherited = constitution_of(parent)
    child = {"vsb_id": child_id, "name": str(spec.get("child_name") or child_id), "domain": parent.get("domain"),
             "realm": parent.get("realm"), "owner_id": parent.get("owner_id", "default"), "generation": 0,
             "status": "living", "stage": "established", "born_of": {"parent": parent_id, "cca_id": cca_id}}
    child.update({k: v for k, v in inherited.items() if v is not None})
    child = enrich_vsb_entity(child, owner_id=parent.get("owner_id", "default"),
                              problem=str(parent.get("problem") or ""), domain=parent.get("domain") or "enterprise",
                              entity_type=str(parent.get("entity_type") or "waqf_ltd_hybrid"), parent_vsb=parent_id)
    #  enrichment may set defaults; the inherited parts are re-applied so they stay VERBATIM
    child.update({k: v for k, v in constitution_of(parent).items() if v is not None})
    _save_vsb(child)
    try:
        tr = record_transfer(parent_id, child_id, chk["amount"], memo=f"mitosis funding via {cca_id}",
                             transfer_id=f"mitosis-{cca_id}")   # idempotent on the change id: one division, one debit
    except Exception as exc:  # noqa: BLE001 - an unfunded child is never presented as a division
        from agentic_core.config import store_lock
        from agentic_core.economy import living_vsbs as _lv
        with store_lock(_lv._STORE):
            d = _lv._load()
            if isinstance(d.get(child_id), dict):
                d[child_id]["lifecycle_state"] = "retired"
                d[child_id]["retirement"] = {"cca_id": cca_id, "at": _lv._now(), "conserved_wst": 0.0,
                                             "moved": {}, "why": f"its funding transfer failed: {exc.__class__.__name__}"}
                _lv._save(d)
        out.update(refused="funding_failed", child_vsb=child_id,
                   basis=(f"NOT DIVIDED: the funding transfer failed ({exc.__class__.__name__}: {str(exc)[:120]}), "
                          f"so nothing left the parent; the created child {child_id} is retired with its record kept"))
        return out
    out.update(divided=True, child_vsb=child_id, amount_wst=chk["amount"], transfer=tr,
               constitution_inherited=sorted(k for k, v in inherited.items() if v is not None),
               basis=(f"{parent_id} divided: {child_id} inherits its constitution verbatim and is funded with "
                      f"{chk['amount']} WST from the parent's reserve fund"))
    return out
