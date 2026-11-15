"""P5.18 clauses 1 and 2 (W1080, FU-1075) - THE ENTERPRISE'S OWN AGREEMENTS, AS RECORDS THAT SAY ONLY WHAT IS TRUE OF
THEM. NOTHING HERE IS LEGAL ADVICE, and this platform is not a solicitor.

Measured first (W711): the only contract object in the tree was a service contract between two entities of this
platform in virtual units (agentic_core/api/economy.py). No record existed of an agreement with an outside party, of a
party's authority or of an execution.

CLAUSE 1 - PARTIES AS THEY ARE IN LAW. A party is a real person or a registered body, entered by a person with where
and when it was read; this platform checks it against no register. An agreement names its parties only by party
record, so an entity of this platform is never offered as one: an id that names an entity is refused as a party, and
nothing here reads an entity's form. A signatory's authority is recorded as stated and by whom, and the record says
the platform did not verify it.

CLAUSE 2 - AN AGREEMENT RECORD WHOSE STATES ARE KEPT APART. Drafted, reviewed, approved, executed, in force and ended
are six facts, each with who and when, and no answer folds them into one status. An approval is of one exact version,
named by its hash, and a change to the text ends it. "Executed" is a person's entry of the evidence and of which
formalities were met, never a provider's status: a request that carries anything else is refused. An internal service
contract in virtual units is listed apart, never as an agreement.

WHAT THE LAW REQUIRES IS NOT STATED HERE. The rules on execution have not been read at their publisher, so which
formalities an agreement needs is the person's statement, never the platform's.

KEPT ONLY FOR A SIGNED-IN PERSON. A party is a record about a real person or body, and the Owner's ruling of 2026-10-12
builds after sign-in anything that keeps something about a person. With sign-in off every write is refused with that
reason, and nothing is read back. A record is its maker's: another person is answered as though it did not exist, and
an administrator reaches every record.
"""
import hashlib
import re
import time
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from agentic_core.auth.core import auth_enabled, get_current_user

router = APIRouter(prefix="/api/v1/agreements", tags=["agreements"])

PARTIES, AGREEMENTS = "agreement_parties.json", "agreements.json"
STATES = ("drafted", "reviewed", "approved", "executed", "in_force", "ended")
PARTY_KINDS = ("person", "registered_body")

NOT_LEGAL_ADVICE = "Nothing here is legal advice, and this platform is not a solicitor."
NOT_KEPT = ("Nothing is kept here before sign-in: an agreement record holds its parties, real persons and registered "
            "bodies, and the Owner's ruling of 2026-10-12 builds after sign-in anything that keeps something about a "
            "person. Sign-in is the Owner's switch.")
NO_PERSON = "No signed-in person is on this call, so nothing was kept."
NOT_CHECKED = "This platform did not check it against any register or document."
AUTHORITY_NOT_VERIFIED = "This platform did not verify this authority; it is recorded as stated, by the person named."
LAW_NOT_READ = ("Which formalities the law requires is not stated here: the rules on execution have not been read at "
                "their publisher, so the formalities are the ones the person entered.")
NOT_AN_ENTITY = ("{id} is an entity of this platform. An entity here is a record on this platform, not a person in "
                 "law: it has no incorporation, its form is a template for a profit split, and it is never a party to "
                 "an agreement with an outside party. Enter the party as the person or registered body it is.")
SERVICE_CONTRACTS_ARE = ("Service contracts between two entities of this platform, priced in virtual units (WST): records "
                         "of this platform's own economy, not agreements with an outside party, and never listed as "
                         "one. Neither side of one is a person in law.")

LIMITS = {"name": 200, "read_from": 300, "registered_on": 200, "registered_number": 60, "title": 200, "text": 200_000,
          "role": 80, "note": 1000, "evidence": 1000, "formality": 200, "basis": 500, "how": 500,
          "capacity": 120, "authority_as_stated": 500, "stated_by": 200}

#  W1085 (P5.18 clauses 3 and 7) - OBLIGATIONS AND DATES FROM THE TEXT, AND A PERSON'S DOCUMENT AS DATA
NOTICE_UNKNOWN = "The notice period is not known: none has been entered from the text."
UNCONFIRMED = "Not confirmed by a person yet."
NO_DATE = "No date is entered for it."
DATE_BASIS = ("A date here is a person's entry from the text: none is computed by this platform, and none is taken from "
              "a model.")
TEXT_KEPT = ("The text is kept whole, as data, on this machine: no instruction in it is followed, and nothing of it is "
             "sent to an outside service.")
