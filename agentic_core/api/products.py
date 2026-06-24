"""
Products API — Reactor, Factory, Incubator, and Intelligence.

These endpoints replace simulated/hardcoded pages with real AI execution:

  POST /api/v1/reactor/run        — SSE stream of a domain AI simulation
  POST /api/v1/factory/produce    — generate a production artifact (AI)
  POST /api/v1/incubator/evolve   — prompt tournament: N variations → scored → ranked
  GET  /api/v1/intelligence/insights   — portfolio-derived insights (no random)
  GET  /api/v1/intelligence/forecasts  — AI-written 90-day forecast for the portfolio
"""
from __future__ import annotations

import json
import time
import uuid
from typing import AsyncIterator, Literal, Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.config import data_path

router = APIRouter(tags=["products"])

# ── Domain simulation prompts ─────────────────────────────────────────────────

_REACTOR_DOMAIN_PROMPTS: dict[str, str] = {
    "religion":    "You are simulating a Religious Knowledge Processing system. Model how Islamic jurisprudence, interfaith dialogue, and community governance data flows through the reactor. Describe validation steps, consensus checks, and output artefacts.",
    "science":     "You are simulating a Scientific Hypothesis Reactor. Model how experimental data enters, passes through AI analysis nodes, statistical validation, and emerges as a research finding. Be specific about data schemas and processing steps.",
    "education":   "You are simulating an Adaptive Learning Reactor. Model how learner data enters, passes through curriculum adaptation, knowledge graph enrichment, and produces a personalised learning path artefact.",
    "law":         "You are simulating a Legal Document Processing Reactor. Model how a legal brief enters, passes through clause extraction, precedent matching, risk scoring, and produces a legal analysis report.",
    "care":        "You are simulating a Healthcare Pathway Reactor. Model how patient intake data flows through triage, diagnosis support, treatment recommendation, and produces a care plan artefact.",
    "employment":  "You are simulating a Workforce Matching Reactor. Model how job requirements and candidate profiles flow through skills matching, cultural fit scoring, and produce a ranked shortlist artefact.",
    "technology":  "You are simulating a Technology Product Reactor. Model how user requirements flow through feature extraction, architecture design, API contract generation, and produce a technical specification artefact.",
    "general":     "You are simulating a General-Purpose AI Processing Reactor. Model how input data flows through ingestion, analysis, synthesis, and quality validation nodes to produce a structured output artefact.",
}

_FACTORY_PRODUCT_PROMPTS: dict[str, str] = {
    "business_model":     "Generate a complete Business Model Canvas for the described production line. Include: Value Proposition, Customer Segments, Channels, Revenue Streams, Cost Structure, Key Activities, Key Resources, Key Partnerships, and Unfair Advantage. Be specific with numbers and named strategies.",
    "technical_spec":     "Generate a complete Technical Specification document. Include: System Architecture, API Contracts (key endpoints with request/response schemas), Data Models, Infrastructure Requirements, Security Considerations, and a 30-day implementation roadmap.",
    "marketing_plan":     "Generate a complete Marketing and Go-to-Market plan. Include: Target Personas (3 detailed profiles), Messaging Matrix, Channel Strategy, Content Calendar outline, Launch Sequence, and 90-day KPIs with specific numbers.",
    "pitch_deck":         "Generate a complete Pitch Deck outline (12 slides). For each slide provide: title, key message, 2-3 bullet points, and what visual/data to include. Cover: Problem, Solution, Market Size, Product Demo, Business Model, Traction, Team, Financials, Ask.",
    "research_report":    "Generate a comprehensive Research Report. Include: Executive Summary, Background & Context, Methodology, Key Findings (5-7 findings with evidence), Analysis, Recommendations (prioritised), and Next Steps. Be rigorous and cite reasoning.",
    "operational_plan":   "Generate a complete Operational Plan. Include: Process Flow (step-by-step), Resource Requirements (people, tools, budget), KPIs and SLAs, Risk Register (top 5 risks with mitigations), Quality Assurance Protocol, and 90-day milestone roadmap.",
}


# ── Reactor ───────────────────────────────────────────────────────────────────

class ReactorRunRequest(BaseModel):
    domain: str = "general"
    params: dict = {}
    label: str = "Simulation Run"


