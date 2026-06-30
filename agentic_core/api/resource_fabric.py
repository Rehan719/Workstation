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

from agentic_core.vbs.quality import assure_delivery

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
    _R("mjm", "MJM Meta-Judgement", "process_intelligence", "engine",
       "The MJM Orchestrator (Mushahida → Jaiza → Muaina) — the meta-judgement system operating ABOVE the "
       "cognitive engines: witnessed observation → deep assessment → verified action directives. Reusable "
       "standalone: judges over supplied context, or auto-primes the cognitive cascade first.",
       ["meta-judgement", "witnessed observation", "deep assessment", "verified action directives"],
       {"problem": "str", "domain": "str", "prime": "bool (auto cognitive prime)", "engines": "list (priming engines)"},
       "/api/v1/intelligence/mjm", ["synthesis", "governance", "delivery", "design", "development"], biomimetic=True),
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
    _R("reactor", "Reactor · Incubate + Experiment + Studio", "digital_resource", "reactor",
       "The §7 composite Reactor (vision definition): Incubator (parameterised Temperature/Mutation/"
       "Iteration evolution) + Experimentation (what-if scenarios) + Studio (2D analytics & insight over "
       "the REAL evolution fitness) — orchestrated into one run on the native swarm.",
       ["evolution (temperature/mutation/iteration)", "what-if scenarios", "visual analytics & insight"],
       {"subject": "str", "variants": "int 2-5", "temperature": "float 0-1 (diversity)",
        "mutation": "float 0-1", "iterations": "int 1-4", "scenarios": "list (one what-if per line)"},
       "/api/v1/reactor/composite", ["synthesis", "design", "development", "forge", "evolution"]),
    _R("factory", "Production Factory", "digital_resource", "factory",
       "Generates production-grade artefacts (business model, spec, marketing plan, pitch, report).",
       ["artefact production", "production-grade output"],
       {"product_type": "str", "brief": "str"}, "/api/v1/factory/produce",
       ["delivery", "build_to_order", "forge", "commercialisation"]),
    _R("incubator", "Evolution Incubator", "digital_resource", "incubator",
       "The §7 Reactor's generation/evolution loop: each generation produces N variations at a diversity "
       "Temperature, scores + ranks them, and across Iterations the winner is Mutation-evolved into the "
       "next generation — a parameterised Temperature/Mutation/Iteration loop (user design control).",
       ["variation generation", "scoring", "ranking", "parameterised evolution (temperature/mutation/iteration)"],
       {"base_prompt": "str", "variants": "int (2-5)", "temperature": "float 0-1 (diversity)",
        "mutation": "float 0-1 (per-generation change)", "iterations": "int 1-4 (generations)"},
       "/api/v1/incubator/evolve", ["development", "forge", "evolution"]),
    _R("petri_dish", "Petri Dish", "digital_resource", "petri_dish",
       "The §7 smallest CONTAINED experiment: culture one specimen (idea/hypothesis) in isolation under a "
       "chosen medium over a few passages on the native fabric, then assess viability — QMS-gated. Distinct "
       "from the Reactor (multi-scenario what-ifs) and the Incubator (evolutionary tournament).",
       ["contained culture", "isolation experiment", "viability assessment", "idea incubation"],
       {"specimen": "str", "medium": "str (conditions)", "iterations": "int 1-3 (passages)", "domain": "str"},
       "/api/v1/petri/culture", ["synthesis", "design", "development", "forge", "evolution"]),
    _R("experimentation", "Reactor · Experimentation", "digital_resource", "experimentation",
       "The §7 Reactor's what-if engine: projects + compares the outcomes of user-defined scenarios, "
       "ranked against fitness criteria — on the native fabric (in-house), QMS-gated.",
       ["what-if scenarios", "outcome projection", "scenario comparison", "ranking"],
       {"subject": "str", "scenarios": "list (one what-if per line)", "domain": "str"},
       "/api/v1/reactor/experiment", ["synthesis", "design", "development", "forge", "evolution"]),
    _R("studio", "Reactor · Studio", "digital_resource", "studio",
       "The §7 Reactor's Studio: 2D/3D visual analytics & insight over a REAL data series — computes "
       "deterministic stats (count/total/mean/min/max/range) and an in-house insight narrative; renders "
       "bar/line/scatter charts (scatter carries an optional z magnitude). Visualises real data, never faked.",
       ["2d charts", "scatter / z-magnitude", "computed analytics", "insight narrative"],
       {"title": "str", "series": "list of {label,value[,z]}", "chart_type": "bar|line|scatter"},
       "/api/v1/reactor/studio", ["synthesis", "design", "development", "forge", "evolution", "delivery"]),
    _R("generator", "Artefact Generator", "digital_resource", "generator",
       "Generates ONE concrete, targeted artefact (code · schema · config · content · model spec) in a "
       "chosen format on the native swarm — distinct from the Factory (multi-section document production) "
       "and the Laboratory (concept→commercialisation cascade). Reconfigurable / rerunnable / reusable.",
       ["code generation", "schema generation", "config/content generation", "format control"],
       {"artefact_type": "str (code|schema|config|content|model_spec)", "spec": "str",
        "format": "str (python|json|yaml|markdown|…)"},
       "/api/v1/generator/produce", ["development", "forge", "delivery", "build_to_order"]),
    _R("digital_twin", "Digital Twin & Simulator", "digital_resource", "simulator",
       "Forward-simulates a system under a scenario on the native swarm (state trajectory · emergent "
       "behaviour · stress points · setpoints) — the §7 Simulator facility.",
       ["scenario simulation", "forward modelling", "stress/failure analysis", "setpoint optimisation"],
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
       "Signal routing, reflex arcs, arousal state — the organism's live event field. When composed, "
       "fires a real cognitive signal for the objective + reads the live arousal.",
       ["signal routing", "reflex arcs", "arousal state"], {},
       "/api/v1/organism/nervous/status", ["governance", "evolution"], biomimetic=True),
    _R("immune", "Immune System", "organism_system", "biomimetic",
       "Error-rate ring buffer → live health score + threat level — the organism's defence. When "
       "composed, contributes the genuine current immune reading.",
       ["health score", "threat level", "anomaly detection"], {},
       "/api/v1/organism/immune/status", ["governance", "evolution", "delivery"], biomimetic=True, methods=("GET",)),
    _R("self_healing", "Self-Healing Reflex", "organism_system", "biomimetic",
       "Per-provider circuit breakers (CLOSED/OPEN/HALF_OPEN) + healing log — automatic recovery. When "
       "composed, contributes the live breaker/health reading.",
       ["circuit breakers", "auto-recovery", "healing log"], {},
       "/api/v1/organism/self-healing/status", ["governance", "evolution", "delivery"], biomimetic=True, methods=("GET",)),
    _R("metabolic", "Metabolic / ATP", "organism_system", "biomimetic",
       "The ATP energy model + composite-health mode (FULL_POWER/NOMINAL/DEGRADED/EMERGENCY) — the "
       "organism's metabolism. When composed, reads the live ATP + operating mode.",
       ["atp energy model", "composite health", "operating mode"],
       {"metabolic_load": "float 0-1"}, "/api/v1/organism/status", ["governance", "evolution"], biomimetic=True, methods=("GET",)),
    _R("circadian", "Circadian Heartbeat", "organism_system", "biomimetic",
       "Time-of-day cycle (ACTIVE_FOCUS/ACTIVE_REST/REST/MAINTENANCE) modulating cognition + metabolism. "
       "When composed, reads the live circadian phase.",
       ["circadian cycle", "peak-focus window", "rhythm modulation"], {},
       "/api/v1/organism/status", ["governance", "evolution"], biomimetic=True, methods=("GET",)),
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
       "The §5 living-organisation cascade: the AI CEO directs a USER-DESIGNED C-Suite, each officer drives "
       "its Centre of Excellence, and the Business Transformation Office build-to-orders the delivery. "
       "Reconfigure the org structure — which C-Suite officers — via csuite_roles (design control).",
       ["ceo directive", "reconfigurable c-suite", "coe synthesis", "build-to-order"],
       {"mission": "str", "domain": "str",
        "csuite_roles": "e.g. CSO,CFO,CTO,COO,CLO,Forecasting,Policy", "coe_specialisms": "e.g. Pricing,Compliance"},
       "/api/v1/swarm/cascade",
       ["delivery", "build_to_order", "commercialisation", "governance"]),
    _R("change_control", "Change Control Agency", "enterprise_org", "governance",
       "Arms-length governance: LOW auto-approve, MEDIUM/HIGH AI review, CRITICAL blocked.",
       ["change submission", "tiered review", "governed implementation"],
       {"title": "str", "change_type": "str", "description": "str"}, "/api/v1/cca/submit",
       ["governance", "evolution", "delivery"]),
    _R("capital_fund", "Sovereign Capital Fund", "enterprise_org", "treasury",
       "Virtual capital allocation + marketplace for the VSB ecosystem (virtual WST only — real-money "
       "rails gated). When composed, reads the live treasury (available/allocated/utilisation/health).",
       ["capital allocation", "portfolio", "marketplace"], {"amount": "float", "recipient": "str"},
       "/api/v1/fund/allocate", ["delivery", "commercialisation"]),
    _R("products_catalogue", "Products Catalogue", "enterprise_org", "catalogue",
       "The real product catalogue (the owned SDK/product set). When composed, returns the genuine "
       "catalogue ranked by relevance to the objective (deterministic token match — never fabricated).",
       ["product catalogue", "relevance match", "tiers"], {}, "/api/v1/catalog/products",
       ["commercialisation", "delivery", "build_to_order"], methods=("GET",)),
    _R("build_to_order", "Build-to-Order", "enterprise_org", "bto",
       "Bespoke Build-to-Order: assemble a real blueprint integrating chosen catalogue products + "
       "platform components (entity/organism/VSB/C-Suite). When composed, builds the genuine blueprint.",
       ["bespoke assembly", "product integration", "blueprint"],
       {"entity_name": "str", "product_resources": "list (catalog slugs)", "components": "list (vsb,csuite,…)"},
       "/api/v1/bto/configure", ["build_to_order", "delivery", "commercialisation"]),
    _R("compliance", "Unified Compliance Engine", "process_intelligence", "engine",
       "Sharia/Halal · UK Legal (London) · Regulatory · EHS · Ethical · Constitutional — one federated check.",
       ["halal/sharia", "uk legal", "regulatory", "ehs", "ethical", "constitutional"],
       {"subject": "str", "domain": "str", "jurisdiction": "str"}, "/api/v1/compliance/check",
       ["synthesis", "design", "development", "delivery", "commercialisation", "governance", "forge", "build_to_order"]),

    # Native AI fabric — Workstation's OWN AI resources (in-house-first, no external dependency)
    _R("native_orchestrator", "Native AI Orchestrator", "ai_native", "orchestrator",
       "In-house-first completion over OWNED resources: native structured-reasoning floor · local "
       "Ollama model when present · external accelerants opt-in only. Every result reports served_by.",
       ["in-house completion", "graceful degradation", "provenance (served_by)", "model preference (auto/native/local)"],
       {"prompt": "str", "agent": "str", "prefer_external": "bool", "model": "str (auto|native|local)"},
       "/api/v1/native-ai/complete",
       ["synthesis", "design", "development", "delivery", "governance", "forge"]),
    _R("native_ensemble", "Native AI Model Ensemble", "ai_native", "ensemble",
       "Run a prompt across MULTIPLE owned models in parallel, then synthesise a consensus — owned "
       "orchestration as a composable resource. Defaults to all discovered local models + the native floor; "
       "every member reports which owned resource served it.",
       ["multi-model ensemble", "parallel", "consensus synthesis", "owned-model provenance"],
       {"prompt": "str", "models": "list (tier ids; empty = all owned)", "synthesize": "bool"},
       "/api/v1/native-ai/ensemble",
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


class RunCompositionRequest(BaseModel):
    objective: str = ""
    prefer_external: bool = False
    timeout: float = 12.0


def _csv(v) -> list:
    return [s.strip() for s in str(v or "").replace(";", ",").replace("\n", ",").split(",") if s.strip()]


def _cfg_num(v, default, cast=int):
    """Coerce a composed-config value to a number, tolerating the registry placeholder strings that
    compose() merges in for un-overridden params (e.g. 'int 1-3 (passages)') → fall back to default."""
    try:
        return cast(v)
    except (TypeError, ValueError):
        return default


async def _run_real_resource(rid: str, config: dict, objective: str, domain: str) -> Optional[Dict[str, Any]]:
    """§7 deep integration — invoke a composed resource's REAL endpoint logic (not a prompt approximation),
    built from the user's reconfigured params, so a committed composition runs the ACTUAL engines/resources.
    Returns a compact result dict, or None when the resource has no inline real handler. Best-effort +
    isolated (one resource's failure never blocks the others or the run)."""
    cfg = config or {}
    try:
        if rid == "petri_dish":
            from agentic_core.api.products import petri_culture, PetriRequest
            r = await petri_culture(PetriRequest(specimen=str(cfg.get("specimen") or objective), domain=domain,
                                                 medium=str(cfg.get("medium") or "standard"),
                                                 iterations=_cfg_num(cfg.get("iterations"), 1, int)))
            return {"resource": "petri_dish", "ran": "/api/v1/petri/culture", "viable": r.viable,
                    "passages": r.passages, "output": (r.culture or "")[:600]}
        if rid == "mjm":
            from agentic_core.api.intelligence import mjm_assess, MJMRequest
            r = await mjm_assess(MJMRequest(problem=objective, domain=domain, engines=_csv(cfg.get("engines"))))
            return {"resource": "mjm", "ran": "/api/v1/intelligence/mjm",
                    "cognitive_primed": r["cognitive_primed"], "output": (r["assessment"] or "")[:600]}
        if rid == "cognitive_cascade":
            from agentic_core.api.intelligence import solve_with_cognitive_stack, SolveRequest
            r = await solve_with_cognitive_stack(SolveRequest(problem=objective, domain=domain,
                                                              engines=_csv(cfg.get("engines"))))
            return {"resource": "cognitive_cascade", "ran": "/api/v1/intelligence/solve",
                    "engines_used": r.get("engines_used"), "output": (r.get("synthesis") or "")[:600]}
        if rid == "experimentation":
            from agentic_core.api.products import reactor_experiment, ExperimentRequest
            scen = _csv(cfg.get("scenarios")) or [f"Pursue: {objective}", f"Defer: {objective}"]
            r = await reactor_experiment(ExperimentRequest(
                subject=str(cfg.get("subject") or objective), domain=domain, scenarios=scen,
                fitness_criteria=str(cfg.get("fitness_criteria") or "impact, feasibility, risk, opportunity")))
            return {"resource": "experimentation", "ran": "/api/v1/reactor/experiment",
                    "scenarios_run": r.scenarios_run, "output": (r.comparison or "")[:600]}
        if rid == "incubator":
            from agentic_core.api.products import incubator_evolve, EvolveTournamentRequest
            r = await incubator_evolve(EvolveTournamentRequest(
                name=str(cfg.get("name") or objective)[:80], base_prompt=str(cfg.get("base_prompt") or objective),
                domain=domain, variants=_cfg_num(cfg.get("variants"), 3, int),
                temperature=_cfg_num(cfg.get("temperature"), 0.7, float),
                mutation=_cfg_num(cfg.get("mutation"), 0.5, float), iterations=_cfg_num(cfg.get("iterations"), 1, int)))
            return {"resource": "incubator", "ran": "/api/v1/incubator/evolve",
                    "generations_run": r.generations_run, "winner": r.winner.response[:300] if r.winner else None,
                    "output": (r.analysis or "")[:400]}
        # §6↔§7 — the OWNED native AI resources run their REAL logic when composed, reporting which owned
        #   resource actually served (ollama local model / native deterministic floor / opt-in external).
        if rid in ("bdp", "spi", "apie", "ddpie"):
            # all four headline PI engines run their REAL staged pipeline (collected from the SSE stream),
            # honouring the user's reconfigured rigor/focus — not a generic prompt stage.
            from agentic_core.api.intelligence import run_intelligence_collected
            _ep = {"apie": "authorship", "ddpie": "design-dev"}.get(rid, rid)
            r = await run_intelligence_collected(str(cfg.get("challenge") or objective), domain, rid,
                                                 rigor=str(cfg.get("rigor") or "standard"),
                                                 focus=str(cfg.get("focus") or ""))
            return {"resource": rid, "ran": f"/api/v1/intelligence/{_ep}",
                    "stages": r.get("stages"), "output": (r.get("analysis") or "")[:600]}
        if rid == "nexus":
            # the §7 Synthesis Nexus orchestrator runs its REAL 4-layer chain (cognitive cascade → MJM →
            #   auto-selected primary engine → apex synthesis), collected to completion — not a prompt.
            from agentic_core.api.intelligence import run_intelligence_collected
            r = await run_intelligence_collected(str(cfg.get("challenge") or objective), domain, "nexus",
                                                 focus=str(cfg.get("activity") or "auto"))
            return {"resource": "nexus", "ran": "/api/v1/intelligence/nexus",
                    "stages": r.get("stages"), "output": (r.get("analysis") or "")[:600]}
        if rid == "genesis":
            # the §4 Genesis Concept→Commercialisation journey runs its REAL cascade (cognitive · MJM ·
            #   research · model/rank · design · operations · commercialisation · gaas gate), bounded:
            #   establish=False so it produces the blueprint WITHOUT spawning a living VSB per run.
            from agentic_core.api.genesis import genesis_journey, JourneyRequest
            j = await genesis_journey(JourneyRequest(problem=str(cfg.get("problem") or objective), domain=domain,
                                                     realm=str(cfg.get("realm") or "enterprise"), establish=False))
            prov = j.get("ai_provenance") or {}
            sb = ",".join(sorted((prov.get("served_by") or {}).keys())) or "native"
            comm = j.get("phase_3_commercialisation")
            out = comm if isinstance(comm, str) else (j.get("phase_2_design_development") if isinstance(j.get("phase_2_design_development"), str) else "")
            return {"resource": "genesis", "ran": "/api/v1/genesis/journey", "served_by": sb,
                    "stages_verified": j.get("stages_verified"), "engines_used": j.get("engines_used"),
                    "status": j.get("status"), "output": (str(out) or "Concept→Commercialisation journey complete")[:600]}
        if rid == "genome":
            from agentic_core.organism.genome import encode_genome, EncodeRequest
            g = await encode_genome(EncodeRequest(entity_name=str(cfg.get("entity_name") or objective)[:80],
                                                  domain=domain, description=str(objective)[:500]))
            top = max((g.get("traits") or {}).items(), key=lambda kv: kv[1], default=(None, None))[0]
            return {"resource": "genome", "ran": "/api/v1/organism/genome/encode",
                    "genome_id": g.get("genome_id"), "fitness": g.get("fitness_score"),
                    "dominant_trait": top, "output": (str(g.get("expression") or "") or f"genome {g.get('genome_id')}")[:400]}
        # §8 organism systems — when composed, each runs its REAL engine/reading (the living biomimetic
        #   substrate the composition runs ON), not a prompt approximation: constitutional gate · live
        #   immune/self-healing health · ATP metabolism · circadian phase · a real nervous signal · the
        #   Sovereign-Evolution office state. Readings are bounded + side-effect-free (gaas logs to the UEG,
        #   which is the genuine, appropriate behaviour of a governance gate).
        if rid == "gaas_v5":
            from agentic_core.api.constitutional_gaas import gaas_intercept, InterceptRequest
            res = await gaas_intercept(InterceptRequest(
                action_type=str(cfg.get("action_type") or "fabric.composition"),
                payload={"objective": objective, "domain": domain}, proposed_output=objective[:500]))
            keep = {k: res.get(k) for k in ("status", "allowed", "decision", "verdict", "ueg_hash", "escalated")
                    if isinstance(res, dict) and k in res}
            return {"resource": "gaas_v5", "ran": "/api/v1/gaas/intercept", **keep,
                    "output": (json.dumps(res, default=str)[:500] if isinstance(res, dict) else str(res)[:500])}
        if rid == "nervous_system":
            from agentic_core.organism.nervous import nervous
            from agentic_core.organism.biobus import biobus
            nervous.fire("cognitive", "fabric.composition", str(objective)[:120], 0.6)   # a REAL signal fires
            ctx = biobus.organism_context(0.3)
            ner = ctx.get("nervous") or {}
            return {"resource": "nervous_system", "ran": "/api/v1/organism/nervous/stimulate",
                    "signal_fired": True, "arousal": ner.get("arousal") or ner.get("state"),
                    "output": json.dumps(ner, default=str)[:400] or "nervous signal fired"}
        if rid == "immune":
            from agentic_core.organism.immune import immune
            st = immune.status()
            return {"resource": "immune", "ran": "/api/v1/organism/immune/status",
                    "health": st.get("health"), "threat_level": st.get("threat_level"),
                    "output": json.dumps({k: st.get(k) for k in ("health", "threat_level", "errors_in_window", "hot_endpoint")}, default=str)[:400]}
        if rid == "self_healing":
            from agentic_core.organism.self_healing import self_healer
            st = self_healer.status()
            return {"resource": "self_healing", "ran": "/api/v1/organism/self-healing/status",
                    "overall_health": st.get("overall_health"), "open_circuits": st.get("open_circuits"),
                    "output": json.dumps({k: st.get(k) for k in ("overall_health", "open_circuits", "thresholds")}, default=str)[:400]}
        if rid == "metabolic":
            from agentic_core.organism.biobus import biobus
            ctx = biobus.organism_context(_cfg_num(cfg.get("metabolic_load"), 0.3, float))
            return {"resource": "metabolic", "ran": "/api/v1/organism/status",
                    "composite_health": ctx.get("composite_health"), "mode": ctx.get("mode"),
                    "metabolic": ctx.get("metabolic"),
                    "output": json.dumps({"metabolic": ctx.get("metabolic"), "mode": ctx.get("mode"),
                                          "composite_health": ctx.get("composite_health")}, default=str)[:400]}
        if rid == "circadian":
            from agentic_core.organism.biobus import biobus
            ctx = biobus.organism_context(0.3)
            circ = ctx.get("circadian") or {}
            return {"resource": "circadian", "ran": "/api/v1/organism/status",
                    "cycle": circ.get("cycle"), "is_peak_focus": circ.get("is_peak_focus"),
                    "output": json.dumps(circ, default=str)[:400] or "circadian phase read"}
        if rid == "sovereign_evolution":
            # the REAL Sovereign-Evolution Office state (last cycle / roadmap) — a bounded reading, NOT a
            #   full self-improvement cycle (which would proliferate proposals on every composition run).
            from agentic_core.api.sovereign_evolution import office_status
            st = await office_status()
            return {"resource": "sovereign_evolution", "ran": "/api/v1/sovereign-evolution/status",
                    "last_cycle": st.get("last_cycle") if isinstance(st, dict) else None,
                    "output": (json.dumps(st, default=str)[:500] if isinstance(st, dict) else str(st)[:500])}
        # Enterprise/org layer — when composed, each runs its REAL engine/reading (bounded, no state
        #   proliferation): live treasury · the genuine tiered-governance verdict for the objective · the
        #   real Products Catalogue (matched to the objective) · a real Build-to-Order blueprint.
        if rid == "capital_fund":
            from agentic_core.api.capital_fund import fund_status, fund_portfolio
            s = await fund_status(); p = await fund_portfolio()
            return {"resource": "capital_fund", "ran": "/api/v1/fund/status",
                    "total_capital": s.get("total_capital"), "available": s.get("available"),
                    "allocated": s.get("allocated"), "utilisation_pct": s.get("utilisation_pct"),
                    "fund_health": s.get("fund_health"), "allocation_count": p.get("allocation_count"),
                    "output": json.dumps({"available": s.get("available"), "allocated": s.get("allocated"),
                                          "utilisation_pct": s.get("utilisation_pct"), "by_domain": p.get("by_domain")},
                                         default=str)[:400]}
        if rid == "change_control":
            # the REAL tiered-governance verdict for the objective (classification + the live organism gate),
            #   WITHOUT persisting a change record (no proliferation on every composition run).
            from agentic_core.api.change_control import _determine_tier
            from agentic_core.organism.immune import immune
            from agentic_core.organism.biobus import biobus
            tier = _determine_tier(str(cfg.get("change_type") or "feature"), str(objective))
            health = (biobus.organism_context(0.3) or {}).get("composite_health", 1.0)
            threat = immune.status().get("threat_level", "NOMINAL")
            verdict = ("blocked (human escalation)" if tier == "CRITICAL"
                       else "auto-approved" if (tier == "LOW" and health >= 0.6 and threat in ("NOMINAL", "ELEVATED"))
                       else "queued for AI review")
            return {"resource": "change_control", "ran": "/api/v1/cca/submit (assess · not persisted)",
                    "impact_tier": tier, "verdict": verdict, "organism_health": round(float(health), 3),
                    "immune_threat": threat,
                    "output": f"Governance: tier {tier} → {verdict} (organism health {round(float(health), 3)}, immune {threat})."}
        if rid == "products_catalogue":
            from agentic_core.catalog.api import list_products
            ps = list_products()
            obj_tokens = {w for w in str(objective).lower().replace(",", " ").split() if len(w) > 3}
            def _score(p):
                hay = (str(p.get("name", "")) + " " + str(p.get("category", "")) + " "
                       + " ".join(p.get("features", []) or [])).lower()
                return sum(1 for t in obj_tokens if t in hay)
            ranked = sorted(ps, key=_score, reverse=True)
            top = [{"slug": p["slug"], "name": p["name"], "tier": p.get("tier"), "match": _score(p)}
                   for p in ranked[:5]]
            return {"resource": "products_catalogue", "ran": "/api/v1/catalog/products",
                    "total_products": len(ps), "top_matches": top,
                    "output": json.dumps(top, default=str)[:400]}
        if rid == "build_to_order":
            from agentic_core.catalog.bto import configure_bto, BTOConfigureRequest
            from agentic_core.catalog.api import list_products
            slugs = _csv(cfg.get("product_resources")) or [p["slug"] for p in list_products()[:2]]
            comps = _csv(cfg.get("components")) or ["vsb", "csuite"]
            bp = await configure_bto(BTOConfigureRequest(
                entity_name=str(cfg.get("entity_name") or objective)[:80],
                product_resources=slugs, components=comps))
            return {"resource": "build_to_order", "ran": "/api/v1/bto/configure",
                    "blueprint_id": bp.get("blueprint_id"), "resource_count": bp.get("resource_count"),
                    "component_count": bp.get("component_count"),
                    "output": json.dumps({"resource_count": bp.get("resource_count"),
                                          "component_count": bp.get("component_count"),
                                          "components": list((bp.get("components") or {}).keys())},
                                         default=str)[:400]}
        if rid == "native_orchestrator":
            from agentic_core.ai.native import orchestrator
            res = await orchestrator.complete(str(cfg.get("prompt") or objective),
                                              agent=str(cfg.get("agent") or "fabric-composition"),
                                              prefer_external=bool(cfg.get("prefer_external", False)),
                                              prefer=str(cfg.get("model") or "auto"))
            return {"resource": "native_orchestrator", "ran": "/api/v1/native-ai/complete",
                    "served_by": res.get("served_by"), "is_external": res.get("is_external"),
                    "output": (res.get("output") or "")[:600]}
        if rid == "native_ensemble":
            from agentic_core.ai.native import orchestrator
            res = await orchestrator.ensemble(str(cfg.get("prompt") or objective),
                                              agent="fabric-ensemble", models=_csv(cfg.get("models")) or None,
                                              synthesize=bool(cfg.get("synthesize", True)))
            members = res.get("members") or []
            # synthesis when >1 member produced; else fall back to the single member's output
            out = (res.get("synthesis") or {}).get("output") or ""
            if not out:
                out = next((m.get("output", "") for m in members if m.get("output")), "")
            return {"resource": "native_ensemble", "ran": "/api/v1/native-ai/ensemble",
                    "models_run": res.get("models_run"), "members": len(members),
                    "served_by": ",".join(sorted({str(m.get("served_by")) for m in members if m.get("served_by")})),
                    "output": out[:600]}
        # §7 musculoskeletal facilities — each runs its REAL engine when composed, now driven by the
        #   OWNED native swarm (§6). Reactor + Factory previously streamed via the legacy external-first
        #   cascade; their shared native-driven runners are reused here so a composition runs the genuine
        #   engine with in-house provenance.
        if rid == "reactor":
            # the §7 composite Reactor = Incubator (evolution) + Experimentation (what-if) + Studio
            #   (analytics over the real fitness) — the vision's definition, run as one on the swarm.
            from agentic_core.api.products import run_reactor_composite
            r = await run_reactor_composite(
                subject=str(cfg.get("subject") or objective), domain=domain,
                variants=_cfg_num(cfg.get("variants"), 3, int),
                temperature=_cfg_num(cfg.get("temperature"), 0.7, float),
                mutation=_cfg_num(cfg.get("mutation"), 0.5, float),
                iterations=_cfg_num(cfg.get("iterations"), 1, int),
                scenarios=_csv(cfg.get("scenarios")) or None)
            return {"resource": "reactor", "ran": "/api/v1/reactor/composite", "served_by": r["served_by"],
                    "sub_facilities": r["sub_facilities"], "generations_run": r["evolution"]["generations_run"],
                    "scenarios_run": r["experimentation"]["scenarios_run"],
                    "studio_dimensions": (r["studio"] or {}).get("dimensions"),
                    "output": (r["evolution"]["winner"] or r["experimentation"]["comparison"] or "")[:600]}
        if rid == "factory":
            from agentic_core.api.products import run_factory_produce
            prod = await run_factory_produce(name=str(cfg.get("name") or objective)[:80],
                                             product_type=str(cfg.get("product_type") or "business_model"),
                                             domain=domain, description=str(cfg.get("brief") or objective)[:500],
                                             prefer=str(cfg.get("model") or "auto"))
            return {"resource": "factory", "ran": "/api/v1/factory/produce", "served_by": prod["served_by"],
                    "is_external": prod["is_external"], "product_type": str(cfg.get("product_type") or "business_model"),
                    "output": (prod["output"] or "")[:600]}
        if rid == "resource_optimizer":
            from agentic_core.api.optimizer import allocate, AllocateRequest
            req_map = cfg.get("requirements")
            if not isinstance(req_map, dict) or not req_map:
                req_map = {"CPU": 4, "RAM": 1024}
            r = await allocate(AllocateRequest(domain=domain, requirements=req_map,
                                               tier=str(cfg.get("tier") or "standard")))
            return {"resource": "resource_optimizer", "ran": "/api/v1/optimizer/allocate",
                    "posture": r.get("posture"), "simulated_capacity": r.get("simulated_capacity"),
                    "output": (json.dumps({k: v for k, v in r.items() if k not in ("note",)})[:600])}
        if rid == "digital_twin":
            # the §7 Simulator: forward-simulate a system under a scenario on the native swarm — genuine
            #   in-house cognition (no fabricated telemetry; honestly a model-driven simulation narrative).
            from agentic_core.ai.native import orchestrator
            system = str(cfg.get("system") or objective)[:200]
            scenario = str(cfg.get("scenario") or "baseline operation")[:200]
            prompt = (f"You are a digital-twin simulator. System under twin: {system} (domain {domain}). "
                      f"Forward-simulate the scenario: {scenario}.\n## State Trajectory (t0→tN)\n"
                      "## Emergent Behaviour\n## Stress / Failure Points\n## Recommended Setpoints")
            res = await orchestrator.complete(prompt, agent="digital-twin",
                                              prefer=str(cfg.get("model") or "auto"))
            return {"resource": "digital_twin", "ran": "/api/v1/twin/simulate", "served_by": res.get("served_by"),
                    "is_external": bool(res.get("is_external")), "scenario": scenario,
                    "output": (res.get("output") or "")[:600]}
        if rid == "generator":
            # the §7 Generator: produce ONE targeted artefact in a chosen format on the native swarm.
            from agentic_core.api.products import run_generator
            g = await run_generator(artefact_type=str(cfg.get("artefact_type") or "content"),
                                    spec=str(cfg.get("spec") or objective), domain=domain,
                                    fmt=str(cfg.get("format") or "markdown"),
                                    prefer=str(cfg.get("model") or "auto"))
            return {"resource": "generator", "ran": "/api/v1/generator/produce",
                    "artefact_type": g["artefact_type"], "format": g["format"],
                    "served_by": g["served_by"], "is_external": g["is_external"],
                    "output": (g["output"] or "")[:600]}
        if rid == "synthesis_studio":
            # the §7 Laboratory: run the genuine concept→commercialisation cascade (compose-mode — no VSB
            #   spawn), on the native swarm. max_stages bounds how many of the 9 stages run.
            from agentic_core.api.synthesis_studio import run_lab_cascade
            r = await run_lab_cascade(challenge=str(cfg.get("brief") or objective),
                                      realm=str(cfg.get("realm") or "enterprise"), domain=domain,
                                      solution_name=str(cfg.get("solution_name") or ""),
                                      max_stages=_cfg_num(cfg.get("max_stages"), 3, int))
            sb = ",".join(sorted(r["served_by"].keys())) or "native"
            out = r["stages"].get("solution_concept") or next(iter(r["stages"].values()), "")
            return {"resource": "synthesis_studio", "ran": "/api/v1/studio/synthesise",
                    "stages_run": r["stages_run"], "served_by": sb, "output": (out or "")[:600]}
        if rid == "studio":
            # the §7 Studio: deterministic 2D/3D analytics + insight over a REAL configured data series.
            #   Honestly skips (returns None → generic stage) when no numeric series is configured.
            series = cfg.get("series")
            if not isinstance(series, list) or not series:
                return None
            from agentic_core.api.products import reactor_studio, StudioRequest, StudioPoint
            pts = []
            for p in series:
                if isinstance(p, dict) and p.get("label") is not None and p.get("value") is not None:
                    pts.append(StudioPoint(label=str(p["label"]), value=float(p["value"]),
                                           z=(float(p["z"]) if p.get("z") is not None else None)))
            if not pts:
                return None
            r = await reactor_studio(StudioRequest(title=str(cfg.get("title") or objective)[:120], domain=domain,
                                                   chart_type=str(cfg.get("chart_type") or "bar"), series=pts))
            return {"resource": "studio", "ran": "/api/v1/reactor/studio", "dimensions": r.dimensions,
                    "analytics": r.analytics, "output": (r.insight or json.dumps(r.analytics))[:600]}
        if rid == "native_swarm":
            from agentic_core.ai.native import orchestrator
            raw = cfg.get("stages")
            if isinstance(raw, str) and raw.strip():
                stages = [{"role": "stage", "instruction": s.strip()} for s in raw.splitlines() if s.strip()]
            elif isinstance(raw, list) and raw:
                stages = [s if isinstance(s, dict) else {"role": "stage", "instruction": str(s)} for s in raw]
            else:
                stages = [{"role": "synthesist", "instruction": f"Advance the objective: {objective}"}]
            res = await orchestrator.swarm(str(cfg.get("agent") or "fabric-swarm"), stages,
                                           context=str(cfg.get("context") or objective))
            served = res["trace"][0]["served_by"] if res.get("trace") else "native"
            return {"resource": "native_swarm", "ran": "/api/v1/resources/swarm/run",
                    "stages_run": len(stages), "served_by": served, "output": (res.get("final") or "")[:600]}
    except Exception as e:
        return {"resource": rid, "error": str(e)[:160]}
    return None


@router.post("/compositions/{cid}/run")
async def run_composition(cid: str, req: RunCompositionRequest):
    """Run a saved configuration end-to-end on Workstation's OWN native swarm (§6): each composed resource
    becomes a pipeline stage (the org-cascade resource is a §5 stage), the user's reconfigured parameters
    feed in, each stage completes in-house-first and feeds the next, and the combined run is QMS-gated +
    document-controlled (§10/§8). Resources with a real endpoint (Petri/Incubator/Reactor/MJM/Cascade) ALSO
    execute their genuine logic — so a committed composition runs the ACTUAL engines, fully rerunnable (§7)."""
    comp = next((c for c in _load_compositions() if c["id"] == cid), None)
    if not comp:
        raise HTTPException(status_code=404, detail=f"Composition {cid} not found.")

    stages: List[Dict[str, str]] = []
    for r in comp.get("resources", []):
        base = _BY_ID.get(r["id"], {})
        caps = ", ".join(base.get("capabilities", [])) or base.get("type", r.get("resource_class", ""))
        # the user-SET params are those whose value differs from the declared type placeholder
        configured = {k: v for k, v in (r.get("config") or {}).items()
                      if v != base.get("reconfigurable_params", {}).get(k)}
        cfg_txt = "; ".join(f"{k}={v}" for k, v in configured.items())
        if r["id"] == "vsb_org_swarm":
            # §5 fine-resolution: run the living organisation with the USER-DESIGNED C-Suite (§7 design
            # control over the §5 org structure), on the native swarm — the Chief→Build-to-Order tiers.
            roles = configured.get("csuite_roles") or "CSO, CFO, CTO, COO, CLO"
            coes = configured.get("coe_specialisms")
            instruction = (
                f"You are the §5 living organisation. Run the org cascade for the objective: the AI CEO "
                f"directs the user-designed C-Suite ({roles}); each named officer drives its Centre of "
                f"Excellence" + (f" (specialisms: {coes})" if coes else "") + "; and the Business "
                f"Transformation Office build-to-orders the delivery. Provide:\n"
                "## AI CEO Directive\n## C-Suite Plans (one section per officer)\n"
                "## Centres of Excellence\n## Build-to-Order Delivery")
        else:
            instruction = (f"As the «{r['name']}» resource ({base.get('type', r.get('resource_class', ''))}), "
                           f"apply your capabilities ({caps}) to advance the objective."
                           + (f" Configured parameters: {cfg_txt}." if cfg_txt else "")
                           + " Build on the prior stage's output; be specific and actionable.")
        stages.append({"role": r["name"], "instruction": instruction})
    if not stages:
        raise HTTPException(status_code=400, detail="Composition has no resources to run.")

    objective = req.objective or f"Execute the '{comp['name']}' configuration for {comp.get('usage_area', 'synthesis')}."
    from agentic_core.ai.native import orchestrator
    _t0 = time.time()
    res = await orchestrator.swarm("composition-run", stages, context=objective,
                                   prefer_external=req.prefer_external, timeout=req.timeout)
    # §10/§8 — the combined run is gated by the living QMS + document-controlled under the QMS
    qa = await assure_delivery(res.get("final", ""), [r["name"] for r in comp["resources"]],
                               label="composition_run")
    try:
        from agentic_core.api.operational_excellence import record_outcome
        served = res["trace"][0]["served_by"] if res.get("trace") else "native"
        record_outcome("composition_run", f"composition:{comp['name']}", served_by=served,
                       is_external=bool(res.get("any_external")),
                       duration_ms=int((time.time() - _t0) * 1000),
                       success=bool(res.get("trace")), ref=cid)
    except Exception:
        pass
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "resource_fabric.composition.run",
                           f"{comp['name']}: {len(stages)} stages", 0.6)
    except Exception:
        pass

    # §7→§5→§6→§8 END-TO-END: when the configuration includes the living-organisation resource, ALSO run the
    # REAL Chief→Build-to-Order cascade (fine-resolution §5: AI CEO → user-designed C-Suite → CoEs → BTO →
    # Build-to-Order, with the living management systems, arms-length appraisals, constitutional governance,
    # §8 homeostatic posture and §6 in-house provenance) for the objective — so the §7 fabric delivers the
    # genuine §5 machinery, not just a prompt stage. Additive (keeps the swarm trace) + best-effort.
    org_cascade = None
    org_r = next((r for r in comp.get("resources", []) if r["id"] == "vsb_org_swarm"), None)
    if org_r:
        try:
            from agentic_core.api.swarm import cascade_orchestration, CascadeRequest
            cfg = org_r.get("config") or {}
            def _csv(v): return [s.strip() for s in str(v).replace(";", ",").split(",") if s.strip()]
            casc = await cascade_orchestration(CascadeRequest(
                mission=objective, domain=(comp.get("usage_area") or "general"),
                csuite_roles=_csv(cfg.get("csuite_roles", "")),
                coe_specialisms=_csv(cfg.get("coe_specialisms", "")),
            ))
            org_cascade = {
                "ran": "real §5 Chief→Build-to-Order cascade",
                "run_id": casc.get("run_id"),
                "org_hierarchy": casc.get("org_hierarchy"),
                "csuite_engaged": (casc.get("csuite_roster") or {}).get("engaged"),
                "management_systems": list((casc.get("management_systems") or {}).keys()),
                "appraisals": list((casc.get("appraisals") or {}).keys()),
                "quality": casc.get("quality"),
                "biomimetic": casc.get("biomimetic"),
                "homeostasis": casc.get("homeostasis"),
                "governance": (casc.get("governance") or {}).get("status") if isinstance(casc.get("governance"), dict) else casc.get("governance"),
                "ai_provenance": casc.get("ai_provenance"),
                "ueg_hash": casc.get("ueg_hash"),
            }
        except Exception:
            org_cascade = None

    # §7 deep integration: for each composed resource with a REAL endpoint, ALSO execute its genuine logic
    # (the actual Petri culture / Incubator evolution / Reactor experiment / MJM judgement / Cognitive solve)
    # built from the user's reconfigured params — so the composition runs the real engines, not only prompt
    # stages. Additive + isolated (best-effort per resource; the org-cascade resource is handled above).
    domain = comp.get("usage_area") or "general"
    real_runs: list = []
    for r in comp.get("resources", []):
        if r["id"] == "vsb_org_swarm":
            continue
        rr = await _run_real_resource(r["id"], r.get("config") or {}, objective, domain)
        if rr is not None:
            real_runs.append(rr)

    return {"composition_id": cid, "name": comp["name"], "usage_area": comp.get("usage_area"),
            "objective": objective, "posture": "in-house-first", "quality_assurance": qa,
            "org_cascade": org_cascade, "real_resource_runs": real_runs, **res}


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


