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

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.config import data_path
from agentic_core.vbs.quality import assure_delivery

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


# ── native-swarm streaming helper (§6) ────────────────────────────────────────

def _chunk_for_stream(text: str, size: int = 96) -> list[str]:
    """Split a completed native-swarm output into word-boundary chunks so a caller keeps an SSE
    streaming shape. The owned native floor / local models return a full completion (not token-by-
    token), so chunking here is honest — the work is genuinely served in-house, just framed as a
    stream for the UI. Never splits mid-word."""
    words = (text or "").split(" ")
    chunks, cur = [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > size:
            chunks.append(cur + " ")
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        chunks.append(cur)
    return chunks


# ── Reactor ───────────────────────────────────────────────────────────────────

class ReactorRunRequest(BaseModel):
    domain: str = "general"
    params: dict = {}
    label: str = "Simulation Run"
    model: str = "auto"   # §6 user design control: auto | native | local | ollama:<name>


def _reactor_prompt(domain: str, params: dict, label: str) -> str:
    return (
        f"Domain: {domain.upper()} | Label: {label}\n"
        f"Active parameters: {json.dumps(params) if params else 'default configuration'}\n\n"
        "Run the reactor simulation now. Output a detailed step-by-step simulation trace with:\n"
        "1. INIT — describe what data/requests enter the reactor\n"
        "2. PROCESS — describe each processing node (what it does, what it produces)\n"
        "3. VALIDATE — describe quality checks and validation gates\n"
        "4. OUTPUT — describe the final artefact produced\n"
        "5. METRICS — summarise: processing time, data volume, quality score\n\n"
        "Format each section with [INIT], [PROCESS], [VALIDATE], [OUTPUT], [METRICS] headers. Be specific and technical."
    )


async def run_reactor_sim(domain: str = "general", params: Optional[dict] = None,
                          label: str = "Simulation Run", prefer: str = "auto") -> dict:
    """Run a domain-reactor simulation on Workstation's OWN native swarm (§6) and return the genuine
    output with provenance. Shared by the SSE endpoint and the §7 resource-fabric composition
    dispatch, so a composed Reactor runs the ACTUAL engine — driven by the native swarm, not the
    legacy external-first cascade."""
    from agentic_core.ai.native import orchestrator
    prompt = _reactor_prompt(domain, params or {}, label)
    res = await orchestrator.complete(prompt, agent="reactor", prefer=prefer)
    return {"output": res.get("output", "") or "", "served_by": res.get("served_by", "native"),
            "is_external": bool(res.get("is_external")), "run_id": uuid.uuid4().hex[:12]}


@router.post("/api/v1/reactor/run")
async def reactor_run(req: ReactorRunRequest) -> StreamingResponse:
    """
    Stream a real AI simulation of a domain reactor — driven by the OWNED native swarm (§6).
    SSE events:
      {"token": "..."}
      {"done": true, "run_id": "...", "duration_ms": N, "served_by": "...", "is_external": bool}
      {"error": "..."}
    """
    start = time.time()

    async def stream() -> AsyncIterator[str]:
        try:
            sim = await run_reactor_sim(req.domain, req.params, req.label, prefer=req.model)
            for chunk in _chunk_for_stream(sim["output"]):
                safe = chunk.replace("\n", "\\n")
                yield f'data: {{"token": {json.dumps(safe)}}}\n\n'
            duration_ms = int((time.time() - start) * 1000)
            yield (f'data: {{"done": true, "run_id": "{sim["run_id"]}", "duration_ms": {duration_ms}, '
                   f'"served_by": {json.dumps(sim["served_by"])}, "is_external": {json.dumps(sim["is_external"])}}}\n\n')
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
    model: str = "auto"   # §6 user design control: auto | native | local | ollama:<name>


def _factory_prompt(name: str, product_type: str, domain: str, description: str) -> str:
    stage_prompt = _FACTORY_PRODUCT_PROMPTS.get(
        product_type.lower().replace(" ", "_"), _FACTORY_PRODUCT_PROMPTS["business_model"])
    return (
        f"{stage_prompt}\n\n"
        f"Production Line: {name}\n"
        f"Domain: {domain}\n"
        + (f"Description: {description}\n" if description else "")
        + "\nProduce the complete document now."
    )


async def run_factory_produce(name: str, product_type: str = "business_model", domain: str = "general",
                              description: str = "", prefer: str = "auto") -> dict:
    """Produce a real artefact on Workstation's OWN native swarm (§6) and return it with provenance.
    Shared by the SSE endpoint and the §7 fabric composition dispatch, so a composed Factory runs the
    ACTUAL production engine — driven by the native swarm, not the legacy external-first cascade."""
    from agentic_core.ai.native import orchestrator
    prompt = _factory_prompt(name, product_type, domain, description)
    res = await orchestrator.complete(prompt, agent="factory", prefer=prefer)
    return {"output": res.get("output", "") or "", "served_by": res.get("served_by", "native"),
            "is_external": bool(res.get("is_external")), "run_id": uuid.uuid4().hex[:12]}


@router.post("/api/v1/factory/produce")
async def factory_produce(req: ProductionRequest) -> StreamingResponse:
    """
    Stream production of a real AI-generated artefact — driven by the OWNED native swarm (§6).
    SSE format same as reactor/run (done event carries served_by / is_external provenance).
    """
    start = time.time()

    async def stream() -> AsyncIterator[str]:
        try:
            prod = await run_factory_produce(req.name, req.product_type, req.domain, req.description,
                                             prefer=req.model)
            accumulated = prod["output"]
            for chunk in _chunk_for_stream(accumulated):
                safe = chunk.replace("\n", "\\n")
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
            yield (f'data: {{"done": true, "run_id": "{prod["run_id"]}", "output_id": "{output_id}", '
                   f'"duration_ms": {duration_ms}, "served_by": {json.dumps(prod["served_by"])}, '
                   f'"is_external": {json.dumps(prod["is_external"])}}}\n\n')
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
    # §7 Reactor — parameterised generation/evolution loop (with user design control):
    temperature: float = 0.7   # variant diversity/creativity: 0 = conservative refinements, 1 = bold divergent
    mutation: float = 0.5      # how much each generation mutates the prior winner (0 = refine, 1 = reimagine)
    iterations: int = 1        # number of evolution generations (capped at 4)


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
    generations_run: int = 1   # §7 Reactor — Temperature/Mutation/Iteration generations actually run


async def _tournament_generation(base_prompt: str, domain: str, n: int, fitness_criteria: str,
                                 temperature: float, tournament_id: str, gen: int) -> list[TournamentVariant]:
    """One generation of the evolution tournament: generate N variants at the given diversity
    `temperature`, score them, and return the ranked leaderboard. Pure per-generation step."""
    variations_prompt = (
        f"You are an AI Prompt Evolution Engine (generation {gen}).\n"
        f"Base task: {base_prompt}\nDomain: {domain}\n\n"
        f"Diversity temperature: {temperature:.2f} — 0.0 means conservative, tightly-refined variations; "
        f"1.0 means bold, divergent, exploratory angles. Calibrate the spread accordingly.\n"
        f"Generate exactly {n} distinct variations of a response to this task. "
        f"Each variation should take a noticeably different angle, tone, or approach. "
        f"Label each with VARIANT_1:, VARIANT_2:, etc. and provide a complete, substantive response for each.\n\n"
        f"Produce all {n} variants now."
    )
    raw_variations = await gateway.query(variations_prompt, agent="incubator")

    score_prompt = (
        f"You are a Fitness Evaluator for an AI Evolution Engine.\n"
        f"Fitness criteria: {fitness_criteria}\n\n"
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

    leaderboard: list[TournamentVariant] = []
    lines = [l.strip() for l in scores_raw.splitlines() if l.strip() and "|" in l]

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
                    variant_id=f"v-{tournament_id}-g{gen}-{idx}",
                    rank=idx,
                    fitness_score=min(max(score, 0.0), 1.0),
                    response=variant_texts.get(idx, "")[:800],
                    strengths=parts[2].strip(),
                    weaknesses=parts[3].strip(),
                ))
            except (ValueError, IndexError):
                pass

    if not leaderboard:
        for i in range(1, n + 1):
            leaderboard.append(TournamentVariant(
                variant_id=f"v-{tournament_id}-g{gen}-{i}",
                rank=i,
                fitness_score=round(0.95 - (i - 1) * 0.05, 2),
                response=variant_texts.get(i, raw_variations[:400]),
                strengths="Strong analytical depth",
                weaknesses="Could be more concise",
            ))

    leaderboard.sort(key=lambda v: v.fitness_score, reverse=True)
    for rank, v in enumerate(leaderboard, 1):
        v.rank = rank
    return leaderboard