LIMITS.update({"what_owed": 500, "clause": 80, "notice": 200})


# ── the store ─────────────────────────────────────────────────────────────────────────────────────────────────

def _path(name: str):
    from agentic_core.config import data_path
    return data_path(name)


def _read(name: str) -> list:
    """A missing store is empty; a store that exists and cannot be read whole is refused, never answered as empty."""
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        rows = read_json_strict(_path(name), [], expect=list)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e)) from None
    if not all(isinstance(r, dict) and r.get("id") for r in rows):
        raise HTTPException(status_code=503, detail=f"{name} is not a list of records, so nothing was done.")
    return rows


def _mutate(name: str, change):
    """Read, change and write under the store's lock. `change(rows)` raises HTTPException to refuse, and then nothing
    is written."""
    from agentic_core.config import atomic_write_json, store_lock
    p = _path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    lock = store_lock(p, timeout=5.0)
    try:
        lock.__enter__()
    except TimeoutError:
        raise HTTPException(status_code=503, detail=(
            "The agreement store is busy: another change is being written, so nothing was done. Retry.")) from None
    try:
        rows = _read(name)
        out = change(rows)
        atomic_write_json(p, rows)
        return out
    finally:
        lock.__exit__(None, None, None)


# ── who is calling ────────────────────────────────────────────────────────────────────────────────────────────

def _person(user) -> str:
    """The signed-in person a write is kept for. With sign-in off, or on a call that holds no person, nothing is."""
    if not auth_enabled():
        raise HTTPException(status_code=403, detail=NOT_KEPT)
    if not isinstance(user, dict) or not user.get("username"):
        raise HTTPException(status_code=403, detail=NO_PERSON)
    return str(user["username"])


def _reaches(user, row: dict) -> bool:
    """Whether this caller may read or add to a record: its maker, or an administrator. Nobody with sign-in off."""
    if not auth_enabled() or not isinstance(user, dict) or not user.get("username"):
        return False
    return user.get("role") == "admin" or row.get("owner") == user.get("username")


# ── what a request says ───────────────────────────────────────────────────────────────────────────────────────

class _Asked(BaseModel):
    """A request whose every field is read: a field this route does not take is refused by name, never ignored."""
    model_config = ConfigDict(extra="allow")


def _only(req: _Asked, takes: str) -> None:
    extra = sorted((req.model_extra or {}).keys())
    if extra:
        raise HTTPException(status_code=400, detail=(
            f"{takes} {', '.join(repr(k) for k in extra)} {'is' if len(extra) == 1 else 'are'} not part of it, so "
            f"nothing was kept."))


def _text(value, what: str, key: str, *, required: bool = True) -> Optional[str]:
    s = str(value if value is not None else "").strip()
    if not s:
        if required:
            raise HTTPException(status_code=400, detail=f"{what} is needed, and none was given, so nothing was kept.")
        return None
    if len(s) > LIMITS[key]:
        raise HTTPException(status_code=400, detail=(
            f"{what} is {len(s)} characters, more than the {LIMITS[key]} this record holds, so nothing was kept."))
    return s


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _date(value, what: str) -> str:
    """A date a person entered: written YYYY-MM-DD, and not after today (a day's grace for the time zones ahead)."""
    s = str(value or "").strip()
    d = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            d = date.fromisoformat(s)
        except ValueError:
            d = None
    if d is None:
        raise HTTPException(status_code=400, detail=(
            f"{what} must be a date written YYYY-MM-DD; '{s or 'nothing'}' is not one, so nothing was kept."))
    if d > _today() + timedelta(days=1):
        raise HTTPException(status_code=400, detail=(
            f"{what} is {s}, after today; a date that has not come is not recorded as one that has, so nothing was "
            f"kept."))
    return s


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── clause 1: parties ─────────────────────────────────────────────────────────────────────────────────────────

class PartyRequest(_Asked):
    kind: str = ""
    name: str = ""
    registered_on: Optional[str] = None
    registered_number: Optional[str] = None
    read_from: str = ""
    read_on: str = ""


def _entity_named(value: Optional[str], user) -> bool:
    """Whether a value a person gave is the id of an entity of this platform that they may reach (another person's
    entity is answered as any unknown id is, so nothing here says it exists)."""
    v = str(value or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,120}", v):      # an id is one word: a name is never read as a path
        return False
    try:
        from agentic_core.api.vsb import entity_for_caller
        return isinstance(entity_for_caller(v, user), dict)
    except HTTPException:
        raise
    except Exception:
        return False