def _model_configuration(resource_ids: List[str], usage_area: str,
                         config: Dict[str, Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """MODEL a proposed configuration (no save): resolve the resources with their reconfigured params,
    and derive the pipeline, combined capabilities, class/biomimetic mix, shared usage areas, the params
    still needing values, and any usage-area incompatibilities. The §7 'modelling … before commit'."""
    resolved: List[Dict[str, Any]] = []
    classes: Dict[str, int] = {}
    caps: List[str] = []
    biomimetic = 0
    unset: Dict[str, List[str]] = {}
    shared_areas: Optional[set] = None
    incompatibilities: List[Dict[str, str]] = []
    for rid in resource_ids:
        base = _BY_ID[rid]
        overrides = config.get(rid, {})
        merged = {**base["reconfigurable_params"], **overrides}
        resolved.append({"id": rid, "name": base["name"], "resource_class": base["resource_class"],
                         "endpoint": base["endpoint"], "config": merged})
        classes[base["resource_class"]] = classes.get(base["resource_class"], 0) + 1
        caps.extend(base["capabilities"])
        if base["biomimetic"]:
            biomimetic += 1
        still = [k for k in base["reconfigurable_params"] if k not in overrides]
        if still:
            unset[rid] = still
        areas = set(base["usable_in"])
        shared_areas = areas if shared_areas is None else (shared_areas & areas)
        if usage_area not in base["usable_in"]:
            incompatibilities.append({"id": rid, "name": base["name"],
                                      "reason": f"does not support usage area '{usage_area}'"})
    model = {
        "pipeline": [r["name"] for r in resolved],
        "combined_capabilities": sorted(set(caps)),
        "resource_classes": classes,
        "biomimetic_resources": biomimetic,
        "shared_usage_areas": sorted(shared_areas or []),
        "usage_area": usage_area,
        "usage_area_supported_by_all": len(incompatibilities) == 0,
        "incompatibilities": incompatibilities,
        "unset_params": unset,
    }
    # §7→§8 — project the living organism's CURRENT capacity for this configuration's cognitive load, so the
    # user designs with awareness of whether the organism can admit it now (read-only; the run is governed by
    # §8 homeostasis at execution time). Best-effort, fail-soft.
    try:
        from agentic_core.ai.native.homeostasis import homeostasis
        model["organism_capacity"] = homeostasis.project(len(resolved))
    except Exception:
        model["organism_capacity"] = None
    return resolved, model


async def _simulate_configuration(name: str, resource_ids: List[str], usage_area: str,
                                  config: Dict[str, Dict[str, Any]]):
    """MODEL + SIMULATE a configuration before commit (§7): the config plan is gated by the living QMS
    (held to the §10 bar, recorded within the §8 organism). commit_ready iff the gate passes AND every
    selected resource supports the chosen usage area."""
    resolved, model = _model_configuration(resource_ids, usage_area, config)
    n = len(resolved)
    plan_text = (f"Configuration '{name}' for usage area '{usage_area}', composing {n} resources: "
                 + ", ".join(model["pipeline"]) + ". Combined capabilities: "
                 + ", ".join(model["combined_capabilities"][:24]) + ".") if n else ""
    qa = await assure_delivery(plan_text, [r["name"] for r in resolved], label="composition")
    commit_ready = bool(qa["quality"].get("qms_gate_passed") and model["usage_area_supported_by_all"])
    return resolved, model, qa, commit_ready


@router.post("/compose/simulate")
async def simulate_composition(req: ComposeRequest):
    """§7 — MODEL + SIMULATE a configuration BEFORE commit. Returns the modelled structure + a living-QMS
    simulation (gate + §10 bar + §8 organism) + commit-readiness. Nothing is saved."""
    unknown = [rid for rid in req.resource_ids if rid not in _BY_ID]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown resource ids: {unknown}")
    if not req.resource_ids:
        raise HTTPException(status_code=400, detail="Select at least one resource to model.")
    resolved, model, qa, commit_ready = await _simulate_configuration(
        req.name or "(unnamed)", req.resource_ids, req.usage_area, req.config)
    return {"name": req.name, "usage_area": req.usage_area, "resources": resolved,
            "model": model, "simulation": qa, "commit_ready": commit_ready, "saved": False,
            "note": "Modelled + simulated before commit (§7) — not saved. Adjust the design, then compose."}


@router.post("/compose")
async def compose(req: ComposeRequest):
    """Combine selected resources into a named, reusable, re-runnable configuration — modelled +
    QMS-gated, and document-controlled under the QMS on commit (the saved config carries its model +
    quality record)."""
    unknown = [rid for rid in req.resource_ids if rid not in _BY_ID]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown resource ids: {unknown}")

    resolved, model, qa, commit_ready = await _simulate_configuration(
        req.name, req.resource_ids, req.usage_area, req.config)

    composition = {
        "id": f"comp-{uuid.uuid4().hex[:8]}",
        "name": req.name,
        "usage_area": req.usage_area,
        "resources": resolved,
        "model": model,
        "quality_assurance": qa,
        "commit_ready": commit_ready,
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
