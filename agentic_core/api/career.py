"""
Career Domain API — Employment domain endpoints for Application Studio.

  POST /api/v1/career/uploads/auto   — classify uploaded file into a career category
  POST /api/v1/career/generate       — generate career documents (CV, cover letter, etc.)
  POST /api/v1/career/job-search     — AI-synthesized job listings based on profile
  POST /api/v1/career/job-search/use — mark a job listing as applied-to
"""
from __future__ import annotations

import json
import re
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text, person_said

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
        "Middle: the achievements STATED in the candidate profile context that match the role requirements "
        "(if none are stated, write [ADD: an achievement you have recorded] - never supply one). "
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
    # W495 (FU-124, S12.2) — before this round an uploaded CV of any type but .txt/.md arrived here as
    # INVENTED text ("Primary topics identified: Digital Sovereign Intelligence, Autonomous Evolution"),
    # so Application Studio generated an application "from" a document nobody had read. Unread files now
    # carry empty text; they are NAMED back to the caller rather than silently thinning the context.
    _unread: List[Dict[str, Any]] = []
    if req.file_ids:
        try:
            from agentic_core.ingestion.api import ingestion_manager
            registry = ingestion_manager.registry
            for entry in registry:
                if entry.get("file_id") in req.file_ids:
                    text = (entry.get("extracted_text") or "").strip()
                    category = entry.get("category", "document")
                    if text and entry.get("status") == "EXTRACTED":
                        profile_context += f"\n[{category.upper()}]\n{text[:600]}\n"
                    else:
                        _unread.append({"filename": entry.get("filename"),
                                        "status": entry.get("status") or "NOT_EXTRACTED",
                                        "basis": entry.get("extraction_basis") or ""})
        except Exception:
            pass

    target_context = ""
    if req.company_website:
        target_context += f"Company website: {req.company_website}\n"
    if req.linkedin_url:
        target_context += f"LinkedIn URL: {req.linkedin_url}\n"
    if req.instructions:
        target_context += f"Special instructions: {req.instructions}\n"

    #  P3.23 (W610) — THE CAREER AGENT MAY ONLY ASSEMBLE WHAT THE CANDIDATE RECORDED. A CV is a claim about a
    #  person, so nothing recorded means nothing is generated: the request is REFUSED and says what to record.
    #  Every prompt carries the recorded-only instruction, and every output is CHECKED afterwards: a number or a
    #  year it contains that the recorded profile does not is listed as an unsupported specific, because an
    #  instruction to a model is not a guarantee about its output.
    if not profile_context.strip():
        return {"results": [], "generated_count": 0, "unread_files": _unread, "refused": "nothing_recorded",
                "unread_basis": "",
                "basis": ("REFUSED: nothing about the candidate is recorded (no readable uploaded document was "
                          "named), and the career agent assembles only what was recorded - it never invents an "
                          "achievement, a metric or a date. Upload a CV or a record of your experience first.")}
    _recorded_numbers = set(re.findall(r"\d+(?:[.,]\d+)?", profile_context))
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
            + "\nUse ONLY facts stated in the candidate profile context. For any achievement, metric, employer, "
              "date or qualification it does not state, write [ADD: what is needed] instead. Never invent one."
            + "\nGenerate the complete document now in Markdown format."
        )

        content, provenance = await ai_text(prompt, "career_generator",
        user_text=person_said(req.instructions))
        results.append({
            "output_id": uuid.uuid4().hex[:10],
            "output_type": output_type,
            "title": output_type.replace("_", " ").title(),
            "content": content,
            #  every number or year in the output that the recorded profile does not contain
            "unsupported_specifics": sorted({n for n in re.findall(r"\d+(?:[.,]\d+)?", str(content or ""))
                                             if n not in _recorded_numbers}),
            "ai_provenance": provenance,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })

    # W495 - the caller is told which of its uploads contributed nothing, and why
    return {"results": results, "generated_count": len(results),
            "refused": None,
            "basis": ("assembled from the recorded profile only; any number or year an output contains that the "
                      "record does not is listed in that output's unsupported_specifics"),
            "unread_files": _unread,
            "unread_basis": ("" if not _unread else
                             f"{len(_unread)} uploaded file(s) contributed nothing to these outputs "
                             f"because this platform has not read them: "
                             + "; ".join(f"{u['filename']} ({u['status']})" for u in _unread))}


# ── Job search (AI-synthesized listings) ─────────────────────────────────────

#  W574 (M1 R5.1) — THE PROMPT'S OWN FIELD TEMPLATE CAME BACK AS A JOB LISTING. The deterministic
#  floor echoes the template line from the prompt, and the parser accepted ANY {…} line, so the echo
#  became a row and the page reported "Synthesised 1 illustrative listing". A person acts on a job
#  listing; that one was the scaffolding of the request that asked for it.
#
#  THE TEST IS ON THE VALUES, not on the shape of the line, and it is deliberately CONSERVATIVE: a
#  listing is discarded only when EVERY value it carries is one of the template's own placeholders.
#  A half-filled listing survives, because a real advert with one missing field is still an advert,
#  and discarding it would trade this defect for the opposite one.
_PLACEHOLDER_VALUES = {"...", "…", "tag1", "tag2", "2-sentence description",
                       "title", "company", "location", "salary_estimate"}


def _is_template_echo(obj: dict) -> bool:
    """True when a parsed line is the prompt's field template rather than a listing."""
    vals = []
    for v in (obj or {}).values():
        if isinstance(v, str):
            vals.append(v.strip().lower())
        elif isinstance(v, list):
            vals += [str(x).strip().lower() for x in v]
    if not vals:
        return True
    return all(v in _PLACEHOLDER_VALUES or not v for v in vals)


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

    raw, provenance = await ai_text(prompt, "career_job_search",
        user_text=person_said(req.query, req.instructions))

    # W574 (M1 R5.1) — THE PROMPT'S OWN FIELD TEMPLATE CAME BACK AS A JOB LISTING. The deterministic
    # floor echoes the template line above ({"title": "...", "company": "...", …}) and this parser
    # accepted any {…} line, so the echo became a row and the page reported "Synthesised 1
    # illustrative listing". A person acts on a job listing; this one was the scaffolding of the
    # request that asked for it.
    #
    # The test is on the VALUES, not on the line — see `_is_template_echo`, which is module-level so
    # a guard can drive it rather than infer it from this function's source.
    listings, _echoes = [], 0
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = json.loads(line)
                if _is_template_echo(obj):
                    _echoes += 1
                    continue
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
        # W574 (M1 R5.1) — AN ABSENCE THAT WOULD OTHERWISE READ AS A FACT. If the only thing the
        # model returned was the prompt's own field template, the honest answer is zero listings AND
        # the reason: a bare `total: 0` would read as "no roles match", which is a different and
        # false statement about the job market rather than about this deployment.
        # (A numeric `template_echoes_discarded` was returned here too and removed in the same
        # round: the pre-flight's key screen found it reaching no surface, and the sentence below
        # already states the count in words where a reader actually meets it.)
        "none_basis": (
            f"{_echoes} line(s) came back as the prompt's own field template rather than a listing "
            f"and were discarded. No listing could be synthesised here — this says nothing about "
            f"whether such roles exist." if _echoes and not listings else None),
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
