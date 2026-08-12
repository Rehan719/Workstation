"""
Evolution Engine — AI-generated system improvement proposals.

The IDBO can observe its own state (projects, immune health, biometrics) and
propose improvements to itself. Users vote to accept or reject proposals.

  GET  /api/v191/evolution/proposals         — list current proposals
  POST /api/v191/evolution/proposals/generate — ask AI to generate new proposals
  POST /api/v191/evolution/proposals/{id}/approve
  POST /api/v191/evolution/proposals/{id}/reject
  GET  /api/v191/evolution/history           — approved/rejected log
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/evolution", tags=["evolution"])

_STORE = data_path("evolution_proposals.json")


def _load() -> list[dict]:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text())
        except Exception:
            pass
    return []


def _save(proposals: list[dict]) -> None:
    from agentic_core.config import atomic_write_json
    atomic_write_json(_STORE, proposals)


def _mirror_cca_outcomes(proposals: list[dict]) -> list[dict]:
    """Arms-length reconciliation: a proposal routed to Change Control mirrors ITS CCA's outcome
    (approved/implemented → approved; rejected → rejected) — the fragment can no longer diverge from
    the governed decision."""
    changed = False
    for p in proposals:
        if p.get("status") == "under_change_control" and p.get("cca_id"):
            try:
                from agentic_core.api.change_control import _load_change
                c = _load_change(p["cca_id"]) or {}
                if c.get("status") in ("approved", "implemented"):
                    p["status"] = "approved"
                    p["resolved_at"] = c.get("implemented_at") or c.get("reviewed_at")
                    changed = True
                elif c.get("status") == "rejected":
                    p["status"] = "rejected"
                    p["resolved_at"] = c.get("reviewed_at")
                    changed = True
            except Exception:
                pass
    if changed:
        _save(proposals)
    return proposals


@router.get("/proposals")
async def get_proposals(status: str = "pending"):
    """Return proposals filtered by status (pending | under_change_control | approved | rejected | all).
    Proposals routed to Change Control mirror their CCA's governed outcome."""
    proposals = _mirror_cca_outcomes(_load())
    if status != "all":
        proposals = [p for p in proposals if p.get("status") == status]
    return proposals


class GenerateRequest(BaseModel):
    context: str = ""


