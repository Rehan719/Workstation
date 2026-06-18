"""
Projects API — the core entity that binds the MVP spine together.

Every AI workflow in Workstation runs inside a Project. A Project has:
  - A realm (technology, science, religion, education, law, care, employment)
  - A domain/type (saas, research, content, service, product, policy, curriculum)
  - A lifecycle stage: concept → prototype → commercialise
  - A set of AI-generated outputs linked to synthesis download URLs

Endpoints
---------
POST   /projects/                  create project
GET    /projects/                  list all projects
GET    /projects/{id}              get single project
PATCH  /projects/{id}              update title / description
DELETE /projects/{id}              delete project + outputs
POST   /projects/{id}/run          run AI workflow → SSE stream of tokens
POST   /projects/{id}/advance      advance stage (concept→prototype→commercialise)
GET    /projects/{id}/outputs      list generated outputs for a project
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import AsyncIterator, Literal, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/projects", tags=["projects"])

# ── Persistence ───────────────────────────────────────────────────────────────
_STORE = Path(os.getenv("PROJECTS_DIR", "data/projects"))
_STORE.mkdir(parents=True, exist_ok=True)

Stage = Literal["concept", "prototype", "commercialise"]
STAGE_ORDER: list[Stage] = ["concept", "prototype", "commercialise"]

REALM_PROMPTS: dict[str, str] = {
    "technology":  "You are an expert technology product strategist and software architect.",
    "science":     "You are an expert research scientist and innovation strategist.",
    "religion":    "You are a thoughtful scholar of comparative religion and community design.",
    "education":   "You are an expert curriculum designer and learning-science specialist.",
    "law":         "You are an expert legal strategist and policy analyst.",
    "care":        "You are an expert healthcare innovator and care-pathway designer.",
    "employment":  "You are an expert workforce strategist and career-development coach.",
    "general":     "You are an expert business strategist and product manager.",
}

STAGE_PROMPTS: dict[Stage, str] = {
    "concept": (
        "Generate a detailed Concept Document for the following project. "
        "Include: executive summary, problem statement, proposed solution, "
        "target market, key differentiators, and initial risk assessment. "
        "Be specific, actionable, and commercially rigorous."
    ),
    "prototype": (
        "Generate a Prototype Specification for the following project. "
        "Include: core feature set (MVP scope), technical architecture overview, "
        "user journey map, success metrics, and a 30-day build plan. "
        "Be concrete — name actual technologies, APIs, and workflows."
    ),
    "commercialise": (
        "Generate a Commercialisation Playbook for the following project. "
        "Include: go-to-market strategy, pricing model, customer acquisition channels, "
        "revenue projections (12-month), partnership opportunities, and launch checklist. "
        "Be specific with numbers, timelines, and named channels."
    ),
}


# ── Models ────────────────────────────────────────────────────────────────────

class ProjectOutput(BaseModel):
    output_id: str
    stage: Stage
    created_at: float
    download_url: str
    preview: str  # first 400 chars of the generated text


class Project(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    title: str
    description: str
    realm: str = "general"
    domain: str = "product"
    stage: Stage = "concept"
    status: Literal["idle", "running", "done", "error"] = "idle"
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    outputs: list[ProjectOutput] = Field(default_factory=list)


class CreateProjectRequest(BaseModel):
    title: str
    description: str
    realm: str = "general"
    domain: str = "product"


class UpdateProjectRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# ── Storage helpers ───────────────────────────────────────────────────────────

def _path(project_id: str) -> Path:
    return _STORE / f"{project_id}.json"


def _load(project_id: str) -> Project:
    p = _path(project_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return Project(**json.loads(p.read_text()))


def _save(project: Project) -> None:
    project.updated_at = time.time()
    _path(project.id).write_text(project.model_dump_json(indent=2))


def _all_projects() -> list[Project]:
    projects = []
    for f in sorted(_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            projects.append(Project(**json.loads(f.read_text())))
        except Exception:
            pass
    return projects


# ── Output persistence (reuses synthesis download dir) ───────────────────────
_OUTPUTS_DIR = Path(os.getenv("SYNTHESIS_OUTPUT_DIR", "data/synthesis_outputs"))
_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def _save_output(project: Project, text: str) -> ProjectOutput:
    output_id = uuid.uuid4().hex
    out_path = _OUTPUTS_DIR / f"{output_id}.txt"
    out_path.write_text(text, encoding="utf-8")
    output = ProjectOutput(
        output_id=output_id,
        stage=project.stage,
        created_at=time.time(),
        download_url=f"/api/v1/synthesis/download/{output_id}",
        preview=text[:400],
    )
    project.outputs.append(output)
    return output


# ── Governance proposals (models + helpers — routes registered BEFORE /{project_id}) ──

_PROPOSALS_DIR = Path(os.getenv("PROPOSALS_DIR", "data/proposals"))
_PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)


class Proposal(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    project_id: str
    project_title: str
    from_stage: Stage
    to_stage: Stage
    status: Literal["pending", "approved", "rejected"] = "pending"
    votes_for: int = 0
    votes_against: int = 0
    created_at: float = Field(default_factory=time.time)


def _save_proposal(p: Proposal) -> None:
    (_PROPOSALS_DIR / f"{p.id}.json").write_text(p.model_dump_json(indent=2))


def _load_proposal(proposal_id: str) -> Proposal:
    f = _PROPOSALS_DIR / f"{proposal_id}.json"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Proposal not found")
    return Proposal(**json.loads(f.read_text()))


def _all_proposals() -> list[Proposal]:
    out = []
    for f in sorted(_PROPOSALS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            out.append(Proposal(**json.loads(f.read_text())))
        except Exception:
            pass
    return out


# ── Static-path routes MUST come before /{project_id} ─────────────────────────

@router.get("/stats/summary")
async def project_stats() -> dict:
    """Aggregated portfolio metrics derived from all projects on disk."""
    projects = _all_projects()
    by_stage: dict[str, int] = {"concept": 0, "prototype": 0, "commercialise": 0}
    by_realm: dict[str, int] = {}
    total_outputs = 0
    for p in projects:
        by_stage[p.stage] = by_stage.get(p.stage, 0) + 1
        by_realm[p.realm] = by_realm.get(p.realm, 0) + 1
        total_outputs += len(p.outputs)
    try:
        import psutil as _psutil
        cpu = _psutil.cpu_percent(interval=None)
        mem = _psutil.virtual_memory().percent
    except Exception:
        cpu, mem = 0.0, 0.0

    total = len(projects)
    swarm_health = min(1.0, 0.70 + total * 0.02) if total > 0 else 0.70

    return {
        "total_projects": total,
        "by_stage": by_stage,
        "by_realm": by_realm,
        "total_outputs": total_outputs,
        "active": sum(1 for p in projects if p.status == "running"),
        "complete": sum(1 for p in projects if p.stage == "commercialise"),
        "cpu_percent": round(cpu, 1),
        "memory_percent": round(mem, 1),
        "swarm_health": round(swarm_health, 3),
    }


@router.get("/governance/proposals", response_model=list[Proposal])
async def list_proposals() -> list[Proposal]:
    return _all_proposals()


@router.post("/governance/proposals/{proposal_id}/vote", response_model=Proposal)
async def vote_proposal(proposal_id: str, approve: bool = True) -> Proposal:
    proposal = _load_proposal(proposal_id)
    if proposal.status != "pending":
        raise HTTPException(status_code=400, detail=f"Proposal already {proposal.status}.")
    if approve:
        proposal.votes_for += 1
    else:
        proposal.votes_against += 1
    proposal.status = "approved" if approve else "rejected"
    if proposal.status == "approved":
        try:
            project = _load(proposal.project_id)
            project.stage = proposal.to_stage
            project.status = "idle"
            _save(project)
        except Exception:
            pass
    _save_proposal(proposal)
    return proposal


# ── CRUD endpoints ────────────────────────────────────────────────────────────

@router.post("/", response_model=Project, status_code=201)
async def create_project(req: CreateProjectRequest) -> Project:
    project = Project(
        title=req.title,
        description=req.description,
        realm=req.realm.lower(),
        domain=req.domain.lower(),
    )
    _save(project)
    return project


@router.get("/", response_model=list[Project])
async def list_projects() -> list[Project]:
    return _all_projects()


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str) -> Project:
    return _load(project_id)


@router.patch("/{project_id}", response_model=Project)
async def update_project(project_id: str, req: UpdateProjectRequest) -> Project:
    project = _load(project_id)
    if req.title is not None:
        project.title = req.title
    if req.description is not None:
        project.description = req.description
    _save(project)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str) -> None:
    p = _path(project_id)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    p.unlink()


# ── AI Run endpoint (SSE streaming) ──────────────────────────────────────────

@router.post("/{project_id}/run")
async def run_project(project_id: str) -> StreamingResponse:
    """
    Stream AI-generated content for this project's current stage.
    SSE format:
      data: {"token": "..."}          — incremental token
      data: {"done": true, "output_id": "...", "download_url": "..."}  — final
      data: {"error": "..."}          — on failure
    """
    project = _load(project_id)
    if project.status == "running":
        raise HTTPException(status_code=409, detail="Project is already running")

    project.status = "running"
    _save(project)

    system_prompt = REALM_PROMPTS.get(project.realm, REALM_PROMPTS["general"])
    stage_instruction = STAGE_PROMPTS[project.stage]
    full_prompt = (
        f"{stage_instruction}\n\n"
        f"Project title: {project.title}\n"
        f"Project description: {project.description}\n"
        f"Realm: {project.realm} · Domain: {project.domain}\n\n"
        f"Produce a comprehensive, professional document now."
    )

    async def event_stream() -> AsyncIterator[str]:
        accumulated = ""
        completed = False
        try:
            async for token in gateway.stream(full_prompt, agent="projects"):
                accumulated += token
                safe = token.replace("\n", "\\n")
                yield f'data: {{"token": {json.dumps(safe)}}}\n\n'

            # Persist and close out
            output = _save_output(project, accumulated)
            project.status = "done"
            _save(project)
            completed = True
            yield (
                f'data: {{"done": true, "output_id": "{output.output_id}", '
                f'"download_url": "{output.download_url}", '
                f'"preview": {json.dumps(output.preview)}}}\n\n'
            )
        except Exception as exc:
            project.status = "error"
            _save(project)
            yield f'data: {{"error": {json.dumps(str(exc))}}}\n\n'
        finally:
            # Client disconnected before stream finished — reset so user can retry
            if not completed:
                try:
                    stale = _load(project_id)
                    if stale.status == "running":
                        stale.status = "idle"
                        _save(stale)
                except Exception:
                    pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Stage advancement ─────────────────────────────────────────────────────────

@router.post("/{project_id}/advance", response_model=Project)
async def advance_stage(project_id: str) -> Project:
    """
    Advance the project's lifecycle stage: concept → prototype → commercialise.
    Guard: at least one output must exist at the current stage before advancing.
    """
    project = _load(project_id)
    current_idx = STAGE_ORDER.index(project.stage)

    if current_idx >= len(STAGE_ORDER) - 1:
        raise HTTPException(
            status_code=400,
            detail="Project is already at the final stage (commercialise).",
        )

    has_output_at_stage = any(o.stage == project.stage for o in project.outputs)
    if not has_output_at_stage:
        raise HTTPException(
            status_code=422,
            detail=f"Run the AI workflow at least once in the '{project.stage}' stage before advancing.",
        )

    project.stage = STAGE_ORDER[current_idx + 1]
    project.status = "idle"
    _save(project)
    return project


# ── Outputs list ──────────────────────────────────────────────────────────────

@router.get("/{project_id}/outputs", response_model=list[ProjectOutput])
async def list_outputs(project_id: str) -> list[ProjectOutput]:
    project = _load(project_id)
    return list(reversed(project.outputs))


# ── Governance propose-advance (per-project, needs project_id) ────────────────

@router.post("/{project_id}/propose-advance", response_model=Proposal, status_code=201)
async def propose_advance(project_id: str) -> Proposal:
    """
    Create a governance proposal to advance this project's stage.
    The stage does NOT advance until the proposal is approved via GovernanceHub.
    """
    project = _load(project_id)
    current_idx = STAGE_ORDER.index(project.stage)
    if current_idx >= len(STAGE_ORDER) - 1:
        raise HTTPException(status_code=400, detail="Already at final stage.")
    has_output = any(o.stage == project.stage for o in project.outputs)
    if not has_output:
        raise HTTPException(
            status_code=422,
            detail=f"Run the AI workflow at the '{project.stage}' stage before requesting advancement.",
        )
    proposal = Proposal(
        project_id=project.id,
        project_title=project.title,
        from_stage=project.stage,
        to_stage=STAGE_ORDER[current_idx + 1],
    )
    _save_proposal(proposal)
    return proposal


