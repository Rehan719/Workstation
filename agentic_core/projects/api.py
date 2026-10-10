"""
Projects API — the core entity that binds the MVP spine together.

Every AI workflow in Workstation runs inside a Project. A Project has:
  - A subject kind (science, religion, education, law, care, employment — taxonomy DOMAINS — plus the
    legacy extras 'technology' and 'general'). W505: this field is called `realm` for compatibility with
    stored projects, and it has never held a taxonomy realm; the real realm axis is `taxonomy_realm`.
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
from agentic_core.config import data_path
from typing import AsyncIterator, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, request_owner_id, user_can_access

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/projects", tags=["projects"])

# ── Persistence ───────────────────────────────────────────────────────────────
_STORE = Path((os.getenv("PROJECTS_DIR") or str(data_path("projects"))))
_STORE.mkdir(parents=True, exist_ok=True)

Stage = Literal["concept", "prototype", "commercialise"]
STAGE_ORDER: list[Stage] = ["concept", "prototype", "commercialise"]

# W505 (P2.5) — THE AXES, VALIDATED AGAINST THE TAXONOMY. Measured: every key below is a DOMAIN
# (six are exactly taxonomy.DOMAINS) or one of two extras in neither axis; NONE is a taxonomy REALM
# ('enterprise', 'learning', 'developing', 'scholarship'). This field has never held a realm. It is not
# renamed — stored projects hold these values and are readers of it (W495) — but it is now validated
# against what it actually holds, and the real realm axis is ADDED beside it (see `realm` below).
_SUBJECT_KINDS: tuple[str, ...] = ("technology", "general")   # in neither taxonomy axis, kept for stored rows


def _valid_subject(value: str) -> tuple[str, str]:
    """Normalise this API's `realm` field and say WHICH AXIS the value came from.

    W505 (P2.5) — this field receives two different axes depending on how the user arrived, and both are
    legitimate today:
      * ProjectsHub's picker sends a CANONICAL REALM (its options are CANON_REALMS; W321 corrected that
        list because "domains were listed as realms").
      * A domain hub's StartProjectCTA navigates with realm=care / law / education / science — a DOMAIN.
    An earlier version of this validated against DOMAINS alone, which would have rejected every
    picker-created project's realm and silently replaced it with "general" — the very defect this item is
    about, one layer over, and invisible because the fallback is itself a valid value.

    Returns (value, source). Nothing is rejected that the product can currently send; what changes is that
    the stored row now SAYS which axis its value belongs to instead of leaving a reader to guess."""
    from agentic_core.taxonomy import DOMAINS, REALMS
    v = str(value or "").strip().lower()
    if v in DOMAINS:
        return v, "taxonomy domain"
    if v in REALMS:
        return v, "taxonomy realm"
    if v in _SUBJECT_KINDS:
        return v, "legacy value, in neither taxonomy axis"
    return "general", f"unrecognised ({v or 'empty'}) — fell back to 'general'"


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
    # §13 (W495, FU-131, S12.6) - the run's done frame already reports served_by and is_external, and
    # this record dropped both: the saved preview, the downloaded .txt and the exported .md all carried
    # no provenance, so a deterministic-floor scaffold read as an "AI deliverable". Provenance travels
    # with the output, not beside it.
    served_by: Optional[str] = None
    is_external: bool = False
    provenance_basis: str = ""


class Project(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    # W364 — the owner this project belongs to. Stamped SERVER-side on create; legacy projects
    # written before ownership existed carry None and are admin-only (never leaked to a tenant).
    owner_id: Optional[str] = None
    title: str
    description: str
    realm: str = "general"          # W505: a DOMAIN or a legacy value — see _valid_subject
    domain: str = "product"
    taxonomy_realm: str = "enterprise"      # W505 (P2.5) — the taxonomy's realm axis
    realm_source: str = ""                  # W505 — which axis `realm` came from, said not guessed
    stage: Stage = "concept"
    status: Literal["idle", "running", "done", "error"] = "idle"
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    outputs: list[ProjectOutput] = Field(default_factory=list)


class CreateProjectRequest(BaseModel):
    title: str
    description: str
    realm: str = "general"          # W505: a DOMAIN or a legacy value — see _valid_subject
    domain: str = "product"
    # W505 (P2.5) — the taxonomy's realm axis, ADDED rather than written over `realm` above. It changes
    # the DEPTH and REGISTER of what is generated (taxonomy.realm_directive), which no project generation
    # consulted before. Validated by normalise_realm, so an unknown value becomes the canonical default
    # instead of being stored as a realm that does not exist.
    taxonomy_realm: str = "enterprise"


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


def _load_scoped(project_id: str, user: dict | None) -> Project:
    """W364 — load a project the caller is entitled to. A project owned by someone else is
    indistinguishable from one that does not exist (404-never-403), so the store cannot be probed
    for other tenants' ids. Auth-off single-user mode is unguarded by design."""
    project = _load(project_id)
    if not user_can_access(user, project.owner_id):
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return project


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
_OUTPUTS_DIR = Path((os.getenv("SYNTHESIS_OUTPUT_DIR") or str(data_path("synthesis_outputs"))))
_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def _save_output(project: Project, text: str,
                 served_by: str | None = None, is_external: bool = False) -> ProjectOutput:
    output_id = uuid.uuid4().hex
    # W495 (FU-131, S12.6) - the file on disk is what a Download hands the user, so the label goes INTO
    # it (the W490 rule: provenance travels with the output, and a browser-side helper cannot reach a
    # file served straight off disk).
    _basis = ("composed by the deterministic in-house floor - not model-generated analysis"
              if (served_by or "native") == "native" and not is_external else
              f"generated by {served_by}" + (" (external provider)" if is_external else " (in-house model)")
              if served_by else "provenance not recorded for this output")
    out_path = _OUTPUTS_DIR / f"{output_id}.txt"
    out_path.write_text(f"_[{_basis}]_\n\n{text}", encoding="utf-8")
    output = ProjectOutput(
        output_id=output_id,
        stage=project.stage,
        created_at=time.time(),
        download_url=f"/api/v1/synthesis/download/{output_id}",
        preview=text[:400],
        served_by=served_by,
        is_external=is_external,
        provenance_basis=_basis,
    )
    project.outputs.append(output)
    return output


