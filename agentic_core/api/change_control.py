"""
Change Control Agency (CCA) — Arms-Length Governance for Organism Changes.

The CCA is an autonomous governance body that reviews and approves/rejects
changes to the IDBO organism — configuration changes, VSB mutations,
platform upgrades, policy amendments, and capability additions.

Biological analogy: the CCA mirrors the adaptive immune system's memory B-cells
— every significant change is reviewed, recorded, and either integrated or
rejected with reasoning. The constitutional gate (GaaS) is consulted on
high-impact changes.

Governance tiers:
  LOW    — auto-approved if organism is healthy (config tweaks, minor docs)
  MEDIUM — AI review required, logged, 24h cooling period
  HIGH   — AI review + constitutional alignment check + manual flag
  CRITICAL — blocked pending explicit admin approval

  POST /api/v1/cca/submit           — submit a change request
  GET  /api/v1/cca/queue            — pending change requests
  POST /api/v1/cca/{cca_id}/review  — trigger AI review (auto or on-demand)
  GET  /api/v1/cca/approved         — approved change log
  GET  /api/v1/cca/rejected         — rejected change log
  GET  /api/v1/cca/{cca_id}         — get a specific change request
  POST /api/v1/cca/{cca_id}/implement — mark change as implemented
  GET  /api/v1/cca/impact/{cca_id}  — AI impact assessment
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1/cca", tags=["change-control-agency"])

_CCA_STORE = Path("data/change_control")
_CCA_STORE.mkdir(parents=True, exist_ok=True)

ChangeStatus = Literal["submitted", "under_review", "approved", "rejected", "implemented", "withdrawn"]
ImpactTier = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def _cca_path(cca_id: str) -> Path:
    return _CCA_STORE / f"{cca_id}.json"


def _load_change(cca_id: str) -> dict | None:
    p = _cca_path(cca_id)
    return json.loads(p.read_text()) if p.exists() else None


def _save_change(change: dict) -> None:
    _cca_path(change["cca_id"]).write_text(json.dumps(change, indent=2))


def _list_changes(status_filter: str | None = None) -> list[dict]:
    result = []
    for p in sorted(_CCA_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            c = json.loads(p.read_text())
            if status_filter and c.get("status") != status_filter:
                continue
            result.append({
                "cca_id": c["cca_id"],
                "title": c.get("title", ""),
                "change_type": c.get("change_type", ""),
                "impact_tier": c.get("impact_tier", "MEDIUM"),
                "status": c.get("status", "submitted"),
                "submitted_by": c.get("submitted_by", "system"),
                "submitted_at": c.get("submitted_at", ""),
                "reviewed_at": c.get("reviewed_at"),
                "decision": c.get("decision"),
            })
        except Exception:
            pass
    return result


# ── Impact tier determination ─────────────────────────────────────────────────

_TIER_MAP: dict[str, ImpactTier] = {
    "config_minor":         "LOW",
    "config_major":         "MEDIUM",
    "organism_mutation":    "HIGH",
    "vsb_evolution":        "MEDIUM",
    "genome_edit":          "HIGH",
    "constitutional":       "CRITICAL",
    "platform_upgrade":     "MEDIUM",
    "capability_add":       "MEDIUM",
    "capability_remove":    "HIGH",
    "policy_amendment":     "HIGH",
    "data_schema":          "MEDIUM",
    "security_change":      "HIGH",
    "integration_add":      "LOW",
    "integration_remove":   "MEDIUM",
}


def _determine_tier(change_type: str, description: str) -> ImpactTier:
    base = _TIER_MAP.get(change_type, "MEDIUM")
    # Elevate if keywords suggest constitutional or organism impact
    critical_keywords = ["constitution", "genome core", "delete all", "reset organism", "override gaas"]
    if any(k in description.lower() for k in critical_keywords):
        return "CRITICAL"
    return base


# ── Request models ────────────────────────────────────────────────────────────

class SubmitChangeRequest(BaseModel):
    title: str
    change_type: str = "config_minor"
    description: str
    rationale: str = ""
    affected_systems: list[str] = []
    submitted_by: str = "system"
    vsb_id: str | None = None
    rollback_plan: str = ""


class ReviewDecision(BaseModel):
    override_decision: str | None = None  # "approved" | "rejected" | None (use AI)
    reviewer_notes: str = ""


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/submit")
async def submit_change(req: SubmitChangeRequest):
    """Submit a change request to the Change Control Agency."""
    cca_id = f"cca-{uuid.uuid4().hex[:10]}"
    tier = _determine_tier(req.change_type, req.description)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    change = {
        "cca_id": cca_id,
        "title": req.title,
        "change_type": req.change_type,
        "description": req.description,
        "rationale": req.rationale,
        "affected_systems": req.affected_systems,
        "submitted_by": req.submitted_by,
        "submitted_at": now,
        "impact_tier": tier,
        "status": "submitted",
        "vsb_id": req.vsb_id,
        "rollback_plan": req.rollback_plan,
        "review_result": None,
        "decision": None,
        "reviewed_at": None,
        "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": req.submitted_by}],
    }

    # AUTO-APPROVE low-tier changes when organism is healthy
    ctx = biobus.organism_context()
    if tier == "LOW" and ctx["composite_health"] >= 0.6:
        change["status"] = "approved"
        change["decision"] = "auto_approved"
        change["reviewed_at"] = now
        change["review_result"] = "Auto-approved: LOW impact change, organism healthy."
        change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "biobus"})
        biobus.fire_signal("motor", "cca.auto_approve", f"Auto-approved: {req.title}", 0.3)
    else:
        biobus.fire_signal("sensory", "cca.submit", f"Change submitted: {req.title} [{tier}]", 0.5)

    _save_change(change)
    return {
        "cca_id": cca_id,
        "impact_tier": tier,
        "status": change["status"],
        "message": f"Change request {cca_id} submitted. Tier: {tier}. Status: {change['status']}.",
    }


@router.get("/queue")
async def get_queue():
    """List all pending change requests awaiting review."""
    pending = _list_changes("submitted") + _list_changes("under_review")
    return {"queue": pending, "total": len(pending)}


@router.get("/approved")
async def get_approved():
    return {"changes": _list_changes("approved"), "total": len(_list_changes("approved"))}


@router.get("/rejected")
async def get_rejected():
    return {"changes": _list_changes("rejected"), "total": len(_list_changes("rejected"))}


@router.get("/implemented")
async def get_implemented():
    return {"changes": _list_changes("implemented"), "total": len(_list_changes("implemented"))}


@router.get("/{cca_id}")
async def get_change(cca_id: str):
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    return c


@router.post("/{cca_id}/review")
async def review_change(cca_id: str, req: ReviewDecision):
    """
    Trigger AI review of a change request.
    Organism context is included so the AI can assess impact against current health.
    """
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] not in ("submitted", "under_review"):
        raise HTTPException(status_code=400, detail=f"Change is {c['status']} — cannot review.")

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    c["status"] = "under_review"
    c["audit_trail"].append({"event": "review_started", "ts": now})
    _save_change(c)

    biobus.fire_signal("cognitive", "cca.review", f"Reviewing: {c['title']}", 0.6)

    if req.override_decision:
        decision = req.override_decision
        review_text = f"Manual override: {req.reviewer_notes or 'No notes.'}"
    else:
        # AI review
        ctx = biobus.organism_context()
        prompt = (
            f"You are the Chief Governance Officer of Workstation IDBO, reviewing a change request.\n\n"
            f"Change Title: {c['title']}\n"
            f"Type: {c['change_type']}\n"
            f"Impact Tier: {c['impact_tier']}\n"
            f"Description: {c['description']}\n"
            f"Rationale: {c['rationale'] or 'Not provided.'}\n"
            f"Affected Systems: {', '.join(c['affected_systems']) or 'Not specified.'}\n"
            f"Rollback Plan: {c['rollback_plan'] or 'Not provided.'}\n\n"
            f"Current Organism Health:\n"
            f"  Composite health: {ctx['composite_health']:.0%}\n"
            f"  Immune threat: {ctx['immune']['threat_level']}\n"
            f"  Organism mode: {ctx['mode']}\n"
            f"  Circadian cycle: {ctx['circadian']['cycle']}\n\n"
            f"Assess this change against:\n"
            f"1. Necessity — is this change truly needed?\n"
            f"2. Risk — what could go wrong? Is the rollback plan adequate?\n"
            f"3. Timing — is now the right time given organism health?\n"
            f"4. Alignment — does this align with the IDBO mission and constitution?\n"
            f"5. Decision — APPROVED or REJECTED, with one clear sentence of reasoning.\n\n"
            f"End your response with exactly one of: [DECISION: APPROVED] or [DECISION: REJECTED]"
        )
        review_text = await gateway.query(prompt, agent="cca_review")

        if "[DECISION: APPROVED]" in review_text.upper():
            decision = "approved"
        elif "[DECISION: REJECTED]" in review_text.upper():
            decision = "rejected"
        else:
            # Default to approved for non-critical when organism is healthy
            decision = "approved" if (
                c["impact_tier"] != "CRITICAL" and ctx["composite_health"] >= 0.5
            ) else "rejected"

    c["status"] = decision
    c["decision"] = decision
    c["reviewed_at"] = now
    c["review_result"] = review_text
    c["audit_trail"].append({"event": decision, "ts": now, "by": "cca_ai"})
    _save_change(c)

    signal = "motor" if decision == "approved" else "reflex"
    biobus.fire_signal(signal, "cca.decision", f"CCA {decision.upper()}: {c['title']}", 0.6)

    return {
        "cca_id": cca_id,
        "decision": decision,
        "review_result": review_text[:500],
        "status": c["status"],
    }


@router.post("/{cca_id}/implement")
async def implement_change(cca_id: str):
    """Mark an approved change as implemented."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] != "approved":
        raise HTTPException(status_code=400, detail=f"Change must be approved before implementation. Status: {c['status']}")

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    c["status"] = "implemented"
    c["implemented_at"] = now
    c["audit_trail"].append({"event": "implemented", "ts": now})
    _save_change(c)

    biobus.fire_signal("motor", "cca.implement", f"Implemented: {c['title']}", 0.7)
    return {"cca_id": cca_id, "status": "implemented", "implemented_at": now}


