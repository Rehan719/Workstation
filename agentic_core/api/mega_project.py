"""
Mega-Project Synthesis API — surfaces the `agentic_core.mega_project` capability into the in-house
pipeline, REDONE honestly. The original `MegaProjectSynthesizer` returned hardcoded, fabricated
figures (a fixed "$1.5T valuation / 450% ROI / 98.5% Monte-Carlo confidence") — a violation of the
never-fabricate rule. This endpoint instead produces investor-grade deliverables for a large concept
on Workstation's OWN native fabric (`gateway.query_meta`), grounded in the concept, with in-house
provenance and no invented numbers.

  GET  /api/v1/mega-project/sections    — the deliverable section structure
  POST /api/v1/mega-project/synthesise  — synthesise the deliverables on the native fabric
"""
from __future__ import annotations

import time
import uuid
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/mega-project", tags=["mega-project"])

_SECTIONS = ["Executive Summary", "Business Plan", "Market & Opportunity", "Feasibility Study",
             "Capital Plan", "Roadmap", "Risks & Mitigations"]


@router.get("/sections")
async def sections():
    return {"sections": _SECTIONS, "posture": "in-house-first"}


class SynthesiseRequest(BaseModel):
    concept: str
    domain: str = "enterprise"


@router.post("/synthesise")
async def synthesise(req: SynthesiseRequest):
    """Synthesise investor-grade mega-project deliverables on the native fabric (no fabricated
    numbers — figures are framed as to-be-modelled, grounded in the concept)."""
    prompt = (
        "You are the Mega-Project Synthesis Engine. Produce honest, investor-grade deliverables for a "
        "large-scale concept. Do NOT invent specific figures — frame valuations, ROI and confidence as "
        "to-be-modelled with the method to derive them.\n\n"
        f"Concept: {req.concept}\nDomain: {req.domain}\n\n"
        + "\n".join(f"## {s}" for s in _SECTIONS)
    )
    text, provenance = await ai_text(prompt, "mega_project", timeout=40.0)
    return {
        "synthesis_id": f"mega-{uuid.uuid4().hex[:8]}",
        "concept": req.concept,
        "domain": req.domain,
        "sections": _SECTIONS,
        "deliverable": text,
        "ai_provenance": provenance,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