# ── Governance proposals (models + helpers — routes registered BEFORE /{project_id}) ──

_PROPOSALS_DIR = Path((os.getenv("PROPOSALS_DIR") or str(data_path("proposals"))))
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

    return {
        "total_projects": total,
        "by_stage": by_stage,
        "by_realm": by_realm,
        "total_outputs": total_outputs,
        "active": sum(1 for p in projects if p.status == "running"),
        "complete": sum(1 for p in projects if p.stage == "commercialise"),
        "cpu_percent": round(cpu, 1),
        "memory_percent": round(mem, 1),
        #  W642 (FU-655, ledger v14 R5) - this was min(1, 0.70 + 0.02 x the number of projects): a formula
        #  over a COUNT, returned as a health figure. Nothing measures swarm health here. The key stays so a
        #  reader of it gets a statement rather than a KeyError, and the statement is that it is not measured.
        "swarm_health": None,
        "swarm_health_basis": "not measured: no instrument here observes the swarm's health",
    }


@router.get("/governance/proposals", response_model=list[Proposal])
async def list_proposals() -> list[Proposal]:
    return _all_proposals()


@router.post("/governance/proposals/{proposal_id}/vote", response_model=Proposal)
async def vote_proposal(proposal_id: str, approve: bool = True) -> Proposal:
    proposal = _load_proposal(proposal_id)
    if proposal.status != "pending":
        raise HTTPException(status_code=400, detail=f"Proposal already {proposal.status}.")
    # §5 (W495, FU-131, S10.1) — this approved first and applied blindly. The proposal RECORDS the
    # stage it was raised from, and nothing checked it, so approving a stale concept->prototype proposal
    # after the project had reached commercialise moved the stage BACKWARD while the page said "stage
    # advanced". And `except Exception: pass` meant approving a proposal whose project had been DELETED
    # returned 200 "approved" with nothing advanced. A decision must not be recorded as taken when the
    # thing it decides cannot be done: both cases now refuse, and nothing is written.
    if approve:
        try:
            project = _load(proposal.project_id)
        except HTTPException:
            raise HTTPException(status_code=404, detail=(
                f"The project this proposal refers to ({proposal.project_id}) no longer exists, so the "
                f"stage cannot advance. Nothing was approved."))
        if project.stage != proposal.from_stage:
            raise HTTPException(status_code=409, detail=(
                f"This proposal was raised from '{proposal.from_stage}' and the project is now at "
                f"'{project.stage}'. Approving it would set the stage to '{proposal.to_stage}'"
                + (" — backwards." if STAGE_ORDER.index(proposal.to_stage) < STAGE_ORDER.index(project.stage)
                   else " — from a stage it has left.")
                + " Nothing was approved; raise a new proposal from the current stage."))
        project.stage = proposal.to_stage
        project.status = "idle"
        _save(project)          # a save that fails must surface, never be swallowed
        proposal.votes_for += 1
        proposal.status = "approved"
    else:
        proposal.votes_against += 1
        proposal.status = "rejected"
    _save_proposal(proposal)
    return proposal


