"""
Law Domain API — Legal document analysis and generation.

  POST /api/v1/law/analyse       — analyse a contract or legal document (AI)
  POST /api/v1/law/generate      — generate a legal document from a template
  GET  /api/v1/law/templates     — list available legal document templates
"""
from __future__ import annotations

import json as _json
import pathlib as _pathlib
import time
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.auth.core import get_current_user, require_admin
from pydantic import BaseModel

import functools

from agentic_core.api._ai_provenance import ai_text as _ai_text, person_said, disclaimer_for
from agentic_core.api._ai_provenance import MATERIAL_SLOT      # W680 - a person's material travels as marked data

#  W637 (FU-597) — this router's domain, bound once. Every ai_text call below carries it, so the native floor
#  prints the real domain instead of "the request named no domain".
ai_text = functools.partial(_ai_text, domain="law")
DOCUMENT_LIMIT = 8000          # how much of a pasted document is handed over; the rest is SAID to be unread

router = APIRouter(prefix="/api/v1/law", tags=["law"])

#  W627 (FU-536) - the floor's disclaimer says what the floor did, which was no legal research at all
_FLOOR_LAW = ("Composed by the native floor, not by a model: NO legal research or analysis was performed, no law "
              "was looked up, and the 'Relevant Law' and 'Conclusion' headings hold terms from your question. "
              "It is not legal advice - consult a qualified solicitor.")

_TEMPLATES = [
    {"id": "nda", "name": "Non-Disclosure Agreement", "category": "Contracts", "jurisdiction": "England & Wales"},
    {"id": "employment_contract", "name": "Employment Contract", "category": "Employment", "jurisdiction": "England & Wales"},
    {"id": "service_agreement", "name": "Service Level Agreement", "category": "Contracts", "jurisdiction": "England & Wales"},
    {"id": "partnership_deed", "name": "Partnership Deed", "category": "Governance", "jurisdiction": "England & Wales"},
    {"id": "privacy_policy", "name": "Privacy Policy (GDPR)", "category": "Compliance", "jurisdiction": "UK GDPR"},
    {"id": "terms_of_service", "name": "Terms of Service", "category": "Compliance", "jurisdiction": "England & Wales"},
    {"id": "ip_assignment", "name": "IP Assignment Agreement", "category": "Intellectual Property", "jurisdiction": "England & Wales"},
    {"id": "et1_claim", "name": "Employment Tribunal ET1 Claim", "category": "Litigation", "jurisdiction": "England & Wales"},
    {"id": "cease_desist", "name": "Cease and Desist Letter", "category": "Litigation", "jurisdiction": "England & Wales"},
    {"id": "data_processing_agreement", "name": "Data Processing Agreement", "category": "Compliance", "jurisdiction": "UK GDPR"},
]

_TEMPLATE_PROMPTS: dict[str, str] = {
    "nda": (
        "Draft a legally sound Non-Disclosure Agreement (NDA) under English law. "
        "Include: parties, recitals, definition of confidential information, obligations, "
        "permitted disclosures, duration (a field the parties fill), remedies, governing law (England & Wales), "
        "and signature blocks. Mark all customisable fields with [SQUARE BRACKETS]."
    ),
    "employment_contract": (
        "Draft an employment contract under English law. "
        "Include: job title, remuneration, hours, holiday entitlement (leave the figure as a field and say "
        "the current statutory minimum must be checked at the official source), "
        "notice periods, IP ownership, restrictive covenants, disciplinary procedure reference, "
        "and governing law. Mark all customisable fields with [SQUARE BRACKETS]."
    ),
    "service_agreement": (
        "Draft a Service Level Agreement (SLA) under English law. "
        "Include: services scope, service levels (uptime, response times), "
        "payment terms, IP ownership, liability cap, termination provisions, "
        "and dispute resolution. Mark customisable fields with [SQUARE BRACKETS]."
    ),
    "privacy_policy": (
        "Draft a Privacy Policy for a UK-based digital service that addresses the UK GDPR's notice "
        "requirements; do not describe the draft as compliant. "
        "Include: data controller details, legal basis for processing, data categories collected, "
        "retention periods, data subject rights (access, erasure, portability), "
        "third-party sharing, cookies, and ICO contact details. "
        "Mark customisable fields with [SQUARE BRACKETS]."
    ),
    #  the tribunal claim's prompt stood here. It chose the grounds and asked for a persuasive particulars
    #  section from nothing; the template is assembled by the clerk and refused by this generator.
}


