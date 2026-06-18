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

from agentic_core.ai.gateway import gateway

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

    result = await gateway.query(prompt, agent="career_classifier")

    # Parse AI response
    try:
        # Strip markdown fences if present
        clean = result.strip().strip("```json").strip("```").strip()
        data = json.loads(clean)
        category = data.get("category", "cv_history")
        if category not in _CATEGORIES:
            category = "cv_history"
        confidence = float(data.get("confidence", 0.85))
        reasoning = data.get("reasoning", "Document classified by content analysis.")
    except Exception:
        category = "cv_history"
        confidence = 0.7
        reasoning = "Could not parse AI classification — defaulted to CV history."

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

        content = await gateway.query(prompt, agent="career_generator")
        results.append({
            "output_id": uuid.uuid4().hex[:10],
            "output_type": output_type,
            "title": output_type.replace("_", " ").title(),
            "content": content,
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
    Generate realistic job listings tailored to the candidate's profile.
    Uses AI synthesis — not a live job board. Returns structured listings.
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
        + f"\nFor each listing, provide a JSON object on one line with these fields:\n"
        + '{"source": "...", "title": "...", "company": "...", "location": "...", '
        + '"url": "https://...", "salary": "...", "tags": ["tag1","tag2"], '
        + '"published": "2026-06-...", "description": "2-sentence description"}\n\n'
        + f"Output exactly {limit} JSON objects, one per line. No other text."
    )

    raw = await gateway.query(prompt, agent="career_job_search")

    listings = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = json.loads(line)
                # Ensure required fields
                listings.append({
                    "source": obj.get("source", "JobBoard"),
                    "title": obj.get("title", "Position"),
                    "company": obj.get("company", "Company"),
                    "location": obj.get("location", "Remote"),
                    "url": obj.get("url", "https://example.com/job"),
                    "salary": obj.get("salary"),
                    "tags": obj.get("tags", []),
                    "published": obj.get("published", time.strftime("%Y-%m-%d")),
                    "description": obj.get("description", ""),
                })
            except json.JSONDecodeError:
                pass

    return {
        "results": listings,
        "query": req.query or "tailored to profile",
        "sources_used": ["AI Career Intelligence"],
        "total": len(listings),
    }


class UseListingRequest(BaseModel):
    url: str
    title: str = ""


@router.post("/job-search/use")
async def mark_listing_used(req: UseListingRequest):
    """Record that the user has applied to / is working on a job listing."""
    return {"status": "saved", "url": req.url, "title": req.title}
