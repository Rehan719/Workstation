"""W879 (FU-1008) - FOUR POPULATIONS, READ TOGETHER, CHANGING NOTHING.

The roster the heartbeat tends, the entity records, the ledgers and the owner accounts are four stores keyed by the
same id. On the Owner's store they held 36, 70, 107 and 103 (W676), and 59 ledgers belonged to no entity record. The
Owner ruled on 2026-10-12 that before any clause of the money-on-paper item, a reconciliation read runs across ledger,
owner payments, fund and roster, driven on a store made wrong in each way it can be.

This is the population part of that read. For every id that any of the four stores holds, it says which stores hold
it, groups the ids by that shape, and says what each shape means as the stores are written. It writes, moves and
deletes nothing. A store that cannot be read whole is NOT KNOWN: it is never read as an empty population, and each
shape lists it as not known. A member that cannot be read whole (one record, one ledger) is counted as present,
because its file is there, and is named as unreadable. The fund is read on its own route (GET /api/v1/fund/status,
its set_aside_reconciliation, W876): it is one pool, not a population keyed by entity.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

POPULATIONS = ("roster", "entity_records", "ledgers", "owner_accounts")
_NOUN = {"roster": "a place on the roster", "entity_records": "an entity record", "ledgers": "a ledger",
         "owner_accounts": "an owner account"}
#  Scopes the platform keeps books under that are not entities, so no entity record is expected for them.
PLATFORM_SCOPES = {
    "workstation-idbo": ("the platform's own scope: the economy routes' default id, admin-only under sign-in, which "
                         "has no entity record by design"),
}
LIST_CAP = 50


def _problem(what: str, exc: BaseException) -> str:
    return f"{what} could not be read whole ({type(exc).__name__}: {str(exc)[:160]})"


def _read_roster() -> Dict[str, Any]:
    from agentic_core.economy import living_vsbs as _lv
    try:
        d = _lv._load()
    except Exception as exc:                      # noqa: BLE001 - not known is said, never read as empty
        return {"ids": None, "problem": _problem("the roster", exc)}
    return {"ids": {str(k) for k in d}, "problem": None}


def _read_records() -> Dict[str, Any]:
    from agentic_core.api import vsb as _vsb
    from agentic_core.config import read_json_strict
    store = _vsb._VSB_STORE
    try:
        files = sorted(store.glob("*.json")) if store.exists() else []
    except OSError as exc:
        return {"ids": None, "problem": _problem("the entity records", exc)}
    ids, unreadable, mismatched = set(), [], []
    for p in files:
        ids.add(p.stem)                           # the file is there: the record exists, whether or not it reads
        try:
            rec = read_json_strict(p, dict, expect=dict)
        except Exception:                         # noqa: BLE001 - present, and named as unreadable
            unreadable.append(p.stem)
            continue
        if rec.get("vsb_id") != p.stem:           # a record naming no id is skipped by the entity listing
            mismatched.append({"id": p.stem, "record_says": rec.get("vsb_id")})
    return {"ids": ids, "problem": None, "unreadable": unreadable, "id_mismatch": mismatched}


def _read_ledgers() -> Dict[str, Any]:
    from agentic_core.economy import ledger as _led
    store = _led._STORE
    try:
        files = sorted(store.glob("*_ledger.json")) if store.exists() else []
    except OSError as exc:
        return {"ids": None, "problem": _problem("the ledgers", exc)}
    ids, unreadable = set(), []
    for p in files:
        vsb = p.name[: -len("_ledger.json")]
        ids.add(vsb)
        try:
            _led.read_strict(p, vsb)
        except Exception:                         # noqa: BLE001 - present, and named as unreadable
            unreadable.append(vsb)
    return {"ids": ids, "problem": None, "unreadable": unreadable}


def _read_accounts() -> Dict[str, Any]:
    from agentic_core.economy import owner_payments as _op
    try:
        d = _op._read()
    except Exception as exc:                      # noqa: BLE001 - not known is said, never read as empty
        return {"ids": None, "problem": _problem("the owner accounts", exc)}
    mismatched = [{"id": str(k), "account_says": a.get("vsb_id")} for k, a in sorted(d.items())
                  if isinstance(a, dict) and a.get("vsb_id") not in (None, k)]
    return {"ids": {str(k) for k in d}, "problem": None, "id_mismatch": mismatched}


def _reads_as(held: Dict[str, Optional[bool]], platform: Optional[str]) -> Dict[str, Any]:
    """What one shape of membership means as the stores are written, and whether a person must say what it is.
    Each membership is True, False, or None when that store could not be read."""
    roster, record, ledger, account = (held[p] for p in POPULATIONS)
    books = [_NOUN[p] for p in ("ledgers", "owner_accounts") if held[p]]
    if platform:
        return {"reads_as": PLATFORM_SCOPES[platform], "needs_a_person": False}
    if roster is True and record is True and ledger is True and account is True:
        return {"reads_as": "a registered entity with its record and both books: all four stores hold it",
                "needs_a_person": False}
    if roster is True and record is False:
        return {"reads_as": ("on the roster with no entity record: the heartbeat tends an id whose record is not "
                             "there, and only a person can say whether the record was lost or the place is stale"),
                "needs_a_person": True}
    if record is False and books:
        return {"reads_as": (f"{' and '.join(books)} with no entity record"
                             + (" and no place on the roster" if roster is False else
                                ", and whether it is on the roster is not known")
                             + ": a simulation's books (cycles run for a scope that was never established) or the "
                               "books of an entity whose record is gone. The stores cannot tell these apart, so a "
                               "person must say which"),
                "needs_a_person": True}
    if account is True and ledger is False:
        return {"reads_as": ("an owner account with no ledger beside it: what it accrued has no books of its own to "
                             "be reconciled against, so a person must say where it came from"),
                "needs_a_person": True}
    if record is True and roster is False:
        return {"reads_as": ("an entity record that is not on the roster: deregistered (deregistering keeps the "
                             "record and stops the tending) or never registered, so the heartbeat does not tend it"
                             + (f"; it has {' and '.join(books)}" if books else "")),
                "needs_a_person": False}
    if record is True and roster is True and ledger is False and account is False:
        return {"reads_as": "a registered entity with its record and no books yet: it has not been operated",
                "needs_a_person": False}
    if record is True and roster is True and ledger is True and account is False:
        return {"reads_as": ("a registered entity with its record and a ledger, and no owner account: no owner share "
                             "has been accrued to it"),
                "needs_a_person": False}
    not_known = [p for p in POPULATIONS if held[p] is None]
    return {"reads_as": ("held by " + (", ".join(_NOUN[p] for p in POPULATIONS if held[p]) or "nothing read")
                         + (f"; whether it has {' or '.join(_NOUN[p] for p in not_known)} is not known, because that "
                            "store could not be read" if not_known else "")),
            "needs_a_person": False}


def reconcile() -> Dict[str, Any]:
    """The four populations, read together. Read-only: nothing is written, moved or deleted."""
    read = {"roster": _read_roster(), "entity_records": _read_records(), "ledgers": _read_ledgers(),
            "owner_accounts": _read_accounts()}
    known = [p for p in POPULATIONS if read[p]["ids"] is not None]
    unknown = [p for p in POPULATIONS if p not in known]
    every = set().union(*(read[p]["ids"] for p in known)) if known else set()
    shapes: Dict[tuple, List[str]] = {}
    for vid in sorted(every):
        key = tuple((vid in read[p]["ids"]) if p in known else None for p in POPULATIONS)
        shapes.setdefault(key + ((vid if vid in PLATFORM_SCOPES else None),), []).append(vid)
    rows = []
    for key, ids in sorted(shapes.items(), key=lambda kv: (-len(kv[1]), repr(kv[0]))):
        held = dict(zip(POPULATIONS, key[:4]))
        rows.append({"held_by": [p for p in POPULATIONS if held[p]],
                     "not_held_by": [p for p in POPULATIONS if held[p] is False],
                     "not_known": [p for p in POPULATIONS if held[p] is None],
                     "count": len(ids), "ids": ids[:LIST_CAP], "ids_listed": min(len(ids), LIST_CAP),
                     **_reads_as(held, key[4])})
    counts = {p: (len(read[p]["ids"]) if read[p]["ids"] is not None else None) for p in POPULATIONS}
    unreadable = {p: read[p]["unreadable"] for p in ("entity_records", "ledgers") if read[p].get("unreadable")}
    mismatch = {p: read[p]["id_mismatch"] for p in ("entity_records", "owner_accounts") if read[p].get("id_mismatch")}
    in_all = sum(r["count"] for r in rows if len(r["held_by"]) == 4)
    need = sum(r["count"] for r in rows if r["needs_a_person"])
    complete = not unknown and not unreadable
    figures = ", ".join(f"{counts[p] if counts[p] is not None else 'not known'} {lbl}" for p, lbl in (
        ("roster", "on the roster"), ("entity_records", "entity records"), ("ledgers", "ledgers"),
        ("owner_accounts", "owner accounts")))
    basis = (f"{figures}: {len(every)} distinct id(s) across the stores that could be read, {in_all} of them in all "
             f"four. {need} id(s) need a person to say what they are, because books or a place on the roster stand "
             f"where the stores cannot explain them; every other shape follows from how the stores are written, and "
             f"says how. Read only: nothing was written, moved or deleted.")
    if unknown:
        basis += (" NOT KNOWN: " + "; ".join(read[p]["problem"] for p in unknown)
                  + ". No id's membership of that store is said; each shape lists it as not known.")
    if unreadable:
        basis += " " + "; ".join(f"{len(v)} {p.replace('_', ' ')} could not be read whole: {', '.join(v[:10])}"
                                 for p, v in unreadable.items()) + " (counted as present, because the file is there)."
    if mismatch:
        basis += " " + "; ".join(f"{len(v)} of the {p.replace('_', ' ')} do not name, inside, the id they are "
                                 f"filed under" for p, v in mismatch.items()) + "."
    return {"populations": counts, "not_known": {p: read[p]["problem"] for p in unknown},
            "distinct_ids": len(every), "in_all_four": in_all, "needs_a_person": need,
            "complete": complete, "reconciled": bool(complete and need == 0 and not mismatch),
            "shapes": rows, "unreadable": unreadable, "id_mismatch": mismatch,
            "platform_scopes": dict(PLATFORM_SCOPES), "basis": basis,
            "fund": "read on its own route: GET /api/v1/fund/status, set_aside_reconciliation (W876)",
            "writes": "none"}