def _public_party(p: dict) -> dict:
    out = {k: p.get(k) for k in ("id", "kind", "name", "registered_on", "registered_number", "read_from", "read_on",
                                 "entered_by", "entered_at")}
    out["checked_by_this_platform"] = False
    out["basis"] = (f"As entered by {p.get('entered_by')}, read from {p.get('read_from')} on {p.get('read_on')}. "
                    f"{NOT_CHECKED}")
    return out


@router.post("/parties")
async def enter_party(req: PartyRequest, user: dict | None = Depends(get_current_user)):
    """Clause 1: a party is a real person or a registered body, entered with where and when it was read."""
    who = _person(user)
    _only(req, "A party is entered by its kind, its name, the register a registered body is on and its number there, "
               "where it was read and when;")
    kind = str(req.kind or "").strip()
    if kind not in PARTY_KINDS:
        raise HTTPException(status_code=400, detail=(
            f"A party is a real person ('person') or a registered body ('registered_body'); "
            f"'{kind or 'nothing'}' is neither, so nothing was kept."))
    name = _text(req.name, "The party's name", "name")
    on = _text(req.registered_on, "The register this body is on", "registered_on", required=kind == "registered_body")
    num = _text(req.registered_number, "Its number on that register", "registered_number",
                required=kind == "registered_body")
    if kind == "person" and (on or num):
        raise HTTPException(status_code=400, detail=(
            "A person is entered by name with where and when it was read; a register and number are a registered "
            "body's, so nothing was kept."))
    for value in (name, num):
        if _entity_named(value, user):
            raise HTTPException(status_code=400, detail=NOT_AN_ENTITY.format(id=f"'{value}'"))
    where = _text(req.read_from, "Where the party's details were read", "read_from")
    when = _date(req.read_on, "The date they were read")
    party = {"id": f"pty-{uuid.uuid4().hex[:10]}", "owner": who, "kind": kind, "name": name, "registered_on": on,
             "registered_number": num, "read_from": where, "read_on": when, "entered_by": who, "entered_at": _now()}
    _mutate(PARTIES, lambda rows: rows.append(party))
    return {"party": _public_party(party), "not_legal_advice": NOT_LEGAL_ADVICE}


@router.get("/parties")
async def list_parties(user: dict | None = Depends(get_current_user)):
    """The parties this person entered (an administrator: every party)."""
    if not auth_enabled():
        return {"parties": [], "kept": False, "not_kept_because": NOT_KEPT, "not_legal_advice": NOT_LEGAL_ADVICE}
    rows = [_public_party(p) for p in _read(PARTIES) if _reaches(user, p)]
    return {"parties": rows[::-1], "kept": True, "total": len(rows), "not_legal_advice": NOT_LEGAL_ADVICE}


# ── clause 2: agreement records ───────────────────────────────────────────────────────────────────────────────

class AgreementRequest(_Asked):
    title: str = ""
    text: str = ""
    parties: List[Any] = []


class TextChange(_Asked):
    text: str = ""
    from_hash: str = ""


class ReviewRequest(_Asked):
    hash: str = ""
    note: Optional[str] = None


class ApprovalRequest(_Asked):
    hash: str = ""


class ExecutionRequest(_Asked):
    hash: str = ""
    signed_on: str = ""
    evidence: str = ""
    formalities_met: List[Any] = []


class InForceRequest(_Asked):
    from_date: str = ""
    basis: str = ""


class EndedRequest(_Asked):
    on: str = ""
    how: str = ""


class ObligationRequest(_Asked):
    owed_by: str = ""
    owed_to: str = ""
    what: str = ""
    clause: str = ""
    due_on: Optional[str] = None


class NoticeRequest(_Asked):
    as_stated: str = ""
    clause: str = ""


class ConfirmRequest(_Asked):
    pass


def _any_date(value, what: str) -> str:
    """A date a person entered from the text: written YYYY-MM-DD, past or to come (a date falls due later)."""
    s = str(value or "").strip()
    d = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            d = date.fromisoformat(s)
        except ValueError:
            d = None
    if d is None:
        raise HTTPException(status_code=400, detail=(
            f"{what} must be a date written YYYY-MM-DD; '{s or 'nothing'}' is not one, so nothing was kept."))
    return s


def _obligations(a: dict) -> List[dict]:
    out = []
    for o in a.get("obligations") or []:
        out.append({**o,
                    **({} if o.get("confirmed") else {"confirmed_said": UNCONFIRMED}),
                    **({} if o.get("due_on") else {"due_said": NO_DATE})})
    return out


