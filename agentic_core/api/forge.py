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
from agentic_core.config import atomic_write_json, data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from agentic_core.api._ai_provenance import reply_evidence as _reply_evidence   # W698: the level travels with the record
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/forge", tags=["forge-pipelines"])

_STORE = data_path("forge_runs.json")

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
    atomic_write_json(_STORE, rows[-100:])


@router.get("/resources")
async def forge_resources():
    """The digital resource stages selectable for a pipeline."""
    return {
        "resources": [{"id": k, "name": v["name"], "role": v["role"],
                       "biomimetic": v["biomimetic"], "params": v["params"]} for k, v in _STAGES.items()],
        #  P3.30 (ledger v16 R4.12) - `params` names keys; the request field that carries them is `config`
        "params_basis": ("`params` lists the keys a stage's configuration may carry. On POST /forge/run each "
                         "stage is {\"type\": <id>, \"config\": {<key>: <value>}} - the request field is "
                         "`config`, and a stage `type` that is not one of the ids above is refused (422)."),
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
#  W805 (FU-823) - the most stages one pipeline runs; a longer one is refused rather than cut
_MAX_STAGES = 7


async def _execute(req: ForgeRunRequest) -> Dict[str, Any]:
    #  P3.30 (ledger v16 R4.12) - AN UNKNOWN STAGE IS REFUSED, NOT REPLACED. Unknown types were filtered out,
    #  and when none was left the default three-stage pipeline ran in their place: a caller who asked for a
    #  stage that does not exist received a different pipeline's run with nothing to say so, and a mixed list
    #  ran a silent subset. Refused HERE - the one function both /run and /rerun reach - before any call is
    #  made or any row is stored, with a text detail naming what was unknown and what exists.
    _unknown = [str(s.type) for s in req.stages if s.type not in _STAGES]
    if _unknown:
        raise HTTPException(status_code=422, detail=(
            f"unknown Forge stage type(s): {', '.join(repr(u[:60]) for u in _unknown)}. Nothing was run and "
            f"nothing was stored. The stage types are: {', '.join(sorted(_STAGES))}. Send no stages at all "
            f"to run the default pipeline ({' -> '.join(_DEFAULT_PIPELINE)})."))
    #  W805 (FU-823) - A PIPELINE LONGER THAN A RUN IS REFUSED, NOT CUT. The loop ran the first seven while the
    #  record listed every stage asked for, so a stage that never ran was reported as part of the pipeline.
    if len(req.stages) > _MAX_STAGES:
        raise HTTPException(status_code=422, detail=(
            f"a Forge pipeline runs at most {_MAX_STAGES} stages and this one names {len(req.stages)}, so nothing "
            f"was run and nothing was stored. Send {_MAX_STAGES} or fewer."))
    run_id = f"forge-{uuid.uuid4().hex[:8]}"
    start = time.time()
    stage_ids = [s.type for s in req.stages] or list(_DEFAULT_PIPELINE)
    _pipeline_source = "requested" if req.stages else "default"
    #  W805 (FU-823) - BY POSITION, not by type: two stages of one type each keep their own configuration
    configs = [s.config for s in req.stages]

    # In-house-first AI with provenance: every stage records which OWNED resource served it.
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False, **_reply_evidence()}

    async def _q_meta(prompt: str, agent: str, user_text: Optional[str] = None) -> tuple:
        """The output and what served it; served_by is None when the call failed (W805, FU-823). Each caller says
        which words the person wrote (W651, FU-675), as every gateway call does."""
        try:
            res = await gateway.query_meta(prompt, agent=agent, augment=False, user_text=user_text)
            sb = res.get("served_by", "native")
            provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
            provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
            return res.get("output", ""), sb
        except Exception as e:
            return f"[{agent} unavailable: {e}]", None

    async def _q(prompt: str, agent: str) -> str:
        return (await _q_meta(prompt, agent, user_text=(req.objective or None)))[0]   # W651 (FU-675)

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
    for _pos805, sid in enumerate(stage_ids):
        stage = _STAGES[sid]
        cfg = (configs[_pos805] if _pos805 < len(configs) else {}) or {}
        prompt = (f"{stage['prompt']}\n\nObjective: {req.objective}\nDomain: {req.domain}\n"
                  + (f"Configuration: {cfg}\n" if cfg else "")
                  + f"Prior pipeline context: {context[-600:]}")
        result, _served805 = await _q_meta(prompt, f"forge_{sid}", user_text=(req.objective or None))
        context += f"\n\n## {stage['name']} output\n{result[:400]}"
        #  W803 (FU-983, ledger v17 R4[5]) - WHAT THE STAGE IS. Each is a prompt asking the serving resource to act as
        #  the facility it is named after; the facility's own engine is not called. The page said so; the body did not.
        outputs.append({"resource": sid, "name": stage["name"], "biomimetic": stage["biomimetic"],
                        "config": cfg, "output": result,
                        #  W805 (FU-823) - what served THIS stage (None when its call failed), and so its level
                        "served_by": _served805, **_reply_evidence(_served805),
                        "kind": "persona_prompt",
                        "kind_basis": (f"a prompt asking the serving resource to act as the {stage['name']}; the "
                                       f"{stage['name']} facility's own engine was not called")})

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
        gov = UnifiedConstitutionalInterceptorV16Omega("forge-node", UEGLogger())

        async def _attest():
            return f"Forge pipeline {run_id} synthesised under constitutional supervision."
        res = await gov.intercept({"intent": "forge_pipeline", "domain": req.domain}, _attest)
        # W494 (FU-130) — a bare status string, with nothing saying the pipeline's output was not seen
        from agentic_core.gaas.v5 import intent_gate_result
        governance = intent_gate_result(res.status, res.checkpoint_id, getattr(res, "node", None))
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
        #  P3.30 (R4.12) - whether these stages were asked for or are the default for a request naming none
        "pipeline_source": _pipeline_source,
        "pipeline_basis": ("the stages the request named, in its order" if _pipeline_source == "requested" else
                           "the request named no stage, so the default pipeline ran: "
                           + " -> ".join(_DEFAULT_PIPELINE)),
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
    """Re-run a saved pipeline WITH THE PER-STAGE CONFIGURATION IT WAS RUN WITH. W508 (P2.8(4)).

    This used to rebuild the stages as `StageConfig(type=s)` from `r["pipeline"]`, which holds the stage TYPES
    and nothing else — so every per-stage `config` the original run carried was silently dropped and the
    "rerun" executed a DIFFERENT pipeline while reporting itself as a rerun of that one. A stage's config
    reaches its prompt ("Configuration: {cfg}"), so dropping it changes the work.

    The config was never lost: `_execute` stores it on each stage output. It simply was not read back. The
    response now states, per stage, whether a config was carried, so a caller can tell a faithful rerun from
    one whose original had none.
    """
    for r in _load():
        if r["run_id"] == run_id:
            # the config as RUN, recovered from the stage outputs rather than from the type list
            #  W805 (FU-823) - BY POSITION: keyed by type, two stages of one type took the last one's configuration
            _outs805 = [o for o in (r.get("stage_outputs") or []) if isinstance(o, dict)]
            _cfgs805 = [((_outs805[i].get("config") or {}) if i < len(_outs805)
                         and str(_outs805[i].get("resource")) == str(sid) else {})
                        for i, sid in enumerate(r["pipeline"])]
            saved_cfg = {str(o.get("resource")): (o.get("config") or {}) for o in _outs805}
            stages = [StageConfig(type=sid, config=_cfgs805[i]) for i, sid in enumerate(r["pipeline"])]
            req = ForgeRunRequest(objective=r["objective"], domain=r["domain"], realm=r["realm"],
                                  stages=stages,
                                  usage_area=r.get("usage_area", "forge"), name=f"{r['name']} (rerun)")
            out = await _execute(req)
            if isinstance(out, dict):
                carried = {}
                for i, sid in enumerate(r["pipeline"]):
                    carried[sid] = carried.get(sid, False) or bool(_cfgs805[i])
                out["rerun_of"] = run_id
                out["config_carried"] = carried
                #  W805 - exact per position, where the map above (kept for its readers) cannot tell two of a type apart
                out["config_carried_by_position"] = [{"position": i + 1, "stage": sid, "carried": bool(_cfgs805[i])}
                                                     for i, sid in enumerate(r["pipeline"])]
                out["rerun_basis"] = (
                    ("every stage was re-run with the configuration the original carried"
                     if all(carried.values()) else
                     ("the original run carried no per-stage configuration, so there was none to carry"
                      if not any(carried.values()) else
                      "the stages whose original carried a configuration were re-run with it; "
                      f"{sum(1 for v in carried.values() if not v)} stage(s) had none")))
            return out
    raise HTTPException(status_code=404, detail=f"Run {run_id} not found.")