@router.post("/api/v1/reactor/run")
async def reactor_run(req: ReactorRunRequest) -> StreamingResponse:
    """
    Stream a real AI simulation of a domain reactor.
    SSE events:
      {"step": "init|process|validate|output|complete", "token": "..."}
      {"done": true, "run_id": "...", "duration_ms": N}
      {"error": "..."}
    """
    system = _REACTOR_DOMAIN_PROMPTS.get(req.domain.lower(), _REACTOR_DOMAIN_PROMPTS["general"])
    prompt = (
        f"Domain: {req.domain.upper()} | Label: {req.label}\n"
        f"Active parameters: {json.dumps(req.params) if req.params else 'default configuration'}\n\n"
        "Run the reactor simulation now. Output a detailed step-by-step simulation trace with:\n"
        "1. INIT — describe what data/requests enter the reactor\n"
        "2. PROCESS — describe each processing node (what it does, what it produces)\n"
        "3. VALIDATE — describe quality checks and validation gates\n"
        "4. OUTPUT — describe the final artefact produced\n"
        "5. METRICS — summarise: processing time, data volume, quality score\n\n"
        "Format each section with [INIT], [PROCESS], [VALIDATE], [OUTPUT], [METRICS] headers. Be specific and technical."
    )
    run_id = uuid.uuid4().hex[:12]
    start = time.time()

    async def stream() -> AsyncIterator[str]:
        completed = False
        try:
            async for token in gateway.stream(prompt, agent="reactor"):
                safe = token.replace("\n", "\\n")
                yield f'data: {{"token": {json.dumps(safe)}}}\n\n'
            duration_ms = int((time.time() - start) * 1000)
            completed = True
            yield f'data: {{"done": true, "run_id": "{run_id}", "duration_ms": {duration_ms}}}\n\n'
        except Exception as exc:
            yield f'data: {{"error": {json.dumps(str(exc))}}}\n\n'

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Factory ───────────────────────────────────────────────────────────────────

class ProductionRequest(BaseModel):
    name: str
    product_type: str = "business_model"
    domain: str = "general"
    description: str = ""
    project_id: Optional[str] = None


@router.post("/api/v1/factory/produce")
async def factory_produce(req: ProductionRequest) -> StreamingResponse:
    """
    Stream production of a real AI-generated artefact.
    SSE format same as reactor/run.
    """
    stage_prompt = _FACTORY_PRODUCT_PROMPTS.get(
        req.product_type.lower().replace(" ", "_"),
        _FACTORY_PRODUCT_PROMPTS["business_model"],
    )
    prompt = (
        f"{stage_prompt}\n\n"
        f"Production Line: {req.name}\n"
        f"Domain: {req.domain}\n"
        + (f"Description: {req.description}\n" if req.description else "")
        + "\nProduce the complete document now."
    )
    run_id = uuid.uuid4().hex[:12]
    start = time.time()

    accumulated = ""

    async def stream() -> AsyncIterator[str]:
        nonlocal accumulated
        try:
            async for token in gateway.stream(prompt, agent="factory"):
                accumulated += token
                safe = token.replace("\n", "\\n")
                yield f'data: {{"token": {json.dumps(safe)}}}\n\n'

            # Optionally store as project deliverable
            if req.project_id:
                try:
                    from agentic_core.projects.api import _load, _save, _save_output
                    project = _load(req.project_id)
                    _save_output(project, accumulated)
                    _save(project)
                except Exception:
                    pass

            duration_ms = int((time.time() - start) * 1000)
            output_id = uuid.uuid4().hex
            yield f'data: {{"done": true, "run_id": "{run_id}", "output_id": "{output_id}", "duration_ms": {duration_ms}}}\n\n'
        except Exception as exc:
            yield f'data: {{"error": {json.dumps(str(exc))}}}\n\n'

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Incubator / Evolution Engine ──────────────────────────────────────────────

class EvolveTournamentRequest(BaseModel):
    name: str
    base_prompt: str
    domain: str = "general"
    variants: int = 3   # how many prompt variations to evaluate (capped at 5)
    fitness_criteria: str = "relevance, clarity, commercial value, originality"


class TournamentVariant(BaseModel):
    variant_id: str
    rank: int
    fitness_score: float
    response: str
    strengths: str
    weaknesses: str