class ParticularSpec(BaseModel):
    """P3.30 (ledger v16 R5.12) - ONE PARTICULAR: what it is called and the words a bundle line must carry.
    The field was an untyped list, so a particular sent as plain text reached the specialist's `.get()` and
    the route answered 500. Typed, a wrong shape is refused by the contract with a 422 that names the field.
    Both fields keep the defaults the specialist already tolerated (no name, no words -> a BLANK)."""
    name: str = ""
    words: list[str] = []


class AssembleRequest(BaseModel):
    template_id: str
    particulars: list[ParticularSpec] = []   # each filled ONLY from a located bundle line
    authorities: list = []        # names of statutes or cases - each resolved against the corpus or refused


@router.post("/matter/assemble")
async def matter_assemble(req: AssembleRequest, user: dict | None = Depends(get_current_user)):
    """P3.23 / FU-278 — the legal specialist ASSEMBLES: every particular comes from a located line of a document in
    the one named folder (with its document and line), or is a BLANK; every authority is resolved against the
    corpus or refused; a filing-shaped artefact is a draft until the Owner approves it. Not legal advice."""
    from agentic_core.legal import specialist
    #  the specialist is handed the plain dicts it has always read; its code is unchanged
    return specialist.assemble(req.template_id, [p.model_dump() for p in req.particulars], req.authorities)


@router.post("/matter/artefacts/{artefact_id}/approve")
async def matter_approve(artefact_id: str, admin: dict = Depends(require_admin)):
    """The Owner's approval of a filing-shaped artefact - the human gate the ruling of 2026-10-03c requires."""
    from agentic_core.legal import specialist
    res = specialist.approve(artefact_id, by=str(admin.get("username") or "owner"))
    if not res["approved"]:
        raise HTTPException(status_code=404 if res["refused"] == "not_found" else 409, detail=res)
    return res


@router.get("/bundle")
async def matter_bundle():
    """P3.23 (W605) — the live matter's ONE named folder: its state, whether indexing may start (MEASURED from
    the folder, never stored), and how many documents it holds. Never a document's contents, and nothing about
    the matter leaves this machine."""
    from agentic_core.legal import bundle as _bundle
    return _bundle.status()


@router.get("/templates")
async def list_templates():
    """Return available legal document templates."""
    return {"templates": _TEMPLATES, "total": len(_TEMPLATES),
            #  Each template's own `jurisdiction` says what that template is FOR, which is legitimately
            #  per-template. THE MATTER's jurisdiction is a different fact with one home and a basis,
            #  published here so a reader can see which is which and where the second came from.
            "matter_jurisdiction": _MATTER_JURISDICTION,
            "matter_jurisdiction_basis": _MATTER_JURISDICTION_BASIS}


#  THE MATTER'S JURISDICTION HAS ONE HOME, WITH ITS BASIS. It was a typed literal here and in ten
#  templates below, with no source anywhere — the same class W565 removed from the suite constant. It is
#  now read from agentic_core/legal/matter.json, which records how it was established: inferred from this
#  repository's own corpus (ACAS and "Employment Tribunal" rule Northern Ireland out) and confirmed by the
#  Owner. The load never raises: a missing or malformed file leaves the previous literal as the default and
#  says so, because a request default is not the place to discover a configuration error.
_MATTER_FILE = _pathlib.Path(__file__).resolve().parents[1] / "legal" / "matter.json"


def matter_jurisdiction() -> tuple:
    """(jurisdiction, basis). Never raises, and NEVER guesses — the fallback is named as a fallback."""
    try:
        _m = _json.loads(_MATTER_FILE.read_text(encoding="utf-8"))
        _j = str(_m.get("jurisdiction") or "").strip()
        if _j:
            return _j, str(_m.get("jurisdiction_basis") or "").strip() or "no basis recorded in matter.json"
        return ("England & Wales",
                "FALLBACK: matter.json records no jurisdiction. This is the historical literal, not a "
                "measurement, and it must not be read as one")
    except Exception as _e:                      # noqa: BLE001 — a config error is not a request error
        return ("England & Wales",
                f"FALLBACK: matter.json could not be read ({type(_e).__name__}). This is the historical "
                f"literal, not a measurement, and it must not be read as one")


_MATTER_JURISDICTION, _MATTER_JURISDICTION_BASIS = matter_jurisdiction()


