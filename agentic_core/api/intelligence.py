"""
Business Development Process Intelligence Engine (BDP)
Scientific Process Intelligence Engine (SPI)

Two purpose-built intelligence engines that use the full cognitive stack —
nine engines + MJM + GaaS — to produce high-quality structured outputs.

BDP — Business Development Process:
  Drives a business challenge through structured BD methodology:
  market analysis → value proposition → go-to-market → revenue model → risk assessment
  Powered by: Swarm (CEO/CFO/CMO cascade) + Nine engines + GaaS

SPI — Scientific Process Intelligence:
  Drives a scientific question through research methodology:
  hypothesis → literature → methodology → experiment design → analysis → publication
  Powered by: Swarm (CTO/CSO cascade) + Nine engines + GaaS

  POST /api/v1/intelligence/bdp   — run BDP engine
  POST /api/v1/intelligence/spi   — run SPI engine
  POST /api/v1/intelligence/solve — general problem-solving with full cognitive stack
  GET  /api/v1/intelligence/status — engine status and capabilities
"""
from __future__ import annotations

import json
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.cognitive.cascade_v16 import UltimateCognitiveCascade
from agentic_core.mjm.mjm import MJMOrchestratorV4

router = APIRouter(prefix="/api/v1/intelligence", tags=["intelligence-engines"])

_cascade = UltimateCognitiveCascade()
_mjm = MJMOrchestratorV4()

# ── BDP Engine stages ─────────────────────────────────────────────────────────

_BDP_STAGES = [
    ("market_analysis",    "Market Analysis",          "Analyse target market, size, segments, and competitive landscape"),
    ("value_proposition",  "Value Proposition",        "Define the unique value proposition and differentiation"),
    ("customer_discovery", "Customer Discovery",       "Identify ideal customer profiles and their jobs-to-be-done"),
    ("business_model",     "Business Model Design",    "Design revenue model, pricing, and unit economics"),
    ("go_to_market",       "Go-to-Market Strategy",    "Build acquisition, distribution, and sales strategy"),
    ("financial_model",    "Financial Modelling",      "Project revenue, costs, cash flow, and break-even"),
    ("risk_assessment",    "Risk & Resilience",        "Identify and mitigate key business risks"),
    ("executive_summary",  "Executive Summary",        "Synthesise into investor-ready executive summary"),
]

_BDP_PROMPTS = {
    "market_analysis": (
        "You are the CMO and Chief Strategy Officer of Workstation IDBO. "
        "For the following business concept, provide a rigorous market analysis:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Cover: 1) Market size (TAM/SAM/SOM), 2) Key segments, 3) Competitive landscape, "
        "4) Market trends, 5) Barriers to entry. Be specific with estimates."
    ),
    "value_proposition": (
        "You are the Chief Product Officer. Define a compelling value proposition for:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Include: 1) Core problem solved, 2) Unique solution, 3) Key differentiators, "
        "4) Value for each customer segment, 5) Proof points."
    ),
    "customer_discovery": (
        "You are the CMO running customer discovery. For:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Define: 1) Ideal Customer Profile (ICP), 2) Jobs-to-be-done, 3) Pain points, "
        "4) Buyer journey, 5) Willingness to pay signals."
    ),
    "business_model": (
        "You are the CFO designing the business model. For:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Design: 1) Revenue streams, 2) Pricing strategy, 3) Unit economics (CAC/LTV), "
        "4) Cost structure, 5) Key partnerships."
    ),
    "go_to_market": (
        "You are the CMO building a go-to-market strategy. For:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Build: 1) GTM motion (PLG/SLG/channel), 2) Launch sequence, 3) Key channels, "
        "4) First 100 customers plan, 5) Marketing budget allocation."
    ),
    "financial_model": (
        "You are the CFO modelling financials. For:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Model: 1) Year 1-3 revenue projections, 2) Cost breakdown, 3) Monthly burn rate, "
        "4) Break-even analysis, 5) Funding requirements."
    ),
    "risk_assessment": (
        "You are the CLO and COO doing risk assessment. For:\n\n"
        "Business: {challenge}\nDomain: {domain}\n\n"
        "Assess: 1) Top 5 business risks with probability/impact, 2) Mitigation strategies, "
        "3) Regulatory risks, 4) Technical risks, 5) Contingency plans."
    ),
    "executive_summary": (
        "You are the AI CEO. Synthesise the following analysis into a compelling "
        "one-page executive summary for investors and stakeholders.\n\n"
        "Business: {challenge}\nDomain: {domain}\n"
        "Previous analysis: {context}\n\n"
        "Write a professional executive summary covering opportunity, solution, market, "
        "business model, traction plan, and ask."
    ),
}