def _notice(a: dict) -> dict:
    n = a.get("notice")
    return {**n, "known": True} if n else {"known": False, "said": NOTICE_UNKNOWN}


def _text_kept(a: dict) -> dict:
    t = str(_current(a).get("text") or "")
    return {"chars": len(t), "of": len(t), "basis": TEXT_KEPT}


class SignatoryRequest(_Asked):
    party_id: str = ""
    name: str = ""
    capacity: str = ""
    authority_as_stated: str = ""
    stated_by: str = ""


def _mine(rows: list, aid: str, user) -> dict:
    a = next((r for r in rows if r.get("id") == aid), None)
    if a is None or not _reaches(user, a):
        raise HTTPException(status_code=404, detail=f"No agreement record {aid} was found.")
    return a


def _version_of(a: dict, h: str) -> Optional[dict]:
    return next((v for v in a.get("versions") or [] if v.get("hash") == h), None)


def _current(a: dict) -> dict:
    return (a.get("versions") or [{}])[-1]


def _facts(a: dict) -> List[dict]:
    """The six facts, apart, in their order. A fact not recorded says so; none is inferred from another."""
    cur = _current(a)
    d = a.get("drafted") or {}
    reviews = [{**r, "of_current_text": r.get("hash") == cur.get("hash")} for r in a.get("reviews") or []]
    ap, ex, inf, end = a.get("approval"), a.get("executed"), a.get("in_force"), a.get("ended")
    return [
        {"state": "drafted", "recorded": True, "by": d.get("by"), "at": d.get("at"), "version": d.get("version"),
         "hash": d.get("hash")},
        {"state": "reviewed", "recorded": bool(reviews), "reviews": reviews,
         **({} if reviews else {"said": "No review is recorded."})},
        {"state": "approved", "recorded": ap is not None, **(ap or {"said": "No approval of the current text is recorded."}),
         "ended_approvals": a.get("approvals_ended") or []},
        {"state": "executed", "recorded": ex is not None,
         **({**ex, "of_current_text": ex.get("hash") == cur.get("hash"), "formalities_the_law_requires": None,
             "law_basis": LAW_NOT_READ} if ex else {"said": "No execution is recorded."})},
        {"state": "in_force", "recorded": inf is not None, **(inf or {"said": "That it is in force is not recorded."})},
        {"state": "ended", "recorded": end is not None, **(end or {"said": "No end is recorded."})},
    ]


def _parties_of(a: dict, parties: Optional[list]) -> List[dict]:
    by_id = {p["id"]: p for p in parties or []}
    out = []
    for ap in a.get("parties") or []:
        p = by_id.get(ap.get("party_id"))
        out.append({"party_id": ap.get("party_id"), "role": ap.get("role"),
                    "party": _public_party(p) if p else None,
                    **({} if p else {"said": "This party's record is not in the party store."}),
                    "signatories": [{**s, "verified_by_this_platform": False, "basis": AUTHORITY_NOT_VERIFIED}
                                    for s in ap.get("signatories") or []]})
    return out


def _summary(a: dict, parties: Optional[list]) -> dict:
    cur = _current(a)
    return {"id": a.get("id"), "title": a.get("title"), "version": cur.get("version"), "hash": cur.get("hash"),
            "parties": [{"role": p["role"], "name": (p["party"] or {}).get("name")} for p in _parties_of(a, parties)],
            "facts": [{k: f.get(k) for k in ("state", "recorded", "by", "at", "entered_by", "entered_at")
                       if f.get(k) is not None} for f in _facts(a)]}


def _whole(a: dict, parties: Optional[list]) -> dict:
    return {"id": a.get("id"), "title": a.get("title"), "owner": a.get("owner"),
            "parties": _parties_of(a, parties),
            "versions": [{k: v.get(k) for k in ("version", "hash", "by", "at", "text")} for v in a.get("versions") or []],
            "current": {k: _current(a).get(k) for k in ("version", "hash")},
            "obligations": _obligations(a), "notice": _notice(a), "text_kept": _text_kept(a), "date_basis": DATE_BASIS,
            "facts": _facts(a), "not_legal_advice": NOT_LEGAL_ADVICE}


