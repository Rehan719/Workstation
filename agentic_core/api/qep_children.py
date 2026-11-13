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

from fastapi import APIRouter, Depends, HTTPException

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
