"""AN ENTITY'S OWN SPECIALISTS - a short roster per entity, not a registry of people (P5.15 clause 6).

OWNER RULING 2026-10-12 (the review cell, clause 6): an entity may attach its own specialists to its third tier, a
short roster per entity and not a registry of people. Clause 5 says what the third tier is: a NAMED PERSON's record -
name, credential as stated, what was reviewed, the date and when it lapses - and the platform does not verify a
credential and says so.

THIS PART (W932) IS THE ROSTER, and it is the entity's own:

    GET  /api/v1/entity-specialists/{vsb_id}                          the roster: who is on it now, and who was
    POST /api/v1/entity-specialists/{vsb_id}                          attach a specialist
    POST /api/v1/entity-specialists/{vsb_id}/{specialist_id}/retire   retire one, with the reason

- A specialist is a name, the discipline (clause 7's four, in its order), the credential as the person states it,
  what they review for this entity, and the date their place lapses. Nothing else is kept: no contact detail can
  ride in, so the roster cannot become a registry of people.
- Five at a time. The ruling says "a short roster"; five is Workstation's number and the answer says so.
- A lapsed place is said lapsed on every read and does not count against the five. A specialist leaves by a recorded
  retirement with its reason, who and when; nothing is deleted.
- Under sign-in only the entity's owner, or an administrator, reads or writes it; to anyone else the entity is not
  found. An entity the platform does not hold has no roster.
- The platform verifies no credential, and every answer says so.

W933 (part 2) - THE RECOMMENDATION, read from the entity's own record. P5.15's release clause: for a generated
entity, engaging a specialist is a chargeable option the platform recommends. An entity is generated when its record
names a door through which Workstation made it (established_through: the Genesis journey or the spawn route). Such
an entity is recommended a specialist; any other is told no recommendation is made, and why. Engaging one is
chargeable to the ENTITY: the specialist's fee is its own cost, declared among its costs for a cycle, so it comes off
before profit (P5.16 clause 6). Workstation sets no price for it and charges nothing for it. The roster is shown on
the entity's page (components/EntitySpecialists.tsx, on the Cockpit's deliverables tab).

W934 (part 3) - THE SIGNATURE, the third tier for the entity's work (clauses 5 and 6):

    POST /api/v1/entity-specialists/{vsb_id}/{specialist_id}/sign   sign one version of one of its deliverables
    GET  /api/v1/entity-specialists/{vsb_id}/signatures             each signature, whether it counts and why not,
                                                                    and the tier each deliverable has reached

- A signature is a named person's record: the specialist's name and credential as stated (from the roster), the
  deliverable and what in it they reviewed, the date reviewed (not after today), and when it lapses (after today,
  and not after their place lapses). Only a specialist holding a place signs.
- It is bound to the exact text it signed (sha256): once the deliverable is run again, the new version is
  unreviewed until it is signed. A lapsed signature does not count. Nothing is deleted.
- It is the person's statement, entered by the entity's owner or an administrator with who entered it. Workstation
  composes no part of it and charges nothing for it.
"""
from __future__ import annotations

import datetime as _dt
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.api._review_tier import NOT_VERIFIED
from agentic_core.auth.core import get_current_user, user_can_access

router = APIRouter(prefix="/api/v1/entity-specialists", tags=["review-cell"])

STORE = "entity_specialists.json"
LIMIT = 5                                                     # "a short roster": Workstation's number, said below
DISCIPLINES = ("care", "law", "education", "money_readiness")   # clause 7, in its order
BASIS = ("A short roster per entity, not a registry of people (P5.15 clause 6): a name, the discipline, the "
         "credential as the person states it, what they review for this entity, and when their place lapses. No "
         "contact detail is kept. Five at a time is Workstation's own number; the ruling says a short roster. A "
         "lapsed place does not count against the five. A specialist leaves by a recorded retirement and is never "
         "deleted. A specialist holding a place signs one version of this entity's work, and that signature is its "
         "third tier (the signatures are read at .../signatures).")