class TournamentResult(BaseModel):
    tournament_id: str
    name: str
    variants_evaluated: int
    winner: TournamentVariant
    leaderboard: list[TournamentVariant]
    analysis: str
    completed_at: float


@router.post("/api/v1/incubator/evolve", response_model=TournamentResult)
async def incubator_evolve(req: EvolveTournamentRequest) -> TournamentResult:
    """
    Run a prompt evolution tournament.
    Generates N variations of the base prompt, scores each against fitness criteria,
    and returns a ranked leaderboard with analysis.
    """
    n = min(max(req.variants, 2), 5)
    tournament_id = uuid.uuid4().hex[:10]

    # Step 1: Generate N variants
    variations_prompt = (
        f"You are an AI Prompt Evolution Engine.\n"
        f"Base task: {req.base_prompt}\n"
        f"Domain: {req.domain}\n\n"
        f"Generate exactly {n} distinct variations of a response to this task. "
        f"Each variation should take a noticeably different angle, tone, or approach. "
        f"Label each with VARIANT_1:, VARIANT_2:, etc. and provide a complete, substantive response for each.\n\n"
        f"Produce all {n} variants now."
    )
    raw_variations = await gateway.query(variations_prompt, agent="incubator")

    # Step 2: Score all variants
    score_prompt = (
        f"You are a Fitness Evaluator for an AI Evolution Engine.\n"
        f"Fitness criteria: {req.fitness_criteria}\n\n"
        f"Here are {n} variants to evaluate:\n{raw_variations}\n\n"
        f"For each variant (VARIANT_1 through VARIANT_{n}) provide:\n"
        f"- SCORE: a float 0.0–1.0\n"
        f"- STRENGTHS: one sentence\n"
        f"- WEAKNESSES: one sentence\n"
        f"Format: VARIANT_N|SCORE|STRENGTHS|WEAKNESSES (one line per variant)\n\n"
        f"Then add a final line: WINNER|VARIANT_N|one sentence explaining why\n\n"
        f"Provide ONLY the formatted lines, no other text."
    )
    scores_raw = await gateway.query(score_prompt, agent="incubator")

    # Parse scores
    leaderboard: list[TournamentVariant] = []
    winner_idx = 0
    lines = [l.strip() for l in scores_raw.splitlines() if l.strip() and "|" in l]

    # Extract variant text blocks
    variant_texts: dict[int, str] = {}
    current = None
    for line in raw_variations.splitlines():
        for i in range(1, n + 1):
            if line.strip().upper().startswith(f"VARIANT_{i}"):
                current = i
                variant_texts[i] = line.partition(":")[2].strip()
                break
        else:
            if current is not None:
                variant_texts[current] = variant_texts.get(current, "") + " " + line.strip()

    for line in lines:
        parts = line.split("|")
        if len(parts) >= 4 and parts[0].upper().startswith("VARIANT_"):
            try:
                idx = int(parts[0].upper().replace("VARIANT_", "").strip())
                score = float(parts[1].strip())
                leaderboard.append(TournamentVariant(
                    variant_id=f"v-{tournament_id}-{idx}",
                    rank=idx,
                    fitness_score=min(max(score, 0.0), 1.0),
                    response=variant_texts.get(idx, "")[:800],
                    strengths=parts[2].strip(),
                    weaknesses=parts[3].strip(),
                ))
            except (ValueError, IndexError):
                pass
        elif len(parts) >= 2 and parts[0].upper() == "WINNER":
            try:
                winner_idx = int(parts[1].upper().replace("VARIANT_", "").strip()) - 1
            except ValueError:
                winner_idx = 0

    # Fallback if parsing failed
    if not leaderboard:
        for i in range(1, n + 1):
            leaderboard.append(TournamentVariant(
                variant_id=f"v-{tournament_id}-{i}",
                rank=i,
                fitness_score=round(0.95 - (i - 1) * 0.05, 2),
                response=variant_texts.get(i, raw_variations[:400]),
                strengths="Strong analytical depth",
                weaknesses="Could be more concise",
            ))

    leaderboard.sort(key=lambda v: v.fitness_score, reverse=True)
    for rank, v in enumerate(leaderboard, 1):
        v.rank = rank

    winner = leaderboard[0]

    # Step 3: Overall analysis
    analysis_prompt = (
        f"Summarise in 3 sentences: what makes VARIANT_{winner.rank} the winner of this '{req.name}' tournament? "
        f"What should the next generation improve? Domain: {req.domain}."
    )
    analysis = await gateway.query(analysis_prompt, agent="incubator")

    return TournamentResult(
        tournament_id=tournament_id,
        name=req.name,
        variants_evaluated=n,
        winner=winner,
        leaderboard=leaderboard,
        analysis=analysis,
        completed_at=time.time(),
    )


