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
