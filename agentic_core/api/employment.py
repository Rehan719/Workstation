"""
Employment Domain API — career development tools, brought to parity with the other domains
(Law/Science/Care/Education/Religion). Clean string/list inputs (no file uploads), every AI-mediated
response served on Workstation's OWN native fabric with honest in-house provenance.

  GET  /api/v1/employment/services       — list the employment tools
  POST /api/v1/employment/cv             — tailor a CV / résumé to a target role
  POST /api/v1/employment/cover-letter   — draft a tailored cover letter
  POST /api/v1/employment/interview-prep — prepare for an interview (likely questions + STAR prep)
  POST /api/v1/employment/career-path    — map a development roadmap from current → target role
"""
from __future__ import annotations

import time
import uuid
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/employment", tags=["employment"])

_SERVICES = [
    {"id": "cv", "name": "CV / Résumé Tailoring", "description": "Tailor a CV to a target role with achievement-led, ATS-friendly bullet points."},
    {"id": "cover_letter", "name": "Cover Letter", "description": "Draft a focused, tailored cover letter for a specific role and employer."},
    {"id": "interview_prep", "name": "Interview Preparation", "description": "Likely questions plus STAR-method answer frameworks for the role."},
    {"id": "career_path", "name": "Career Path & Skills Gap", "description": "A development roadmap and skills-gap analysis from current to target role."},
    {"id": "application", "name": "Application Form & Supporting Statement", "description": "Address a person specification point-by-point and draft answers to application-form questions."},
    {"id": "salary_negotiation", "name": "Salary & Offer Negotiation", "description": "A compensation strategy: market positioning, a target range, scripts, non-salary levers, BATNA and etiquette."},
]


@router.get("/services")
async def list_services():
    return {"services": _SERVICES, "total": len(_SERVICES)}


# ── CV / résumé tailoring ──────────────────────────────────────────────────────
class CVRequest(BaseModel):
    target_role: str
    experience: str                      # free-text career/experience summary
    skills: List[str] = []
    seniority: str = "mid"               # entry | mid | senior | lead | executive