def _service_contracts(user) -> dict:
    """The internal service contracts this caller may see, listed apart from the agreements, never as one."""
    out = {"what_these_are": SERVICE_CONTRACTS_ARE, "route": "/api/v1/economy/contracts"}
    try:
        from agentic_core.api.economy import _load_contracts, _public_contract, _require_economy_access

        def _can(vid) -> bool:
            try:
                _require_economy_access(vid, user)
                return True
            except HTTPException:
                return False
        rows = [_public_contract(c) for c in _load_contracts() if _can(c.get("client_vsb")) or _can(c.get("provider_vsb"))]
        out.update(contracts=rows[::-1], total=len(rows), unread=None)
    except HTTPException as e:
        out.update(contracts=None, total=None, unread=f"The service-contract store could not be read: {e.detail}")
    return out


@router.post("")
async def draft_agreement(req: AgreementRequest, user: dict | None = Depends(get_current_user)):
    """Clause 2: an agreement record, drafted: its text as version 1 with its hash, and its parties by party record."""
    who = _person(user)
    _only(req, "An agreement is drafted with its title, its text and its parties;")
    title = _text(req.title, "The agreement's title", "title")
    text = _text(req.text, "The agreement's text", "text")
    if not isinstance(req.parties, list) or len(req.parties) < 2:
        raise HTTPException(status_code=400, detail=(
            "An agreement names at least two parties, each a party record with its role, so nothing was kept."))
    mine = {p["id"]: p for p in _read(PARTIES) if _reaches(user, p)}
    named = []
    for item in req.parties:
        if not isinstance(item, dict) or set(item) - {"party_id", "role"}:
            raise HTTPException(status_code=400, detail=(
                "Each party of an agreement is named by its party record ('party_id') and its role ('role') only, "
                "so nothing was kept."))
        pid = str(item.get("party_id") or "").strip()
        role = _text(item.get("role"), "Each party's role", "role")
        if pid not in mine:
            if _entity_named(pid, user):
                raise HTTPException(status_code=400, detail=NOT_AN_ENTITY.format(id=f"'{pid}'"))
            raise HTTPException(status_code=400, detail=(
                f"'{pid or 'nothing'}' is not a party record of yours. A party is entered first, as the person or "
                f"registered body it is (POST /api/v1/agreements/parties), so nothing was kept."))
        if pid in {n["party_id"] for n in named}:
            raise HTTPException(status_code=400, detail=(
                f"{mine[pid]['name']} ({pid}) is named twice as a party, so nothing was kept."))
        named.append({"party_id": pid, "role": role, "signatories": []})
    at, h = _now(), _hash(text)
    a = {"id": f"agr-{uuid.uuid4().hex[:10]}", "owner": who, "title": title, "parties": named,
         "versions": [{"version": 1, "hash": h, "text": text, "by": who, "at": at}],
         "drafted": {"by": who, "at": at, "version": 1, "hash": h},
         "reviews": [], "approval": None, "approvals_ended": [], "executed": None, "in_force": None, "ended": None}
    _mutate(AGREEMENTS, lambda rows: rows.append(a))
    return _whole(a, list(mine.values()))


@router.get("")
async def list_agreements(user: dict | None = Depends(get_current_user)):
    """This person's agreement records (an administrator: every one), each with its six facts apart; the internal
    service contracts in virtual units listed apart, never as agreements."""
    contracts = _service_contracts(user)
    if not auth_enabled():
        return {"agreements": [], "kept": False, "not_kept_because": NOT_KEPT,
                "internal_service_contracts": contracts, "not_legal_advice": NOT_LEGAL_ADVICE}
    parties = _read(PARTIES)
    rows = [_summary(a, parties) for a in _read(AGREEMENTS) if _reaches(user, a)]
    return {"agreements": rows[::-1], "kept": True, "total": len(rows), "internal_service_contracts": contracts,
            "not_legal_advice": NOT_LEGAL_ADVICE}


@router.get("/{aid}")
async def read_agreement(aid: str, user: dict | None = Depends(get_current_user)):
    if not auth_enabled():
        raise HTTPException(status_code=404, detail=f"No agreement record {aid} was found. {NOT_KEPT}")
    return _whole(_mine(_read(AGREEMENTS), aid, user), _read(PARTIES))


def _fact(aid: str, user, record) -> dict:
    """Record one fact on an agreement this person reaches, under the store's lock; `record(a, who)` refuses or
    changes the record."""
    who = _person(user)

    def _change(rows):
        a = _mine(rows, aid, user)
        record(a, who)
        return a
    a = _mutate(AGREEMENTS, _change)
    return _whole(a, _read(PARTIES))


def _not_after_end(a: dict, what: str) -> None:
    end = a.get("ended")
    if end:
        raise HTTPException(status_code=409, detail=(
            f"This agreement's end is recorded (on {end.get('on')}, entered by {end.get('entered_by')}), so {what} "
            f"was not recorded."))


