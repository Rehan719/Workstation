"""
Native AI Fabric API — Workstation's OWN AI resources, exposed.

Surfaces the in-house AI control plane (W1): the model-resource registry (owned native
engine + self-hosted local model + optional external accelerants), the orchestrator
(in-house-first completion), and the swarm engine (bespoke, reusable agent-cascade trees).
Everything is honest about which resource served and whether any external provider was used.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agentic_core.ai.native import orchestrator, registry
from agentic_core.ai.native.model_resource import external_allowed

router = APIRouter(prefix="/api/v1/native-ai", tags=["native-ai-fabric"])


@router.get("/status")
async def native_status():
    resources = registry.available()
    owned = [r for r in resources if not r["is_external"] and r["available"]]
    order = registry.select()
    # HONEST active-resolution: the resource that will actually serve the next completion, and whether that
    # is a REAL model (local Ollama / external accelerant) or the deterministic native FLOOR (is_model=False,
    # structured reasoning — not an LLM). Surfaced so the Owner can see, at a glance, exactly what is serving.
    active = order[0] if order else "native"
    is_real_model = active != "native"
    active_row = next((r for r in resources if r["name"] == active), None)
    # §6 (W323) — MEASURED serving mode beside the prediction: the selection head can list a model
    # that keeps failing while the floor actually serves — `mode` now follows what the learning
    # loop MEASURED on the most recent recorded work, never just the optimistic prediction.
    measured = None
    _last_at = None
    try:
        from agentic_core.api.operational_excellence import model_health
        _rows = [(k, v) for k, v in (model_health() or {}).items()
                 if v.get("window_runs", 0) > 0 and v.get("last_at")]
        if _rows:
            _rows.sort(key=lambda kv: kv[1].get("last_at", ""), reverse=True)
            measured = _rows[0][0]
            _last_at = _rows[0][1].get("last_at")
    except Exception:
        pass
    mode_predicted = "real_model" if is_real_model else "deterministic_floor"
    mode_measured = ("unmeasured" if measured is None
                     else ("deterministic_floor" if measured == "native" else "real_model"))
    return {
        "posture": "in-house-first",
        "external_allowed": external_allowed(),
        "owned_resources_available": [r["name"] for r in owned],
        "selection_order": order,
        "active_model": active,
        "active_model_label": (active_row or {}).get("model", active),
        "is_real_model": is_real_model,
        "mode": mode_measured if mode_measured != "unmeasured" else mode_predicted,
        "mode_predicted": mode_predicted,
        "mode_measured": mode_measured,
        "measured_recent_server": measured,
        "mode_note": ("mode follows the MEASURED most-recent server when history exists "
                      "(prediction only until then) — the two disagree when a listed model keeps failing"),
        # §6 (W424) — `floor_active` is derived from ONE row: the most recent recorded
        # completion. It answers "what served last", NOT "what is serving now", and the old
        # name invited the second reading. The value is unchanged; what it MEASURES is now
        # stated, and the row it was computed from travels with it so the claim is checkable.
        "floor_active": (mode_measured == "deterministic_floor" if mode_measured != "unmeasured"
                         else not is_real_model),
        "floor_active_basis": (
            ("most recent recorded completion was served by " + str(measured)
             + " (one row, at " + str(_last_at) + ") — this is history, not a live probe")
            if measured is not None else
            "no completion has been recorded yet; predicted from whether a real model is listed"),
        "floor_note": (None if is_real_model else
                       "The deterministic native floor is serving — honest structured reasoning, NOT an LLM. "
                       "Run a local Ollama model (or enable an external accelerant) for generative prose."),
        "guarantee": "Workstation always produces a real, structured result from its OWN resources "
                     "with NO external dependency; external providers are optional accelerants "
                     "(flag-gated by AI_ALLOW_EXTERNAL).",
        "resources": resources,
    }


@router.get("/homeostasis")
async def native_homeostasis():
    """§8→§6: the live biomimetic homeostatic posture governing the native AI fabric — how the living
    organism's state (immune · circadian · metabolic ATP · composite health) currently modulates how much
    cognitive work the swarm/tree will admit. Real organism state; cognition also feeds ATP back (closed loop)."""
    from agentic_core.ai.native.homeostasis import homeostasis
    return homeostasis.snapshot()


@router.get("/resources")
async def native_resources():
    return {"resources": registry.available(), "selection_order": registry.select()}


@router.get("/models")
async def native_models():
    """The OWNED model resources, with the local models actually discovered on the Ollama server — each
    selectable by name (model='ollama:<name>'). The native deterministic floor is always available."""
    from agentic_core.ai.native.model_resource import local_models
    discovered = local_models()
    tiers = [{"id": "auto", "label": "Auto (in-house-first)", "kind": "policy"},
             {"id": "native", "label": "Native floor (deterministic)", "kind": "native"}]
    if discovered:
        tiers.append({"id": "local", "label": "Local model (default)", "kind": "local"})
        tiers += [{"id": f"ollama:{m}", "label": m, "kind": "local"} for m in discovered]
    from agentic_core.ai.native.model_resource import effective_default_local, lifecycle_state
    _st = lifecycle_state()
    return {"local_models": discovered,
            "default_local": effective_default_local() if discovered else None,
            "promoted_default": _st.get("default_local"), "retired": _st.get("retired") or [],
            "tiers": tiers,
            "note": "Owned models. Route a completion to any with model=<id>. External providers are opt-in "
                    "accelerants (AI_ALLOW_EXTERNAL); the native floor is always available."}


# ── Owned-model LIFECYCLE (W276) — evaluate · promote · retire · reinstate ──────────────────────
class LifecycleModelRequest(BaseModel):
    model: str


def _ueg_lifecycle(action: str, model: str, extra: Dict[str, Any] | None = None) -> None:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": f"native_ai.model.{action}", "model": model, **(extra or {})})
    except Exception:
        pass


@router.get("/lifecycle")
async def model_lifecycle():
    """§6 (W276) — the owned-model estate's lifecycle state: the promoted serving default, retired
    models, the active estate default orchestration draws on, and recent evaluations."""
    from agentic_core.ai.native.model_resource import (lifecycle_state, effective_default_local,
                                                       active_local_models, local_models)
    st = lifecycle_state()
    return {"promoted_default": st.get("default_local"),
            "effective_default": effective_default_local(),
            "retired": st.get("retired") or [],
            "discovered": local_models(), "active_estate": active_local_models(),
            "evaluations": (st.get("evaluations") or [])[-10:]}


@router.post("/lifecycle/evaluate")
async def evaluate_model(req: LifecycleModelRequest):
    """§6 (W276) — run a bounded, HONEST evaluation of a named local model: three small probes
    routed explicitly to it. Scored only on what genuinely happened (did the target actually
    serve · non-empty output · requested structure present · latency); when the model cannot
    serve, that is the result — never a fabricated score. Attempts feed the W275 health window."""
    import time as _t
    probes = [
        ("structure", "Reply with exactly two sections:\n## Summary\n## Risks\nTopic: a halal "
                      "meal-kit venture.", "## Risks"),
        ("instruction", "List exactly three bullet points, each under 10 words, on safe data "
                        "handling.", "-"),
        ("reasoning", "A VSB earns 100 WST and its costs are 40 WST. State the surplus and ONE "
                      "prudent use for it.\n## Answer", "60"),
    ]
    results = []
    served_target = 0
    for pid, prompt, marker in probes:
        _p0 = _t.time()
        r = await orchestrator.complete(prompt, agent=f"eval:{req.model}",
                                        prefer=f"ollama:{req.model}", timeout=20.0)
        on_target = r.get("served_by") == f"ollama:{req.model}"
        served_target += 1 if on_target else 0
        results.append({"probe": pid, "served_by": r.get("served_by"), "on_target": on_target,
                        "non_empty": bool((r.get("output") or "").strip()),
                        "structure_hit": marker.lower() in (r.get("output") or "").lower(),
                        "ms": int((_t.time() - _p0) * 1000)})
    can_serve = served_target == len(probes)
    score = (round(sum(1.0 for x in results if x["structure_hit"]) / len(results), 2)
             if can_serve else None)   # honest: no score when the target never served
    from agentic_core.ai.native.model_resource import lifecycle_state, save_lifecycle
    st = lifecycle_state()
    evaluation = {"model": req.model, "can_serve": can_serve, "score": score,
                  "probes": results, "at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                       __import__("time").gmtime())}
    st["evaluations"].append(evaluation)
    save_lifecycle(st)
    _ueg_lifecycle("evaluated", req.model, {"can_serve": can_serve, "score": score})
    return evaluation


@router.post("/lifecycle/promote")
async def promote_model(req: LifecycleModelRequest):
    """§6 (W276) — promote a DISCOVERED local model to the persisted serving default (the 'ollama'
    resource + gateway serve with it; env OLLAMA_MODEL becomes the fallback). Honest: promoting an
    undiscovered model is refused, not pretended."""
    from fastapi import HTTPException
    from agentic_core.ai.native.model_resource import local_models, lifecycle_state, save_lifecycle
    if req.model not in local_models():
        raise HTTPException(status_code=409, detail=f"Model '{req.model}' is not discovered on the "
                            "local server — pull it first; promotion never pretends.")
    st = lifecycle_state()
    st["default_local"] = req.model
    st["retired"] = [m for m in (st.get("retired") or []) if m != req.model]
    save_lifecycle(st)
    _ueg_lifecycle("promoted", req.model)
    return {"promoted": req.model, "effective_default": req.model}


@router.post("/lifecycle/retire")
async def retire_model(req: LifecycleModelRequest):
    """§6 (W276) — retire a local model from the ACTIVE estate: default orchestration (ensemble,
    'ollama' default routing) stops drawing on it; explicit ollama:<name> routing remains the
    user's explicit choice. Reversible via /lifecycle/reinstate."""
    from agentic_core.ai.native.model_resource import lifecycle_state, save_lifecycle
    st = lifecycle_state()
    if req.model not in (st.get("retired") or []):
        st["retired"].append(req.model)
    if st.get("default_local") == req.model:
        st["default_local"] = None            # a retired model cannot stay the promoted default
    save_lifecycle(st)
    _ueg_lifecycle("retired", req.model)
    return {"retired": st["retired"], "promoted_default": st.get("default_local")}