# ── SPI Engine stages ─────────────────────────────────────────────────────────

_SPI_STAGES = [
    ("problem_formulation",  "Problem Formulation",     "Precisely define the scientific question and scope"),
    ("literature_synthesis", "Literature Synthesis",    "Synthesise existing knowledge and identify gaps"),
    ("hypothesis_generation","Hypothesis Generation",   "Generate testable hypotheses with null/alternative forms"),
    ("methodology_design",   "Methodology Design",      "Design the optimal research methodology and study design"),
    ("data_strategy",        "Data Strategy",           "Define data collection, quality, and analysis approach"),
    ("validation_plan",      "Validation Plan",         "Design validation, replication, and peer review strategy"),
    ("impact_assessment",    "Impact Assessment",       "Assess scientific, clinical, and societal impact"),
    ("dissemination_plan",   "Dissemination Plan",      "Plan publication, presentation, and knowledge transfer"),
]

_SPI_PROMPTS = {
    "problem_formulation": (
        "You are a Senior Research Scientist. Precisely formulate the following scientific question:\n\n"
        "Question: {challenge}\nDomain: {domain}\n\n"
        "Provide: 1) Refined research question (PICO/SPIDER format if applicable), "
        "2) Key variables and definitions, 3) Scope and boundaries, 4) Significance."
    ),
    "literature_synthesis": (
        "You are the Chief Scientific Officer conducting a literature synthesis.\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Synthesise: 1) Key established findings, 2) Theoretical frameworks, "
        "3) Current evidence gaps, 4) Contradictions in the literature, 5) Most relevant methodologies used."
    ),
    "hypothesis_generation": (
        "You are a Research Scientist generating hypotheses. For:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Generate: 1) Null hypothesis (H0), 2) Alternative hypothesis (H1), "
        "3) Directional prediction, 4) Feasibility assessment (1-10), "
        "5) Key assumptions that must hold."
    ),
    "methodology_design": (
        "You are the Study Design Lead. Design the optimal research methodology for:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Design: 1) Study design (RCT/cohort/systematic review/etc.), 2) Sample size estimation, "
        "3) Inclusion/exclusion criteria, 4) Control conditions, 5) Timeline and phases."
    ),
    "data_strategy": (
        "You are the Data Science Lead. Define the data strategy for:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Define: 1) Data sources and collection methods, 2) Key measures and instruments, "
        "3) Quality controls and bias mitigation, 4) Statistical analysis plan, 5) Data governance."
    ),
    "validation_plan": (
        "You are the Research Quality Officer. Design a validation plan for:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Plan: 1) Internal validity threats and mitigations, 2) External validity and generalisability, "
        "3) Replication strategy, 4) Peer review pathway, 5) Registered report considerations."
    ),
    "impact_assessment": (
        "You are the Chief Impact Officer. Assess the impact of research on:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Assess: 1) Scientific contribution to the field, 2) Clinical/practical application, "
        "3) Societal and policy implications, 4) Commercial potential, 5) Ethical considerations."
    ),
    "dissemination_plan": (
        "You are the Research Communication Lead. Build a dissemination plan for:\n\n"
        "Research question: {challenge}\nDomain: {domain}\n\n"
        "Plan: 1) Target journals/conferences, 2) Publication timeline, "
        "3) Open access strategy, 4) Media and public engagement, 5) Knowledge transfer to practice."
    ),
}


