"""
Forge — executable Digital Resource pipelines.

Makes the IDBO's digital resources — Petri Dish · Incubator · Laboratory ·
Factory · Generator · Simulator · Reactor — accessible, reconfigurable,
re-runnable and reusable as STAGES of an AI-mediated cascade pipeline,
orchestrated through the VSB swarm hierarchy (AI CEO frames the objective →
each resource processes in cascade carrying prior context → CoE/BTO integrate
the multi-type outputs). Produces integrated outputs for Concept →
Commercialisation, and can feed a bespoke VSB IDBO entity.

Builds on the Resource Fabric (/api/v1/resources) and the reactor ecosystem
(agentic_core/reactor/*). Governed by gaas.v5, audited to the UEG.

  GET  /api/v1/forge/resources         — the digital resource stages + reconfigurable params
  POST /api/v1/forge/run               — execute a configured pipeline of selected resources
  GET  /api/v1/forge/runs              — list saved runs (reusable)
  POST /api/v1/forge/runs/{run_id}/rerun — re-run a saved pipeline
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/forge", tags=["forge-pipelines"])

_STORE = Path("data/forge_runs.json")

# The digital resources, each an executable cascade stage (biomimetic + reconfigurable).
_STAGES: Dict[str, Dict[str, Any]] = {
    "petri_dish": {
        "name": "Petri Dish", "biomimetic": "culture in a controlled micro-environment",
        "role": "Small-scale controlled experimentation — test viability/hypothesis cheaply.",
        "params": {"hypothesis": "str"},
        "prompt": ("As a Digital Petri Dish, run a small-scale controlled experiment on the objective. "
                   "Output: ## Experiment Setup\n## Observations\n## Viability Verdict"),
    },
    "incubator": {
        "name": "Incubator", "biomimetic": "nurture & grow under optimal conditions",
        "role": "Iterative development — evolve and rank variants of the concept.",
        "params": {"variations": "int"},
        "prompt": ("As a Digital Incubator, iteratively develop the concept: generate 3 variants, "
                   "evaluate, and rank. Output: ## Variants\n## Evaluation\n## Recommended Variant"),
    },
    "laboratory": {
        "name": "Laboratory", "biomimetic": "deep analysis & synthesis bench",
        "role": "Research synthesis & analysis — rigorous findings from inputs.",
        "params": {"depth": "str"},
        "prompt": ("As a Digital Laboratory, perform rigorous research synthesis on the objective. "
                   "Output: ## Method\n## Findings (evidence-based)\n## Implications"),
    },
    "factory": {
        "name": "Factory", "biomimetic": "production line",
        "role": "Production — generate a production-grade artifact.",
        "params": {"artifact": "str"},
        "prompt": ("As a Digital Factory, produce a production-grade artifact for the objective. "
                   "Output: ## Artifact (complete, structured, ready-to-use)\n## Quality Notes"),
    },
    "generator": {
        "name": "Generator", "biomimetic": "morphogenesis — generate form",
        "role": "Generate a specific output type (doc / site / app scaffold / model).",
        "params": {"output_type": "str"},
        "prompt": ("As a Digital Generator, generate the requested output type for the objective. "
                   "Output: ## Generated Output\n## Usage"),
    },
    "simulator": {
        "name": "Simulator", "biomimetic": "digital-twin scenario modelling",
        "role": "Model & simulate — scenario testing and optimisation via digital twin.",
        "params": {"scenario": "str"},
        "prompt": ("As a Digital Twin Simulator, model the objective and simulate scenarios. "
                   "Output: ## Model\n## Scenario Results\n## Optimisation"),
    },
    "reactor": {
        "name": "Reactor", "biomimetic": "domain processing chamber",
        "role": "Domain-specific processing pipeline.",
        "params": {"domain": "str"},
        "prompt": ("As a Domain Reactor, process the objective through a domain-specific pipeline "
                   "(ingestion → analysis → synthesis → validation). Output: ## Processing Trace\n## Output Artefact"),
    },
}


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(rows: List[Dict[str, Any]]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(rows[-100:], indent=2), encoding="utf-8")


@router.get("/resources")
async def forge_resources():
    """The digital resource stages selectable for a pipeline."""
    return {
        "resources": [{"id": k, "name": v["name"], "role": v["role"],
                       "biomimetic": v["biomimetic"], "params": v["params"]} for k, v in _STAGES.items()],
        "usage_areas": ["synthesis", "build_to_order", "forge"],
        "reconfigurable": True, "rerunnable": True, "reusable": True,
    }


class StageConfig(BaseModel):
    type: str
    config: Dict[str, Any] = {}


class ForgeRunRequest(BaseModel):
    objective: str
    domain: str = "enterprise"
    realm: str = "enterprise"
    stages: List[StageConfig] = []          # ordered; empty = a sensible default pipeline
    usage_area: str = "forge"               # synthesis | build_to_order | forge
    name: str = ""


_DEFAULT_PIPELINE = ["petri_dish", "laboratory", "factory"]


async def _execute(req: ForgeRunRequest) -> Dict[str, Any]:
    run_id = f"forge-{uuid.uuid4().hex[:8]}"
    start = time.time()
    stage_ids = [s.type for s in req.stages if s.type in _STAGES] or _DEFAULT_PIPELINE
    configs = {s.type: s.config for s in req.stages}

    # In-house-first AI with provenance: every stage records which OWNED resource served it.
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _q(prompt: str, agent: str) -> str:
        try:
            res = await gateway.query_meta(prompt, agent=agent)
            sb = res.get("served_by", "native")
            provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
            provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
            return res.get("output", "")
        except Exception as e:
            return f"[{agent} unavailable: {e}]"

    # 1. AI CEO frames the objective (swarm hierarchy entry)
    ceo = await _q(
        f"You are the AI CEO of a VSB. Frame this objective for a Forge pipeline that will run these "
        f"digital resources in cascade: {', '.join(_STAGES[s]['name'] for s in stage_ids)}.\n\n"
        f"Objective: {req.objective}\nDomain: {req.domain} | Realm: {req.realm}\n\n"
        "## Framing (what success looks like)\n## Directive to the resource pipeline",
        "forge_ceo")

    # 2. Each resource processes in cascade, carrying accumulated context
    context = f"CEO framing: {ceo[:500]}"
    outputs: List[Dict[str, Any]] = []
    for sid in stage_ids[:7]:
        stage = _STAGES[sid]
        cfg = configs.get(sid, {})
        prompt = (f"{stage['prompt']}\n\nObjective: {req.objective}\nDomain: {req.domain}\n"
                  + (f"Configuration: {cfg}\n" if cfg else "")
                  + f"Prior pipeline context: {context[-600:]}")
        result = await _q(prompt, f"forge_{sid}")
        context += f"\n\n## {stage['name']} output\n{result[:400]}"
        outputs.append({"resource": sid, "name": stage["name"], "biomimetic": stage["biomimetic"],
                        "config": cfg, "output": result})

    # 3. CoE integrates the multi-type outputs (swarm synthesis)
    integration = await _q(
        "You are the Centre of Excellence integrating a Forge pipeline's outputs into one coherent, "
        f"high-quality deliverable for Concept → Commercialisation.\n\nObjective: {req.objective}\n"
        f"Pipeline: {' → '.join(_STAGES[s]['name'] for s in stage_ids)}\n"
        f"Stage outputs:\n{context[-1500:]}\n\n"
        "## Integrated Deliverable\n## Multi-Type Outputs Produced\n## Path to Commercialisation (next: establish a VSB)",
        "forge_coe")

    # Governance attestation + audit
    governance = "ungated"
    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        gov = UnifiedConstitutionalInterceptorV16Omega("forge-node", UEGLogger("meta/gaas_v5_ueg.json"))

        async def _attest():
            return f"Forge pipeline {run_id} synthesised under constitutional supervision."
        res = await gov.intercept({"intent": "forge_pipeline", "domain": req.domain}, _attest)
        governance = res.status
    except Exception:
        pass
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "forge.run", f"{len(outputs)} stages: {req.objective[:50]}", 0.8)
    except Exception:
        pass

    run = {
        "run_id": run_id,
        "name": req.name or f"Forge: {req.objective[:50]}",
        "objective": req.objective, "domain": req.domain, "realm": req.realm,
        "usage_area": req.usage_area,
        "pipeline": stage_ids,
        "ceo_framing": ceo,
        "stage_outputs": outputs,
        "integrated_deliverable": integration,
        "governance": governance,
        "ai_provenance": provenance,
        "reusable": True, "rerunnable": True,
        "duration_ms": int((time.time() - start) * 1000),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "next": "POST /api/v1/genesis/establish to commercialise this as a living VSB IDBO entity.",
    }
    rows = _load()
    rows.append(run)
    _save(rows)
    return run


@router.post("/run")
async def forge_run(req: ForgeRunRequest):
    """Execute a configured digital-resource pipeline (swarm-orchestrated cascade)."""
    return await _execute(req)


@router.get("/runs")
async def forge_runs():
    rows = _load()
    return {"runs": [{"run_id": r["run_id"], "name": r["name"], "pipeline": r["pipeline"],
                      "usage_area": r.get("usage_area"), "created_at": r["created_at"]} for r in rows[-50:]][::-1],
            "total": len(rows)}


@router.post("/runs/{run_id}/rerun")
async def forge_rerun(run_id: str):
    for r in _load():
        if r["run_id"] == run_id:
            req = ForgeRunRequest(objective=r["objective"], domain=r["domain"], realm=r["realm"],
                                  stages=[StageConfig(type=s) for s in r["pipeline"]],
                                  usage_area=r.get("usage_area", "forge"), name=f"{r['name']} (rerun)")
            return await _execute(req)
    raise HTTPException(status_code=404, detail=f"Run {run_id} not found.")
