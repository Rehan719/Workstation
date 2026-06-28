"""
Business Development Process Intelligence Engine (BDP)
Scientific Process Intelligence Engine (SPI)
Authorship Processes Intelligence Engine (APIE)
Design & Development Processes Intelligence Engine (DDPIE)

Four purpose-built intelligence engines using the full cognitive stack —
nine engines + MJM + GaaS — to produce high-quality structured outputs.

BDP — Business Development Process (8 stages):
  market analysis → value proposition → go-to-market → revenue model → risk

SPI — Scientific Process Intelligence (8 stages):
  hypothesis → literature → methodology → experiment → analysis → publication

APIE — Authorship Processes Intelligence (9 stages):
  source discovery → argument architecture → outline → draft → evidence weaving →
  peer review simulation → revision intelligence → integrity audit → publication readiness

DDPIE — Design & Development Processes Intelligence (9 stages):
  requirements → architecture → domain modelling → API contract → security →
  implementation blueprint → test strategy → devops pipeline → technical review

  POST /api/v1/intelligence/bdp         — run BDP engine
  POST /api/v1/intelligence/spi         — run SPI engine
  POST /api/v1/intelligence/authorship  — run APIE engine
  POST /api/v1/intelligence/design-dev  — run DDPIE engine
  POST /api/v1/intelligence/solve       — general problem-solving with cognitive stack
  GET  /api/v1/intelligence/status      — engine status and capabilities
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
        "Deliver a rigorous, investor-grade market analysis:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Market Size (TAM / SAM / SOM with specific £/$ estimates and methodology)\n"
        "## Market Segmentation (3-5 distinct segments ranked by opportunity)\n"
        "## Competitive Landscape (top 5 competitors: strengths, weaknesses, market share)\n"
        "## Market Trends & Tailwinds (3-5 structural forces favouring this opportunity)\n"
        "## Market Timing (why now — what has changed in the last 2 years)\n"
        "## Barriers to Entry (what protects a well-positioned entrant)\n"
        "## Win Strategy (the 1 asymmetric advantage that makes this winnable)\n"
    ),
    "value_proposition": (
        "You are the Chief Product Officer of Workstation IDBO. "
        "Define a breakthrough value proposition:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Core Problem (the painful, expensive, urgent problem being solved)\n"
        "## Unique Solution (what is built and exactly how it solves the problem)\n"
        "## Key Differentiators (3 reasons this is genuinely better than alternatives)\n"
        "## Customer Value by Segment (specific value for each of the 3 key segments)\n"
        "## Proof Points (evidence the solution works — early data, analogies, case studies)\n"
        "## Value Proposition Statement (one sentence: For [who] who [need], [product] is [category] that [benefit]. Unlike [alternative], [product] [key differentiator].)\n"
        "## Jobs-to-be-Done Map (functional, emotional, social jobs this product fulfils)\n"
    ),
    "customer_discovery": (
        "You are the CMO leading customer discovery. Map the customer landscape:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Ideal Customer Profile (ICP) — firmographics, psychographics, technographics\n"
        "## Primary Persona (full profile: name, role, goals, frustrations, day-in-life)\n"
        "## Secondary Persona (second most important buyer/user)\n"
        "## Jobs-to-be-Done (functional job, emotional job, social job with specific examples)\n"
        "## Pain Points Hierarchy (ranked by severity and frequency — top 6 pains)\n"
        "## Buyer Journey Map (Awareness → Consideration → Decision → Onboarding → Expansion)\n"
        "## Willingness-to-Pay Signals (pricing anchors, budget cycles, decision-making criteria)\n"
        "## Early Adopter Profile (the precise segment to target in month 1-3)\n"
    ),
    "business_model": (
        "You are the CFO designing the complete business model:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Revenue Streams (all revenue streams with % of total revenue projection)\n"
        "## Pricing Strategy (pricing model, tiers, anchoring, freemium/trial logic)\n"
        "## Unit Economics (CAC, LTV, Payback Period, LTV:CAC ratio — with methodology)\n"
        "## Cost Structure (fixed costs, variable costs, COGS, key cost drivers)\n"
        "## Key Partnerships (3-5 critical partners — what each unlocks)\n"
        "## Key Resources (AI, data, IP, talent — what is essential to deliver value)\n"
        "## Financial Projections (Month 1, 3, 6, 12, 24, 36 — revenue, customers, burn)\n"
        "## Break-Even Analysis (when and at what revenue/volume level)\n"
    ),
    "go_to_market": (
        "You are the CMO designing the go-to-market strategy:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## GTM Motion (PLG / SLG / Channel-led / Hybrid — justify for this market)\n"
        "## Beachhead Market (the one segment to win first and why)\n"
        "## Launch Sequence (pre-launch → launch → post-launch — week-by-week for 12 weeks)\n"
        "## Acquisition Channels (ranked by expected CAC, volume, and strategic value)\n"
        "## First 100 Customers Plan (exactly how to acquire the first 100 paying customers)\n"
        "## Content & Thought Leadership Strategy (owned media, SEO, community)\n"
        "## Partnerships & Distribution Leverage (channel partners, integrations, co-selling)\n"
        "## 90-Day Commercial Targets (specific KPIs with numbers for revenue, pipeline, CAC)\n"
    ),
    "financial_model": (
        "You are the CFO building the financial model:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Revenue Model Architecture (how revenue scales with customers and usage)\n"
        "## Year 1 Monthly Projection (M1-M12: customers, MRR, churn, net revenue)\n"
        "## Year 2-3 Annual Projection (ARR, growth rate, gross margin, EBITDA trajectory)\n"
        "## Cost Breakdown (headcount, infrastructure, sales & marketing, G&A — phased)\n"
        "## Monthly Cash Burn Rate (by phase: pre-product, MVP, growth)\n"
        "## Break-Even Analysis (revenue and customer count to reach cash-flow positive)\n"
        "## Funding Requirements (total raise, use of funds, runway, key milestones unlocked)\n"
        "## Key Assumptions & Sensitivities (top 5 assumptions; bull/base/bear scenarios)\n"
    ),
    "risk_assessment": (
        "You are the CLO and COO conducting risk assessment:\n\n"
        "Business: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Top 5 Business Risks (probability × impact matrix with specific mitigations)\n"
        "## Regulatory & Compliance Risks (jurisdiction-specific legal exposure)\n"
        "## Technical & Product Risks (build risk, integration risk, scalability risk)\n"
        "## Market & Competitive Risks (demand risk, competitive response, timing risk)\n"
        "## Team & Execution Risks (key person dependency, capability gaps, culture)\n"
        "## Contingency Plans (trigger conditions and response for each top risk)\n"
        "## Risk Score Card (overall risk rating: 1-10 per dimension)\n"
        "## Risk Mitigation Roadmap (priority order and timeline for risk reduction)\n"
    ),
    "executive_summary": (
        "You are the AI CEO synthesising a compelling investor-ready executive summary.\n\n"
        "Business: {challenge}\nDomain: {domain}\n"
        "Full analysis: {context}\n\n"
        "## The Opportunity (the problem, why it matters, why now)\n"
        "## The Solution (what it is, how it works, why it's 10x better)\n"
        "## Market (TAM/SAM/SOM, target segment, market timing)\n"
        "## Business Model (revenue model, unit economics, margin profile)\n"
        "## Traction & Validation (early evidence, customers, metrics)\n"
        "## Competitive Advantage (the moat — what makes this defensible)\n"
        "## Team (key people, relevant experience, unfair advantages)\n"
        "## The Ask & Use of Funds (amount, milestones, runway)\n"
        "## 12-Month Vision (where this is in 12 months if funded)\n"
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
        "You are a Senior Research Scientist and epistemologist. Formulate the research problem:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Refined Research Question (PICO/SPIDER/FINER format — precise, answerable, novel)\n"
        "## Conceptual Framework (theoretical lens / disciplinary paradigm)\n"
        "## Key Variables & Operational Definitions (independent, dependent, confounding)\n"
        "## Scope & Boundaries (what is in vs out of scope — temporal, geographic, population)\n"
        "## Scientific Significance (why this question matters — contribution to the field)\n"
        "## Practical Significance (real-world applications if answered)\n"
        "## Research Feasibility Assessment (time, resource, ethical feasibility — 1-10 each)\n"
        "## Ontological & Epistemological Stance (positivist/interpretivist/pragmatist — justify)\n"
    ),
    "literature_synthesis": (
        "You are the Chief Scientific Officer conducting a systematic literature synthesis:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Foundational Theories & Frameworks (seminal theoretical works underpinning this field)\n"
        "## Key Established Findings (what the evidence robustly shows — with effect sizes where relevant)\n"
        "## Leading Methodological Approaches (dominant research designs in this area)\n"
        "## Current Evidence Gaps (what is genuinely unknown or under-researched)\n"
        "## Contradictions & Contested Areas (where evidence conflicts and why)\n"
        "## Influential Scholars & Schools of Thought (who shapes this field and how)\n"
        "## Emerging Research Directions (what is being published now — frontier topics)\n"
        "## Synthesis Map (how existing evidence clusters and what it collectively suggests)\n"
    ),
    "hypothesis_generation": (
        "You are a Research Scientist generating rigorous hypotheses:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Null Hypothesis H0 (precise, testable, falsifiable)\n"
        "## Alternative Hypothesis H1 (directional prediction with rationale)\n"
        "## Secondary Hypotheses (2-3 subsidiary hypotheses to test)\n"
        "## Mechanistic Model (proposed causal mechanism linking variables)\n"
        "## Effect Size Prediction (expected magnitude and direction with justification)\n"
        "## Key Assumptions (5 assumptions that must hold for the hypotheses to be valid)\n"
        "## Feasibility Assessment (technical, ethical, resource feasibility — 1-10 each)\n"
        "## Hypothesis Prioritisation (which to test first and why)\n"
    ),
    "methodology_design": (
        "You are the Study Design Lead. Design the optimal research methodology:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Study Design Selection (RCT/cohort/case-control/systematic review/mixed-methods — justify)\n"
        "## Sample Design (population, sampling strategy, sample size calculation with power analysis)\n"
        "## Inclusion & Exclusion Criteria (precise eligibility with rationale)\n"
        "## Intervention / Exposure Design (what happens to participants — protocol detail)\n"
        "## Control Conditions & Blinding (control group design, blinding strategy)\n"
        "## Data Collection Protocol (instruments, procedures, timing, quality checks)\n"
        "## Timeline & Phases (Gantt-style: phase 1-4 with milestones and deliverables)\n"
        "## Ethical Considerations (consent, data protection, risk minimisation, IRB requirements)\n"
        "## Limitations & Mitigation (design limitations and how to address them)\n"
    ),
    "data_strategy": (
        "You are the Data Science Lead defining the data and analysis strategy:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Primary Data Sources (where data comes from — with quality and availability assessment)\n"
        "## Secondary Data Sources (existing datasets to leverage)\n"
        "## Measurement Instruments (validated scales, sensors, tools — psychometric properties)\n"
        "## Primary Statistical Analysis Plan (main analysis approach with software)\n"
        "## Secondary Analyses (subgroup analyses, sensitivity analyses, exploratory analyses)\n"
        "## Data Quality Framework (missing data strategy, outlier handling, cleaning protocol)\n"
        "## Bias Mitigation Strategy (selection bias, information bias, confounding — controls)\n"
        "## Data Governance Plan (storage, access control, retention, GDPR compliance)\n"
        "## Reporting Standards (CONSORT/STROBE/PRISMA/etc. — applicable checklist)\n"
    ),
    "validation_plan": (
        "You are the Research Quality and Reproducibility Officer:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Internal Validity Assessment (threats: selection, attrition, maturation, instrumentation)\n"
        "## External Validity & Generalisability (population, ecological, temporal validity)\n"
        "## Construct Validity (are instruments measuring what we claim — convergent/discriminant)\n"
        "## Statistical Conclusion Validity (power, multiple comparisons, effect size reporting)\n"
        "## Replication Strategy (pre-registration, open data, materials — reproducibility plan)\n"
        "## Pre-Registration Plan (OSF/ClinicalTrials.gov — what to pre-register and when)\n"
        "## Peer Review Pathway (target reviewers, open vs closed review preference)\n"
        "## Adversarial Collaboration (who might challenge findings and how to pre-empt)\n"
        "## Quality Score (1-10 across all validity dimensions with improvement actions)\n"
    ),
    "impact_assessment": (
        "You are the Chief Impact Officer assessing research significance:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Scientific Contribution (how this advances theory and methodology in the field)\n"
        "## Clinical / Practical Application (direct applications if findings are positive)\n"
        "## Policy Implications (how findings could influence policy — with specific policy levers)\n"
        "## Societal Impact (broader social, economic, cultural implications)\n"
        "## Commercial Potential (IP, spin-out, licensing, industry partnership opportunities)\n"
        "## Ethical Impact (potential harms, dual-use concerns, equity implications)\n"
        "## Impact Timeline (when impacts materialise: 1 year / 5 years / 10 years)\n"
        "## Impact Metrics (Research Excellence Framework / Altmetrics / citation prediction)\n"
        "## Impact Maximisation Actions (3 high-leverage activities to amplify research impact)\n"
    ),
    "dissemination_plan": (
        "You are the Research Communication and Knowledge Translation Lead:\n\n"
        "Research Question: {challenge}\nDomain: {domain}\nContext: {context}\n\n"
        "## Primary Publication Target (journal/venue: impact factor, audience, fit, timeline)\n"
        "## Secondary Outlets (3 additional venues for different audiences)\n"
        "## Conference Presentation Strategy (which conferences, abstract deadlines, format)\n"
        "## Open Access Strategy (gold/green/diamond OA — repository, preprint server, licence)\n"
        "## Data Sharing Plan (which data to share, where, with what restrictions)\n"
        "## Non-Academic Dissemination (policy briefs, media, public engagement, social media)\n"
        "## Knowledge Translation to Practice (how findings reach practitioners and services)\n"
        "## Publication Timeline (pre-print → submission → revision → acceptance — month-by-month)\n"
        "## Impact Tracking Plan (how to monitor citations, policy uptake, media coverage)\n"
    ),
}


# ── AI-powered cognitive + MJM helpers ───────────────────────────────────────

# §7 — the cognitive engines as a reconfigurable catalogue: users can select WHICH engines run.
_COGNITIVE_LENSES = [
    ("inkashaf",  "INKASHAF (Pattern Discovery & Revelation)",
     "What hidden patterns, structures, and non-obvious connections does this reveal? What is the deep nature of this challenge?"),
    ("samajh",    "SAMAJH (Deep Comprehension & Contextual Understanding)",
     "What is the true meaning, context, and full implication of this problem? What are we really dealing with beneath the surface?"),
    ("soch",      "SOCH (Reflective Thinking & Hypothesis Generation)",
     "What hypotheses, alternative framings, and creative interpretations emerge? What are we not yet considering?"),
    ("aqal",      "AQAL (Logical Reasoning & Strategic Planning)",
     "What is the optimal logical structure for addressing this? What reasoning path leads to the most rigorous outcome?"),
    ("hoshiyari", "HOSHIYARI (Anomaly Detection & Risk Intelligence)",
     "What risks, blind spots, biases, and failure modes must we guard against? What could go wrong that we are not seeing?"),
    ("iman",      "IMAN (Values Alignment & Ethical Conviction)",
     "Does this align with ethical principles, mission, and human flourishing? What values must guide the approach?"),
]


async def _ai_cognitive_prime(problem: str, domain: str, engines: list | None = None) -> str:
    """Run the cognitive engines (Inkashaf→Samajh→Soch→Aqal→Hoshiyari→Iman) as real AI analysis.
    §7 user design control: `engines` (subset of the lens ids) reconfigures WHICH engines run; the default
    (None/empty) runs all six (backward-compatible). Single in-house-first gateway call."""
    wanted = {str(e).lower() for e in (engines or [])}
    sel = [e for e in _COGNITIVE_LENSES if (not wanted or e[0] in wanted)] or _COGNITIVE_LENSES
    lenses = "".join(f"## {name}\n{q}\n\n" for _id, name, q in sel)
    prompt = (
        f"You are the Cognitive Architecture — {len(sel)} specialised intelligence systems operating in "
        "biological cascade sequence. Analyse the following through each lens:\n\n"
        f"Problem: {problem}\nDomain: {domain}\n\n"
        f"{lenses}"
        "For each engine, provide 3-4 sharp, specific insights. Be concrete and analytical."
    )
    try:
        return await gateway.query(prompt, agent="cognitive_cascade_ai")
    except Exception as e:
        return f"Cognitive priming: {e}"


async def _ai_mjm_lifecycle(problem: str, domain: str, cognitive_context: str) -> str:
    """
    MJM Orchestrator (Mushahida-Jaiza-Muaina) as real AI analysis.
    Takes the cognitive cascade output as input for deeper meta-assessment.
    """
    prompt = (
        "You are the MJM Orchestrator — the meta-judgement system operating above the cognitive engines. "
        "Process this through the three phases of Mushahida-Jaiza-Muaina:\n\n"
        f"Problem: {problem}\nDomain: {domain}\n"
        f"Cognitive Intelligence Input:\n{cognitive_context[:1200]}\n\n"
        "## MUSHAHIDA (Witnessed Observation — الملاحظة)\n"
        "After witnessing the full cognitive analysis: what is the true nature and essence of this challenge? "
        "What observation, when made clearly, changes how we must approach this?\n\n"
        "## JAIZA (Deep Assessment — التقييم)\n"
        "Having comprehensively assessed all dimensions: what is your authoritative evaluation? "
        "What is the definitive judgement on priority, feasibility, and strategic direction?\n\n"
        "## MUAINA (Verified Action — التحقق)\n"
        "Having observed and assessed: what are the 3-5 verified, confident action directives? "
        "State each with the confidence level (%), the evidence basis, and the first concrete step.\n\n"
        "## MJM SYNTHESIS\n"
        "In 2-3 sentences: the single most important insight from this full MJM lifecycle, "
        "and the overarching direction it prescribes."
    )
    try:
        return await gateway.query(prompt, agent="mjm_orchestrator_ai")
    except Exception as e:
        return f"MJM assessment: {e}"


async def _run_intelligence_stream(
    challenge: str,
    domain: str,
    stages: list,
    prompts: dict,
    engine_name: str,
    cognitive_context: str = "",
    mjm_context: str = "",
    rigor: str = "standard",
    focus: str = "",
):
    """Generic SSE stream for BDP/SPI engines with optional cognitive + MJM context injection.
    §7 user design control: `rigor` (standard|rigorous|exhaustive) and `focus` (lens) genuinely steer the
    analysis — woven into every stage's directives, honored at run time (not decorative)."""
    context_accumulator = ""

    def _ev(stage: str, label: str, content: str, data: dict | None = None) -> str:
        payload: dict = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {json.dumps(payload)}\n\n"

    yield _ev("init", f"{engine_name} Initiated", f"Processing: {challenge[:120]}")

    # Structural cascade prime (fast — returns stubs confirming cascade is active)
    try:
        await _cascade.execute_cascade({"problem": challenge, "domain": domain})
    except Exception:
        pass
    yield _ev("cognitive_prime", "Cognitive Priming", cognitive_context or "Cognitive engines primed.")

    # §7 reconfiguration — rigor + focus genuinely steer every stage (woven into the shared directives).
    _RIGOR = {
        "standard": "",
        "rigorous": "Apply RIGOROUS analytical depth: justify each claim with evidence/reasoning and weigh counter-arguments.",
        "exhaustive": "Apply EXHAUSTIVE depth: be comprehensive — justify every claim with evidence, weigh "
                      "alternatives and counter-arguments, and surface edge cases and second-order effects.",
    }
    directives = ""
    _rd = _RIGOR.get((rigor or "standard").lower(), "")
    if _rd:
        directives += f"\n\nANALYSIS DIRECTIVE ({rigor}): {_rd}"
    if focus and focus.strip():
        directives += f"\n\nFOCUS LENS: weight the analysis toward — {focus.strip()}"
    yield _ev("config", "Reconfiguration", f"rigor={rigor or 'standard'}" + (f" · focus: {focus.strip()}" if focus and focus.strip() else ""))

    enrichment = directives
    if cognitive_context:
        enrichment += f"\n\nCOGNITIVE INTELLIGENCE:\n{cognitive_context[:600]}"
    if mjm_context:
        enrichment += f"\n\nMJM ASSESSMENT:\n{mjm_context[:400]}"

    for stage_key, stage_label, stage_desc in stages:
        yield _ev(f"{stage_key}_start", stage_label, stage_desc)

        prompt_template = prompts.get(stage_key, "")
        if not prompt_template:
            continue

        prompt = prompt_template.format(
            challenge=challenge,
            domain=domain,
            context=(context_accumulator[-600:] if context_accumulator else "") + enrichment,
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
    # §7 user design control — genuinely reconfigure the engine's behaviour (honored at run time):
    rigor: str = "standard"   # standard | rigorous | exhaustive — analytical depth/evidence demand
    focus: str = ""           # optional lens the analysis is weighted toward


class SolveRequest(BaseModel):
    problem: str
    domain: str = "general"
    context: str = ""
    engines: list[str] = []   # §7 — select which cognitive engines run (empty = all six)


@router.get("/cognitive-engines")
async def cognitive_engines_catalogue():
    """§7 — the reconfigurable cognitive-engine catalogue: the lenses users can select for the cascade."""
    return {"engines": [{"id": e[0], "name": e[1]} for e in _COGNITIVE_LENSES],
            "note": "Select any subset for /solve (or the cascade); empty = all run."}


@router.post("/bdp")
async def business_development_process(req: IntelligenceRequest):
    """
    Business Development Process Intelligence Engine.
    Full structured BD analysis via agent cascade, streamed as SSE.
    """
    return StreamingResponse(
        _run_intelligence_stream(req.challenge, req.domain, _BDP_STAGES, _BDP_PROMPTS, "BDP",
                                 rigor=req.rigor, focus=req.focus),
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
        _run_intelligence_stream(req.challenge, req.domain, _SPI_STAGES, _SPI_PROMPTS, "SPI",
                                 rigor=req.rigor, focus=req.focus),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/solve")
async def solve_with_cognitive_stack(req: SolveRequest):
    """
    Full cognitive stack synthesis. Now returns AI-powered Cognitive cascade + MJM +
    final synthesis — all three layers user-visible with structured sections.
    """
    cognitive_analysis = await _ai_cognitive_prime(req.problem, req.domain, req.engines)
    mjm_assessment = await _ai_mjm_lifecycle(req.problem, req.domain, cognitive_analysis)

    synthesis_prompt = (
        "You are the IDBO Synthesis Engine integrating all intelligence layers.\n\n"
        f"Problem: {req.problem}\nDomain: {req.domain}\n"
        + (f"User context: {req.context}\n" if req.context else "")
        + f"\nCognitive Cascade Analysis (6 engines):\n{cognitive_analysis[:1200]}\n"
        f"\nMJM Assessment (Mushahida-Jaiza-Muaina):\n{mjm_assessment[:800]}\n\n"
        "Deliver an integrated synthesis:\n"
        "## Core Insight (the single most important truth revealed by the analysis)\n"
        "## Root Cause Analysis (what is really happening beneath the surface)\n"
        "## Recommended Approach (the optimal path forward — specific, actionable)\n"
        "## Priority Action Steps (5 concrete actions in priority order)\n"
        "## Success Criteria (how we know it worked — measurable outcomes)\n"
        "## Risks & Mitigations (top 3 risks with specific countermeasures)\n"
        "## Synergistic Opportunities (what cross-domain or cross-engine insights open up)"
    )
    try:
        synthesis = await gateway.query(synthesis_prompt, agent="cognitive_solve")
    except Exception as e:
        synthesis = f"Synthesis: {e}"

    return {
        "problem": req.problem,
        "domain": req.domain,
        "cognitive_cascade": cognitive_analysis,
        "mjm_assessment": mjm_assessment,
        "synthesis": synthesis,
        "status": "complete",
        "engines_used": ["Inkashaf", "Samajh", "Soch", "Aqal", "Hoshiyari", "Iman", "MJM", "AIGateway"],
    }


# ── Synthesis Nexus — cross-engine autonomous chaining ────────────────────────

_ENGINE_MAP = {
    "bdp":     (_BDP_STAGES, _BDP_PROMPTS),
    "spi":     (_SPI_STAGES, _SPI_PROMPTS),
}

_ACTIVITY_ENGINE = {
    "synthesis":   "bdp",
    "research":    "spi",
    "authorship":  "apie",
    "development": "ddpie",
    "auto":        "auto",
}


class NexusRequest(BaseModel):
    challenge: str
    domain: str = "enterprise"
    activity: str = "auto"   # synthesis | research | authorship | development | auto
    engines: list[str] = []  # explicit override: ["bdp", "spi", "apie", "ddpie"]
    # APIE fields (if authorship selected)
    genre: str = "academic paper"
    audience: str = "academic peers"
    citation_style: str = "APA"
    word_count: str = "8000"
    # DDPIE fields (if development selected)
    tech_stack: str = "Python / FastAPI / React / PostgreSQL"
    scale: str = "startup"
    deployment_target: str = "cloud"


async def _nexus_auto_select(challenge: str, domain: str, cognitive_result: str) -> str:
    """Autonomously select the optimal primary engine based on input + cognitive analysis."""
    prompt = (
        "You are an intelligence router. Based on the challenge and cognitive analysis below, "
        "select the single most appropriate intelligence engine.\n\n"
        f"Challenge: {challenge}\nDomain: {domain}\n"
        f"Cognitive analysis excerpt: {cognitive_result[:400]}\n\n"
        "Available engines:\n"
        "- bdp: Business Development Process (market analysis, GTM, financial modelling, revenue)\n"
        "- spi: Scientific Process Intelligence (research, experiments, hypotheses, data)\n"
        "- apie: Authorship & Scholarship (writing, papers, academic documents, literature)\n"
        "- ddpie: Design & Development (software, systems, architecture, engineering)\n\n"
        "Respond with ONLY one of: bdp, spi, apie, ddpie"
    )
    try:
        result = (await gateway.query(prompt, agent="nexus_router")).strip().lower()
        for engine in ["bdp", "spi", "apie", "ddpie"]:
            if engine in result:
                return engine
    except Exception:
        pass
    return "bdp"


async def _run_nexus_stream(req: NexusRequest):
    """Full autonomous synergistic nexus — cognitive → MJM → primary engine → unified synthesis."""

    def _ev(stage: str, label: str, content: str, data: dict | None = None) -> str:
        payload: dict = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {json.dumps(payload)}\n\n"

    yield _ev("init", "Nexus Initiated", f"Autonomous synergistic pipeline: {req.challenge[:100]}")

    # ── Layer 1: AI Cognitive Cascade (6 engines) ─────────────────────────────
    yield _ev("cognitive_start", "Cognitive Cascade", "Six cognitive engines activating: Inkashaf → Samajh → Soch → Aqal → Hoshiyari → Iman")
    cognitive_result = await _ai_cognitive_prime(req.challenge, req.domain)
    yield _ev("cognitive_complete", "Cognitive Cascade Complete", cognitive_result, {
        "engines": ["Inkashaf", "Samajh", "Soch", "Aqal", "Hoshiyari", "Iman"],
        "layer": 1,
    })

    # ── Layer 2: MJM Meta-Assessment ──────────────────────────────────────────
    yield _ev("mjm_start", "MJM Assessment", "Mushahida-Jaiza-Muaina meta-judgement integrating cognitive outputs")
    mjm_result = await _ai_mjm_lifecycle(req.challenge, req.domain, cognitive_result)
    yield _ev("mjm_complete", "MJM Complete", mjm_result, {
        "phases": ["Mushahida", "Jaiza", "Muaina"],
        "layer": 2,
    })

    # ── Engine selection ──────────────────────────────────────────────────────
    selected_engine = req.engines[0] if req.engines else _ACTIVITY_ENGINE.get(req.activity, "auto")
    if selected_engine == "auto":
        yield _ev("routing", "Intelligent Routing", "Autonomously selecting optimal engine...")
        selected_engine = await _nexus_auto_select(req.challenge, req.domain, cognitive_result)
    yield _ev("engine_selected", "Engine Selected", f"Primary engine: {selected_engine.upper()}", {
        "engine": selected_engine,
        "layer": 3,
    })

    # ── Layer 3: Primary engine with cognitive + MJM enrichment ──────────────
    if selected_engine == "apie":
        context_accumulator = ""
        enrichment = f"\n\nCOGNITIVE INTELLIGENCE:\n{cognitive_result[:500]}\nMJM ASSESSMENT:\n{mjm_result[:300]}"
        for i, (stage_key, stage_label, stage_desc) in enumerate(_APIE_STAGES):
            yield _ev(f"{stage_key}_start", stage_label, stage_desc)
            prompt_template = _APIE_PROMPTS.get(stage_key, "")
            if not prompt_template:
                continue
            prompt = prompt_template.format(
                topic=req.challenge, domain=req.domain, genre=req.genre,
                audience=req.audience, citation_style=req.citation_style,
                word_count=req.word_count,
                context=(context_accumulator[-400:] if context_accumulator else "") + enrichment,
            )
            try:
                result = await gateway.query(prompt, agent=f"nexus_apie_{stage_key}")
            except Exception as e:
                result = f"[{stage_label} — {e}]"
            context_accumulator += f"\n\n## {stage_label}\n{result[:500]}"
            yield _ev(stage_key, stage_label, result, {"stage_num": i + 1, "total": len(_APIE_STAGES)})

    elif selected_engine == "ddpie":
        context_accumulator = ""
        enrichment = f"\n\nCOGNITIVE INTELLIGENCE:\n{cognitive_result[:500]}\nMJM ASSESSMENT:\n{mjm_result[:300]}"
        for i, (stage_key, stage_label, stage_desc) in enumerate(_DDPIE_STAGES):
            yield _ev(f"{stage_key}_start", stage_label, stage_desc)
            prompt_template = _DDPIE_PROMPTS.get(stage_key, "")
            if not prompt_template:
                continue
            prompt = prompt_template.format(
                system=req.challenge, domain=req.domain, tech_stack=req.tech_stack,
                scale=req.scale, deployment_target=req.deployment_target,
                context=(context_accumulator[-400:] if context_accumulator else "") + enrichment,
            )
            try:
                result = await gateway.query(prompt, agent=f"nexus_ddpie_{stage_key}")
            except Exception as e:
                result = f"[{stage_label} — {e}]"
            context_accumulator += f"\n\n## {stage_label}\n{result[:500]}"
            yield _ev(stage_key, stage_label, result, {"stage_num": i + 1, "total": len(_DDPIE_STAGES)})

    else:
        # BDP or SPI
        stages, prompts = _ENGINE_MAP.get(selected_engine, (_BDP_STAGES, _BDP_PROMPTS))
        context_accumulator = ""
        enrichment = f"\n\nCOGNITIVE INTELLIGENCE:\n{cognitive_result[:500]}\nMJM ASSESSMENT:\n{mjm_result[:300]}"
        for i, (stage_key, stage_label, stage_desc) in enumerate(stages):
            yield _ev(f"{stage_key}_start", stage_label, stage_desc)
            prompt_template = prompts.get(stage_key, "")
            if not prompt_template:
                continue
            prompt = prompt_template.format(
                challenge=req.challenge, domain=req.domain,
                context=(context_accumulator[-400:] if context_accumulator else "") + enrichment,
            )
            try:
                result = await gateway.query(prompt, agent=f"nexus_{selected_engine}_{stage_key}")
            except Exception as e:
                result = f"[{stage_label} — {e}]"
            context_accumulator += f"\n\n## {stage_label}\n{result[:500]}"
            yield _ev(stage_key, stage_label, result, {"stage_num": i + 1, "total": len(stages)})

    # ── Layer 4: Nexus Synthesis (integrates all layers) ─────────────────────
    yield _ev("synthesis_start", "Nexus Synthesis", "Integrating cognitive, MJM, and engine outputs into unified intelligence")
    synthesis_prompt = (
        f"You are the IDBO Synthesis Nexus — the apex intelligence layer.\n\n"
        f"Challenge: {req.challenge}\nDomain: {req.domain}\nEngine: {selected_engine.upper()}\n\n"
        f"Cognitive Cascade (6 engines):\n{cognitive_result[:800]}\n\n"
        f"MJM Assessment:\n{mjm_result[:600]}\n\n"
        "Deliver the Nexus Synthesis:\n"
        "## Cross-Engine Synthesis (what all intelligence layers collectively reveal)\n"
        "## Highest-Leverage Insight (the one finding that changes everything)\n"
        "## Integrated Action Blueprint (concrete next steps drawing on ALL engines)\n"
        "## Emergent Opportunities (what synergistic combinations make possible)\n"
        "## Coherence Assessment (how well the findings align — and where tensions exist)\n"
        "## Sovereign Recommendation (the definitive direction this intelligence prescribes)"
    )
    try:
        synthesis = await gateway.query(synthesis_prompt, agent="nexus_synthesis")
    except Exception as e:
        synthesis = f"Synthesis: {e}"

    yield _ev("nexus_complete", "Nexus Complete", synthesis, {
        "engine_used": selected_engine,
        "layers_completed": 4,
        "cognitive_engines": 6,
        "mjm_phases": 3,
    })


@router.post("/nexus")
async def synthesis_nexus(req: NexusRequest):
    """
    Synthesis Nexus — fully autonomous, synergistic, multi-layer intelligence.
    Layer 1: AI Cognitive Cascade (6 engines: Inkashaf/Samajh/Soch/Aqal/Hoshiyari/Iman)
    Layer 2: MJM Meta-Assessment (Mushahida/Jaiza/Muaina)
    Layer 3: Intelligently selected primary engine (BDP/SPI/APIE/DDPIE) — enriched by L1+L2
    Layer 4: Nexus Synthesis — unified integration of all intelligence layers.
    All layers stream as SSE. The engine is autonomously selected when activity='auto'.
    """
    return StreamingResponse(
        _run_nexus_stream(req),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/status")
async def intelligence_status():
    return {
        "engines_available": ["BDP", "SPI", "APIE", "DDPIE", "Solve", "Nexus"],
        "cognitive_stack": {
            "cascade": "UltimateCognitiveCascade (6 foundational + 3 meta engines)",
            "mjm": "MJMOrchestratorV4 (Mushahida-Jaiza-Muaina)",
            "gaas": "GaaSValidatorV4 (constitutional gate)",
        },
        "bdp_stages": len(_BDP_STAGES),
        "spi_stages": len(_SPI_STAGES),
        "apie_stages": 9,
        "ddpie_stages": 9,
        "streaming": "SSE",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORSHIP PROCESSES INTELLIGENCE ENGINE (APIE)
# ═══════════════════════════════════════════════════════════════════════════════

_APIE_STAGES = [
    ("source_discovery",        "Source Discovery",           "Map the literature landscape and identify authoritative sources"),
    ("argument_architecture",   "Argument Architecture",      "Build claim hierarchy, evidence chains, and logical structure"),
    ("structural_outline",      "Structural Outline",         "Design section hierarchy, flow, and narrative arc"),
    ("draft_synthesis",         "Draft Synthesis",            "Generate section-by-section draft with evidence integration"),
    ("evidence_weaving",        "Evidence & Citation Weaving","Weave citations, cross-references, and evidence annotations"),
    ("peer_review_simulation",  "Peer Review Simulation",     "Conduct blind academic peer review — identify gaps and weaknesses"),
    ("revision_intelligence",   "Revision Intelligence",      "Generate targeted revision notes and improvement directives"),
    ("integrity_audit",         "Integrity Audit",            "Audit originality, coherence, logical consistency, and academic rigour"),
    ("publication_readiness",   "Publication Readiness",      "Final prep — format compliance, submission checklist, cover letter"),
]

_APIE_PROMPTS = {
    "source_discovery": (
        "You are a Senior Research Librarian and academic writing coach. "
        "For the following scholarly work, map the authoritative knowledge landscape:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\nAudience: {audience}\n\n"
        "Deliver:\n"
        "## Primary Source Categories (tier 1-3 sources by authority)\n"
        "## Key Theoretical Frameworks (foundational scholars and works)\n"
        "## Seminal Works to Cite (10 essential references with annotation)\n"
        "## Knowledge Gaps in Existing Literature (where this work can contribute)\n"
        "## Emerging Debates and Controversies (live academic disputes)\n"
        "## Methodological Precedents (how others have studied this)\n"
        "## Recommended Search Strings (5 Boolean search queries for key databases)\n"
        "## Red-Flag Sources to Avoid (low-credibility sources in this field)\n"
    ),
    "argument_architecture": (
        "You are a master of academic argument construction. Build a rigorous argument architecture for:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\n\n"
        "Deliver:\n"
        "## Central Thesis Statement (1-2 sentences, falsifiable and precise)\n"
        "## Core Claims Hierarchy (3-5 main claims supporting the thesis)\n"
        "## Evidence Map (which evidence supports which claim)\n"
        "## Logical Structure (deductive/inductive/abductive/mixed — explain choice)\n"
        "## Counter-Arguments to Address (3 strongest objections with rebuttals)\n"
        "## Assumed Knowledge (what readers are assumed to know)\n"
        "## Conceptual Definitions (5 key terms defined with precision)\n"
        "## Rhetorical Strategy (how to persuade this specific audience)\n"
        "## Synthesis Move (how this work advances the field beyond existing literature)\n"
    ),
    "structural_outline": (
        "You are a professional academic editor. Design the optimal structure for this work:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\n"
        "Word count target: {word_count}\nCitation style: {citation_style}\n\n"
        "Deliver:\n"
        "## Full Section Hierarchy (all sections with sub-sections and estimated word counts)\n"
        "## Introduction Architecture (hook, context, thesis, roadmap — paragraph plan)\n"
        "## Literature Review Structure (thematic or chronological — justify)\n"
        "## Main Body Flow (section-by-section argument progression)\n"
        "## Conclusion Architecture (synthesis, contribution, future work, limitations)\n"
        "## Transitions Strategy (how sections connect and build)\n"
        "## Abstract Template (200-word structure with sentence-by-sentence breakdown)\n"
        "## Visual/Table Requirements (figures, tables, diagrams needed)\n"
    ),
    "draft_synthesis": (
        "You are a skilled academic writer. Draft the core sections for this work:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\nAudience: {audience}\n"
        "Previous analysis: {context}\n\n"
        "Write full draft text for:\n"
        "## Introduction (complete draft — hook, context-setting, thesis statement, scope, roadmap)\n"
        "## Literature Review Opening (positioning in the field, key debates, gaps identified)\n"
        "## First Main Body Section (fully developed argument with evidence integration)\n"
        "## Conclusion Draft (synthesis of argument, contribution statement, future directions)\n\n"
        "Style: Precise academic register, active voice where appropriate, "
        "signal phrases for citations (e.g. 'As [Author] argues...'), no hedging without purpose."
    ),
    "evidence_weaving": (
        "You are a citation and evidence integration specialist. Build the evidence framework for:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nCitation style: {citation_style}\n"
        "Previous analysis: {context}\n\n"
        "Deliver:\n"
        "## In-Text Citation Examples (10 model citations in {citation_style} format)\n"
        "## Evidence Integration Patterns (quote/paraphrase/summary — when to use each)\n"
        "## Signal Phrase Bank (20 academic signal phrases categorised by rhetorical purpose)\n"
        "## Statistical Evidence Presentation (how to introduce data, tables, and figures)\n"
        "## Cross-Reference Map (which sections should reference each other)\n"
        "## Reference List Structure ({citation_style} format — 15 model entries)\n"
        "## Annotated Bibliography Draft (8 sources with 60-word annotations)\n"
        "## Academic Integrity Checklist (10-point originality and attribution guide)\n"
    ),
    "peer_review_simulation": (
        "You are a blind peer reviewer for a prestigious {domain} journal. "
        "Conduct a rigorous review of this work:\n\n"
        "Topic/Thesis: {topic}\nGenre: {genre}\nDomain: {domain}\n"
        "Work summary: {context}\n\n"
        "Deliver a formal peer review:\n"
        "## Overall Assessment (Accept / Major Revisions / Minor Revisions / Reject — with rationale)\n"
        "## Strengths (what this work does exceptionally well — be specific)\n"
        "## Major Concerns (fundamental issues that must be addressed)\n"
        "## Minor Concerns (smaller stylistic or structural issues)\n"
        "## Argument Rigour Evaluation (logical soundness, evidence quality)\n"
        "## Literature Coverage Assessment (key works missing or misrepresented)\n"
        "## Clarity and Writing Quality Feedback\n"
        "## Specific Revision Requests (numbered list of required changes)\n"
        "## Recommendation to Editor with Conditions\n"
    ),
    "revision_intelligence": (
        "You are a senior academic writing coach reviewing responses to peer critique. "
        "Generate targeted revision intelligence for:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\n"
        "Peer review findings: {context}\n\n"
        "Deliver:\n"
        "## Revision Priority Matrix (Must-Do / Should-Do / Can-Do categories)\n"
        "## Point-by-Point Response Plan (addressing each reviewer concern explicitly)\n"
        "## Structural Revisions Required (sections to add, remove, or restructure)\n"
        "## Argument Strengthening Actions (specific claims to reinforce with evidence)\n"
        "## Literature Gaps to Fill (missing citations and sources to integrate)\n"
        "## Sample Revised Paragraphs (3 examples showing before/after revisions)\n"
        "## Author Response Letter Template (professional resubmission cover letter)\n"
        "## Revision Timeline (realistic schedule for completing all changes)\n"
    ),
    "integrity_audit": (
        "You are an academic quality and integrity auditor. "
        "Conduct a rigorous audit for:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\n"
        "Full work summary: {context}\n\n"
        "Audit across:\n"
        "## Originality Assessment (contribution to knowledge — what is genuinely new)\n"
        "## Logical Coherence Check (does the argument hold throughout the work)\n"
        "## Evidence Sufficiency Audit (is each major claim adequately evidenced)\n"
        "## Internal Consistency Check (no contradictions between sections)\n"
        "## Academic Rigour Score (1-10 per dimension: argument, evidence, methodology, writing)\n"
        "## Ethical Compliance Check (research ethics, consent, data handling)\n"
        "## Bias Audit (ideological, confirmation, selection bias — identify and assess)\n"
        "## Citation Completeness (all major claims properly attributed)\n"
        "## Overall Quality Score (% publication readiness with grade A-F)\n"
        "## Final 12-Point Checklist before Submission\n"
    ),
    "publication_readiness": (
        "You are a publication specialist and academic submissions coordinator. "
        "Produce a complete publication readiness package for:\n\n"
        "Topic/Thesis: {topic}\nDomain: {domain}\nGenre: {genre}\n"
        "Audience: {audience}\nCitation style: {citation_style}\n"
        "Integrity audit: {context}\n\n"
        "Deliver:\n"
        "## Target Venue Selection (5 journals/publishers ranked by fit, with rationale and impact)\n"
        "## Author Guidelines Summary (typical word limit, format, submission requirements)\n"
        "## Title Optimisation (3 alternative title options with different rhetorical strategies)\n"
        "## Abstract Versions (150-word and 250-word polished versions)\n"
        "## Keywords Strategy (12 optimised keywords for maximum discoverability)\n"
        "## Cover Letter Template (complete, personalised for top venue)\n"
        "## Submission Checklist (24-point final review before submitting)\n"
        "## Open Access Strategy (preprint, institutional repository, CC licence options)\n"
        "## Post-Publication Dissemination Plan (academic networks, social media, press release)\n"
        "## Impact Maximisation Strategy (how to reach the right readers after publication)\n"
    ),
}


def _rigor_directive(rigor: str) -> str:
    """§7 — turn a rigor level into a run-time analysis directive woven into an engine's prompts (honored)."""
    table = {
        "rigorous": "\n\nANALYSIS DIRECTIVE (rigorous): justify each claim with evidence/reasoning and weigh counter-arguments.",
        "exhaustive": "\n\nANALYSIS DIRECTIVE (exhaustive): be comprehensive — justify every claim with evidence, "
                      "weigh alternatives and counter-arguments, and surface edge cases and second-order effects.",
    }
    return table.get((rigor or "standard").lower(), "")


class AuthorshipRequest(BaseModel):
    topic: str
    genre: str = "academic paper"
    domain: str = "science"
    audience: str = "academic peers"
    citation_style: str = "APA"
    word_count: str = "8000"
    rigor: str = "standard"   # §7 — standard | rigorous | exhaustive (honored at run time)


async def _run_authorship_stream(req: AuthorshipRequest):
    context_accumulator = ""

    def _ev(stage: str, label: str, content: str, data: dict | None = None) -> str:
        payload: dict = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {json.dumps(payload)}\n\n"

    yield _ev("init", "APIE Initiated", f"Scholarship & Authorship pipeline: {req.topic[:120]}")
    directive = _rigor_directive(req.rigor)   # §7 — honored in every stage
    if directive:
        yield _ev("config", "Reconfiguration", f"rigor={req.rigor}")

    for i, (stage_key, stage_label, stage_desc) in enumerate(_APIE_STAGES):
        yield _ev(f"{stage_key}_start", stage_label, stage_desc)

        prompt_template = _APIE_PROMPTS.get(stage_key, "")
        if not prompt_template:
            continue

        prompt = prompt_template.format(
            topic=req.topic,
            domain=req.domain,
            genre=req.genre,
            audience=req.audience,
            citation_style=req.citation_style,
            word_count=req.word_count,
            context=directive + (context_accumulator[-900:] if context_accumulator else ""),
        )

        try:
            result = await gateway.query(prompt, agent=f"apie_{stage_key}")
        except Exception as e:
            result = f"[{stage_label} pending — {e}]"

        context_accumulator += f"\n\n## {stage_label}\n{result[:700]}"
        yield _ev(stage_key, stage_label, result, {"stage_num": i + 1, "total": len(_APIE_STAGES)})

    yield _ev("complete", "APIE Complete", "9-stage authorship pipeline complete.", {
        "stages_completed": len(_APIE_STAGES),
        "engine": "APIE",
        "genre": req.genre,
        "citation_style": req.citation_style,
    })


@router.post("/authorship")
async def authorship_intelligence_engine(req: AuthorshipRequest):
    """
    Scholarship & Authorship Processes Intelligence Engine (APIE).
    9-stage pipeline: source discovery → argument → outline → draft →
    evidence weaving → peer review → revision → integrity audit → publication readiness.
    Streamed as SSE.
    """
    return StreamingResponse(
        _run_authorship_stream(req),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN & DEVELOPMENT PROCESSES INTELLIGENCE ENGINE (DDPIE)
# ═══════════════════════════════════════════════════════════════════════════════

_DDPIE_STAGES = [
    ("requirements_intelligence", "Requirements Intelligence",  "Elicit and structure functional/non-functional requirements as user stories"),
    ("architecture_design",       "Architecture Design",        "Design system architecture, component topology, and tech stack"),
    ("domain_modelling",          "Domain Modelling",           "Model entities, relationships, bounded contexts, and data schemas"),
    ("api_contract",              "API Contract Design",        "Specify API contracts, endpoints, and request/response schemas"),
    ("security_architecture",     "Security Architecture",      "Design security posture, threat model, and OWASP compliance"),
    ("implementation_blueprint",  "Implementation Blueprint",   "Break down into modules, estimate effort, and plan sprints"),
    ("test_strategy",             "Test Strategy",              "Design test pyramid, TDD approach, and quality gates"),
    ("devops_pipeline",           "DevOps Pipeline",            "Design CI/CD, containerisation, IaC, and deployment strategy"),
    ("technical_review",          "Technical Review",           "Architecture Decision Records, code review criteria, go/no-go gate"),
]

_DDPIE_PROMPTS = {
    "requirements_intelligence": (
        "You are a Senior Business Analyst and product requirements engineer. "
        "Elicit and structure requirements for the following system:\n\n"
        "System/Product: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n\n"
        "Deliver:\n"
        "## Product Vision Statement (1 paragraph — what it is, for whom, and why it matters)\n"
        "## Functional Requirements (12-15 as user stories: As a [user] I want [action] so that [benefit])\n"
        "## Non-Functional Requirements (performance, security, scalability, reliability, compliance)\n"
        "## Acceptance Criteria (3 critical user stories with Given/When/Then format)\n"
        "## System Boundaries (in scope vs explicitly out of scope)\n"
        "## Stakeholder Map (primary, secondary, and shadow users with needs)\n"
        "## Constraints and Assumptions (technical, business, regulatory)\n"
        "## MoSCoW Priority Matrix (Must/Should/Could/Won't for MVP)\n"
        "## Definition of Done (project-level DoD criteria)\n"
        "## Requirements Traceability Matrix (user need → requirement → acceptance test)\n"
    ),
    "architecture_design": (
        "You are a Principal Software Architect. Design the system architecture for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n"
        "Requirements: {context}\n\n"
        "Deliver:\n"
        "## Architecture Pattern Decision (monolith/microservices/event-driven/serverless — with rationale)\n"
        "## Component Topology (all major components, boundaries, and connections described as structured text)\n"
        "## Technology Stack (each layer with specific technology choices and justification)\n"
        "## Data Architecture Overview (storage layer, data flow, caching strategy)\n"
        "## Integration Architecture (external systems, third-party APIs, messaging layer)\n"
        "## Scalability Strategy (horizontal/vertical scaling, bottlenecks, capacity planning)\n"
        "## Resilience Design (circuit breakers, retries, fallbacks, graceful degradation)\n"
        "## Key Architecture Decision Records (3 ADRs: context/options/decision/consequences)\n"
        "## Quality Attribute Scenarios (FURPS+ or ISO 25010 assessment)\n"
        "## Technical Debt Register (known compromises and resolution roadmap)\n"
    ),
    "domain_modelling": (
        "You are a Domain-Driven Design expert. Build the domain model for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\n"
        "Architecture: {context}\n\n"
        "Deliver:\n"
        "## Bounded Contexts (domain partitions — name, responsibility, team ownership)\n"
        "## Ubiquitous Language Glossary (20 core domain terms precisely defined)\n"
        "## Core Aggregates (6 key aggregates with invariants and lifecycle)\n"
        "## Entity Relationship Design (key entities, attributes, relationships, cardinalities)\n"
        "## Value Objects and Enumerations (immutable domain concepts)\n"
        "## Domain Events (key events triggering state changes — event storming output)\n"
        "## Database Schema Design (primary tables/collections with fields, types, indexes)\n"
        "## Data Migration Strategy (schema evolution, versioning, rollback)\n"
        "## CQRS / Event Sourcing Applicability (assess fit for this system's read/write patterns)\n"
        "## Data Governance Model (ownership, lineage, retention, GDPR considerations)\n"
    ),
    "api_contract": (
        "You are an API Design Lead and OpenAPI specification expert. Design the API for:\n\n"
        "System: {system}\nDomain: {domain}\nStack: {tech_stack}\n"
        "Domain model: {context}\n\n"
        "Deliver:\n"
        "## API Design Philosophy (REST/GraphQL/gRPC/hybrid — justify for this system)\n"
        "## Resource Hierarchy (URL structure and naming conventions)\n"
        "## Core Endpoint Catalogue (20 endpoints: method, path, description, key request/response fields)\n"
        "## Authentication & Authorisation Design (JWT/OAuth2/API keys — flows and token lifecycle)\n"
        "## Error Response Standards (error codes, problem+json format, error taxonomy)\n"
        "## Pagination, Filtering, and Sorting Conventions\n"
        "## API Versioning Strategy (URI vs header versioning — deprecation policy)\n"
        "## Rate Limiting and Throttling Design (tiers, headers, retry-after)\n"
        "## OpenAPI 3.1 Schema Snippet (5 key models as YAML)\n"
        "## Contract Testing Approach (consumer-driven contracts, Pact or equivalent)\n"
        "## API Documentation and Developer Experience Strategy\n"
    ),
    "security_architecture": (
        "You are a Principal Security Architect and OWASP Top 10 expert. Design the security posture for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n"
        "API design: {context}\n\n"
        "Deliver:\n"
        "## Threat Model (STRIDE analysis: Spoofing / Tampering / Repudiation / Info Disclosure / DoS / Elevation)\n"
        "## Attack Surface Analysis (external interfaces, data stores, third-party integrations)\n"
        "## OWASP Top 10 Compliance Map (assessment and mitigations for each category)\n"
        "## Authentication Architecture (MFA, session management, token lifecycle, refresh strategy)\n"
        "## Authorisation Model (RBAC/ABAC — permissions matrix for key roles)\n"
        "## Data Protection Design (encryption at rest/transit, PII handling, key management)\n"
        "## Security Testing Strategy (SAST/DAST tools, penetration testing cadence)\n"
        "## Secrets Management Design (how credentials/keys/tokens are stored and rotated)\n"
        "## Compliance Requirements (GDPR, UK GDPR, SOC2, ISO 27001 — applicable standards)\n"
        "## Security Incident Response Plan (detection, containment, recovery, comms)\n"
        "## Security Maturity Score (1-10 per dimension with improvement roadmap)\n"
    ),
    "implementation_blueprint": (
        "You are a Head of Engineering and technical delivery lead. Create the implementation blueprint for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n"
        "Security architecture: {context}\n\n"
        "Deliver:\n"
        "## Module Breakdown (all implementation modules: name, description, owner, dependencies, effort)\n"
        "## Development Phases (Foundation / Core / Integration / Polish / Launch — what each phase ships)\n"
        "## Sprint Plan (10 sprints, 2-week cadence — deliverables and acceptance criteria per sprint)\n"
        "## Effort Estimation (T-shirt sizing per module: XS/S/M/L/XL with confidence %)\n"
        "## Team Structure Recommendation (roles, squad composition, skills required)\n"
        "## Development Environment Setup (local / staging / production environments)\n"
        "## Code Quality Standards (linting, formatting, PR review process, naming conventions)\n"
        "## Technical Risk Register (top 6 implementation risks with probability/impact/mitigation)\n"
        "## MVP Feature Set (minimum viable product — what must ship first)\n"
        "## Definition of Ready + Definition of Done (story-level criteria)\n"
    ),
    "test_strategy": (
        "You are a Head of Quality Engineering and TDD practitioner. Design the test strategy for:\n\n"
        "System: {system}\nDomain: {domain}\nStack: {tech_stack}\n"
        "Implementation blueprint: {context}\n\n"
        "Deliver:\n"
        "## Test Philosophy (TDD/BDD/ATDD — justify choice for this system)\n"
        "## Test Pyramid Design (unit/integration/contract/e2e — target ratios and reasoning)\n"
        "## Unit Test Strategy (what to test, mocking strategy, coverage targets per module)\n"
        "## Integration Test Strategy (which integrations to test, test doubles vs real systems)\n"
        "## End-to-End Test Scenarios (10 critical user journeys to automate)\n"
        "## Performance Test Plan (load testing, stress testing, SLA targets with specific numbers)\n"
        "## Security Test Plan (SAST tools, DAST schedule, penetration test scope)\n"
        "## Test Data Management (fixtures, factories, anonymisation, environment isolation)\n"
        "## Quality Gates (must pass before merge, before staging, before production)\n"
        "## Testing Tools Recommendation (frameworks per test type with version pinning rationale)\n"
        "## Continuous Testing in CI/CD (which tests run at which pipeline stage)\n"
    ),
    "devops_pipeline": (
        "You are a Principal DevOps Engineer and Site Reliability Engineering lead. Design the pipeline for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n"
        "Deployment target: {deployment_target}\nTest strategy: {context}\n\n"
        "Deliver:\n"
        "## CI/CD Pipeline Architecture (stages, triggers, quality gates per environment)\n"
        "## Containerisation Strategy (Docker, Kubernetes, container registry, image signing policy)\n"
        "## Infrastructure as Code Design (Terraform/Pulumi — module structure and state management)\n"
        "## Environment Strategy (dev/staging/prod — config, secrets, promotion gates)\n"
        "## Deployment Strategy (blue/green / canary / rolling — justify for this system)\n"
        "## Observability Stack (metrics, logging, distributed tracing, alerting — tools and dashboards)\n"
        "## SLA / SLO / SLI Definitions (availability, latency, error rate targets with numbers)\n"
        "## On-Call Runbook (escalation path, incident severity levels, war room procedure)\n"
        "## Disaster Recovery Plan (RPO/RTO targets, backup strategy, failover procedure)\n"
        "## Cost Optimisation Strategy (right-sizing, auto-scaling, reserved vs spot instances)\n"
        "## GitOps Workflow (branch strategy, PR gates, automated deploy trigger rules)\n"
    ),
    "technical_review": (
        "You are a Principal Engineer chairing a Technical Review Board. "
        "Conduct the final technical review for:\n\n"
        "System: {system}\nDomain: {domain}\nScale: {scale}\nStack: {tech_stack}\n"
        "Full design summary: {context}\n\n"
        "Deliver:\n"
        "## Architecture Review Summary (strengths and concerns across all design layers)\n"
        "## Architecture Decision Records — Final Set (5 ADRs with full context/options/consequences)\n"
        "## Technical Risk Assessment (probability × impact matrix for top 8 risks)\n"
        "## Code Review Standards Charter (criteria, time expectations, reviewer responsibilities)\n"
        "## Non-Functional Requirements Validation (each NFR: met / partially / not met — with evidence)\n"
        "## Dependency Vulnerability Assessment (key dependencies, update cadence, CVE monitoring)\n"
        "## Scalability Projection (current design supports N users — re-architecture trigger points)\n"
        "## Operational Readiness Checklist (24-point go-live readiness gate)\n"
        "## Technical Debt Budget (what debt is acceptable now vs what must be paid before launch)\n"
        "## Go / No-Go Decision with Conditions (gate recommendation with specific criteria)\n"
        "## Technical Roadmap — Post-Launch Priorities (next 6 months engineering agenda)\n"
    ),
}


class DesignDevRequest(BaseModel):
    system: str
    domain: str = "enterprise"
    tech_stack: str = "Python / FastAPI / React / PostgreSQL"
    scale: str = "startup"
    deployment_target: str = "cloud"
    rigor: str = "standard"   # §7 — standard | rigorous | exhaustive (honored at run time)


async def _run_design_dev_stream(req: DesignDevRequest):
    context_accumulator = ""

    def _ev(stage: str, label: str, content: str, data: dict | None = None) -> str:
        payload: dict = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {json.dumps(payload)}\n\n"

    yield _ev("init", "DDPIE Initiated", f"Design & Development pipeline: {req.system[:120]}")
    directive = _rigor_directive(req.rigor)   # §7 — honored in every stage
    if directive:
        yield _ev("config", "Reconfiguration", f"rigor={req.rigor}")

    for i, (stage_key, stage_label, stage_desc) in enumerate(_DDPIE_STAGES):
        yield _ev(f"{stage_key}_start", stage_label, stage_desc)

        prompt_template = _DDPIE_PROMPTS.get(stage_key, "")
        if not prompt_template:
            continue

        prompt = prompt_template.format(
            system=req.system,
            domain=req.domain,
            tech_stack=req.tech_stack,
            scale=req.scale,
            deployment_target=req.deployment_target,
            context=directive + (context_accumulator[-900:] if context_accumulator else ""),
        )

        try:
            result = await gateway.query(prompt, agent=f"ddpie_{stage_key}")
        except Exception as e:
            result = f"[{stage_label} pending — {e}]"

        context_accumulator += f"\n\n## {stage_label}\n{result[:700]}"
        yield _ev(stage_key, stage_label, result, {"stage_num": i + 1, "total": len(_DDPIE_STAGES)})

    yield _ev("complete", "DDPIE Complete", "9-stage design & development pipeline complete.", {
        "stages_completed": len(_DDPIE_STAGES),
        "engine": "DDPIE",
        "tech_stack": req.tech_stack,
        "scale": req.scale,
    })


@router.post("/design-dev")
async def design_dev_intelligence_engine(req: DesignDevRequest):
    """
    Design & Development Processes Intelligence Engine (DDPIE).
    9-stage pipeline: requirements → architecture → domain modelling → API contract →
    security → implementation blueprint → test strategy → devops → technical review.
    Streamed as SSE.
    """
    return StreamingResponse(
        _run_design_dev_stream(req),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