@router.post("/lifecycle/reinstate")
async def reinstate_model(req: LifecycleModelRequest):
    """§6 (W276) — return a retired model to the active estate."""
    from agentic_core.ai.native.model_resource import lifecycle_state, save_lifecycle
    st = lifecycle_state()
    st["retired"] = [m for m in (st.get("retired") or []) if m != req.model]
    save_lifecycle(st)
    _ueg_lifecycle("reinstated", req.model)
    return {"retired": st["retired"]}


# Catalogue of Workstation's OWN AI capabilities — each backed by a REAL, integrated agentic_core module
# (the integration sweep; see docs/AGENTIC_CORE_INTEGRATION_AUDIT.md). Discoverability for the fabric.
_CAPABILITIES = [
    {"name": "Workflow tree", "endpoint": "POST /api/v1/native-ai/tree", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "Autonomously decompose a goal into a dependency DAG and run it in-house-first with parallel branches, biomimetically governed + logged."},
    {"name": "Agent swarm cascade", "endpoint": "POST /api/v1/native-ai/swarm", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "Run a bespoke linear agent-cascade over owned resources."},
    {"name": "In-house completion", "endpoint": "POST /api/v1/native-ai/complete", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "In-house-first completion with health-based resource selection + the always-available native floor."},
    {"name": "Minimax decision", "endpoint": "POST /api/v1/native-ai/decide", "kind": "decision",
     "source": "cognition.minimax_optimizer", "in_house": True,
     "description": "Maximin over caller-supplied per-action utilities under worst-case stressors; without action_utilities every action ties and NO winner is invented."},
    {"name": "Validation", "endpoint": "POST /api/v1/native-ai/validate", "kind": "validation",
     "source": "validation.accuracy_validator", "in_house": True,
     "description": "Real difflib semantic-similarity / numerical-tolerance / code-presence checks against a reference."},
    {"name": "Statistical rigor", "endpoint": "POST /api/v1/native-ai/rigor", "kind": "analysis",
     "source": "statistics.live_rigor_monitor", "in_house": True,
     "description": "Real scipy 95% CI + one-sample t-test over an accumulated metric series — reports n, and returns null (with the reason) when the data cannot support a test."},
    {"name": "Swarm consensus", "endpoint": "POST /api/v1/native-ai/consensus", "kind": "swarm",
     "source": "swarm.conflict_resolution", "in_house": True,
     "description": "Real threshold vote-tally — the STRONGEST clearing choice wins, ties are disclosed, and the tally travels with the verdict."},
    {"name": "Signal transduction", "endpoint": "POST /api/v1/native-ai/transduce", "kind": "biomimetic",
     "source": "signaling.empirical_transduction", "in_house": True,
     "description": "Hill saturation transform (K50=0.5) — where a signal sits on a sigmoidal dose-response curve. Nothing is timed; supra-threshold means input ≥ K50."},
    {"name": "Quorum threshold", "endpoint": "POST /api/v1/native-ai/quorum", "kind": "biomimetic",
     "source": "quorum.sensing", "in_house": True,
     "description": "Threshold model over the platform's defined agent catalog (or a supplied population, echoed as such) — arithmetic density × threshold, not an observation of behaviour."},
    {"name": "Intent inference", "endpoint": "POST /api/v1/native-ai/intent", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real regex keyword-pattern intent classification (deterministic, not LLM)."},
    {"name": "Entailment", "endpoint": "POST /api/v1/native-ai/entailment", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real word-overlap natural-language inference (ENTAILED / PARTIAL / NEUTRAL)."},
    {"name": "Seed derivation", "endpoint": "POST /api/v1/native-ai/entropy", "kind": "crypto",
     "source": "crypto.entropy_pool", "in_house": True,
     "description": "SHA3-512 + XOR deterministic seed derivation over caller-supplied metadata — reproducible seeding; reads NO system entropy, never for keys/nonces/tokens."},
    {"name": "Graph topology", "endpoint": "POST /api/v1/native-ai/topology", "kind": "topology",
     "source": "topology.defense", "in_house": True,
     "description": "Real Betti numbers — β₀ components (union-find) + β₁ cycles over APPLIED edges; discarded edges and the β₁ threshold are disclosed in the payload."},
    {"name": "VBS governance", "endpoint": "POST /api/v1/vbs/*", "kind": "governance",
     "source": "vbs", "in_house": True,
     "description": "Real QMS quality gates + DCMS SHA3-512 versioning + BMS unit-economics + EMS + Mycelial backbone."},
    {"name": "UEG provenance", "endpoint": "GET /api/v1/ueg/verify", "kind": "provenance",
     "source": "ueg.logger", "in_house": True,
     "description": "Real hash-chained SHA3-512 Merkle-DAG audit ledger with full-chain verify_chain()."},
    {"name": "Degradation detection", "endpoint": "GET /api/v1/operations/degradation", "kind": "analysis",
     "source": "self_improvement.degradation_detector", "in_house": True,
     "description": "Real telemetry degradation detection (latency rise / accuracy drop) over the learning loop."},
]


@router.get("/capabilities")
async def native_capabilities():
    """Catalogue of Workstation's OWN AI capabilities — each backed by a REAL, integrated agentic_core
    module (no external dependency). The fabric's breadth, discoverable."""
    return {"posture": "in-house-first", "count": len(_CAPABILITIES),
            "note": "Every capability is backed by a real, integrated agentic_core module — see "
                    "docs/AGENTIC_CORE_INTEGRATION_AUDIT.md for the full real-vs-mock sweep.",
            "capabilities": _CAPABILITIES}


@router.get("/selfcheck")
async def native_selfcheck():
    """Fabric integrity check: actually IMPORT each integrated capability's source module and report
    which are live. Guards the whole integration arc — if any owned capability's backing module breaks,
    this flips all_live to false (honest, real import probe — not a static claim)."""
    import importlib
    sources = sorted({c["source"] for c in _CAPABILITIES})
    modules = []
    for src in sources:
        try:
            importlib.import_module(f"agentic_core.{src}")
            modules.append({"source": src, "live": True})
        except Exception as e:
            modules.append({"source": src, "live": False, "error": type(e).__name__})
    live = sum(1 for m in modules if m["live"])
    return {"posture": "in-house-first", "total": len(modules), "live": live,
            "all_live": live == len(modules), "modules": modules}


class CompleteRequest(BaseModel):
    prompt: str
    agent: str = "assistant"
    prefer_external: bool = False
    timeout: float = 30.0
    model: str = "auto"   # §6 model-tier preference: auto | native (force floor) | local (require Ollama)


class EnsembleRequest(BaseModel):
    prompt: str
    agent: str = "ensemble"
    models: List[str] = []      # tier ids (e.g. ["ollama:llama3.2","ollama:llama2","native"]); empty = all owned
    synthesize: bool = True


@router.post("/ensemble")
async def native_ensemble(req: EnsembleRequest):
    """§6 — run a prompt across MULTIPLE owned models in parallel, then synthesise a consensus. Owned
    orchestration as a composable resource; every member reports which owned resource served it."""
    return await orchestrator.ensemble(req.prompt, agent=req.agent,
                                       models=req.models or None, synthesize=req.synthesize)


@router.post("/complete")
async def native_complete(req: CompleteRequest):
    res = await orchestrator.complete(req.prompt, agent=req.agent, timeout=req.timeout,
                                      prefer_external=req.prefer_external, prefer=req.model)
    return res


class SwarmStage(BaseModel):
    role: str
    instruction: str


class SwarmRequest(BaseModel):
    agent: str = "swarm"
    context: str = ""
    prefer_external: bool = False
    stages: List[SwarmStage] = []


@router.post("/swarm")
async def native_swarm(req: SwarmRequest):
    stages: List[Dict[str, str]] = [{"role": s.role, "instruction": s.instruction} for s in req.stages]
    if not stages:
        stages = [
            {"role": "analyst", "instruction": "Analyse the objective and key factors."},
            {"role": "designer", "instruction": "Design the approach from the analysis."},
            {"role": "synthesiser", "instruction": "Synthesise the final recommendation."},
        ]
    res = await orchestrator.swarm(req.agent, stages, context=req.context, prefer_external=req.prefer_external)
    return res


class TreeRequest(BaseModel):
    goal: str
    context: str = ""
    max_parallel: int = 4
    prefer_external: bool = False
    timeout: float = 30.0


class TransduceRequest(BaseModel):
    input_signal: float = Field(ge=0.0, allow_inf_nan=False)   # a Hill transform of a negative concentration has no referent
    hill: float = Field(default=4.5, gt=0.0, le=100.0, allow_inf_nan=False)
    include_curve: bool = False


@router.post("/transduce")
async def native_transduce(req: TransduceRequest):
    """Owned Hill saturation transform (agentic_core/signaling): where a signal sits on a sigmoidal
    dose-response curve — activation = s^h / (K50^h + s^h), K50 = 0.5, disclosed in the payload.

    W437 — this endpoint used to report `latency_s` (nothing was timed — a constant formula wearing
    a unit) and echo a `frequency` parameter that provably never entered the result, under the method
    string "Hill-equation pulsatile cascade". Both are DELETED, not renamed; `propagated` became
    `supra_threshold`, stated for what it is (input_signal >= K50), and the basis travels with it."""
    from agentic_core.signaling.empirical_transduction import EmpiricalSignalTransduction
    r = EmpiricalSignalTransduction(hill=req.hill).transform(req.input_signal)
    out = {"input_signal": req.input_signal, "activation": r["activation"],
           "supra_threshold": r["supra_threshold"], "k50": r["k50"], "hill": r["hill"],
           "basis": r["basis"], "method": "Hill saturation transform (owned signaling)"}
    if req.include_curve:
        out["dose_response"] = r["dose_response"]
        out["dose_response_domain"] = r["dose_response_domain"]
    return out


class TopologyRequest(BaseModel):
    nodes: List[Any] = []
    edges: List[Any] = []     # each edge: [u, v] (or {source, target})


@router.post("/topology")
async def native_topology(req: TopologyRequest):
    """Owned graph-topology analysis (agentic_core/topology.TopologyDefense): REAL Betti numbers of the
    1-complex — β₀ = connected components (union-find), β₁ = E−V+β₀ = independent cycles, computed over
    the edges the union-find actually APPLIED. A tree → β₁=0; a cycle → β₁≥1; disconnection raises β₀.

    W437 — β₁ used to count the RAW edge list while validation quietly discarded malformed/dangling
    edges (junk edges reported as "structural holes"), and "SPIKE_DETECTED" asserted a temporal rise
    against a baseline that never existed, using an undisclosed 3.0 cutoff that ignored β₀ entirely.
    Now the discard is disclosed, the threshold is in the payload, and the verdict fields say only
    what one measurement can say: fragmented (β₀>1) and beta1_over_threshold."""
    from agentic_core.topology.defense import TopologyDefense
    res = await TopologyDefense().compute_persistent_homology({"nodes": req.nodes, "edges": req.edges})
    return {"beta0_components": res["beta0"], "beta1_cycles": res["beta1"],
            "fragmented": res["fragmented"], "beta1_threshold": res["beta1_threshold"],
            "beta1_over_threshold": res["beta1_over_threshold"],
            "nodes_submitted": res["nodes_submitted"], "nodes_distinct": res["nodes_distinct"],
            "nodes_discarded": res["nodes_discarded"], "edges_submitted": res["edges_submitted"],
            "edges_applied": res["edges_applied"], "edges_discarded": res["edges_discarded"],
            "basis": res["basis"],
            "method": "graph Betti numbers via Euler characteristic (owned topology)"}


class EntropyRequest(BaseModel):
    sources: List[Dict[str, Any]] = []   # each: {size, source, content_hash, timestamp}


@router.post("/entropy")
async def native_entropy(req: EntropyRequest):
    """Owned deterministic seed derivation (agentic_core/crypto.EntropyPool): SHA3-512 + XOR mixing over
    the caller-supplied source metadata — same sources (fixed timestamps) ⇒ same seed, which is the
    point: reproducible in-house seeding. NO system entropy is read anywhere.

    W437 — this endpoint used to report `bits_harvested` (a fixed +128 per source that never examined
    a byte — five empty dicts "harvested" 640 bits into a 512-bit register) and a `pool_integrity`
    digest that was byte-identical to the seed, so it could never disagree with the value it claimed
    to attest. The counter is now what it always was (mixing_rounds), the digest is a disjoint slice
    of the pool hash, and the response says plainly what this seed must never be used for."""
    from agentic_core.crypto.entropy_pool import EntropyPool
    pool = EntropyPool()
    for s in req.sources:
        pool.add_entropy(s)
    return {"seed": pool.get_seed(), "mixing_rounds": pool.mixing_rounds,
            "pool_digest": pool.pool_digest(), "sources_mixed": len(req.sources),
            "algo": "sha3_512 + XOR mixing", "method": "deterministic seed derivation (owned crypto)",
            "basis": ("deterministic derivation over caller-supplied metadata; no system, hardware or "
                      "physical entropy is read — do NOT use this seed as a key, nonce, or token"
                      + ("; no sources were supplied, so this is the fixed genesis-constant seed "
                         "(identical in every deployment)" if not req.sources else "")
                      + (f"; {pool.timestamps_defaulted} source(s) carried no timestamp — a fixed 0 "
                         f"was used for each (the derivation stays deterministic)"
                         if pool.timestamps_defaulted else ""))}


class QuorumRequest(BaseModel):
    agents: int | None = Field(default=None, ge=0, le=1_000_000_000)   # None → the platform's agent catalog is counted
    secretion: float = Field(default=10.0, ge=0.0, allow_inf_nan=False)   # AI-2 analog secreted per agent
    threshold: float = Field(default=50.0, gt=0.0, allow_inf_nan=False)


@router.post("/quorum")
async def native_quorum(req: QuorumRequest):
    """Owned quorum threshold model (agentic_core/quorum.QuorumSensing) over the platform's defined
    agent catalog — or an explicitly supplied population, echoed as such.

    W437 — this endpoint claimed "sensing", a "shared field" and "real threshold kinetics" while
    computing agents × secretion > threshold over numbers the caller typed in. It also rounded the
    reported concentration but compared the unrounded one, so a payload could display
    50.0 > 50.0 = true. Now the population defaults to the platform's agent catalog with
    population_source disclosing which was used — and the refuter pass corrected the first version
    of this fix, which called that catalog "live_roster": _AGENTS is a static definition that never
    changes at runtime, and naming a constant a live observation is the same defect class. The
    reported concentration is the exact product the verdict derives from (a single multiplication,
    not a float-summing loop the basis would misdescribe as ×)."""
    from agentic_core.quorum.sensing import QuorumSensing
    from agentic_core.api.swarm import _AGENTS
    if req.agents is None:
        population, source, source_desc = len(_AGENTS), "agent_catalog", \
            "the platform's defined agent catalog — a static definition, not a runtime observation"
    else:
        population, source, source_desc = req.agents, "caller_supplied", "caller-supplied population"
    q = QuorumSensing("swarm", threshold=req.threshold)
    q.secrete_ai2(population * req.secretion)
    concentration = q.ai2_concentration   # exact — the verdict below derives from THIS value
    mode = q.get_behavior_mode()
    return {"agents": population, "population_source": source,
            "concentration": concentration, "threshold": req.threshold,
            "behavior_mode": mode, "cooperative": mode == "COOPERATIVE",
            "basis": (f"{population} agents ({source_desc}) × secretion {req.secretion} = "
                      f"{concentration} vs threshold {req.threshold} — an arithmetic threshold "
                      f"check, not an observation of live behaviour"),
            "method": "quorum threshold model (owned biomimetic swarm)"}


class IntentRequest(BaseModel):
    text: str


@router.post("/intent")
async def native_intent(req: IntentRequest):
    """Owned NLP intent inference (agentic_core/nlp.NLIEngine): REAL regex keyword-pattern scoring over
    the text — deterministic, not LLM. Returns the best intent + confidence + all per-intent scores."""
    from agentic_core.nlp.nli_engine import NLIEngine
    return NLIEngine().infer_intent(req.text)


class EntailmentRequest(BaseModel):
    premise: str
    hypothesis: str


@router.post("/entailment")
async def native_entailment(req: EntailmentRequest):
    """Owned NLP entailment (agentic_core/nlp.NLIEngine) — LEXICAL word-overlap inference.

    W431: returns the deciding number and the limits of the method, not a bare verdict. It used to
    report ENTAILED for "The sky is not blue" -> "The sky is blue", because a negator sits in the
    PREMISE and overlap only counts hypothesis tokens found there. Asymmetric negation now yields
    CONTRADICTION — the label this docstring always promised and the code never returned.
    ENTAILED | PARTIAL_ENTAILMENT | NEUTRAL | CONTRADICTION | UNDECIDABLE. Deterministic, and
    lexical: it does not read word order, quantifiers, or role inversion."""
    from agentic_core.nlp.nli_engine import NLIEngine
    detail = NLIEngine().entailment_detail(req.premise, req.hypothesis)
    # The ratio and the limits travel WITH the verdict: a label that makes a logical claim on lexical
    # evidence must show the evidence, or the caller has no way to judge it.
    return {"premise": req.premise, "hypothesis": req.hypothesis, **detail}


class Vote(BaseModel):
    voter: str
    choice: str


class ConsensusRequest(BaseModel):
    proposal_id: str = "proposal"
    votes: List[Vote] = []
    total_nodes: int = Field(default=0, ge=0)     # 0 → use the number of DISTINCT voters
    threshold: float = Field(default=0.66, gt=0.0, le=1.0)   # W437: was unbounded — -1.0 "reached consensus"


@router.post("/consensus")
async def native_consensus(req: ConsensusRequest):
    """Owned swarm consensus (agentic_core/swarm.ConsensusEngine): REAL threshold vote-tally — the
    STRONGEST choice clearing the threshold wins; an exact top tie is disclosed, never resolved by
    input order (W431). The tally, shares and basis travel with the verdict so a caller can check it.

    W437 — the W431 engine fix existed but this handler still called the old single-value path,
    dropping the tally/tie/basis it computes; total_nodes still counted the RAW ballot list although
    votes are keyed by voter and later ballots overwrite earlier ones (three entries from one voter
    reported as a 3-vote ballot); and threshold accepted any float — -1.0 returned a "reached"
    consensus that is meaningless by construction. All three closed."""
    from agentic_core.swarm.conflict_resolution import ConsensusEngine
    ce = ConsensusEngine(threshold=req.threshold)
    for v in req.votes:
        ce.record_vote(req.proposal_id, v.voter, v.choice)
    distinct = len(ce.votes.get(req.proposal_id) or {})
    total = req.total_nodes or distinct
    detail = ce.consensus_detail(req.proposal_id, total)
    return {"reached": detail["reached"], "choice": detail["choice"], "tied": detail["tied"],
            "tied_choices": detail["tied_choices"], "tally": detail["tally"],
            "shares": detail["shares"], "threshold": req.threshold,
            "total_nodes": total, "ballots_submitted": len(req.votes),
            "distinct_voters": detail["distinct_voters"], "basis": detail["basis"],
            "method": "threshold consensus (owned swarm)"}


class RigorRequest(BaseModel):
    metric_name: str
    # W437: NaN/inf observations are refused at the door — a NaN used to reach scipy, compare
    # False as "not significant", get sealed into the UEG chain, and then 500 the response
    value: float = Field(allow_inf_nan=False)
    baseline: float = Field(default=0.0, allow_inf_nan=False)


# Shared statistical-rigor monitor — real scipy CI + t-tests over a live metric series; logs each
# validation to the owned UEG provenance chain. Stateful (accumulates per-metric history) by design.
def _rigor_monitor():
    from agentic_core.statistics.live_rigor_monitor import LiveRigorMonitor
    from agentic_core.ueg.registry import ueg_ledger
    global _RIGOR
    try:
        return _RIGOR
    except NameError:
        _RIGOR = LiveRigorMonitor(ueg=ueg_ledger)
        return _RIGOR


@router.post("/rigor")
async def native_rigor(req: RigorRequest):
    """Owned statistical-rigor capability (agentic_core/statistics.LiveRigorMonitor): REAL scipy 95%
    t-interval CI + one-sample t-test over the accumulated per-metric series. Tri-state and honest:
    when the test could not run (n<3, or zero variance), p_value and significant are null with the
    reason in `basis` — never a fabricated 1.0.

    W437 — the old response carried `power` (a call counter: n/100 + 0.5, no power analysis existed)
    whose gate froze `significant` at false for 29 calls regardless of evidence — a live p-value of
    1.5e-24 was reported "not significant". First calls returned p_value 1.0 and a zero-width CI that
    were never computed, and a zero-variance series 500'd AFTER sealing a NaN into the UEG chain."""
    res = await _rigor_monitor().validate_metric(req.metric_name, req.value, req.baseline)
    return {"metric": res["metric"], "value": res["value"], "baseline": res["baseline"],
            "n": res["n"],
            "ci_95": list(res["ci_95"]) if res["ci_95"] is not None else None,
            "p_value": res["p_value"], "significant": res["significant"], "basis": res["basis"],
            "method": "scipy t-interval CI + one-sample t-test (owned statistics)"}


class ValidateRequest(BaseModel):
    prediction: Any
    actual: Any
    # W437: a validated enum — an unknown value used to fall silently into the equality branch while
    # the hardcoded method string claimed difflib ran
    task_type: Literal["SEMANTIC", "NUMERICAL", "APP_CODE", "GENERIC"] = "SEMANTIC"


_VALIDATE_METHODS = {
    "SEMANTIC": "difflib SequenceMatcher ratio vs 0.8 (owned validation)",
    "NUMERICAL": "absolute error vs 1% tolerance (owned validation)",
    "APP_CODE": "syntax-token presence check — not a correctness measure (owned validation)",
    "GENERIC": "exact equality — binary, no confidence gradient (owned validation)",
}


@router.post("/validate")
async def native_validate(req: ValidateRequest):
    """Owned validation capability (agentic_core/validation.AccuracyValidator): reference comparison
    per task type, with the confidence basis travelling alongside — not LLM self-grading.

    W437 — the W432 engine fix (confidence: null where nothing computes one, with confidence_basis)
    existed but THIS handler still cast `float(confidence)`, which 500'd on every GENERIC/APP_CODE
    call, dropped the basis, and stamped one hardcoded "(difflib, real)" method string on all four
    branches. The method now names the branch that actually ran."""
    from agentic_core.validation.accuracy_validator import AccuracyValidator
    res = AccuracyValidator().validate_output(req.prediction, req.actual, task_type=req.task_type)
    return {"is_accurate": bool(res["is_accurate"]),
            "confidence": (None if res["confidence"] is None else float(res["confidence"])),
            "confidence_basis": res["confidence_basis"], "task_type": res["task_type"],
            "method": _VALIDATE_METHODS[req.task_type]}


class DecideRequest(BaseModel):
    state: Dict[str, Any] = {}
    actions: List[str] = []
    # W437: the only way this endpoint can genuinely decide. The default utility never reads the
    # action, so without per-action utilities every 2+ action call ties — disclosed, never invented.
    action_utilities: Dict[str, float] | None = None


@router.post("/decide")
async def native_decide(req: DecideRequest):
    """In-house minimax (maximin) over candidate actions under worst-case stressors — the OWNED
    cognition capability (agentic_core/cognition).

    W437 refuter catch on the W431 fix: the tie disclosure was honest but made the endpoint a
    PERMANENT refusal — the default utility ignores the action, so no reachable input could ever
    discriminate, while the docstring advertised "when no custom utility is provided" for a
    parameter that did not exist. `action_utilities` now exists: supply a base utility per action
    and the maximin genuinely ranks them; omit it and the all-tie refusal stands, stated as such."""
    from agentic_core.cognition.minimax_optimizer import MinimaxOptimizer, default_utility_func
    actions = req.actions or ["proceed", "refine", "hold"]
    state = req.state or {"base_stability": 0.9}
    if req.action_utilities is not None:
        missing = [a for a in actions if a not in req.action_utilities]
        if missing:
            raise HTTPException(status_code=422,
                                detail=f"action_utilities must cover every action; missing: {missing} "
                                       f"(a partial table would silently hand missing actions a default)")
        au = dict(req.action_utilities)

        def _utility(state_: Dict[str, Any], action: str, stressor: str) -> float:
            base = float(au[action])
            if stressor == "hypoxia":
                base -= 0.3
            if stressor == "high_load":
                base -= 0.1
            return max(0.0, base)

        util, util_source = _utility, "caller-supplied per-action utilities"
    else:
        util, util_source = default_utility_func, (
            "default survival utility — it does NOT read the action, so with 2+ actions every "
            "candidate ties and no winner is invented; supply action_utilities to rank")
    res = MinimaxOptimizer().evaluate_strategy(state, actions, util)
    return {"posture": "in-house", "method": "minimax adversarial (owned cognition)",
            "actions": actions, "utility_source": util_source,
            "stressor_note": ("two of the four stressors subtract nothing, so the binding worst case "
                              "is always hypoxia (−0.3); stressors shift all actions equally and never "
                              "change the ranking"),
            **res}


@router.post("/tree")
async def native_tree(req: TreeRequest):
    """Autonomous workflow-TREE orchestration: the native swarm decomposes the goal into a dependency
    tree and runs it in-house-first with PARALLEL branches — the living-organism cascade (immune-throttled
    parallelism + biobus signals + learning loop). Every node reports the OWNED resource that served it."""
    return await orchestrator.orchestrate_tree(
        req.goal, context=req.context, max_parallel=req.max_parallel,
        prefer_external=req.prefer_external, timeout=req.timeout)