@router.put("/{aid}/text")
async def change_text(aid: str, req: TextChange, user: dict | None = Depends(get_current_user)):
    """A new version of the text. The approval of the version it replaces is ended, with why; an executed record's
    text is never changed (a variation is a record of its own)."""
    _person(user)
    _only(req, "A change to the text gives the new text and the hash of the version it changes;")
    text = _text(req.text, "The new text", "text")

    def _record(a, who):
        _not_after_end(a, "a change to its text")
        ex = a.get("executed")
        if ex:
            raise HTTPException(status_code=409, detail=(
                f"This agreement's execution is recorded (version {ex.get('version')}, entered by "
                f"{ex.get('entered_by')}). The text of an executed agreement is not changed here: a variation is an "
                f"agreement record of its own. Nothing was changed."))
        cur = _current(a)
        if str(req.from_hash or "").strip() != cur.get("hash"):
            raise HTTPException(status_code=409, detail=(
                f"The text is now version {cur.get('version')} ({cur.get('hash')}), not the version this change was "
                f"made from, so nothing was changed. Read it again and change that."))
        h = _hash(text)
        if h == cur.get("hash"):
            raise HTTPException(status_code=400, detail=(
                f"The text given is version {cur.get('version')} as it stands, so nothing was changed."))
        n, at = int(cur.get("version") or 0) + 1, _now()
        a["versions"].append({"version": n, "hash": h, "text": text, "by": who, "at": at})
        ap = a.get("approval")
        if ap:
            a.setdefault("approvals_ended", []).append({
                **ap, "ended_at": at, "ended_by": who,
                "ended_because": f"the text changed: version {n} ({h}) replaced the approved version {ap.get('version')}"})
            a["approval"] = None
    return _fact(aid, user, _record)


@router.post("/{aid}/review")
async def review(aid: str, req: ReviewRequest, user: dict | None = Depends(get_current_user)):
    """A person's review of the text as it stands, named by its hash."""
    _person(user)
    _only(req, "A review names the hash of the text reviewed, with a note if there is one;")
    note = _text(req.note, "The review's note", "note", required=False)

    def _record(a, who):
        _not_after_end(a, "a review")
        cur = _current(a)
        if str(req.hash or "").strip() != cur.get("hash"):
            raise HTTPException(status_code=409, detail=(
                f"The text is now version {cur.get('version')} ({cur.get('hash')}), not the version named, so no "
                f"review was recorded. A review is of the text as it stands."))
        a.setdefault("reviews", []).append({"by": who, "at": _now(), "version": cur.get("version"),
                                            "hash": cur.get("hash"), "note": note})
    return _fact(aid, user, _record)


@router.post("/{aid}/approve")
async def approve(aid: str, req: ApprovalRequest, user: dict | None = Depends(get_current_user)):
    """An approval of one exact version, named by its hash. A change to the text ends it."""
    _person(user)
    _only(req, "An approval names the hash of the one version approved;")

    def _record(a, who):
        _not_after_end(a, "an approval")
        cur = _current(a)
        if str(req.hash or "").strip() != cur.get("hash"):
            raise HTTPException(status_code=409, detail=(
                f"The text is now version {cur.get('version')} ({cur.get('hash')}), not the version named, so "
                f"nothing was approved. An approval is of one exact version, named by its hash."))
        ap = a.get("approval")
        if ap:
            raise HTTPException(status_code=409, detail=(
                f"Version {ap.get('version')} is already approved, by {ap.get('by')} at {ap.get('at')}, so nothing "
                f"was changed."))
        a["approval"] = {"by": who, "at": _now(), "version": cur.get("version"), "hash": cur.get("hash")}
    return _fact(aid, user, _record)