#  W933 - the doors through which Workstation generates an entity; each writes established_through on the record
GENERATING_DOORS = {"genesis_journey": "the Genesis journey", "spawn_route": "the spawn route"}
CHARGE = ("Engaging a specialist is a chargeable option. Their fee is this entity's own cost: declare it among the "
          "entity's costs for a cycle, and it comes off before profit (P5.16 clause 6). Workstation sets no price for it "
          "and charges nothing for it.")
WHEN = ("A specialist is warranted before this entity's work is relied on in care, law, education or money readiness "
        "(P5.15 clause 7), and they review in that discipline. This is Workstation's own statement; it claims no "
        "professional's role.")


def _recommendation(record: Dict[str, Any]) -> Dict[str, Any]:
    """P5.15 RELEASE: for a generated entity, engaging a specialist is a chargeable option the platform recommends.
    Read from the entity's own record: the door that made it."""
    door = str(record.get("established_through") or "")
    if door in GENERATING_DOORS:
        said = (f"Workstation generated this entity, through {GENERATING_DOORS[door]}, so it recommends engaging a "
                f"specialist to review the entity's work before anyone relies on it.")
    else:
        said = ("This entity's record names no door through which Workstation generated it, so Workstation makes no "
                "recommendation for it. Attaching a specialist remains open to it.")
    return {"recommended": door in GENERATING_DOORS, "chargeable": True, "established_through": door or None,
            "said": said, "charge": CHARGE, "when_warranted": WHEN}


class Specialist(BaseModel):
    model_config = {"extra": "forbid"}          # no contact detail can ride in: this is not a registry of people
    name: str
    discipline: str
    credential_as_stated: str
    reviews: str                                # what they review for this entity
    lapses_on: str                              # an ISO date, after today


class Signing(BaseModel):
    model_config = {"extra": "forbid"}          # the person's statement, and nothing Workstation composes
    deliverable_id: str
    reviewed: str                               # what in it they reviewed
    date: str                                   # the date they reviewed it: not after today
    lapses_on: str                              # after today, and not after their place lapses


class Retirement(BaseModel):
    model_config = {"extra": "forbid"}
    reason: str


def _today() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


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
    except Exception as e:                              # noqa: BLE001 - said, never read as an empty roster
        raise HTTPException(status_code=503, detail=(
            f"The roster could not be read ({type(e).__name__}), so no specialist is shown and none is added."))
    return {k: [r for r in v if isinstance(r, dict)] for k, v in (data or {}).items() if isinstance(v, list)}


