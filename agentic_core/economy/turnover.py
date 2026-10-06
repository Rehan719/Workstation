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
