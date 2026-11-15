"""P5.19 clauses 1, 2, 4 and 5 (W1082, FU-1078) - PHYSICAL ASSETS AS RECORDS AND EVIDENCE: NOTHING IS CONNECTED AND
NOTHING IS CONTROLLED.

Measured first (W711): no record of a physical asset existed; the devices and telemetry the integration surface lists
are labelled simulated, and a digital twin is a text specification.

CLAUSE 1 - AN ASSET RECORD for a physical thing (a vehicle, a robot, a drone, a laboratory instrument), holding what
it is as a person entered it, who owns it, who possesses it and the agreement record it is held under. Owner and
possessor are party records (agentic_core/api/agreements.py), so an entity of this platform is never either.

CLAUSE 2 - SIX FACTS THAT ARE NEVER MERGED: the right to use it; the permission of the place it would be used in; the
maker's evidence of conformity; the user's own safety evidence (assessment, training, inspection and maintenance);
insurance; and a named person's declaration that it is ready. Each is evidence a person attached, with who, when and
when it lapses; a fact with nothing attached reads "not evidenced"; no score, percentage or single word of readiness
is computed from them. The agreement an asset is held under is never read as any of the six: a lease is not
permission to operate.

CLAUSE 4 - NOTHING IS CONTROLLED: nothing here connects to a device, sends it a command or takes in its telemetry, and
no twin or simulation is offered as evidence of safety.

CLAUSE 5 - A LAPSE IS A CHANGE OF STATE: evidence past its date reads lapsed, and a declaration of readiness resting on
evidence that has lapsed reads withdrawn until a person declares again.

Safety evidence is a competent person's: it is recorded here, never judged. Kept only for a signed-in person, as the
agreement records are: an asset record names who owns and possesses it, real persons and registered bodies.
"""
import uuid
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.api.agreements import (AGREEMENTS, NOT_AN_ENTITY, PARTIES, _Asked, _entity_named, _mutate, _now,
                                         _only, _reaches, _read, _today)
from agentic_core.auth.core import auth_enabled, get_current_user

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])

ASSETS = "assets.json"
KINDS = ("vehicle", "robot", "drone", "laboratory_instrument", "other")
FACTS = ("right_to_use", "place_permission", "maker_conformity", "user_safety", "insurance", "readiness")
FACT_NAMES = {
    "right_to_use": "the right to use it",
    "place_permission": "the permission of the place it would be used in",
    "maker_conformity": "the maker's evidence of conformity",
    "user_safety": "the user's own safety evidence (assessment, training, inspection and maintenance)",
    "insurance": "insurance",
    "readiness": "a named person's declaration that it is ready",
}
NOT_KEPT = ("Nothing is kept here before sign-in: an asset record names who owns and who possesses it, real persons "
            "and registered bodies, and the Owner's ruling of 2026-10-12 builds after sign-in anything that keeps "
            "something about a person. Sign-in is the Owner's switch.")
NOT_EVIDENCED = "not evidenced"
NOT_CONTROLLED = ("Nothing here connects to it, sends it a command or takes in anything from it: it is a record, and "
                  "no twin or simulation is evidence of its safety.")
NOT_JUDGED = ("Each piece of evidence is recorded as the person attached it; this platform judges none of it, and "
              "computes no score and no single word of readiness from the six.")
AGREEMENT_IS_NOT_PERMISSION = ("The agreement it is held under is recorded as stated. It is not, of itself, evidence "
                               "of the right to use it or of any place's permission to use it there.")
LIMITS_EXTRA = {"what": 300, "evidence": 500, "named_person": 200}


def _person(user) -> str:
    if not auth_enabled():
        raise HTTPException(status_code=403, detail=NOT_KEPT)
    if not isinstance(user, dict) or not user.get("username"):
        raise HTTPException(status_code=403, detail="No signed-in person is on this call, so nothing was kept.")
    return str(user["username"])


def _short(value, what: str, key: str, required: bool = True) -> Optional[str]:
    s = str(value if value is not None else "").strip()
    if not s:
        if required:
            raise HTTPException(status_code=400, detail=f"{what} is needed, and none was given, so nothing was kept.")
        return None
    if len(s) > LIMITS_EXTRA[key]:
        raise HTTPException(status_code=400, detail=(
            f"{what} is {len(s)} characters, more than the {LIMITS_EXTRA[key]} this record holds, so nothing was kept."))
    return s


