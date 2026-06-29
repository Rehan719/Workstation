"""
Native AI Fabric API — Workstation's OWN AI resources, exposed.

Surfaces the in-house AI control plane (W1): the model-resource registry (owned native
engine + self-hosted local model + optional external accelerants), the orchestrator
(in-house-first completion), and the swarm engine (bespoke, reusable agent-cascade trees).
Everything is honest about which resource served and whether any external provider was used.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

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
    return {
        "posture": "in-house-first",
        "external_allowed": external_allowed(),
        "owned_resources_available": [r["name"] for r in owned],
        "selection_order": order,
        "active_model": active,
        "active_model_label": (active_row or {}).get("model", active),
        "is_real_model": is_real_model,
        "mode": "real_model" if is_real_model else "deterministic_floor",
        "floor_active": not is_real_model,
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
    return {"local_models": discovered, "default_local": os.getenv("OLLAMA_MODEL", "llama3.2") if discovered else None,
            "tiers": tiers,
            "note": "Owned models. Route a completion to any with model=<id>. External providers are opt-in "
                    "accelerants (AI_ALLOW_EXTERNAL); the native floor is always available."}


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
     "description": "Real maximin game-theory decision over actions under worst-case stressors."},
    {"name": "Validation", "endpoint": "POST /api/v1/native-ai/validate", "kind": "validation",
     "source": "validation.accuracy_validator", "in_house": True,
     "description": "Real difflib semantic-similarity / numerical-tolerance / code-presence checks against a reference."},
    {"name": "Statistical rigor", "endpoint": "POST /api/v1/native-ai/rigor", "kind": "analysis",
     "source": "statistics.live_rigor_monitor", "in_house": True,
     "description": "Real scipy 95% CI + one-sample t-test + power-gated significance over a live metric series."},
    {"name": "Swarm consensus", "endpoint": "POST /api/v1/native-ai/consensus", "kind": "swarm",
     "source": "swarm.conflict_resolution", "in_house": True,
     "description": "Real threshold vote-tally — a choice wins once its share crosses the threshold."},
    {"name": "Signal transduction", "endpoint": "POST /api/v1/native-ai/transduce", "kind": "biomimetic",
     "source": "signaling.empirical_transduction", "in_house": True,
     "description": "Real Hill-equation sigmoidal cascade — does a signal propagate supra-threshold? (with latency kinetics)."},
    {"name": "Quorum sensing", "endpoint": "POST /api/v1/native-ai/quorum", "kind": "biomimetic",
     "source": "quorum.sensing", "in_house": True,
     "description": "Real bacterial-style AI-2 density model — the swarm flips COOPERATIVE/INDEPENDENT at a population threshold."},
    {"name": "Intent inference", "endpoint": "POST /api/v1/native-ai/intent", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real regex keyword-pattern intent classification (deterministic, not LLM)."},
    {"name": "Entailment", "endpoint": "POST /api/v1/native-ai/entailment", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real word-overlap natural-language inference (ENTAILED / PARTIAL / NEUTRAL)."},
    {"name": "Entropy pool", "endpoint": "POST /api/v1/native-ai/entropy", "kind": "crypto",
     "source": "crypto.entropy_pool", "in_house": True,
     "description": "Real SHA3-512 + XOR entropy mixing → a deterministic seed for reproducible in-house seeding."},
    {"name": "Graph topology", "endpoint": "POST /api/v1/native-ai/topology", "kind": "topology",
     "source": "topology.defense", "in_house": True,
     "description": "Real Betti numbers of a graph — β₀ components (union-find) + β₁ cycles ('structural holes'); detects fractures."},
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
    input_signal: float
    frequency: float = 0.5
    hill: float = 4.5
    include_trajectory: bool = False


@router.post("/transduce")
async def native_transduce(req: TransduceRequest):
    """Owned biomimetic signal transduction (agentic_core/signaling.EmpiricalSignalTransduction): a REAL
    Hill-equation (sigmoidal) pulsatile cascade — models whether a signal of a given strength propagates
    (peak >= 0.5 ⇒ supra-threshold) and its latency. Real biochemical-kinetics math, not a constant."""
    from agentic_core.signaling.empirical_transduction import EmpiricalSignalTransduction
    r = EmpiricalSignalTransduction(frequency=req.frequency, hill=req.hill).simulate_cascade(req.input_signal)
    out = {"input_signal": req.input_signal, "peak_intensity": float(r["peak_intensity"]),
           "latency_s": float(r["latency"]), "hill": req.hill, "frequency": req.frequency,
           "propagated": bool(r["peak_intensity"] >= 0.5), "trajectory_points": len(r["trajectory"]),
           "method": "Hill-equation pulsatile cascade (owned signaling)"}
    if req.include_trajectory:
        out["trajectory"] = [float(x) for x in r["trajectory"]]
    return out


class TopologyRequest(BaseModel):
    nodes: List[Any] = []
    edges: List[Any] = []     # each edge: [u, v] (or {source, target})


@router.post("/topology")
async def native_topology(req: TopologyRequest):
    """Owned graph-topology analysis (agentic_core/topology.TopologyDefense): REAL Betti numbers of the
    1-complex — β₀ = connected components (union-find), β₁ = E−V+β₀ = independent cycles ('structural
    holes'). A tree → β₁=0; a cycle → β₁≥1; a fracture (disconnection) raises β₀. Real graph math."""
    from agentic_core.topology.defense import TopologyDefense
    res = await TopologyDefense().compute_persistent_homology({"nodes": req.nodes, "edges": req.edges})
    return {"beta0_components": res["beta0"], "beta1_cycles": res["beta1"], "status": res["status"],
            "nodes": len(req.nodes), "edges": len(req.edges),
            "method": "graph Betti numbers via Euler characteristic (owned topology)"}


class EntropyRequest(BaseModel):
    sources: List[Dict[str, Any]] = []   # each: {size, source, content_hash, timestamp}


@router.post("/entropy")
async def native_entropy(req: EntropyRequest):
    """Owned entropy pool (agentic_core/crypto.EntropyPool): REAL SHA3-512 + XOR entropy mixing over the
    provided sources, yielding a deterministic 64-bit seed + a pool-integrity digest. Real crypto, not a
    PRNG call — same sources (fixed timestamps) ⇒ same seed (reproducible in-house seeding)."""
    from agentic_core.crypto.entropy_pool import EntropyPool
    pool = EntropyPool()
    for s in req.sources:
        pool.add_entropy(s)
    return {"seed": pool.get_seed(), "bits_harvested": pool.total_bits_harvested,
            "pool_integrity": pool.get_status()["pool_integrity"], "sources_mixed": len(req.sources),
            "algo": "sha3_512 + XOR mixing", "method": "entropy pool (owned crypto)"}


class QuorumRequest(BaseModel):
    agents: int = 1            # number of agents currently signalling into the shared field
    secretion: float = 10.0    # AI-2 analog secreted per agent
    threshold: float = 50.0


@router.post("/quorum")
async def native_quorum(req: QuorumRequest):
    """Owned biomimetic swarm quorum sensing (agentic_core/quorum.QuorumSensing): REAL bacterial-style
    AI-2 density model — N agents secrete into a shared field; the swarm flips to COOPERATIVE once the
    aggregate concentration crosses the threshold, else stays INDEPENDENT. Real threshold kinetics."""
    from agentic_core.quorum.sensing import QuorumSensing
    q = QuorumSensing("swarm", threshold=req.threshold)
    for _ in range(max(0, int(req.agents))):
        q.secrete_ai2(req.secretion)
    mode = q.get_behavior_mode()
    return {"agents": req.agents, "concentration": round(q.ai2_concentration, 2), "threshold": req.threshold,
            "behavior_mode": mode, "cooperative": mode == "COOPERATIVE",
            "method": "quorum sensing (owned biomimetic swarm)"}


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
    """Owned NLP entailment (agentic_core/nlp.NLIEngine): REAL word-overlap natural-language inference —
    does the premise entail the hypothesis? ENTAILED | PARTIAL_ENTAILMENT | NEUTRAL. Deterministic."""
    from agentic_core.nlp.nli_engine import NLIEngine
    label = NLIEngine().verify_premise_entailment(req.premise, req.hypothesis)
    return {"premise": req.premise, "hypothesis": req.hypothesis, "label": label,
            "method": "word-overlap NLI (owned nlp)"}


class Vote(BaseModel):
    voter: str
    choice: str


class ConsensusRequest(BaseModel):
    proposal_id: str = "proposal"
    votes: List[Vote] = []
    total_nodes: int = 0          # 0 → use the number of votes cast
    threshold: float = 0.66


@router.post("/consensus")
async def native_consensus(req: ConsensusRequest):
    """Owned swarm consensus (agentic_core/swarm.ConsensusEngine): REAL threshold vote-tally over swarm
    members — a choice wins when its share of total_nodes ≥ threshold, else no consensus. Not LLM."""
    from agentic_core.swarm.conflict_resolution import ConsensusEngine
    ce = ConsensusEngine(threshold=req.threshold)
    for v in req.votes:
        ce.record_vote(req.proposal_id, v.voter, v.choice)
    total = req.total_nodes or len(req.votes)
    agreed = ce.check_consensus(req.proposal_id, total) if total else None
    return {"reached": agreed is not None, "choice": agreed, "threshold": req.threshold,
            "total_nodes": total, "votes_cast": len(req.votes),
            "method": "threshold consensus (owned swarm)"}


class RigorRequest(BaseModel):
    metric_name: str
    value: float
    baseline: float = 0.0


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
    """Owned statistical-rigor capability (agentic_core/statistics.LiveRigorMonitor): REAL scipy 95% CI
    + one-sample t-test (p-value) + power-gated significance over a live metric series — not a fabricated
    confidence. Each validation is sealed into the owned UEG provenance chain."""
    res = await _rigor_monitor().validate_metric(req.metric_name, req.value, req.baseline)
    return {"metric": res["metric"], "value": res["value"], "baseline": res["baseline"],
            "ci_95": [float(res["ci_95"][0]), float(res["ci_95"][1])], "p_value": float(res["p_value"]),
            "power": float(res["power"]), "significant": bool(res["significant"]),
            "method": "scipy CI + one-sample t-test (owned statistics)"}


class ValidateRequest(BaseModel):
    prediction: Any
    actual: Any
    task_type: str = "SEMANTIC"   # SEMANTIC | NUMERICAL | APP_CODE | GENERIC


@router.post("/validate")
async def native_validate(req: ValidateRequest):
    """Owned validation capability (agentic_core/validation.AccuracyValidator): real difflib semantic
    similarity / numerical-tolerance / code-presence checks against a REFERENCE — not LLM self-grading."""
    from agentic_core.validation.accuracy_validator import AccuracyValidator
    res = AccuracyValidator().validate_output(req.prediction, req.actual, task_type=req.task_type)
    return {"is_accurate": bool(res["is_accurate"]), "confidence": float(res["confidence"]),
            "task_type": res["task_type"], "method": "agentic_core/validation.AccuracyValidator (difflib, real)"}


class DecideRequest(BaseModel):
    state: Dict[str, Any] = {}
    actions: List[str] = []


@router.post("/decide")
async def native_decide(req: DecideRequest):
    """In-house minimax (maximin) decision over candidate actions under worst-case stressors — the OWNED
    cognition decision capability (agentic_core/cognition). Real game-theory, not LLM text. Uses the
    survival-utility default when no custom utility is provided."""
    from agentic_core.cognition.minimax_optimizer import MinimaxOptimizer, default_utility_func
    actions = req.actions or ["proceed", "refine", "hold"]
    state = req.state or {"base_stability": 0.9}
    res = MinimaxOptimizer().evaluate_strategy(state, actions, default_utility_func)
    return {"posture": "in-house", "method": "minimax adversarial (owned cognition)",
            "actions": actions, **res}


@router.post("/tree")
async def native_tree(req: TreeRequest):
    """Autonomous workflow-TREE orchestration: the native swarm decomposes the goal into a dependency
    tree and runs it in-house-first with PARALLEL branches — the living-organism cascade (immune-throttled
    parallelism + biobus signals + learning loop). Every node reports the OWNED resource that served it."""
    return await orchestrator.orchestrate_tree(
        req.goal, context=req.context, max_parallel=req.max_parallel,
        prefer_external=req.prefer_external, timeout=req.timeout)