def _require_entity(vsb_id: str, user: Any) -> Dict[str, Any]:
    """An entity the platform does not hold has no roster; under sign-in another person's entity is not found."""
    from agentic_core.api.vsb import _load_vsb
    record = _load_vsb(vsb_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Entity {vsb_id} not found, so it has no roster.")
    if not user_can_access(user if isinstance(user, dict) else None, record.get("owner_id")):
        raise HTTPException(status_code=404, detail=f"Entity {vsb_id} not found, so it has no roster.")
    return record


def _by(user: Any) -> str:
    #  who wrote it: the signed-in name, or the single-user label when sign-in is off (as the review records say it)
    return (user.get("username") if isinstance(user, dict) else None) or "single-user-mode"


def _state(entry: Dict[str, Any], today: _dt.date) -> str:
    if entry.get("retired_at"):
        return "retired"
    try:
        lapses = _dt.date.fromisoformat(str(entry.get("lapses_on"))[:10])
    except ValueError:
        return "lapsed"                                   # a date that cannot be read is not a place still held
    return "lapsed" if lapses < today else "active"


def _view(vsb_id: str, rows: List[Dict[str, Any]], record: Dict[str, Any]) -> Dict[str, Any]:
    today = _today()
    shown = [{**r, "state": _state(r, today)} for r in rows]
    active = [r for r in shown if r["state"] == "active"]
    return {"vsb_id": vsb_id, "limit": LIMIT, "active": active,
            "lapsed": [r for r in shown if r["state"] == "lapsed"],
            "retired": [r for r in shown if r["state"] == "retired"],
            "places_left": max(0, LIMIT - len(active)), "disciplines": list(DISCIPLINES),
            "basis": BASIS, "credential_basis": NOT_VERIFIED, "recommendation": _recommendation(record)}


@router.get("/{vsb_id}")
async def roster(vsb_id: str, user: dict | None = Depends(get_current_user)):
    record = _require_entity(vsb_id, user)
    return _view(vsb_id, _read().get(vsb_id, []), record)


@router.post("/{vsb_id}")
async def attach(vsb_id: str, req: Specialist, user: dict | None = Depends(get_current_user)):
    """Attach a specialist to this entity's roster. Refused, with nothing written, when a field is empty, the
    discipline is not one of clause 7's four, the lapse date is not a date after today, or five places are held."""
    record = _require_entity(vsb_id, user)
    fields = {k: str(getattr(req, k) or "").strip() for k in ("name", "discipline", "credential_as_stated", "reviews",
                                                               "lapses_on")}
    empty = [k for k, v in fields.items() if not v]
    if empty:
        raise HTTPException(status_code=422, detail=f"Not attached: a specialist names {', '.join(empty)}.")
    if fields["discipline"] not in DISCIPLINES:
        raise HTTPException(status_code=422, detail=(
            f"Not attached: the discipline is one of {', '.join(DISCIPLINES)} (P5.15 clause 7), not {fields['discipline']!r}."))
    try:
        lapses = _dt.date.fromisoformat(fields["lapses_on"][:10])
    except ValueError:
        raise HTTPException(status_code=422, detail="Not attached: the date the place lapses is not a date (YYYY-MM-DD).")
    if lapses <= _today():
        raise HTTPException(status_code=422, detail=f"Not attached: the place would lapse on {lapses.isoformat()}, "
                                                    f"which is not after today.")
    entry = {"specialist_id": f"spec-{uuid.uuid4().hex[:10]}", **fields, "lapses_on": lapses.isoformat(),
             "added_by": _by(user), "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    from agentic_core.config import mutate_json
    refused: Dict[str, str] = {}

    def _add(existing):
        data = existing if isinstance(existing, dict) else {}
        rows = [r for r in (data.get(vsb_id) or []) if isinstance(r, dict)]
        held = sum(1 for r in rows if _state(r, _today()) == "active")
        if held >= LIMIT:
            refused["why"] = (f"Not attached: this entity's roster holds {held} specialists, and a roster holds "
                              f"{LIMIT} at a time. Retire one, with the reason, to make a place.")
            return data
        rows.append(entry)
        data[vsb_id] = rows
        return data
    _read()                                                  # an unreadable store refuses before any write
    mutate_json(_path(), _add, dict)
    if refused:
        raise HTTPException(status_code=409, detail=refused["why"])
    return {"attached": True, "specialist": {**entry, "state": "active"}, "credential_basis": NOT_VERIFIED,
            **{k: v for k, v in _view(vsb_id, _read().get(vsb_id, []), record).items() if k in ("places_left", "limit")}}


@router.post("/{vsb_id}/{specialist_id}/retire")
async def retire(vsb_id: str, specialist_id: str, req: Retirement, user: dict | None = Depends(get_current_user)):
    """Retire a specialist from the roster, with the reason. The entry is kept, marked retired with who and when."""
    _require_entity(vsb_id, user)
    reason = str(req.reason or "").strip()
    if not reason:
        raise HTTPException(status_code=422, detail="Not retired: a retirement gives its reason.")
    from agentic_core.config import mutate_json
    outcome: Dict[str, Any] = {}

    def _retire(existing):
        data = existing if isinstance(existing, dict) else {}
        for r in data.get(vsb_id) or []:
            if isinstance(r, dict) and r.get("specialist_id") == specialist_id:
                if r.get("retired_at"):
                    outcome["code"] = 409
                    return data
                r.update(retired_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), retired_by=_by(user),
                         retired_reason=reason)
                outcome["entry"] = dict(r)
                return data
        outcome["code"] = 404
        return data
    _read()
    mutate_json(_path(), _retire, dict)
    if outcome.get("code") == 404:
        raise HTTPException(status_code=404, detail=f"No specialist {specialist_id} is on this entity's roster.")
    if outcome.get("code") == 409:
        raise HTTPException(status_code=409, detail=f"Specialist {specialist_id} is already retired; the record stands.")
    return {"retired": True, "specialist": {**outcome["entry"], "state": "retired"}}


#  W934 (P5.15 clauses 5 and 6) - THE THIRD TIER FOR THIS ENTITY'S WORK: a specialist's signature on one exact version
SIGNED_STORE = "entity_signatures.json"
SIGN_BASIS = ("A signature is the third tier for this entity's work (P5.15 clause 5): a named person's record - their "
              "name and credential as stated, what they reviewed (one version of one of this entity's deliverables, "
              "and what in it), the date they reviewed it, and when the signature lapses. Only a specialist holding a "
              "place on this entity's roster signs, and a signature does not outlive that place. A signature is of the "
              "exact text it signed: once the deliverable is run again, the new version is unreviewed until it is "
              "signed. A signature is the person's statement; Workstation composes no part of it.")


def _signed_path():
    from agentic_core.config import data_path
    return data_path(SIGNED_STORE)


def _read_signed() -> Dict[str, List[Dict[str, Any]]]:
    p = _signed_path()
    if not p.exists():
        return {}
    from agentic_core.config import read_json_strict
    try:
        data = read_json_strict(p, dict, expect=dict)
    except Exception as e:                              # noqa: BLE001 - said, never read as "nothing is signed"
        raise HTTPException(status_code=503, detail=(
            f"The signatures could not be read ({type(e).__name__}), so no signature is shown and none is added."))
    return {k: [r for r in v if isinstance(r, dict)] for k, v in (data or {}).items() if isinstance(v, list)}


def _text_hash(text: Any) -> str:
    import hashlib
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def _entity_deliverables(vsb_id: str, user: Any) -> Dict[str, Dict[str, Any]]:
    """This entity's deliverables the caller may read, by id."""
    from agentic_core.api import deliverables as _dl
    u = user if isinstance(user, dict) else None
    return {d["id"]: d for d in _dl._load() if d.get("vsb_id") == vsb_id and d.get("id")
            and user_can_access(u, d.get("owner_id"))}


def judge_signature(sig: Dict[str, Any], deliverable: Optional[Dict[str, Any]], today: _dt.date) -> Optional[str]:
    """Why a stored signature does not count now, or None when it does."""
    try:
        lapses = _dt.date.fromisoformat(str(sig.get("lapses_on"))[:10])
    except ValueError:
        return "its lapse date cannot be read"
    if lapses < today:
        return f"it lapsed on {lapses.isoformat()}"
    if deliverable is None:
        return "the deliverable it signed is no longer held"
    if sig.get("content_sha256") != _text_hash(deliverable.get("content")):
        return (f"it signed version {sig.get('version')}; the deliverable has been run again since, and its version "
                f"{len(deliverable.get('versions') or [])} is not signed")
    return None


def deliverable_review(sigs: List[Dict[str, Any]], deliverable: Dict[str, Any], today: _dt.date) -> Dict[str, Any]:
    """The tier one of this entity's deliverables has reached: a qualified person's signature on its current text,
    or unreviewed. Nothing here is a review Workstation made."""
    from agentic_core.api._review_tier import LABEL, SIGNED_BY_PERSON, UNREVIEWED
    mine = [s for s in sigs if s.get("deliverable_id") == deliverable.get("id")]
    judged = [(s, judge_signature(s, deliverable, today)) for s in mine]
    good = [s for s, why in judged if why is None]
    if good:
        top = max(good, key=lambda s: str(s.get("date")))
        return {"tier": SIGNED_BY_PERSON, "label": LABEL[SIGNED_BY_PERSON],
                "basis": (f"signed by {top['name']} ({top['credential_as_stated']} - as stated; {NOT_VERIFIED}) on "
                          f"{top['date']}, for version {top['version']}, until {top['lapses_on']}"),
                "signatures_counted": len(good), "signatures_not_counted": len(judged) - len(good)}
    return {"tier": UNREVIEWED, "label": LABEL[UNREVIEWED],
            "basis": ("no specialist on this entity's roster has signed its current text"
                      + (f"; {len(judged)} signature(s) of it do not count" if judged else "")),
            "signatures_counted": 0, "signatures_not_counted": len(judged)}


@router.post("/{vsb_id}/{specialist_id}/sign")
async def sign(vsb_id: str, specialist_id: str, req: Signing, user: dict | None = Depends(get_current_user)):
    """A specialist holding a place on this entity's roster signs the current version of one of its deliverables.
    Refused, with nothing written, when a field is empty, the specialist is not on the roster or holds no place, a
    date is not a date, the review is dated after today, the signature would lapse by today or after the place lapses,
    or the deliverable is not one of this entity's."""
    _require_entity(vsb_id, user)
    fields = {k: str(getattr(req, k) or "").strip() for k in ("deliverable_id", "reviewed", "date", "lapses_on")}
    empty = [k for k, v in fields.items() if not v]
    if empty:
        raise HTTPException(status_code=422, detail=f"Not signed: a signature names {', '.join(empty)}.")
    today = _today()
    spec = next((r for r in _read().get(vsb_id, []) if r.get("specialist_id") == specialist_id), None)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"No specialist {specialist_id} is on this entity's roster.")
    state = _state(spec, today)
    if state != "active":
        raise HTTPException(status_code=409, detail=(
            f"Not signed: {spec.get('name')} is {state} on this entity's roster, and only a specialist holding a "
            f"place signs."))
    try:
        on = _dt.date.fromisoformat(fields["date"][:10])
        lapses = _dt.date.fromisoformat(fields["lapses_on"][:10])
    except ValueError:
        raise HTTPException(status_code=422, detail=(
            "Not signed: the date reviewed and the date the signature lapses are dates (YYYY-MM-DD)."))
    if on > today:
        raise HTTPException(status_code=422, detail=f"Not signed: the review is dated {on.isoformat()}, after today.")
    if lapses <= today:
        raise HTTPException(status_code=422, detail=(
            f"Not signed: the signature would lapse on {lapses.isoformat()}, which is not after today."))
    place = _dt.date.fromisoformat(str(spec.get("lapses_on"))[:10])
    if lapses > place:
        raise HTTPException(status_code=422, detail=(
            f"Not signed: the signature would lapse on {lapses.isoformat()}, after {spec.get('name')}'s place lapses "
            f"on {place.isoformat()}. A signature does not outlive the place."))
    d = _entity_deliverables(vsb_id, user).get(fields["deliverable_id"])
    if d is None:
        raise HTTPException(status_code=404, detail=(
            f"Deliverable {fields['deliverable_id']} is not one of this entity's, so it is not signed for it."))
    entry = {"signature_id": f"sig-{uuid.uuid4().hex[:10]}", "specialist_id": specialist_id,
             "name": spec.get("name"), "credential_as_stated": spec.get("credential_as_stated"),
             "discipline": spec.get("discipline"), "deliverable_id": d["id"], "deliverable_title": d.get("title"),
             "version": len(d.get("versions") or []) or 1, "content_sha256": _text_hash(d.get("content")),
             "reviewed": fields["reviewed"], "date": on.isoformat(), "lapses_on": lapses.isoformat(),
             "entered_by": _by(user), "entered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    from agentic_core.config import mutate_json

    def _add(existing):
        data = existing if isinstance(existing, dict) else {}
        data.setdefault(vsb_id, []).append(entry)
        return data
    _read_signed()                                           # an unreadable store refuses before any write
    mutate_json(_signed_path(), _add, dict)
    return {"signed": True, "signature": entry, "credential_basis": NOT_VERIFIED,
            "deliverable_now_says": deliverable_review(_read_signed().get(vsb_id, []), d, _today())}


@router.get("/{vsb_id}/signatures")
async def signatures(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_entity(vsb_id, user)
    held = _entity_deliverables(vsb_id, user)
    sigs = _read_signed().get(vsb_id, [])
    today = _today()
    rows = []
    for s in sigs:
        why = judge_signature(s, held.get(str(s.get("deliverable_id"))), today)
        rows.append({**s, "counts": why is None, "why_not": why})
    return {"vsb_id": vsb_id, "signatures": rows,
            "deliverables": {i: deliverable_review(sigs, d, today) for i, d in held.items()},
            "basis": SIGN_BASIS, "credential_basis": NOT_VERIFIED}
