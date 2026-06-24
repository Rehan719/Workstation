"""
Sovereign Evolution Office — autonomous, VSB-curated self-improvement.

Workstation is an IDBO owned and run by a Virtual Sovereign Business: an AI CEO
delegating to a specialised C-Suite, which tasks the Centres of Excellence (CoE)
and the Business Transformation Office (BTO). This module makes the organism's
own evolution processes — self-improvement, self-maintenance, self-development
(advancement) and self-correction — *autonomous and curated by that same org*.

One cycle:
    1. Introspect   — the organism observes itself (projects, immune, resources, routes)
    2. CEO triage   — the AI CEO frames prioritised improvement directives across the
                      four self-* functions and assigns each to a C-Suite owner
    3. C-Suite      — the assigned executives evaluate their directives (verdict + effort)
    4. CoE + BTO    — quality-gate the verdicts and sequence them into a Now/Next/Later
                      transformation roadmap, flagging items for the Change Control Agency

Builds on the existing introspection/proposal engine (api/v191/evolution.py) and the
VSB org cascade (api/swarm.py); it does not replace them.

  GET  /api/v1/sovereign-evolution/status   — office status, self-* functions, org tiers
  POST /api/v1/sovereign-evolution/cycle    — run one autonomous curated cycle
  GET  /api/v1/sovereign-evolution/roadmap  — the latest curated transformation roadmap
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/sovereign-evolution", tags=["sovereign-evolution"])

_ROADMAP = data_path("sovereign_evolution_roadmap.json")

_SELF_FUNCTIONS = {
    "improvement": "Self-improvement — optimise what already works (UX, performance, cost)",
    "maintenance": "Self-maintenance — health, self-healing, dependency and debt hygiene",
    "development": "Self-development — advancement, new capabilities, strategic growth",
    "correction":  "Self-correction — detect and fix errors, bugs, regressions, gaps",
}

# C-Suite owners the CEO can delegate to (mirrors api/swarm.py _AGENTS).
_CSUITE = {
    "CTO": "Chief Technology Officer — architecture, performance, resilience, AI/ML",
    "COO": "Chief Operating Officer — process, operational efficiency, scaling, hygiene",
    "CFO": "Chief Financial Officer — cost, unit economics, resource allocation",
    "CLO": "Chief Legal Officer — compliance, governance, risk mitigation",
}


def _load_roadmap() -> Dict[str, Any]:
    if _ROADMAP.exists():
        try:
            return json.loads(_ROADMAP.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_roadmap(data: Dict[str, Any]) -> None:
    _ROADMAP.parent.mkdir(parents=True, exist_ok=True)
    _ROADMAP.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _introspect() -> Dict[str, Any]:
    """The organism observes its own state (sensory layer of the cycle)."""
    state: Dict[str, Any] = {}
    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        stages: Dict[str, int] = {}
        for p in projects:
            stage = getattr(p, "stage", "unknown")
            stages[stage] = stages.get(stage, 0) + 1
        state["projects"] = {"total": len(projects), "by_stage": stages}
    except Exception:
        state["projects"] = {"total": 0}
    try:
        from agentic_core.organism.immune import immune
        state["immune"] = immune.status()
    except Exception:
        pass
    try:
        from agentic_core.organism.self_healing import self_healer
        state["self_healing"] = self_healer.status()
    except Exception:
        pass
    try:
        import psutil
        state["resources"] = {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
        }
    except Exception:
        pass
    return state


def _state_text(state: Dict[str, Any]) -> str:
    lines = []
    proj = state.get("projects", {})
    lines.append(f"Projects: {proj.get('total', 0)} total, by stage {proj.get('by_stage', {})}")
    if "immune" in state:
        imm = state["immune"]
        lines.append(f"Immune: health {imm.get('health')}, threat {imm.get('threat_level')}, "
                     f"errors_in_window {imm.get('errors_in_window')}")
    if "self_healing" in state:
        lines.append(f"Self-healing: {state['self_healing']}")
    if "resources" in state:
        r = state["resources"]
        lines.append(f"Resources: CPU {r.get('cpu_percent')}%, Memory {r.get('memory_percent')}%")
    return "\n".join(lines)


async def _q(prompt: str, agent: str) -> str:
    try:
        return await gateway.query(prompt, agent=agent)
    except Exception as e:
        return f"[{agent} unavailable: {e}]"


def _parse_directives(raw: str) -> List[Dict[str, str]]:
    directives = []
    for line in raw.splitlines():
        line = line.strip()
        if "|" not in line or line.upper().startswith("DIRECTIVE |"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # Expect: FUNCTION | OWNER | PRIORITY | TITLE | RATIONALE  (5 fields, optional leading label)
        if len(parts) >= 5 and parts[0].lower() in _SELF_FUNCTIONS:
            fn, owner, prio, title, rationale = parts[0], parts[1], parts[2], parts[3], " ".join(parts[4:])
        elif len(parts) >= 6 and parts[1].lower() in _SELF_FUNCTIONS:
            fn, owner, prio, title, rationale = parts[1], parts[2], parts[3], parts[4], " ".join(parts[5:])
        else:
            continue
        owner_u = owner.upper()
        directives.append({
            "id": f"dir-{uuid.uuid4().hex[:8]}",
            "function": fn.lower(),
            "owner": owner_u if owner_u in _CSUITE else "CTO",
            "priority": prio.upper() if prio.upper() in ("P1", "P2", "P3") else "P2",
            "title": title,
            "rationale": rationale,
        })
    return directives


class CycleRequest(BaseModel):
    focus: str = ""            # optional steer, e.g. "frontend latency"
    submit_to_change_control: bool = False


@router.get("/status")
async def office_status():
    roadmap = _load_roadmap()
    return {
        "office": "Sovereign Evolution Office",
        "owner": "IDBO Virtual Sovereign Business",
        "org_tiers": ["AI CEO", "C-Suite (CTO/COO/CFO/CLO)", "Centres of Excellence", "Business Transformation Office"],
        "self_functions": _SELF_FUNCTIONS,
        "governance": "Change Control Agency (/api/v1/cca)",
        "last_cycle": roadmap.get("created_at"),
        "roadmap_items": len(roadmap.get("directives", [])),
    }


@router.post("/cycle")
async def run_cycle(req: CycleRequest):
    """
    Run one autonomous self-improvement cycle, curated by the VSB org.
    Introspect → CEO triage → C-Suite verdicts → CoE/BTO roadmap.
    """
    cycle_id = uuid.uuid4().hex[:10]
    start = time.time()

    # 1. Introspection (sensory)
    state = _introspect()
    state_text = _state_text(state)

    # 2. CEO triage — frame prioritised directives across the four self-* functions
    ceo_prompt = (
        "You are the AI CEO of the Virtual Sovereign Business that owns and curates Workstation "
        "(an Intelligent Digital Biomimetic Organism). Observe the organism's self-reported state "
        "and issue prioritised improvement directives across the four self-* functions:\n"
        "  improvement (optimise what works), maintenance (health/self-healing/debt),\n"
        "  development (advancement/new capability), correction (errors/bugs/gaps).\n\n"
        f"Organism state:\n{state_text}\n"
        + (f"CEO focus this cycle: {req.focus}\n" if req.focus else "")
        + "\nOutput 4-6 directives, ONE PER LINE, exactly as:\n"
        "FUNCTION | OWNER | PRIORITY | TITLE | RATIONALE\n"
        "FUNCTION = improvement|maintenance|development|correction\n"
        "OWNER = CTO|COO|CFO|CLO (the C-Suite officer best suited)\n"
        "PRIORITY = P1|P2|P3\n"
        "TITLE = max 9 words. RATIONALE = what observation triggered it. No other text."
    )
    ceo_raw = await _q(ceo_prompt, "sovereign_evo_ceo")
    directives = _parse_directives(ceo_raw)
    if not directives:
        directives = [{
            "id": f"dir-{uuid.uuid4().hex[:8]}", "function": "maintenance", "owner": "COO",
            "priority": "P2", "title": "Routine organism health review",
            "rationale": "No parseable CEO directives; defaulting to a maintenance sweep.",
        }]

    # 3. C-Suite delegation — assigned executives evaluate their directives
    directive_text = "\n".join(
        f"- [{d['owner']} | {d['function']} | {d['priority']}] {d['title']} — {d['rationale']}"
        for d in directives
    )
    csuite_prompt = (
        "You are the C-Suite of the VSB. The CEO has delegated these improvement directives to "
        "their named owners. Each owner returns a crisp executive verdict.\n\n"
        f"{directive_text}\n\n"
        "Output ONE LINE PER directive, exactly as:\n"
        "TITLE | VERDICT | EFFORT | EXECUTION_NOTE\n"
        "VERDICT = proceed|defer|reject. EFFORT = S|M|L. EXECUTION_NOTE = one sentence. No other text."
    )
    csuite_raw = await _q(csuite_prompt, "sovereign_evo_csuite")

    # Merge verdicts back onto directives (best-effort title match)
    verdicts: Dict[str, Dict[str, str]] = {}
    for line in csuite_raw.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            verdicts[parts[0].lower()] = {"verdict": parts[1].lower(), "effort": parts[2].upper(), "note": parts[3]}
    for d in directives:
        v = verdicts.get(d["title"].lower())
        if not v:  # fuzzy: first verdict whose title is a prefix
            for k, vv in verdicts.items():
                if k[:12] and k[:12] in d["title"].lower():
                    v = vv
                    break
        d["verdict"] = (v or {}).get("verdict", "proceed")
        d["effort"] = (v or {}).get("effort", "M")
        d["execution_note"] = (v or {}).get("note", "")

    # 4. CoE quality gate + BTO sequencing into a transformation roadmap
    proceed = [d for d in directives if d.get("verdict") != "reject"]
    bto_input = "\n".join(
        f"- [{d['owner']} | {d['function']} | {d['priority']} | effort {d['effort']}] {d['title']}"
        for d in proceed
    )
    bto_prompt = (
        "You are the Centres of Excellence (quality/standards) and the Business Transformation "
        "Office (sequencing) of the VSB. Given the CEO directives and C-Suite verdicts below, "
        "quality-gate them and sequence them into a transformation roadmap.\n\n"
        f"{bto_input}\n\n"
        "## CoE Quality Gate (standards and risks to honour — 2-3 bullets)\n"
        "## Transformation Roadmap\n"
        "  - NOW (this cycle): items\n  - NEXT: items\n  - LATER: items\n"
        "## Governance (which items must go to the Change Control Agency, and why)"
    )
    bto_roadmap = await _q(bto_prompt, "sovereign_evo_bto")

    roadmap = {
        "cycle_id": cycle_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_ms": int((time.time() - start) * 1000),
        "introspection": state,
        "ceo_directives": directives,
        "bto_roadmap": bto_roadmap,
        "curated_by": ["AI CEO", "C-Suite", "CoE", "BTO"],
        "items_proceeding": len(proceed),
    }

    # 5. Optional governance hand-off to the Change Control Agency (real integration)
    submitted = []
    if req.submit_to_change_control:
        try:
            from agentic_core.api import change_control as cca
            for d in proceed:
                if d["priority"] == "P1" or d["function"] == "correction":
                    change = await cca.submit_change(cca.SubmitChangeRequest(
                        title=d["title"],
                        change_type="code_change" if d["function"] == "correction" else "config_minor",
                        description=f"[Sovereign Evolution · {d['function']} · owner {d['owner']}] {d['rationale']}",
                        rationale=d.get("execution_note", ""),
                        affected_systems=[d["owner"]],
                        submitted_by="sovereign-evolution-office",
                    ))
                    submitted.append({
                        "title": d["title"],
                        "cca_id": change.get("cca_id") if isinstance(change, dict) else None,
                        "impact_tier": change.get("impact_tier") if isinstance(change, dict) else None,
                        "status": change.get("status") if isinstance(change, dict) else None,
                    })
        except Exception as e:
            submitted.append({"error": str(e)})
    roadmap["change_control_submissions"] = submitted

    _save_roadmap(roadmap)

    # Biomimetic signal: the organism evolved itself
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "sovereign_evolution.cycle",
                           f"{len(directives)} directives curated", 0.8)
    except Exception:
        pass

    return roadmap


@router.get("/roadmap")
async def current_roadmap():
    roadmap = _load_roadmap()
    if not roadmap:
        return {"roadmap": None, "message": "No cycle has run yet. POST /cycle to generate one."}
    return roadmap
