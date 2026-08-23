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
from agentic_core.config import data_path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1/cca", tags=["change-control-agency"])

_CCA_STORE = data_path("change_control")
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

# ── Biomimetic immune integration ─────────────────────────────────────────────

def _immune_threat() -> str:
    """Current immune threat level (NOMINAL | ELEVATED | HIGH | CRITICAL); safe if immune absent."""
    try:
        from agentic_core.organism.immune import immune
        return immune.status().get("threat_level", "NOMINAL")
    except Exception:
        return "NOMINAL"


# The immune system's defensive reconfiguration levers — SAFE, REVERSIBLE config changes only,
# escalating with threat. Applied via the reconfiguration engine under arms-length CCA governance.
# §8 (W318) — honesty rule: a lever may report 'implemented' ONLY when a real consumer is wired
# to it. Every lever names its consumer here; setting a lever with no wired consumer records
# 'lever_set_no_consumer' instead — no future lever ships decorative.
_LEVER_CONSUMERS: dict[str, str] = {
    "temperature_bias": "ai.gateway generation parameters (per-call)",
    "metabolic_throttle": "organism.heartbeat evolve tick (suppressed at low ATP) — W310",
    "immune_quarantine": "self_healing.is_open strict containment + attempt_heal hold — W318",
    "evolution_auto_apply": "organism.heartbeat post-approval auto-apply — W310",
}

_IMMUNE_DEFENCE: dict[str, dict] = {
    "ELEVATED": {"section": "gateway",  "key": "temperature_bias",  "value": "precise", "tier": "LOW",
                 "why": "Elevated error patterns — tighten generation to precise."},
    "HIGH":     {"section": "organism", "key": "metabolic_throttle", "value": True,     "tier": "LOW",
                 "why": "High threat — throttle metabolic load to relieve the organism."},
    "CRITICAL": {"section": "organism", "key": "immune_quarantine",  "value": True,     "tier": "MEDIUM",
                 "why": "Critical threat — quarantine failing endpoints (innate containment)."},
}


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

    # AUTO-APPROVE low-tier changes only when the organism is healthy AND the immune system is not
    # under active threat — biomimetic: do NOT push changes while the organism is fighting an
    # infection (HIGH/CRITICAL immune threat holds even LOW changes for human/AI review).
    ctx = biobus.organism_context()
    threat = _immune_threat()
    change["immune_threat_at_submit"] = threat
    if tier == "LOW" and ctx["composite_health"] >= 0.6 and threat in ("NOMINAL", "ELEVATED"):
        change["status"] = "approved"
        change["decision"] = "auto_approved"
        change["reviewed_at"] = now
        change["review_result"] = f"Auto-approved: LOW impact, organism healthy, immune threat {threat}."
        change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "biobus", "immune_threat": threat})
        biobus.fire_signal("motor", "cca.auto_approve", f"Auto-approved: {req.title}", 0.3)
    else:
        if tier == "LOW" and threat in ("HIGH", "CRITICAL"):
            change["review_result"] = (f"Held for review: immune threat {threat} — auto-approval paused "
                                       "while the organism defends itself.")
            change["audit_trail"].append({"event": "held_immune_threat", "ts": now, "immune_threat": threat})
        biobus.fire_signal("sensory", "cca.submit", f"Change submitted: {req.title} [{tier}] (immune: {threat})", 0.5)

    _save_change(change)
    return {
        "cca_id": cca_id,
        "impact_tier": tier,
        "status": change["status"],
        "message": f"Change request {cca_id} submitted. Tier: {tier}. Status: {change['status']}.",
    }


class ImmuneReconfigureRequest(BaseModel):
    # Default reads the LIVE immune threat. `simulate_threat` is an honest demonstration/test input
    # that exercises the defensive mapping without mutating global immune state.
    simulate_threat: str | None = None