# ── CRUD endpoints ────────────────────────────────────────────────────────────

@router.post("/", response_model=Project, status_code=201)
async def create_project(req: CreateProjectRequest,
                         user: dict | None = Depends(get_current_user)) -> Project:
    # W505 (P2.5) — the two axes, resolved ONCE. `realm` may carry either a taxonomy domain or a
    # canonical realm depending on the entry path (the picker sends a realm, a domain hub's CTA sends a
    # domain), so the axis is determined first and the canonical realm is seeded from it when that is what
    # arrived — otherwise from the request's own `taxonomy_realm`.
    from agentic_core.taxonomy import REALMS as _REALMS, normalise_realm as _norm
    _subject = _valid_subject(req.realm)
    _tax_realm = _norm(_subject[0] if _subject[0] in _REALMS else req.taxonomy_realm)
    project = Project(
        owner_id=request_owner_id(user),   # W364 — server-stamped; a client cannot claim an owner
        title=req.title,
        description=req.description,
        # W505 (P2.5) — validated against the taxonomy, and the row says which axis the value is from.
        # When `realm` IS a canonical realm (the picker's path), it also seeds `taxonomy_realm`, so a
        # picker-created project carries the realm the user chose rather than the field's default.
        realm=_subject[0],
        realm_source=_subject[1],
        taxonomy_realm=_tax_realm,
        domain=req.domain.lower(),
    )
    _save(project)
    biobus.fire_signal("sensory", "projects.create",
                       f"New project: {req.title} [{req.realm}/{req.domain}]", 0.5)
    return project


@router.get("/", response_model=list[Project])
async def list_projects(user: dict | None = Depends(get_current_user)) -> list[Project]:
    # W364 — a tenant sees only their own projects (auth-off returns everything, unchanged)
    return [p for p in _all_projects() if user_can_access(user, p.owner_id)]


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str, user: dict | None = Depends(get_current_user)) -> Project:
    return _load_scoped(project_id, user)


@router.patch("/{project_id}", response_model=Project)
async def update_project(project_id: str, req: UpdateProjectRequest,
                         user: dict | None = Depends(get_current_user)) -> Project:
    project = _load_scoped(project_id, user)
    if req.title is not None:
        project.title = req.title
    if req.description is not None:
        project.description = req.description
    _save(project)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, user: dict | None = Depends(get_current_user)) -> None:
    # W364 — deletion is destructive and was previously unscoped: any signed-in user could
    # permanently delete another user's project. Scoped now (404 when not the caller's).
    _load_scoped(project_id, user)
    _path(project_id).unlink()


# ── AI Run endpoint (SSE streaming) ──────────────────────────────────────────

