"""
Career Domain API — Employment domain endpoints for Application Studio.

  POST /api/v1/career/uploads/auto   — classify uploaded file into a career category
  POST /api/v1/career/generate       — generate career documents (CV, cover letter, etc.)
  POST /api/v1/career/job-search     — AI-synthesized job listings based on profile
  POST /api/v1/career/job-search/use — mark a job listing as applied-to
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/career", tags=["career"])

# ── Auto-classify upload ──────────────────────────────────────────────────────

_CATEGORIES = [
    "cv_history", "past_applications", "star_examples", "job_ad",
    "job_description", "person_spec", "application_guidance", "interview_prep_materials",
]


@router.post("/uploads/auto")
async def auto_classify_upload(file: UploadFile = File(...)):
    """
    Classify an uploaded file into a career input category using AI.
    Returns: {filename, classification: {category, confidence, reasoning}}
    """
    content = await file.read()
    # Extract text preview (up to 2KB)
    try:
        text_preview = content[:2000].decode("utf-8", errors="ignore")
    except Exception:
        text_preview = file.filename or ""

    prompt = (
        "You are a career document classifier. Given a filename and document preview, "
        "classify it into exactly one of these categories:\n"
        f"{json.dumps(_CATEGORIES)}\n\n"
        f"Filename: {file.filename}\n"
        f"Content preview (first 2000 chars):\n{text_preview}\n\n"
        "Respond with a JSON object: "
        '{"category": "<one of the above>", "confidence": <float 0-1>, "reasoning": "<one sentence>"}'
        "\nOnly output valid JSON. Do not add any other text."
    )

    result, provenance = await ai_text(prompt, "career_classifier")

    # W489 (sweep S12.1, C3) — A DOCUMENT NOBODY CLASSIFIED IS NOT FILED AS IF SOMEBODY HAD.
    # This block invented three readings. On the native floor the reply is not JSON, so the `except`
    # branch hard-coded category="cv_history" and confidence=0.7 — and the page then told the user
    # '"person_spec.txt" classified as Old CVs (70% confidence)' beneath a line promising the content
    # had been analysed. Nothing had been read: the 70% was a literal, and the file was really filed
    # under CV history, so the invented label went on to shape every later /career/generate prompt.
    # A missing or unknown category was coerced to cv_history the same way, and a reply carrying no
    # confidence at all was given 0.85. Now: no classification means 'uncategorized' (a category the
    # page already handles, listing those files as Unresolved) and a confidence of None — absent,
    # because absent is what it is. A number is only reported when the model actually returned one.
    try:
        # Strip markdown fences if present
        clean = result.strip().strip("```json").strip("```").strip()
        data = json.loads(clean)
        category = data.get("category") or "uncategorized"
        if category not in _CATEGORIES:
            category = "uncategorized"
        conf_raw = data.get("confidence")
        confidence = (float(conf_raw) if isinstance(conf_raw, (int, float))
                      and not isinstance(conf_raw, bool) else None)
        reasoning = data.get("reasoning") or (
            "The classifier returned a category with no reasoning." if confidence is not None else
            "The classifier named a category but gave no confidence, so none is reported.")
        if category == "uncategorized":
            confidence = None
            reasoning = "No category was returned that matches the filing categories — nothing was classified."
    except Exception:
        category = "uncategorized"
        confidence = None
        reasoning = ("The classifier's reply could not be read as a classification, so nothing was "
                     "classified — this file is filed as uncategorized, not under a guessed category.")

    # Store the file via ingestion manager
    from agentic_core.ingestion.api import ingestion_manager
    import io
    file.file = io.BytesIO(content)
    file.filename = file.filename
    stored = await ingestion_manager.ingest_file(file, category=category)

    return {
        "filename": file.filename,
        "file_id": stored["file_id"],
        "classification": {
            "category": category,
            "confidence": confidence,
            "reasoning": reasoning,
        },
        "ai_provenance": provenance,
    }


# ── Generate career documents ─────────────────────────────────────────────────

_OUTPUT_PROMPTS: dict[str, str] = {
    "cv": (
        "Generate a professional, ATS-optimised CV in Markdown format. "
        "Structure: Professional Summary, Core Competencies (skills grid), "
        "Work Experience (reverse chronological, with STAR-style bullets), "
        "Education, Certifications. Tailor it tightly to the target role."
    ),
    "cover_letter": (
        "Write a compelling, personalised cover letter (3-4 paragraphs). "
        "Opening: hook tied to the company's mission. "
        "Middle: 2 concrete achievements from the candidate's background that match the role requirements. "
        "Closing: clear call to action. Professional but warm tone."
    ),
    "supporting_statement": (
        "Write a supporting statement responding directly to each competency or criterion in the person specification. "
        "Use the STAR (Situation, Task, Action, Result) method for each example. "
        "Provide evidence-based responses. Length: 600-900 words."
    ),
    "application_form": (
        "Draft answers for a standard job application form. "
        "Sections: Why do you want this role? (150 words), "
        "What relevant experience do you bring? (200 words), "
        "Describe a challenge you overcame (STAR, 200 words), "
        "What are your key strengths for this position? (150 words). "
        "Tailor each answer to the specific role."
    ),
    "interview_prep": (
        "Create a comprehensive interview preparation guide. Include: "
        "1. Top 10 likely interview questions with ideal answer frameworks "
        "2. 5 STAR stories mapped to competencies from the job description "
        "3. Questions to ask the interviewer "
        "4. Research points about the company "
        "5. Practical preparation checklist (day before, morning of). "
        "Format clearly with headers and bullet points."
    ),
    "new_job_prep": (
        "Create a 90-day new job preparation plan. Include: "
        "Pre-start (confirm logistics, research company, prepare questions), "
        "Week 1 (listening and learning agenda), "
        "Month 1 (relationship building, quick wins), "
        "Month 2-3 (project delivery, establishing credibility). "
        "Include specific actions for each phase."
    ),
    "in_job_support": (
        "Create an in-job performance and progression guide. Include: "
        "Performance metrics to track, "
        "How to build visibility with leadership, "
        "Skills development roadmap for promotion, "
        "How to handle performance reviews effectively, "
        "Networking and mentoring strategy within the organisation."
    ),
    "linkedin_profile": (
        "Write a compelling LinkedIn profile optimised for the target role. "
        "Sections: Headline (120 chars, keyword-rich), "
        "About (300 words, first-person, achievement-focused), "
        "Featured section suggestions, "
        "Experience bullet points (top 3 roles), "
        "Skills section (top 15 keywords). "
        "Optimise for recruiter search and algorithm."
    ),
}


class GenerateRequest(BaseModel):
    file_ids: list[str] = []
    company_website: str = ""
    linkedin_url: str = ""
    instructions: str = ""
    output_types: list[str]


@router.post("/generate")
async def generate_career_docs(req: GenerateRequest):
    """
    Generate one or more career documents using uploaded file content + AI.
    Returns a list of generated documents.
    """
    if not req.output_types:
        raise HTTPException(status_code=400, detail="At least one output_type required.")

    # Retrieve uploaded file content from ingestion registry
    profile_context = ""
    if req.file_ids:
        try:
            from agentic_core.ingestion.api import ingestion_manager
            registry = ingestion_manager.registry
            for entry in registry:
                if entry.get("file_id") in req.file_ids:
                    text = entry.get("extracted_text", "")
                    category = entry.get("category", "document")
                    if text:
                        profile_context += f"\n[{category.upper()}]\n{text[:600]}\n"
        except Exception:
            pass

    target_context = ""
    if req.company_website:
        target_context += f"Company website: {req.company_website}\n"
    if req.linkedin_url:
        target_context += f"LinkedIn URL: {req.linkedin_url}\n"
    if req.instructions:
        target_context += f"Special instructions: {req.instructions}\n"

    results = []
    for output_type in req.output_types[:8]:  # cap at 8 to avoid rate-limit abuse
        prompt_base = _OUTPUT_PROMPTS.get(
            output_type,
            f"Generate a professional {output_type.replace('_', ' ')} document tailored for the candidate."
        )
        prompt = (
            f"{prompt_base}\n\n"
            + (f"Candidate profile context:\n{profile_context}\n" if profile_context else "")
            + (f"Target role context:\n{target_context}\n" if target_context else "")
            + "\nGenerate the complete document now in Markdown format."
        )

        content, provenance = await ai_text(prompt, "career_generator")
        results.append({
            "output_id": uuid.uuid4().hex[:10],
            "output_type": output_type,
            "title": output_type.replace("_", " ").title(),
            "content": content,
            "ai_provenance": provenance,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })

    return {"results": results, "generated_count": len(results)}


# ── Job search (AI-synthesized listings) ─────────────────────────────────────

class JobSearchRequest(BaseModel):
    file_ids: list[str] = []
    instructions: str = ""
    query: str = ""
    limit: int = 10


@router.post("/job-search")
async def job_search(req: JobSearchRequest):
    """
    Synthesise ILLUSTRATIVE example listings tailored to the candidate's profile — AI synthesis, not a
    live job board (W454, ledger 1.6 / R5.0). The old prompt asked the model to invent a URL and a
    published date for each listing and the page linked them as if live; a listing here carries no
    url and no date, its salary is labelled an estimate, `illustrative` is True on every row, and
    `sources_used` is EMPTY — synthesis is not a source. The page says all of this.
    """
    profile_summary = ""
    if req.file_ids:
        try:
            from agentic_core.ingestion.api import ingestion_manager
            for entry in ingestion_manager.registry:
                if entry.get("file_id") in req.file_ids:
                    text = entry.get("extracted_text", "")
                    if text:
                        profile_summary += text[:300] + "\n"
        except Exception:
            pass

    limit = min(max(req.limit, 3), 12)

    prompt = (
        f"You are a job market analyst. Generate exactly {limit} realistic job listings "
        f"tailored to the following candidate profile.\n\n"
        + (f"Profile:\n{profile_summary}\n" if profile_summary else "")
        + (f"Search query: {req.query}\n" if req.query else "")
        + (f"Additional criteria: {req.instructions}\n" if req.instructions else "")
        + f"\nThese are ILLUSTRATIVE example listings (the kind of role this candidate could target), not real "
        + "adverts: do not invent employers' web addresses or posting dates. For each listing, provide a JSON "
        + "object on one line with these fields:\n"
        + '{"title": "...", "company": "...", "location": "...", "salary_estimate": "...", '
        + '"tags": ["tag1","tag2"], "description": "2-sentence description"}\n\n'
        + f"Output exactly {limit} JSON objects, one per line. No other text."
    )

    raw, provenance = await ai_text(prompt, "career_job_search")

    listings = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = json.loads(line)
                listings.append({
                    "listing_id": uuid.uuid4().hex[:10],
                    "title": obj.get("title", "Position"),
                    "company": obj.get("company", "Company"),
                    "location": obj.get("location", "Remote"),
                    # W454 — labelled for what it is; never a fabricated url / posting date
                    "salary_estimate": obj.get("salary_estimate") or obj.get("salary"),
                    "tags": obj.get("tags", []),
                    "description": obj.get("description", ""),
                    "illustrative": True,
                    "basis": "AI-synthesised example — not a live advert; verify any role, employer or figure independently",
                })
            except json.JSONDecodeError:
                pass

    return {
        "results": listings,
        "query": req.query or "tailored to profile",
        "sources_used": [],                       # W454 — synthesis is not a source
        "illustrative": True,
        "basis": ("AI-synthesised example listings — not a live job board; no listing here links to a real "
                  "advert, and every employer, role and figure must be verified independently"),
        "total": len(listings),
        "ai_provenance": provenance,
    }


class UseListingRequest(BaseModel):
    listing_id: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    salary_estimate: str | None = None


@router.post("/job-search/use")
async def mark_listing_used(req: UseListingRequest):
    """W454 (refuter F1) — this returned `{"status": "saved"}` and persisted NOTHING while the page flipped
    the card to a green 'Set as Target Job Ad' and the generator never saw the role. Now the listing is
    INGESTED as a `job_ad` entry — the same registry the Studio's upload slots read and the generator
    builds its target context from — labelled illustrative in its own text, so what the tick says is
    what happened."""
    if not (req.title or req.description):
        raise HTTPException(status_code=422, detail="a listing needs at least a title or a description")
    from agentic_core.ingestion.api import ingestion_manager
    text = (f"# Target role (ILLUSTRATIVE — an AI-synthesised example listing, not a live advert; verify the "
            f"employer, role and figures independently)\n\n"
            f"Title: {req.title}\nCompany: {req.company or 'not stated'}\nLocation: {req.location or 'not stated'}\n"
            + (f"Salary estimate: {req.salary_estimate}\n" if req.salary_estimate else "")
            + f"\n{req.description}\n")
    entry = ingestion_manager.ingest_text(text, filename=f"illustrative-listing-{(req.title or 'role')[:40]}.md",
                                          category="job_ad")
    return {"status": "attached", "listing_id": req.listing_id or None, "file_id": entry.get("file_id"),
            "category": "job_ad", "title": req.title, "illustrative": True}