@router.post("/proposals/generate")
async def generate_proposals(req: GenerateRequest):
    """
    Observe system state and generate AI improvement proposals.
    """
    system_context = ""
    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        stages: dict[str, int] = {}
        for p in projects:
            stages[p.stage] = stages.get(p.stage, 0) + 1
        system_context += f"Projects: {len(projects)} total — {stages}\n"
    except Exception:
        system_context += "Projects: unavailable\n"

    try:
        from agentic_core.organism.immune import immune
        imm = immune.status()
        system_context += (
            f"Immune health: {imm['health']} ({imm['threat_level']}), "
            f"errors in window: {imm['errors_in_window']}\n"
        )
    except Exception:
        system_context += "Immune: unavailable\n"

    try:
        import psutil
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        system_context += f"System: CPU {cpu}%, Memory {mem}%\n"
    except Exception:
        pass

    if req.context:
        system_context += f"User context: {req.context}\n"

    prompt = (
        "You are the Evolution Engine of an Intelligent Digital Biomimetic Organism (IDBO) "
        "called Workstation. Your role is to observe the system's state and propose "
        "concrete, actionable improvements.\n\n"
        f"Current system state:\n{system_context}\n"
        "Generate exactly 4 improvement proposals. For each, provide:\n"
        "PROPOSAL_N | TYPE | TITLE | DESCRIPTION | IMPACT | RATIONALE\n\n"
        "Where:\n"
        "  TYPE: UX_OPTIMIZATION | PERFORMANCE | RESILIENCE | FEATURE | PROCESS\n"
        "  IMPACT: High | Medium | Low\n"
        "  TITLE: max 10 words\n"
        "  DESCRIPTION: 1-2 sentences, specific and actionable\n"
        "  RATIONALE: why now, what observation triggered this\n\n"
        "Output only the 4 PROPOSAL lines, no other text."
    )

    raw = await gateway.query(prompt, agent="evolution_engine")

    proposals = _load()
    new_proposals = []

    for line in raw.splitlines():
        line = line.strip()
        if not line.upper().startswith("PROPOSAL_"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6:
            continue
        try:
            proposal = {
                "id": f"ep-{uuid.uuid4().hex[:8]}",
                "type": parts[1].upper().replace(" ", "_"),
                "title": parts[2],
                "description": parts[3],
                "impact": parts[4].capitalize(),
                "rationale": parts[5],
                "status": "pending",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            proposals.append(proposal)
            new_proposals.append(proposal)
        except Exception:
            continue

    if not new_proposals:
        fallback = {
            "id": f"ep-{uuid.uuid4().hex[:8]}",
            "type": "PERFORMANCE",
            "title": "Review AI provider failover strategy",
            "description": (raw[:200] if raw else "No parseable proposals generated."),
            "impact": "Medium",
            "rationale": "System observation triggered this review.",
            "status": "pending",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        proposals.append(fallback)
        new_proposals.append(fallback)

    _save(proposals)
    return {"generated": len(new_proposals), "proposals": new_proposals}


@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: str):
    """Approving a self-modification proposal now files a REAL Change Control request and holds the
    proposal `under_change_control` — the arms-length chain (LOW auto-approve when healthy;
    MEDIUM/HIGH AI review; CRITICAL blocked; HIGH/CRITICAL twin pre-validation) decides, not this
    fragment. Previously this endpoint self-approved outside all governance."""
    proposals = _load()
    for p in proposals:
        if p["id"] == proposal_id:
            if p.get("status") == "under_change_control" and p.get("cca_id"):
                return {"status": "under_change_control", "proposal_id": proposal_id,
                        "cca_id": p["cca_id"], "note": "Already with the Change Control Agency."}
            if p.get("status") in ("approved", "rejected"):
                return {"status": p["status"], "proposal_id": proposal_id, "cca_id": p.get("cca_id"),
                        "note": "Already resolved — no duplicate Change Control request filed."}
            from agentic_core.api.change_control import submit_change, SubmitChangeRequest
            impact = str(p.get("impact", "Medium")).lower()
            change_type = {"high": "platform_upgrade", "medium": "capability_add",
                           "low": "config_minor"}.get(impact, "capability_add")
            cca = await submit_change(SubmitChangeRequest(
                title=f"[evolution] {p.get('title', proposal_id)}"[:120],
                change_type=change_type,
                description=str(p.get("description", ""))[:800],
                rationale=str(p.get("rationale", "Evolution-engine proposal (v191 fragment)"))[:400],
                affected_systems=["evolution"], submitted_by="evolution:v191",
                rollback_plan="Proposal only — no action taken until governed implementation."))
            p["status"] = "approved" if cca.get("status") == "approved" else "under_change_control"
            p["cca_id"] = cca.get("cca_id")
            p["resolved_at"] = (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                                if p["status"] == "approved" else None)
            _save(proposals)
            return {"status": p["status"], "proposal_id": proposal_id, "title": p.get("title"),
                    "cca_id": p["cca_id"], "impact_tier": cca.get("impact_tier"),
                    "governance": "arms-length via the Change Control Agency"}
    raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found.")


@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: str):
    proposals = _load()
    for p in proposals:
        if p["id"] == proposal_id:
            p["status"] = "rejected"
            p["resolved_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            _save(proposals)
            return {"status": "rejected", "proposal_id": proposal_id}
    raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found.")


@router.get("/history")
async def evolution_history():
    proposals = _load()
    resolved = [p for p in proposals if p.get("status") in ("approved", "rejected")]
    return {
        "resolved": resolved,
        "total_approved": sum(1 for p in resolved if p["status"] == "approved"),
        "total_rejected": sum(1 for p in resolved if p["status"] == "rejected"),
    }
