"""
Human Synthesis Studio — End-to-end Concept to Commercialisation cascade.

This is the flagship BTO (Business Transformation Office) workflow:

  User describes a challenge →
  AI CEO initiates cascade →
  Multi-agent swarm synthesises:
    1. Challenge analysis + opportunity mapping
    2. Solution concept design
    3. VSB entity structure (AI CEO + C-Suite + CoE + BTO)
    4. Business Model Canvas
    5. QMS / BMS / DCS framework
    6. Go-to-market + commercialisation strategy
    7. Regulatory / legal / compliance map
    8. Digital twin simulation design
    9. Launch roadmap
  → Delivers complete VSB entity package as a spawned project

  POST /api/v1/studio/synthesise      — full cascade (SSE streaming)
  POST /api/v1/studio/vsb/spawn       — spawn a VSB entity from a project
  GET  /api/v1/studio/vsb/{entity_id} — retrieve spawned VSB entity
  GET  /api/v1/studio/vsb             — list all VSB entities
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/studio", tags=["synthesis-studio"])

_VSB_STORE = Path("data/vsb_entities")
_VSB_STORE.mkdir(parents=True, exist_ok=True)


# ── VSB Entity model ──────────────────────────────────────────────────────────

def _vsb_path(entity_id: str) -> Path:
    return _VSB_STORE / f"{entity_id}.json"


def _load_vsb(entity_id: str) -> dict | None:
    p = _vsb_path(entity_id)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return None


def _save_vsb(entity: dict) -> None:
    _vsb_path(entity["entity_id"]).write_text(json.dumps(entity, indent=2))


def _list_vsb() -> list[dict]:
    entities = []
    for p in sorted(_VSB_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            entities.append(json.loads(p.read_text()))
        except Exception:
            pass
    return entities


# ── Cascade synthesis ─────────────────────────────────────────────────────────

_CASCADE_STAGES = [
    ("challenge_analysis",     "CHALLENGE ANALYSIS",     "Analysing the challenge and mapping opportunity space"),
    ("solution_concept",       "SOLUTION CONCEPT",       "Designing the most effective solution concept"),
    ("vsb_structure",          "VSB ENTITY STRUCTURE",   "Designing AI CEO, C-Suite, CoE, and BTO structure"),
    ("business_model",         "BUSINESS MODEL",         "Building Business Model Canvas and revenue architecture"),
    ("management_systems",     "MANAGEMENT SYSTEMS",     "Designing QMS, BMS, DCS, and EMS frameworks"),
    ("regulatory_map",         "REGULATORY MAP",         "Mapping legal, regulatory, and compliance requirements"),
    ("go_to_market",           "GO-TO-MARKET",           "Designing commercialisation and launch strategy"),
    ("digital_twin",           "DIGITAL TWIN",           "Designing digital twin simulation model"),
    ("launch_roadmap",         "LAUNCH ROADMAP",         "Building 90-day launch roadmap with milestones"),
]

_STAGE_PROMPTS: dict[str, str] = {
    "challenge_analysis": (
        "You are the AI CEO of a Virtual Sovereign Business. "
        "Conduct a rigorous analysis of the following challenge.\n\n"
        "CHALLENGE: {challenge}\nDOMAIN: {domain}\nREALM: {realm}\n\n"
        "Deliver:\n"
        "## Challenge Definition (precise problem statement)\n"
        "## Root Cause Analysis (5 Whys or Fishbone)\n"
        "## Opportunity Mapping (what value can be created)\n"
        "## Affected Stakeholders (who benefits and how)\n"
        "## Market Size Estimate (TAM/SAM/SOM)\n"
        "## Urgency and Impact Score (1-10 each with rationale)\n"
        "## Solution Feasibility Assessment\n"
    ),
    "solution_concept": (
        "Building on the challenge analysis, design the optimal solution concept.\n\n"
        "CHALLENGE: {challenge}\nDOMAIN: {domain}\n\n"
        "Deliver:\n"
        "## Core Solution Concept (what it is in one paragraph)\n"
        "## Key Innovation (what makes this different/better)\n"
        "## Product/Service Definition (what the customer receives)\n"
        "## Technology Stack Recommendation\n"
        "## IP and Differentiation Strategy\n"
        "## Proof of Concept Design (minimal experiment to validate)\n"
        "## Success Metrics (how we know it works)\n"
    ),
    "vsb_structure": (
        "Design the Virtual Sovereign Business (VSB) entity structure for this solution.\n\n"
        "CHALLENGE: {challenge}\nSOLUTION: {solution_name}\nDOMAIN: {domain}\n\n"
        "Deliver:\n"
        "## AI CEO Role and Decision Authority\n"
        "## C-Suite Structure (CFO, CTO, CMO, COO, CLO — roles and responsibilities)\n"
        "## Centres of Excellence (CoE) — which specialisms are needed\n"
        "## Business Transformation Office (BTO) — transformation workstreams\n"
        "## AI Agent Swarm Design (which agents, what they do, how they cascade)\n"
        "## Governance Structure (decision rights, escalation paths)\n"
        "## Resource Requirements (AI tools, human oversight, external expertise)\n"
    ),
    "business_model": (
        "Design the complete business model for this VSB entity.\n\n"
        "CHALLENGE: {challenge}\nSOLUTION: {solution_name}\nDOMAIN: {domain}\n\n"
        "Complete Business Model Canvas:\n"
        "## Value Proposition (what pain do we solve, what gain do we create)\n"
        "## Customer Segments (who are the early adopters, early majority)\n"
        "## Channels (how we reach and serve customers)\n"
        "## Customer Relationships (how we acquire, retain, grow)\n"
        "## Revenue Streams (pricing model, revenue architecture, projections)\n"
        "## Key Resources (AI, IP, data, partnerships)\n"
        "## Key Activities (what must the VSB execute excellently)\n"
        "## Key Partnerships (who we need in the ecosystem)\n"
        "## Cost Structure (fixed vs variable, unit economics)\n"
        "## Financial Projections (Year 1, 2, 3 estimates with assumptions)\n"
    ),
    "management_systems": (
        "Design the integrated management systems for this VSB entity.\n\n"
        "SOLUTION: {solution_name}\nDOMAIN: {domain}\n\n"
        "Deliver:\n"
        "## Quality Management System (QMS) — ISO 9001-aligned framework\n"
        "   - Quality policy, objectives, KPIs\n"
        "   - Document control procedures\n"
        "   - Non-conformance and corrective action process\n"
        "   - Internal audit schedule\n"
        "## Business Management System (BMS)\n"
        "   - Balanced Scorecard (financial, customer, process, learning perspectives)\n"
        "   - OKR framework (3 objectives with key results)\n"
        "## Document Control System (DCS)\n"
        "   - Document taxonomy and naming convention\n"
        "   - Version control and approval workflow\n"
        "## Environmental Management System (EMS) — ISO 14001 considerations\n"
        "## AI Governance Framework\n"
    ),
    "regulatory_map": (
        "Map the regulatory, legal, and compliance landscape for this solution.\n\n"
        "CHALLENGE: {challenge}\nSOLUTION: {solution_name}\nDOMAIN: {domain}\nREALM: {realm}\n\n"
        "Deliver:\n"
        "## Applicable Legislation and Regulations (jurisdiction-specific)\n"
        "## Licensing and Permits Required\n"
        "## Data Protection and Privacy Compliance (GDPR/UK GDPR/other)\n"
        "## Health and Safety Requirements\n"
        "## Industry-Specific Standards and Accreditations\n"
        "## Ethical Compliance Requirements (AI ethics, fairness, transparency)\n"
        "## Intellectual Property Protection Strategy\n"
        "## Regulatory Risk Register (top 5 risks with mitigations)\n"
        "## Compliance Timeline and Action Plan\n"
    ),
    "go_to_market": (
        "Design the go-to-market and commercialisation strategy.\n\n"
        "SOLUTION: {solution_name}\nDOMAIN: {domain}\nREALM: {realm}\n\n"
        "Deliver:\n"
        "## Market Entry Strategy (beachhead market, expansion path)\n"
        "## Ideal Customer Profile (ICP) — 3 detailed personas\n"
        "## Value Proposition Messaging (headline, tagline, elevator pitch)\n"
        "## Sales Strategy (channels, sales motion, pricing)\n"
        "## Marketing Strategy (content, digital, partnerships, events)\n"
        "## Partnerships and Distribution Strategy\n"
        "## Launch Campaign Design (pre-launch, launch, post-launch)\n"
        "## 90-Day Commercial Targets (KPIs with specific numbers)\n"
        "## Customer Success and Retention Strategy\n"
    ),
    "digital_twin": (
        "Design a digital twin simulation model for this solution.\n\n"
        "CHALLENGE: {challenge}\nSOLUTION: {solution_name}\nDOMAIN: {domain}\n\n"
        "Deliver:\n"
        "## Digital Twin Architecture (what systems/processes are modelled)\n"
        "## Data Inputs (what real-world data feeds the model)\n"
        "## Model Components (agents, environments, feedback loops)\n"
        "## Simulation Scenarios (3-5 key scenarios to test)\n"
        "## Validation Methodology (how we know the model is accurate)\n"
        "## Key Outputs and Metrics (what the simulation measures)\n"
        "## Integration with Physical Systems\n"
        "## AI/ML Models Required\n"
        "## Failure Mode Analysis (what the twin helps us anticipate)\n"
    ),
    "launch_roadmap": (
        "Build the 90-day launch roadmap for this VSB entity.\n\n"
        "SOLUTION: {solution_name}\nDOMAIN: {domain}\n\n"
        "Deliver:\n"
        "## Phase 1: Foundation (Days 1-30)\n"
        "   - Legal entity establishment steps\n"
        "   - Core team/AI agent configuration\n"
        "   - Management systems setup\n"
        "   - MVP development milestones\n"
        "## Phase 2: Validation (Days 31-60)\n"
        "   - Beta customer acquisition\n"
        "   - Product/market fit validation\n"
        "   - Regulatory clearances\n"
        "   - First revenue target\n"
        "## Phase 3: Launch (Days 61-90)\n"
        "   - Public launch activities\n"
        "   - Scale-up plan\n"
        "   - Investment/funding strategy\n"
        "   - 12-month growth trajectory\n"
        "## Critical Path (dependencies and blockers)\n"
        "## Budget Estimate (total cost to launch)\n"
        "## Decision Gates (go/no-go criteria at each phase)\n"
    ),
}


class SynthesiseRequest(BaseModel):
    challenge: str
    realm: str = "enterprise"
    domain: str = "general"
    solution_name: str = ""
    context: str = ""


@router.post("/synthesise")
async def synthesise(req: SynthesiseRequest) -> StreamingResponse:
    """
    Full concept-to-commercialisation synthesis cascade (SSE streaming).
    Runs 9 AI stages, streaming results as they complete.
    """
    solution_name = req.solution_name or f"{req.domain.title()} Solution"
    synthesis_id = uuid.uuid4().hex[:12]
    start = time.time()
    results: dict[str, str] = {}

    async def stream() -> AsyncIterator[str]:
        # Announce start
        yield f'data: {json.dumps({"stage": "init", "synthesis_id": synthesis_id, "total_stages": len(_CASCADE_STAGES), "challenge": req.challenge})}\n\n'

        for i, (stage_key, stage_label, stage_desc) in enumerate(_CASCADE_STAGES):
            yield f'data: {json.dumps({"stage": "start", "stage_key": stage_key, "stage_label": stage_label, "description": stage_desc, "stage_num": i + 1})}\n\n'

            prompt_template = _STAGE_PROMPTS[stage_key]
            prompt = prompt_template.format(
                challenge=req.challenge,
                domain=req.domain,
                realm=req.realm,
                solution_name=solution_name,
                solution=results.get("solution_concept", "")[:200],
            )

            stage_content = await gateway.query(prompt, agent=f"studio_{stage_key}")
            results[stage_key] = stage_content

            yield f'data: {json.dumps({"stage": "complete", "stage_key": stage_key, "stage_label": stage_label, "content": stage_content, "stage_num": i + 1})}\n\n'

        # Spawn the VSB entity
        entity_id = f"vsb-{synthesis_id[:8]}"
        entity = {
            "entity_id": entity_id,
            "synthesis_id": synthesis_id,
            "challenge": req.challenge,
            "solution_name": solution_name,
            "realm": req.realm,
            "domain": req.domain,
            "status": "active",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stages": results,
            "duration_seconds": round(time.time() - start, 1),
        }
        _save_vsb(entity)

        # Also create a project for lifecycle tracking
        try:
            from agentic_core.projects.api import _save
            from agentic_core.projects.api import Project
            project = Project(
                id=synthesis_id,
                title=f"[VSB] {solution_name}",
                description=req.challenge[:500],
                realm=req.realm,
                domain=req.domain,
                stage="prototype",
                status="idle",
                outputs=[],
                created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                updated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )
            _save(project)
        except Exception:
            pass

        duration_ms = int((time.time() - start) * 1000)
        yield f'data: {json.dumps({"stage": "done", "synthesis_id": synthesis_id, "entity_id": entity_id, "solution_name": solution_name, "duration_ms": duration_ms, "stages_completed": len(_CASCADE_STAGES)})}\n\n'

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── VSB Entity management ─────────────────────────────────────────────────────

class SpawnRequest(BaseModel):
    project_id: str
    solution_name: str
    challenge: str = ""
    realm: str = "enterprise"
    domain: str = "general"


@router.post("/vsb/spawn")
async def spawn_vsb_entity(req: SpawnRequest):
    """
    Spawn a VSB entity from an existing project.
    Generates a compact VSB structure without the full cascade.
    """
    entity_id = f"vsb-{uuid.uuid4().hex[:8]}"

    prompt = (
        f"Design a compact Virtual Sovereign Business (VSB) entity for the following.\n\n"
        f"Project: {req.solution_name}\n"
        f"Challenge addressed: {req.challenge or 'Not specified'}\n"
        f"Realm: {req.realm}\nDomain: {req.domain}\n\n"
        "Provide:\n"
        "## AI CEO Mission Statement (2 sentences)\n"
        "## C-Suite (CFO / CTO / CMO / COO — one-line role each)\n"
        "## Primary CoE (top 2 Centres of Excellence needed)\n"
        "## First 3 BTO Workstreams\n"
        "## Entity Operating Principles (5 principles)\n"
        "## 30-Day Priority Actions (numbered list of 5)"
    )

    structure = await gateway.query(prompt, agent="vsb_spawner")

    entity = {
        "entity_id": entity_id,
        "project_id": req.project_id,
        "solution_name": req.solution_name,
        "challenge": req.challenge,
        "realm": req.realm,
        "domain": req.domain,
        "status": "active",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "structure": structure,
        "type": "spawned",
    }
    _save_vsb(entity)

    return {"entity_id": entity_id, "solution_name": req.solution_name, "structure": structure, "status": "spawned"}


@router.get("/vsb")
async def list_vsb_entities():
    """List all VSB entities."""
    entities = _list_vsb()
    return {
        "entities": [
            {
                "entity_id": e["entity_id"],
                "solution_name": e.get("solution_name", ""),
                "domain": e.get("domain", ""),
                "realm": e.get("realm", ""),
                "status": e.get("status", ""),
                "created_at": e.get("created_at", ""),
                "type": e.get("type", "synthesised"),
            }
            for e in entities
        ],
        "total": len(entities),
    }


@router.get("/vsb/{entity_id}")
async def get_vsb_entity(entity_id: str):
    """Retrieve a full VSB entity by ID."""
    entity = _load_vsb(entity_id)
    if not entity:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"VSB entity {entity_id} not found.")
    return entity