class AnalyseRequest(BaseModel):
    document_text: str
    document_type: str = "contract"
    jurisdiction: str = _MATTER_JURISDICTION
    analysis_focus: str = "general"  # general | risk | compliance | negotiation
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/analyse")
async def analyse_document(req: AnalyseRequest):
    """
    Analyse a legal document using AI. Returns structured risk assessment,
    key clauses summary, and recommendations.
    """
    focus_instruction = {
        "general": "Provide a comprehensive analysis covering all key aspects.",
        "risk": "Focus on identifying legal risks, unfavourable clauses, and liability exposure.",
        "compliance": "Focus on regulatory compliance issues, especially GDPR, employment law, and consumer protection.",
        "negotiation": "Identify clauses that are negotiable, unfavourable positions, and suggested counterproposals.",
    }.get(req.analysis_focus, "Provide a comprehensive analysis covering all key aspects.")

    prompt = (
        f"Analyse the following {req.document_type} document as it reads under {req.jurisdiction} law. "
        f"Claim no professional role. Give no probability, forecast or confidence figure.\n\n"
        f"Document type: {req.document_type}\n"
        f"Jurisdiction: {req.jurisdiction}\n"
        f"Analysis focus: {req.analysis_focus}\n\n"
        + MATERIAL_SLOT + "\n\n"
        + f"{focus_instruction}\n\n"
        "Structure your analysis with these sections:\n"
        "## Executive Summary\n"
        "## Key Clauses (table: Clause | Assessment | Risk Level)\n"
        "## Legal Risks (numbered list with severity: HIGH/MEDIUM/LOW)\n"
        "## Missing Provisions\n"
        "## Recommendations\n"
        "## Red Flags (if any)\n\n"
        "Be specific, cite clause numbers where present. Use plain English where possible."
    )

    #  W680 - the document is handed to the helper as MATERIAL: marked as data, cut there and the cut RECORDED.
    #  It was cut at 8,000 characters inside the instruction and the analysis said nothing of it.
    analysis, provenance = await ai_text(prompt, "law_analyst", realm=req.realm,
        user_text=person_said(req.analysis_focus),
        material=req.document_text, material_label="DOCUMENT", material_limit=DOCUMENT_LIMIT)
    _mat = (provenance or {}).get("material") or {}
    if _mat and not _mat.get("read_whole"):
        #  said in the TEXT, so it travels with a copy, a download and a saved version
        analysis = ((analysis + "\n\n") if analysis else "") + (
            f"_ONLY PART OF THE DOCUMENT WAS READ: the first {_mat.get('read_chars'):,} of {_mat.get('chars'):,} "
            f"characters. Nothing here speaks for the rest - a clause, a schedule or a signature block beyond "
            f"that point was not read. Analyse the document in parts._")

    return {
        "analysis_id": uuid.uuid4().hex[:10],
        "document_type": req.document_type,
        "jurisdiction": req.jurisdiction,
        "analysis_focus": req.analysis_focus,
        "analysis": analysis,
        "document_read": {k: _mat.get(k) for k in ("chars", "read_chars", "read_whole", "basis")} if _mat else None,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #  W627 (FU-536) - "AI-generated" analysis is not what the floor produced
        "disclaimer": (_FLOOR_LAW if provenance.get("floor_note") else
            "This analysis is AI-generated for informational purposes only. "
            "It does not constitute legal advice. Consult a qualified solicitor for legal matters."
        ),
    }


