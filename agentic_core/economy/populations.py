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
    ids, unreadable, owner = set(), [], {}
    for p in files:
        vsb = p.name[: -len("_ledger.json")]
        ids.add(vsb)
        try:
            owner[vsb] = owner_book(_led.read_strict(p, vsb))      # W880 (FU-1009) - its owner share, read once
        except Exception:                         # noqa: BLE001 - present, and named as unreadable
            unreadable.append(vsb)
    return {"ids": ids, "problem": None, "unreadable": unreadable, "owner": owner}


def _read_accounts() -> Dict[str, Any]:
    from agentic_core.economy import owner_payments as _op
    try:
        d = _op._read()
    except Exception as exc:                      # noqa: BLE001 - not known is said, never read as empty
        return {"ids": None, "problem": _problem("the owner accounts", exc)}
    mismatched = [{"id": str(k), "account_says": a.get("vsb_id")} for k, a in sorted(d.items())
                  if isinstance(a, dict) and a.get("vsb_id") not in (None, k)]
    return {"ids": {str(k) for k in d}, "problem": None, "id_mismatch": mismatched, "accounts": d}


#  W880 (FU-1009) - WHICH RECORD IS THE OWNER'S SHARE. Every cycle's owner share is recorded twice: in the owner pot
#  (record("owner", ...)) and, since double entry began, as a posting Dr distribution_owner / Cr cash. It is accrued a
#  third time, to the owner account a payout draws on, and a failed accrual waits as a claim since W505.
OWNER_SHARE_RECORD = ("The owner's share is what the book of record distributed to the owner: the double-entry owner "
                      "postings (the Owner's ruling of 2026-10-12). The owner account is the record a payout draws on; "
                      "where it differs from the book of record, the difference is said here and nothing is "
                      "corrected. The pot is a derived view and holds books older than double entry.")


def owner_book(data: Dict[str, Any]) -> Dict[str, Any]:
    """The owner's share as one ledger's two books hold it. A period close credits distribution_owner back to retained
    earnings, so the share distributed is the debits to it that are not a close, less any credit that is not one."""
    postings = [p for p in (data.get("postings") or []) if isinstance(p, dict)]
    booked = 0.0
    for p in postings:
        if p.get("source") == "period_close" or str(p.get("memo") or "").startswith("period close"):
            continue                              # a close moves the share into retained earnings and pays nobody
        if p.get("debit") == "distribution_owner":
            booked += float(p.get("amount") or 0.0)
        elif p.get("credit") == "distribution_owner":
            booked -= float(p.get("amount") or 0.0)
    first = min((str(p.get("ts") or "") for p in postings if p.get("ts")), default=None)
    before = sum(float(e.get("amount") or 0.0) for e in (data.get("entries") or [])
                 if isinstance(e, dict) and e.get("account") == "owner" and e.get("kind", "credit") == "credit"
                 and (first is None or str(e.get("ts") or "") < first))
    return {"book_of_record_wst": round(booked, 2),
            "pot_wst": round(float((data.get("balances") or {}).get("owner", 0.0) or 0.0), 2),
            "double_entry_began": first, "pot_before_double_entry_wst": round(before, 2)}