@router.get("/impact/{cca_id}")
async def impact_assessment(cca_id: str):
    """AI-generated impact assessment for a change request."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")

    ctx = biobus.organism_context()
    prompt = (
        f"You are an impact assessment specialist for Workstation IDBO.\n\n"
        f"Change: {c['title']}\n"
        f"Description: {c['description']}\n"
        f"Affected systems: {', '.join(c['affected_systems']) or 'unknown'}\n"
        f"Current organism mode: {ctx['mode']}\n\n"
        f"Provide a concise impact assessment:\n"
        f"## Direct Impacts (systems affected)\n"
        f"## Indirect Impacts (downstream effects)\n"
        f"## Risks (what could go wrong)\n"
        f"## Mitigation (how to reduce risk)\n"
        f"## Estimated Recovery Time (if something goes wrong)\n"
        f"## Recommended Implementation Window (best time relative to circadian cycle)\n"
    )
    assessment = await gateway.query(prompt, agent="cca_impact")
    biobus.fire_signal("cognitive", "cca.impact", f"Impact assessed: {c['title']}", 0.4)
    return {"cca_id": cca_id, "assessment": assessment, "organism_mode": ctx["mode"]}


@router.get("")
async def list_all_changes():
    """List all change requests across all statuses."""
    all_changes = _list_changes()
    by_status: dict[str, int] = {}
    for c in all_changes:
        s = c["status"]
        by_status[s] = by_status.get(s, 0) + 1
    return {"changes": all_changes[:50], "total": len(all_changes), "by_status": by_status}
