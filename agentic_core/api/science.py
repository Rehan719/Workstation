"""
Science Domain API — Research synthesis and scholarly tools.

  POST /api/v1/science/synthesise     — synthesise a research question into a structured report
  POST /api/v1/science/hypothesis     — generate and evaluate hypotheses for a research question
  POST /api/v1/science/literature     — produce a structured literature review outline
  GET  /api/v1/science/methodologies  — list supported research methodologies
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/science", tags=["science"])

_METHODOLOGIES = [
    {"id": "systematic_review", "name": "Systematic Review", "type": "qualitative/quantitative"},
    {"id": "meta_analysis", "name": "Meta-Analysis", "type": "quantitative"},
    {"id": "rct", "name": "Randomised Controlled Trial", "type": "quantitative"},
    {"id": "cohort_study", "name": "Cohort Study", "type": "observational"},
    {"id": "case_control", "name": "Case-Control Study", "type": "observational"},
    {"id": "grounded_theory", "name": "Grounded Theory", "type": "qualitative"},
    {"id": "mixed_methods", "name": "Mixed Methods", "type": "mixed"},
    {"id": "computational", "name": "Computational / In Silico", "type": "computational"},
    {"id": "experimental", "name": "Laboratory Experimental", "type": "experimental"},
    {"id": "survey", "name": "Survey Research", "type": "quantitative/qualitative"},
]


@router.get("/methodologies")
async def list_methodologies():
    return {"methodologies": _METHODOLOGIES, "total": len(_METHODOLOGIES)}


class SynthesiseRequest(BaseModel):
    research_question: str
    domain: str = "general"  # e.g. medicine, physics, social science
    methodology: str = "systematic_review"
    depth: str = "standard"  # brief | standard | comprehensive


@router.post("/synthesise")
async def synthesise_research(req: SynthesiseRequest):
    """
    Synthesise a research question into a structured evidence report.
    Uses PICO/SPIDER framework for health, adapted for other domains.
    """
    depth_instructions = {
        "brief": "Produce a concise 500-word synthesis with 3-5 key findings.",
        "standard": "Produce a 1000-1500 word synthesis with 6-8 key findings, analysis, and recommendations.",
        "comprehensive": (
            "Produce a comprehensive 2000+ word evidence synthesis with full GRADE assessment, "
            "subgroup considerations, heterogeneity discussion, and detailed recommendations."
        ),
    }.get(req.depth, "Produce a 1000-1500 word synthesis with 6-8 key findings.")

    prompt = (
        f"You are a senior research scientist and evidence synthesis specialist.\n"
        f"Research question: {req.research_question}\n"
        f"Domain: {req.domain}\n"
        f"Primary methodology lens: {req.methodology.replace('_', ' ')}\n\n"
        f"{depth_instructions}\n\n"
        "Structure your synthesis with these sections:\n"
        "## Research Question\n"
        "## Background & Rationale\n"
        "## Methodology Framework\n"
        "## Key Evidence Findings (numbered, with evidence quality notes)\n"
        "## Synthesis & Analysis\n"
        "## Limitations & Gaps\n"
        "## Conclusions\n"
        "## Recommended Next Steps\n\n"
        "Be rigorous, cite reasoning, acknowledge uncertainty. "
        "Where evidence is absent, state this explicitly rather than speculating."
    )

    report = await gateway.query(prompt, agent="science_synthesiser")

    return {
        "synthesis_id": uuid.uuid4().hex[:10],
        "research_question": req.research_question,
        "domain": req.domain,
        "methodology": req.methodology,
        "depth": req.depth,
        "report": report,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class HypothesisRequest(BaseModel):
    research_question: str
    domain: str = "general"
    background_context: str = ""
    num_hypotheses: int = 3


@router.post("/hypothesis")
async def generate_hypotheses(req: HypothesisRequest):
    """
    Generate testable hypotheses for a research question with evaluation.
    """
    n = min(max(req.num_hypotheses, 2), 5)

    prompt = (
        f"You are a research design expert. Generate exactly {n} distinct, testable hypotheses "
        f"for the following research question.\n\n"
        f"Research question: {req.research_question}\n"
        f"Domain: {req.domain}\n"
        + (f"Background: {req.background_context}\n" if req.background_context else "")
        + f"\nFor each hypothesis provide:\n"
        "- NULL hypothesis (H0)\n"
        "- ALTERNATIVE hypothesis (H1)\n"
        "- Rationale (1-2 sentences)\n"
        "- Suggested test/study design\n"
        "- Feasibility assessment (High/Medium/Low with reason)\n"
        "- Novel contribution score (1-10)\n\n"
        f"Format each as: HYPOTHESIS_N | H0: ... | H1: ... | Rationale: ... | "
        "Test design: ... | Feasibility: ... | Novelty: N/10\n\n"
        f"Then add a RECOMMENDATION line: which hypothesis to pursue first and why."
    )

    raw = await gateway.query(prompt, agent="science_hypothesis")

    hypotheses = []
    recommendation = ""
    for line in raw.splitlines():
        line = line.strip()
        if line.upper().startswith("HYPOTHESIS_"):
            hypotheses.append(line)
        elif line.upper().startswith("RECOMMENDATION"):
            recommendation = line.partition(":")[2].strip()

    return {
        "hypothesis_set_id": uuid.uuid4().hex[:10],
        "research_question": req.research_question,
        "domain": req.domain,
        "hypotheses_raw": hypotheses if hypotheses else [raw],
        "recommendation": recommendation,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class LiteratureRequest(BaseModel):
    research_question: str
    domain: str = "general"
    scope_years: int = 10  # how many years back to scope
    include_grey_literature: bool = False


@router.post("/literature")
async def literature_review_outline(req: LiteratureRequest):
    """
    Generate a structured literature review outline with search strategy.
    """
    prompt = (
        f"You are a systematic review specialist. Create a comprehensive literature review outline "
        f"for the following research question.\n\n"
        f"Research question: {req.research_question}\n"
        f"Domain: {req.domain}\n"
        f"Scope: Last {req.scope_years} years\n"
        f"Include grey literature: {req.include_grey_literature}\n\n"
        "Produce:\n"
        "## 1. Search Strategy\n"
        "   - Recommended databases (list at least 5 relevant ones)\n"
        "   - PICO/SPIDER framework breakdown\n"
        "   - Boolean search string examples\n"
        "   - MeSH/controlled vocabulary terms\n"
        "## 2. Inclusion/Exclusion Criteria Table\n"
        "## 3. Literature Review Structure (proposed chapter/section outline)\n"
        "## 4. Key Themes to Cover (6-8 themes with brief descriptions)\n"
        "## 5. Quality Assessment Tool (which tool to use and why)\n"
        "## 6. Data Extraction Template (fields to capture)\n\n"
        "Be specific and actionable. Tailor to the domain."
    )

    outline = await gateway.query(prompt, agent="science_literature")

    return {
        "review_id": uuid.uuid4().hex[:10],
        "research_question": req.research_question,
        "domain": req.domain,
        "scope_years": req.scope_years,
        "outline": outline,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