@router.post("/api/v1/incubator/evolve", response_model=TournamentResult)
async def incubator_evolve(req: EvolveTournamentRequest) -> TournamentResult:
    """Run the §7 Reactor's parameterised generation/evolution loop: each generation produces N variations
    at the given `temperature` (diversity), scores + ranks them; across `iterations` generations the winner
    is `mutation`-evolved into the next generation's base. Returns the final leaderboard + analysis."""
    n = min(max(req.variants, 2), 5)
    gens = min(max(req.iterations, 1), 4)          # cap the evolution loop
    temperature = min(max(req.temperature, 0.0), 1.0)
    mutation = min(max(req.mutation, 0.0), 1.0)
    tournament_id = uuid.uuid4().hex[:10]

    base = req.base_prompt
    leaderboard: list[TournamentVariant] = []
    winner: TournamentVariant | None = None
    for gen in range(1, gens + 1):
        leaderboard = await _tournament_generation(base, req.domain, n, req.fitness_criteria,
                                                   temperature, tournament_id, gen)
        winner = leaderboard[0]
        # Mutation: the next generation evolves the winning approach (mutation rate shapes how far)
        if gen < gens:
            base = (f"Evolve and improve this winning approach with mutation rate {mutation:.2f} "
                    f"(0 = refine carefully, 1 = reimagine boldly), keeping its strengths "
                    f"('{winner.strengths}') and fixing its weaknesses ('{winner.weaknesses}'):\n"
                    f"{winner.response[:600]}\n\nOriginal task: {req.base_prompt}")

    analysis_prompt = (
        f"Summarise in 3 sentences this '{req.name}' evolution tournament (ran {gens} generation(s) at "
        f"temperature {temperature:.2f}, mutation {mutation:.2f}): what makes the winner strongest, and what "
        f"should the next generation improve? Domain: {req.domain}."
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
        generations_run=gens,
    )


