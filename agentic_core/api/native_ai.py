"""
Native AI Fabric API — Workstation's OWN AI resources, exposed.

Surfaces the in-house AI control plane (W1): the model-resource registry (owned native
engine + self-hosted local model + optional external accelerants), the orchestrator
(in-house-first completion), and the swarm engine (bespoke, reusable agent-cascade trees).
Everything is honest about which resource served and whether any external provider was used.
"""
from __future__ import annotations

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
    return {
        "posture": "in-house-first",
        "external_allowed": external_allowed(),
        "owned_resources_available": [r["name"] for r in owned],
        "selection_order": registry.select(),
        "guarantee": "Workstation always produces a real, structured result from its OWN resources "
                     "with NO external dependency; external providers are optional accelerants "
                     "(flag-gated by AI_ALLOW_EXTERNAL).",
        "resources": resources,
    }


@router.get("/resources")
async def native_resources():
    return {"resources": registry.available(), "selection_order": registry.select()}


class CompleteRequest(BaseModel):
    prompt: str
    agent: str = "assistant"
    prefer_external: bool = False
    timeout: float = 30.0


@router.post("/complete")
async def native_complete(req: CompleteRequest):
    res = await orchestrator.complete(req.prompt, agent=req.agent,
                                      timeout=req.timeout, prefer_external=req.prefer_external)
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