@router.post("/{project_id}/run")
async def run_project(project_id: str,
                      user: dict | None = Depends(get_current_user)) -> StreamingResponse:
    """
    Stream AI-generated content for this project's current stage.
    SSE format:
      data: {"token": "..."}          — incremental token
      data: {"done": true, "output_id": "...", "download_url": "..."}  — final
      data: {"error": "..."}          — on failure
    """
    project = _load_scoped(project_id, user)
    if project.status == "running":
        raise HTTPException(status_code=409, detail="Project is already running")

    project.status = "running"
    _save(project)

    system_prompt = REALM_PROMPTS.get(project.realm, REALM_PROMPTS["general"])
    stage_instruction = STAGE_PROMPTS[project.stage]
    # W505 (P2.5) — the realm axis DOES something now. taxonomy.py says "realm changes the DEPTH and
    # REGISTER of what is generated", and no project generation consulted it: the prompt named
    # `project.realm` (a domain) and nothing else. The directive is prepended so the axis is real.
    from agentic_core.taxonomy import normalise_realm as _nr, realm_directive as _rd
    _realm = _nr(getattr(project, "taxonomy_realm", "") or "enterprise")
    full_prompt = (
        f"{_rd(_realm)}\n\n"
        f"{stage_instruction}\n\n"
        f"Project title: {project.title}\n"
        f"Project description: {project.description}\n"
        f"Subject: {project.realm} · Domain: {project.domain} · Realm: {_realm}\n\n"
        f"Produce a comprehensive, professional document now."
    )

    async def event_stream() -> AsyncIterator[str]:
        accumulated = ""
        completed = False
        biobus.fire_signal("cognitive", "projects.run", f"{project.title} [{project.stage}]", 0.6)
        try:
            fin: dict = {}
            # W451 — stream_meta: the done frame discloses who served it and whether the profile shaped it
            # P2.2 (W511) — stated, not inherited: the prompt is already composed from this project's
            # own record, so no cross-request recall is wanted here.
            # §17.5 invariant 1 (W343, FU-276) — the caller's identity reaches the memory layer, or what they asked for is stored where even they cannot recall it.
            _owner_id = user.get("username") if isinstance(user, dict) else None
            async for ev in gateway.stream_meta(full_prompt, agent="projects", augment=False, owner_id=_owner_id,
                                                user_text=(chr(10).join(x for x in (   # W651 (FU-675)
                                                    project.title, project.description) if x) or None)):
                if "token" in ev:
                    accumulated += ev["token"]
                    safe = ev["token"].replace("\n", "\\n")
                    yield f'data: {{"token": {json.dumps(safe)}}}\n\n'
                elif ev.get("done"):
                    fin = ev
            if fin.get("guardrail_passed") is False:
                accumulated = fin.get("output") or accumulated   # persist the replacement, never the violation

            # Persist and close out
            output = _save_output(project, accumulated,
                                  served_by=fin.get("served_by"),
                                  is_external=bool(fin.get("is_external")))
            project.status = "done"
            _save(project)
            completed = True
            biobus.record_operation("project_run", "projects.run", success=True, payload=f"{project.title}")
            yield (
                f'data: {{"done": true, "output_id": "{output.output_id}", '
                f'"download_url": "{output.download_url}", '
                f'"served_by": {json.dumps(fin.get("served_by"))}, "is_external": {json.dumps(bool(fin.get("is_external")))}, '
                f'"profile_applied": {json.dumps(bool(fin.get("profile_applied")))}, '
                f'"preview": {json.dumps(output.preview)}}}\n\n'
            )
        except Exception as exc:
            project.status = "error"
            _save(project)
            biobus.record_operation("project_run", "projects.run", success=False)
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
async def advance_stage(project_id: str,
                        user: dict | None = Depends(get_current_user)) -> Project:
    """
    Advance the project's lifecycle stage: concept → prototype → commercialise.
    Guard: at least one output must exist at the current stage before advancing.
    """
    project = _load_scoped(project_id, user)
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

    prev_stage = project.stage
    project.stage = STAGE_ORDER[current_idx + 1]
    project.status = "idle"
    _save(project)
    biobus.fire_signal(
        "motor", "projects.advance",
        f"{project.title}: {prev_stage} → {project.stage}",
        0.7,
    )
    return project


# ── Outputs list ──────────────────────────────────────────────────────────────

@router.get("/{project_id}/outputs", response_model=list[ProjectOutput])
async def list_outputs(project_id: str,
                       user: dict | None = Depends(get_current_user)) -> list[ProjectOutput]:
    project = _load_scoped(project_id, user)
    return list(reversed(project.outputs))


# ── Governance propose-advance (per-project, needs project_id) ────────────────

@router.post("/{project_id}/propose-advance", response_model=Proposal, status_code=201)
async def propose_advance(project_id: str,
                          user: dict | None = Depends(get_current_user)) -> Proposal:
    """
    Create a governance proposal to advance this project's stage.
    The stage does NOT advance until the proposal is approved via GovernanceHub.
    """
    project = _load_scoped(project_id, user)
    current_idx = STAGE_ORDER.index(project.stage)
    if current_idx >= len(STAGE_ORDER) - 1:
        raise HTTPException(status_code=400, detail="Already at final stage.")
    has_output = any(o.stage == project.stage for o in project.outputs)
    if not has_output:
        raise HTTPException(
            status_code=422,
            detail=f"Run the AI workflow at the '{project.stage}' stage before requesting advancement.",
        )
    # §5 (W495, FU-131, S10.1) — clicking Propose Advance twice created two pending proposals for the
    # same step, which is how a STALE proposal came to exist: advance by other means, then approve the
    # leftover and the stage moves backward. One pending proposal per project and from_stage.
    for _p in _all_proposals():
        if (_p.status == "pending" and _p.project_id == project.id
                and _p.from_stage == project.stage):
            raise HTTPException(status_code=409, detail=(
                f"A pending proposal to advance this project from '{project.stage}' already exists "
                f"({_p.id}). Approve or reject that one rather than raising a second."))
    proposal = Proposal(
        project_id=project.id,
        project_title=project.title,
        from_stage=project.stage,
        to_stage=STAGE_ORDER[current_idx + 1],
    )
    _save_proposal(proposal)
    return proposal