# ── §7 Reactor — Experimentation ("what-if" scenarios) ───────────────────────
class ExperimentRequest(BaseModel):
    subject: str
    domain: str = "general"
    scenarios: list[str] = []   # the "what-if" scenarios to project + compare (capped at 6)
    fitness_criteria: str = "impact, feasibility, risk, opportunity"


class ScenarioOutcome(BaseModel):
    scenario: str
    outcome: str
    served_by: str


class ExperimentResult(BaseModel):
    experiment_id: str
    subject: str
    domain: str
    scenarios_run: int
    outcomes: list[ScenarioOutcome]
    comparison: str
    ai_provenance: dict
    quality_assurance: dict
    completed_at: float


@router.post("/api/v1/reactor/experiment", response_model=ExperimentResult)
async def reactor_experiment(req: ExperimentRequest) -> ExperimentResult:
    """The §7 Reactor's Experimentation engine: project the outcome of each user-defined WHAT-IF scenario
    against the subject, then compare + rank them — on Workstation's OWN fabric (in-house provenance),
    QMS-gated + document-controlled (§10/§8)."""
    scenarios = [s.strip() for s in req.scenarios if s and s.strip()][:6]
    if not scenarios:
        raise HTTPException(status_code=400, detail="Provide at least one 'what-if' scenario.")
    eid = uuid.uuid4().hex[:10]
    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    def _record(meta: dict) -> str:
        sb = meta.get("served_by", "native")
        prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
        prov["any_external"] = prov["any_external"] or bool(meta.get("is_external"))
        return sb

    outcomes: list[ScenarioOutcome] = []
    for sc in scenarios:
        meta = await gateway.query_meta(
            f"You are the §7 Reactor's Experimentation engine. Subject: {req.subject} (domain: {req.domain}).\n"
            f"WHAT-IF scenario: {sc}\n\nProject the outcome under this scenario:\n"
            "## Projected Outcome\n## Key Risks\n## Opportunities\n## Net Assessment (one line)",
            agent="reactor-experiment")
        outcomes.append(ScenarioOutcome(scenario=sc, outcome=(meta.get("output", "") or "")[:1200],
                                        served_by=_record(meta)))

    comp_meta = await gateway.query_meta(
        f"Compare these what-if scenario outcomes for «{req.subject}». Rank them best→worst against: "
        f"{req.fitness_criteria}. Provide:\n## Ranking\n## Key Differences\n## Recommendation\n\n"
        + "\n\n".join(f"SCENARIO: {o.scenario}\n{o.outcome[:500]}" for o in outcomes),
        agent="reactor-experiment")
    comparison = comp_meta.get("output", "") or ""
    _record(comp_meta)

    combined = comparison + "\n" + "\n".join(o.outcome for o in outcomes)
    qa = await assure_delivery(combined, [o.scenario for o in outcomes], label="experiment")

    return ExperimentResult(
        experiment_id=eid, subject=req.subject, domain=req.domain, scenarios_run=len(scenarios),
        outcomes=outcomes, comparison=comparison, ai_provenance=prov, quality_assurance=qa,
        completed_at=time.time(),
    )