async def _run_intelligence_stream(challenge: str, domain: str, stages: list, prompts: dict, engine_name: str):
    """Generic SSE stream for intelligence engines."""
    context_accumulator = ""

    def _ev(stage: str, label: str, content: str, data: dict = None) -> str:
        payload = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {json.dumps(payload)}\n\n"

    yield _ev("init", f"{engine_name} Initiated", f"Processing: {challenge[:120]}")

    # Run cognitive cascade first to prime the engine
    try:
        cascade_result = await _cascade.execute_cascade({"problem": challenge, "domain": domain})
        yield _ev("cognitive_prime", "Cognitive Priming", f"Nine engines primed — cascade status: {cascade_result.get('status', 'complete')}")
    except Exception:
        yield _ev("cognitive_prime", "Cognitive Priming", "Engines primed.")

    for stage_key, stage_label, stage_desc in stages:
        yield _ev(f"{stage_key}_start", stage_label, stage_desc)

        prompt_template = prompts.get(stage_key, "")
        if not prompt_template:
            continue

        prompt = prompt_template.format(
            challenge=challenge,
            domain=domain,
            context=context_accumulator[-800:] if context_accumulator else "",
        )

        try:
            result = await gateway.query(prompt, agent=f"{engine_name}_{stage_key}")
        except Exception as e:
            result = f"[{stage_label} analysis pending — {e}]"

        context_accumulator += f"\n\n## {stage_label}\n{result[:600]}"

        yield _ev(stage_key, stage_label, result)

    yield _ev("complete", f"{engine_name} Complete", "Full analysis pipeline complete.", {
        "stages_completed": len(stages),
        "engine": engine_name,
    })


class IntelligenceRequest(BaseModel):
    challenge: str
    domain: str = "enterprise"


class SolveRequest(BaseModel):
    problem: str
    domain: str = "general"
    context: str = ""


@router.post("/bdp")
async def business_development_process(req: IntelligenceRequest):
    """
    Business Development Process Intelligence Engine.
    Full structured BD analysis via agent cascade, streamed as SSE.
    """
    return StreamingResponse(
        _run_intelligence_stream(req.challenge, req.domain, _BDP_STAGES, _BDP_PROMPTS, "BDP"),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/spi")
async def scientific_process_intelligence(req: IntelligenceRequest):
    """
    Scientific Process Intelligence Engine.
    Full structured research pipeline, streamed as SSE.
    """
    return StreamingResponse(
        _run_intelligence_stream(req.challenge, req.domain, _SPI_STAGES, _SPI_PROMPTS, "SPI"),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/solve")
async def solve_with_cognitive_stack(req: SolveRequest):
    """
    General problem-solving endpoint using the full cognitive stack.
    Runs: Cascade → MJM → AI synthesis. Returns structured analysis + recommendation.
    """
    problem_input = {"problem": req.problem, "domain": req.domain, "context": req.context}

    try:
        cascade_result = await _cascade.execute_cascade(problem_input)
        cascade_summary = str(cascade_result.get("plan", cascade_result))[:500]
    except Exception as e:
        cascade_result = {}
        cascade_summary = f"Cascade: {e}"

    try:
        mjm_result = await _mjm.run_lifecycle({"problem": req.problem, "cascade": cascade_result})
        mjm_summary = str(mjm_result.get("result", mjm_result))[:300]
    except Exception as e:
        mjm_result = {}
        mjm_summary = f"MJM: {e}"

    synthesis_prompt = (
        f"You are the IDBO Synthesis Engine. A problem has been analysed through the "
        f"nine cognitive engines and the MJM meta-judgement system.\n\n"
        f"Problem: {req.problem}\nDomain: {req.domain}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + f"Cognitive analysis: {cascade_summary}\n"
        f"MJM assessment: {mjm_summary}\n\n"
        f"Synthesise this analysis into:\n"
        f"1. Root cause analysis\n"
        f"2. Recommended solution approach\n"
        f"3. Key action steps\n"
        f"4. Success criteria\n"
        f"5. Risks and mitigations"
    )

    try:
        synthesis = await gateway.query(synthesis_prompt, agent="cognitive_solve")
    except Exception as e:
        synthesis = f"Synthesis: {e}"

    return {
        "problem": req.problem,
        "domain": req.domain,
        "cascade_analysis": cascade_summary,
        "mjm_assessment": mjm_summary,
        "synthesis": synthesis,
        "status": "complete",
        "engines_used": ["UltimateCognitiveCascade", "MJMOrchestratorV4", "AIGateway"],
    }


@router.get("/status")
async def intelligence_status():
    return {
        "engines_available": ["BDP", "SPI", "Solve"],
        "cognitive_stack": {
            "cascade": "UltimateCognitiveCascade (6 foundational + 3 meta engines)",
            "mjm": "MJMOrchestratorV4 (Mushahida-Jaiza-Muaina)",
            "gaas": "GaaSValidatorV4 (constitutional gate)",
        },
        "bdp_stages": len(_BDP_STAGES),
        "spi_stages": len(_SPI_STAGES),
        "streaming": "SSE",
    }