def _lapse_date(value) -> str:
    """When the evidence lapses, as the person entered it: any real date, past or to come."""
    import re
    s = str(value or "").strip()
    d = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            d = date.fromisoformat(s)
        except ValueError:
            d = None
    if d is None:
        raise HTTPException(status_code=400, detail=(
            f"When the evidence lapses must be a date written YYYY-MM-DD; '{s or 'nothing'}' is not one, so nothing "
            f"was kept. Evidence with no end of its own is entered with the date its holder would next check it."))
    return s


class AssetRequest(_Asked):
    what: str = ""
    kind: str = ""
    owned_by: str = ""
    possessed_by: str = ""
    agreement_id: str = ""


class EvidenceRequest(_Asked):
    fact: str = ""
    evidence: str = ""
    lapses_on: str = ""
    named_person: Optional[str] = None


def _lapsed(e: dict, today: date) -> bool:
    try:
        return date.fromisoformat(str(e.get("lapses_on"))) < today
    except ValueError:
        return False


def _facts(a: dict) -> List[dict]:
    """The six facts, apart, in their order; each piece of evidence says whether it has lapsed, and a declaration of
    readiness resting on evidence that has lapsed says it is withdrawn. Nothing is computed across the six."""
    today = _today()
    by_id = {e["id"]: e for e in a.get("evidence") or []}
    out = []
    for fact in FACTS:
        entries = []
        for e in a.get("evidence") or []:
            if e.get("fact") != fact:
                continue
            row = {**e, "state": "lapsed" if _lapsed(e, today) else "current"}
            if fact == "readiness":
                gone = [by_id[i] for i in e.get("rests_on") or [] if i in by_id and _lapsed(by_id[i], today)]
                if row["state"] == "current" and gone:
                    row["state"] = "withdrawn"
                    row["withdrawn_because"] = (
                        "it rests on evidence that has lapsed: " + "; ".join(
                            f"{FACT_NAMES[g['fact']]} ({g['evidence']}), lapsed on {g['lapses_on']}" for g in gone)
                        + ". It stays withdrawn until a person declares again.")
            entries.append(row)
        out.append({"fact": fact, "name": FACT_NAMES[fact], "evidence": entries,
                    **({} if entries else {"said": NOT_EVIDENCED})})
    return out


def _public(a: dict, parties: list, agreements: list) -> dict:
    p = {x["id"]: x for x in parties}
    ag = {x["id"]: x for x in agreements}

    def party(pid):
        x = p.get(pid)
        return {"party_id": pid, "name": x.get("name") if x else None, "kind": x.get("kind") if x else None,
                **({} if x else {"said": "This party's record is not in the party store."})}
    held = ag.get(a.get("agreement_id"))
    return {"id": a["id"], "what": a["what"], "kind": a["kind"], "owned_by": party(a.get("owned_by")),
            "possessed_by": party(a.get("possessed_by")),
            "held_under": {"agreement_id": a.get("agreement_id"), "title": held.get("title") if held else None,
                           **({} if held else {"said": "This agreement record is not in the agreement store."}),
                           "basis": AGREEMENT_IS_NOT_PERMISSION},
            "entered_by": a.get("entered_by"), "entered_at": a.get("entered_at"),
            "facts": _facts(a), "controlled": False, "controlled_basis": NOT_CONTROLLED, "judged_basis": NOT_JUDGED}


def _mine(rows: list, aid: str, user) -> dict:
    a = next((r for r in rows if r.get("id") == aid), None)
    if a is None or not _reaches(user, a):
        raise HTTPException(status_code=404, detail=f"No asset record {aid} was found.")
    return a


