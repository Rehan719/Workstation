"""
Iterative Refinement API — lets a user advance/develop/refine ANY tool output in-house. Generic by
design: it takes a previous output + a refinement instruction and returns the full improved version,
served on Workstation's OWN native fabric with honest in-house provenance. The frontend <DomainTool>
result card posts here so every one of the 18 domain tools + the fabric-run resources gains iterative
refinement (each refinement builds on the last). Honest: refines/extends only the supplied content —
never fabricates facts not present or implied in the draft + instruction.

  POST /api/v1/refine — return an improved version of `previous` per `instruction`
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text, person_said

router = APIRouter(prefix="/api/v1", tags=["refine"])


class RefineRequest(BaseModel):
    previous: str                 # the current draft/output to refine
    instruction: str              # how to advance/develop/refine it
    context: str = ""             # optional: what the output is (e.g. the tool's title)
    #  W671 (Owner ruling 2026-10-11) - the tool the draft came from, so a religious tool's draft is known as
    #  one. It is a hint the page gives; the gate below also reads the text, so omitting it opens nothing.
    source_endpoint: str = ""


_RELIGION_SOURCES = ("/api/v1/religion/", "/api/v1/qep/", "/api/qep/")


#  Words that mark religious content and are not in the teaching-subject list (which names subjects a curriculum
#  teaches). A word list can FLAG and never clear: an unmatched text was not reviewed, and the response says so.
_RELIGIOUS_WORDS = ("fatwa", "halal", "haram", "ramadan", "interfaith", "mufti", "imam", "mosque", "masjid",
                    "salah", "zakat", "hajj", "umrah", "ayah", "surah", "prophet", "scripture", "bible", "torah",
                    "gospel", "theology", "religious ruling", "madhab", "madhhab", "ijma", "qiyas")


def _religious_reason(req: "RefineRequest", rewrite: str = ""):
    """Why this refine request is treated as religious content, or None. Two readings, either enough: the tool
    the draft came from, as the page states it; and this platform's own religious-subject screen over the draft
    and the instruction - which can flag and never clear, so None here means only that nothing matched."""
    src = str(req.source_endpoint or "")
    if src.startswith(_RELIGION_SOURCES):
        return f"the draft came from a Religion tool ({src})"
    from agentic_core.religious_domain.subject_screen import screen_subject
    hit = screen_subject(req.previous, req.instruction, req.context, rewrite)
    if hit.get("flagged"):
        return "the draft, the instruction or the rewrite names " + ", ".join(hit.get("matched") or [])
    import re as _re
    hay = " ".join(str(x or "") for x in (req.previous, req.instruction, req.context, rewrite)).lower()
    more = sorted({w for w in _RELIGIOUS_WORDS if _re.search(r"(?<![a-z])" + _re.escape(w) + r"(?![a-z])", hay)})
    if more:
        return "the draft, the instruction or the rewrite names " + ", ".join(more)
    return None


@router.post("/refine")
async def refine(req: RefineRequest):
    """Iteratively advance a previous output. Returns the FULL improved version (not just a diff) so
    the user can refine again on top of it."""
    what = f" ({req.context})" if req.context else ""
    prompt = (
        f"You are refining an existing draft{what}. Apply the user's instruction and return the FULL "
        "improved version (not a diff, not commentary) — keep everything that should stay, change what "
        "the instruction asks, and preserve the original format/structure. Do NOT invent facts that are "
        "not present in or clearly implied by the draft; if the instruction asks for information the draft "
        "cannot support, note that briefly at the end rather than fabricating it.\n\n"
        f"Refinement instruction:\n{req.instruction}\n\n"
        f"Current draft:\n{req.previous}"
    )
    refined, provenance = await ai_text(prompt, "refiner",
        user_text=person_said(req.instruction))
    # §3A (W336) — DRAFT-PRESERVING floor: the deterministic floor cannot genuinely rewrite a
    # draft, and the audit proved its output DISCARDED the user's work entirely. When the floor
    # serves, the user's draft is returned intact with the floor's structured additions appended
    # under an honest label — refinement never loses work, and the capability is never overstated.
    if provenance.get("served_by") == "native" and req.previous.strip():
        refined = (f"{req.previous.rstrip()}\n\n---\n\n"
                   f"### Refinement additions (in-house structured floor — the draft above is "
                   f"preserved verbatim; a full rewrite needs the owned model)\n\n{refined}")
    #  W671 (OWNER RULING 2026-10-11) - A MODEL'S REWRITE OF RELIGIOUS CONTENT IS MODEL-COMPOSED RELIGIOUS
    #  CONTENT. Every Religion tool result offered "Refine this output", and what came back was shown with no
    #  scholar gate - the one path round the rule the research tools now follow. The gate is HERE, at the
    #  route, so any caller meets it: a draft that came from a Religion tool, or whose text or instruction
    #  names a religious subject, is rewritten only under the same rule. Unapproved, the person's draft is
    #  returned as it was and the rewrite is queued for a named scholar; nothing composed is shown.
    _review668 = {}
    _religious = _religious_reason(req, refined if provenance.get("served_by") != "native" else "")
    if _religious and provenance.get("served_by") != "native":
        from agentic_core.api.religion import _scholar_gated, _review_fields
        _shown, _held, _sr_state, _note = _scholar_gated(
            "refine", refined, req.instruction, (), provenance)
        if _sr_state.get("state") == "approved":
            refined = _shown            # the text the gate approved, exactly - not the route's own copy of it
        else:
            refined = req.previous
            #  the quality figures in the provenance were measured on the rewrite that is not being shown
            provenance = {k: v for k, v in (provenance or {}).items() if k != "quality_assurance"}
            provenance["quality_assurance_basis"] = ("not reported: it was measured on a rewrite that is "
                                                     "withheld, and says nothing about the draft returned")
        _review668 = {**_review_fields(_note, _sr_state), "refine_withheld": _sr_state.get("state") != "approved",
                      "religious_basis": _religious}
    return {
        "refine_id": uuid.uuid4().hex[:10],
        "refined": refined,
        #  what the religious-content reading rests on, when it found nothing: a word list, which cannot clear
        **({} if _religious else {"religious_screen": "no religious term matched the draft, the instruction or "
                                                      "the rewrite - a word list, which can flag and never clear"}),
        **_review668,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
