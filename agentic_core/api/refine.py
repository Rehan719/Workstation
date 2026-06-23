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

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1", tags=["refine"])


class RefineRequest(BaseModel):
    previous: str                 # the current draft/output to refine
    instruction: str              # how to advance/develop/refine it
    context: str = ""             # optional: what the output is (e.g. the tool's title)


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
    refined, provenance = await ai_text(prompt, "refiner")
    return {
        "refine_id": uuid.uuid4().hex[:10],
        "refined": refined,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
