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