@router.post("")
async def enter_asset(req: AssetRequest, user: dict | None = Depends(get_current_user)):
    """Clause 1: a physical thing, as a person entered it, who owns and who possesses it (party records), and the
    agreement record it is held under."""
    who = _person(user)
    _only(req, "An asset is entered by what it is, its kind, who owns it, who possesses it and the agreement it is held "
               "under;")
    what = _short(req.what, "What the asset is", "what")
    kind = str(req.kind or "").strip()
    if kind not in KINDS:
        raise HTTPException(status_code=400, detail=(
            f"An asset's kind is one of {', '.join(KINDS)}; '{kind or 'nothing'}' is not one, so nothing was kept."))
    mine = {p["id"]: p for p in _read(PARTIES) if _reaches(user, p)}
    for role, pid in (("owns", req.owned_by), ("possesses", req.possessed_by)):
        pid = str(pid or "").strip()
        if not pid:
            raise HTTPException(status_code=400, detail=(
                f"Nobody was named as who {role} it: that is a party record of yours, as the person or registered "
                f"body it is, so nothing was kept."))
        if pid not in mine:
            if _entity_named(pid, user):
                raise HTTPException(status_code=400, detail=NOT_AN_ENTITY.format(id=f"'{pid}'"))
            raise HTTPException(status_code=400, detail=(
                f"Who {role} it is named by a party record of yours, as the person or registered body it is; "
                f"'{pid or 'nothing'}' is not one, so nothing was kept."))
    aid = str(req.agreement_id or "").strip()
    if not aid:
        raise HTTPException(status_code=400, detail=(
            "No agreement was named: an asset is held under an agreement record of yours, so nothing was kept."))
    if not any(x.get("id") == aid and _reaches(user, x) for x in _read(AGREEMENTS)):
        raise HTTPException(status_code=400, detail=(
            f"An asset is held under an agreement record of yours; '{aid or 'nothing'}' is not one, so nothing was "
            f"kept."))
    a = {"id": f"ast-{uuid.uuid4().hex[:10]}", "owner": who, "what": what, "kind": kind,
         "owned_by": str(req.owned_by).strip(), "possessed_by": str(req.possessed_by).strip(), "agreement_id": aid,
         "entered_by": who, "entered_at": _now(), "evidence": []}
    _mutate(ASSETS, lambda rows: rows.append(a))
    return _public(a, list(mine.values()), _read(AGREEMENTS))


@router.get("")
async def list_assets(user: dict | None = Depends(get_current_user)):
    """This person's asset records (an administrator: every one), each with its six facts apart."""
    if not auth_enabled():
        return {"assets": [], "kept": False, "not_kept_because": NOT_KEPT, "controlled_basis": NOT_CONTROLLED}
    parties, agreements = _read(PARTIES), _read(AGREEMENTS)
    rows = [_public(a, parties, agreements) for a in _read(ASSETS) if _reaches(user, a)]
    return {"assets": rows[::-1], "kept": True, "total": len(rows), "controlled_basis": NOT_CONTROLLED,
            "judged_basis": NOT_JUDGED}


@router.get("/{aid}")
async def read_asset(aid: str, user: dict | None = Depends(get_current_user)):
    if not auth_enabled():
        raise HTTPException(status_code=404, detail=f"No asset record {aid} was found. {NOT_KEPT}")
    return _public(_mine(_read(ASSETS), aid, user), _read(PARTIES), _read(AGREEMENTS))


@router.post("/{aid}/evidence")
async def attach_evidence(aid: str, req: EvidenceRequest, user: dict | None = Depends(get_current_user)):
    """Clause 2: one piece of evidence for one of the six facts, as a person attached it, with when it lapses. A
    declaration of readiness names the person declaring, and rests on the evidence current when it is made."""
    who = _person(user)
    _only(req, "Evidence is attached to one fact, with what it is, when it lapses and, for a declaration of readiness, "
               "the person declaring;")
    fact = str(req.fact or "").strip()
    if fact not in FACTS:
        raise HTTPException(status_code=400, detail=(
            f"Evidence is attached to one of the six facts ({', '.join(FACTS)}); '{fact or 'nothing'}' is not one, so "
            f"nothing was kept."))
    evidence = _short(req.evidence, "What the evidence is", "evidence")
    lapses = _lapse_date(req.lapses_on)
    named = _short(req.named_person, "The person declaring it ready", "named_person", required=fact == "readiness")
    if fact != "readiness" and named:
        raise HTTPException(status_code=400, detail=(
            "A named person is the declaration of readiness's; evidence for another fact is attached without one, so "
            "nothing was kept."))

    def _change(rows):
        a = _mine(rows, aid, user)
        today = _today()
        e = {"id": f"evd-{uuid.uuid4().hex[:10]}", "fact": fact, "evidence": evidence, "lapses_on": lapses,
             "attached_by": who, "attached_at": _now()}
        if fact == "readiness":
            e["named_person"] = named
            e["rests_on"] = [x["id"] for x in a.get("evidence") or []
                             if x.get("fact") != "readiness" and not _lapsed(x, today)]
        a.setdefault("evidence", []).append(e)
        return a
    a = _mutate(ASSETS, _change)
    return _public(a, _read(PARTIES), _read(AGREEMENTS))