@router.post("/cv")
async def tailor_cv(req: CVRequest):
    skills_text = ("Key skills: " + ", ".join(req.skills) + "\n") if req.skills else ""
    prompt = (
        "You are an expert CV writer and career coach. Tailor a CV to the target role using "
        "achievement-led, ATS-friendly bullet points (strong action verbs, quantified impact).\n\n"
        f"Target role: {req.target_role}\n"
        f"Seniority: {req.seniority}\n"
        f"{skills_text}"
        f"Candidate experience:\n{req.experience}\n\n"
        "Produce:\n"
        "## Professional Summary (3-4 lines positioned for the target role)\n"
        "## Core Skills (a focused, role-relevant list)\n"
        "## Experience (rewrite the candidate's experience as achievement-led bullets, quantified where possible)\n"
        "## Suggested Keywords (ATS terms to include for this role)\n"
        "## Gaps & Recommendations (honest gaps for this role and how to address them)"
    )
    cv, provenance = await ai_text(prompt, "employment_cv")
    return {
        "cv_id": uuid.uuid4().hex[:10],
        "target_role": req.target_role,
        "seniority": req.seniority,
        "cv": cv,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Cover letter ───────────────────────────────────────────────────────────────
class CoverLetterRequest(BaseModel):
    target_role: str
    company: str = ""
    highlights: str = ""                 # what to emphasise (achievements / motivation)
    tone: str = "professional"           # professional | warm | concise | enthusiastic


@router.post("/cover-letter")
async def cover_letter(req: CoverLetterRequest):
    company_text = f"Company: {req.company}\n" if req.company else ""
    highlights_text = f"Emphasise: {req.highlights}\n" if req.highlights else ""
    prompt = (
        "You are an expert cover-letter writer. Draft a focused, tailored cover letter.\n\n"
        f"Target role: {req.target_role}\n"
        f"{company_text}{highlights_text}"
        f"Tone: {req.tone}\n\n"
        "Produce a complete cover letter (3-4 short paragraphs): a strong opening tied to the role, "
        "a body evidencing fit with concrete examples, a paragraph on motivation/fit with the employer, "
        "and a confident close. Avoid clichés and generic filler."
    )
    letter, provenance = await ai_text(prompt, "employment_cover_letter")
    return {
        "letter_id": uuid.uuid4().hex[:10],
        "target_role": req.target_role,
        "company": req.company,
        "cover_letter": letter,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Interview preparation ──────────────────────────────────────────────────────
class InterviewPrepRequest(BaseModel):
    target_role: str
    seniority: str = "mid"
    competencies: List[str] = []         # competencies / themes to prepare for


@router.post("/interview-prep")
async def interview_prep(req: InterviewPrepRequest):
    comp_text = ("Focus competencies: " + ", ".join(req.competencies) + "\n") if req.competencies else ""
    prompt = (
        "You are an experienced interview coach. Prepare a candidate for an interview.\n\n"
        f"Target role: {req.target_role}\n"
        f"Seniority: {req.seniority}\n"
        f"{comp_text}\n"
        "Produce:\n"
        "## Likely Questions (8-10, mixing behavioural, technical/role-specific, and situational)\n"
        "## STAR Frameworks (for 3 key behavioural questions, give a Situation-Task-Action-Result scaffold)\n"
        "## Questions to Ask the Interviewer (5 thoughtful questions)\n"
        "## Red Flags to Avoid\n"
        "## Preparation Checklist"
    )
    prep, provenance = await ai_text(prompt, "employment_interview")
    return {
        "prep_id": uuid.uuid4().hex[:10],
        "target_role": req.target_role,
        "seniority": req.seniority,
        "prep": prep,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Career path / skills gap ───────────────────────────────────────────────────
class CareerPathRequest(BaseModel):
    current_role: str
    target_role: str
    experience_years: int = 3
    constraints: str = ""                # e.g. "part-time study only, 12-month horizon"


@router.post("/career-path")
async def career_path(req: CareerPathRequest):
    constraints_text = f"Constraints: {req.constraints}\n" if req.constraints else ""
    prompt = (
        "You are a career strategist. Map a realistic development roadmap and skills-gap analysis.\n\n"
        f"Current role: {req.current_role}\n"
        f"Target role: {req.target_role}\n"
        f"Experience: {req.experience_years} years\n"
        f"{constraints_text}\n"
        "Produce:\n"
        "## Skills Gap (skills/experience the target role needs that the candidate likely lacks)\n"
        "## Roadmap (sequenced milestones with realistic timeframes from current → target)\n"
        "## Learning & Credentials (specific courses, certifications, or experiences to pursue)\n"
        "## Quick Wins (things achievable in the next 90 days)\n"
        "## Risks & Honest Assessment (how realistic the transition is, and key dependencies)"
    )
    roadmap, provenance = await ai_text(prompt, "employment_career_path")
    return {
        "path_id": uuid.uuid4().hex[:10],
        "current_role": req.current_role,
        "target_role": req.target_role,
        "roadmap": roadmap,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Salary & offer negotiation ─────────────────────────────────────────────────
class SalaryNegotiationRequest(BaseModel):
    target_role: str
    location: str = ""
    seniority: str = "mid"               # entry | mid | senior | lead | executive
    experience_years: int = 3
    current_salary: str = ""             # free text, e.g. "£45,000" or "not disclosed"
    offered_salary: str = ""             # the offer on the table, if any
    leverage: str = ""                   # competing offers, scarce skills, strong performance, etc.


@router.post("/salary-negotiation")
async def salary_negotiation(req: SalaryNegotiationRequest):
    """Compensation & offer-negotiation strategist: a structured plan — market positioning, a target range
    with justification, anchoring scripts, non-salary levers, BATNA and etiquette. Reasoned guidance based on
    typical market structure — NOT live salary data; verify figures against current sources."""
    details = "".join([
        f"Location: {req.location}\n" if req.location else "",
        f"Current salary: {req.current_salary}\n" if req.current_salary else "",
        f"Offer on the table: {req.offered_salary}\n" if req.offered_salary else "",
        f"Leverage: {req.leverage}\n" if req.leverage else "",
    ])
    prompt = (
        "You are an experienced compensation and negotiation coach. Build a practical, ethical salary / "
        "offer negotiation strategy for the candidate.\n\n"
        f"Target role: {req.target_role}\nSeniority: {req.seniority}\nExperience: {req.experience_years} years\n"
        f"{details}\n"
        "Produce:\n"
        "## Market Positioning (how this role/seniority/location typically sits — be explicit that this is "
        "reasoned from typical market structure, NOT live data, and that they should verify against current sources)\n"
        "## Target Range (walk-away, target, and stretch figures, each with brief reasoning)\n"
        "## Justification Points (the evidence to support the ask — impact, scarcity, market, leverage)\n"
        "## Negotiation Scripts (concrete wording: opening the conversation, countering an offer, holding firm, closing)\n"
        "## Non-Salary Levers (benefits, equity, bonus, flexibility, title, start date, early review)\n"
        "## BATNA & Walk-Away (best alternative; the point at which to decline)\n"
        "## Etiquette & Risks (how to negotiate firmly without damaging the relationship)\n\n"
        "Be specific and practical. Never fabricate precise market figures as if they were data — frame ranges "
        "as reasoned estimates to validate."
    )
    plan, provenance = await ai_text(prompt, "employment_salary")
    return {
        "negotiation_id": uuid.uuid4().hex[:10],
        "target_role": req.target_role,
        "seniority": req.seniority,
        "plan": plan,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": ("Reasoned negotiation guidance, not live salary data or financial advice — verify "
                       "figures against current market sources for your role and location."),
    }


# ── Application form & supporting statement ────────────────────────────────────
class ApplicationRequest(BaseModel):
    target_role: str
    person_spec: str = ""                # the job's person specification / selection criteria
    experience: str = ""                 # candidate's relevant experience/evidence
    questions: List[str] = []            # specific application-form questions to answer
    word_limit: int = 0                  # 0 = no explicit limit
    organisation: str = ""


@router.post("/application")
async def application_support(req: ApplicationRequest):
    """Draft a supporting statement that addresses the person specification criterion-by-criterion
    with evidence, plus tailored answers to any application-form questions."""
    org_text = f"Organisation: {req.organisation}\n" if req.organisation else ""
    spec_text = (f"Person specification / selection criteria:\n{req.person_spec}\n\n"
                 if req.person_spec else "")
    exp_text = f"Candidate experience and evidence:\n{req.experience}\n\n" if req.experience else ""
    limit_text = (f"Keep the supporting statement within roughly {req.word_limit} words.\n"
                  if req.word_limit and req.word_limit > 0 else "")
    if req.questions:
        questions_block = ("## Application Question Answers\n"
                           "Draft a strong, evidence-based answer to each question below:\n"
                           + "\n".join(f"  {i+1}. {q}" for i, q in enumerate(req.questions)) + "\n\n")
    else:
        questions_block = ""

    prompt = (
        "You are an expert job-application coach (UK public sector, NHS, charity and graduate schemes). "
        "Help the candidate write a compelling, HONEST application.\n\n"
        f"Target role: {req.target_role}\n"
        f"{org_text}{spec_text}{exp_text}{limit_text}\n"
        "Produce:\n"
        "## Supporting Statement\n"
        "Address each essential and desirable criterion from the person specification in turn, evidencing "
        "it with concrete, STAR-structured examples from the candidate's experience. If a criterion has no "
        "clear evidence, say so honestly and suggest the closest transferable evidence — never invent "
        "experience the candidate does not have.\n\n"
        f"{questions_block}"
        "## Criteria Coverage Check\n"
        "A short checklist of which person-spec criteria are well-evidenced, partially evidenced, or a gap."
    )
    statement, provenance = await ai_text(prompt, "employment_application")
    return {
        "application_id": uuid.uuid4().hex[:10],
        "target_role": req.target_role,
        "organisation": req.organisation,
        "questions_answered": len(req.questions),
        "statement": statement,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
