"""THE CHILDREN'S TOOLS - built, and held behind one gate (P5.21 clauses 3 and 4; W943).

OWNER RULINGS 2026-10-12 and 2026-10-14: the children's Education and Quran tools are built and HELD. Nothing
reaches a child until sign-in is on AND a scholar on the roster has approved the CURRENT approval pack
(agentic_core/religious_domain/approval_pack.py). Every children's tool route is on this router, under the one
prefix approval_pack.CHILDREN_PREFIX, and the router itself asks the gate before any handler runs: a route added
here cannot skip it. A held tool answers 423 with the gate's own sentence, which says why it is held.

Each tool is described in approval_pack.CHILDREN_TOOLS in the change that builds it, with the routes it serves.
The census in test_w943 lists the routes mounted under the prefix and fails on one the pack does not describe,
on a described one that is not mounted, and on one that does not answer HELD with the gate's sentence while
sign-in is off.

TOOL 1 - MEMORISATION PRACTICE, RUN BY A PARENT OR TEACHER. The adult chooses a verse. The child sees its first
word, fetched from the named edition, and says the rest from memory to the adult; the adult may show the next
word, or the whole verse. It is the adult tool's arithmetic over the FETCHED text (memorization/practice.py):
nothing is composed, nothing listens, nothing is marked, and nothing is recorded. The wording on the screen is
served from the tool's entry in the pack, so the screen says what the scholar approved and nothing else.
"""
from __future__ import annotations

import datetime as _dt
import hashlib as _hashlib

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.auth.core import get_current_user
from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock
from agentic_core.religious_domain import api as _qep
from agentic_core.religious_domain import approval_pack as _ap
from agentic_core.religious_domain.memorization import practice as _practice


def _held() -> None:
    """THE GATE, asked before every handler on this router. Held: 423, with the gate's own sentence."""
    gate = _ap.children_tools_open()
    if not gate["open"]:
        raise HTTPException(status_code=423, detail=gate["basis"])


router = APIRouter(prefix=_ap.CHILDREN_PREFIX, tags=["qep-children"], dependencies=[Depends(_held)])

MEMORISATION = "memorisation-practice"
_EDITION = "quran-uthmani"           # the edition the adult practice routes fetch, named on every answer


def _screen(tool_id: str) -> dict:
    """What the adult's screen shows beside the verse: the tool's own entry in the pack, never a second copy."""
    tool = next(t for t in _ap.CHILDREN_TOOLS if t["id"] == tool_id)
    return {"tool": tool["id"], "name": tool["name"], "wording": list(tool["wording"])}


_NOTHING_KEPT = ("nothing about the child, the verse or how the practice went is recorded; the child is not "
                 "signed in and is not named")


@router.get("/memorisation/{surah_number}/{ayah_number}")
async def children_memorisation(surah_number: int, ayah_number: int, shown_words: int = 1, reveal: bool = False):
    """The verse's first word(s), as fetched from the named edition; the whole verse only when the adult asks."""
    fetched = await _qep._practice_text(surah_number, ayah_number)
    out = {"ref": f"{surah_number}:{ayah_number}", **_practice.hidden_view(fetched, shown_words),
           "revealed": bool(reveal), **_qep._corpus_provenance(_EDITION), "screen": _screen(MEMORISATION),
           "judged": False, "judged_basis": "nothing the child says is received, listened to or assessed",
           "kept": False, "kept_basis": _NOTHING_KEPT}
    if reveal:
        out["text"] = fetched
    return out


@router.get("/memorisation/{surah_number}/{ayah_number}/next")
async def children_memorisation_next(surah_number: int, ayah_number: int, after_words: int = 0):
    """The one word after the first `after_words` words, for when the child pauses and the adult shows it."""
    fetched = await _qep._practice_text(surah_number, ayah_number)
    return {"ref": f"{surah_number}:{ayah_number}", **_practice.next_word(fetched, after_words),
            **_qep._corpus_provenance(_EDITION), "screen": _screen(MEMORISATION),
            "judged": False, "judged_basis": "a position in the verse as fetched; nothing was listened to",
            "kept": False, "kept_basis": _NOTHING_KEPT}