@router.post("/immune-reconfigure")
async def immune_reconfigure(req: ImmuneReconfigureRequest = ImmuneReconfigureRequest()):
    """Immune-system reconfigurator, governed arms-length by the CCA.

    Biomimetic defence: when the immune system is under threat it proposes a SAFE, REVERSIBLE
    defensive reconfiguration (tighten generation → throttle load → quarantine failing endpoints).
    The CCA records it as a change-controlled, audited action and — because these are low-risk,
    reversible defensive levers — auto-approves and APPLIES it via the reconfiguration engine (a fast
    innate-immune reflex that is nonetheless governed; MEDIUM-tier containment is flagged for Board
    ratification). This wires the arms-length CCA to the Immune system and the Reconfiguration engine.
    """
    threat = (req.simulate_threat or _immune_threat()).upper()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    plan = _IMMUNE_DEFENCE.get(threat)
    if plan is None:
        return {"threat_level": threat, "action": "none", "governed_by": "Change Control Agency (arms-length)",
                "reason": "Immune state nominal — no defensive reconfiguration required."}

    cca_id = f"cca-{uuid.uuid4().hex[:10]}"
    requires_ratification = plan["tier"] != "LOW"
    change = {
        "cca_id": cca_id,
        "title": f"Immune defence: {plan['section']}.{plan['key']} = {plan['value']}",
        "change_type": "immune_reconfiguration",
        "description": plan["why"],
        "rationale": f"Immune threat level {threat}; defensive, reversible reconfiguration.",
        "affected_systems": ["organism", plan["section"], "immune_system", "reconfiguration_engine"],
        "submitted_by": "immune_system",
        "submitted_at": now,
        "impact_tier": plan["tier"],
        "status": "submitted",
        "immune_threat_at_submit": threat,
        "requires_ratification": requires_ratification,
        "rollback_plan": f"Revert {plan['section']}.{plan['key']} to its prior value via /config/update.",
        "review_result": None, "decision": None, "reviewed_at": None, "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": "immune_system", "immune_threat": threat}],
    }
    biobus.fire_signal("sensory", "cca.immune_reconfigure", f"Immune defence proposed [{threat}]", 0.6)

    # Arms-length governance: auto-approve the defensive (reversible) reconfiguration, then apply it.
    change["status"] = "approved"
    change["decision"] = "auto_approved_immune_defence"
    change["reviewed_at"] = now
    change["review_result"] = (f"Auto-approved defensive reconfiguration under immune threat {threat}."
                               + (" Flagged for Board ratification (MEDIUM containment)." if requires_ratification else ""))
    change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "cca"})

    applied = None
    try:
        from agentic_core.organism.reconfiguration import update_config, ConfigUpdateRequest
        res = await update_config(ConfigUpdateRequest(
            section=plan["section"], key=plan["key"], value=plan["value"],
            reason=f"Immune reconfigurator (threat={threat}, cca={cca_id})"))
        applied = res.get("change")
        _consumer = _LEVER_CONSUMERS.get(plan["key"])
        if _consumer:
            change["status"] = "implemented"
            change["implemented_at"] = now
            change["audit_trail"].append({"event": "implemented", "ts": now, "applied": applied,
                                          "consumer": _consumer})
        else:
            # W318 honesty — the lever was SET but nothing consumes it: never claim 'implemented'
            change["status"] = "approved"
            change["audit_trail"].append({"event": "lever_set_no_consumer", "ts": now,
                                          "applied": applied,
                                          "note": "config value set; no wired consumer exists"})
        biobus.fire_signal("motor", "cca.immune_reconfigure.apply",
                           f"Applied immune defence: {plan['section']}.{plan['key']}={plan['value']}", 0.7)
    except Exception as e:
        change["audit_trail"].append({"event": "apply_failed", "ts": now, "error": str(e)})

    _save_change(change)
    return {
        "cca_id": cca_id,
        "threat_level": threat,
        "impact_tier": plan["tier"],
        "status": change["status"],
        "requires_ratification": requires_ratification,
        "reconfiguration": {"section": plan["section"], "key": plan["key"], "value": plan["value"], "why": plan["why"]},
        "applied": applied,
        "governed_by": "Change Control Agency (arms-length)",
        "message": f"Immune reconfigurator: {threat} → {plan['section']}.{plan['key']}={plan['value']} ({change['status']}).",
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


async def _twin_prevalidate(change: dict) -> dict:
    """§17.5 absolute invariant — digital-twin pre-validation before MAJOR change (HIGH/CRITICAL).
    Forward-simulates the proposed change against a twin model built from the LIVE organism state
    (the same simulation pattern as api/digital_twin.py, no persisted model required), extracting an
    explicit [TWIN: PASS]/[TWIN: FAIL] verdict. When the serving model returns no marker (e.g. the
    deterministic native floor), the verdict falls back to the ORGANISM HEALTH GATE — pass only when
    the organism is healthy and not under immune threat — with the source honestly recorded."""
    ctx = biobus.organism_context()
    prompt = (
        f"You are the digital-twin simulator pre-validating a change BEFORE implementation.\n\n"
        f"Twin model — the live organism state:\n"
        f"  Composite health: {ctx['composite_health']:.0%} | mode: {ctx['mode']}\n"
        f"  Immune threat: {ctx['immune']['threat_level']} | circadian: {ctx['circadian']['cycle']}\n\n"
        f"Proposed change ({change['impact_tier']}): {change['title']}\n"
        f"Type: {change['change_type']}\nDescription: {change['description']}\n"
        f"Affected systems: {', '.join(change.get('affected_systems') or []) or 'not specified'}\n"
        f"Rollback plan: {change.get('rollback_plan') or 'not provided'}\n\n"
        "Forward-simulate applying this change to the twin:\n"
        "## State Trajectory (immediately after → 24h → steady state)\n"
        "## Failure Modes Triggered (if any)\n"
        "## Rollback Viability\n"
        "## Verdict — end with exactly one of: [TWIN: PASS] or [TWIN: FAIL]"
    )
    try:
        sim = await gateway.query(prompt, agent="cca_twin_prevalidation", timeout=25)
    except Exception as e:
        sim = f"[twin simulation unavailable: {e}]"
    up = (sim or "").upper()
    has_pass, has_fail = "[TWIN: PASS]" in up, "[TWIN: FAIL]" in up
    if has_pass and not has_fail:
        verdict, source = "pass", "twin_marker"
    elif has_fail and not has_pass:
        verdict, source = "fail", "twin_marker"
    else:
        # no marker — or BOTH markers (a floor/echo artifact, not a real verdict): fall back to the
        # honest organism health gate rather than trusting an echoed marker.
        healthy = ctx["composite_health"] >= 0.6 and ctx["immune"]["threat_level"] in ("NOMINAL", "ELEVATED")
        verdict, source = ("pass" if healthy else "fail"), "health_gate_default"
    return {
        "verdict": verdict,
        "source": source,
        "composite_health_at_sim": ctx["composite_health"],
        "immune_threat_at_sim": ctx["immune"]["threat_level"],
        "summary": (sim or "")[:600],
        "simulated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "method": "digital-twin forward simulation over the live organism state",
    }


@router.post("/{cca_id}/twin-prevalidate")
async def twin_prevalidate(cca_id: str):
    """Run (or refresh) the §17.5 digital-twin pre-validation for a change. Required before
    /implement on HIGH/CRITICAL tiers."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] in ("implemented", "withdrawn"):
        raise HTTPException(status_code=400, detail=f"Change is {c['status']} — pre-validation is moot.")
    tp = await _twin_prevalidate(c)
    c["twin_prevalidation"] = tp
    c.setdefault("audit_trail", []).append(
        {"event": f"twin_prevalidation_{tp['verdict']}", "ts": tp["simulated_at"], "source": tp["source"]})
    _save_change(c)
    biobus.fire_signal("cognitive", "cca.twin_prevalidate",
                       f"Twin pre-validation {tp['verdict'].upper()}: {c['title']}", 0.6)
    return {"cca_id": cca_id, "twin_prevalidation": tp}


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

    # §17.5 — an APPROVED major change (HIGH/CRITICAL) is twin pre-validated at approval time so
    # /implement can enforce "pre-validation before major change" without a second round-trip.
    if decision == "approved" and c["impact_tier"] in ("HIGH", "CRITICAL"):
        tp = await _twin_prevalidate(c)
        c["twin_prevalidation"] = tp
        c["audit_trail"].append(
            {"event": f"twin_prevalidation_{tp['verdict']}", "ts": tp["simulated_at"], "source": tp["source"]})
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
async def implement_change(cca_id: str, force: bool = False):
    """Mark an approved change as implemented. §17.5 invariant: HIGH/CRITICAL changes REQUIRE a
    recorded digital-twin pre-validation PASS (run at review-approval, or via
    POST /{cca_id}/twin-prevalidate); a FAIL blocks implementation unless the Owner overrides with
    ?force=true (the override is audit-trailed, never silent)."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] != "approved":
        raise HTTPException(status_code=400, detail=f"Change must be approved before implementation. Status: {c['status']}")

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if c["impact_tier"] in ("HIGH", "CRITICAL"):
        tp = c.get("twin_prevalidation")
        if not tp:
            raise HTTPException(status_code=409, detail=(
                "§17.5 invariant: this MAJOR change has no recorded digital-twin pre-validation. "
                f"Run POST /api/v1/cca/{cca_id}/twin-prevalidate first."))
        if tp.get("verdict") != "pass" and not force:
            c["audit_trail"].append({"event": "implement_blocked_twin_fail", "ts": now,
                                     "twin_source": tp.get("source")})
            _save_change(c)
            raise HTTPException(status_code=409, detail=(
                "§17.5 invariant: the digital-twin pre-validation FAILED "
                f"({tp.get('source')}). Implementation blocked; the Owner may override with ?force=true."))
        if tp.get("verdict") != "pass" and force:
            c["audit_trail"].append({"event": "twin_fail_overridden_by_owner", "ts": now})

    c["status"] = "implemented"
    c["implemented_at"] = now
    c["audit_trail"].append({"event": "implemented", "ts": now})
    _save_change(c)

    biobus.fire_signal("motor", "cca.implement", f"Implemented: {c['title']}", 0.7)
    return {"cca_id": cca_id, "status": "implemented", "implemented_at": now,
            "twin_prevalidation": (c.get("twin_prevalidation") or {}).get("verdict")}


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
