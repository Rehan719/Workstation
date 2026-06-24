"""
Resource Fabric — the unified, reconfigurable resource catalogue.

One place to discover, select, reconfigure, and COMBINE every resource of the
Workstation IDBO — across the Synthesis Lab, Design, Development, Delivery,
Build-to-Order, and the Forge. It federates (does not duplicate) the existing
process-intelligence engines, digital resources (reactors/factories/incubators/
labs/twins/generators/simulators), organism biomimetic systems, and the
enterprise/org layer into a single fabric. Selections can be composed into named,
reusable, re-runnable configurations.

  GET  /api/v1/resources                       — list/filter the resource fabric
  GET  /api/v1/resources/{resource_id}         — one resource + its reconfig schema
  POST /api/v1/resources/compose               — combine selected resources into a config
  GET  /api/v1/resources/compositions          — list saved compositions
  GET  /api/v1/resources/compositions/{cid}    — get one composition
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/resources", tags=["resource-fabric"])

_STORE = data_path("resource_compositions.json")

# Usage areas a resource can be selected into.
# synthesis | design | development | delivery | build_to_order | forge | commercialisation | governance | evolution


def _R(rid, name, cls, rtype, desc, caps, params, endpoint, usable_in,
       reusable=True, rerunnable=True, biomimetic=False, methods=("POST",)) -> Dict[str, Any]:
    return {
        "id": rid, "name": name, "resource_class": cls, "type": rtype, "description": desc,
        "capabilities": caps, "reconfigurable_params": params, "endpoint": endpoint,
        "methods": list(methods), "reusable": reusable, "rerunnable": rerunnable,
        "biomimetic": biomimetic, "usable_in": usable_in,
    }


# ── The unified resource registry (federates real, live resources) ────────────
_REGISTRY: List[Dict[str, Any]] = [
    # Process-Intelligence cognition engines
    _R("bdp", "Business Development Process", "process_intelligence", "engine",
       "8-stage business intelligence: market → value prop → model → GTM → financials → risk.",
       ["market analysis", "business model", "go-to-market", "financial model", "risk"],
       {"challenge": "str", "domain": "str"}, "/api/v1/intelligence/bdp",
       ["synthesis", "design", "commercialisation", "build_to_order", "forge"]),
    _R("spi", "Scientific Process Intelligence", "process_intelligence", "engine",
       "8-stage research intelligence: problem → literature → hypothesis → methodology → validation.",
       ["hypothesis generation", "literature synthesis", "methodology", "validation"],
       {"challenge": "str", "domain": "str"}, "/api/v1/intelligence/spi",
       ["synthesis", "design", "development", "forge"]),
    _R("apie", "Scholarship & Authorship Intelligence", "process_intelligence", "engine",
       "9-stage authorship: source discovery → argument → draft → evidence → peer review → publication.",
       ["research reports", "papers", "reviews", "citations", "integrity audit"],
       {"topic": "str", "genre": "str", "citation_style": "str", "word_count": "str"},
       "/api/v1/intelligence/authorship", ["synthesis", "design", "development", "forge"]),
    _R("ddpie", "Design & Development Intelligence", "process_intelligence", "engine",
       "9-stage engineering: requirements → architecture → API → security → blueprint → tests → devops.",
       ["architecture", "api contract", "security", "test strategy", "devops"],
       {"system": "str", "tech_stack": "str", "scale": "str", "deployment_target": "str"},
       "/api/v1/intelligence/design-dev", ["design", "development", "delivery", "forge", "build_to_order"]),
    _R("cognitive_cascade", "Nine Cognitive Engines + MJM", "process_intelligence", "engine",
       "6 cognitive engines (Inkashaf/Samajh/Soch/Aqal/Hoshiyari/Iman) + MJM meta-judgement.",
       ["pattern discovery", "comprehension", "reasoning", "anomaly detection", "values alignment"],
       {"problem": "str", "domain": "str"}, "/api/v1/intelligence/solve",
       ["synthesis", "design", "development", "delivery", "governance"], biomimetic=True),
    _R("nexus", "Synthesis Nexus", "process_intelligence", "orchestrator",
       "4-layer autonomous chain: cognitive cascade → MJM → auto-selected engine → apex synthesis.",
       ["auto engine routing", "cross-engine synthesis", "synergistic chaining"],
       {"challenge": "str", "domain": "str", "activity": "str"}, "/api/v1/intelligence/nexus",
       ["synthesis", "design", "development", "delivery"], biomimetic=True),
    _R("genesis", "Genesis Sovereign Journey", "process_intelligence", "orchestrator",
       "End-to-end Concept → Design → Commercialisation, ending in a living VSB blueprint.",
       ["conceptualisation", "design", "commercialisation", "vsb blueprint"],
       {"problem": "str", "domain": "str", "realm": "str"}, "/api/v1/genesis/journey",
       ["synthesis", "design", "development", "delivery", "commercialisation"], biomimetic=True),

    # Digital resources (reconfigurable / rerunnable / reusable)
    _R("synthesis_studio", "Synthesis Lab", "digital_resource", "laboratory",
       "Autonomously generates varied content types (reports, decks, sites, apps, models) from instructions + data.",
       ["multi-format content generation", "9-stage BTO cascade", "vsb spawn"],
       {"brief": "str", "output_types": "list", "domain": "str"}, "/api/v1/studio/synthesise",
       ["synthesis", "design", "development", "forge"]),
    _R("reactor", "Domain Reactor", "digital_resource", "reactor",
       "Streams a domain AI processing simulation (ingestion → analysis → synthesis → validation).",
       ["domain simulation", "data flow modelling", "artefact output"],
       {"domain": "str"}, "/api/v1/reactor/run", ["development", "forge", "synthesis"]),
    _R("factory", "Production Factory", "digital_resource", "factory",
       "Generates production-grade artefacts (business model, spec, marketing plan, pitch, report).",
       ["artefact production", "production-grade output"],
       {"product_type": "str", "brief": "str"}, "/api/v1/factory/produce",
       ["delivery", "build_to_order", "forge", "commercialisation"]),
    _R("incubator", "Evolution Incubator", "digital_resource", "incubator",
       "Prompt tournament: generates N variations, scores and ranks them (iterative development).",
       ["variation generation", "scoring", "ranking", "iterative evolution"],
       {"brief": "str", "variations": "int"}, "/api/v1/incubator/evolve",
       ["development", "forge", "evolution"]),
    _R("digital_twin", "Digital Twin & Simulator", "digital_resource", "simulator",
       "Generates AI models and runs scenario simulations / optimisation (generators + simulators).",
       ["model generation", "scenario simulation", "optimisation"],
       {"system": "str", "scenario": "str"}, "/api/v1/twin", ["design", "development", "delivery", "forge"]),

    # Organism biomimetic systems
    _R("gaas_v5", "Constitutional Gate (gaas.v5)", "organism_system", "governance_engine",
       "v16-Omega constitutional interceptor + self-tuning breaker + SHA3-512 UEG audit log.",
       ["pre/post gate", "self-tuning circuit breaker", "tamper-evident audit"],
       {"action_type": "str", "payload": "dict"}, "/api/v1/gaas/intercept",
       ["governance", "delivery", "evolution"], biomimetic=True),
    _R("sovereign_evolution", "Sovereign Evolution Office", "organism_system", "evolution_engine",
       "Autonomous self-improvement curated by the VSB org (CEO→C-Suite→CoE→BTO), routes to Change Control.",
       ["introspection", "org-curated proposals", "transformation roadmap", "governance hand-off"],
       {"focus": "str", "submit_to_change_control": "bool"}, "/api/v1/sovereign-evolution/cycle",
       ["evolution", "governance"], biomimetic=True),
    _R("nervous_system", "Nervous System", "organism_system", "biomimetic",
       "Signal routing, reflex arcs, arousal state — the organism's live event field.",
       ["signal routing", "reflex arcs", "arousal state"], {},
       "/api/v1/organism/nervous/status", ["governance", "evolution"], biomimetic=True, methods=("GET",)),
    _R("genome", "Genome Registry", "organism_system", "biomimetic",
       "3-layer epigenetic memory encoding VSB DNA and acquired traits.",
       ["DNA encoding", "epigenetic memory", "trait inheritance"], {"trait": "str"},
       "/api/v1/genome", ["design", "delivery", "evolution"], biomimetic=True),

    # Enterprise / org layer
    _R("vsb_spawn", "VSB Spawn Pipeline", "enterprise_org", "spawner",
       "Spawns a living VSB IDBO entity via cascade → MJM → GaaS → genome → swarm (SSE).",
       ["vsb instantiation", "genome encoding", "swarm config"],
       {"challenge": "str", "domain": "str", "scope": "str"}, "/api/v1/vsb/spawn",
       ["delivery", "commercialisation", "build_to_order"]),
    _R("genesis_establish", "Establish Enterprise IDBO", "enterprise_org", "spawner",
       "Turns a Genesis blueprint into a real, persisted, governed, operational VSB IDBO entity.",
       ["living entity generation", "blueprint → enterprise"],
       {"problem": "str", "domain": "str", "concept": "str", "commercialisation": "str"},
       "/api/v1/genesis/establish", ["delivery", "commercialisation"]),
    _R("vsb_org_swarm", "AI CEO → C-Suite → CoE", "enterprise_org", "org_swarm",
       "The VSB organisational cascade: AI CEO directs, C-Suite delegates, CoE delivers.",
       ["ceo directive", "c-suite delegation", "coe synthesis"],
       {"mission": "str", "domain": "str"}, "/api/v1/swarm/cascade",
       ["delivery", "build_to_order", "commercialisation", "governance"]),
    _R("change_control", "Change Control Agency", "enterprise_org", "governance",
       "Arms-length governance: LOW auto-approve, MEDIUM/HIGH AI review, CRITICAL blocked.",
       ["change submission", "tiered review", "governed implementation"],
       {"title": "str", "change_type": "str", "description": "str"}, "/api/v1/cca/submit",
       ["governance", "evolution", "delivery"]),
    _R("capital_fund", "Sovereign Capital Fund", "enterprise_org", "treasury",
       "Virtual capital allocation + marketplace for the VSB ecosystem.",
       ["capital allocation", "portfolio", "marketplace"], {"amount": "float", "recipient": "str"},
       "/api/v1/fund/allocate", ["delivery", "commercialisation"]),
    _R("compliance", "Unified Compliance Engine", "process_intelligence", "engine",
       "Sharia/Halal · UK Legal (London) · Regulatory · EHS · Ethical · Constitutional — one federated check.",
       ["halal/sharia", "uk legal", "regulatory", "ehs", "ethical", "constitutional"],
       {"subject": "str", "domain": "str", "jurisdiction": "str"}, "/api/v1/compliance/check",
       ["synthesis", "design", "development", "delivery", "commercialisation", "governance", "forge", "build_to_order"]),

    # Native AI fabric — Workstation's OWN AI resources (in-house-first, no external dependency)
    _R("native_orchestrator", "Native AI Orchestrator", "ai_native", "orchestrator",
       "In-house-first completion over OWNED resources: native structured-reasoning floor · local "
       "Ollama model when present · external accelerants opt-in only. Every result reports served_by.",
       ["in-house completion", "graceful degradation", "provenance (served_by)"],
       {"prompt": "str", "agent": "str", "prefer_external": "bool"}, "/api/v1/native-ai/complete",
       ["synthesis", "design", "development", "delivery", "governance", "forge"]),
    _R("native_swarm", "Native AI Swarm", "ai_native", "swarm",
       "A bespoke, RECONFIGURABLE agent-cascade run on Workstation's OWN resources — define stages "
       "(role + instruction); each stage completes in-house-first and feeds the next. Define once, "
       "reuse and re-run as a living resource (full user design control).",
       ["bespoke cascade", "reconfigurable stages", "in-house provenance", "reusable", "rerunnable"],
       {"agent": "str", "context": "str", "stages": "list[{role,instruction}]"},
       "/api/v1/resources/swarm/run",
       ["synthesis", "design", "development", "delivery", "governance", "forge", "build_to_order"]),

    # Workstation's OWN omnimedia output factory — surfaced into the fabric so the swarm/delivery
    # pipeline can render deliverables across formats (agentic_core.omnimedia).
    _R("omnimedia", "Omnimedia Output Factory", "output_media", "generator",
       "Workstation's own multimedia output factory — renders deliverables across formats "
       "(pptx/pdf/docx/xlsx/html/mp4/mp3/png/svg): infographics, video, audio, digital-twin, "
       "documents, dashboards. Markdown export is live; richer formats via the omnimedia generators.",
       ["multi-format output", "infographic", "video", "audio", "document", "dashboard"],
       {"deliverable_id": "str", "format": "str"}, "/api/v1/deliverables/output-formats",
       ["synthesis", "delivery", "commercialisation", "forge"], methods=("GET",)),

    # Workstation's OWN multi-instance federation mesh — surfaced into the fabric so VSBs can
    # federate (peer discovery, reputation-weighted BFT consensus, health) (agentic_core.mesh).
    _R("federation_mesh", "Federation Mesh", "federation", "mesh",
       "Workstation's own multi-instance federation mesh: peer discovery, reputation-weighted BFT "
       "consensus (2/3+1), health/heartbeat, and treaty negotiation — for federating VSB IDBO "
       "instances. Single-node deployments report simulated peers (honestly flagged).",
       ["peer discovery", "BFT consensus", "reputation/health", "treaty negotiation"],
       {}, "/api/v1/mesh/status", ["governance", "delivery", "evolution"],
       biomimetic=True, methods=("GET",)),

    # Workstation's OWN mega-project synthesis — redone honestly on the native fabric (the original
    # returned fabricated figures); surfaced so the swarm/delivery can produce investor-grade
    # deliverables for large concepts (agentic_core.mega_project).
    _R("mega_project", "Mega-Project Synthesiser", "process_intelligence", "synthesiser",
       "Investor-grade deliverables for a large-scale concept (business plan · market · feasibility · "
       "capital plan · roadmap · risks), produced on the native fabric — honest (no invented figures; "
       "valuations/ROI framed as to-be-modelled).",
       ["business plan", "feasibility", "capital plan", "roadmap", "risk"],
       {"concept": "str", "domain": "str"}, "/api/v1/mega-project/synthesise",
       ["synthesis", "commercialisation", "delivery", "forge"]),

    # Workstation's OWN adaptive resource optimiser — surfaced so the swarm/delivery can verify,
    # schedule, assemble and allocate resources (agentic_core.optimizer). Single-node simulated capacity.
    _R("resource_optimizer", "Adaptive Resource Optimiser", "digital_resource", "optimizer",
       "Verify a resource request (RAL) → cost-aware schedule → assemble a dynamic pool → "
       "tiered-fair allocate. Real engine logic; capacity is a simulated single-node baseline.",
       ["resource verification", "scheduling", "dynamic assembly", "tiered allocation"],
       {"domain": "str", "requirements": "dict", "tier": "str"}, "/api/v1/optimizer/allocate",
       ["delivery", "forge", "governance", "evolution"]),

    # Workstation's OWN collective-intelligence truth consensus — surfaced so the swarm/mesh can
    # agree on ground truth (agentic_core.collective). Operates only on submitted claims.
    _R("truth_consensus", "Collective Truth Consensus", "process_intelligence", "consensus",
       "Reputation-weighted confidence aggregation over a set of claims — accepts a claim when the "
       "weighted consensus clears the threshold. For cross-swarm / cross-VSB agreement on ground truth.",
       ["consensus", "reputation weighting", "calibration"],
       {"claims": "list[{claim,confidence,reputation}]", "threshold": "float"},
       "/api/v1/collective/consensus", ["governance", "evolution", "delivery"], biomimetic=True),
]

_BY_ID = {r["id"]: r for r in _REGISTRY}


def _load_compositions() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_compositions(rows: List[Dict[str, Any]]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(rows, indent=2), encoding="utf-8")


@router.get("")
async def list_resources(resource_class: Optional[str] = None, usable_in: Optional[str] = None):
    """List the resource fabric, optionally filtered by class and/or usage area."""
    items = _REGISTRY
    if resource_class:
        items = [r for r in items if r["resource_class"] == resource_class]
    if usable_in:
        items = [r for r in items if usable_in in r["usable_in"]]
    classes: Dict[str, int] = {}
    for r in _REGISTRY:
        classes[r["resource_class"]] = classes.get(r["resource_class"], 0) + 1
    return {
        "resources": items,
        "total": len(items),
        "classes": classes,
        "usage_areas": ["synthesis", "design", "development", "delivery",
                        "build_to_order", "forge", "commercialisation", "governance", "evolution"],
    }


@router.get("/compositions")
async def list_compositions():
    return {"compositions": _load_compositions()}


@router.get("/compositions/{cid}")
async def get_composition(cid: str):
    for c in _load_compositions():
        if c["id"] == cid:
            return c
    raise HTTPException(status_code=404, detail=f"Composition {cid} not found.")


# ── Native swarm cascades — first-class reconfigurable resources (user design control) ──
# A swarm cascade is an ordered list of {role, instruction} stages run in-house-first on
# Workstation's OWN resources. Users DEFINE a bespoke cascade (reconfigure the stages), it is
# SAVED as a reusable resource, and can be RE-RUN on demand — the result reports served_by per
# stage so it is provably running on owned resources. (Declared before /{resource_id} so the
# static /swarm* paths win over the dynamic resource lookup.)
_SWARM_STORE = data_path("swarm_cascades.json")


def _load_swarms() -> List[Dict[str, Any]]:
    if _SWARM_STORE.exists():
        try:
            return json.loads(_SWARM_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_swarms(rows: List[Dict[str, Any]]) -> None:
    _SWARM_STORE.parent.mkdir(parents=True, exist_ok=True)
    _SWARM_STORE.write_text(json.dumps(rows[-200:], indent=2), encoding="utf-8")


def register_swarm(name: str, stages: List[Dict[str, str]], context: str = "",
                   usage_area: str = "synthesis", vsb_id: str | None = None,
                   org: List[str] | None = None) -> Dict[str, Any]:
    """Persist a bespoke native swarm cascade as a reusable, re-runnable fabric resource and
    return it. Shared by the /swarm/define endpoint and by Genesis (which gives every established
    VSB its OWN cascade) — one path, so per-VSB swarms run through the same owned-resource runner."""
    cascade = {
        "id": f"swarm-{uuid.uuid4().hex[:8]}",
        "name": name,
        "kind": "ai_native_swarm",
        "stages": [{"role": s.get("role", ""), "instruction": s.get("instruction", "")} for s in stages],
        "context": context,
        "usage_area": usage_area,
        "posture": "in-house-first",
        "reusable": True,
        "rerunnable": True,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if vsb_id:
        cascade["vsb_id"] = vsb_id
    if org:
        cascade["org"] = org
    rows = _load_swarms()
    rows.append(cascade)
    _save_swarms(rows)
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "resource_fabric.swarm.register",
                           f"{name}: {len(cascade['stages'])} stages", 0.5)
    except Exception:
        pass
    return cascade


class SwarmStageSpec(BaseModel):
    role: str
    instruction: str


class DefineSwarmRequest(BaseModel):
    name: str
    stages: List[SwarmStageSpec]
    context: str = ""
    usage_area: str = "synthesis"


class RunSwarmRequest(BaseModel):
    swarm_id: Optional[str] = None        # run a SAVED cascade …
    stages: List[SwarmStageSpec] = []     # … or an ad-hoc one
    context: str = ""
    agent: str = "fabric-swarm"
    prefer_external: bool = False
    timeout: float = 12.0


@router.post("/swarm/define")
async def define_swarm(req: DefineSwarmRequest):
    """Define + save a bespoke, reusable, re-runnable native swarm cascade (user design control)."""
    return register_swarm(req.name, [s.model_dump() for s in req.stages],
                          context=req.context, usage_area=req.usage_area)


@router.get("/swarm")
async def list_swarms(vsb_id: Optional[str] = None):
    rows = _load_swarms()
    if vsb_id:
        rows = [c for c in rows if c.get("vsb_id") == vsb_id]
    return {"cascades": rows, "total": len(rows)}


@router.get("/swarm/{sid}")
async def get_swarm(sid: str):
    for c in _load_swarms():
        if c["id"] == sid:
            return c
    raise HTTPException(status_code=404, detail=f"Swarm cascade {sid} not found.")


@router.post("/swarm/run")
async def run_swarm(req: RunSwarmRequest):
    """Run a swarm cascade (saved via swarm_id, or ad-hoc stages) on Workstation's OWN resources.
    Returns the per-stage trace with served_by + whether any external accelerant was used."""
    stages = [s.model_dump() for s in req.stages]
    context = req.context
    name = "ad-hoc"
    if req.swarm_id:
        saved = next((c for c in _load_swarms() if c["id"] == req.swarm_id), None)
        if not saved:
            raise HTTPException(status_code=404, detail=f"Swarm cascade {req.swarm_id} not found.")
        stages = saved["stages"]
        context = req.context or saved.get("context", "")
        name = saved["name"]
    if not stages:
        raise HTTPException(status_code=400, detail="Provide stages or a saved swarm_id to run.")
    from agentic_core.ai.native import orchestrator
    _t0 = time.time()
    res = await orchestrator.swarm(req.agent, stages, context=context,
                                   prefer_external=req.prefer_external, timeout=req.timeout)
    # operational-excellence learning loop: record the real outcome of this run
    try:
        from agentic_core.api.operational_excellence import record_outcome
        served = res["trace"][0]["served_by"] if res.get("trace") else "native"
        record_outcome("swarm_run", f"swarm:{name}", served_by=served,
                       is_external=bool(res.get("any_external")),
                       duration_ms=int((time.time() - _t0) * 1000),
                       success=bool(res.get("trace")), ref=req.swarm_id)
    except Exception:
        pass
    return {"name": name, "swarm_id": req.swarm_id, "posture": "in-house-first", **res}


@router.get("/{resource_id}")
async def get_resource(resource_id: str):
    r = _BY_ID.get(resource_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found.")
    return r


class ComposeRequest(BaseModel):
    name: str
    resource_ids: List[str]
    usage_area: str = "synthesis"
    config: Dict[str, Dict[str, Any]] = {}   # per-resource param overrides {id: {param: value}}


@router.post("/compose")
async def compose(req: ComposeRequest):
    """Combine selected resources into a named, reusable, re-runnable configuration."""
    unknown = [rid for rid in req.resource_ids if rid not in _BY_ID]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown resource ids: {unknown}")

    resolved = []
    for rid in req.resource_ids:
        base = _BY_ID[rid]
        resolved.append({
            "id": rid,
            "name": base["name"],
            "resource_class": base["resource_class"],
            "endpoint": base["endpoint"],
            "config": {**base["reconfigurable_params"], **req.config.get(rid, {})},
        })

    composition = {
        "id": f"comp-{uuid.uuid4().hex[:8]}",
        "name": req.name,
        "usage_area": req.usage_area,
        "resources": resolved,
        "reusable": True,
        "rerunnable": True,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    rows = _load_compositions()
    rows.append(composition)
    _save_compositions(rows)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "resource_fabric.compose",
                           f"{req.name}: {len(resolved)} resources", 0.6)
    except Exception:
        pass

    return composition