class ResearchRequest(BaseModel):
    question: str
    jurisdiction: str = "England & Wales"
    area_of_law: str = "general"   # contract | employment | IP | data protection | dispute | company | ...
    context: str = ""
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/research")
async def legal_research(req: ResearchRequest):
    """Structured legal research / issue analysis using the IRAC method (Issue → Relevant Law → Application →
    Conclusion) with practical considerations, risks, and next steps. AI-generated informational guidance —
    NOT legal advice."""
    prompt = (
        f"Set out the following {req.area_of_law} question under {req.jurisdiction} law using the IRAC "
        f"method. Claim no professional role.\n\n"
        f"Question: {req.question}\nJurisdiction: {req.jurisdiction}\nArea of law: {req.area_of_law}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + "\nStructure your analysis with these sections:\n"
        "## Issue (the precise legal question(s) at stake)\n"
        "## Relevant Law (the statutes, regulations, and established legal principles that apply — name them specifically)\n"
        "## Application (apply the law to the facts; reason through both sides)\n"
        "## Conclusion (what the sources named above support and what they do not settle; give no "
        "probability, forecast or confidence figure, and do not say what a court or tribunal would decide)\n"
        "## Practical Considerations (steps to take, evidence needed, any time limits / limitation periods)\n"
        "## Risks & Caveats\n"
        "## Recommended Next Steps\n\n"
        "Name a statute or case ONLY if you can give its exact title; if you are not certain it exists and "
        "is in force, say that it must be checked and do not name it. Use plain English. Where the law is "
        "uncertain or fact-dependent, say so. Where a time limit may apply, say that one may and that it "
        "must be checked today at the official source - never state a period from memory."
    )

    analysis, provenance = await ai_text(prompt, "law_researcher", realm=req.realm,
        user_text=person_said(req.question))

    return {
        "research_id": uuid.uuid4().hex[:10],
        "question": req.question,
        "jurisdiction": req.jurisdiction,
        "area_of_law": req.area_of_law,
        "analysis": analysis,
        "method": "IRAC",
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (_FLOOR_LAW if provenance.get("floor_note") else
            "This legal research is AI-generated for informational purposes only and does NOT constitute "
            "legal advice. Laws change and outcomes are fact-specific — consult a qualified solicitor."
        ),
    }


class GenerateRequest(BaseModel):
    template_id: str
    parties: dict = {}
    custom_instructions: str = ""
    jurisdiction: str = "England & Wales"
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/generate")
async def generate_document(req: GenerateRequest):
    """
    Generate a legal document from a template using AI.
    Returns the full document text in Markdown format.
    """
    #  OWNER RULING 2026-10-12 - A FILING-SHAPED DOCUMENT HAS ONE DOOR. The clerk fills such a document only
    #  from located lines, refuses an authority it does not hold and keeps the result a draft until the Owner
    #  approves it. This generator had none of that and wrote one from a prompt. It refuses, and names the door.
    from agentic_core.legal.specialist import FILING_SHAPED as _filing_shaped
    if req.template_id in _filing_shaped:
        raise HTTPException(status_code=409, detail=(
            f"'{req.template_id}' is a filing-shaped document and is not generated here. It is assembled by "
            f"the clerk at POST /api/v1/law/matter/assemble: every particular comes from a located line of a "
            f"document or is left blank, every authority is resolved or refused, and the result is a draft "
            f"until it is approved. Nothing here is legal advice."))
    base_prompt = _TEMPLATE_PROMPTS.get(
        req.template_id,
        f"Draft a comprehensive {req.template_id.replace('_', ' ')} agreement under {req.jurisdiction} law. "
        "Include all standard clauses, mark customisable fields with [SQUARE BRACKETS]."
    )

    parties_context = ""
    if req.parties:
        parties_context = f"\nParties: {req.parties}\n"

    prompt = (
        f"{base_prompt}\n"
        f"Jurisdiction: {req.jurisdiction}\n"
        + parties_context
        + (f"Additional instructions: {req.custom_instructions}\n" if req.custom_instructions else "")
        + "\nGenerate the complete legal document now in Markdown format with proper headings and clause numbering."
    )

    #  P3.30 (ledger v15 R5[8]) - THE PARTY NAMES ARE THE PERSON'S WORDS TOO. Only the instructions were named,
    #  so a request carrying parties and no instructions told the floor that nothing had been said. The VALUES
    #  the person typed are passed, one per line; person_said drops anything that is not a string, so a nested
    #  object is never stringified into words nobody wrote. The keys are form labels and are not passed.
    document, provenance = await ai_text(prompt, "law_generator", realm=req.realm,
        user_text=person_said(req.custom_instructions, list((req.parties or {}).values())))

    template_name = next(
        (t["name"] for t in _TEMPLATES if t["id"] == req.template_id),
        req.template_id.replace("_", " ").title(),
    )

    return {
        "document_id": uuid.uuid4().hex[:10],
        "template_id": req.template_id,
        "template_name": template_name,
        "jurisdiction": req.jurisdiction,
        "document": document,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": disclaimer_for(
            provenance, "This document is AI-generated and provided as a starting point only.",
            "It must be reviewed by a qualified solicitor before use. "
            #  P3.23 — the not-legal-advice statement is on EVERY response a person reads, not only the matter's
            "Nothing here is legal advice."),
    }