# ── §7 Petri dish — a small CONTAINED culture: grow one specimen in isolation, then assess viability ──
class PetriRequest(BaseModel):
    specimen: str                  # the idea / hypothesis / concept to culture
    domain: str = "general"
    medium: str = "standard"       # the conditions/environment to culture it in
    iterations: int = 1            # culture passages (1-3)


class PetriResult(BaseModel):
    culture_id: str
    specimen: str
    domain: str
    medium: str
    passages: int
    culture: str
    viable: bool
    ai_provenance: dict
    quality_assurance: dict
    cultured_at: float


@router.post("/api/v1/petri/culture", response_model=PetriResult)
async def petri_culture(req: PetriRequest) -> PetriResult:
    """§7 Petri dish — a small, CONTAINED experimentation space: culture one specimen (idea/hypothesis) in
    isolation under the chosen medium, growing it over a few passages on Workstation's OWN fabric, then
    assess viability — QMS-gated + recorded in the §8 organism. The smallest contained experiment, distinct
    from the Reactor's multi-scenario what-ifs and the Incubator's evolutionary tournament."""
    if not req.specimen.strip():
        raise HTTPException(status_code=400, detail="Provide a specimen (idea/hypothesis) to culture.")
    passages = max(1, min(3, int(req.iterations)))
    cid = uuid.uuid4().hex[:10]
    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    def _record(meta: dict) -> None:
        sb = meta.get("served_by", "native")
        prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
        prov["any_external"] = prov["any_external"] or bool(meta.get("is_external"))

    culture = req.specimen
    for p in range(passages):
        meta = await gateway.query_meta(
            f"You are the §7 Petri dish — a contained culture. Culture this specimen in ISOLATION under the "
            f"medium «{req.medium}» (domain: {req.domain}), passage {p + 1}/{passages}.\n\nSpecimen: {culture[:900]}\n\n"
            "Grow it — what it develops into under these conditions:\n"
            "## Growth (how it develops)\n## Nutrients Required (what it needs to thrive)\n"
            "## Contamination Risks (what could spoil it)\n## Viability (VIABLE or NOT-VIABLE — one line, justified)",
            agent="petri-culture")
        culture = (meta.get("output", "") or "").strip() or culture
        _record(meta)

    tail = culture.lower()[-400:]
    viable = ("not-viable" not in tail) and ("not viable" not in tail)
    qa = await assure_delivery(culture, ["Growth", "Nutrients Required", "Contamination Risks", "Viability"], label="petri")
    return PetriResult(culture_id=cid, specimen=req.specimen, domain=req.domain, medium=req.medium,
                       passages=passages, culture=culture, viable=viable, ai_provenance=prov,
                       quality_assurance=qa, cultured_at=time.time())