@router.post("/{aid}/executed")
async def executed(aid: str, req: ExecutionRequest, user: dict | None = Depends(get_current_user)):
    """A person's entry that the agreement was executed: the version signed, when, the evidence of it and which
    formalities were met, as they state them. Never a provider's status."""
    _person(user)
    _only(req, ("An execution is a person's entry of the version signed, the date, the evidence and which formalities "
                "were met, never a provider's status;"))
    when = _date(req.signed_on, "The date it was signed")
    evidence = _text(req.evidence, "The evidence that it was executed", "evidence")
    met = req.formalities_met if isinstance(req.formalities_met, list) else []
    met = [_text(f, "Each formality met", "formality") for f in met]
    if not met or len(met) > 20:
        raise HTTPException(status_code=400, detail=(
            "An execution says which formalities were met, as the person states them (one to twenty), so nothing "
            f"was recorded. {LAW_NOT_READ}"))

    def _record(a, who):
        _not_after_end(a, "an execution")
        ex = a.get("executed")
        if ex:
            raise HTTPException(status_code=409, detail=(
                f"Its execution is already recorded, entered by {ex.get('entered_by')} at {ex.get('entered_at')}, so "
                f"nothing was changed."))
        v = _version_of(a, str(req.hash or "").strip())
        if v is None:
            raise HTTPException(status_code=400, detail=(
                "No version of this agreement has the hash named, so no execution was recorded. Name the version "
                "that was signed."))
        a["executed"] = {"entered_by": who, "entered_at": _now(), "version": v.get("version"), "hash": v.get("hash"),
                         "signed_on": when, "evidence": evidence, "formalities_met": met}
    return _fact(aid, user, _record)


@router.post("/{aid}/in-force")
async def in_force(aid: str, req: InForceRequest, user: dict | None = Depends(get_current_user)):
    """A person's entry that the agreement is in force, from a date, and on what basis, as they state it."""
    _person(user)
    _only(req, "That it is in force is entered with the date it is in force from and on what basis;")
    when = _date(req.from_date, "The date it is in force from")
    basis = _text(req.basis, "What puts it in force", "basis")

    def _record(a, who):
        _not_after_end(a, "that it is in force")
        inf = a.get("in_force")
        if inf:
            raise HTTPException(status_code=409, detail=(
                f"That it is in force is already recorded, from {inf.get('from')}, entered by {inf.get('entered_by')}, "
                f"so nothing was changed."))
        a["in_force"] = {"entered_by": who, "entered_at": _now(), "from": when, "basis": basis}
    return _fact(aid, user, _record)


@router.post("/{aid}/ended")
async def ended(aid: str, req: EndedRequest, user: dict | None = Depends(get_current_user)):
    """A person's entry that the agreement ended, on a date, and how, as they state it."""
    _person(user)
    _only(req, "An end is entered with the date it ended and how;")
    when = _date(req.on, "The date it ended")
    how = _text(req.how, "How it ended", "how")

    def _record(a, who):
        _not_after_end(a, "another end")
        for fact, key, said in (("executed", "signed_on", "it was signed"), ("in_force", "from", "it is in force from")):
            earlier = (a.get(fact) or {}).get(key)
            if earlier and when < earlier:
                raise HTTPException(status_code=400, detail=(
                    f"The end entered ({when}) is before the date {said} ({earlier}), as recorded, so no end was "
                    f"recorded."))
        a["ended"] = {"entered_by": who, "entered_at": _now(), "on": when, "how": how}
    return _fact(aid, user, _record)


@router.post("/{aid}/signatories")
async def add_signatory(aid: str, req: SignatoryRequest, user: dict | None = Depends(get_current_user)):
    """Clause 1: a signatory for one of the agreement's parties, with their authority as stated and by whom. The
    platform does not verify it, and the record says so."""
    _person(user)
    _only(req, "A signatory is entered with the party they sign for, their name, their capacity, their authority as "
               "stated and who stated it;")
    name = _text(req.name, "The signatory's name", "name")
    capacity = _text(req.capacity, "The capacity they sign in", "capacity")
    authority = _text(req.authority_as_stated, "Their authority, as stated", "authority_as_stated")
    stated_by = _text(req.stated_by, "Who stated that authority", "stated_by")

    def _record(a, who):
        _not_after_end(a, "a signatory")
        pid = str(req.party_id or "").strip()
        slot = next((p for p in a.get("parties") or [] if p.get("party_id") == pid), None)
        if slot is None:
            raise HTTPException(status_code=400, detail=(
                f"'{pid or 'nothing'}' is not a party to this agreement, so no signatory was recorded."))
        slot.setdefault("signatories", []).append({
            "name": name, "capacity": capacity, "authority_as_stated": authority, "stated_by": stated_by,
            "recorded_by": who, "recorded_at": _now()})
    return _fact(aid, user, _record)