def _share_row(vid: str, book: Optional[Dict[str, Any]], book_problem: Optional[str], acct: Any,
               acct_problem: Optional[str], pending: Any, pending_problem: Optional[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"vsb_id": vid, "owner_share_is": OWNER_SHARE_RECORD}
    problems = [x for x in (book_problem, acct_problem,
                            pending_problem and f"the claims from failed accruals could not be read ({pending_problem})")
                if x]
    if problems:
        out.update({"known": False, "basis": "NOT KNOWN: " + "; ".join(problems) + ". Nothing is compared."})
        return out
    acct = acct if isinstance(acct, dict) else None
    accrued = round(float((acct or {}).get("accrued") or 0.0), 2)
    paid = round(float((acct or {}).get("paid_out") or 0.0), 2)
    pend = round(float(pending or 0.0), 2)
    out.update({"known": True, "ledger_exists": book is not None, "account_exists": acct is not None,
                "accrued_wst": accrued, "paid_out_wst": paid, "pending_claims_wst": pend,
                "simulated": bool((acct or {}).get("simulated")), **(book or {})})
    if book is None:
        out.update({"not_accrued_wst": None, "accrued_beyond_book_wst": None})
        parts = [f"There is no ledger for {vid}, so what its owner account accrued ({accrued:,.2f} WST) has no book "
                 f"of record to be checked against."]
    else:
        b = book["book_of_record_wst"]
        gap = round(b - accrued - pend, 2)
        out["not_accrued_wst"] = gap if gap >= 0.005 else 0.0
        out["accrued_beyond_book_wst"] = round(-gap, 2) if gap <= -0.005 else 0.0
        parts = [f"The book of record distributed {b:,.2f} WST to the owner (the double-entry owner postings); the "
                 f"pot, a derived view, says {book['pot_wst']:,.2f}"
                 + (f", {book['pot_before_double_entry_wst']:,.2f} of it from before double entry began "
                    f"({book['double_entry_began']})." if book["double_entry_began"] else
                    ", and these books hold no double-entry posting at all."),
                 (f"The owner account accrued {accrued:,.2f} and paid out {paid:,.2f}" if acct is not None else
                  "There is no owner account for it")
                 + (f"; {pend:,.2f} waits as a claim from accruals that failed." if pend else ".")]
        if gap >= 0.005:
            parts.append(f"{gap:,.2f} WST distributed on the book of record was neither accrued nor held as a "
                         f"claim: a cycle whose accrual failed before W505, when a failure left no claim (before W465 "
                         f"it was not even said), or a cycle run before owner accruals were recorded. The stores "
                         f"cannot tell these apart.")
        elif gap <= -0.005:
            parts.append(f"The account holds {-gap:,.2f} WST more than the book of record distributed: accruals "
                         f"from cycles run before double entry began, whose share the book of record never held.")
        else:
            parts.append("The account and the book of record agree.")
    if (acct or {}).get("simulated"):
        parts.append("This is a simulation's account: its share is shown and never paid (the Owner's ruling of "
                     "2026-10-13).")
    parts.append("Read only: nothing was accrued or posted to close a difference.")
    out["basis"] = " ".join(parts)
    return out


def owner_share(vsb_id: str) -> Dict[str, Any]:
    """W880 (FU-1009) - one id's owner share: the book of record, the pot, the owner account and the claims from
    failed accruals, with the difference said and its causes named. Read only."""
    from agentic_core.economy import ledger as _led
    from agentic_core.economy import owner_payments as _op
    vid = str(vsb_id or "")
    book, book_problem = None, None
    if not vid or any(c in vid for c in "/\\") or vid in (".", ".."):
        book_problem = f"{vid!r} is not an id a ledger can be filed under"
    else:
        path = _led._STORE / f"{vid}_ledger.json"
        if path.exists():
            try:
                book = owner_book(_led.read_strict(path, vid))
            except Exception as exc:              # noqa: BLE001 - not known, never zero
                book, book_problem = None, _problem("the ledger", exc)
    try:
        acct, acct_problem = _op._read().get(vid), None
    except Exception as exc:                      # noqa: BLE001 - not known, never zero
        acct, acct_problem = None, _problem("the owner accounts", exc)
    pend = _op.pending_missed(vid)
    return _share_row(vid, book, book_problem, acct, acct_problem, pend.get("total_wst"), pend.get("unreadable"))


def _owner_shares(read: Dict[str, Any]) -> Dict[str, Any]:
    """Every id with a ledger or an owner account, compared; the largest differences first."""
    from agentic_core.economy import owner_payments as _op
    books = read["ledgers"].get("owner") or {}
    accounts = read["owner_accounts"].get("accounts")
    if read["ledgers"]["ids"] is None or accounts is None:
        return {"known": False, "rows": [], "owner_share_is": OWNER_SHARE_RECORD,
                "basis": "the ledgers or the owner accounts could not be read whole, so no owner share is compared"}
    pend = _op.pending_missed()
    by: Dict[str, float] = {}
    for r in pend.get("rows") or []:
        if isinstance(r, dict):
            by[str(r.get("vsb_id"))] = round(by.get(str(r.get("vsb_id")), 0.0) + float(r.get("amount_wst") or 0.0), 2)
    skip = set(read["ledgers"].get("unreadable") or [])
    rows = [_share_row(v, books.get(v), None, accounts.get(v), None, by.get(v, 0.0), pend.get("unreadable"))
            for v in sorted((set(books) | set(accounts)) - skip)]
    known = [r for r in rows if r.get("known")]
    short = [r for r in known if (r.get("not_accrued_wst") or 0) > 0]
    beyond = [r for r in known if (r.get("accrued_beyond_book_wst") or 0) > 0]
    rows.sort(key=lambda r: -max(r.get("not_accrued_wst") or 0, r.get("accrued_beyond_book_wst") or 0))
    not_accrued = round(sum(r["not_accrued_wst"] for r in short), 2)
    beyond_wst = round(sum(r["accrued_beyond_book_wst"] for r in beyond), 2)
    return {"known": True, "compared": len(known), "not_known": len(rows) - len(known),
            "rows": rows[:LIST_CAP], "rows_listed": min(len(rows), LIST_CAP),
            "not_accrued_wst": not_accrued, "ids_not_accrued": len(short),
            "accrued_beyond_book_wst": beyond_wst, "ids_accrued_beyond_book": len(beyond),
            "owner_share_is": OWNER_SHARE_RECORD,
            "basis": (f"{len(known)} id(s) with a ledger or an owner account compared. On {len(short)} the book of "
                      f"record distributed {not_accrued:,.2f} WST to the owner that was neither accrued nor held as a "
                      f"claim; on {len(beyond)} the account holds {beyond_wst:,.2f} WST more than the book of record "
                      f"distributed (accruals from before double entry began). " + OWNER_SHARE_RECORD
                      + (f" {len(skip)} unreadable ledger(s) are not compared." if skip else ""))}


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
            "owner_shares": _owner_shares(read),          # W880 (FU-1009)
            "fund": "read on its own route: GET /api/v1/fund/status, set_aside_reconciliation (W876)",
            "writes": "none"}