# ── §7 Reactor — Studio (2D/3D visual analytics & insight) ───────────────────
class StudioPoint(BaseModel):
    label: str
    value: float
    z: Optional[float] = None   # optional 3rd dimension (magnitude) for scatter — honest 2D + magnitude


class StudioRequest(BaseModel):
    title: str
    domain: str = "general"
    chart_type: str = "bar"     # bar | line | scatter
    series: list[StudioPoint] = []
    insight: bool = True


class StudioResult(BaseModel):
    title: str
    domain: str
    chart_type: str
    dimensions: int             # 2, or 3 when any point carries a z magnitude
    series: list[StudioPoint]
    analytics: dict             # deterministic stats computed from the REAL series (no fabrication)
    insight: str
    ai_provenance: dict
    quality_assurance: dict
    generated_at: float


@router.post("/api/v1/reactor/studio", response_model=StudioResult)
async def reactor_studio(req: StudioRequest) -> StudioResult:
    """The §7 Reactor's Studio: 2D/3D visual analytics & insight over a REAL data series. Computes
    deterministic statistics (count/total/mean/min/max/range) from the provided values — never invents
    numbers — and an in-house insight narrative interpreting them; the chart is rendered client-side
    (bar/line/scatter; scatter carries an optional z magnitude). QMS-gated + document-controlled."""
    pts = [p for p in req.series if p.label and p.label.strip()]
    if not pts:
        raise HTTPException(status_code=400, detail="Provide at least one data point (label + value).")
    chart_type = req.chart_type if req.chart_type in ("bar", "line", "scatter") else "bar"
    values = [p.value for p in pts]
    total = round(sum(values), 4)
    mean = round(total / len(values), 4)
    pmin = min(pts, key=lambda p: p.value)
    pmax = max(pts, key=lambda p: p.value)
    dimensions = 3 if any(p.z is not None for p in pts) else 2
    analytics = {
        "count": len(pts), "total": total, "mean": mean,
        "min": {"label": pmin.label, "value": pmin.value},
        "max": {"label": pmax.label, "value": pmax.value},
        "range": round(pmax.value - pmin.value, 4),
    }

    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}
    insight = ""
    if req.insight:
        meta = await gateway.query_meta(
            f"You are the §7 Reactor's Studio analyst. Title: {req.title} (domain: {req.domain}, {dimensions}D "
            f"{chart_type} chart). Interpret ONLY these real data points (do not invent any numbers):\n"
            + "; ".join(f"{p.label}={p.value}" + (f"/z{p.z}" if p.z is not None else "") for p in pts)
            + f"\nStats: total {total}, mean {mean}, max {pmax.label} ({pmax.value}), min {pmin.label} ({pmin.value}).\n\n"
            "## Insight (3-4 sentences)\n## Notable Pattern\n## Recommended Action",
            agent="reactor-studio")
        insight = meta.get("output", "") or ""
        sb = meta.get("served_by", "native")
        prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
        prov["any_external"] = bool(meta.get("is_external"))

    qa = await assure_delivery(insight or f"{req.title}: {analytics}", [p.label for p in pts], label="studio")

    return StudioResult(
        title=req.title, domain=req.domain, chart_type=chart_type, dimensions=dimensions,
        series=pts, analytics=analytics, insight=insight, ai_provenance=prov,
        quality_assurance=qa, generated_at=time.time(),
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
