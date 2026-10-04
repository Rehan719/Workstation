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

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/law", tags=["law"])

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
        "permitted disclosures, duration (3 years), remedies, governing law (England & Wales), "
        "and signature blocks. Mark all customisable fields with [SQUARE BRACKETS]."
    ),
    "employment_contract": (
        "Draft a compliant employment contract under English law (Employment Rights Act 1996). "
        "Include: job title, remuneration, hours, holiday entitlement (28 days statutory), "
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
        "Draft a GDPR-compliant Privacy Policy for a UK-based digital service. "
        "Include: data controller details, legal basis for processing, data categories collected, "
        "retention periods, data subject rights (access, erasure, portability), "
        "third-party sharing, cookies, and ICO contact details. "
        "Mark customisable fields with [SQUARE BRACKETS]."
    ),
    "et1_claim": (
        "Draft a detailed Employment Tribunal ET1 claim form. "
        "Include: claimant and respondent details, grounds of claim (unfair dismissal / discrimination), "
        "timeline of events, remedy sought (reinstatement / compensation), "
        "and a compelling particulars of claim section. Mark with [SQUARE BRACKETS] where user input needed."
    ),
}


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
        f"You are a senior {req.jurisdiction} solicitor specialising in {req.document_type} law. "
        f"Analyse the following legal document.\n\n"
        f"Document type: {req.document_type}\n"
        f"Jurisdiction: {req.jurisdiction}\n"
        f"Analysis focus: {req.analysis_focus}\n\n"
        f"DOCUMENT:\n{req.document_text[:8000]}\n\n"
        f"{focus_instruction}\n\n"
        "Structure your analysis with these sections:\n"
        "## Executive Summary\n"
        "## Key Clauses (table: Clause | Assessment | Risk Level)\n"
        "## Legal Risks (numbered list with severity: HIGH/MEDIUM/LOW)\n"
        "## Missing Provisions\n"
        "## Recommendations\n"
        "## Red Flags (if any)\n\n"
        "Be specific, cite clause numbers where present. Use plain English where possible."
    )

    analysis, provenance = await ai_text(prompt, "law_analyst", realm=req.realm)

    return {
        "analysis_id": uuid.uuid4().hex[:10],
        "document_type": req.document_type,
        "jurisdiction": req.jurisdiction,
        "analysis_focus": req.analysis_focus,
        "analysis": analysis,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
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
        f"You are a senior {req.jurisdiction} solicitor specialising in {req.area_of_law} law. "
        f"Research and analyse the following legal question using the IRAC method.\n\n"
        f"Question: {req.question}\nJurisdiction: {req.jurisdiction}\nArea of law: {req.area_of_law}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + "\nStructure your analysis with these sections:\n"
        "## Issue (the precise legal question(s) at stake)\n"
        "## Relevant Law (the statutes, regulations, and established legal principles that apply — name them specifically)\n"
        "## Application (apply the law to the facts; reason through both sides)\n"
        "## Conclusion (the most likely position, with a confidence level)\n"
        "## Practical Considerations (steps to take, evidence needed, any time limits / limitation periods)\n"
        "## Risks & Caveats\n"
        "## Recommended Next Steps\n\n"
        "Name real statutes / legal principles where applicable. Use plain English. Where the law is uncertain "
        "or fact-dependent, say so honestly rather than overstating certainty."
    )

    analysis, provenance = await ai_text(prompt, "law_researcher", realm=req.realm)

    return {
        "research_id": uuid.uuid4().hex[:10],
        "question": req.question,
        "jurisdiction": req.jurisdiction,
        "area_of_law": req.area_of_law,
        "analysis": analysis,
        "method": "IRAC",
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
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

    document, provenance = await ai_text(prompt, "law_generator", realm=req.realm)

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
        "disclaimer": (
            "This document is AI-generated and provided as a starting point only. "
            "It must be reviewed by a qualified solicitor before use."
        ),
    }