# ── TOOL 2 - A CHALLENGE AGAINST THE CHILD'S OWN PAST (W944) ─────────────────────────────────────────────────────
#  R4: a challenge is only against the child's own past - no ranking, no award, no streak. R6: the adult runs it; the
#  child does not sign in and is never named: a child is one of the signed-in adult's numbered children, 1 to 9. R7:
#  what is kept is which portions were practised and on which day, for the adult running the tool. The weekly counts
#  are worked out from those days on every read, and never kept as a measure of the child.
CHALLENGE = "own-past-challenge"
_CHILDREN = range(1, 10)
_EARLIER_WEEKS = 8


def _today() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _adult(user) -> str:
    """The signed-in parent or teacher whose record this is. No children's tool is run without one."""
    if not (isinstance(user, dict) and user.get("username")):
        raise HTTPException(status_code=401, detail="A children's tool is run by a signed-in parent or teacher.")
    return str(user["username"])


def _child(child: int) -> str:
    if child not in _CHILDREN:
        raise HTTPException(status_code=422, detail=("A child is one of your numbered children, 1 to 9. A child is "
                                                     "never named here."))
    return str(child)


def _record_path(adult: str):
    #  the file is named by a digest of the adult's account, so no name of anyone is in a path
    return data_path("children_practice", _hashlib.sha256(adult.encode("utf-8")).hexdigest()[:32] + ".json")


def _load(path) -> dict:
    return read_json_strict(path, {"children": {}}, expect=dict)


class PractisedRequest(BaseModel):
    model_config = {"extra": "forbid"}
    surah_number: int
    from_ayah: int
    to_ayah: int


def _view(slot: str, children: dict) -> dict:
    """This week's count of portions practised, beside the child's own earlier weeks, and the screen's sentences:
    the pack's own templates with these counts in them."""
    days = children.get(slot) or []
    today = _today()
    monday = today - _dt.timedelta(days=today.weekday())
    per_week: dict = {}
    for e in days:
        d = _dt.date.fromisoformat(e["on"])
        start = d - _dt.timedelta(days=d.weekday())
        per_week[start] = per_week.get(start, 0) + 1
    this_week = per_week.get(monday, 0)
    earlier = [{"week_starting": (monday - _dt.timedelta(weeks=i)).isoformat(),
                "portions": per_week.get(monday - _dt.timedelta(weeks=i), 0)} for i in range(1, _EARLIER_WEEKS + 1)]
    tool = next(t for t in _ap.CHILDREN_TOOLS if t["id"] == CHALLENGE)
    counts = {"this_week": this_week, "last_week": earlier[0]["portions"]}
    return {"child": int(slot), "this_week": this_week, "earlier_weeks": earlier,
            "screen": {"tool": tool["id"], "name": tool["name"], "wording": list(tool["wording"]),
                       "sentences": [w.format(**counts) for w in tool["wording"]]},
            "practised": days,
            "compared_with": "this child's own earlier weeks, and nobody else",
            "kept_basis": ("which portion was practised and on which day, for you and this numbered child only; the "
                           "weekly counts are worked out from those days when read, and are not kept"),
            "judged": False, "judged_basis": "the adult says a portion was practised; nothing here assesses it"}


@router.post("/challenge/{child}/practised")
async def children_challenge_practised(child: int, req: PractisedRequest,
                                       user: dict | None = Depends(get_current_user)):
    """The adult notes that the child practised a portion today: a surah, its first verse and its last."""
    adult, slot = _adult(user), _child(child)
    _qep._check_ref(req.surah_number, req.from_ayah)
    _qep._check_ref(req.surah_number, req.to_ayah)
    if req.to_ayah < req.from_ayah:
        raise HTTPException(status_code=422, detail="A portion runs from its first verse to its last; the last is "
                                                    "before the first here.")
    path = _record_path(adult)
    path.parent.mkdir(parents=True, exist_ok=True)
    with store_lock(path):
        rec = _load(path)
        rec.setdefault("children", {}).setdefault(slot, []).append(
            {"surah": req.surah_number, "from_ayah": req.from_ayah, "to_ayah": req.to_ayah, "on": _today().isoformat()})
        atomic_write_json(path, rec)
    return _view(slot, rec["children"])