@router.post("/{aid}/obligations")
async def add_obligation(aid: str, req: ObligationRequest, user: dict | None = Depends(get_current_user)):
    """Clause 3: an obligation as read from the text - who owes what to whom, under which clause, and when it falls due
    if a person entered a date. It names the clause it was read from, and waits for a person to confirm it."""
    _person(user)
    _only(req, "An obligation is entered with who owes it, to whom, what is owed, the clause it was read from and, if the "
               "text gives one, the date it falls due;")
    what = _text(req.what, "What is owed", "what_owed")
    clause = _text(req.clause, "The clause it was read from", "clause")
    due = _any_date(req.due_on, "The date it falls due") if str(req.due_on or "").strip() else None

    def _record(a, who):
        _not_after_end(a, "an obligation")
        ids = {p.get("party_id") for p in a.get("parties") or []}
        for role, pid in (("owes", req.owed_by), ("is owed", req.owed_to)):
            if str(pid or "").strip() not in ids:
                raise HTTPException(status_code=400, detail=(
                    f"Who {role} it is one of this agreement's parties; '{str(pid or '').strip() or 'nothing'}' is not "
                    f"one, so nothing was kept."))
        if str(req.owed_by).strip() == str(req.owed_to).strip():
            raise HTTPException(status_code=400, detail="A party does not owe an obligation to itself, so nothing was kept.")
        at = _now()
        a.setdefault("obligations", []).append({
            "id": f"obl-{uuid.uuid4().hex[:10]}", "owed_by": str(req.owed_by).strip(), "owed_to": str(req.owed_to).strip(),
            "what": what, "clause": clause, "due_on": due, "entered_by": who, "entered_at": at,
            **({"due_basis": f"entered by {who} at {at} from the text"} if due else {}), "confirmed": None})
    return _fact(aid, user, _record)


@router.post("/{aid}/obligations/{oid}/confirm")
async def confirm_obligation(aid: str, oid: str, req: ConfirmRequest, user: dict | None = Depends(get_current_user)):
    """Clause 3: a person confirms an obligation was read from its clause; the record names who and when."""
    _person(user)
    _only(req, "A confirmation carries nothing but itself;")

    def _record(a, who):
        _not_after_end(a, "a confirmation")
        o = next((x for x in a.get("obligations") or [] if x.get("id") == oid), None)
        if o is None:
            raise HTTPException(status_code=404, detail=f"No obligation {oid} is on this agreement.")
        if o.get("confirmed"):
            raise HTTPException(status_code=409, detail=(
                f"It is already confirmed, by {o['confirmed']['by']} at {o['confirmed']['at']}, so nothing was changed."))
        o["confirmed"] = {"by": who, "at": _now()}
    return _fact(aid, user, _record)


@router.post("/{aid}/notice")
async def enter_notice(aid: str, req: NoticeRequest, user: dict | None = Depends(get_current_user)):
    """Clause 3: the notice period as the text states it and the clause it was read from; an earlier entry is kept.
    With none entered, the record says the notice period is not known."""
    _person(user)
    _only(req, "The notice period is entered as the text states it, with the clause it was read from;")
    as_stated = _text(req.as_stated, "The notice period, as the text states it", "notice")
    clause = _text(req.clause, "The clause it was read from", "clause")

    def _record(a, who):
        _not_after_end(a, "a notice period")
        if a.get("notice"):
            a.setdefault("notice_history", []).append(a["notice"])
        a["notice"] = {"as_stated": as_stated, "clause": clause, "entered_by": who, "entered_at": _now()}
    return _fact(aid, user, _record)


def falling_due(user, within_days: int) -> dict:
    """W1085 - what on this person's agreement records waits on a person: an obligation falling due within the window
    or past its date, and an obligation no person has confirmed. Read by the one list of what waits on a person."""
    today = _today()
    items = []
    for a in _read(AGREEMENTS):
        if not _reaches(user, a) or a.get("ended"):
            continue
        for o in a.get("obligations") or []:
            base = {"agreement_id": a["id"], "agreement_title": a.get("title"), "obligation_id": o["id"],
                    "what": o.get("what"), "clause": o.get("clause"), "due_on": o.get("due_on"),
                    "confirmed": bool(o.get("confirmed"))}
            if o.get("due_on"):
                days = (date.fromisoformat(o["due_on"]) - today).days
                if days <= within_days:
                    items.append({**base, "kind": "falls_due", "days": days,
                                  "said": (f"falls due in {days} day{'s' if days != 1 else ''}" if days > 0 else
                                           "falls due today" if days == 0 else
                                           f"fell due {-days} day{'s' if days != -1 else ''} ago")})
            if not o.get("confirmed"):
                items.append({**base, "kind": "unconfirmed", "said": UNCONFIRMED})
    items.sort(key=lambda x: (x["kind"] != "falls_due", x.get("days") if x.get("days") is not None else 10 ** 6))
    return {"items": items, "within_days": within_days}
