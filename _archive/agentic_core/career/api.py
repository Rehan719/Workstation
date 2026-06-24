import logging
import uuid
from typing import Any, Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from config.paths import DATA_DIR
from agentic_core.ingestion.api import ingestion_manager
from agentic_core.career.classifier import classify_content
from agentic_core.career.documents import career_document_generator
from agentic_core.career.job_search import search_jobs

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/career", tags=["Employment Application Studio"])

INPUT_CATEGORIES: List[Dict[str, str]] = [
    {"id": "cv_history", "label": "Old CVs"},
    {"id": "past_applications", "label": "Past Applications"},
    {"id": "star_examples", "label": "STAR Examples"},
    {"id": "job_ad", "label": "Target Job Ad"},
    {"id": "job_description", "label": "Job Description"},
    {"id": "person_spec", "label": "Person Specification"},
    {"id": "application_guidance", "label": "Application Guidance"},
    {"id": "interview_prep_materials", "label": "Interview Preparation Materials"},
    {"id": "miscellaneous", "label": "Miscellaneous (Auto-Categorize)"},
]

OUTPUT_TYPES: List[Dict[str, str]] = [
    {"id": "cv", "label": "CV"},
    {"id": "cover_letter", "label": "Cover Letter"},
    {"id": "supporting_statement", "label": "Supporting Statement"},
    {"id": "application_form", "label": "Application Forms"},
    {"id": "interview_prep", "label": "Interview Preparation Materials"},
    {"id": "new_job_prep", "label": "New Job Preparation Materials"},
    {"id": "in_job_support", "label": "In-Job Support"},
    {"id": "linkedin_profile", "label": "LinkedIn Profile"},
]

_CATEGORY_CONTEXT_KEYS = {
    "cv_history": "cv_history_count",
    "past_applications": "application_count",
    "star_examples": "star_example_count",
    "job_ad": "job_ad_count",
    "job_description": "job_description_count",
    "person_spec": "person_spec_count",
    "application_guidance": "application_guidance_count",
    "interview_prep_materials": "interview_prep_count",
}


class CareerGenerateRequest(BaseModel):
    file_ids: List[str] = []
    company_website: str = ""
    linkedin_url: str = ""
    instructions: str = ""
    output_types: List[str] = []


class JobSearchRequest(BaseModel):
    file_ids: List[str] = []
    instructions: str = ""
    query: str = ""
    limit: int = 10


class UseJobListingRequest(BaseModel):
    title: str = "Untitled Role"
    company: str = ""
    location: str = ""
    url: str = ""
    description: str = ""
    source: str = ""


@router.get("/inputs")
async def list_input_categories():
    return {"categories": INPUT_CATEGORIES}


@router.get("/outputs")
async def list_output_types():
    return {"outputs": OUTPUT_TYPES}


@router.post("/uploads/auto")
async def upload_and_classify(file: UploadFile = File(...)):
    """Ingests an uncategorised file then autonomously assigns it to a known input category."""
    try:
        entry = await ingestion_manager.ingest_file(file, category=None)
    except Exception as e:
        logger.error(f"Auto-categorize ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    classification = classify_content(entry["filename"], entry["extracted_text"])
    entry["category"] = classification["category"]
    ingestion_manager._save_registry()

    return {**entry, "classification": classification}


def _gather_context(file_ids: List[str], company_website: str, linkedin_url: str) -> Dict[str, Any]:
    selected = [e for e in ingestion_manager.registry if e["file_id"] in file_ids]
    counts: Dict[str, int] = {}
    for entry in selected:
        category = entry.get("category")
        key = _CATEGORY_CONTEXT_KEYS.get(category)
        if key:
            counts[key] = counts.get(key, 0) + 1
    if company_website:
        counts["company_website"] = company_website
    if linkedin_url:
        counts["linkedin_url"] = linkedin_url
    return counts


def _derive_job_query(instructions: str, file_ids: List[str]) -> str:
    if instructions and instructions.strip():
        return instructions.strip()[:120]
    selected = [e for e in ingestion_manager.registry if e["file_id"] in file_ids]
    for category in ("job_ad", "job_description", "person_spec", "cv_history"):
        match = next((e for e in selected if e.get("category") == category), None)
        if match and match.get("extracted_text"):
            return match["extracted_text"][:120].replace("\n", " ").strip()
    return "remote"


@router.post("/job-search")
async def job_search(request: JobSearchRequest):
    """Performs a live, broad web search across public job board APIs, tailored to uploaded materials and instructions."""
    explicit_query = request.query.strip()
    query = explicit_query or _derive_job_query(request.instructions, request.file_ids)
    result = await search_jobs(query, limit=max(1, min(request.limit, 50)))
    return result


@router.post("/job-search/use")
async def use_job_listing(request: UseJobListingRequest):
    """Tags a found job listing as the Target Job Ad input so it feeds the generation pipeline."""
    text = (
        f"{request.title} at {request.company} ({request.location})\n"
        f"Source: {request.source} {request.url}\n\n{request.description}"
    )
    entry = ingestion_manager.ingest_text(text, f"{request.title} - {request.company or 'job listing'}.txt", category="job_ad")
    return entry


@router.post("/generate")
async def generate_career_documents(request: CareerGenerateRequest):
    context = _gather_context(request.file_ids, request.company_website, request.linkedin_url)
    output_dir = DATA_DIR / "career_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for output_type in request.output_types:
        doc = career_document_generator.generate(output_type, context, request.instructions)
        output_id = str(uuid.uuid4())
        (output_dir / f"{output_id}.md").write_text(doc["markdown"], encoding="utf-8")
        results.append({
            "output_id": output_id,
            "output_type": output_type,
            "title": doc["title"],
            "content": doc["markdown"],
            "timestamp": doc["timestamp"],
        })
    return {"results": results}