@router.get("/challenge/{child}")
async def children_challenge(child: int, user: dict | None = Depends(get_current_user)):
    """The challenge: this week beside the child's own earlier weeks."""
    adult, slot = _adult(user), _child(child)
    return _view(slot, _load(_record_path(adult)).get("children") or {})


@router.delete("/challenge/{child}")
async def children_challenge_remove(child: int, user: dict | None = Depends(get_current_user)):
    """The adult removes this child's record. Nothing of it is kept afterwards."""
    adult, slot = _adult(user), _child(child)
    path = _record_path(adult)
    removed = 0
    if path.exists():
        with store_lock(path):
            rec = _load(path)
            removed = len((rec.get("children") or {}).pop(slot, None) or [])
            atomic_write_json(path, rec)
    return {"child": int(slot), "removed": removed,
            "basis": (f"removed the {removed} portion(s) noted for this child; nothing of them is kept" if removed else
                      "there was nothing noted for this child to remove")}


# ── TOOL 3 - TEACHING AIDS FOR A TEACHER (W945) ──────────────────────────────────────────────────────────────────
#  A sheet of one portion for a lesson: each verse as fetched from the named edition, or, for recall practice, only
#  each verse's first word. R1: every verse is fetched, never written, with the edition named; a verse that cannot be
#  fetched is named as missing and nothing is put in its place. Nothing about the teacher's class or any child is
#  recorded.
TEACHING = "teaching-aids"
_SHEET_MOST_VERSES = 40


@router.get("/teaching/sheet/{surah_number}")
async def children_teaching_sheet(surah_number: int, from_ayah: int, to_ayah: int, first_words: bool = False,
                                  user: dict | None = Depends(get_current_user)):
    """A teacher's sheet of verses from_ayah..to_ayah of one surah, whole or first words only."""
    _adult(user)
    _qep._check_ref(surah_number, from_ayah)
    _qep._check_ref(surah_number, to_ayah)
    if to_ayah < from_ayah:
        raise HTTPException(status_code=422, detail="A portion runs from its first verse to its last; the last is "
                                                    "before the first here.")
    if to_ayah - from_ayah + 1 > _SHEET_MOST_VERSES:
        raise HTTPException(status_code=422, detail=(f"A sheet holds at most {_SHEET_MOST_VERSES} verses, each "
                                                     "fetched from the named edition; choose a shorter portion."))
    verses, missing = [], []
    for ayah in range(from_ayah, to_ayah + 1):
        fetched = await _qep.fetch_ayah_arabic(surah_number, ayah)
        ref = f"{surah_number}:{ayah}"
        if not fetched:
            missing.append(ref)
        elif first_words:
            view = _practice.hidden_view(fetched, 1)
            verses.append({"ref": ref, "shown": view["shown"], "hidden_words": view["hidden_words"]})
        else:
            verses.append({"ref": ref, "text": fetched})
    tool = next(t for t in _ap.CHILDREN_TOOLS if t["id"] == TEACHING)
    fill = {"surah": surah_number, "from_ayah": from_ayah, "to_ayah": to_ayah}
    return {"surah": surah_number, "from_ayah": from_ayah, "to_ayah": to_ayah, "first_words": bool(first_words),
            "verses": verses, "missing": missing, "complete": not missing, **_qep._corpus_provenance(_EDITION),
            "screen": {"tool": tool["id"], "name": tool["name"], "wording": list(tool["wording"]),
                       "sentences": [w.format(**fill) for w in tool["wording"]]},
            "kept": False, "kept_basis": "nothing about the teacher's class or any child is recorded"}