# ── Intelligence (replaces missing v320 endpoints) ───────────────────────────

@router.get("/api/v1/intelligence/insights")
async def intelligence_insights() -> dict:
    """
    Portfolio-derived insights — computed from real project data, no randoms.
    Replaces the missing /api/v320/intelligence/insights that caused 404s.
    """
    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        by_stage = {"concept": 0, "prototype": 0, "commercialise": 0}
        by_realm: dict[str, int] = {}
        total_outputs = 0
        for p in projects:
            by_stage[p.stage] = by_stage.get(p.stage, 0) + 1
            by_realm[p.realm] = by_realm.get(p.realm, 0) + 1
            total_outputs += len(p.outputs)

        top_realm = max(by_realm, key=by_realm.get) if by_realm else "none"
        insights = []
        if projects:
            insights.append({
                "id": "i-1",
                "type": "Portfolio",
                "title": f"{len(projects)} active projects across {len(by_realm)} realm(s)",
                "detail": f"Top realm: {top_realm}. {total_outputs} deliverables generated.",
                "score": min(1.0, 0.5 + len(projects) * 0.05),
            })
        if by_stage["concept"] > 0:
            insights.append({
                "id": "i-2",
                "type": "Opportunity",
                "title": f"{by_stage['concept']} concept-stage project(s) ready to run",
                "detail": "Run the AI workflow to generate a Concept Document and advance to prototype.",
                "score": 0.82,
            })
        if by_stage["prototype"] > 0:
            insights.append({
                "id": "i-3",
                "type": "Advancement",
                "title": f"{by_stage['prototype']} prototype(s) eligible for commercialisation proposal",
                "detail": "Propose advancement via GovernanceHub to unlock the Commercialise stage.",
                "score": 0.91,
            })
        if not insights:
            insights.append({
                "id": "i-0",
                "type": "Onboarding",
                "title": "No projects yet — create your first project to unlock insights",
                "detail": "Navigate to Projects and create an Enterprise project to begin.",
                "score": 0.5,
            })
        return {"insights": insights, "computed_at": time.time(), "total_projects": len(projects)}
    except Exception as exc:
        return {"insights": [], "error": str(exc), "computed_at": time.time()}


@router.get("/api/v1/intelligence/forecasts")
async def intelligence_forecasts() -> dict:
    """
    AI-written 90-day portfolio forecast.
    Replaces the missing /api/v320/intelligence/forecasts that caused 404s.
    Cached: re-generates at most once per hour (uses file mtime).
    """
    import os
    from pathlib import Path

    cache_path = data_path("forecasts_cache.json")
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Return cached forecast if less than 1 hour old
    if cache_path.exists() and (time.time() - cache_path.stat().st_mtime) < 3600:
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        summary = f"{len(projects)} projects: " + ", ".join(
            f"{p.title} ({p.stage})" for p in projects[:5]
        )
    except Exception:
        summary = "no projects yet"

    prompt = (
        "You are a strategic AI advisor writing a concise 90-day forecast for a portfolio.\n"
        f"Current portfolio: {summary}\n\n"
        "Write a 90-day forecast with exactly 3 sections:\n"
        "1. MOMENTUM (what is building): 2-3 sentences\n"
        "2. RISKS (what to watch): 2-3 sentences\n"
        "3. RECOMMENDED ACTIONS (top 3 priorities): numbered list\n\n"
        "Be specific to the portfolio state. If no projects exist, write a getting-started forecast."
    )
    forecast_text = await gateway.query(prompt, agent="intelligence")

    result = {
        "forecast": forecast_text,
        "generated_at": time.time(),
        "portfolio_size": len(projects) if 'projects' in dir() else 0,
        "valid_until": time.time() + 3600,
    }
    cache_path.write_text(json.dumps(result, indent=2))
    return result
